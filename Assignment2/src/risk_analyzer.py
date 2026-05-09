import pandas as pd

from src.ml_risk_model import predict_risk_level


def analyze_risks(structured_requirements: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in structured_requirements.iterrows():
        text = row["requirement_text"].lower()
        impact = 5 if any(word in text for word in ["delete", "reject", "refresh"]) else 3
        probability = 4 if any(word in text for word in ["empty", "length", "completed"]) else 3
        complexity = 3
        visibility = 5
        score = impact * 0.4 + probability * 0.3 + complexity * 0.2 + visibility * 0.1
        rows.append(
            {
                "requirement_id": row["requirement_id"],
                "risk_score": round(score, 2),
                "risk_level": predict_risk_level(score),
            }
        )
    return pd.DataFrame(rows)
