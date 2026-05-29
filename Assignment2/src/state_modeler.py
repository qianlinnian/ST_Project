from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion
from src.oracle_generator import generate_expected_result
from src.prompt_templates import (
    STATE_MODEL_IMPROVEMENT_SYSTEM,
    state_model_improvement_prompt,
)


DEFAULT_GENERIC_STATE_MODEL = {
    "states": ["Initial State", "Active State", "Completed State", "Error/Rejected State"],
    "transitions": [
        {
            "transition_id": "TR-001",
            "source_state": "Initial State",
            "event": "submit valid action or input",
            "target_state": "Active State",
            "guard": "Input or action satisfies the requirement constraints",
            "test_data": "Representative valid data",
        },
        {
            "transition_id": "TR-002",
            "source_state": "Initial State",
            "event": "submit invalid action or input",
            "target_state": "Error/Rejected State",
            "guard": "Input or action violates a requirement constraint",
            "test_data": "Representative invalid data",
        },
        {
            "transition_id": "TR-003",
            "source_state": "Active State",
            "event": "complete the primary workflow action",
            "target_state": "Completed State",
            "guard": "The entity or workflow is active and can be completed",
            "test_data": "Valid completion action",
        },
    ],
}


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value or "")


def _state_model_focus_frame(structured_requirements: pd.DataFrame) -> pd.DataFrame:
    if structured_requirements.empty:
        return structured_requirements

    lifecycle_keywords = {
        "add",
        "create",
        "update",
        "edit",
        "save",
        "delete",
        "remove",
        "complete",
        "completed",
        "toggle",
        "cancel",
        "escape",
        "reject",
        "persist",
        "reload",
        "restart",
    }
    context_keywords = {
        "filter",
        "view",
        "list exists",
        "page",
        "screen",
        "display",
        "show",
        "navigate",
    }

    scored_rows: list[tuple[int, int, dict[str, Any]]] = []
    for index, (_, row) in enumerate(structured_requirements.iterrows()):
        actions = _as_text(row.get("actions", "")).lower()
        conditions = _as_text(row.get("conditions", "")).lower()
        expected = _as_text(row.get("expected_results", "")).lower()
        requirement = _as_text(row.get("requirement_text", "")).lower()
        combined = " | ".join([actions, conditions, expected, requirement])

        positive = sum(1 for keyword in lifecycle_keywords if keyword in combined)
        negative = sum(1 for keyword in context_keywords if keyword in combined)
        score = positive - negative
        scored_rows.append((score, index, row.to_dict()))

    prioritized = [item for item in scored_rows if item[0] > 0]
    if len(prioritized) < max(3, min(6, len(scored_rows))):
        prioritized = sorted(scored_rows, key=lambda item: (item[0], -item[1]), reverse=True)
    else:
        prioritized = sorted(prioritized, key=lambda item: (item[0], -item[1]), reverse=True)

    selected_count = min(len(prioritized), max(4, min(10, len(scored_rows))))
    selected = prioritized[:selected_count]
    selected_indexes = sorted(item[1] for item in selected)
    return structured_requirements.iloc[selected_indexes].reset_index(drop=True)


def build_state_model(
    states: list[str] | None = None,
    transitions: list[dict] | None = None,
) -> dict:
    selected_states = states or DEFAULT_GENERIC_STATE_MODEL["states"]
    selected_transitions = transitions or DEFAULT_GENERIC_STATE_MODEL["transitions"]
    return {
        "states": selected_states,
        "transitions": [
            (
                transition.get("source_state", ""),
                transition.get("target_state", ""),
                transition.get("event", ""),
            )
            for transition in selected_transitions
        ],
        "transition_details": selected_transitions,
    }


def _transition_identity(transition: dict) -> tuple[str, str, str]:
    return (
        transition.get("source_state", ""),
        transition.get("event", ""),
        transition.get("target_state", ""),
    )


def _dedupe_transitions(transitions: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for transition in transitions:
        identity = _transition_identity(transition)
        if identity in seen:
            continue
        seen.add(identity)
        unique.append(transition)
    return unique


def _selected_transitions_for_coverage(model: dict, coverage_goal: str) -> list[dict]:
    transitions = _dedupe_transitions(model.get("transition_details", []))
    if coverage_goal == "All States":
        covered_states = {"Initial State"}
        selected = []
        for transition in transitions:
            target = transition.get("target_state", "")
            if target and target not in covered_states:
                selected.append(transition)
                covered_states.add(target)
        return selected
    return transitions


def _order_transitions_with_resets(transitions: list[dict]) -> list[tuple[bool, dict]]:
    if not transitions:
        return []

    remaining = transitions.copy()
    current_state = "Initial State"
    ordered = []

    while remaining:
        next_index = next(
            (
                index
                for index, transition in enumerate(remaining)
                if transition.get("source_state") == current_state
            ),
            None,
        )
        reset_required = next_index is None
        if reset_required:
            current_state = "Initial State"
            next_index = next(
                (
                    index
                    for index, transition in enumerate(remaining)
                    if transition.get("source_state") == current_state
                ),
                0,
            )

        transition = remaining.pop(next_index)
        ordered.append((reset_required, transition))
        current_state = transition.get("target_state", current_state)

    return ordered


def infer_state_model_from_requirements(structured_requirements: pd.DataFrame) -> dict:
    if structured_requirements.empty:
        return build_state_model()

    states = ["Initial State"]
    transitions = []
    counter = 1

    for _, row in structured_requirements.iterrows():
        req_text = _as_text(row.get("requirement_text", ""))
        actions = row.get("actions", [])
        conditions = row.get("conditions", [])
        expected_results = row.get("expected_results", [])
        action_text = _as_text(actions) or req_text or "perform requirement action"
        condition_text = _as_text(conditions) or "Requirement preconditions are satisfied"
        expected_text = _as_text(expected_results) or "Expected requirement outcome is reached"
        target_state = f"Postcondition for {row.get('requirement_id', counter)}"
        if target_state not in states:
            states.append(target_state)
        transitions.append(
            {
                "transition_id": f"TR-{counter:03d}",
                "source_state": "Initial State",
                "event": action_text,
                "target_state": target_state,
                "guard": condition_text,
                "test_data": expected_text,
            }
        )
        counter += 1

    if len(transitions) < 2:
        fallback = DEFAULT_GENERIC_STATE_MODEL["transitions"][1]
        transitions.append({**fallback, "transition_id": f"TR-{counter:03d}"})
        if fallback["target_state"] not in states:
            states.append(fallback["target_state"])

    return build_state_model(states=states, transitions=transitions)


def improve_state_model_with_llm(
    structured_requirements: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
) -> dict:
    if (
        structured_requirements.empty
        or not use_llm
        or not provider
        or not is_llm_enabled(provider)
    ):
        return infer_state_model_from_requirements(structured_requirements)

    focused_requirements = _state_model_focus_frame(structured_requirements)
    prompt = state_model_improvement_prompt(focused_requirements)
    parsed = call_json_completion(
        STATE_MODEL_IMPROVEMENT_SYSTEM,
        prompt,
        provider=provider,
        model=model,
        max_tokens=1800,
        task_label="State Model Improvement",
    )

    states = parsed.get("states", [])
    transitions = parsed.get("transitions", [])
    if not states or not transitions:
        raise ValueError("LLM returned incomplete state model")

    return build_state_model(states=states, transitions=transitions)


def generate_all_states_sequence(state_model: dict | None = None) -> pd.DataFrame:
    model = state_model or build_state_model()
    rows = []
    for index, state in enumerate(model.get("states", []), start=1):
        rows.append(
            {
                "sequence_id": f"STATE-{index:03d}",
                "coverage_goal": "All States",
                "state": state,
                "precondition": "The system is available and the relevant workflow can be exercised.",
                "steps": f"1. Establish or navigate to the conditions required for state: {state}\n2. Observe the system state",
                "expected_result": f"The system reaches or displays the '{state}' state as defined by the requirements or model.",
            }
        )
    return pd.DataFrame(rows)


def generate_all_transitions_sequence(state_model: dict | None = None) -> pd.DataFrame:
    model = state_model or build_state_model()
    rows = []
    for index, transition in enumerate(model.get("transition_details", []), start=1):
        event = transition.get("event", "perform transition event")
        source = transition.get("source_state", "Initial State")
        target = transition.get("target_state", "Expected Target State")
        test_data = transition.get("test_data", "Representative data for the transition")
        rows.append(
            {
                "sequence_id": f"TRANS-{index:03d}",
                "transition_id": transition.get("transition_id", f"TR-{index:03d}"),
                "coverage_goal": "All Transitions",
                "source_state": source,
                "event": event,
                "guard": transition.get("guard", "Transition preconditions are satisfied"),
                "test_data": test_data,
                "target_state": target,
                "precondition": f"The system is in source state: {source}.",
                "steps": (
                    f"1. Establish source state: {source}\n"
                    f"2. Apply event/action: {event}\n"
                    f"3. Observe the resulting system state"
                ),
                "expected_result": generate_expected_result(
                    technique="State Transition Testing",
                    action=f"{source} --{event}--> {target}",
                    test_data=test_data,
                ),
            }
        )
    return pd.DataFrame(rows)


def generate_optimized_transition_sequence(
    state_model: dict | None = None,
    coverage_goal: str = "All Transitions",
) -> pd.DataFrame:
    model = state_model or build_state_model()
    selected = _selected_transitions_for_coverage(model, coverage_goal)
    ordered = _order_transitions_with_resets(selected)
    rows = []

    for index, (reset_required, transition) in enumerate(ordered, start=1):
        event = transition.get("event", "perform transition event")
        source = transition.get("source_state", "Initial State")
        target = transition.get("target_state", "Expected Target State")
        test_data = transition.get("test_data", "Representative data for the transition")
        reset_step = (
            "1. Reset or navigate the system to the source state\n"
            if reset_required
            else ""
        )
        rows.append(
            {
                "sequence_id": f"OPT-TRANS-{index:03d}",
                "transition_id": transition.get("transition_id", f"TR-{index:03d}"),
                "coverage_goal": coverage_goal,
                "optimization_rule": "Cover each selected state or transition once; reset only when the next transition cannot be chained from the current state.",
                "reset_required": reset_required,
                "source_state": source,
                "event": event,
                "guard": transition.get("guard", "Transition preconditions are satisfied"),
                "test_data": test_data,
                "target_state": target,
                "precondition": f"The system is in source state: {source}.",
                "steps": (
                    f"{reset_step}"
                    f"{'2' if reset_required else '1'}. Establish source state: {source}\n"
                    f"{'3' if reset_required else '2'}. Apply event/action: {event}\n"
                    f"{'4' if reset_required else '3'}. Observe the resulting system state"
                ),
                "expected_result": generate_expected_result(
                    technique="State Transition Testing",
                    action=f"{source} --{event}--> {target}",
                    test_data=test_data,
                ),
            }
        )

    return pd.DataFrame(rows)


def generate_state_transition_tests(
    requirement_id: str = "REQ-STATE-GENERIC",
    coverage_id: str = "COV-STATE-GENERIC",
    start_index: int = 1,
    state_model: dict | None = None,
) -> pd.DataFrame:
    rows = []
    transitions = generate_all_transitions_sequence(state_model)
    for offset, row in transitions.iterrows():
        rows.append(
            {
                "test_case_id": f"TC-ST-{start_index + offset:03d}",
                "requirement_id": requirement_id,
                "coverage_id": coverage_id,
                "technique": "State Transition Testing",
                "precondition": row["precondition"],
                "test_data": row["test_data"],
                "steps": row["steps"],
                "expected_result": row["expected_result"],
                "priority": "High",
                "risk_score": 0.0,
                "risk_level": "Medium",
                "coverage_type": "State Transition",
                "automation_candidate": "Yes",
                "source": "Generic State Model",
                "design_basis": f"{row['source_state']} --{row['event']}--> {row['target_state']}",
            }
        )
    return pd.DataFrame(rows)


def build_todo_state_model() -> dict:
    return build_state_model()
