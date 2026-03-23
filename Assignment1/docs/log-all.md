> 这个是普通的 日志输出，里面有一部分内容是可以体现 不同 轮次之间的对比的，一部分输出可以体现出 闭环输出的 作用可以提高 覆盖率。
> 不是全部的！all指的是包含大多数的测试指令的输出（因为后面有更新参数，所有一些没有留存下来，所以是大多数不是全部）

============================================================

============================================================
▶ 使用 deepseek-chat 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-chat
需求文档: 无
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-chat)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 5 column 54 (char 130)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 33 个测试用例
    生成了 33 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_170856.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.2%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 45 column 23 (char 2269)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 33 个测试用例
    补充了 33 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_170856.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.8%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 45 column 23 (char 2460)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 30 个测试用例
    补充了 30 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_170856.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.8%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_170856.json
    test_file: output\test_index_20260322_170856.js

[完成] 总耗时: 335.8s

============================================================
▶ 使用 deepseek-reasoner 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-reasoner
需求文档: 无
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-reasoner)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 5 column 23 (char 140)
[警告] 第二次解析失败: Expecting value: line 5 column 23 (char 140)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 15 个测试用例
    生成了 15 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_171614.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 41.2%  分支覆盖率: 24.7%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 54 column 15 (char 1840)
[警告] 第二次解析失败: Expecting value: line 54 column 15 (char 1840)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 6 个测试用例
    补充了 6 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_171614.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 41.2%  分支覆盖率: 24.7%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 29 column 23 (char 1106)
[警告] 第二次解析失败: Expecting value: line 29 column 23 (char 1106)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 19 个测试用例
    补充了 19 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_171614.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 43.3%  分支覆盖率: 32.4%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_171614.json
    test_file: output\test_index_20260322_171614.js

[完成] 总耗时: 428.0s

============================================================
▶ 使用 google 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: google
需求文档: 无
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
    生成了 98 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_172248.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 30.2%  分支覆盖率: 25.8%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 125 column 19 (char 3065)
[警告] 第二次解析失败: Expecting value: line 125 column 19 (char 3065)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 107 个测试用例
    补充了 107 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_172248.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 58.4%  分支覆盖率: 44.0%
    覆盖率不足，生成补充测试用例...
    补充了 75 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_172248.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 58.4%  分支覆盖率: 44.0%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_172248.json
    test_file: output\test_index_20260322_172248.js

[完成] 总耗时: 464.2s

============================================================
▶ 使用 github 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: github
需求文档: 无
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (github)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 61 column 30 (char 2433)
[警告] 第二次解析失败: Expecting value: line 61 column 30 (char 2433)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 10 个测试用例
    生成了 10 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_172751.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 22.7%  分支覆盖率: 7.7%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 29 column 23 (char 1064)
[警告] 第二次解析失败: Expecting value: line 29 column 23 (char 1064)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 7 个测试用例
    补充了 7 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_172751.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 24.8%  分支覆盖率: 11.5%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 117 column 25 (char 3752)
[警告] 第二次解析失败: Expecting value: line 117 column 25 (char 3752)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 14 个测试用例
    补充了 14 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_172751.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.5%  分支覆盖率: 18.7%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_172751.json
    test_file: output\test_index_20260322_172751.js

[完成] 总耗时: 56.4s

============================================================

============================================================
实验对比结果
============================================================
LLM             模型                                用例数       耗时     语句覆盖     分支覆盖   轮次      通过/失败
------------------------------------------------------------------------------------------------
deepseek-chat   deepseek-chat                      96   335.8s    26.9%    19.8%    3    0/96
deepseek-reasoner deepseek-reasoner                  40   428.0s    43.3%    32.4%    3    0/40
google          gemini-2.5-flash                  280   464.2s    58.4%    44.0%    3    1/279
github          gpt-4o-mini                        31    56.4s    26.5%    18.7%    3    0/31

对比报告已保存: output\comparison_report.md
(st) d:\course_content\ST\ST_Project\Assignment1>python main.py --source targets/index.js --compare --requirement targets/requirements_index.md
D:\anaconda3\envs\st\lib\site-packages\google\api_core\_python_version_support.py:275: FutureWarning: You are using a Python version (3.10.20) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
  warnings.warn(message, FutureWarning)
d:\course_content\ST\ST_Project\Assignment1\src\llm\client.py:17: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
对比模式：将使用以下 LLM 后端运行: deepseek-chat, deepseek-reasoner, google, github
============================================================

============================================================
▶ 使用 deepseek-chat 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-chat
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-chat)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 93 column 31 (char 4759)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 29 个测试用例
    生成了 29 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_175222.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 38.2%  分支覆盖率: 28.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 29 column 23 (char 1118)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 32 个测试用例
    补充了 32 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_175222.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 38.2%  分支覆盖率: 28.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 37 column 23 (char 1766)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 5 个测试用例
    补充了 5 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_175222.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 38.2%  分支覆盖率: 28.6%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_175222.json
    test_file: output\test_index_20260322_175222.js

[完成] 总耗时: 350.9s

============================================================
▶ 使用 deepseek-reasoner 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-reasoner
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-reasoner)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 13 column 23 (char 425)
[警告] 第二次解析失败: Expecting value: line 13 column 23 (char 425)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 48 个测试用例
    生成了 48 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_175923.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 65.1%  分支覆盖率: 50.0%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting property name enclosed in double quotes: line 29 column 51 (char 1322)
[警告] 第二次解析失败: Expecting property name enclosed in double quotes: line 29 column 51 (char 1322)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 23 个测试用例
    补充了 23 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_175923.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 66.4%  分支覆盖率: 50.5%
    覆盖率不足，生成补充测试用例...
    补充了 27 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_175923.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 66.4%  分支覆盖率: 51.1%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_175923.json
    test_file: output\test_index_20260322_175923.js

[完成] 总耗时: 670.3s

============================================================
▶ 使用 google 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: google
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting ',' delimiter: line 2428 column 6 (char 69474)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 149 个测试用例
    生成了 149 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_181132.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 25.2%  分支覆盖率: 12.6%
    覆盖率不足，生成补充测试用例...
    补充了 127 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_181132.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.1%  分支覆盖率: 12.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 132 column 20 (char 3460)
[警告] 第二次解析失败: Expecting value: line 132 column 20 (char 3460)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 96 个测试用例
    补充了 96 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_181132.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 31.1%  分支覆盖率: 18.1%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_181132.json
    test_file: output\test_index_20260322_181132.js

[完成] 总耗时: 534.9s

============================================================
▶ 使用 github 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: github
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (github)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 13 column 23 (char 320)
[警告] 第二次解析失败: Expecting value: line 13 column 23 (char 320)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 14 个测试用例
    生成了 14 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_181635.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.2%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 29 column 23 (char 1047)
[警告] 第二次解析失败: Expecting value: line 29 column 23 (char 1047)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 7 个测试用例
    补充了 7 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_181635.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.8%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 21 column 23 (char 841)
[警告] 第二次解析失败: Expecting value: line 21 column 23 (char 841)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 5 个测试用例
    补充了 5 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_181635.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.8%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_181635.json
    test_file: output\test_index_20260322_181635.js

[完成] 总耗时: 46.9s

============================================================
实验对比结果
============================================================
测试项目                                LLM             模型                                用例数       耗时     语句覆盖     分支覆盖   轮次      通过/失败        
------------------------------------------------------------------------------------------------------------------------------------
index.js                            deepseek-chat   deepseek-chat                      96   335.8s    26.9%    19.8%    3    0/96
index.js                            deepseek-reasoner deepseek-reasoner                  40   428.0s    43.3%    32.4%    3    0/40
index.js                            google          gemini-2.5-flash                  280   464.2s    58.4%    44.0%    3    1/279
index.js                            github          gpt-4o-mini                        31    56.4s    26.5%    18.7%    3    0/31
index.js                            deepseek-chat   deepseek-chat                      66   350.9s    38.2%    28.6%    3    7/59
index.js                            deepseek-reasoner deepseek-reasoner                  98   670.3s    66.4%    51.1%    3    4/94
index.js                            google          gemini-2.5-flash                  372   534.9s    31.1%    18.1%    3    0/372
index.js                            github          gpt-4o-mini                        26    46.9s    26.9%    19.8%    3    0/26

对比报告已保存: output\comparison_report.md

(st) d:\course_content\ST\ST_Project\Assignment1>
(st) d:\course_content\ST\ST_Project\Assignment1>
(st) d:\course_content\ST\ST_Project\Assignment1>python main.py --source targets/index.js --compare --requirement targets/requirements_index.md
(st) d:\course_content\ST\ST_Project\Assignment1># Python 项目对比（带需求文档）
'#' 不是内部或外部命令，也不是可运行的程序
或批处理文件。

(st) d:\course_content\ST\ST_Project\Assignment1>python main.py --source targets/convert_number_to_words.py --compare --requirement targets/requirements_convert_number_to_words.md
D:\anaconda3\envs\st\lib\site-packages\google\api_core\_python_version_support.py:275: FutureWarning: You are using a Python version (3.10.20) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
  warnings.warn(message, FutureWarning)
d:\course_content\ST\ST_Project\Assignment1\src\llm\client.py:17: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
对比模式：将使用以下 LLM 后端运行: deepseek-chat, deepseek-reasoner, google, github
============================================================

============================================================
▶ 使用 deepseek-chat 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: deepseek-chat
需求文档: targets/requirements_convert_number_to_words.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-chat)...
[4] 解析 LLM 响应...
    生成了 25 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_182546.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 2 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_182546.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 2 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_182546.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260322_182546.json
    test_file: output\test_convert_number_to_words_20260322_182546.py

[完成] 总耗时: 105.0s

============================================================
▶ 使用 deepseek-reasoner 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: deepseek-reasoner
需求文档: targets/requirements_convert_number_to_words.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-reasoner)...
[4] 解析 LLM 响应...
    生成了 29 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_183028.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 2 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_183028.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 2 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_183028.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260322_183028.json
    test_file: output\test_convert_number_to_words_20260322_183028.py

[完成] 总耗时: 740.0s

============================================================
▶ 使用 google 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: google
需求文档: targets/requirements_convert_number_to_words.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
    生成了 35 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_184016.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 1 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_184016.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 2 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_184016.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260322_184016.json
    test_file: output\test_convert_number_to_words_20260322_184016.py

[完成] 总耗时: 189.7s

============================================================
▶ 使用 github 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: github
需求文档: targets/requirements_convert_number_to_words.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (github)...
[4] 解析 LLM 响应...
    生成了 11 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_184144.py -v
    语句覆盖率: 85.9%  分支覆盖率: 84.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting ',' delimiter: line 29 column 24 (char 926)
[警告] 第二次解析失败: Expecting ',' delimiter: line 29 column 24 (char 926)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 4 个测试用例
    补充了 4 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_184144.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率不足，生成补充测试用例...
    补充了 3 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260322_184144.py -v
    语句覆盖率: 85.9%  分支覆盖率: 84.6%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260322_184144.json
    test_file: output\test_convert_number_to_words_20260322_184144.py

[完成] 总耗时: 24.2s

============================================================
实验对比结果
============================================================
测试项目                                LLM             模型                                用例数       耗时     语句覆盖     分支覆盖   轮次      通过/失败        
------------------------------------------------------------------------------------------------------------------------------------
convert_number_to_words.py          deepseek-chat   deepseek-chat                      28   113.9s    91.0%    92.3%    3   18/8
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  28   483.8s    91.0%    92.3%    3   16/11
convert_number_to_words.py          google          gemini-2.5-flash                   44   151.4s    91.0%    92.3%    3   39/4
convert_number_to_words.py          github          gpt-4o-mini                        27    29.7s    91.0%    92.3%    3   17/7
convert_number_to_words.py          deepseek-chat   deepseek-chat                      29   105.0s    91.0%    92.3%    3   22/5
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  33   740.0s    91.0%    92.3%    3   27/4
convert_number_to_words.py          google          gemini-2.5-flash                   38   189.7s    91.0%    92.3%    3   33/4
convert_number_to_words.py          github          gpt-4o-mini                        18    24.2s    85.9%    84.6%    3    8/7

对比报告已保存: output\comparison_report.md

(st) d:\course_content\ST\ST_Project\Assignment1>
(st) d:\course_content\ST\ST_Project\Assignment1># JS 项目对比（带需求文档）
'#' 不是内部或外部命令，也不是可运行的程序
或批处理文件。

(st) d:\course_content\ST\ST_Project\Assignment1>python main.py --source targets/index.js --compare --requirement targets/requirements_index.md
D:\anaconda3\envs\st\lib\site-packages\google\api_core\_python_version_support.py:275: FutureWarning: You are using a Python version (3.10.20) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
  warnings.warn(message, FutureWarning)
d:\course_content\ST\ST_Project\Assignment1\src\llm\client.py:17: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
对比模式：将使用以下 LLM 后端运行: deepseek-chat, deepseek-reasoner, google, github
============================================================

============================================================
▶ 使用 deepseek-chat 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-chat
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-chat)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 93 column 31 (char 4368)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 30 个测试用例
    生成了 30 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_184344.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 38.2%  分支覆盖率: 28.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 37 column 23 (char 1363)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 24 个测试用例
    补充了 24 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_184344.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 38.2%  分支覆盖率: 28.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 1 column 1 (char 0)
[警告] 第二次解析失败: Expecting value: line 37 column 23 (char 1810)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 30 个测试用例
    补充了 30 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_184344.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 38.2%  分支覆盖率: 28.6%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_184344.json
    test_file: output\test_index_20260322_184344.js

[完成] 总耗时: 320.1s

============================================================
▶ 使用 deepseek-reasoner 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: deepseek-reasoner
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-reasoner)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 176 column 17 (char 4163)
[警告] 第二次解析失败: Expecting value: line 176 column 17 (char 4163)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 54 个测试用例
    生成了 54 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_185044.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.1%  分支覆盖率: 12.6%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting property name enclosed in double quotes: line 13 column 42 (char 422)
[警告] 第二次解析失败: Expecting property name enclosed in double quotes: line 13 column 42 (char 422)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 16 个测试用例
    补充了 16 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_185044.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 28.1%  分支覆盖率: 20.3%
    覆盖率不足，生成补充测试用例...
    补充了 35 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_185044.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 28.1%  分支覆盖率: 20.3%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_185044.json
    test_file: output\test_index_20260322_185044.js

[完成] 总耗时: 543.5s

============================================================
▶ 使用 google 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: google
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
    生成了 97 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_185806.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.1%  分支覆盖率: 16.5%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 162 column 16 (char 3891)
[警告] 第二次解析失败: Expecting value: line 162 column 16 (char 3891)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 76 个测试用例
    补充了 76 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_185806.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 48.7%  分支覆盖率: 33.5%
    覆盖率不足，生成补充测试用例...
[错误] google 运行失败: [Google] API 免费额度已用完，请稍后重试或更换模型。详情: https://ai.google.dev/gemini-api/docs/rate-limits

============================================================
▶ 使用 github 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/index.js
LLM: github
需求文档: targets/requirements_index.md
输出目录: output
对比模式: 是
最大闭环轮次: 3
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/index.js (语言: javascript)
[2] 构建 Prompt...
[3] 调用 LLM (github)...
[4] 解析 LLM 响应...
[警告] 第一次解析失败: Expecting value: line 13 column 23 (char 320)
[警告] 第二次解析失败: Expecting value: line 13 column 23 (char 320)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 14 个测试用例
    生成了 14 个测试用例

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_190051.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 18.7%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 29 column 23 (char 1107)
[警告] 第二次解析失败: Expecting value: line 29 column 23 (char 1107)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 7 个测试用例
    补充了 7 个测试用例

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_190051.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.2%
    覆盖率不足，生成补充测试用例...
[警告] 第一次解析失败: Expecting value: line 29 column 23 (char 1058)
[警告] 第二次解析失败: Expecting value: line 29 column 23 (char 1058)
[警告] 尝试逐个提取 JSON 对象...
[修复] 逐个提取成功，得到 9 个测试用例
    补充了 9 个测试用例

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: npx jest --testPathPattern d:/course_content/ST/ST_Project/Assignment1/output/test_index_20260322_190051.js --coverage --coverageReporters=json --collectCoverageFrom=targets/index.js --no-cache
    语句覆盖率: 26.9%  分支覆盖率: 19.2%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_index_20260322_190051.json
    test_file: output\test_index_20260322_190051.js

[完成] 总耗时: 53.8s

============================================================
实验对比结果
============================================================
测试项目                                LLM             模型                                用例数       耗时     语句覆盖     分支覆盖   轮次      通过/失败        
------------------------------------------------------------------------------------------------------------------------------------
index.js                            deepseek-chat   deepseek-chat                      96   335.8s    26.9%    19.8%    3    0/96
index.js                            deepseek-reasoner deepseek-reasoner                  40   428.0s    43.3%    32.4%    3    0/40
index.js                            google          gemini-2.5-flash                  280   464.2s    58.4%    44.0%    3    1/279
index.js                            github          gpt-4o-mini                        31    56.4s    26.5%    18.7%    3    0/31
index.js                            deepseek-chat   deepseek-chat                      66   350.9s    38.2%    28.6%    3    7/59
index.js                            deepseek-reasoner deepseek-reasoner                  98   670.3s    66.4%    51.1%    3    4/94
index.js                            google          gemini-2.5-flash                  372   534.9s    31.1%    18.1%    3    0/372
index.js                            github          gpt-4o-mini                        26    46.9s    26.9%    19.8%    3    0/26
index.js                            deepseek-chat   deepseek-chat                      84   320.1s    38.2%    28.6%    3    0/84
index.js                            deepseek-reasoner deepseek-reasoner                 105   543.5s    28.1%    20.3%    3    0/105
index.js                            github          gpt-4o-mini                        30    53.8s    26.9%    19.2%    3    0/30

对比报告已保存: output\comparison_report.md


(st) d:\course_content\ST\ST_Project\Assignment1>python main.py --source targets/convert_number_to_words.py --compare --script  
D:\anaconda3\envs\st\lib\site-packages\google\api_core\_python_version_support.py:275: FutureWarning: You are using a Python version (3.10.20) which Google will stop supporting in new releases of google.api_core once it reaches its end of life (2026-10-04). Please upgrade to the latest Python version, or at least Python 3.11, to continue receiving updates for google.api_core past that date.
  warnings.warn(message, FutureWarning)
d:\course_content\ST\ST_Project\Assignment1\src\llm\client.py:17: FutureWarning: 

All support for the `google.generativeai` package has ended. It will no longer be receiving
updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
See README for more details:

https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

  import google.generativeai as genai
对比模式：将使用以下 LLM 后端运行: deepseek-chat, deepseek-reasoner, google, github
============================================================

============================================================
▶ 使用 deepseek-chat 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: deepseek-chat
需求文档: 无
输出目录: output
对比模式: 是
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-chat)...
[4] 解析 LLM 响应...
    生成了 24 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（140 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260323_154213.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率达标，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260323_154213.json
    test_file: output\test_convert_number_to_words_20260323_154213.py

[完成] 总耗时: 138.0s

============================================================
▶ 使用 deepseek-reasoner 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: deepseek-reasoner
需求文档: 无
输出目录: output
对比模式: 是
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (deepseek-reasoner)...
[4] 解析 LLM 响应...
    生成了 27 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（196 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260323_154928.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率达标，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260323_154928.json
    test_file: output\test_convert_number_to_words_20260323_154928.py

[完成] 总耗时: 434.8s

============================================================
▶ 使用 google 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: google
需求文档: 无
输出目录: output
对比模式: 是
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (google)...
[4] 解析 LLM 响应...
    生成了 28 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（172 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260323_155106.py -v
    语句覆盖率: 91.0%  分支覆盖率: 92.3%
    覆盖率达标，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260323_155106.json
    test_file: output\test_convert_number_to_words_20260323_155106.py

[完成] 总耗时: 97.5s

============================================================
▶ 使用 github 运行...
============================================================
============================================================
白盒测试用例生成工具
源文件: targets/convert_number_to_words.py
LLM: github
需求文档: 无
输出目录: output
对比模式: 是
脚本模式: 是
闭环: 开启（最多 3 轮）
============================================================
[1] 分析源代码: targets/convert_number_to_words.py (语言: python)
[2] 构建 Prompt...
[3] 调用 LLM (github)...
[4] 解析 LLM 响应...
    生成了 15 个测试用例
[Script] 调用 LLM 生成测试脚本...
[Script] 成功生成测试脚本（68 行）

[闭环] 第 1/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260323_155131.py -v
    语句覆盖率: 85.9%  分支覆盖率: 84.6%
    覆盖率不足，LLM 生成补充测试方法...
    [语法检查] Python 语法错误: unindent does not match any outer indentation level (<unknown>, line 74)
    保持当前版本继续下一轮

[闭环] 第 2/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260323_155131.py -v
    语句覆盖率: 85.9%  分支覆盖率: 84.6%
    覆盖率不足，LLM 生成补充测试方法...
    [语法检查] Python 语法错误: unindent does not match any outer indentation level (<unknown>, line 74)
    保持当前版本继续下一轮

[闭环] 第 3/3 轮 - 运行覆盖率测量...
  运行命令: python -m coverage run --source d:\course_content\ST\ST_Project\Assignment1\targets --branch -m pytest d:\course_content\ST\ST_Project\Assignment1\output\test_convert_number_to_words_20260323_155131.py -v
    语句覆盖率: 85.9%  分支覆盖率: 84.6%
    已达最大轮次 3，闭环结束。

[保存] 输出文件...
    test_cases: output\test_cases_convert_number_to_words_20260323_155131.json
    test_file: output\test_convert_number_to_words_20260323_155131.py

[完成] 总耗时: 38.8s

============================================================
实验对比结果
============================================================
测试项目                                LLM             模型                                用例数       耗时     语句覆盖     分支覆盖   轮次      通过/失败
------------------------------------------------------------------------------------------------------------------------------------
convert_number_to_words.py          deepseek-chat   deepseek-chat                      28   113.9s    91.0%    92.3%    3   18/8
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  28   483.8s    91.0%    92.3%    3   16/11
convert_number_to_words.py          google          gemini-2.5-flash                   44   151.4s    91.0%    92.3%    3   39/4
convert_number_to_words.py          github          gpt-4o-mini                        27    29.7s    91.0%    92.3%    3   17/7
convert_number_to_words.py          deepseek-chat   deepseek-chat                      29   105.0s    91.0%    92.3%    3   22/5
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  33   740.0s    91.0%    92.3%    3   27/4
convert_number_to_words.py          google          gemini-2.5-flash                   38   189.7s    91.0%    92.3%    3   33/4
convert_number_to_words.py          github          gpt-4o-mini                        18    24.2s    85.9%    84.6%    3    8/7
convert_number_to_words.py          deepseek-chat   deepseek-chat                      22    90.5s    91.0%    92.3%    1   21/1
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  20   259.7s    91.0%    92.3%    1   19/1
convert_number_to_words.py          github          gpt-4o-mini                        15    21.4s    91.0%    92.3%    1   13/2
convert_number_to_words.py          deepseek-chat   deepseek-chat                      18    94.0s    91.0%    92.3%    1   17/1
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  23   271.5s    91.0%    92.3%    1   20/3
convert_number_to_words.py          google          gemini-2.5-flash                   26    97.6s    91.0%    92.3%    1   23/3
convert_number_to_words.py          github          gpt-4o-mini                        22    32.7s    91.0%    92.3%    1   20/2
convert_number_to_words.py          deepseek-chat   deepseek-chat                      24   138.0s    91.0%    92.3%    1   23/1
convert_number_to_words.py          deepseek-reasoner deepseek-reasoner                  27   434.8s    91.0%    92.3%    1   25/2
convert_number_to_words.py          google          gemini-2.5-flash                   28    97.5s    91.0%    92.3%    1   25/3
convert_number_to_words.py          github          gpt-4o-mini                        15    38.8s    85.9%    84.6%    3   11/4

对比报告已保存: output\comparison_report.md