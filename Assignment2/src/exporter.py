from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

import pandas as pd


# 导出目录：Assignment2/exports
EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"


def _ensure_export_dir() -> None:
    """确保导出目录存在。"""
    EXPORT_DIR.mkdir(exist_ok=True)


def _safe_filename(filename: str) -> str:
    """移除文件名中的不安全字符。"""
    return re.sub(r"[^A-Za-z0-9_.-]", "_", filename)


def export_csv(data: pd.DataFrame, filename: str) -> Path:
    """将 DataFrame 导出为 CSV。"""
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    data.to_csv(path, index=False)
    return path


def export_json(data: pd.DataFrame | Mapping[str, Any], filename: str) -> Path:
    """将 DataFrame 或项目状态字典导出为 JSON。"""
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
    """将一个或多个 DataFrame 导出为 Excel。"""
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
    """构建需求、覆盖项、测试策略和测试用例之间的追溯矩阵。"""
    req_cols = [
        column
        for column in ["requirement_id", "requirement_text", "module"]
        if column in structured_requirements.columns
    ]
    cov_cols = [
        column
        for column in ["coverage_id", "requirement_id", "description", "coverage_item", "coverage_type", "risk_level"]
        if column in coverage_items.columns
    ]
    strategy_cols = [
        column
        for column in ["coverage_id", "technique", "technique_standard", "strategy_reason"]
        if column in strategies.columns
    ]
    tc_cols = [
        column
        for column in ["test_case_id", "requirement_id", "coverage_id", "technique", "priority", "risk_level", "source"]
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
        "coverage_description",
        "coverage_type",
        "technique",
        "technique_standard",
        "test_case_id",
        "priority",
        "risk_level",
        "coverage_risk_level",
        "source",
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
    state_sequences: pd.DataFrame | None = None,
    prefix: str = "autotestdesign",
) -> dict[str, Path]:
    """导出一组常用测试设计工件。"""
    traceability = build_traceability_matrix(
        structured_requirements,
        coverage_items,
        strategies,
        test_cases,
    )
    artifacts = {
        "requirements_csv": export_csv(structured_requirements, f"{prefix}_requirements_structured.csv"),
        "coverage_csv": export_csv(coverage_items, f"{prefix}_coverage_items.csv"),
        "strategies_csv": export_csv(strategies, f"{prefix}_test_strategies.csv"),
        "test_cases_csv": export_csv(test_cases, f"{prefix}_test_cases.csv"),
        "test_suite_json": export_json(test_cases, f"{prefix}_test_suite.json"),
        "traceability_excel": export_excel(traceability, f"{prefix}_traceability_matrix.xlsx"),
    }

    excel_sheets = {
        "Requirements": structured_requirements,
        "Coverage": coverage_items,
        "Strategies": strategies,
        "Test Cases": test_cases,
        "Traceability": traceability,
    }

    if state_sequences is not None and not state_sequences.empty:
        excel_sheets["State Transitions"] = state_sequences
        artifacts["state_transitions_csv"] = export_csv(
            state_sequences,
            f"{prefix}_state_transitions.csv",
        )

    artifacts["test_design_excel"] = export_excel(
        excel_sheets,
        f"{prefix}_test_design_artifacts.xlsx",
    )
    return artifacts


def export_pytest_draft(test_cases: pd.DataFrame, filename: str = "test_todolist_generated_draft.py") -> Path:
    """导出 PyTest 草稿。草稿需要后续人工连接到真实 TodoList UI 或 API。"""
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)

    lines = [
        '"""PyTest draft generated by AutoTestDesign.',
        "Complete these tests against the actual simpletodolist implementation before execution.",
        '"""',
        "",
        "import pytest",
        "",
        "",
        "@pytest.mark.parametrize(",
        "    'case',",
        "    [",
    ]

    for case in test_cases.to_dict("records"):
        lines.extend(
            [
                "        {",
                f"            'test_case_id': {case.get('test_case_id', '')!r},",
                f"            'requirement_id': {case.get('requirement_id', '')!r},",
                f"            'coverage_id': {case.get('coverage_id', '')!r},",
                f"            'technique': {case.get('technique', '')!r},",
                f"            'test_data': {case.get('test_data', '')!r},",
                f"            'expected_result': {case.get('expected_result', '')!r},",
                "        },",
            ]
        )

    lines.extend(
        [
            "    ],",
            ")",
            "def test_todolist_generated_case(case):",
            "    assert case['test_case_id']",
            "    pytest.skip('Connect this generated draft to the simpletodolist UI or application API before execution.')",
            "",
        ]
    )

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
