
D:\course\ST\ST_Project\Assignment1\src\llm\client.py:17: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: google
需求文档: 无
输出目录: output
对比模式: 否
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 第二次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 130 个测试用例
    生成了 130 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（954 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
需求文档: 无
输出目录: output
对比模式: 否
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 第二次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 130 个测试用例
    生成了 130 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（954 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
对比模式: 否
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 第二次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 130 个测试用例
    生成了 130 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（954 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 第二次解析失败: Expecting value: line 242 column 18 (char 7304)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 130 个测试用例
    生成了 130 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（954 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
    生成了 130 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（954 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
[Script] 成功生成测试脚本（954 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...

[闭环] 第 1/3 轮 - 运行覆盖率测量...
[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern D:/course/ST/ST_Project/Assignment1/output/test_index_20260402_143811.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 94.1%  分支覆盖率: 86.8%
    语句覆盖率: 94.1%  分支覆盖率: 86.8%
    覆盖率达标，闭环结束。


[保存] 输出文件...
    test_cases: output\test_cases_index_20260402_143811.json
    test_file: output\test_index_20260402_143811.js

[完成] 总耗时: 282.2s