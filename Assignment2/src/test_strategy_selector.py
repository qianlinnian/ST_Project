from __future__ import annotations

import pandas as pd


# 测试技术标准映射表
# 每个测试技术对应 ISTQB 和 ISO/IEC/IEEE 29119-4 标准的描述
TECHNIQUE_STANDARDS = {
    "Equivalence Partitioning": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 equivalence partitioning",
    "Boundary Value Analysis": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 boundary value analysis",
    "Decision Table Testing": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 decision table testing",
    "State Transition Testing": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 state transition testing",
}


def _text(row: pd.Series) -> str:
    """
    辅助函数：从覆盖项行中提取所有文本字段，用于策略选择的关键词匹配
    
    Args:
        row: 单个覆盖项的数据行
        
    Returns:
        合并后的小写文本字符串
    """
    values = [
        row.get("description", ""),       # 覆盖项描述
        row.get("coverage_item", ""),     # 覆盖项内容
        row.get("coverage_type", ""),     # 覆盖类型
        row.get("tags", ""),              # 标签
        row.get("related_techniques", ""),# 相关技术
    ]
    return " ".join(str(value).lower() for value in values if value is not None)


def _choose_strategy(row: pd.Series) -> tuple[str, str]:
    """
    根据覆盖项内容选择最合适的测试技术
    
    选择优先级（按顺序匹配）：
    1. 状态转换测试 - 涉及状态、转换、完成、激活等关键词
    2. 边界值分析 - 涉及边界、范围、长度、限制等关键词
    3. 决策表测试 - 涉及条件、规则、组合、删除、存在等关键词
    4. 等价类划分 - 涉及输入、有效、无效、功能、创建、添加等关键词
    5. 默认使用等价类划分
    
    Args:
        row: 单个覆盖项的数据行
        
    Returns:
        元组 (测试技术名称, 选择理由)
    """
    text = _text(row)

    # 状态转换测试：适用于事件驱动的行为，如 Todo 的生命周期状态变化
    if any(word in text for word in ["state", "transition", "complete", "completed", "active", "toggle"]):
        return (
            "State Transition Testing",
            "The coverage item focuses on Todo lifecycle states or transitions; state transition testing is appropriate for event-driven behaviour.",
        )

    # 边界值分析：适用于输入限制或边界条件
    if any(word in text for word in ["boundary", "range", "length", "limit", "empty", "blank", "minimum", "maximum"]):
        return (
            "Boundary Value Analysis",
            "The coverage item references input limits or boundary conditions; boundary value analysis targets values on and around boundaries.",
        )

    # 决策表测试：适用于多条件组合的业务规则
    if any(word in text for word in ["condition", "rule", "combination", "delete", "exist", "missing", "decision"]):
        return (
            "Decision Table Testing",
            "The coverage item depends on combinations of conditions and actions; decision table testing makes the rules explicit.",
        )

    # 等价类划分：适用于输入验证和功能测试
    if any(word in text for word in ["input", "valid", "invalid", "functional", "create", "add", "display", "list"]):
        return (
            "Equivalence Partitioning",
            "The coverage item can be divided into valid and invalid input or behaviour classes; one representative per partition is selected.",
        )

    # 默认使用等价类划分
    return (
        "Equivalence Partitioning",
        "Default black-box technique for representative coverage when no stronger condition, boundary, or state signal is present.",
    )


def select_strategies(coverage_items: pd.DataFrame) -> pd.DataFrame:
    """
    为每个覆盖项选择测试策略（测试技术）
    
    Args:
        coverage_items: 覆盖项 DataFrame，包含覆盖项的详细信息
        
    Returns:
        策略选择结果 DataFrame，包含 coverage_id、technique、strategy_reason 等字段
    """
    rows = []
    for _, row in coverage_items.iterrows():
        technique, reason = _choose_strategy(row)
        rows.append(
            {
                "coverage_id": row["coverage_id"],       # 覆盖项ID
                "requirement_id": row.get("requirement_id", ""),  # 关联的需求ID
                "coverage_type": row.get("coverage_type", "Functional"),  # 覆盖类型
                "risk_level": row.get("risk_level", "Medium"),    # 风险等级
                "technique": technique,                 # 选择的测试技术
                "technique_standard": TECHNIQUE_STANDARDS[technique],  # 技术标准
                "strategy_reason": reason,              # 选择理由
            }
        )
    return pd.DataFrame(rows)
