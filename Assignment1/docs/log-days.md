# 问题1输出
(st) D:\course_content\ST\ST_Project\Assignment1>python main.py --source targets/index.js --llm deepseek-chat --script
D:\anaconda3\envs\st\lib\site-packages\google\api_core\_python_version_support.py:275: FutureWarning: You are using a Python version (3.10.20) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
  warnings.warn(message, FutureWarning)
D:\course_content\ST\ST_Project\Assignment1\src\llm\client.py:17: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-chat
需求文档: 无
输出目录: output
对比模式: 否
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-chat)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 5 column 54 (char 126)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 38 个测试用例
    生成了 38 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（342 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern D:/course_content/ST/ST_Project/Assignment1/output/test_index_20260323_114953.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 70.2%  分支覆盖率: 61.5%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 5 column 23 (char 112)
[警告] 第二次解析失败: Expecting value: line 5 column 23 (char 112)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 17 个测试用例
    补充了 17 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（355 行）

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern D:/course_content/ST/ST_Project/Assignment1/output/test_index_20260323_114953.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 86.1%  分支覆盖率: 76.4%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 205 column 23 (char 6780)
[警告] 第二次解析失败: Expecting value: line 205 column 23 (char 6780)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 27 个测试用例
    补充了 27 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（366 行）

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern D:/course_content/ST/ST_Project/Assignment1/output/test_index_20260323_114953.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 0.0%  分支覆盖率: 0.0%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260323_114953.json
    test_file: output\test_index_20260323_114953.js

[完成] 总耗时: 608.8s

## 分析
第2轮已经到了 86.1%/76.4%，很接近达标了。但第3轮 LLM 生成的脚本可能有语法错误导致 Jest 完全无法运行，覆盖率变成 0。

问题是：每轮都让 LLM 重新生成整个脚本（82个用例 → 366行），用例越多越容易生成有错误的代码，反而破坏了之前好的结果。

解决方案：保留上一轮的最佳脚本，如果新脚本覆盖率反而下降，就回退到上一轮的版本。

# 问题2：回退机制生效但闭环补充持续失败
虽然加入了回退机制能保留最佳覆盖率的代码，但后续闭环补充轮次生成的脚本覆盖率都是 0%，导致每次都回退到第1轮结果，闭环无法实际提升覆盖率。

## 原因分析
1. **闭环补充时让 LLM 重新生成整个脚本**：随着用例累积（60+个），prompt 中包含已有脚本全文 + 源代码 + 未覆盖信息，内容过长导致 LLM 输出被截断（`SyntaxError: Unexpected end of input`），Jest 无法运行。
2. **语法错误的脚本覆盖了好的脚本**：截断的代码写入测试文件后覆盖率变为 0%。

## 解决策略
1. **补充片段拼接**：新增 `build_supplement_script_prompt`，闭环补充时只让 LLM 生成补充的 test 方法片段（不含 import/describe 外壳），由代码自动拼接到已有脚本的 `});` 前。prompt 只发送未覆盖行的代码片段（上下文3行），大幅减少 prompt 长度。
2. **语法检查**：拼接后用 `node --check`（JS）或 `ast.parse`（Python）验证语法，语法错误则丢弃本次补充。
3. **回退机制**：记录最佳覆盖率版本，覆盖率下降时自动回退，最终输出保证使用最佳版本。

# 问题3：采用了llm补充用例脚本后，覆盖率得到提升，但是准确率明显下降

| 测试项目 | LLM | 模型 | 用例数 | 耗时 | 语句覆盖 | 分支覆盖 | 轮次 | 通过/失败 | 时间 |
|----------|-----|------|--------|------|----------|----------|------|-----------|------|
| index.js | deepseek-chat | deepseek-chat | 108 | 401.3s | 26.9% | 19.8% | 3 | 0/108 | 2026-03-23 00:14:59 |
| index.js | deepseek-chat | deepseek-chat | 82 | 608.8s | 0.0% | 0.0% | 3 | 0/0 | 2026-03-23 11:56:33 |
| index.js | deepseek-chat | deepseek-chat | 96 | 580.8s | 69.3% | 62.6% | 3 | 33/0 | 2026-03-23 12:19:17 |
| index.js | deepseek-chat | deepseek-chat | 32 | 334.5s | 76.0% | 63.2% | 3 | 31/1 | 2026-03-23 12:40:56 |
| index.js | deepseek-chat | deepseek-chat | 38 | 365.5s | 72.7% | 63.7% | 3 | 37/1 | 2026-03-23 12:49:17 |
| index.js | deepseek-chat | deepseek-chat | 22 | 398.8s | 64.7% | 57.1% | 3 | 19/3 | 2026-03-23 13:06:18 |
| index.js | deepseek-chat | deepseek-chat | 36 | 262.4s | 76.5% | 63.7% | 3 | 33/58 | 2026-03-23 13:26:08 |
| index.js | deepseek-chat | deepseek-chat | 39 | 284.2s | 67.2% | 59.3% | 3 | 39/36 | 2026-03-23 13:52:59 |
| index.js | deepseek-reasoner | deepseek-reasoner | 27 | 498.0s | 97.1% | 85.2% | 2 | 28/17 | 2026-03-23 14:01:17 |
| index.js | github | gpt-4o-mini | 13 | 58.0s | 34.0% | 20.9% | 3 | 4/37 | 2026-03-23 14:06:03 |
前面的 准确率提升是因为采用了 llm生成可运行的测试脚本，覆盖率提升是因为 llm 生成了更多的测试用例并且能够触发更多的代码路径。但后续闭环补充时 llm 生成的脚本可能存在语法错误或逻辑错误，导致测试无法正确运行，覆盖率反而下降，准确率也明显下降。
## 原因分析
1. **用例质量下降**：闭环补充时 LLM 生成的用例可能更倾向于覆盖未覆盖行，但不一定符合正确的输入输出关系，导致测试用例的准确率下降。
2. **过拟合未覆盖行**：LLM 可能过度拟合未覆盖行的代码结构，生成的用例虽然能触发这些行，但输入输出不合理，导致测试失败率增加。
3. **语法错误导致测试失败**：补充脚本虽然通过了语法检查，但逻辑错误或不完整的代码片段可能导致测试运行时错误，进一步降低准确率。


