# All Prompt Templates

下面内容为项目中实际使用的 Prompt 模板原文。为了避免 Markdown 渲染，这里统一使用四个反引号包裹外层内容，因此模板内部的 `##`、列表和代码块都会按原样显示。

### 1. Initial (General)

````python
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
请严格返回 JSON 数组（注意：JSON 中不能使用 `10**18` 等编程表达式，必须写成完整数字如 `1000000000000000000`）：
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
````

### 2. Initial Prompt (AST-assisted Mode)

````python
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
请严格返回 JSON 数组（注意：JSON 中不能使用 `10**18` 等编程表达式，必须写成完整数字如 `1000000000000000000`）：
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
````

### 3. Supplement (JSON)

````python
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
````

### 4. Script Generation

#### 4.1 JavaScript branch

````python
if language == "javascript":
    framework_guide = f"""## 测试框架：Jest
## 导入方式
```javascript
const _{module_name}Module = require('../targets/{source_filename}');
const {module_name} = _{module_name}Module.default || _{module_name}Module;
```
## 要求
- 使用 describe/test/expect 结构
- 正确使用链式调用（如 {module_name}('2023-01-01').format('YYYY')）
- 异常测试使用 expect(() => {{ ... }}).toThrow()
- 请返回完整可运行的 Jest 测试文件代码"""
    code_block_lang = "javascript"
````

#### 4.2 Python branch

````python
if language == "python":
    framework_guide = f"""## 测试框架：pytest
## 导入方式
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from {module_name} import *
```
## 要求
- 使用 class + test_ 方法结构
- 异常测试使用 pytest.raises()
- 请返回完整可运行的 pytest 测试文件代码"""
    code_block_lang = "python"
````

#### 4.3 Prompt body

````python
prompt = f"""你是一个测试工程师。请根据以下源代码和 JSON 测试用例，生成一个完整的、可直接运行的测试脚本。

## 被测源代码（{language}）
```{language}
{source_code}
```

## JSON 测试用例
```json
{test_cases_json}
```

{framework_guide}

## 重要
- 根据每个测试用例的 description 和 input/expected_output 理解测试意图
- 如果 JSON 中的 expected_output 是描述性文字（如"对应的日期对象"），请根据源代码逻辑推断实际返回值
- 确保每个测试用例都被转化为可执行的测试方法
- 确保代码语法正确，所有括号、引号都正确闭合
- 只返回代码，用 ```{code_block_lang} ``` 包裹，不要包含其他解释文字"""
````

### 5. Fragment Supplement

#### 5.1 JavaScript example

````javascript
test('补充: 测试描述', () => {{
  const result = {module_name}('2023-01-01').someMethod();
  expect(result).toBe(expectedValue);
}});
````

#### 5.2 Python example

````python
def test_sup_001(self):
    result = some_function(args)
    assert result == expected_value
````

#### 5.3 Prompt body

````python
prompt = f"""你是一个测试工程师。当前测试的覆盖率不足，请针对未覆盖的代码生成 5-15 个补充测试方法。

## 当前覆盖率
- 语句覆盖率：{coverage_report.get('statement_coverage', 0):.1f}%
- 分支覆盖率：{coverage_report.get('branch_coverage', 0):.1f}%

## 未覆盖的代码片段
```
{snippet}
```

## 未覆盖的分支
{branches_str}

## 要求
- **只输出测试方法本身**，不要包含 import、require、describe、class 等外壳代码
- {format_hint}
- 确保代码语法正确，所有括号和引号正确闭合
- 只返回代码，用 ```{code_block_lang} ``` 包裹"""
````