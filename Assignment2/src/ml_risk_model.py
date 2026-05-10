import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression # dummy import if not installed
import joblib

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# def calculate_rules_based_risk_score(impact: float, probability: float) -> float:
#     # Risk Score = Impact * 0.6 + Probability * 0.4
#     return impact * 0.6 + probability * 0.4

# def predict_risk_level(score: float) -> str:
#     if score >= 4.0:
#         return "High"
#     if score >= 3.0:
#         return "Medium"
#     return "Low"

def calculate_rules_based_risk_score(impact: float, probability: float) -> float:
    """Risk Score = Impact * 0.6 + Probability * 0.4"""
    return impact * 0.6 + probability * 0.4


def predict_risk_level(score: float) -> str:
    """Must be consistent with the LLM prompt thresholds"""
    if score >= 0.70:
        return "High"
    elif score >= 0.40:
        return "Medium"
    else:
        return "Low"

class MLRiskModel:
    def __init__(self):
        self.model = None
        self.is_trained = False
        
    def train(self):
        """Train a lightweight risk model on mock historic results.
        If scikit-learn is not robustly setup, fails back to rules predictably.
        """
        try:
            from sklearn.ensemble import RandomForestClassifier
            path = DATA_DIR / "mock_historical_results.csv"
            if not path.exists():
                return
            df = pd.read_csv(path)
            X = df[['impact', 'probability']]
            y = df['risk_level']
            self.model = RandomForestClassifier(n_estimators=10, random_state=42)
            self.model.fit(X, y)
            self.is_trained = True
        except ImportError:
            pass

    def predict(self, impact: float, probability: float) -> str:
        if self.is_trained and self.model:
            import pandas as pd
            X_new = pd.DataFrame([{
                'impact': impact,
                'probability': probability
            }])
            return self.model.predict(X_new)[0]
        else:
            score = calculate_rules_based_risk_score(impact, probability)
            return predict_risk_level(score)

