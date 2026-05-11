import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_sample_requirements() -> pd.DataFrame:
    """Load mock requirements from CSV for demonstration and testing."""
    path = DATA_DIR / "mock_todolist_requirements.csv"
    
    if not path.exists():
        print(f"[Warning] Mock requirements file not found: {path}")
        return pd.DataFrame(columns=["requirement_id", "requirement_text", "module"])
    
    try:
        df = pd.read_csv(path)
        print(f"[Info] Loaded {len(df)} sample requirements from {path.name}")
        return df
    except Exception as e:
        print(f"[Error] Failed to load requirements: {e}")
        return pd.DataFrame(columns=["requirement_id", "requirement_text", "module"])


def load_requirements_as_dicts() -> List[Dict[str, Any]]:
    """Load requirements as list of dictionaries."""
    df = load_sample_requirements()
    if df.empty:
        return []
    return df.to_dict('records')