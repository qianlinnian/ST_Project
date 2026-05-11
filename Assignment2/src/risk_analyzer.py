import pandas as pd
from typing import List

from src.ml_risk_model import predict_risk_level, calculate_rules_based_risk_score, MLRiskModel
from src.models import Requirement, RiskRecord


def analyze_risks(structured_requirements: pd.DataFrame) -> pd.DataFrame:
    # Legacy wrapper for Dataframes
    rows = []
    for _, row in structured_requirements.iterrows():
        text = row["requirement_text"].lower()
        impact = 5 if any(word in text for word in ["delete", "reject", "refresh"]) else 3
        probability = 4 if any(word in text for word in ["empty", "limit", "100", "completed"]) else 3
        score = calculate_rules_based_risk_score(impact, probability)
        rows.append(
            {
                "requirement_id": row["requirement_id"],
                "risk_score": round(score, 2),
                "risk_level": predict_risk_level(score),
            }
        )
    return pd.DataFrame(rows)


def analyze_requirements_risks(requirements: List[Requirement]) -> List[RiskRecord]:
    model = MLRiskModel()
    model.train()  # Try to train with historical data
    
    records = []
    for req in requirements:
        text = req.requirement_text.lower()
        
        # Heuristics for the dimensions
        impact = 5.0 if any(word in text for word in ["delete", "reject", "persist", "save"]) else 3.0
        probability = 4.0 if any(word in text for word in ["empty", "limit", "100", "character"]) else 3.0
        
        score = calculate_rules_based_risk_score(impact, probability)
        
        # Use ML Model to predict risk level, fallbacks to rule-based inside `predict`
        risk_level = model.predict(impact, probability)
        
        reason = f"Derived from text keywords (Impact={impact}, Prob={probability})."
        
        record = RiskRecord(
            requirement_id=req.requirement_id,
            impact=impact,
            probability=probability,
            risk_score=round(score, 2),
            risk_level=risk_level,
            reason=reason
        )
        records.append(record)
        
    return records

