import pandas as pd
from typing import List

from src.nlp_processor import extract_requirement_parts
from src.models import Requirement


def structure_requirements(requirements: pd.DataFrame) -> pd.DataFrame:
    """
    为 DataFrame 显示/调试用途，结构化需求文本。
    注意：此函数主要用于展示，实际解析建议使用 parse_requirements。
    """
    rows = []
    for _, row in requirements.iterrows():
        parts = extract_requirement_parts(row["requirement_text"])
        
        # 保留原始列表格式（推荐），仅在需要展示时才转字符串
        row_dict = row.to_dict()
        row_dict.update({
            "input_fields": parts.get("input_fields", []),
            "data_ranges": parts.get("data_ranges", []),
            "conditions": parts.get("conditions", []),
            "actions": parts.get("actions", []),
            "expected_results": parts.get("expected_results", [])
        })
        rows.append(row_dict)
    
    return pd.DataFrame(rows)


def parse_requirements(requirements_data: List[dict]) -> List[Requirement]:
    """
    将原始需求数据解析为 Requirement 对象列表（核心解析函数）。
    """
    parsed_reqs = []
    for data in requirements_data:
        req_id = data.get("requirement_id", f"REQ_{len(parsed_reqs)+1}")
        req_text = data.get("requirement_text", "").strip()
        module = data.get("module", "")

        if not req_text:
            continue  # 跳过空需求

        parts = extract_requirement_parts(req_text)
        
        req = Requirement(
            requirement_id=req_id,
            requirement_text=req_text,
            module=module,
            input_fields=parts.get("input_fields", []),
            data_ranges=parts.get("data_ranges", []),
            conditions=parts.get("conditions", []),
            actions=parts.get("actions", []),
            expected_results=parts.get("expected_results", [])
        )
        parsed_reqs.append(req)
        
    return parsed_reqs