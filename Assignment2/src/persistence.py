from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1] / "data" / "projects"


def ensure_project_dir() -> Path:
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    return PROJECT_DIR


def dataframe_to_records(data: pd.DataFrame) -> list[dict]:
    return data.fillna("").to_dict(orient="records")


def records_to_dataframe(records: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(records or [])


def build_project_state(
    project_name: str,
    selected_provider: str,
    selected_model: str,
    artifacts: dict[str, pd.DataFrame],
) -> dict:
    return {
        "project_name": project_name,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "selected_provider": selected_provider,
        "selected_model": selected_model,
        "artifacts": {
            name: dataframe_to_records(value)
            for name, value in artifacts.items()
        },
    }


def save_project(project_state: dict, filename: str = "simpletodolist_project.json") -> Path:
    ensure_project_dir()
    path = PROJECT_DIR / filename
    path.write_text(json.dumps(project_state, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def list_projects() -> list[str]:
    ensure_project_dir()
    return sorted(path.name for path in PROJECT_DIR.glob("*.json"))


def load_project(filename: str) -> dict:
    path = PROJECT_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))
