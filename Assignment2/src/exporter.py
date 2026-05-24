from __future__ import annotations

import json
import re
from pathlib import Path
from pprint import pformat
from typing import Any, Mapping

import pandas as pd


EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"


def _ensure_export_dir() -> None:
    EXPORT_DIR.mkdir(exist_ok=True)


def _safe_filename(filename: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", filename)


def _clean_value(value: Any) -> Any:
    if isinstance(value, (list, tuple)):
        return [_clean_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _clean_value(item) for key, item in value.items()}
    if pd.isna(value):
        return ""
    return value


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
        ]
        if column in coverage_items.columns
    ]
    strategy_cols = [
        column
        for column in ["coverage_id", "technique", "technique_standard", "strategy_reason"]
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

    if not matrix.empty and cov_cols:
        coverage = coverage_items[cov_cols].drop_duplicates("coverage_id")
        coverage = coverage.rename(
            columns={
                "description": "coverage_description",
                "coverage_item": "coverage_description",
                "risk_level": "coverage_risk_level",
            }
        )
        matrix = matrix.merge(coverage, on="coverage_id", how="left", suffixes=("", "_coverage"))

    if not matrix.empty and strategy_cols:
        strategy = strategies[strategy_cols].drop_duplicates("coverage_id")
        matrix = matrix.merge(strategy, on="coverage_id", how="left", suffixes=("", "_strategy"))

    if not matrix.empty and req_cols:
        requirements = structured_requirements[req_cols].drop_duplicates("requirement_id")
        matrix = matrix.merge(requirements, on="requirement_id", how="left", suffixes=("", "_requirement"))

    desired_order = [
        "requirement_id",
        "requirement_text",
        "module",
        "coverage_id",
        "suite_id",
        "suite_name",
        "coverage_description",
        "coverage_type",
        "related_techniques",
        "tags",
        "notes",
        "technique",
        "technique_standard",
        "test_case_id",
        "test_data",
        "expected_result",
        "priority",
        "risk_level",
        "coverage_risk_level",
        "source",
        "design_basis",
        "llm_reason",
        "strategy_reason",
    ]
    ordered = [column for column in desired_order if column in matrix.columns]
    remaining = [column for column in matrix.columns if column not in ordered]
    return matrix[ordered + remaining]


def export_test_artifacts(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
    test_cases: pd.DataFrame,
    optimized_test_cases: pd.DataFrame | None = None,
    state_sequences: pd.DataFrame | None = None,
    prefix: str = "autotestdesign",
    test_suites: pd.DataFrame | None = None,
    state_model: dict | None = None,
    export_format: str = "mixed",
) -> dict[str, Path]:
    final_suite = optimized_test_cases if optimized_test_cases is not None else test_cases
    traceability = build_traceability_matrix(
        structured_requirements,
        coverage_items,
        strategies,
        final_suite,
    )
    test_suites = test_suites if test_suites is not None else pd.DataFrame()
    state_sequences = state_sequences if state_sequences is not None else pd.DataFrame()
    export_format = str(export_format or "mixed").lower()

    excel_sheets = {
        "Requirements": structured_requirements,
        "Coverage": coverage_items,
        "Strategies": strategies,
        "Test Suites": test_suites,
        "Test Cases": test_cases,
        "Optimized Test Suite": final_suite,
        "Traceability": traceability,
    }
    if not state_sequences.empty:
        excel_sheets["State Transitions"] = state_sequences

    json_payload = {
        "requirements": structured_requirements.to_dict("records"),
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
        "coverage_csv": export_csv(coverage_items, f"{prefix}_coverage_items.csv"),
        "strategies_csv": export_csv(strategies, f"{prefix}_test_strategies.csv"),
        "test_suites_csv": export_csv(test_suites, f"{prefix}_test_suites.csv"),
        "test_cases_csv": export_csv(test_cases, f"{prefix}_test_cases.csv"),
        "optimized_test_suite_csv": export_csv(final_suite, f"{prefix}_optimized_test_suite.csv"),
        "traceability_csv": export_csv(traceability, f"{prefix}_traceability_matrix.csv"),
    }

    if not state_sequences.empty:
        artifacts["state_transitions_csv"] = export_csv(
            state_sequences,
            f"{prefix}_state_transitions.csv",
        )

    if export_format == "csv":
        return artifacts

    artifacts["test_suite_json"] = export_json(
        json_payload,
        f"{prefix}_test_suite.json",
    )
    artifacts["traceability_excel"] = export_excel(traceability, f"{prefix}_traceability_matrix.xlsx")
    artifacts["test_design_excel"] = export_excel(
        excel_sheets,
        f"{prefix}_test_design_artifacts.xlsx",
    )
    return artifacts


def export_selenium_pytest_draft(
    test_cases: pd.DataFrame,
    filename: str = "test_todolist_selenium_draft.py",
) -> Path:
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    fields = [
        "test_case_id",
        "suite_id",
        "suite_name",
        "requirement_id",
        "coverage_id",
        "technique",
        "test_data",
        "steps",
        "expected_result",
        "priority",
        "risk_level",
        "source",
        "design_basis",
    ]
    records = [
        {field: _clean_value(case.get(field, "")) for field in fields}
        for case in test_cases.to_dict("records")
    ]

    lines = [
        '"""Selenium + PyTest draft generated by AutoTestDesign.',
        "",
        "This file maps generated test design cases to a future browser automation script.",
        "It is not executable until the simpletodolist URL, selectors, actions, and assertions",
        "are completed manually.",
        '"""',
        "",
        "import pytest",
        "",
        'BASE_URL = "http://localhost:3000"',
        f"GENERATED_CASES = {pformat(records, width=100, sort_dicts=False)}",
        "",
        "",
        '@pytest.mark.parametrize("case", GENERATED_CASES)',
        "def test_todolist_generated_case(case):",
        "    pytest.skip(",
        '        "Complete Selenium browser setup, selectors, actions, and assertions "',
        '        "for simpletodolist before executing this draft."',
        "    )",
        "",
        "    # TODO: Open BASE_URL with Selenium.",
        "    # TODO: Convert case['steps'] into browser actions.",
        "    # TODO: Use case['test_data'] as input data.",
        "    # TODO: Assert observable UI behavior using case['expected_result'].",
        "    assert case['test_case_id']",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def export_pytest_draft(test_cases: pd.DataFrame, filename: str = "test_todolist_selenium_draft.py") -> Path:
    return export_selenium_pytest_draft(test_cases, filename)
