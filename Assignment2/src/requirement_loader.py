from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_sample_requirements() -> pd.DataFrame:
    path = DATA_DIR / "mock_todolist_requirements.csv"
    return pd.read_csv(path)
