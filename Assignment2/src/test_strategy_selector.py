import pandas as pd


def select_strategies(coverage_items: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in coverage_items.iterrows():
        text = str(row.get("description", row.get("coverage_item", ""))).lower()
        if "empty" in text or "length" in text:
            technique = "Boundary Value Analysis"
        elif "delete" in text or "completed" in text:
            technique = "Decision Table"
        else:
            technique = "Equivalence Partitioning"
        rows.append({"coverage_id": row["coverage_id"], "technique": technique})
    return pd.DataFrame(rows)
