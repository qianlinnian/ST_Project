"""
Prompt templates
Purpose: build structured prompts that guide the LLM to generate white-box test cases.
Includes three prompts:
  1. Initial generation (with AST analysis results, for Python)
  2. General mode (no AST, non-Python languages, LLM analyzes the code structure itself)
  3. Supplement generation (feedback round when coverage is insufficient)
"""

import json
from typing import Dict, Any, Optional, List


def build_general_prompt(source_code: str, language: str,
                         requirements: Optional[str] = None) -> str:
    """
    Build the general-mode prompt (for non-Python languages, without AST analysis).
    The LLM analyzes the code structure on its own before generating test cases.

    :param source_code: Source code content
    :param language: Programming language name, such as "javascript" or "java"
    :param requirements: Optional requirements document
    :return: Complete prompt string
    """
    req_section = ""
    if requirements:
        req_section = f"\n## Requirements\n{requirements}\n"

    prompt = f"""You are a white-box testing expert.

## Source Code ({language})
```{language}
{source_code}
```
{req_section}
## Task
1. **First analyze the code structure**: identify all functions, branches (if/else/switch), loops, exception handling, and compound conditions.
2. **Then generate test cases** that cover the following goals:
   - Statement coverage: cover every executable line
   - Branch coverage: cover both True and False outcomes of each branch
   - Condition coverage: cover each sub-condition combination in compound expressions
   - Path coverage: cover all feasible execution paths

## Output Format
Please return a strict JSON array only (note: JSON cannot contain programming expressions such as `10**18`; write the full number instead, such as `1000000000000000000`):
```json
[
  {{
    "id": "TC001",
    "description": "Test description",
    "input": {{"parameter_name": value}},
    "expected_output": "Expected output",
    "covered_branches": ["Branch description"],
    "covered_paths": ["Path description"]
  }}
]
```
Please return JSON only, with no other text."""
    return prompt


def build_python_prompt(source_code: str, analysis: Dict[str, Any],
                        requirements: Optional[str] = None) -> str:
    """
    Build the initial-generation prompt (for Python, with AST analysis results).
    The source code and the AST-derived function, branch, condition, and path information
    are sent together to the LLM so it can generate high-coverage test cases.

    :param source_code: Python source code
    :param analysis: Structured analysis result returned by PythonAnalyzer.analyze()
    :param requirements: Optional requirements document content
    :return: Complete prompt string
    """
    # 将分析结果格式化为可读字符串
    functions_str = json.dumps(analysis["functions"], indent=2, ensure_ascii=False)
    branches_str = json.dumps(analysis["branches"], indent=2, ensure_ascii=False)
    conditions_str = json.dumps(analysis["conditions"], indent=2, ensure_ascii=False)
    paths_str = json.dumps(analysis["paths"], indent=2, ensure_ascii=False)
    print(f"Running build_python_prompt\n")
    # 需求文档部分（可选）
    req_section = ""
    if requirements:
        req_section = f"\n## Requirements\n{requirements}\n"

    prompt = f"""You are a white-box testing expert. Please generate comprehensive white-box test cases based on the source code and the code structure analysis below.

## Source Code
```python
{source_code}
```

## Code Structure Analysis (from AST)

### Function List
{functions_str}

### Branch Points (if/for/while/try)
{branches_str}

### Compound Conditions (and/or expressions)
{conditions_str}

### Execution Paths
{paths_str}
{req_section}
## Task
Generate test cases to achieve the following coverage goals:
1. **Statement coverage**: cover every executable line
2. **Branch coverage**: cover both True and False outcomes of each branch
3. **Condition coverage**: cover every True/False combination of each sub-condition in a compound expression
4. **Path coverage**: cover all feasible execution paths

## Output Format
Please return a strict JSON array only (note: JSON cannot contain programming expressions such as `10**18`; write the full number instead, such as `1000000000000000000`):
```json
[
  {{
    "id": "TC001",
    "description": "Test description (explain which branch/condition/path is covered)",
    "input": {{"parameter_name": value}},
    "expected_output": "Expected output",
    "covered_branches": ["L line number: condition → True/False"],
    "covered_paths": ["Path description"]
  }}
]
```
Please return JSON only, with no other text."""
    return prompt


def build_supplement_prompt(source_code: str, coverage_report: Dict[str, Any],
                            existing_tests: List[Dict]) -> str:
    """
    Build the supplement-generation prompt (feedback round when coverage is insufficient).
    The current coverage report and uncovered line/branch information are fed back to the LLM
    so it can generate supplementary tests.

    :param source_code: Source code content
    :param coverage_report: Coverage report, including statement_coverage and uncovered_lines
    :param existing_tests: Existing test case list
    :return: Complete prompt string
    """
    # 在源代码中标注未覆盖的行
    lines = source_code.splitlines()
    uncovered = set(coverage_report.get("uncovered_lines", []))
    annotated_lines = []
    for i, line in enumerate(lines, 1):
        marker = " ✗ Uncovered" if i in uncovered else ""
        annotated_lines.append(f"{i:4d} | {line}{marker}")
    annotated_source = "\n".join(annotated_lines)

    # 格式化未覆盖分支
    uncovered_branches = coverage_report.get("uncovered_branches", [])
    branches_str = "\n".join(f"  - {b}" for b in uncovered_branches) if uncovered_branches else "  none"

    prompt = f"""The previously generated test cases do not provide sufficient coverage. Please add supplementary test cases.

## Current Coverage
- Statement coverage: {coverage_report.get('statement_coverage', 0):.1f}%
- Branch coverage: {coverage_report.get('branch_coverage', 0):.1f}%

## Uncovered Code Lines
{list(uncovered)}

## Uncovered Branches
{branches_str}

## Source Code (with uncovered lines annotated)
```
{annotated_source}
```

## Number of Existing Test Cases: {len(existing_tests)}

## Task
Please generate **only supplementary test cases**, focusing specifically on the uncovered lines and branches above.
Do not duplicate existing test cases.

## Output Format
Please return a strict JSON array only:
```json
[
  {{
    "id": "TC_SUP_001",
    "description": "Supplementary test description",
    "input": {{"parameter_name": value}},
    "expected_output": "Expected output",
    "covered_branches": ["Target uncovered branch"],
    "covered_paths": ["Target uncovered path"]
  }}
]
```
Please return JSON only, with no other text."""
    return prompt


def build_script_prompt(source_code: str, test_cases_json: str,
                        language: str, source_filename: str) -> str:
    """
    Build the test-script generation prompt (adaptive output mode).
    The LLM directly generates runnable test scripts from JSON test cases plus source code.

    :param source_code: Source code under test
    :param test_cases_json: Test cases in JSON string format
    :param language: Programming language (python / javascript)
    :param source_filename: Source file name under test
    :return: Prompt string
    """
    module_name = source_filename.rsplit(".", 1)[0]

    if language == "javascript":
        framework_guide = f"""## Test Framework: Jest
## Import style
```javascript
const _{module_name}Module = require('../targets/{source_filename}');
const {module_name} = _{module_name}Module.default || _{module_name}Module;
```
## Requirements
- Use a describe/test/expect structure
- Use chained calls correctly (for example, {module_name}('2023-01-01').format('YYYY'))
- Use expect(() => {{ ... }}).toThrow() for exception tests
- Return a complete runnable Jest test file"""
        code_block_lang = "javascript"
    else:
        framework_guide = f"""## Test Framework: pytest
## Import style
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'targets'))
from {module_name} import *
```
## Requirements
- Use a class + test_ method structure
- Use pytest.raises() for exception tests
- Return a complete runnable pytest test file"""
        code_block_lang = "python"

    prompt = f"""You are a test engineer. Please generate a complete, runnable test script from the source code and JSON test cases below.

## Source Code Under Test ({language})
```{language}
{source_code}
```

## JSON Test Cases
```json
{test_cases_json}
```

{framework_guide}

## Important
- Infer the test intent from each test case's description and input/expected_output
- If expected_output in the JSON is descriptive text (for example, "the corresponding date object"), infer the actual return value from the source code logic
- Ensure every test case is converted into an executable test method
- Ensure the code syntax is correct, with all parentheses and quotes properly closed
- Return code only, wrapped in ```{code_block_lang} ``` and do not include any other explanation text"""

    return prompt


def build_supplement_script_prompt(source_code: str, coverage_report: Dict[str, Any],
                                   language: str, source_filename: str) -> str:
    """
    Build the supplementary test-method-fragment prompt (used in the script feedback loop).
    Only the supplementary test method fragment is generated, without import/describe scaffolding.
    The caller appends it to the existing script.

    :param source_code: Source code under test
    :param coverage_report: Current coverage report
    :param language: Programming language
    :param source_filename: Source file name under test
    :return: Prompt string
    """
    module_name = source_filename.rsplit(".", 1)[0]

    # 提取未覆盖行及上下文
    lines = source_code.splitlines()
    uncovered = set(coverage_report.get("uncovered_lines", []))
    relevant_lines = set()
    for line_no in uncovered:
        for i in range(max(1, line_no - 3), min(len(lines) + 1, line_no + 4)):
            relevant_lines.add(i)
    snippet_lines = []
    for i in sorted(relevant_lines):
        marker = " // NOT COVERED" if i in uncovered else ""
        snippet_lines.append(f"{i:4d} | {lines[i-1]}{marker}")
    snippet = "\n".join(snippet_lines)

    uncovered_branches = coverage_report.get("uncovered_branches", [])
    branches_str = "\n".join(f"  - {b}" for b in uncovered_branches) if uncovered_branches else "  none"

    code_block_lang = "javascript" if language == "javascript" else "python"

    if language == "javascript":
        format_hint = f"""Each test method should follow this format (use 2-space indentation and the function name {module_name}):
```javascript
  test('Supplementary: test description', () => {{
    const result = {module_name}('2023-01-01').someMethod();
    expect(result).toBe(expectedValue);
  }});
```"""
    else:
        format_hint = f"""Each test method should follow this format (use 8-space indentation):
```python
    def test_sup_001(self):
        result = some_function(args)
        assert result == expected_value
```"""

    prompt = f"""You are a test engineer. The current test coverage is insufficient, so please generate 5-15 supplementary test methods for the uncovered code.

## Current Coverage
- Statement coverage: {coverage_report.get('statement_coverage', 0):.1f}%
- Branch coverage: {coverage_report.get('branch_coverage', 0):.1f}%

## Uncovered Code Snippet
```
{snippet}
```

## Uncovered Branches
{branches_str}

## Requirements
- **Output only the test methods themselves**, without import, require, describe, class, or other scaffolding
- {format_hint}
- Ensure the code syntax is correct, with all parentheses and quotes properly closed
- Return code only, wrapped in ```{code_block_lang} ```"""

    return prompt