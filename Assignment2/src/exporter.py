from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

import json

import pandas as pd


EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"
RISK_ANALYSIS_COLUMNS = [
    "risk_id",
    "requirement_id",
    "risk_description",
    "risk_category",
    "impact",
    "likelihood",
    "risk_score",
    "risk_level",
    "reason",
    "test_suggestion",
]
STRUCTURED_REQUIREMENT_COLUMNS = [
    "requirement_id",
    "module",
    "requirement_text",
    "input_fields",
    "data_ranges",
    "conditions",
    "actions",
    "expected_results",
]
COVERAGE_ITEM_COLUMNS = [
    "coverage_id",
    "requirement_id",
    "description",
    "coverage_type",
    "risk_level",
    "related_techniques",
    "tags",
    "notes",
    "source",
]
TEST_STRATEGY_COLUMNS = [
    "coverage_id",
    "requirement_id",
    "coverage_type",
    "risk_level",
    "technique",
    "strategy_reason",
    "source",
]
TEST_SUITE_COLUMNS = [
    "suite_id",
    "suite_name",
    "module",
    "risk_level",
    "priority",
    "coverage_ids",
    "techniques",
    "coverage_types",
    "suite_objective",
    "optimization_basis",
    "source",
    "llm_changes",
]
TEST_CASE_COLUMNS = [
    "test_case_id",
    "suite_id",
    "suite_name",
    "requirement_id",
    "coverage_id",
    "technique",
    "precondition",
    "test_data",
    "steps",
    "expected_result",
    "priority",
    "risk_score",
    "risk_level",
    "suite_risk_level",
    "suite_priority",
    "coverage_type",
    "automation_candidate",
    "source",
    "design_basis",
]
TRACEABILITY_COLUMNS = [
    "requirement_id",
    "requirement_text",
    "requirement_type",
    "coverage_id",
    "coverage_description",
    "suite_id",
    "suite_name",
    "test_case_id",
    "technique",
    "risk_level",
]
STATE_TRANSITION_COLUMNS = [
    "sequence_id",
    "transition_id",
    "coverage_id",
    "coverage_goal",
    "optimization_rule",
    "reset_required",
    "source_state",
    "event",
    "guard",
    "test_data",
    "target_state",
    "precondition",
    "steps",
    "expected_result",
]


def _ensure_export_dir() -> None:
    EXPORT_DIR.mkdir(exist_ok=True)


def _safe_filename(filename: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", filename)


def ensure_columns(data: pd.DataFrame | None, columns: list[str]) -> pd.DataFrame:
    if data is None:
        return pd.DataFrame(columns=columns)
    normalized = data.copy()
    for column in columns:
        if column not in normalized.columns:
            normalized[column] = pd.NA
    ordered = [column for column in columns if column in normalized.columns]
    remaining = [column for column in normalized.columns if column not in ordered]
    return normalized[ordered + remaining]


def _with_default_columns(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return ensure_columns(data, columns)


def export_csv(data: pd.DataFrame, filename: str) -> Path:
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    data.to_csv(path, index=False)
    return path


def export_json(data: pd.DataFrame | Mapping[str, Any], filename: str) -> Path:
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    payload: Any
    if isinstance(data, pd.DataFrame):
        payload = data.to_dict(orient="records")
    else:
        payload = dict(data)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def export_excel(sheets: Mapping[str, pd.DataFrame] | pd.DataFrame, filename: str) -> Path:
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)

    if isinstance(sheets, pd.DataFrame):
        sheets = {"Sheet1": sheets}

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, data in sheets.items():
            safe_sheet = str(sheet_name)[:31] or "Sheet"
            data.to_excel(writer, sheet_name=safe_sheet, index=False)
    return path


def build_traceability_matrix(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
    test_cases: pd.DataFrame,
) -> pd.DataFrame:
    req_cols = [
        column
        for column in ["requirement_id", "requirement_text", "module"]
        if column in structured_requirements.columns
    ]
    cov_cols = [
        column
        for column in [
            "coverage_id",
            "requirement_id",
            "description",
            "coverage_item",
            "coverage_type",
            "risk_level",
            "related_techniques",
            "tags",
            "notes",
            "source",
        ]
        if column in coverage_items.columns
    ]
    strategy_cols = [
        column
        for column in ["coverage_id", "technique", "strategy_reason"]
        if column in strategies.columns
    ]
    tc_cols = [
        column
        for column in [
            "test_case_id",
            "suite_id",
            "suite_name",
            "requirement_id",
            "coverage_id",
            "technique",
            "priority",
            "risk_level",
            "source",
            "test_data",
            "expected_result",
            "design_basis",
            "llm_reason",
        ]
        if column in test_cases.columns
    ]

    matrix = test_cases[tc_cols].copy() if tc_cols else pd.DataFrame()

    if not matrix.empty and cov_cols and "coverage_id" in matrix.columns:
        coverage = coverage_items[cov_cols].drop_duplicates("coverage_id")
        coverage = coverage.rename(
            columns={
                "description": "coverage_description",
                "coverage_item": "coverage_description",
                "risk_level": "coverage_risk_level",
                "source": "coverage_source",
            }
        )
        matrix = matrix.merge(coverage, on="coverage_id", how="left", suffixes=("", "_coverage"))

    if not matrix.empty and strategy_cols and "coverage_id" in matrix.columns:
        strategy = strategies[strategy_cols].drop_duplicates("coverage_id")
        matrix = matrix.merge(strategy, on="coverage_id", how="left", suffixes=("", "_strategy"))

    if not matrix.empty and req_cols and "requirement_id" in matrix.columns:
        requirements = structured_requirements[req_cols].drop_duplicates("requirement_id")
        matrix = matrix.merge(requirements, on="requirement_id", how="left", suffixes=("", "_requirement"))

    matrix = _fill_state_model_traceability(matrix, structured_requirements)
    ordered = [column for column in TRACEABILITY_COLUMNS if column in matrix.columns]
    return matrix[ordered]


def _fill_state_model_traceability(
    matrix: pd.DataFrame, structured_requirements: pd.DataFrame
) -> pd.DataFrame:
    if matrix.empty or "requirement_id" not in matrix.columns:
        return matrix

    filled = matrix.copy()
    if "requirement_type" not in filled.columns:
        filled["requirement_type"] = pd.NA
    state_rows = filled["requirement_id"].astype(str) == "REQ-STATE-MODEL"
    non_state_rows = ~state_rows
    current = filled.loc[non_state_rows, "requirement_type"]
    missing = current.isna() | current.astype(str).str.strip().isin(["", "None", "nan"])
    filled.loc[non_state_rows & missing, "requirement_type"] = "original"
    if not state_rows.any():
        return filled

    defaults = {
        "requirement_text": "State model derived requirement",
        "requirement_type": "derived",
        "module": _state_model_module(structured_requirements),
        "coverage_description": "State transition coverage derived from the generated behavior model",
        "coverage_type": "State Transition",
        "related_techniques": "State Transition Testing",
        "strategy_reason": "Covers state/event sequences derived from the behavior model.",
    }
    for column, value in defaults.items():
        if column not in filled.columns:
            filled[column] = pd.NA
        current = filled.loc[state_rows, column]
        missing = current.isna() | current.astype(str).str.strip().isin(["", "None", "nan"])
        filled.loc[state_rows & missing, column] = value
    return filled


def _state_model_module(structured_requirements: pd.DataFrame) -> str:
    if structured_requirements.empty or "module" not in structured_requirements.columns:
        return "Cross-module behavior"
    modules = sorted(
        {
            str(value).strip()
            for value in structured_requirements["module"].dropna()
            if str(value).strip()
        }
    )
    if len(modules) == 1:
        return modules[0]
    return "Cross-module behavior"


def export_test_artifacts(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
    test_cases: pd.DataFrame,
    optimized_test_cases: pd.DataFrame | None = None,
    risk_analysis: pd.DataFrame | None = None,
    state_sequences: pd.DataFrame | None = None,
    prefix: str = "autotestdesign",
    test_suites: pd.DataFrame | None = None,
    state_model: dict | None = None,
    export_format: str = "mixed",
) -> dict[str, Path]:
    traceability = build_traceability_matrix(
        structured_requirements,
        coverage_items,
        strategies,
        test_cases,
    )
    final_suite = optimized_test_cases if optimized_test_cases is not None else test_cases
    structured_requirements = ensure_columns(structured_requirements, STRUCTURED_REQUIREMENT_COLUMNS)
    coverage_items = ensure_columns(coverage_items, COVERAGE_ITEM_COLUMNS)
    strategies = ensure_columns(strategies, TEST_STRATEGY_COLUMNS)
    test_cases = ensure_columns(test_cases, TEST_CASE_COLUMNS)
    final_suite = ensure_columns(final_suite, TEST_CASE_COLUMNS)
    test_suites = ensure_columns(test_suites if test_suites is not None else pd.DataFrame(), TEST_SUITE_COLUMNS)
    risk_analysis = _with_default_columns(
        risk_analysis if risk_analysis is not None else pd.DataFrame(),
        RISK_ANALYSIS_COLUMNS,
    )
    state_sequences = _with_default_columns(
        state_sequences if state_sequences is not None else pd.DataFrame(),
        STATE_TRANSITION_COLUMNS,
    )
    export_format = str(export_format or "mixed").lower()

    excel_sheets = {
        "Requirements": structured_requirements,
        "Risk Analysis": risk_analysis,
        "Coverage Items": coverage_items,
        "Test Strategies": strategies,
        "Test Suites": test_suites,
        "Test Cases": test_cases,
        "Optimized Test Suite": final_suite,
        "Traceability": traceability,
        "State Transitions": state_sequences,
    }

    json_payload = {
        "requirements": structured_requirements.to_dict("records"),
        "risk_analysis": risk_analysis.to_dict("records"),
        "coverage_items": coverage_items.to_dict("records"),
        "test_strategies": strategies.to_dict("records"),
        "test_suites": test_suites.to_dict("records"),
        "test_cases": test_cases.to_dict("records"),
        "optimized_test_cases": final_suite.to_dict("records"),
        "traceability_matrix": traceability.to_dict("records"),
        "state_transition_sequences": state_sequences.to_dict("records"),
        "state_model": state_model or {},
    }

    if export_format == "xlsx":
        return {
            "test_design_excel": export_excel(
                excel_sheets,
                f"{prefix}_test_design_artifacts.xlsx",
            )
        }

    if export_format == "json":
        return {
            "test_suite_json": export_json(
                json_payload,
                f"{prefix}_test_suite_artifacts.json",
            )
        }

    artifacts = {
        "requirements_csv": export_csv(structured_requirements, f"{prefix}_requirements_structured.csv"),
        "risk_analysis_csv": export_csv(risk_analysis, f"{prefix}_risk_analysis.csv"),
        "coverage_csv": export_csv(coverage_items, f"{prefix}_coverage_items.csv"),
        "strategies_csv": export_csv(strategies, f"{prefix}_test_strategies.csv"),
        "test_suites_csv": export_csv(test_suites, f"{prefix}_test_suites.csv"),
        "test_cases_csv": export_csv(test_cases, f"{prefix}_test_cases.csv"),
        "optimized_test_suite_csv": export_csv(final_suite, f"{prefix}_optimized_test_suite.csv"),
        "traceability_csv": export_csv(traceability, f"{prefix}_traceability_matrix.csv"),
        "state_transitions_csv": export_csv(state_sequences, f"{prefix}_state_transitions.csv"),
    }

    if export_format == "csv":
        return artifacts

    artifacts["test_suite_json"] = export_json(
        json_payload,
        f"{prefix}_test_suite_artifacts.json",
    )
    artifacts["test_design_excel"] = export_excel(
        excel_sheets,
        f"{prefix}_test_design_artifacts.xlsx",
    )
    return artifacts


