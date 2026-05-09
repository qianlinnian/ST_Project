import pandas as pd


def identify_coverage_items(structured_requirements: pd.DataFrame, risks: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for index, row in structured_requirements.iterrows():
        rows.append(
            {
                "coverage_id": f"COV-{index + 1:03d}",
                "requirement_id": row["requirement_id"],
                "coverage_item": f"Cover behavior: {row['requirement_text']}",
            }
        )
    return pd.DataFrame(rows)
