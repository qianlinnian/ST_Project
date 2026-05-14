"""Prompt templates for optional LLM review.

These prompts do not replace B/C's rule-based modules. They are used to
explain, review, and improve generated artifacts while preserving traceability.
"""


REQUIREMENT_STRUCTURING_SYSTEM = (
    "You are a software testing analyst following ISTQB Foundation Level and "
    "ISO/IEC/IEEE 29119-4 terminology. Extract test-design information from a "
    "single requirement. Return only valid JSON. Do not add markdown."
)

RISK_EXPLANATION_SYSTEM = (
    "You are a risk-based testing reviewer. Explain risk scoring using Impact, "
    "Probability/Likelihood, Risk Score, Risk Level, and Test Priority. Do not "
    "change requirement_id values."
)

COVERAGE_IMPROVEMENT_SYSTEM = (
    "You are a test design reviewer. Review coverage items against the provided "
    "requirements and suggest only missing valid coverage items. Preserve "
    "requirement_id traceability and use black-box or state-based testing terms."
)

TEST_STRATEGY_REVIEW_SYSTEM = (
    "You are a test strategy reviewer. Review whether each coverage item is "
    "mapped to a suitable ISO/IEC/IEEE 29119-4 black-box or state-based test "
    "technique. Do not rewrite the full strategy table. Return only valid JSON. "
    "Preserve coverage_id and requirement_id traceability."
)

TEST_CASE_IMPROVEMENT_SYSTEM = (
    "You are a test case design reviewer. Review generated test cases and suggest "
    "improvements without directly replacing the generated table. Return only "
    "valid JSON. Do not change requirement_id or coverage_id values."
)

ORACLE_REVIEW_SYSTEM = (
    "You are a test oracle reviewer. Review expected_result fields for clarity, "
    "observability, and consistency with the requirement, test data, and selected "
    "test technique. Return only valid JSON."
)

SUITE_OPTIMIZATION_REVIEW_SYSTEM = (
    "You are a test suite optimization reviewer. Review prioritization, "
    "deduplication, and risk-based ordering. Preserve high-risk coverage and "
    "coverage traceability. Return only valid JSON."
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
        "- Do not include requirement_id or module unless they appear in the input."
    )


def risk_explanation_prompt(requirement_text: str, risk_score: float, risk_level: str) -> str:
    return (
        "Explain the risk assessment for the requirement below. The local tool "
        "has already generated risk_score and risk_level; your role is to explain "
        "and review them, not to replace the local model.\n\n"
        f"Requirement:\n{requirement_text}\n\n"
        f"risk_score: {risk_score}\n"
        f"risk_level: {risk_level}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "impact_rationale": "...",\n'
        '  "probability_rationale": "...",\n'
        '  "priority_rationale": "...",\n'
        '  "review_note": "..."\n'
        "}"
    )


def coverage_improvement_prompt(requirements_summary: str, coverage_summary: str) -> str:
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
        '      "requirement_id": "...",\n'
        '      "current_technique": "...",\n'
        '      "recommended_technique": "...",\n'
        '      "change_needed": true,\n'
        '      "recommendation_reason": "...",\n'
        '      "standard_reference": "ISO/IEC/IEEE 29119-4"\n'
        "    }\n"
        "  ],\n"
        '  "review_summary": "..."\n'
        "}\n\n"
        "Only recommend a technique change when the current mapping is clearly weak."
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
        '      "requirement_id": "...",\n'
        '      "coverage_id": "...",\n'
        '      "issue": "...",\n'
        '      "suggested_revision": "...",\n'
        '      "missing_case_suggestion": "...",\n'
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
        '      "observability_issue": "...",\n'
        '      "reason": "..."\n'
        "    }\n"
        "  ],\n"
        '  "review_summary": "..."\n'
        "}"
    )


def suite_optimization_review_prompt(test_case_summary: str, optimized_summary: str) -> str:
    return (
        "Review whether the optimized suite preserves risk and coverage while "
        "reducing redundancy.\n\n"
        f"Original generated test cases:\n{test_case_summary}\n\n"
        f"Optimized suite:\n{optimized_summary}\n\n"
        "Return JSON with this shape:\n"
        "{\n"
        '  "optimization_review": "...",\n'
        '  "removed_or_missing_coverage": ["..."],\n'
        '  "high_risk_preservation": "...",\n'
        '  "recommended_changes": ["..."]\n'
        "}"
    )
