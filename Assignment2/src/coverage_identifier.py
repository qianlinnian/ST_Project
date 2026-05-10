import pandas as pd
from typing import List

from src.models import Requirement, RiskRecord, CoverageItem


def identify_coverage_items(
    structured_requirements: pd.DataFrame, risks: pd.DataFrame
) -> pd.DataFrame:
    """DataFrame版本，主要用于界面展示和调试"""
    rows = []

    # 创建 risk 快速查找表
    risk_dict = {}
    if not risks.empty:
        risk_dict = risks.set_index("requirement_id")["risk_level"].to_dict()

    for index, row in structured_requirements.iterrows():
        req_id = row["requirement_id"]
        risk_level = risk_dict.get(req_id, "Medium")

        # 基础覆盖项
        rows.append(
            {
                "coverage_id": f"COV-{index + 1:03d}",
                "requirement_id": req_id,
                "description": f"Verify core functionality: {row.get('requirement_text', '')[:120]}...",
                "coverage_type": "Functional",
                "risk_level": risk_level,
            }
        )

        # 如果有结构化数据，生成更多覆盖项
        cond_val = row.get("conditions")
        conditions = []
        if isinstance(cond_val, list):
            conditions = cond_val
        else:
            try:
                if pd.notna(cond_val) and str(cond_val).strip():
                    conditions = str(cond_val).split(", ")
            except ValueError:
                if len(cond_val) > 0:
                    conditions = list(cond_val)

        for i, cond in enumerate(conditions):
            cond_str = str(cond).strip()
            if cond_str:
                rows.append(
                    {
                        "coverage_id": f"COV-{index + 1:03d}-C{i+1}",
                        "requirement_id": req_id,
                        "description": f"Validate condition: {cond_str}",
                        "coverage_type": "Condition",
                        "risk_level": risk_level,
                    }
                )

    return pd.DataFrame(rows)


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
