from __future__ import annotations

import re
from typing import Any

import pandas as pd

from src.oracle_generator import generate_expected_result
from src.state_modeler import generate_state_transition_tests
from src.test_strategy_selector import TECHNIQUE_STANDARDS


PRIORITY_BY_RISK = {"High": "High", "Medium": "Medium", "Low": "Low"}
RISK_SCORE_BY_LEVEL = {"High": 5.0, "Medium": 3.0, "Low": 1.0}


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value or "")


def _find_requirement(structured_requirements: pd.DataFrame, requirement_id: str) -> dict:
    if structured_requirements.empty or "requirement_id" not in structured_requirements.columns:
        return {}
    matches = structured_requirements[structured_requirements["requirement_id"] == requirement_id]
    if matches.empty:
        return {}
    return matches.iloc[0].to_dict()


def _extract_length_bounds(*texts: str) -> tuple[int | None, int | None]:
    combined = " ".join(texts).lower()
    numbers = [int(value) for value in re.findall(r"\b\d+\b", combined)]
    min_value = None
    max_value = None

    range_match = re.search(r"(\d+)\s*(?:-|to|~|–)\s*(\d+)", combined)
    if range_match:
        first, second = int(range_match.group(1)), int(range_match.group(2))
        return min(first, second), max(first, second)

    for number in numbers:
        local = combined[max(0, combined.find(str(number)) - 25) : combined.find(str(number)) + 35]
        if any(word in local for word in ["min", "minimum", "least", "at least"]):
            min_value = number
        if any(word in local for word in ["max", "maximum", "limit", "up to", "no more", "less than"]):
            max_value = number

    if max_value is None and numbers and any(word in combined for word in ["length", "character", "char", "limit"]):
        max_value = max(numbers)
    return min_value, max_value


def _make_id(counter: int) -> str:
    return f"TC-{counter:03d}"


def _base_case(
    counter: int,
    requirement_id: str,
    coverage_id: str,
    technique: str,
    coverage: dict,
    requirement: dict,
    test_data: str,
    steps: str,
    expected_result: str | None = None,
    precondition: str = "TodoList page is open and ready for user interaction.",
    source: str | None = None,
    design_basis: str = "",
) -> dict:
    risk_level = str(coverage.get("risk_level") or "Medium")
    return {
        "test_case_id": _make_id(counter),
        "requirement_id": requirement_id,
        "coverage_id": coverage_id,
        "technique": technique,
        "technique_standard": TECHNIQUE_STANDARDS.get(technique, "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4"),
        "precondition": precondition,
        "test_data": test_data,
        "steps": steps,
        "expected_result": expected_result
        or generate_expected_result(
            requirement_text=_as_text(requirement.get("requirement_text", "")),
            test_data=test_data,
            technique=technique,
            action=_as_text(coverage.get("description", "")),
            expected_hint=_first_expected_hint(requirement),
        ),
        "priority": PRIORITY_BY_RISK.get(risk_level, "Medium"),
        "risk_score": RISK_SCORE_BY_LEVEL.get(risk_level, 3.0),
        "risk_level": risk_level,
        "coverage_type": coverage.get("coverage_type", "Functional"),
        "automation_candidate": "Yes",
        "source": source or technique,
        "design_basis": design_basis or _as_text(coverage.get("description", "")),
    }


def _first_expected_hint(requirement: dict) -> str:
    expected = requirement.get("expected_results", "")
    if isinstance(expected, list) and expected:
        return str(expected[0])
    return str(expected or "")


def _ep_cases(counter: int, requirement_id: str, coverage_id: str, coverage: dict, requirement: dict) -> list[dict]:
    description = _as_text(coverage.get("description", ""))
    return [
        _base_case(
            counter,
            requirement_id,
            coverage_id,
            "Equivalence Partitioning",
            coverage,
            requirement,
            "Valid partition: non-empty Todo text such as 'Buy milk'",
            "1. Enter a representative valid Todo text\n2. Submit the Todo\n3. Observe the Todo list",
            source="EP valid partition",
            design_basis=f"Valid equivalence partition for {description}",
        ),
        _base_case(
            counter + 1,
            requirement_id,
            coverage_id,
            "Equivalence Partitioning",
            coverage,
            requirement,
            "Invalid partition: empty string or whitespace-only Todo text",
            "1. Enter an empty or whitespace-only Todo text\n2. Submit the Todo\n3. Observe validation and list state",
            source="EP invalid partition",
            design_basis=f"Invalid equivalence partition for {description}",
        ),
    ]


def _bva_cases(counter: int, requirement_id: str, coverage_id: str, coverage: dict, requirement: dict) -> list[dict]:
    text_sources = [
        _as_text(requirement.get("requirement_text", "")),
        _as_text(requirement.get("data_ranges", "")),
        _as_text(requirement.get("conditions", "")),
        _as_text(coverage.get("description", "")),
    ]
    min_value, max_value = _extract_length_bounds(*text_sources)
    cases = []
    next_id = counter

    if min_value is not None:
        values = [
            (max(min_value - 1, 0), "below minimum boundary"),
            (min_value, "on minimum boundary"),
            (min_value + 1, "just above minimum boundary"),
        ]
    else:
        values = [(0, "generic lower invalid boundary"), (1, "generic lower valid boundary")]

    if max_value is not None:
        values.extend(
            [
                (max(max_value - 1, 0), "just below maximum boundary"),
                (max_value, "on maximum boundary"),
                (max_value + 1, "above maximum boundary"),
            ]
        )
    else:
        values.append(("stated maximum not available", "generic upper boundary review"))

    seen = set()
    for value, label in values:
        key = (str(value), label)
        if key in seen:
            continue
        seen.add(key)
        if isinstance(value, int):
            test_data = f"Todo text length = {value} characters ({label})"
        else:
            test_data = f"{value} ({label}; derived from available requirement text)"
        cases.append(
            _base_case(
                next_id,
                requirement_id,
                coverage_id,
                "Boundary Value Analysis",
                coverage,
                requirement,
                test_data,
                "1. Prepare Todo text with the specified boundary length\n2. Submit the Todo\n3. Observe validation and list state",
                source="BVA boundary set",
                design_basis="Boundary values are selected at, just below, and just above identifiable input limits.",
            )
        )
        next_id += 1
    return cases


def _decision_table_cases(counter: int, requirement_id: str, coverage_id: str, coverage: dict, requirement: dict) -> list[dict]:
    rules = [
        ("Todo exists = Yes; Todo completed = No; Action = Delete", "The active Todo is removed from the list."),
        ("Todo exists = Yes; Todo completed = Yes; Action = Delete", "The completed Todo is removed from the list."),
        ("Todo exists = No; Todo completed = N/A; Action = Delete", "No Todo is removed and the list state remains consistent."),
        ("Todo exists = Yes; Todo completed = No; Action = Mark complete", "The Todo changes from active to completed."),
    ]
    cases = []
    for offset, (test_data, expected) in enumerate(rules):
        cases.append(
            _base_case(
                counter + offset,
                requirement_id,
                coverage_id,
                "Decision Table Testing",
                coverage,
                requirement,
                test_data,
                "1. Establish the condition combination in the decision table\n2. Execute the specified action\n3. Compare the actual result with the expected action outcome",
                expected_result=expected,
                source="Decision table rule",
                design_basis=f"Rule {offset + 1}: {test_data}",
            )
        )
    return cases


def _state_cases(counter: int, requirement_id: str, coverage_id: str, coverage: dict) -> list[dict]:
    state_tests = generate_state_transition_tests(requirement_id, coverage_id, counter)
    rows = state_tests.to_dict("records")
    for row in rows:
        row["coverage_type"] = coverage.get("coverage_type", "State Transition")
        row["risk_level"] = coverage.get("risk_level", row.get("risk_level", "Medium"))
        row["priority"] = PRIORITY_BY_RISK.get(row["risk_level"], row.get("priority", "High"))
        row["risk_score"] = RISK_SCORE_BY_LEVEL.get(row["risk_level"], row.get("risk_score", 3.0))
    return rows


def generate_test_cases(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
    include_state_tests: bool = True,
) -> pd.DataFrame:
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}
    rows: list[dict] = []
    counter = 1

    for _, coverage_row in coverage_items.iterrows():
        coverage = coverage_row.to_dict()
        requirement_id = coverage.get("requirement_id", "")
        coverage_id = coverage.get("coverage_id", "")
        requirement = _find_requirement(structured_requirements, requirement_id)
        strategy = strategy_map.get(coverage_id, {})
        technique = strategy.get("technique", "Equivalence Partitioning")

        if technique == "Boundary Value Analysis":
            generated = _bva_cases(counter, requirement_id, coverage_id, coverage, requirement)
        elif technique == "Decision Table Testing":
            generated = _decision_table_cases(counter, requirement_id, coverage_id, coverage, requirement)
        elif technique == "State Transition Testing":
            generated = _state_cases(counter, requirement_id, coverage_id, coverage)
        else:
            generated = _ep_cases(counter, requirement_id, coverage_id, coverage, requirement)

        rows.extend(generated)
        counter += len(generated)

    if include_state_tests and not any(row.get("technique") == "State Transition Testing" for row in rows):
        state_rows = generate_state_transition_tests(start_index=counter).to_dict("records")
        rows.extend(state_rows)

    return pd.DataFrame(rows)
