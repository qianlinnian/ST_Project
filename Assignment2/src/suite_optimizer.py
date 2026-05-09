import pandas as pd


def prioritize_suite(test_cases: pd.DataFrame) -> pd.DataFrame:
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    data = test_cases.copy()
    data["_priority_order"] = data["priority"].map(priority_order).fillna(3)
    return data.sort_values("_priority_order").drop(columns=["_priority_order"])
