import json
from pathlib import Path

import pandas as pd


EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"


def export_csv(data: pd.DataFrame, filename: str) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    path = EXPORT_DIR / filename
    data.to_csv(path, index=False)
    return path


def export_excel(sheets: dict[str, pd.DataFrame], filename: str) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    path = EXPORT_DIR / filename
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, data in sheets.items():
            safe_name = sheet_name[:31]
            data.to_excel(writer, sheet_name=safe_name, index=False)
    return path


def export_json(data: dict, filename: str) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    path = EXPORT_DIR / filename
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
