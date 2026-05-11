from __future__ import annotations

from typing import Any


def _normalise(value: Any) -> str:
    """
    辅助函数：将任意值规范化为小写字符串
    
    Args:
        value: 任意类型的值
        
    Returns:
        规范化后的小写字符串
    """
    return str(value or "").strip().lower()


def generate_expected_result(
    requirement_text: str = "",
    test_data: str = "",
    technique: str = "",
    action: str = "",
    expected_hint: str = "",
) -> str:
    """
    测试预言生成器：根据测试数据和上下文自动生成预期结果草稿
    
    这是 FR 5.0（测试预言生成）的实现，支持黑盒测试和状态转换测试的预期结果生成。
    预期结果会根据关键词匹配不同的场景生成相应的描述。
    
    Args:
        requirement_text: 需求文本
        test_data: 测试数据描述
        technique: 测试技术名称
        action: 执行的动作描述
        expected_hint: 预期结果提示（如果提供则直接返回）
        
    Returns:
        生成的预期结果字符串
    """
    req = _normalise(requirement_text)
    data = _normalise(test_data)
    tech = _normalise(technique)
    act = _normalise(action)
    hint = str(expected_hint or "").strip()

    # 如果有明确的提示，直接返回
    if hint:
        return hint

    # 合并所有文本用于关键词匹配
    combined = " ".join([req, data, tech, act])

    # 根据关键词匹配不同场景生成预期结果

    # 空输入场景
    if "empty" in combined or "blank" in combined or "0 character" in combined or "whitespace" in combined:
        return "The Todo item is not created; the list remains unchanged and input validation feedback is available."

    # 低于最小值场景
    if "below minimum" in combined or "less than minimum" in combined:
        return "The input is rejected because it is outside the valid equivalence partition; no Todo item is added."

    # 超过最大值场景
    if "above maximum" in combined or "exceeds" in combined or "too long" in combined:
        return "The input is rejected or constrained according to the stated maximum length; no invalid Todo item is stored."

    # 删除场景
    if "delete" in combined or "removed" in combined:
        if "not exist" in combined or "missing" in combined:
            return "No Todo item is removed; the system handles the missing item without corrupting the list state."
        return "The selected Todo item is removed from the list and is no longer visible after the action."

    # 标记完成场景
    if "complete" in combined or "completed" in combined or "mark done" in combined:
        return "The selected Todo item changes to the completed state and the UI/state representation reflects completion."

    # 重新激活场景
    if "active" in combined or "reopen" in combined or "uncomplete" in combined:
        return "The selected Todo item returns to the active state and is no longer shown as completed."

    # 持久化/刷新场景
    if "refresh" in combined or "persist" in combined or "save" in combined or "reload" in combined:
        return "After refresh or reload, the Todo list preserves the expected items and their states."

    # 创建/添加场景
    if "create" in combined or "add" in combined or "valid partition" in combined or "boundary" in combined:
        return "A Todo item is created successfully and appears in the list with the submitted valid text."

    # 决策表测试场景
    if "decision table" in combined:
        return "The observed outcome matches the decision table rule for the specified condition combination."

    # 状态转换测试场景
    if "state transition" in combined:
        return "The system reaches the expected target state after the transition and no invalid state is introduced."

    return f"The observable result satisfies the requirement: {requirement_text}"
