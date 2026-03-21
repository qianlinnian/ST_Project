"""
Prompt 模板
职责：构建结构化的 prompt，引导 LLM 生成白盒测试用例。
包含三种 prompt：
  1. 首次生成（有 AST 分析结果，针对 Python）
  2. 通用模式（无 AST，非 Python 语言，LLM 自行分析代码结构）
  3. 补充生成（覆盖率不足时的反馈轮次）
"""

import json
from typing import Dict, Any, Optional, List


def build_python_prompt(source_code: str, analysis: Dict[str, Any],
                        requirements: Optional[str] = None) -> str:
    """
    构建首次生成 prompt（Python，有 AST 分析结果）
    将源代码和 AST 分析出的函数、分支、条件、路径信息一起发给 LLM，
    让它针对这些结构生成高覆盖率的测试用例。

    :param source_code: Python 源代码
    :param analysis: PythonAnalyzer.analyze() 返回的结构化分析结果
    :param requirements: 可选的需求文档内容
    :return: 完整的 prompt 字符串
    """
    # 将分析结果格式化为可读字符串
    functions_str = json.dumps(analysis["functions"], indent=2, ensure_ascii=False)
    branches_str = json.dumps(analysis["branches"], indent=2, ensure_ascii=False)
    conditions_str = json.dumps(analysis["conditions"], indent=2, ensure_ascii=False)
    paths_str = json.dumps(analysis["paths"], indent=2, ensure_ascii=False)

    # 需求文档部分（可选）
    req_section = ""
    if requirements:
        req_section = f"\n## 需求文档\n{requirements}\n"

    prompt = f"""你是一个白盒测试专家。请根据以下源代码和代码结构分析，生成全面的白盒测试用例。

## 源代码
```python
{source_code}
```

## 代码结构分析（来自 AST）

### 函数列表
{functions_str}

### 分支点（if/for/while/try）
{branches_str}

### 复合条件（and/or 表达式）
{conditions_str}

### 执行路径
{paths_str}
{req_section}
## 任务
请生成测试用例以实现以下覆盖目标：
1. **语句覆盖**：覆盖每一行可执行代码
2. **分支覆盖**：覆盖每个分支的 True 和 False 两个方向
3. **条件覆盖**：覆盖每个复合条件中每个子条件的 True/False 组合
4. **路径覆盖**：覆盖所有可行的执行路径

## 输出格式
请严格返回 JSON 数组，每个测试用例包含以下字段：
```json
[
  {{
    "id": "TC001",
    "description": "测试描述（说明覆盖了什么分支/条件/路径）",
    "input": {{"参数名": 值}},
    "expected_output": "期望输出",
    "covered_branches": ["L行号: 条件 → True/False"],
    "covered_paths": ["路径描述"]
  }}
]
```
请只返回 JSON，不要包含其他文字。"""
    return prompt


def build_general_prompt(source_code: str, language: str,
                         requirements: Optional[str] = None) -> str:
    """
    构建通用模式 prompt（非 Python 语言，无 AST 分析）
    让 LLM 自行分析代码结构后再生成测试用例。

    :param source_code: 源代码内容
    :param language: 编程语言名称，如 "javascript", "java"
    :param requirements: 可选的需求文档
    :return: 完整的 prompt 字符串
    """
    req_section = ""
    if requirements:
        req_section = f"\n## 需求文档\n{requirements}\n"

    prompt = f"""你是一个白盒测试专家。

## 源代码（{language}）
```{language}
{source_code}
```
{req_section}
## 任务
1. **首先分析代码结构**：识别所有函数、分支（if/else/switch）、循环、异常处理和复合条件。
2. **然后生成测试用例**，覆盖以下目标：
   - 语句覆盖：覆盖每一行代码
   - 分支覆盖：覆盖每个分支的 True/False
   - 条件覆盖：覆盖复合条件的各子条件组合
   - 路径覆盖：覆盖所有可行路径

## 输出格式
请严格返回 JSON 数组：
```json
[
  {{
    "id": "TC001",
    "description": "测试描述",
    "input": {{"参数名": 值}},
    "expected_output": "期望输出",
    "covered_branches": ["分支描述"],
    "covered_paths": ["路径描述"]
  }}
]
```
请只返回 JSON，不要包含其他文字。"""
    return prompt


def build_supplement_prompt(source_code: str, coverage_report: Dict[str, Any],
                            existing_tests: List[Dict]) -> str:
    """
    构建补充生成 prompt（覆盖率不足时的反馈轮次）
    将当前覆盖率报告和未覆盖的行/分支信息反馈给 LLM，让它生成补充测试。

    :param source_code: 源代码内容
    :param coverage_report: 覆盖率报告，包含 statement_coverage, uncovered_lines 等
    :param existing_tests: 已有的测试用例列表
    :return: 完整的 prompt 字符串
    """
    # 在源代码中标注未覆盖的行
    lines = source_code.splitlines()
    uncovered = set(coverage_report.get("uncovered_lines", []))
    annotated_lines = []
    for i, line in enumerate(lines, 1):
        marker = " ✗ 未覆盖" if i in uncovered else ""
        annotated_lines.append(f"{i:4d} | {line}{marker}")
    annotated_source = "\n".join(annotated_lines)

    # 格式化未覆盖分支
    uncovered_branches = coverage_report.get("uncovered_branches", [])
    branches_str = "\n".join(f"  - {b}" for b in uncovered_branches) if uncovered_branches else "  无"

    prompt = f"""之前生成的测试用例覆盖率不足，请补充测试用例。

## 当前覆盖率
- 语句覆盖率：{coverage_report.get('statement_coverage', 0):.1f}%
- 分支覆盖率：{coverage_report.get('branch_coverage', 0):.1f}%

## 未覆盖的代码行
{list(uncovered)}

## 未覆盖的分支
{branches_str}

## 源代码（已标注未覆盖行）
```
{annotated_source}
```

## 已有的测试用例数量：{len(existing_tests)} 个

## 任务
请**只生成补充测试用例**，专门针对上述未覆盖的行和分支。
不要重复已有的测试用例。

## 输出格式
请严格返回 JSON 数组：
```json
[
  {{
    "id": "TC_SUP_001",
    "description": "补充测试描述",
    "input": {{"参数名": 值}},
    "expected_output": "期望输出",
    "covered_branches": ["针对的未覆盖分支"],
    "covered_paths": ["针对的未覆盖路径"]
  }}
]
```
请只返回 JSON，不要包含其他文字。"""
    return prompt