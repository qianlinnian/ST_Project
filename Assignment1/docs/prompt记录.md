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


> convert number to word 实验对比结果
> LLM             模型                                用例数       耗时     语句覆盖     分支覆盖   轮次      通过/失败
> ------------------------------------------------------------------------------------------------
> deepseek        deepseek-chat                      25           101.1s    91.0%       92.3%      3        20/3
> openai          gpt-3.5-turbo                      26           25.7s     88.5%       88.5%      3        16/6
> google          gemini-2.5-flash                   39           127.5s    91.0%       92.3%      3        30/9
> github          gpt-4o-mini                        22           5.3s      91.0%       92.3%      3        16/3

