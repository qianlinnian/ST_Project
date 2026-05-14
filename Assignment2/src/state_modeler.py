from __future__ import annotations

from typing import Any

import pandas as pd

from src.oracle_generator import generate_expected_result


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
                "technique_standard": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 state transition testing",
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
