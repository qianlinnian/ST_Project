"""Prompt templates for optional LLM review.

These prompts do not replace B/C's rule-based modules. They are used to
explain, review, and improve generated artifacts while preserving traceability.
"""

from typing import Any

import pandas as pd


def _compact_text(value: Any, limit: int) -> str:
    text = " ".join(_as_text(value).split())
    if len(text) > limit:
        return text[:limit]
    return text


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    return str(value or "")


def _split_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    if ";" in text:
        return [part.strip() for part in text.split(";") if part.strip()]
    return [part.strip() for part in text.split(",") if part.strip()]


REQUIREMENT_STRUCTURING_SYSTEM = (
    "You are a software testing analyst following ISTQB Foundation Level and "
    "ISO/IEC/IEEE 29119-4 terminology. Extract test-design information from a "
    "single requirement. Return only valid JSON. Do not add markdown."
)

COMPACT_REQUIREMENT_STRUCTURING_SYSTEM = """
You are a fast software requirement parser.

Return valid JSON only.
No markdown. No explanation. No trailing comma.

The output must be exactly this JSON object shape:
{"r":[["REQ-ID",["input"],["range"],["condition"],["action"],["expected"]]]}

Rules:
- The root object must contain only key "r".
- "r" must be one array.
- Each item must be one array:
  [id,input_fields,data_ranges,conditions,actions,expected_results]
- Return exactly one item for every input id.
- Use short strings.
- Use empty arrays when a field is not present.
- Do not invent ids.
""".strip()

RISK_ANALYSIS_SYSTEM = (
    "You are a risk analyzer following ISO/IEC/IEEE 29119-4. "
    "Classify and assess the risk of a given requirement. Return only valid JSON. Do not add markdown."
)

COMPACT_RISK_SYSTEM = """
You are a fast software requirement risk classifier.

Return valid JSON only.
No markdown. No explanation. No trailing comma.

The output must be exactly this JSON object shape:
{"r":[["REQ-ID","F",2,2,"short reason"]]}

Rules:
- The root value must be one JSON object.
- The root object must contain only key "r".
- "r" must be one array.
- Each item in "r" must be one array:
  [id,category,impact,likelihood,reason]
- Return exactly one item for every input id.
- Do not omit the final closing brackets.
- The response must end with: ]}

category must be one of:
S = security
R = reliability
I = interaction capability
F = functional suitability

impact and likelihood must be integers from 1 to 3.
reason must be no more than 6 English words.
""".strip()

COMPACT_COVERAGE_IMPROVEMENT_SYSTEM = """
You are a fast test coverage gap reviewer.

Return valid JSON only.
No markdown. No explanation. No trailing comma.

The output must be exactly this JSON object shape:
{"m":[["REQ-ID","CoverageType","missing coverage description",["Technique"],"short reason"]],"s":"summary"}

Rules:
- The root object must contain only keys "m" and "s".
- "m" must be an array.
- Each item in "m" must be:
  [requirement_id, coverage_type, description, related_techniques, reason]
- Only suggest coverage that is missing from current coverage.
- Do not repeat existing coverage.
- Prefer at most 2 missing items per requirement.
- Keep descriptions and reasons short.
- coverage_type must be one of: Functional, Input, Boundary, Condition, Error, State Transition.
""".strip()

TEST_STRATEGY_REVIEW_SYSTEM = (
    "You are a test strategy reviewer. Review whether each coverage item is "
    "mapped to a suitable ISO/IEC/IEEE 29119-4 black-box or state-based test "
    "technique. Preserve coverage_id and requirement_id traceability."
)

COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM = """
You are a fast missing test case generator.

Return valid JSON only.
No markdown. No explanation. No trailing comma.

The output must be exactly this JSON object shape:
{"m":[["REQ-ID","COV-ID","Technique","test data","steps","expected result","priority","risk level","reason"]]}

Rules:
- The root object must contain only key "m".
- "m" must be an array.
- Each item must be:
  [requirement_id, coverage_id, technique, test_data, steps, expected_result, priority, risk_level, reason]
- Return at most 8 items total for this batch.
- Return at most 1 item for each coverage_id.
- Return only missing test cases not already covered by existing cases.
- Preserve existing requirement_id and coverage_id values.
- Keep fields concise and executable; each string should be under 90 characters.
- Use numbered steps in one short sentence.
- reason must be no more than 6 English words.
- Use priority and risk_level values: High, Medium, or Low.
""".strip()

TEST_CASE_GENERATION_SYSTEM = (
    "You are a test case generation assistant following ISTQB Foundation Level "
    "and ISO/IEC/IEEE 29119-4 detailed test techniques. Generate systematic, "
    "traceable test cases from structured requirements, coverage items, and "
    "selected test strategies. Return only valid JSON. Preserve existing "
    "requirement_id and coverage_id values."
)

ORACLE_REVIEW_SYSTEM = (
    "You are a test oracle reviewer. Review expected_result fields for clarity, "
    "observability, and consistency with the requirement, test data, and selected "
    "test technique."
)

SUITE_OPTIMIZATION_REVIEW_SYSTEM = (
    "You are a test suite optimization reviewer. Review prioritization, "
    "deduplication, and risk-based ordering. Preserve high-risk coverage and "
    "explain any recommended minimization."
)

COMPACT_SUITE_MINIMIZATION_SYSTEM = """
You are a fast semantic test suite minimization reviewer.

Return valid JSON only.
No markdown. No explanation. No trailing comma.

The output must be exactly this JSON object shape:
{"keep":["TC-001"],"drop":[["TC-002","short reason"]]}

Rules:
- The root object must contain only keys "keep" and "drop".
- keep must list important test_case_id values to retain.
- drop must list [test_case_id, reason] for redundant or low-value cases.
- Do not drop High priority or High risk cases unless clearly duplicated.
- Do not drop the only test case for a coverage_id.
- Prefer keeping boundary, invalid, error, and state transition cases.
- Reasons must be no more than 6 English words.
""".strip()

STATE_MODEL_IMPROVEMENT_SYSTEM = """
You are a behavior modeling assistant for software test design.

Return valid JSON only.
No markdown. No explanation. No trailing comma.

Create a state transition model from structured requirements.
The model is used for model-based testing and All Transitions coverage.

Return exactly this JSON shape:
{
  "states": ["..."],
  "transitions": [
    {
      "transition_id": "TR-001",
      "source_state": "...",
      "event": "...",
      "target_state": "...",
      "guard": "...",
      "test_data": "..."
    }
  ],
  "coverage_goal": "All Transitions"
}

Rules:
- Use domain-level state names, not requirement ids.
- Keep states and events short.
- Include valid, invalid, filtering, completion, deletion, and persistence states when supported by requirements.
- Do not invent behavior that is not supported by requirements.
- Prefer 4 to 8 states and 5 to 12 transitions.
""".strip()

SUITE_DESIGN_IMPROVEMENT_SYSTEM = (
    "You improve high-level software test suite metadata. Return strict JSON only. "
    "Do not invent coverage IDs and do not remove traceability. Prefer concise names and objectives."
)


def requirement_structuring_prompt(requirement_text: str) -> str:
    return (
        "Analyze the following requirement and extract the fields used by the "
        "AutoTestDesign requirement parser.\n\n"
        f"Requirement:\n{requirement_text}\n\n"
        "Return exactly this JSON shape:\n"
        "{\n"
        '  "input_fields": ["..."],\n'
        '  "data_ranges": ["..."],\n'
        '  "conditions": ["..."],\n'
        '  "actions": ["..."],\n'
        '  "expected_results": ["..."]\n'
        "}\n\n"
        "Rules:\n"
        "- Use empty lists when a field is not present.\n"
        "- Keep values short and directly grounded in the requirement text.\n"
        "- Do not invent requirement_id or module values.\n"
        "- Extract only information explicitly supported by this requirement text."
    )


def test_strategy_review_prompt(coverage_summary: str, strategy_summary: str) -> str:
    return (
        "Review whether the selected test strategy is appropriate for each "
        "coverage item.\n\n"
        "Available techniques:\n"
        "- Equivalence Partitioning\n"
        "- Boundary Value Analysis\n"
        "- Decision Table Testing\n"
        "- State Transition Testing\n\n"
        "Strategy fields used by the tool: coverage_id, requirement_id, "
        "coverage_type, risk_level, technique, technique_standard, strategy_reason.\n\n"
        f"Coverage items:\n{coverage_summary}\n\n"
        f"Selected strategies:\n{strategy_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "strategy_reviews": [\n'
        "    {\n"
        '      "coverage_id": "...",\n'
        '      "current_technique": "...",\n'
        '      "recommended_technique": "...",\n'
        '      "recommendation_reason": "...",\n'
        '      "change_needed": true\n'
        "    }\n"
        "  ]\n"
        "}"
    )


def test_case_generation_prompt(
    requirements_summary: str,
    coverage_summary: str,
    strategy_summary: str,
) -> str:
    return (
        "Generate systematic test cases from structured requirements, coverage items, "
        "and selected test strategies. Use ISTQB Foundation Level terminology and "
        "ISO/IEC/IEEE 29119-4 detailed test techniques. Do not assume any specific "
        "application domain unless it is present in the input requirements.\n\n"
        "Required test case fields: test_case_id, requirement_id, coverage_id, "
        "technique, technique_standard, precondition, test_data, steps, "
        "expected_result, priority, risk_score, risk_level, coverage_type, "
        "automation_candidate, source, design_basis.\n\n"
        f"Structured requirements:\n{requirements_summary}\n\n"
        f"Coverage items:\n{coverage_summary}\n\n"
        f"Selected strategies:\n{strategy_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "test_cases": [\n'
        "    {\n"
        '      "test_case_id": "TC-001",\n'
        '      "requirement_id": "...",\n'
        '      "coverage_id": "...",\n'
        '      "technique": "Equivalence Partitioning|Boundary Value Analysis|Decision Table Testing|State Transition Testing",\n'
        '      "technique_standard": "...",\n'
        '      "precondition": "...",\n'
        '      "test_data": "...",\n'
        '      "steps": "1. ...",\n'
        '      "expected_result": "...",\n'
        '      "priority": "High|Medium|Low",\n'
        '      "risk_score": 0.0,\n'
        '      "risk_level": "High|Medium|Low",\n'
        '      "coverage_type": "...",\n'
        '      "automation_candidate": "Yes|No|Partial",\n'
        '      "source": "LLM prompt generation",\n'
        '      "design_basis": "..."\n'
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Preserve existing requirement_id and coverage_id values."
    )


def oracle_review_prompt(test_case_summary: str) -> str:
    return (
        "Review expected_result values. They must be observable, testable, and "
        "consistent with the requirement, test_data, and technique.\n\n"
        f"Test cases:\n{test_case_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "oracle_reviews": [\n'
        "    {\n"
        '      "test_case_id": "...",\n'
        '      "current_expected_result": "...",\n'
        '      "improved_expected_result": "...",\n'
        '      "reason": "..."\n'
        "    }\n"
        "  ]\n"
        "}"
    )


def suite_optimization_review_prompt(
    test_case_summary: str, optimized_summary: str
) -> str:
    return (
        "Review whether the optimized suite preserves risk and coverage while "
        "reducing redundancy.\n\n"
        f"Original generated test cases:\n{test_case_summary}\n\n"
        f"Optimized suite:\n{optimized_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "optimization_review": "...",\n'
        '  "coverage_risks": ["..."],\n'
        '  "recommended_changes": ["..."]\n'
        "}"
    )


def risk_analysis_batch_prompt(requirements_text: str) -> str:
    return (
        "Analyze the given requirements and assess their risk level based on the criteria below.\n\n"
        "Risk Categories (choose exactly one for each requirement):\n"
        "functional suitability, performance efficiency, compatibility, interaction capability, "
        "reliability, security, maintainability, flexibility, safety\n\n"
        "Likelihood Scoring Criteria:\n"
        "- 3 (High): The defect is very likely to occur. Complex code paths, multiple conditional judgments, lack of input validation, or reliance on known vulnerable mechanisms (e.g., direct write to localStorage without error handling, hard-coded credentials, etc.).\n"
        "- 2 (Medium): The defect may occur under specific conditions. Basic validation exists but is insufficient; moderate logical complexity.\n"
        "- 1 (Low): The defect is extremely unlikely to occur. Pure display logic, simple single-step operations, or no complex state dependencies.\n\n"
        "Impact Scoring Criteria:\n"
        "- 3 (High): Failure leads to severe consequences (e.g., security vulnerabilities, permanent loss of user data, complete unavailability of core functions, bypass of authentication).\n"
        "- 2 (Medium): Failure causes noticeable degradation in functionality or user experience, but the application remains partially usable.\n"
        "- 1 (Low): Failure causes only minor inconvenience, UI glitches, or affects edge cases, without impacting main workflows.\n\n"
        f"Requirements:\n{requirements_text}\n\n"
        "Return exactly this JSON shape, providing one result for each requirement:\n"
        "{\n"
        '  "risk_analyses": [\n'
        "    {\n"
        '      "requirement_id": "...",\n'
        '      "risk_category": "...",\n'
        '      "risk_description": "...",\n'
        '      "likelihood": 1,\n'
        '      "impact": 1,\n'
        '      "reason": "...",\n'
        '      "test_suggestion": "..."\n'
        "    }\n"
        "  ]\n"
        "}"
    )


def compact_requirement_structuring_prompt(batch: list[dict]) -> str:
    lines = ["id|requirement"]
    for item in batch:
        text = " ".join(str(item["requirement_text"]).split())
        if len(text) > 350:
            text = text[:350]
        lines.append(f"{item['requirement_id']}|{text}")
    return "\n".join(lines)


def compact_risk_prompt(batch: list[Any], text_limit: int = 300) -> str:
    lines = ["id|module|requirement"]
    for req in batch:
        req_id = _compact_text(getattr(req, "requirement_id", ""), 80)
        module = _compact_text(getattr(req, "module", ""), 80)
        text = _compact_text(getattr(req, "requirement_text", ""), text_limit)
        lines.append(f"{req_id}|{module}|{text}")
    return "\n".join(lines)


def compact_coverage_improvement_prompt(
    requirements: pd.DataFrame, coverage_items: pd.DataFrame
) -> str:
    lines = ["REQ|id|text|risk"]
    risk_by_req = {}
    if "requirement_id" in coverage_items.columns and "risk_level" in coverage_items.columns:
        risk_by_req = coverage_items.groupby("requirement_id")["risk_level"].first().to_dict()

    for _, row in requirements.iterrows():
        req_id = str(row.get("requirement_id", "")).strip()
        text = _compact_text(row.get("requirement_text", ""), 280)
        risk = str(risk_by_req.get(req_id, row.get("risk_level", "Medium")))
        lines.append(f"REQ|{req_id}|{text}|{risk}")

    lines.append("COV|id|req|type|desc|tech")
    for _, row in coverage_items.iterrows():
        coverage_id = str(row.get("coverage_id", "")).strip()
        req_id = str(row.get("requirement_id", "")).strip()
        coverage_type = str(row.get("coverage_type", "Functional")).strip()
        desc = _compact_text(row.get("description", ""), 180)
        tech = _compact_text(row.get("related_techniques", ""), 120)
        lines.append(f"COV|{coverage_id}|{req_id}|{coverage_type}|{desc}|{tech}")

    return "\n".join(lines)


def missing_test_case_prompt(
    coverage_batch: list[dict],
    requirements: pd.DataFrame,
    strategy_map: dict,
    existing_test_cases: pd.DataFrame,
) -> str:
    requirement_ids = {
        str(row.get("requirement_id", "")).strip()
        for row in coverage_batch
        if str(row.get("requirement_id", "")).strip()
    }
    coverage_ids = {
        str(row.get("coverage_id", "")).strip()
        for row in coverage_batch
        if str(row.get("coverage_id", "")).strip()
    }
    req_rows = (
        requirements[requirements["requirement_id"].astype(str).isin(requirement_ids)]
        if "requirement_id" in requirements.columns
        else requirements
    )
    case_rows = (
        existing_test_cases[existing_test_cases["coverage_id"].astype(str).isin(coverage_ids)]
        if "coverage_id" in existing_test_cases.columns
        else existing_test_cases
    )

    lines = ["REQ|id|text"]
    for _, row in req_rows.iterrows():
        lines.append(
            f"REQ|{_compact_text(row.get('requirement_id', ''), 60)}|"
            f"{_compact_text(row.get('requirement_text', ''), 260)}"
        )

    lines.append("COV|id|req|type|desc|tech|risk")
    for row in coverage_batch:
        cov_id = str(row.get("coverage_id", ""))
        strategy = strategy_map.get(cov_id, {})
        technique = strategy.get("technique", row.get("related_techniques", ""))
        lines.append(
            "|".join(
                [
                    "COV",
                    _compact_text(cov_id, 60),
                    _compact_text(row.get("requirement_id", ""), 60),
                    _compact_text(row.get("coverage_type", ""), 60),
                    _compact_text(row.get("description", ""), 180),
                    _compact_text(technique, 80),
                    _compact_text(row.get("risk_level", "Medium"), 40),
                ]
            )
        )

    lines.append("EXISTING|id|cov|tech|data|expected")
    for _, row in case_rows.iterrows():
        lines.append(
            "|".join(
                [
                    "EXISTING",
                    _compact_text(row.get("test_case_id", ""), 40),
                    _compact_text(row.get("coverage_id", ""), 60),
                    _compact_text(row.get("technique", ""), 80),
                    _compact_text(row.get("test_data", ""), 140),
                    _compact_text(row.get("expected_result", ""), 180),
                ]
            )
        )
    return "\n".join(lines)


def compact_suite_minimization_prompt(suite_payload: dict[str, Any]) -> str:
    lines = [
        f"SUITE|{_compact_text(suite_payload.get('suite_id', ''), 40)}|"
        f"{_compact_text(suite_payload.get('suite_name', ''), 100)}|"
        f"{_compact_text(suite_payload.get('suite_risk_level', ''), 20)}|"
        f"{_compact_text(suite_payload.get('suite_objective', ''), 220)}",
        "COV|id|req|type|risk|desc",
    ]
    for coverage in suite_payload.get("coverage_items", []):
        lines.append(
            "|".join(
                [
                    "COV",
                    _compact_text(coverage.get("coverage_id", ""), 40),
                    _compact_text(coverage.get("requirement_id", ""), 60),
                    _compact_text(coverage.get("coverage_type", ""), 60),
                    _compact_text(coverage.get("risk_level", "Medium"), 20),
                    _compact_text(coverage.get("description", ""), 180),
                ]
            )
        )
    lines.append("CASE|id|req|cov|tech|priority|risk|data|expected|basis")
    for row in suite_payload.get("test_cases", []):
        lines.append(
            "|".join(
                [
                    "CASE",
                    _compact_text(row.get("test_case_id", ""), 40),
                    _compact_text(row.get("requirement_id", ""), 60),
                    _compact_text(row.get("coverage_id", ""), 60),
                    _compact_text(row.get("technique", ""), 80),
                    _compact_text(row.get("priority", "Medium"), 20),
                    _compact_text(row.get("risk_level", "Medium"), 20),
                    _compact_text(row.get("test_data", ""), 120),
                    _compact_text(row.get("expected_result", ""), 160),
                    _compact_text(row.get("design_basis", ""), 120),
                ]
            )
        )
    return "\n".join(lines)


def state_model_improvement_prompt(structured_requirements: pd.DataFrame) -> str:
    lines = ["id|requirement|conditions|actions|expected"]
    for _, row in structured_requirements.iterrows():
        req_id = _compact_text(row.get("requirement_id", ""), 80)
        req_text = _compact_text(row.get("requirement_text", ""), 260)
        conditions = _compact_text(row.get("conditions", ""), 180)
        actions = _compact_text(row.get("actions", ""), 160)
        expected = _compact_text(row.get("expected_results", ""), 180)
        lines.append(f"{req_id}|{req_text}|{conditions}|{actions}|{expected}")
    return "\n".join(lines)


def suite_improvement_prompt(batch: list[dict], coverage_lookup: dict[str, dict]) -> str:
    lines = [
        "Return JSON: {\"suggestions\":[{\"suite_id\":\"TS-001\",\"action\":\"rename|improve_objective\","
        "\"reason\":\"...\",\"suggested_suite_name\":\"...\",\"suggested_objective\":\"...\","
        "\"suggested_optimization_basis\":\"...\",\"related_coverage_ids\":[\"COV-001\"]}]}",
        "SUITE|id|name|module|risk|priority|coverage_ids|techniques|coverage_types|objective|basis",
    ]
    for row in batch:
        coverage_ids = _split_values(row.get("coverage_ids", ""))
        lines.append(
            "|".join(
                [
                    "SUITE",
                    _compact_text(row.get("suite_id"), 40),
                    _compact_text(row.get("suite_name"), 100),
                    _compact_text(row.get("module"), 80),
                    _compact_text(row.get("risk_level"), 20),
                    _compact_text(row.get("priority"), 20),
                    _compact_text("; ".join(coverage_ids), 180),
                    _compact_text(row.get("techniques"), 120),
                    _compact_text(row.get("coverage_types"), 100),
                    _compact_text(row.get("suite_objective"), 240),
                    _compact_text(row.get("optimization_basis"), 120),
                ]
            )
        )
        for coverage_id in coverage_ids:
            coverage = coverage_lookup.get(coverage_id, {})
            lines.append(
                "COV|"
                + "|".join(
                    [
                        _compact_text(coverage_id, 40),
                        _compact_text(coverage.get("requirement_id"), 60),
                        _compact_text(coverage.get("coverage_type"), 60),
                        _compact_text(coverage.get("description"), 220),
                    ]
                )
            )
    return "\n".join(lines)
