from __future__ import annotations

import pandas as pd

from src.oracle_generator import generate_expected_result


# Todo 状态机定义
# 定义 Todo 系统的所有可能状态
TODO_STATES = ["Empty List", "Active Todo", "Completed Todo", "Deleted Todo"]

# Todo 状态转换规则定义
# 每个转换包含：源状态、触发事件、目标状态、守卫条件、测试数据
TODO_TRANSITIONS = [
    {
        "transition_id": "TR-001",        # 转换ID
        "source_state": "Empty List",     # 源状态：空列表
        "event": "create valid todo",     # 触发事件：创建有效Todo
        "target_state": "Active Todo",    # 目标状态：活跃Todo
        "guard": "Todo text is non-empty and satisfies stated input constraints",  # 守卫条件
        "test_data": "Valid Todo text",   # 测试数据
    },
    {
        "transition_id": "TR-002",
        "source_state": "Empty List",
        "event": "reject empty todo",     # 触发事件：拒绝空Todo
        "target_state": "Empty List",     # 目标状态：保持空列表
        "guard": "Todo text is empty or whitespace only",
        "test_data": "Empty string / whitespace",
    },
    {
        "transition_id": "TR-003",
        "source_state": "Active Todo",
        "event": "mark complete",         # 触发事件：标记完成
        "target_state": "Completed Todo",
        "guard": "Todo exists and is active",
        "test_data": "Existing active Todo",
    },
    {
        "transition_id": "TR-004",
        "source_state": "Completed Todo",
        "event": "mark active",           # 触发事件：标记活跃
        "target_state": "Active Todo",
        "guard": "Todo exists and is completed",
        "test_data": "Existing completed Todo",
    },
    {
        "transition_id": "TR-005",
        "source_state": "Active Todo",
        "event": "delete active todo",    # 触发事件：删除活跃Todo
        "target_state": "Deleted Todo",
        "guard": "Todo exists and is active",
        "test_data": "Existing active Todo",
    },
    {
        "transition_id": "TR-006",
        "source_state": "Completed Todo",
        "event": "delete completed todo", # 触发事件：删除已完成Todo
        "target_state": "Deleted Todo",
        "guard": "Todo exists and is completed",
        "test_data": "Existing completed Todo",
    },
]


def build_todo_state_model() -> dict:
    """
    构建 Todo 状态转换模型
    
    Returns:
        状态模型字典，包含 states（状态列表）、transitions（转换三元组）、transition_details（完整转换信息）
    """
    return {
        "states": TODO_STATES,
        "transitions": [
            (
                transition["source_state"],
                transition["target_state"],
                transition["event"],
            )
            for transition in TODO_TRANSITIONS
        ],
        "transition_details": TODO_TRANSITIONS,
    }


def generate_all_states_sequence() -> pd.DataFrame:
    """
    生成"所有状态"覆盖准则的测试序列
    
    覆盖目标：确保系统能够到达每个定义的状态
    
    Returns:
        状态覆盖测试序列 DataFrame
    """
    rows = []
    for index, state in enumerate(TODO_STATES, start=1):
        if state == "Empty List":
            precondition = "TodoList page is open with no Todo items."
            steps = "1. Open the TodoList page\n2. Observe the initial list state"
        elif state == "Active Todo":
            precondition = "TodoList page is open."
            steps = "1. Create a Todo with valid text\n2. Observe the newly created item"
        elif state == "Completed Todo":
            precondition = "At least one active Todo exists."
            steps = "1. Select an active Todo\n2. Mark it as completed\n3. Observe the item state"
        else:
            precondition = "At least one Todo exists."
            steps = "1. Select an existing Todo\n2. Delete it\n3. Observe the list"

        rows.append(
            {
                "sequence_id": f"STATE-{index:03d}",
                "coverage_goal": "All States",
                "state": state,
                "precondition": precondition,
                "steps": steps,
                "expected_result": f"The system reaches or displays the '{state}' state as expected.",
            }
        )
    return pd.DataFrame(rows)


def generate_all_transitions_sequence() -> pd.DataFrame:
    """
    生成"所有转换"覆盖准则的测试序列
    
    覆盖目标：确保每个状态转换都被测试到
    
    Returns:
        转换覆盖测试序列 DataFrame
    """
    rows = []
    for index, transition in enumerate(TODO_TRANSITIONS, start=1):
        event = transition["event"]
        source = transition["source_state"]
        target = transition["target_state"]
        steps = (
            f"1. Establish source state: {source}\n"
            f"2. Apply event/action: {event}\n"
            f"3. Observe the resulting TodoList state"
        )
        rows.append(
            {
                "sequence_id": f"TRANS-{index:03d}",
                "transition_id": transition["transition_id"],
                "coverage_goal": "All Transitions",
                "source_state": source,
                "event": event,
                "guard": transition["guard"],
                "test_data": transition["test_data"],
                "target_state": target,
                "precondition": f"The TodoList is in state: {source}.",
                "steps": steps,
                "expected_result": generate_expected_result(
                    technique="State Transition Testing",
                    action=event,
                    test_data=transition["test_data"],
                ),
            }
        )
    return pd.DataFrame(rows)


def generate_state_transition_tests(
    requirement_id: str = "REQ-STATE-001",
    coverage_id: str = "COV-STATE-001",
    start_index: int = 1,
) -> pd.DataFrame:
    rows = []
    transitions = generate_all_transitions_sequence()
    for offset, row in transitions.iterrows():
        rows.append(
            {
                "test_case_id": f"TC-ST-{start_index + offset:03d}",
                "requirement_id": requirement_id,
                "coverage_id": coverage_id,
                "technique": "State Transition Testing",
                "technique_standard": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 state transition testing",
                "precondition": row["precondition"],
                "test_data": row["test_data"],
                "steps": row["steps"],
                "expected_result": row["expected_result"],
                "priority": "High",
                "risk_score": 0.0,
                "risk_level": "Medium",
                "coverage_type": "State Transition",
                "automation_candidate": "Yes",
                "source": "State Model",
                "design_basis": f"{row['source_state']} --{row['event']}--> {row['target_state']}",
            }
        )
    return pd.DataFrame(rows)
