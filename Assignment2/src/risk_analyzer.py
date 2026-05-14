import pandas as pd
from typing import List

from src.ml_risk_model import (
    predict_risk_level,
    calculate_rules_based_risk_score,
    MLRiskModel,
)
from src.models import Requirement, RiskRecord
from src.ai_client import chat_completion


def analyze_risks(structured_requirements: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in structured_requirements.iterrows():
        text = row["requirement_text"].lower()
        req_id = row["requirement_id"]
        risk_category = _classify_risk_category(text)

        impact = (
            5
            if any(
                word in text
                for word in ["delete", "reject", "refresh", "persist", "save"]
            )
            else 3
        )
        probability = (
            4
            if any(
                word in text
                for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
            )
            else 3
        )
        score = calculate_rules_based_risk_score(impact, probability)
        rows.append(
            {
                "risk_id": f"RSK-{str(req_id).split('-')[-1]}",
                "requirement_id": req_id,
                "risk_category": risk_category,
                "risk_description": _describe_risk(risk_category),
                "impact": impact,
                "likelihood": probability,
                "risk_score": round(score, 2),
                "risk_level": predict_risk_level(score),
                "reason": _risk_reason(impact, probability, text),
                "test_suggestion": _test_suggestion(risk_category),
            }
        )
    return pd.DataFrame(rows)


def _classify_risk_category(text: str) -> str:
    if any(
        word in text for word in ["credential", "password", "login", "admin", "auth"]
    ):
        return "security"
    if any(
        word in text
        for word in ["refresh", "persist", "save", "localstorage", "storage"]
    ):
        return "reliability"
    if any(
        word in text for word in ["filter", "active", "completed", "display", "view"]
    ):
        return "interaction capability"
    if any(
        word in text for word in ["limit", "100", "empty", "blank", "input", "invalid"]
    ):
        return "functional suitability"
    return "functional suitability"


def _describe_risk(risk_category: str) -> str:
    descriptions = {
        "security": "Authentication or protected access behavior may be bypassed or handled incorrectly.",
        "reliability": "Todo data or state may not be preserved consistently across operations.",
        "interaction capability": "The UI may display an incorrect Todo state or filter result.",
        "functional suitability": "The feature may not satisfy the required Todo behavior or input validation rule.",
    }
    return descriptions.get(risk_category, descriptions["functional suitability"])


def _risk_reason(impact: float, probability: float, text: str) -> str:
    signals = []
    if any(word in text for word in ["delete", "reject", "persist", "save", "refresh"]):
        signals.append("high-impact keyword")
    if any(
        word in text
        for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
    ):
        signals.append("error-prone condition or state keyword")
    signal_text = ", ".join(signals) if signals else "basic functional behavior"
    return f"Impact={impact}, Likelihood={probability}; derived from {signal_text}."


def _test_suggestion(risk_category: str) -> str:
    suggestions = {
        "security": "Include negative and unauthorized access tests.",
        "reliability": "Include persistence and recovery-oriented tests.",
        "interaction capability": "Include UI state, filtering, and transition tests.",
        "functional suitability": "Include valid, invalid, and boundary input tests.",
    }
    return suggestions.get(risk_category, suggestions["functional suitability"])


def analyze_requirements_risks(requirements: List[Requirement]) -> List[RiskRecord]:
    model = MLRiskModel()
    model.train()  # Try to train with historical data

    records = []
    for req in requirements:
        text = req.requirement_text.lower()

        # Heuristics for the dimensions
        impact = (
            5.0
            if any(word in text for word in ["delete", "reject", "persist", "save"])
            else 3.0
        )
        probability = (
            4.0
            if any(word in text for word in ["empty", "limit", "100", "character"])
            else 3.0
        )

        score = calculate_rules_based_risk_score(impact, probability)

        # Use ML Model to predict risk level
        risk_level = model.predict(impact, probability)
        reason = f"Derived from text keywords (Impact={impact}, Prob={probability})."

        # LLM fallback as final check (if required, doing a quick prediction to override if Low/Medium but seems High)
        if risk_level in ["Low", "Medium"]:
            try:
                system_prompt = "You are a risk analyzer. Simply respond with High, Medium, or Low based on the requirement text. Keep your answer strictly to one of the above 3 words."
                user_prompt = (
                    f"Analyze risk level for requirement: {req.requirement_text}"
                )
                llm_response = chat_completion(system_prompt, user_prompt).strip()
                if llm_response in ["High", "Medium", "Low"]:
                    if llm_response == "High":
                        risk_level = "High"
                        reason += " Elevated to High by LLM fallback."
            except Exception as e:
                pass

        record = RiskRecord(
            requirement_id=req.requirement_id,
            impact=impact,
            probability=probability,
            risk_score=round(score, 2),
            risk_level=risk_level,
            reason=reason,
        )
        records.append(record)

    return records
