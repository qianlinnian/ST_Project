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
        impact = (
            3 if any(word in text for word in ["delete", "reject", "refresh"]) else 2
        )
        likelihood = (
            3
            if any(word in text for word in ["empty", "limit", "100", "completed"])
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
                "requirement_id": row["requirement_id"],
                "risk_score": score,
                "risk_level": risk_level,
            }
        )
    return pd.DataFrame(rows)


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
