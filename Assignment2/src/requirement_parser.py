import pandas as pd

from src.nlp_processor import extract_requirement_parts


def structure_requirements(requirements: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in requirements.iterrows():
        parts = extract_requirement_parts(row["requirement_text"])
        rows.append({**row.to_dict(), **parts})
    return pd.DataFrame(rows)
