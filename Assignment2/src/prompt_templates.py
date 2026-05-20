"""Prompt templates for optional LLM review.

These prompts do not replace B/C's rule-based modules. They are used to
explain, review, and improve generated artifacts while preserving traceability.
"""

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

COVERAGE_IMPROVEMENT_SYSTEM = (
    "You are a test design reviewer. Review coverage items against the provided "
    "requirements and suggest only missing valid coverage items. Preserve "
    "requirement_id traceability and use black-box or state-based testing terms."
)

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

TEST_CASE_IMPROVEMENT_SYSTEM = (
    "You are a test case design reviewer. Improve generated test cases without "
    "breaking traceability. Do not invent new requirement_id or coverage_id "
    "values unless explicitly asked to suggest missing cases."
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


def coverage_improvement_prompt(
    requirements_summary: str, coverage_summary: str
) -> str:
    return (
        "Review the current coverage items and identify missing valid coverage. "
        "The tool currently uses these coverage fields: coverage_id, "
        "requirement_id, description, coverage_type, risk_level, "
        "related_techniques, tags, notes.\n\n"
        f"Requirements:\n{requirements_summary}\n\n"
        f"Current coverage items:\n{coverage_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "missing_coverage_items": [\n'
        "    {\n"
        '      "requirement_id": "...",\n'
        '      "description": "...",\n'
        '      "coverage_type": "Functional|Input|Boundary|Condition|Error|State Transition",\n'
        '      "risk_level": "High|Medium|Low",\n'
        '      "related_techniques": ["Equivalence Partitioning"],\n'
        '      "reason": "..."\n'
        "    }\n"
        "  ],\n"
        '  "review_summary": "..."\n'
        "}\n\n"
        "Do not duplicate existing coverage_id values. Do not remove existing items."
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


def test_case_improvement_prompt(test_case_summary: str) -> str:
    return (
        "Review generated test cases for clarity, traceability, and executable "
        "test design quality.\n\n"
        "Required test case fields: test_case_id, requirement_id, coverage_id, "
        "technique, technique_standard, precondition, test_data, steps, "
        "expected_result, priority, risk_score, risk_level, coverage_type, "
        "automation_candidate, source, design_basis.\n\n"
        f"Generated test cases:\n{test_case_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "case_reviews": [\n'
        "    {\n"
        '      "test_case_id": "...",\n'
        '      "issue": "...",\n'
        '      "suggested_revision": "...",\n'
        '      "severity": "High|Medium|Low"\n'
        "    }\n"
        "  ],\n"
        '  "review_summary": "..."\n'
        "}\n\n"
        "Do not change requirement_id or coverage_id."
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
