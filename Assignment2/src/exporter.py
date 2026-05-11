from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping

import pandas as pd


# 导出目录路径（项目根目录下的 exports 文件夹）
EXPORT_DIR = Path(__file__).resolve().parents[1] / "exports"


def _ensure_export_dir() -> None:
    """确保导出目录存在，如果不存在则创建"""
    EXPORT_DIR.mkdir(exist_ok=True)


def _safe_filename(filename: str) -> str:
    """
    将文件名转换为安全格式，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        安全的文件名
    """
    return re.sub(r"[^A-Za-z0-9_.-]", "_", filename)


def export_csv(data: pd.DataFrame, filename: str) -> Path:
    """
    将 DataFrame 导出为 CSV 文件
    
    Args:
        data: 要导出的数据
        filename: 导出的文件名
        
    Returns:
        导出文件的路径
    """
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    data.to_csv(path, index=False)
    return path


def export_json(data: pd.DataFrame, filename: str) -> Path:
    """
    将 DataFrame 导出为 JSON 文件
    
    Args:
        data: 要导出的数据
        filename: 导出的文件名
        
    Returns:
        导出文件的路径
    """
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    records = data.to_dict(orient="records")
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def export_excel(sheets: Mapping[str, pd.DataFrame] | pd.DataFrame, filename: str) -> Path:
    """
    将一个或多个 DataFrame 导出为 Excel 文件（多Sheet）
    
    Args:
        sheets: 字典形式的Sheet名称到DataFrame的映射，或单个DataFrame
        filename: 导出的文件名
        
    Returns:
        导出文件的路径
    """
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    
    # 如果传入的是单个DataFrame，包装成字典
    if isinstance(sheets, pd.DataFrame):
        sheets = {"Sheet1": sheets}
    
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, data in sheets.items():
            # Excel Sheet名称最长31个字符
            safe_sheet = str(sheet_name)[:31] or "Sheet"
            data.to_excel(writer, sheet_name=safe_sheet, index=False)
    return path


def build_traceability_matrix(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
    test_cases: pd.DataFrame,
) -> pd.DataFrame:
    """
    构建可追溯性矩阵
    
    矩阵建立需求 → 覆盖项 → 测试策略 → 测试用例之间的映射关系，满足 NFR 4.2.2（可追溯性要求）。
    
    Args:
        structured_requirements: 结构化需求 DataFrame
        coverage_items: 覆盖项 DataFrame
        strategies: 测试策略 DataFrame
        test_cases: 测试用例 DataFrame
        
    Returns:
        可追溯性矩阵 DataFrame
    """
    # 选择需要的列（只使用存在的列）
    req_cols = [column for column in ["requirement_id", "requirement_text", "module"] if column in structured_requirements.columns]
    cov_cols = [column for column in ["coverage_id", "requirement_id", "description", "coverage_type", "risk_level"] if column in coverage_items.columns]
    strategy_cols = [column for column in ["coverage_id", "technique", "technique_standard", "strategy_reason"] if column in strategies.columns]
    tc_cols = [column for column in ["test_case_id", "requirement_id", "coverage_id", "technique", "priority", "risk_level", "source"] if column in test_cases.columns]

    # 以测试用例为基础构建矩阵
    matrix = test_cases[tc_cols].copy() if tc_cols else pd.DataFrame()
    
    # 合并覆盖项信息
    if not matrix.empty and cov_cols:
        cov = coverage_items[cov_cols].drop_duplicates("coverage_id")
        cov = cov.rename(columns={"description": "coverage_description", "risk_level": "coverage_risk_level"})
        matrix = matrix.merge(cov, on="coverage_id", how="left", suffixes=("", "_coverage"))
    
    # 合并策略信息
    if not matrix.empty and strategy_cols:
        strategy = strategies[strategy_cols].drop_duplicates("coverage_id")
        matrix = matrix.merge(strategy, on="coverage_id", how="left", suffixes=("", "_strategy"))
    
    # 合并需求信息
    if not matrix.empty and req_cols:
        req = structured_requirements[req_cols].drop_duplicates("requirement_id")
        matrix = matrix.merge(req, on="requirement_id", how="left", suffixes=("", "_requirement"))

    # 按期望顺序排列列
    desired_order = [
        "requirement_id",          # 需求ID
        "requirement_text",       # 需求文本
        "module",                 # 模块
        "coverage_id",            # 覆盖项ID
        "coverage_description",   # 覆盖项描述
        "coverage_type",          # 覆盖类型
        "technique",              # 测试技术
        "technique_standard",     # 技术标准
        "test_case_id",           # 测试用例ID
        "priority",               # 优先级
        "risk_level",             # 风险等级
        "coverage_risk_level",    # 覆盖项风险等级
        "source",                 # 来源
        "strategy_reason",        # 策略选择理由
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
    """
    导出所有测试工件
    
    这是 FR 6.0（输出与导出）的主入口函数，支持导出多种格式。
    
    Args:
        structured_requirements: 结构化需求
        coverage_items: 覆盖项
        strategies: 测试策略
        test_cases: 测试用例
        state_sequences: 状态转换序列（可选）
        prefix: 导出文件的前缀
        
    Returns:
        导出文件路径字典
    """
    # 构建可追溯性矩阵
    traceability = build_traceability_matrix(structured_requirements, coverage_items, strategies, test_cases)
    
    # 导出各个文件
    artifacts = {
        "requirements_csv": export_csv(structured_requirements, f"{prefix}_requirements_structured.csv"),
        "coverage_csv": export_csv(coverage_items, f"{prefix}_coverage_items.csv"),
        "strategies_csv": export_csv(strategies, f"{prefix}_test_strategies.csv"),
        "test_cases_csv": export_csv(test_cases, f"{prefix}_test_cases.csv"),
        "test_suite_json": export_json(test_cases, f"{prefix}_test_suite.json"),
        "traceability_excel": export_excel(traceability, f"{prefix}_traceability_matrix.xlsx"),
    }

    # 准备Excel多Sheet导出
    excel_sheets = {
        "Requirements": structured_requirements,
        "Coverage": coverage_items,
        "Strategies": strategies,
        "Test Cases": test_cases,
        "Traceability": traceability,
    }
    
    # 如果有状态转换序列，添加到导出
    if state_sequences is not None and not state_sequences.empty:
        excel_sheets["State Transitions"] = state_sequences
        artifacts["state_transitions_csv"] = export_csv(state_sequences, f"{prefix}_state_transitions.csv")

    # 导出完整的测试设计工件Excel
    artifacts["test_design_excel"] = export_excel(excel_sheets, f"{prefix}_test_design_artifacts.xlsx")
    
    return artifacts


def export_pytest_draft(test_cases: pd.DataFrame, filename: str = "test_todolist_generated_draft.py") -> Path:
    """
    导出 PyTest 测试脚本草稿
    
    生成的草稿需要手动完善以连接到实际的 simpletodolist 实现。
    
    Args:
        test_cases: 测试用例 DataFrame
        filename: 导出的文件名
        
    Returns:
        导出文件的路径
    """
    _ensure_export_dir()
    path = EXPORT_DIR / _safe_filename(filename)
    
    lines = [
        '"""PyTest draft generated by AutoTestDesign.',
        "These tests are intentionally scaffolded for manual completion against the target simpletodolist implementation.",
        '"""',
        "",
        "import pytest",
        "",
        "",
        "@pytest.mark.parametrize(",
        "    'case',",
        "    [",
    ]
    
    # 为每个测试用例生成参数化数据
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
