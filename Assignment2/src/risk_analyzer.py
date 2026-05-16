import pandas as pd
from typing import List
import json

from src.models import Requirement, RiskRecord
from src.ai_client import chat_completion
from src.prompt_templates import RISK_ANALYSIS_SYSTEM, risk_analysis_batch_prompt


def analyze_risks(structured_requirements: pd.DataFrame) -> pd.DataFrame:
    # Legacy wrapper for Dataframes
    rows = []
    for _, row in structured_requirements.iterrows():
        text = row["requirement_text"].lower()
        req_id = row["requirement_id"]
        risk_category = _classify_risk_category(text)
        impact = (
            3
            if any(
                word in text
                for word in ["delete", "reject", "refresh", "persist", "save"]
            )
            else 2
        )
        likelihood = (
            3
            if any(
                word in text
                for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
            )
            else 2
        )
        score = likelihood * impact

        if score >= 7:
            risk_level = "High"
        elif score >= 4:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        rows.append(
            {
                "risk_id": f"RSK-{str(req_id).split('-')[-1]}",
                "requirement_id": req_id,
                "risk_category": risk_category,
                "risk_description": _describe_risk(risk_category),
                "impact": impact,
                "likelihood": likelihood,
                "risk_score": score,
                "risk_level": risk_level,
                "reason": _risk_reason(impact, likelihood, text),
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


def _risk_reason(impact: int, likelihood: int, text: str) -> str:
    signals = []
    if any(word in text for word in ["delete", "reject", "persist", "save", "refresh"]):
        signals.append("high-impact keyword")
    if any(
        word in text for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
    ):
        signals.append("error-prone condition or state keyword")
    signal_text = ", ".join(signals) if signals else "basic functional behavior"
    return f"Impact={impact}, Likelihood={likelihood}; derived from {signal_text}."


def _test_suggestion(risk_category: str) -> str:
    suggestions = {
        "security": "Include negative and unauthorized access tests.",
        "reliability": "Include persistence and recovery-oriented tests.",
        "interaction capability": "Include UI state, filtering, and transition tests.",
        "functional suitability": "Include valid, invalid, and boundary input tests.",
    }
    return suggestions.get(risk_category, suggestions["functional suitability"])


def analyze_requirements_risks(requirements: List[Requirement]) -> List[RiskRecord]:
    records = []

    # Process in batches to reduce LLM overhead
    batch_size = 5
    for i in range(0, len(requirements), batch_size):
        batch = requirements[i : i + batch_size]

        reqs_text = []
        for req in batch:
            reqs_text.append(
                f"Requirement ID: {req.requirement_id}\nContent: {req.requirement_text}\n"
            )

        try:
            system_prompt = RISK_ANALYSIS_SYSTEM
            user_prompt = risk_analysis_batch_prompt("\n---\n".join(reqs_text))

            # Using JSON mode for structured output
            llm_response = chat_completion(
                system_prompt, user_prompt, temperature=0.2
            ).strip()

            # Try parsing the json block if there are markdown tags
            if llm_response.startswith("```json"):
                llm_response = llm_response.strip("`").removeprefix("json").strip()
            elif llm_response.startswith("```"):
                llm_response = llm_response.strip("`").strip()

            parsed = json.loads(llm_response)
            analyses = parsed.get("risk_analyses", [])
            analysis_dict = {item.get("requirement_id"): item for item in analyses}

            for req in batch:
                item = analysis_dict.get(req.requirement_id, {})
                risk_category = item.get("risk_category", "functional suitability")
                risk_description = item.get(
                    "risk_description", "No description provided."
                )
                likelihood = int(item.get("likelihood", 1))
                impact = int(item.get("impact", 1))
                reason = item.get("reason", "Analyzed by LLM in batch.")
                test_suggestion = item.get("test_suggestion", "")

                score = likelihood * impact

                if score >= 7:
                    risk_level = "High"
                elif score >= 4:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"

                record = RiskRecord(
                    risk_id=(
                        f"RSK-{req.requirement_id.split('-')[-1]}"
                        if "-" in req.requirement_id
                        else f"RSK-{req.requirement_id}"
                    ),
                    requirement_id=req.requirement_id,
                    risk_category=risk_category,
                    risk_description=risk_description,
                    impact=impact,
                    likelihood=likelihood,
                    risk_score=score,
                    risk_level=risk_level,
                    reason=reason,
                    test_suggestion=test_suggestion,
                )
                records.append(record)

        except Exception as e:
            # Fallback values if LLM parsing fails for the batch
            for req in batch:
                record = RiskRecord(
                    risk_id=(
                        f"RSK-{req.requirement_id.split('-')[-1]}"
                        if "-" in req.requirement_id
                        else f"RSK-{req.requirement_id}"
                    ),
                    requirement_id=req.requirement_id,
                    risk_category="functional suitability",
                    risk_description="Error during LLM analysis",
                    impact=1,
                    likelihood=1,
                    risk_score=1,
                    risk_level="Low",
                    reason=f"Fallback due to LLM error: {str(e)}",
                    test_suggestion="Recommend manual review.",
                )
                records.append(record)

    return records
