from __future__ import annotations

import pandas as pd


PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
RISK_LEVEL_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def deduplicate_suite(test_cases: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicated test cases based on traceability and expected outcome."""
    if test_cases.empty:
        return test_cases.copy()

    subset = [
        column
        for column in [
            "requirement_id",
            "coverage_id",
            "technique",
            "test_data",
            "expected_result",
        ]
        if column in test_cases.columns
    ]

    if not subset:
        return test_cases.copy()

    return test_cases.drop_duplicates(subset=subset, keep="first").reset_index(
        drop=True
    )


def prioritize_suite(test_cases: pd.DataFrame) -> pd.DataFrame:
    """Sort test cases by priority, risk level, and risk score."""
    if test_cases.empty:
        return test_cases.copy()

    data = test_cases.copy()
    data["_priority_order"] = data.get("priority", "Medium").map(PRIORITY_ORDER).fillna(3)
    data["_risk_level_order"] = (
        data.get("risk_level", "Medium").map(RISK_LEVEL_ORDER).fillna(3)
    )
    data["_risk_score_order"] = pd.to_numeric(
        data.get("risk_score", 0), errors="coerce"
    ).fillna(0)

    sort_columns = ["_priority_order", "_risk_level_order", "_risk_score_order"]
    data = data.sort_values(sort_columns, ascending=[True, True, False])
    return data.drop(columns=sort_columns).reset_index(drop=True)


def minimize_suite(
    test_cases: pd.DataFrame,
    max_cases: int | None = None,
    keep_high_risk: bool = True,
) -> pd.DataFrame:
    """Limit suite size while preserving high-risk cases when possible."""
    if test_cases.empty:
        return test_cases.copy()

    optimized = prioritize_suite(deduplicate_suite(test_cases))

    if max_cases is None or max_cases <= 0 or len(optimized) <= max_cases:
        return optimized

    if not keep_high_risk or "risk_level" not in optimized.columns:
        return optimized.head(max_cases).reset_index(drop=True)

    high_risk = optimized[optimized["risk_level"] == "High"]
    remaining = optimized[optimized["risk_level"] != "High"]

    if len(high_risk) >= max_cases:
        return high_risk.head(max_cases).reset_index(drop=True)

    selected = pd.concat(
        [high_risk, remaining.head(max_cases - len(high_risk))],
        ignore_index=True,
    )
    return selected.reset_index(drop=True)


def optimize_suite(
    test_cases: pd.DataFrame, max_cases: int | None = None
) -> pd.DataFrame:
    """FR 7.0 entry point: deduplicate, prioritize, and optionally minimize."""
    return minimize_suite(test_cases, max_cases=max_cases, keep_high_risk=True)
