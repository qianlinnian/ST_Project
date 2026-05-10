import pandas as pd


def generate_test_cases(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
) -> pd.DataFrame:
    strategy_map = dict(zip(strategies["coverage_id"], strategies["technique"]))
    rows = []
    for index, coverage in coverage_items.iterrows():
        technique = strategy_map.get(coverage["coverage_id"], "Equivalence Partitioning")
        rows.append(
            {
                "test_case_id": f"TC-{index + 1:03d}",
                "requirement_id": coverage["requirement_id"],
                "coverage_id": coverage["coverage_id"],
                "technique": technique,
                "precondition": "TodoList page is open and ready constraints are met",
                "test_data": "Input data based on Equivalence Partitioning / Boundary Value Analysis",
                "steps": "1. Set preconditions\n2. Execute action mapping to coverage item",
                "expected_result": "System behavior matches the requirement (Observability)",
                "priority": "Medium",
            }
        )
    return pd.DataFrame(rows)
