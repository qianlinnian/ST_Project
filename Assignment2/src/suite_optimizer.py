from __future__ import annotations

import pandas as pd


# 优先级排序映射（数字越小优先级越高）
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
# 风险等级排序映射（数字越小风险越高）
RISK_LEVEL_ORDER = {"High": 0, "Medium": 1, "Low": 2}


def deduplicate_suite(test_cases: pd.DataFrame) -> pd.DataFrame:
    """
    去除测试套件中的重复测试用例
    
    去重依据：需求ID、覆盖项ID、测试技术、测试数据、预期结果的组合
    
    Args:
        test_cases: 测试用例 DataFrame
        
    Returns:
        去重后的测试用例 DataFrame
    """
    if test_cases.empty:
        return test_cases.copy()
    
    # 确定用于去重的列（只使用存在的列）
    subset = [
        column
        for column in ["requirement_id", "coverage_id", "technique", "test_data", "expected_result"]
        if column in test_cases.columns
    ]
    
    if not subset:
        return test_cases.copy()
    
    return test_cases.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)


def prioritize_suite(test_cases: pd.DataFrame) -> pd.DataFrame:
    """
    按优先级和风险对测试用例进行排序
    
    排序规则（优先级从高到低）：
    1. 优先级（High > Medium > Low）
    2. 风险等级（High > Medium > Low）
    3. 风险分数（降序，分数越高越优先）
    
    Args:
        test_cases: 测试用例 DataFrame
        
    Returns:
        排序后的测试用例 DataFrame
    """
    if test_cases.empty:
        return test_cases.copy()
    
    data = test_cases.copy()
    
    # 创建排序辅助列
    data["_priority_order"] = data.get("priority", "Medium").map(PRIORITY_ORDER).fillna(3)
    data["_risk_level_order"] = data.get("risk_level", "Medium").map(RISK_LEVEL_ORDER).fillna(3)
    data["_risk_score_order"] = pd.to_numeric(data.get("risk_score", 0), errors="coerce").fillna(0)
    
    # 按优先级、风险等级、风险分数排序
    sort_columns = ["_priority_order", "_risk_level_order", "_risk_score_order"]
    data = data.sort_values(sort_columns, ascending=[True, True, False])
    
    # 删除辅助列并重置索引
    return data.drop(columns=sort_columns).reset_index(drop=True)


def minimize_suite(
    test_cases: pd.DataFrame,
    max_cases: int | None = None,
    keep_high_risk: bool = True,
) -> pd.DataFrame:
    """
    最小化测试套件：在满足最大数量限制的同时保留高风险用例
    
    Args:
        test_cases: 测试用例 DataFrame
        max_cases: 最大测试用例数量（None表示不限制）
        keep_high_risk: 是否优先保留高风险用例
        
    Returns:
        最小化后的测试用例 DataFrame
    """
    if test_cases.empty:
        return test_cases.copy()

    # 先去重再排序
    optimized = prioritize_suite(deduplicate_suite(test_cases))
    
    # 如果没有数量限制或已满足限制，直接返回
    if max_cases is None or max_cases <= 0 or len(optimized) <= max_cases:
        return optimized

    # 如果不优先保留高风险或没有风险等级列，直接取前max_cases条
    if not keep_high_risk or "risk_level" not in optimized.columns:
        return optimized.head(max_cases).reset_index(drop=True)

    # 优先保留高风险用例
    high_risk = optimized[optimized["risk_level"] == "High"]
    remaining = optimized[optimized["risk_level"] != "High"]
    
    # 如果高风险用例已经超过限制，只取前max_cases条高风险用例
    if len(high_risk) >= max_cases:
        return high_risk.head(max_cases).reset_index(drop=True)

    # 否则保留所有高风险用例，再从剩余用例中补充
    selected = pd.concat([high_risk, remaining.head(max_cases - len(high_risk))], ignore_index=True)
    return selected.reset_index(drop=True)


def optimize_suite(test_cases: pd.DataFrame, max_cases: int | None = None) -> pd.DataFrame:
    """
    优化测试套件：去重 + 排序 + 最小化
    
    这是 FR 7.0（测试套件优化）的主入口函数，按风险优先级和覆盖效率对测试套件进行优化。
    
    Args:
        test_cases: 测试用例 DataFrame
        max_cases: 最大测试用例数量（可选）
        
    Returns:
        优化后的测试套件 DataFrame
    """
    return minimize_suite(test_cases, max_cases=max_cases, keep_high_risk=True)
