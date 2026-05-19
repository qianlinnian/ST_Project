import pandas as pd
from typing import List

from src.models import Requirement, RiskRecord, CoverageItem


def identify_coverage_items(
    structured_requirements: pd.DataFrame, risks: pd.DataFrame
) -> pd.DataFrame:
    """DataFrame版本，供 Streamlit UI 直接使用。"""
    rows = []

    # 创建 risk 快速查找表
    risk_dict = {}
    if not risks.empty:
        risk_dict = risks.set_index("requirement_id")["risk_level"].to_dict()

    cov_counter = 1

    for index, row in structured_requirements.iterrows():
        req_id = row["requirement_id"]
        risk_level = risk_dict.get(req_id, "Medium")
        requirement_text = str(row.get("requirement_text", ""))
        actions = _as_list(row.get("actions"))
        input_fields = _as_list(row.get("input_fields"))
        conditions = _as_list(row.get("conditions"))
        data_ranges = _as_list(row.get("data_ranges"))
        expected_results = _as_list(row.get("expected_results"))

        # 1. 核心功能覆盖
        actions_desc = actions[0] if actions else requirement_text[:120]
        rows.append(
            {
                "coverage_id": f"COV-{cov_counter:03d}",
                "requirement_id": req_id,
                "description": f"Verify core behavior: {actions_desc}",
                "coverage_type": "Functional",
                "risk_level": risk_level,
                "related_techniques": ["Equivalence Partitioning"],
                "tags": ["core"],
                "notes": _expected_note(expected_results),
            }
        )
        cov_counter += 1

        # 2. 输入字段覆盖
        for field in input_fields:
            field_text = str(field).strip()
            if not field_text:
                continue
            rows.append(
                {
                    "coverage_id": f"COV-{cov_counter:03d}",
                    "requirement_id": req_id,
                    "description": f"Test input field '{field_text}' with valid and invalid data",
                    "coverage_type": "Input",
                    "risk_level": risk_level,
                    "related_techniques": ["Equivalence Partitioning", "Boundary Value Analysis"],
                    "tags": ["input"],
                    "notes": _expected_note(expected_results),
                }
            )
            cov_counter += 1

        # 3. 业务条件覆盖
        for cond in conditions:
            cond_str = str(cond).strip()
            if cond_str:
                rows.append(
                    {
                        "coverage_id": f"COV-{cov_counter:03d}",
                        "requirement_id": req_id,
                        "description": f"Validate condition: {cond_str}",
                        "coverage_type": "Condition",
                        "risk_level": risk_level,
                        "related_techniques": ["Decision Table Testing"],
                        "tags": ["condition"],
                        "notes": _expected_note(expected_results),
                    }
                )
                cov_counter += 1

        # 4. 数据范围 / 边界覆盖
        for data_range in data_ranges:
            range_text = str(data_range).strip()
            if not range_text:
                continue
            rows.append(
                {
                    "coverage_id": f"COV-{cov_counter:03d}",
                    "requirement_id": req_id,
                    "description": f"Test data range and boundaries: {range_text}",
                    "coverage_type": "Boundary",
                    "risk_level": risk_level,
                    "related_techniques": ["Boundary Value Analysis", "Equivalence Partitioning"],
                    "tags": ["boundary"],
                    "notes": _expected_note(expected_results),
                }
            )
            cov_counter += 1

    return pd.DataFrame(rows)


def _as_list(value) -> list:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    try:
        if pd.isna(value):
            return []
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        try:
            import ast

            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                return parsed
        except (SyntaxError, ValueError):
            pass
    return [item.strip() for item in text.split(",") if item.strip()]


def _expected_note(expected_results: list) -> str:
    if not expected_results:
        return ""
    return "Expected result basis: " + "; ".join(str(item) for item in expected_results)


def identify_coverage(
    requirements: List[Requirement], risks: List[RiskRecord]
) -> List[CoverageItem]:
    """
    核心函数：基于结构化需求生成高质量 Coverage Items
    充分利用 FR 1.1 解析出的结构化字段
    """
    coverage_items = []
    cov_counter = 1

    # 创建 risk 快速查找字典
    risk_map = {risk.requirement_id: risk.risk_level for risk in risks}

    for req in requirements:
        risk_level = risk_map.get(req.requirement_id, "Medium")

        # 1. 核心功能覆盖
        actions_desc = req.actions[0] if req.actions else req.requirement_text
        coverage_items.append(
            CoverageItem(
                coverage_id=f"COV-{cov_counter:03d}",
                requirement_id=req.requirement_id,
                description=f"Verify core behavior: {actions_desc}",
                coverage_type="Functional",
                risk_level=risk_level,
                related_techniques=["EP", "BVA"],
                tags=["core"],
            )
        )
        cov_counter += 1

        # 2. 输入字段覆盖
        for field in req.input_fields:
            coverage_items.append(
                CoverageItem(
                    coverage_id=f"COV-{cov_counter:03d}",
                    requirement_id=req.requirement_id,
                    description=f"Test input field '{field}' with valid/invalid data",
                    coverage_type="Input",
                    risk_level=risk_level,
                    related_techniques=["EP", "BVA"],
                    tags=["input"],
                )
            )
            cov_counter += 1

        # 3. 业务条件覆盖
        for condition in req.conditions:
            coverage_items.append(
                CoverageItem(
                    coverage_id=f"COV-{cov_counter:03d}",
                    requirement_id=req.requirement_id,
                    description=f"Validate business rule/condition: {condition}",
                    coverage_type="Condition",
                    risk_level=risk_level,
                    related_techniques=["Decision Table"],
                    tags=["condition"],
                )
            )
            cov_counter += 1

        # 4. 数据范围 / 边界覆盖
        for data_range in req.data_ranges:
            coverage_items.append(
                CoverageItem(
                    coverage_id=f"COV-{cov_counter:03d}",
                    requirement_id=req.requirement_id,
                    description=f"Test data range and boundaries: {data_range}",
                    coverage_type="Boundary",
                    risk_level=risk_level,
                    related_techniques=["BVA", "EP"],
                    tags=["boundary"],
                )
            )
            cov_counter += 1

    return coverage_items
