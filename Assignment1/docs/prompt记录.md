## Prompt Design (Report-ready, English)

This section summarizes the exact prompt templates used by the tool in different stages of the workflow. The templates are implemented in `src/llm/prompts.py` and are parameterized by source code, language, requirement text, and coverage feedback.

### 1. Initial Generation Prompt (General, no AST)

**Function:** `build_general_prompt(source_code, language, requirements=None)`

**Purpose:**
- Used for non-Python targets or cases where AST analysis is not available.
- Instructs the LLM to first infer structure (functions, branches, loops, exceptions, compound conditions), then generate JSON test cases.

**Coverage goals included in prompt:**
- Statement coverage
- Branch coverage (True/False directions)
- Condition coverage (sub-condition combinations)
- Path coverage

**Required output format:** strict JSON array only.

### 2. Initial Generation Prompt (Python with AST)

**Function:** `build_python_prompt(source_code, analysis, requirements=None)`

**Purpose:**
- Used for Python targets when structured AST analysis is available.
- Injects explicit structural data into the prompt:
    - Function list
    - Branch points (if/for/while/try)
    - Compound boolean conditions
    - Execution paths

**Why this version matters:**
- Reduces ambiguity from plain-text code reading.
- Improves first-round branch/path targeting.

**Required output format:** strict JSON array only.

### 3. Supplement Prompt (Coverage-feedback loop, JSON)

**Function:** `build_supplement_prompt(source_code, coverage_report, existing_tests)`

**Purpose:**
- Used when initial generated tests do not meet coverage expectations.
- Sends coverage metrics and uncovered line/branch information back to the LLM.
- Requests only incremental (non-duplicate) test cases.

**Prompt features:**
- Uncovered lines and branches are explicitly highlighted.
- Source code is line-numbered and annotated with uncovered marks.

**Required output format:** strict JSON array only.

### 4. Test Script Generation Prompt (`--script` mode)

**Function:** `build_script_prompt(source_code, test_cases_json, language, source_filename)`

**Purpose:**
- Converts JSON test cases into executable test scripts by asking the LLM to generate runnable code directly.
- Solves the expressiveness gap of JSON-only representation for method-chain APIs (e.g., Day.js).

**Language-adaptive behavior:**
- JavaScript: Jest + `describe/test/expect`, `toThrow()` for exception tests.
- Python: pytest + class/test methods, `pytest.raises()` for exception tests.

**Required output format:** code only, wrapped in the corresponding language code block.

### 5. Supplement Script Fragment Prompt (`--script` closed loop)

**Function:** `build_supplement_script_prompt(source_code, coverage_report, language, source_filename)`

**Purpose:**
- Used when script-mode coverage is still insufficient.
- Requests only additional test method fragments (not full file shell).

**Prompt features:**
- Includes uncovered code lines with nearby context (±3 lines).
- Lists uncovered branches.
- Requires syntax-correct method fragments that can be appended to existing test files.

**Required output format:** code fragment only, wrapped in the corresponding language code block.

### 6. Reporting Notes (can be copied into Method section)

- The report is written in English, while prompt execution language in experiments follows the actual implemented templates.
- All comparative results are valid under a controlled setting because each model is evaluated with the same prompt family and pipeline.
- Prompt variants are not ad-hoc text edits; they correspond to explicit workflow stages: initial generation, coverage feedback, script generation, and script supplementation.

---

# ***初始prompt***
    ``` json
    你是一个白盒测试专家。

    ## 源代码（{language}）
    ```{language}
    {source_code}
    ```
    {req_section}
    ## 任务
    2. **首先分析代码结构**：识别所有函数、分支（if/else/switch）、循环、异常处理和复合条件。
    3. **然后生成测试用例**，覆盖以下目标：
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
    请只返回 JSON，不要包含其他文字。
    ```


# ***补充生成的prompt***
    ``` json
    之前生成的测试用例覆盖率不足，请补充测试用例。

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
    请只返回 JSON，不要包含其他文字。
    ```

# 实验对比报告
## convert number to word 
> convert number to word 实验对比结果 （无需求文档）
| LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |
|-----|------|--------|------|----------|----------|------|-----------|------|
| deepseek-chat | deepseek-chat | 28 | 113.9s | 91.0% | 92.3% | 3 | 18/8 | 2026-03-22 16:24:51 |
| deepseek-reasoner | deepseek-reasoner | 28 | 483.8s | 91.0% | 92.3% | 3 | 16/11 | 2026-03-22 16:32:55 |
| google | gemini-2.5-flash | 44 | 151.4s | 91.0% | 92.3% | 3 | 39/4 | 2026-03-22 16:35:26 |
| github | gpt-4o-mini | 27 | 29.7s | 91.0% | 92.3% | 3 | 17/7 | 2026-03-22 16:35:56 |

> convert number to word 实验对比结果 （有需求文档）
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 29 | 105.0s | 91.0% | 92.3% | 3 | 22/5 | 2026-03-22 18:26:04 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 33 | 740.0s | 91.0% | 92.3% | 3 | 27/4 | 2026-03-22 18:38:24 |
| convert_number_to_words.py | google | gemini-2.5-flash | 38 | 189.7s | 91.0% | 92.3% | 3 | 33/4 | 2026-03-22 18:41:34 |
| convert_number_to_words.py | github | gpt-4o-mini | 18 | 24.2s | 85.9% | 84.6% | 3 | 8/7 | 2026-03-22 18:41:58 |

> convert number to word 实验对比结果 （使用了ast） 
| convert_number_to_words.py | deepseek-chat | deepseek-chat | 18 | 94.0s | 91.0% | 92.3% | 1 | 17/1 | 2026-03-22 22:58:11 |
| convert_number_to_words.py | deepseek-reasoner | deepseek-reasoner | 23 | 271.5s | 91.0% | 92.3% | 1 | 20/3 | 2026-03-22 23:02:43 |
| convert_number_to_words.py | google | gemini-2.5-flash | 26 | 97.6s | 91.0% | 92.3% | 1 | 23/3 | 2026-03-22 23:04:21 |
| convert_number_to_words.py | github | gpt-4o-mini | 22 | 32.7s | 91.0% | 92.3% | 1 | 20/2 | 2026-03-22 23:04:53 |

## dayjs
> Days.js实验对比结果 （无需求文档，此时还没有 --script模式，llm只生成对应的 json 测试用例，不生成测试脚本，所以覆盖率偏低。）
| LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |
|-----|------|--------|------|----------|----------|------|-----------|------|
| deepseek-chat | deepseek-chat | 96 | 335.8s | 26.9% | 19.8% | 3 | 0/96 | 2026-03-22 17:12:44 |
| deepseek-reasoner | deepseek-reasoner | 40 | 428.0s | 43.3% | 32.4% | 3 | 0/40 | 2026-03-22 17:19:52 |
| google | gemini-2.5-flash | 280 | 464.2s | 58.4% | 44.0% | 3 | 1/279 | 2026-03-22 17:27:36 |
| github | gpt-4o-mini | 31 | 56.4s | 26.5% | 18.7% | 3 | 0/31 | 2026-03-22 17:28:33 |

> Day.js实验对比结果 （有需求文档，此时还没有 --script模式，llm只生成对应的 json 测试用例，不生成测试脚本，所以覆盖率偏低。）
| 测试项目 | LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |
|----------|-----|------|--------|------|----------|----------|------|-----------|------|
| index.js | deepseek-chat | deepseek-chat | 66 | 350.9s | 38.2% | 28.6% | 3 | 7/59 | 2026-03-22 17:56:17 |
| index.js | deepseek-reasoner | deepseek-reasoner | 98 | 670.3s | 66.4% | 51.1% | 3 | 4/94 | 2026-03-22 18:07:28 |
| index.js | google | gemini-2.5-flash | 372 | 534.9s | 31.1% | 18.1% | 3 | 0/372 | 2026-03-22 18:16:23 |
| index.js | github | gpt-4o-mini | 26 | 46.9s | 26.9% | 19.8% | 3 | 0/26 | 2026-03-22 18:17:09 |

## 分析
dayjs 是一个链式调用的库，其内部方法（如 format()、startOf()、isValid() 等）需要通过 dayjs(date).method() 的方式调用才能触发对应代码路径。但 LLM 生成的测试用例是 JSON 格式（包含 input 和 expected_output），工具将其转换为 Jest 测试代码时，只能生成 index(input) 这样的构造函数调用，无法自动生成链式方法调用。因此只覆盖了构造函数部分的代码（约 30%），内部方法的代码未被执行。

相比之下，Python 被测项目（convert_number_to_words）是纯函数式的，输入输出都是简单类型（数字→字符串），LLM 生成的用例可以直接转换为有效的函数调用和断言，覆盖率可达 91%+。

结论： 当前工具更适合测试纯函数式代码，对于链式调用风格的库（如 dayjs），JSON 用例格式的表达能力有限，是后续可优化的方向。


# ***含有AST的prompt***
    ``` json
    你是一个白盒测试专家。请根据以下源代码和代码结构分析，生成全面的白盒测试用例。

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
    请只返回 JSON，不要包含其他文字。
    ```
## 实验报告
> 这里是 前面使用ast 的python的部分。


# ***测试脚本生成prompt（自适应输出模式）***
    ```
    你是一个测试工程师。请根据以下源代码和 JSON 测试用例，生成一个完整的、可直接运行的测试脚本。

    ## 被测源代码（{language}）
    ```{language}
    {source_code}
    ```

    ## JSON 测试用例
    ```json
    {test_cases_json}
    ```

    ## 测试框架：Jest / pytest
    ## 导入方式
    （根据语言提供对应的 import/require 示例）

    ## 要求
    - 使用 describe/test/expect（JS）或 class + test_ 方法（Python）结构
    - 正确使用链式调用（如 module('2023-01-01').format('YYYY')）
    - 异常测试使用 expect(() => { ... }).toThrow()（JS）或 pytest.raises()（Python）
    - 请返回完整可运行的测试文件代码

    ## 重要
    - 根据每个测试用例的 description 和 input/expected_output 理解测试意图
    - 如果 JSON 中的 expected_output 是描述性文字（如"对应的日期对象"），请根据源代码逻辑推断实际返回值
    - 确保每个测试用例都被转化为可执行的测试方法
    - 确保代码语法正确，所有括号、引号都正确闭合
    - 只返回代码，用 ```{language} ``` 包裹，不要包含其他解释文字
    ```

## 说明
该 prompt 用于 `--script` 模式的首次脚本生成。与初始 prompt 不同，初始 prompt 让 LLM 输出 JSON 测试用例，而该 prompt 将 JSON 用例 + 源代码一起发给 LLM，让其直接生成可运行的测试脚本代码。解决了 JSON 格式无法表达链式调用（如 dayjs().format()）的问题。


# ***补充测试方法片段prompt（script闭环补充）***
    ```
    你是一个测试工程师。当前测试的覆盖率不足，请针对未覆盖的代码生成 5-15 个补充测试方法。

    ## 当前覆盖率
    - 语句覆盖率：{statement_coverage}%
    - 分支覆盖率：{branch_coverage}%

    ## 未覆盖的代码片段
    ```
    （仅包含未覆盖行及上下文3行，标注 // NOT COVERED）
    ```

    ## 未覆盖的分支
    （未覆盖分支列表）

    ## 要求
    - **只输出测试方法本身**，不要包含 import、require、describe、class 等外壳代码
    - 每个测试方法格式如下：
    ```javascript
      test('补充: 测试描述', () => {
        const result = module('2023-01-01').someMethod();
        expect(result).toBe(expectedValue);
      });
    ```
    - 确保代码语法正确，所有括号和引号正确闭合
    - 只返回代码，用 ```{language} ``` 包裹
    ```

## 说明
该 prompt 用于 `--script` 模式的闭环补充阶段。与"补充生成的prompt"不同：
1. **输出格式不同**：补充生成 prompt 输出 JSON 用例，该 prompt 直接输出可运行的测试方法代码片段
2. **只输出片段**：不包含 import/describe 等外壳代码，由程序自动拼接到已有脚本的 `});` 前
3. **精简输入**：不发送源代码全文和已有脚本全文，只发送未覆盖行及上下文（前后3行），大幅减少 prompt 长度，避免 LLM 输出被截断导致语法错误

#