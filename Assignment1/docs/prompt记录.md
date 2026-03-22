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

> Days.js实验对比结果 （无需求文档）
| LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |
|-----|------|--------|------|----------|----------|------|-----------|------|
| deepseek-chat | deepseek-chat | 96 | 335.8s | 26.9% | 19.8% | 3 | 0/96 | 2026-03-22 17:12:44 |
| deepseek-reasoner | deepseek-reasoner | 40 | 428.0s | 43.3% | 32.4% | 3 | 0/40 | 2026-03-22 17:19:52 |
| google | gemini-2.5-flash | 280 | 464.2s | 58.4% | 44.0% | 3 | 1/279 | 2026-03-22 17:27:36 |
| github | gpt-4o-mini | 31 | 56.4s | 26.5% | 18.7% | 3 | 0/31 | 2026-03-22 17:28:33 |

> Day.js实验对比结果 （有需求文档）
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

