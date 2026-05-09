REQUIREMENT_STRUCTURING_SYSTEM = (
    "You are a software testing assistant. Extract structured testing information "
    "from requirements using concise JSON-like fields."
)

RISK_EXPLANATION_SYSTEM = (
    "You are a risk-based testing assistant. Explain risk score and priority using "
    "ISTQB-style testing terminology."
)

COVERAGE_IMPROVEMENT_SYSTEM = (
    "You are a test design reviewer. Suggest missing coverage items and justify "
    "them based on black-box and state-based testing techniques."
)


def requirement_structuring_prompt(requirement_text: str) -> str:
    return f"Requirement:\n{requirement_text}\n\nExtract input fields, data ranges, conditions, and expected actions."


def risk_explanation_prompt(requirement_text: str, risk_score: float, risk_level: str) -> str:
    return (
        f"Requirement:\n{requirement_text}\n\n"
        f"Risk score: {risk_score}\nRisk level: {risk_level}\n\n"
        "Explain the risk priority briefly."
    )


def coverage_improvement_prompt(requirements_summary: str, coverage_summary: str) -> str:
    return (
        f"Requirements:\n{requirements_summary}\n\n"
        f"Current coverage items:\n{coverage_summary}\n\n"
        "Suggest missing valid coverage items."
    )
