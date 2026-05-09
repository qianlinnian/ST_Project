from pathlib import Path

import pandas as pd


EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"


def export_csv(data: pd.DataFrame, filename: str) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    path = EXPORT_DIR / filename
    data.to_csv(path, index=False)
    return path
