def predict_risk_level(score: float) -> str:
    if score >= 4:
        return "High"
    if score >= 2.5:
        return "Medium"
    return "Low"
