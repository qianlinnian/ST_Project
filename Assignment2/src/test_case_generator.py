from __future__ import annotations

import json
import re
from typing import Any

import pandas as pd

from src.ai_client import chat_completion, is_llm_enabled
from src.llm_execution import call_json_completion, env_int, repair_json_tail, run_parallel_batches
from src.oracle_generator import generate_expected_result, improve_oracles_with_llm
from src.prompt_templates import (
    COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM,
    TEST_CASE_GENERATION_SYSTEM,
    missing_test_case_prompt,
    test_case_generation_prompt as build_test_case_generation_prompt,
)
from src.state_modeler import (
    describe_state_transition_expected_result,
    generate_state_transition_tests,
    infer_state_model_from_requirements,
    state_sequence_coverage_id,
)
from src.test_suite_designer import assign_test_suites_to_cases

PRIORITY_BY_RISK = {"High": "High", "Medium": "Medium", "Low": "Low"}
RISK_SCORE_BY_LEVEL = {"High": 5.0, "Medium": 3.0, "Low": 1.0}
TECHNIQUE_CASE_LIMITS = {
    "Boundary Value Analysis": 5,
    "Decision Table Testing": 3,
    "Equivalence Partitioning": 3,
    "State Transition Testing": 2,
}
REQUIRED_COLUMNS = [
    "test_case_id", "suite_id", "suite_name", "requirement_id", "coverage_id", "technique",
    "precondition", "test_data", "steps", "expected_result", "priority", "risk_score",
    "risk_level", "suite_risk_level", "suite_priority", "coverage_type", "automation_candidate", "source", "design_basis",
]
GENERIC_TEST_DATA_PATTERNS = (
    "Representative valid partition data derived from the requirement",
    "Representative invalid partition data derived from the requirement",
    "Boundary value: below lower boundary",
    "Boundary value: on lower boundary",
    "Boundary value: above upper boundary",
    "Boundary value: below lower invalid boundary",
    "Transition scenario for:",
)
GENERIC_EXPECTED_PATTERNS = (
    "The system reaches the expected target state after the event, or rejects an invalid transition without corrupting state.",
    "The system accepts the representative valid input or behaviour and produces the requirement-consistent observable output.",
    "The observable result is consistent with the specified boundary rule for the selected boundary value.",
)


def _as_text(value: Any) -> str:
    return ", ".join(str(item) for item in value) if isinstance(value, list) else str(value or "")


def _find_requirement(requirements: pd.DataFrame, requirement_id: str) -> dict:
    if requirements.empty or "requirement_id" not in requirements.columns:
        return {}
    matches = requirements[requirements["requirement_id"] == requirement_id]
    return {} if matches.empty else matches.iloc[0].to_dict()


def _bounds(*texts: str) -> tuple[int | None, int | None]:
    combined = " ".join(texts).lower()
    match = re.search(r"(\d+)\s*(?:-|to|~|–)\s*(\d+)", combined)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return min(a, b), max(a, b)
    min_value = max_value = None
    for number in [int(value) for value in re.findall(r"\b\d+\b", combined)]:
        pos = combined.find(str(number))
        local = combined[max(0, pos - 30): pos + 40]
        if any(k in local for k in ["min", "minimum", "least", "lower"]):
            min_value = number
        if any(k in local for k in ["max", "maximum", "limit", "upper", "no more"]):
            max_value = number
    return min_value, max_value


def _hint(req: dict) -> str:
    expected = req.get("expected_results", "")
    return str(expected[0]) if isinstance(expected, list) and expected else str(expected or "")


def _is_generic_text(value: Any, patterns: tuple[str, ...]) -> bool:
    text = str(value or "").strip()
    return any(pattern in text for pattern in patterns)


def _extract_numbers(text: str) -> list[int]:
    return [int(value) for value in re.findall(r"\b\d+\b", text)]


def _coverage_mentions_empty_after_trim(text: str) -> bool:
    lowered = text.lower()
    return "after trimming becomes empty" in lowered or "after trimming is empty" in lowered or "empty after trim" in lowered


def _coverage_mentions_nonexistent(text: str) -> bool:
    lowered = text.lower()
    return "non-existent" in lowered or "nonexistent" in lowered


def _derive_specific_precondition(cov: dict, req: dict, default: str) -> str:
    description = _as_text(cov.get("description", ""))
    lowered = description.lower()
    if "completed item" in lowered:
        return "A completed todo item exists and is visible in the current list."
    if "escape" in lowered:
        return "A todo item is in edit mode with an unsaved title change."
    if _coverage_mentions_nonexistent(lowered):
        return "The referenced entity does not exist in the current dataset."
    if "mixed statuses" in lowered or "all statuses" in lowered:
        return "The current list contains both active and completed todo items."
    return default


def _derive_specific_test_data(cov: dict, req: dict, current: str, technique: str) -> str:
    description = _as_text(cov.get("description", ""))
    lowered = description.lower()
    if current and not _is_generic_text(current, GENERIC_TEST_DATA_PATTERNS):
        return current
    if "completed item" in lowered:
        return "completed todo item"
    if _coverage_mentions_empty_after_trim(lowered):
        return "newTitle: '   '"
    if "non-empty after trim" in lowered:
        return "newTitle: 'Buy milk'"
    if _coverage_mentions_nonexistent(lowered):
        if "list" in lowered:
            return "non-existent listId"
        if "todo" in lowered or "item" in lowered:
            return "non-existent todoId"
    if "all statuses" in lowered or "mixed statuses" in lowered:
        return "list with active and completed todo items"
    if "100 characters and 101 characters" in lowered:
        return "title length = 100 chars; title length = 101 chars"
    if "whitespace characters of varying lengths" in lowered:
        return "title = ' '; title = 100 spaces; title = 101 spaces"
    if technique == "State Transition Testing":
        return f"Transition scenario for: {description or _as_text(req.get('requirement_text', ''))}"
    return current


def _derive_specific_expected_result(row: dict, cov: dict, req: dict, current: str) -> str:
    description = _as_text(cov.get("description", ""))
    lowered = description.lower()
    requirement_id = str(row.get("requirement_id", "")).strip()
    test_data = str(row.get("test_data", "")).lower()
    design_basis = str(row.get("design_basis", ""))

    if str(row.get("coverage_type", "")).strip().lower() == "state transition":
        target_state = ""
        source_state = ""
        event = ""
        match = re.search(r"^(TR-[^:]+):\s*(.*?)\s*--(.*?)-->\s*(.*?)$", design_basis)
        if match:
            source_state = match.group(2).strip()
            event = match.group(3).strip()
            target_state = match.group(4).strip()
        transition = {
            "source_state": source_state,
            "event": event,
            "target_state": target_state,
            "test_data": row.get("test_data", ""),
            "guard": description,
        }
        return describe_state_transition_expected_result(transition)

    if requirement_id == "REQ-TODO-008" or _coverage_mentions_empty_after_trim(lowered):
        return "The todo item is deleted and removed from the list."
    if requirement_id == "REQ-TODO-009" or "restores original title" in lowered:
        return "Editing is cancelled, edit mode exits, and the original title is restored."
    if "completed item" in lowered and "edit mode" in lowered:
        return "The completed item enters edit mode and the edit field shows its current title."
    if _coverage_mentions_nonexistent(lowered) or "non-existent" in test_data:
        return "The operation is rejected and an appropriate error is shown."
    if "all statuses" in lowered or "mixed statuses" in lowered:
        return "Only items matching the selected filter are displayed."
    if "100 characters and 101 characters" in lowered:
        return "A 100-character title is accepted, and a 101-character title is rejected with an error."
    if "whitespace characters of varying lengths" in lowered:
        return "Whitespace-only titles are trimmed and then rejected or deleted according to the requirement."
    if current and not _is_generic_text(current, GENERIC_EXPECTED_PATTERNS):
        return current
    return generate_expected_result(
        requirement_text=_as_text(req.get("requirement_text", "")),
        test_data=row.get("test_data", ""),
        technique=row.get("technique", ""),
        action=_as_text(cov.get("description", "")),
        expected_hint=_hint(req),
    )


def _align_test_case_semantics(test_cases: pd.DataFrame, coverage: pd.DataFrame, requirements: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases

    normalized = _normalise_test_case_frame(test_cases.copy())
    coverage_lookup = (
        coverage.set_index("coverage_id").to_dict("index")
        if coverage is not None and not coverage.empty and "coverage_id" in coverage.columns
        else {}
    )
    requirement_lookup = (
        requirements.set_index("requirement_id").to_dict("index")
        if requirements is not None and not requirements.empty and "requirement_id" in requirements.columns
        else {}
    )

    for index, row in normalized.iterrows():
        coverage_row = coverage_lookup.get(str(row.get("coverage_id", "")).strip(), {})
        req = requirement_lookup.get(str(row.get("requirement_id", "")).strip(), {})
        description = _as_text(coverage_row.get("description", ""))
        lowered = description.lower()

        if str(row.get("requirement_id", "")).strip() == "REQ-TODO-007" and _coverage_mentions_empty_after_trim(lowered):
            if "REQ-TODO-008" in requirement_lookup:
                normalized.at[index, "requirement_id"] = "REQ-TODO-008"
                req = requirement_lookup["REQ-TODO-008"]

        normalized.at[index, "precondition"] = _derive_specific_precondition(
            coverage_row,
            req,
            str(row.get("precondition", "")),
        )
        normalized.at[index, "test_data"] = _derive_specific_test_data(
            coverage_row,
            req,
            str(row.get("test_data", "")),
            str(row.get("technique", "")),
        )
        row_data = normalized.loc[index].to_dict()
        normalized.at[index, "expected_result"] = _derive_specific_expected_result(
            row_data,
            coverage_row,
            req,
            str(row.get("expected_result", "")),
        )
    return normalized


def _case(idx: int, req_id: str, cov_id: str, tech: str, cov: dict, req: dict, data: str, steps: str,
          expected: str | None = None, source: str = "Rule fallback", basis: str = "") -> dict:
    risk = str(cov.get("risk_level") or "Medium")
    req_text = _as_text(req.get("requirement_text", ""))
    cov_text = _as_text(cov.get("description", ""))
    return {
        "test_case_id": f"TC-{idx:03d}",
        "suite_id": "",
        "suite_name": "",
        "requirement_id": req_id,
        "coverage_id": cov_id,
        "technique": tech,
        "precondition": "The system under test is available and the relevant feature can be exercised.",
        "test_data": data,
        "steps": steps,
        "expected_result": expected or generate_expected_result(req_text, data, tech, cov_text, _hint(req)),
        "priority": PRIORITY_BY_RISK.get(risk, "Medium"),
        "risk_score": RISK_SCORE_BY_LEVEL.get(risk, 3.0),
        "risk_level": risk,
        "suite_risk_level": "",
        "suite_priority": "",
        "coverage_type": cov.get("coverage_type", "Functional"),
        "automation_candidate": "Partial",
        "source": source,
        "design_basis": basis or cov_text or req_text,
    }


def _ep(start: int, req_id: str, cov_id: str, cov: dict, req: dict) -> list[dict]:
    basis = _as_text(cov.get("description", "")) or _as_text(req.get("requirement_text", ""))
    return [
        _case(start, req_id, cov_id, "Equivalence Partitioning", cov, req,
              "Representative valid partition data derived from the requirement",
              "1. Prepare representative valid data\n2. Execute the related action\n3. Observe the system response",
              source="Rule fallback", basis=f"Valid equivalence partition for: {basis}"),
        _case(start + 1, req_id, cov_id, "Equivalence Partitioning", cov, req,
              "Representative invalid partition data derived from the requirement",
              "1. Prepare representative invalid data\n2. Execute the related action\n3. Observe validation, rejection, or safe handling",
              source="Rule fallback", basis=f"Invalid equivalence partition for: {basis}"),
    ]


def _bva(start: int, req_id: str, cov_id: str, cov: dict, req: dict) -> list[dict]:
    coverage_text = _as_text(cov.get("description", ""))
    lowered = coverage_text.lower()
    lo, hi = _bounds(_as_text(req.get("requirement_text", "")), _as_text(req.get("data_ranges", "")), coverage_text)
    values = []
    if "100 characters and 101 characters" in lowered:
        values = [("title length = 100 characters", "valid boundary"), ("title length = 101 characters", "invalid boundary")]
    elif "whitespace characters of varying lengths" in lowered:
        values = [("title = 1 whitespace character", "trimmed empty"), ("title = 100 whitespace characters", "trimmed empty"), ("title = 101 whitespace characters", "trimmed empty")]
    else:
        values += [(str(max(lo - 1, 0)), "just below minimum"), (str(lo), "on minimum"), (str(lo + 1), "just above minimum")] if lo is not None else [("below lower boundary", "generic lower invalid boundary"), ("on lower boundary", "generic lower valid boundary")]
        values += [(str(max(hi - 1, 0)), "just below maximum"), (str(hi), "on maximum"), (str(hi + 1), "just above maximum")] if hi is not None else [("above upper boundary", "generic upper boundary review")]
    rows, seen = [], set()
    for value, label in values:
        if (value, label) in seen:
            continue
        seen.add((value, label))
        rows.append(_case(start + len(rows), req_id, cov_id, "Boundary Value Analysis", cov, req,
                          f"Boundary value: {value} ({label})",
                          "1. Prepare data at the boundary point\n2. Execute the related action\n3. Verify the boundary rule",
                          source="Rule fallback",
                          basis="Values are selected on and around identifiable or inferred boundaries."))
    return rows


def _decision(start: int, req_id: str, cov_id: str, cov: dict, req: dict) -> list[dict]:
    rules = [
        ("All required conditions are true", "The permitted action is completed successfully."),
        ("At least one required condition is false", "The action is rejected or the alternative specified outcome occurs."),
        ("Invalid or conflicting condition combination", "The system handles the combination safely and consistently."),
    ]
    return [_case(start + i, req_id, cov_id, "Decision Table Testing", cov, req,
                  f"Rule {i + 1}: {cond}",
                  "1. Establish the condition combination\n2. Execute the action\n3. Verify the expected outcome",
                  expected=exp, source="Rule fallback",
                  basis=f"Decision rule based on requirement conditions: {cond}") for i, (cond, exp) in enumerate(rules)]


def _state(start: int, req_id: str, cov_id: str, cov: dict, state_model: dict) -> list[dict]:
    basis = _as_text(cov.get("description", "")) or "State transition coverage"
    return [
        _case(
            start,
            req_id,
            cov_id,
            "State Transition Testing",
            cov,
            {},
            f"Transition scenario for: {basis}",
            "1. Establish the source state\n2. Trigger the transition event\n3. Verify the target state",
            source="Rule fallback",
            basis=basis,
        )
    ]


def _state_sequence_cases(start: int, state_sequences: pd.DataFrame) -> list[dict]:
    rows = []
    if state_sequences.empty:
        return rows
    for offset, (_, sequence) in enumerate(state_sequences.iterrows()):
        transition_id = str(sequence.get("transition_id", f"TR-{offset + 1:03d}"))
        source = str(sequence.get("source_state", "Initial State"))
        event = str(sequence.get("event", "perform transition event"))
        target = str(sequence.get("target_state", "Expected Target State"))
        transition = sequence.to_dict()
        rows.append(
            {
                "test_case_id": f"TC-{start + offset:03d}",
                "suite_id": "",
                "suite_name": "",
                "requirement_id": "REQ-STATE-MODEL",
                "coverage_id": _state_sequence_coverage_id(sequence, offset + 1),
                "technique": "State Transition Testing",
                "precondition": sequence.get("precondition", f"The system is in source state: {source}."),
                "test_data": sequence.get("test_data", f"Transition data for {transition_id}"),
                "steps": sequence.get(
                    "steps",
                    f"1. Establish source state: {source}\n2. Apply event/action: {event}\n3. Observe the resulting system state",
                ),
                "expected_result": describe_state_transition_expected_result(transition),
                "priority": "High",
                "risk_score": 3.0,
                "risk_level": "Medium",
                "suite_risk_level": "",
                "suite_priority": "",
                "coverage_type": "State Transition",
                "automation_candidate": "Partial",
                "source": "Rule fallback",
                "design_basis": f"{transition_id}: {source} --{event}--> {target}",
            }
        )
    return rows


def _state_sequence_coverage_id(sequence: pd.Series | dict, offset: int) -> str:
    return state_sequence_coverage_id(sequence, offset)


def _split_suite_coverage_ids(value: Any) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    separator = ";" if ";" in text else ","
    return [part.strip() for part in text.split(separator) if part.strip()]


def _generate_for_coverage(
    counter: int,
    coverage_row: dict,
    requirements: pd.DataFrame,
    strategy_map: dict,
    state_model: dict,
) -> list[dict]:
    req_id = coverage_row.get("requirement_id", "")
    cov_id = coverage_row.get("coverage_id", "")
    req = _find_requirement(requirements, req_id)
    tech = strategy_map.get(cov_id, {}).get("technique", "Equivalence Partitioning")
    generated = (
        _bva(counter, req_id, cov_id, coverage_row, req)
        if tech == "Boundary Value Analysis"
        else _decision(counter, req_id, cov_id, coverage_row, req)
        if tech == "Decision Table Testing"
        else _state(counter, req_id, cov_id, coverage_row, state_model)
        if tech == "State Transition Testing"
        else _ep(counter, req_id, cov_id, coverage_row, req)
    )
    return _limit_cases_for_coverage(generated, tech)


def _suite_driven_fallback(
    requirements: pd.DataFrame,
    coverage: pd.DataFrame,
    strategies: pd.DataFrame,
    test_suites: pd.DataFrame,
    include_state: bool,
    state_transition_sequences: pd.DataFrame | None = None,
) -> pd.DataFrame:
    coverage_map = coverage.set_index("coverage_id").to_dict("index") if not coverage.empty else {}
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}
    state_model = infer_state_model_from_requirements(requirements)
    rows, counter = [], 1

    for _, suite in test_suites.iterrows():
        techniques = str(suite.get("techniques", ""))
        coverage_type = str(suite.get("coverage_types", ""))
        source = str(suite.get("source", ""))
        suite_coverage_ids = _split_suite_coverage_ids(suite.get("coverage_ids", ""))
        is_state_suite = (
            "State Transition Testing" in techniques
            and ("State Transition" in coverage_type or "state transition model" in source.lower())
        )
        if is_state_suite and include_state:
            sequence_frame = (
                state_transition_sequences
                if state_transition_sequences is not None
                else pd.DataFrame()
            )
            matched_sequences = sequence_frame
            if (
                not sequence_frame.empty
                and suite_coverage_ids
                and "coverage_id" in sequence_frame.columns
            ):
                matched_sequences = sequence_frame[
                    sequence_frame["coverage_id"].astype(str).isin(suite_coverage_ids)
                ]
            state_rows = _state_sequence_cases(counter, matched_sequences)
            if state_rows:
                rows.extend(state_rows)
                counter += len(state_rows)
                continue

        for coverage_id in suite_coverage_ids:
            coverage_row = coverage_map.get(coverage_id)
            if not coverage_row:
                continue
            coverage_row = {"coverage_id": coverage_id, **coverage_row}
            generated = _generate_for_coverage(
                counter,
                coverage_row,
                requirements,
                strategy_map,
                state_model,
            )
            rows.extend(generated)
            counter += len(generated)

    return _limit_test_case_volume(pd.DataFrame(rows, columns=REQUIRED_COLUMNS))


def _fallback(
    requirements: pd.DataFrame,
    coverage: pd.DataFrame,
    strategies: pd.DataFrame,
    include_state: bool,
    state_transition_sequences: pd.DataFrame | None = None,
    test_suites: pd.DataFrame | None = None,
) -> pd.DataFrame:
    if test_suites is not None and not test_suites.empty:
        return _suite_driven_fallback(
            requirements,
            coverage,
            strategies,
            test_suites,
            include_state,
            state_transition_sequences=state_transition_sequences,
        )

    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}
    state_model = infer_state_model_from_requirements(requirements)
    rows, counter = [], 1
    for _, cov_row in coverage.iterrows():
        cov = cov_row.to_dict()
        generated = _generate_for_coverage(counter, cov, requirements, strategy_map, state_model)
        rows.extend(generated)
        counter += len(generated)
    if include_state:
        if state_transition_sequences is not None and not state_transition_sequences.empty:
            rows.extend(_state_sequence_cases(counter, state_transition_sequences))
        elif not any(r.get("technique") == "State Transition Testing" for r in rows):
            rows.extend(generate_state_transition_tests(start_index=counter, state_model=state_model).to_dict("records"))
    return _limit_test_case_volume(pd.DataFrame(rows, columns=REQUIRED_COLUMNS))


def _limit_cases_for_coverage(rows: list[dict], technique: str) -> list[dict]:
    if not rows:
        return rows
    default_limit = TECHNIQUE_CASE_LIMITS.get(str(technique), 2)
    max_per_coverage = env_int("AUTOTESTDESIGN_MAX_TEST_CASES_PER_COVERAGE", 6, 1, 40)
    return rows[: min(default_limit, max_per_coverage)]


def _limit_test_case_volume(test_cases: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases

    data = _normalise_test_case_frame(test_cases)
    max_per_coverage = env_int("AUTOTESTDESIGN_MAX_TEST_CASES_PER_COVERAGE", 6, 1, 40)
    max_total = env_int("AUTOTESTDESIGN_MAX_GENERATED_TEST_CASES", 1500, 1, 20000)

    limited_groups = []
    group_key = "coverage_id" if "coverage_id" in data.columns else None
    if group_key:
        for _, group in data.groupby(group_key, sort=False):
            technique = str(group.iloc[0].get("technique", ""))
            technique_limit = TECHNIQUE_CASE_LIMITS.get(technique, max_per_coverage)
            limited_groups.append(group.head(min(technique_limit, max_per_coverage)))
        data = pd.concat(limited_groups, ignore_index=True) if limited_groups else data

    if len(data) <= max_total:
        return data.reset_index(drop=True)

    first_per_coverage = data.drop_duplicates(subset=[group_key], keep="first") if group_key else data.head(0)
    first_per_coverage = _sort_by_execution_value(first_per_coverage)
    if len(first_per_coverage) >= max_total:
        return first_per_coverage.head(max_total).reset_index(drop=True)

    used_indexes = set(first_per_coverage.index)
    remaining = data.loc[[idx for idx in data.index if idx not in used_indexes]]
    remaining = _sort_by_execution_value(remaining)
    selected = pd.concat(
        [first_per_coverage, remaining.head(max_total - len(first_per_coverage))],
        ignore_index=True,
    )
    return selected.reset_index(drop=True)


def _sort_by_execution_value(test_cases: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases
    data = test_cases.copy()
    data["_priority_order"] = data.get("priority", "Medium").map({"High": 0, "Medium": 1, "Low": 2}).fillna(3)
    data["_risk_level_order"] = data.get("risk_level", "Medium").map({"High": 0, "Medium": 1, "Low": 2}).fillna(3)
    data["_risk_score_order"] = pd.to_numeric(data.get("risk_score", 0), errors="coerce").fillna(0)
    return data.sort_values(
        ["_priority_order", "_risk_level_order", "_risk_score_order"],
        ascending=[True, True, False],
    ).drop(columns=["_priority_order", "_risk_level_order", "_risk_score_order"])


def _normalise_test_case_frame(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    for col in REQUIRED_COLUMNS:
        if col not in data.columns:
            data[col] = ""
    extra_columns = [col for col in data.columns if col not in REQUIRED_COLUMNS]
    return data[REQUIRED_COLUMNS + extra_columns]


def _renumber_test_cases(test_cases: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases
    renumbered = test_cases.copy()
    renumbered["test_case_id"] = [f"TC-{index:03d}" for index in range(1, len(renumbered) + 1)]
    return renumbered


def _llm_generate(
    requirements: pd.DataFrame,
    coverage: pd.DataFrame,
    strategies: pd.DataFrame,
    provider: str,
    model: str | None,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    coverage_records = coverage.to_dict("records")
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}

    def generate_batch(_batch_index: int, batch: list[dict]) -> pd.DataFrame:
        batch_coverage = pd.DataFrame(batch)
        requirement_ids = {
            str(row.get("requirement_id", ""))
            for row in batch
            if str(row.get("requirement_id", "")).strip()
        }
        batch_requirements = requirements[
            requirements["requirement_id"].astype(str).isin(requirement_ids)
        ] if "requirement_id" in requirements.columns else requirements
        batch_strategies = pd.DataFrame(
            [
                {"coverage_id": row.get("coverage_id"), **strategy_map.get(row.get("coverage_id"), {})}
                for row in batch
            ]
        )
        prompt = build_test_case_generation_prompt(
            batch_requirements.to_string(index=False),
            batch_coverage.to_string(index=False),
            batch_strategies.to_string(index=False),
        )
        parsed = call_json_completion(
            TEST_CASE_GENERATION_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=max(1200, 450 * len(batch)),
            task_label="Test Case Generation",
        )
        data = _normalise_test_case_frame(pd.DataFrame(parsed.get("test_cases", [])))
        if data.empty:
            raise ValueError("LLM returned no test_cases")
        return _align_test_case_semantics(data, batch_coverage, batch_requirements)

    def fallback_batch(_batch_index: int, batch: list[dict], exc: Exception) -> pd.DataFrame:
        batch_coverage = pd.DataFrame(batch)
        batch_cases = _fallback(requirements, batch_coverage, strategies, include_state=False)
        batch_cases["llm_error"] = str(exc)
        batch_cases["source"] = batch_cases["source"].astype(str) + " after LLM batch fallback"
        return batch_cases

    generated_batches, _ = run_parallel_batches(
        coverage_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=generate_batch,
        fallback_batch=fallback_batch,
        task_label="Test Case Generation",
    )
    data = pd.concat(generated_batches, ignore_index=True) if generated_batches else pd.DataFrame()
    data = _normalise_test_case_frame(data)
    if data.empty:
        raise ValueError("LLM returned no test_cases")
    return _renumber_test_cases(_limit_test_case_volume(_align_test_case_semantics(data, coverage, requirements)))


def suggest_missing_test_cases_with_llm(
    requirements: pd.DataFrame,
    coverage: pd.DataFrame,
    strategies: pd.DataFrame,
    existing_test_cases: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    if (
        coverage.empty
        or existing_test_cases.empty
        or not use_llm
        or not provider
        or not is_llm_enabled(provider)
    ):
        return pd.DataFrame(columns=REQUIRED_COLUMNS + ["llm_reason"])

    coverage_records = coverage.to_dict("records")
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}

    def review_batch(_batch_index: int, batch: list[dict]) -> pd.DataFrame:
        prompt = missing_test_case_prompt(batch, requirements, strategy_map, existing_test_cases)
        response_text = chat_completion(
            COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=min(1800, max(700, 120 * len(batch) + 300)),
            task_label="Candidate Test Case Improvement",
        )
        return _parse_missing_test_case_response(response_text, len(batch))

    def fallback_batch(_batch_index: int, _batch: list[dict], exc: Exception) -> pd.DataFrame:
        return pd.DataFrame([{"llm_error": str(exc)}])

    suggested_batches, _ = run_parallel_batches(
        coverage_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=review_batch,
        fallback_batch=fallback_batch,
        task_label="Candidate Test Case Improvement",
    )
    data = pd.concat(suggested_batches, ignore_index=True) if suggested_batches else pd.DataFrame()
    if data.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS + ["llm_reason"])
    for col in REQUIRED_COLUMNS:
        if col not in data.columns:
            data[col] = ""
    return data[REQUIRED_COLUMNS + [col for col in data.columns if col not in REQUIRED_COLUMNS]]


def _parse_missing_test_cases(parsed: dict, batch_size: int) -> pd.DataFrame:
    rows = []
    if isinstance(parsed.get("m"), list):
        items = parsed.get("m", [])
        max_items = env_int("AUTOTESTDESIGN_MAX_MISSING_TEST_CASES_PER_BATCH", 12, 1, 80)
        if len(items) > max_items:
            print(
                "[AutoTestDesign][TestCase][LIMIT] "
                f"selected best {max_items} of {len(items)} LLM missing test cases for this batch",
                flush=True,
            )
        for index, item in enumerate(_select_missing_case_items(items, max_items), start=1):
            parsed_item = _parse_compact_missing_case_item(item)
            if not parsed_item:
                continue
            risk_level = str(parsed_item.get("risk_level", "Medium") or "Medium")
            target_test_case_id = str(parsed_item.get("test_case_id", "")).strip()
            rows.append(
                {
                    "test_case_id": target_test_case_id,
                    "requirement_id": parsed_item.get("requirement_id", ""),
                    "coverage_id": parsed_item.get("coverage_id", ""),
                    "technique": parsed_item.get("technique", ""),
                    "coverage_type": parsed_item.get("coverage_type", ""),
                    "precondition": "The system under test is available and the relevant feature can be exercised.",
                    "test_data": parsed_item.get("test_data", ""),
                    "steps": parsed_item.get("steps", ""),
                    "expected_result": parsed_item.get("expected_result", ""),
                    "priority": parsed_item.get("priority", risk_level),
                    "risk_score": RISK_SCORE_BY_LEVEL.get(risk_level, 3.0),
                    "risk_level": risk_level,
                    "automation_candidate": "Partial",
                    "source": "LLM updated" if target_test_case_id else "LLM added",
                    "design_basis": (
                        "LLM revised an existing weak test case."
                        if target_test_case_id
                        else "LLM identified missing coverage in existing test cases."
                    ),
                    "llm_reason": parsed_item.get("reason", ""),
                }
            )
    return pd.DataFrame(rows)


def _parse_compact_missing_case_item(item: Any) -> dict[str, str] | None:
    if not isinstance(item, list) or len(item) < 7:
        return None

    values = [str(part or "").strip() for part in item]
    first = values[0] if values else ""
    second = values[1] if len(values) > 1 else ""
    third = values[2] if len(values) > 2 else ""

    # New format: [test_case_id_or_empty, req, cov, technique, ...]
    if len(values) >= 11 and second.startswith("REQ") and third.startswith("COV"):
        return {
            "test_case_id": first if first.startswith("TC-") else "",
            "requirement_id": second,
            "coverage_id": third,
            "technique": values[3],
            "coverage_type": values[4],
            "test_data": values[5],
            "steps": values[6],
            "expected_result": values[7],
            "priority": values[8] if len(values) > 8 else "Medium",
            "risk_level": values[9] if len(values) > 9 else "Medium",
            "reason": values[10] if len(values) > 10 else "",
        }

    # Drifted variant: [req, test_case_id, cov, technique, ...]
    if len(values) >= 11 and first.startswith("REQ") and second.startswith("TC-") and third.startswith("COV"):
        return {
            "test_case_id": second,
            "requirement_id": first,
            "coverage_id": third,
            "technique": values[3],
            "coverage_type": values[4],
            "test_data": values[5],
            "steps": values[6],
            "expected_result": values[7],
            "priority": values[8] if len(values) > 8 else "Medium",
            "risk_level": values[9] if len(values) > 9 else "Medium",
            "reason": values[10] if len(values) > 10 else "",
        }

    # Old format: [req, cov, technique, coverage_type, ...]
    if first.startswith("REQ") and second.startswith("COV"):
        return {
            "test_case_id": "",
            "requirement_id": first,
            "coverage_id": second,
            "technique": values[2] if len(values) > 2 else "",
            "coverage_type": values[3] if len(values) > 3 else "",
            "test_data": values[4] if len(values) > 4 else "",
            "steps": values[5] if len(values) > 5 else "",
            "expected_result": values[6] if len(values) > 6 else "",
            "priority": values[7] if len(values) > 7 else "Medium",
            "risk_level": values[8] if len(values) > 8 else "Medium",
            "reason": values[9] if len(values) > 9 else "",
        }

    return None


def _select_missing_case_items(items: list, max_items: int) -> list:
    valid_items = [item for item in items if isinstance(item, list) and len(item) >= 6]
    if len(valid_items) <= max_items:
        return valid_items

    selected = []
    seen_coverage = set()
    for item in sorted(valid_items, key=_missing_case_score, reverse=True):
        coverage_id = str(item[1])
        if coverage_id in seen_coverage and len(seen_coverage) < max_items:
            continue
        selected.append(item)
        seen_coverage.add(coverage_id)
        if len(selected) >= max_items:
            return selected

    selected_keys = {id(item) for item in selected}
    for item in sorted(valid_items, key=_missing_case_score, reverse=True):
        if id(item) in selected_keys:
            continue
        selected.append(item)
        if len(selected) >= max_items:
            break
    return selected


def _missing_case_score(item: list) -> tuple[int, int, int]:
    has_target_id = len(item) >= 11
    base_index = 1 if has_target_id else 0
    technique = str(item[base_index + 2] if len(item) > base_index + 2 else "")
    priority = str(item[base_index + 7] if len(item) > base_index + 7 else "Medium")
    risk_level = str(item[base_index + 8] if len(item) > base_index + 8 else "Medium")
    risk_score = {"High": 3, "Medium": 2, "Low": 1}.get(risk_level, 0)
    priority_score = {"High": 3, "Medium": 2, "Low": 1}.get(priority, 0)
    technique_score = 2 if technique in {"Boundary Value Analysis", "State Transition Testing"} else 1
    return risk_score, priority_score, technique_score


def limit_generated_test_case_volume(test_cases: pd.DataFrame) -> pd.DataFrame:
    return _limit_test_case_volume(test_cases)


def _parse_missing_test_case_response(text: str, batch_size: int) -> pd.DataFrame:
    try:
        return _parse_missing_test_cases(_quiet_clean_json(text), batch_size)
    except Exception as exc:
        items = _extract_complete_missing_case_items(text)
        if not items:
            raise exc
        print(
            "[AutoTestDesign][TestCase][JSON_REPAIR] "
            f"extracted {len(items)} complete missing test cases from truncated response",
            flush=True,
        )
        return _parse_missing_test_cases({"m": items}, batch_size)


def _quiet_clean_json(text: str) -> dict:
    cleaned = str(text or "").strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    for candidate in _json_candidates(cleaned):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass
        try:
            return json.loads(repair_json_tail(candidate))
        except json.JSONDecodeError:
            pass
    return json.loads(cleaned)


def _json_candidates(cleaned: str) -> list[str]:
    candidates = [cleaned]
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidates.append(cleaned[start : end + 1])
    return candidates


def _extract_complete_missing_case_items(text: str) -> list[list]:
    decoder = json.JSONDecoder()
    items = []
    seen = set()
    raw = str(text or "")
    for index, char in enumerate(raw):
        if char != "[":
            continue
        try:
            value, _ = decoder.raw_decode(raw[index:])
        except json.JSONDecodeError:
            continue
        if not _looks_like_compact_missing_case(value):
            continue
        key = tuple(str(part) for part in value[:4])
        if key in seen:
            continue
        seen.add(key)
        items.append(value)
    return items


def _looks_like_compact_missing_case(value: Any) -> bool:
    if (
        isinstance(value, list)
        and len(value) >= 11
        and all(not isinstance(part, (list, dict)) for part in value[:11])
        and str(value[1]).startswith("REQ")
        and str(value[2]).startswith("COV")
    ):
        return True
    return (
        isinstance(value, list)
        and len(value) >= 7
        and all(not isinstance(part, (list, dict)) for part in value[:7])
        and str(value[0]).startswith("REQ")
        and str(value[1]).startswith("COV")
    )


def renumber_test_case_ids(test_cases: pd.DataFrame, prefix: str = "TC") -> pd.DataFrame:
    if test_cases.empty:
        return test_cases.copy()
    renumbered = test_cases.copy()
    renumbered["test_case_id"] = [
        f"{prefix}-{index:03d}" for index in range(1, len(renumbered) + 1)
    ]
    return renumbered


def generate_test_cases(requirements: pd.DataFrame, coverage: pd.DataFrame, strategies: pd.DataFrame,
                        test_suites: pd.DataFrame | None = None,
                        state_transition_sequences: pd.DataFrame | None = None,
                        include_state_tests: bool = True, provider: str | None = None,
                        model: str | None = None, use_llm: bool = True,
                        batch_size: int | None = None,
                        concurrency: int | None = None) -> pd.DataFrame:
    if use_llm and provider and is_llm_enabled(provider):
        try:
            generated = _llm_generate(
                requirements,
                coverage,
                strategies,
                provider,
                model,
                batch_size=batch_size,
                concurrency=concurrency,
            )
            reviewed = improve_oracles_with_llm(
                assign_test_suites_to_cases(generated, test_suites) if test_suites is not None else generated,
                provider=provider,
                model=model,
                use_llm=True,
                batch_size=batch_size,
                concurrency=concurrency,
            )
            return renumber_test_case_ids(_align_test_case_semantics(reviewed, coverage, requirements))
        except Exception as exc:
            fallback = _fallback(
                requirements,
                coverage,
                strategies,
                include_state_tests,
                state_transition_sequences=state_transition_sequences,
                test_suites=test_suites,
            )
            if test_suites is not None:
                fallback = assign_test_suites_to_cases(fallback, test_suites)
            fallback["llm_error"] = str(exc)
            fallback["source"] = "Rule fallback"
            return renumber_test_case_ids(_align_test_case_semantics(fallback, coverage, requirements))
    generated = _fallback(
        requirements,
        coverage,
        strategies,
        include_state_tests,
        state_transition_sequences=state_transition_sequences,
        test_suites=test_suites,
    )
    assigned = (
        assign_test_suites_to_cases(generated, test_suites)
        if test_suites is not None
        else generated
    )
    return renumber_test_case_ids(_align_test_case_semantics(assigned, coverage, requirements))
