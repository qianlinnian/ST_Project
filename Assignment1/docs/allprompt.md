# All Prompt Templates

The content below is the exact prompt text used in the project. To avoid Markdown rendering, the outer layer uses four backticks, so the inner `##`, lists, and code blocks are shown literally.

### 1. Initial (General)

````python
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
````

### 2. Initial Prompt (AST-assisted Mode)

````python
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
````

### 3. Supplement (JSON)

````python
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
````

### 4. Script Generation

#### 4.1 JavaScript branch

````python
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
````

#### 4.2 Python branch

````python
if language == "python":
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
````

#### 4.3 Prompt body

````python
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
````

### 5. Fragment Supplement

#### 5.1 JavaScript example

````javascript
test('Supplementary: test description', () => {{
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
````