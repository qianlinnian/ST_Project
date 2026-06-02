# AutoTestDesign 提示词说明

本文档用于补充说明当前项目中提示词的组织方式与用途，方便助教或评阅者在不先通读全部源码的情况下，理解本项目如何使用 LLM。

## 1. 提示词主存放位置

主要提示词定义位于：

- [./src/prompt_templates.py](./src/prompt_templates.py:1)

该文件主要包含两类内容：

- `SYSTEM` 提示词常量
- 将当前工件压缩成 LLM 输入文本的 prompt 构造函数

例如：

- `COMPACT_REQUIREMENT_STRUCTURING_SYSTEM`
- `COMPACT_RISK_SYSTEM`
- `COMPACT_COVERAGE_IMPROVEMENT_SYSTEM`
- `COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM`
- `ORACLE_REVIEW_SYSTEM`
- `COMPACT_SUITE_MINIMIZATION_SYSTEM`
- `TEST_PLAN_DOCUMENT_IMPROVEMENT_SYSTEM`

以及对应的构造函数：

- `compact_requirement_structuring_prompt(...)`
- `compact_risk_prompt(...)`
- `compact_coverage_improvement_prompt(...)`
- `missing_test_case_prompt(...)`
- `oracle_review_prompt(...)`
- `compact_suite_minimization_prompt(...)`
- `test_plan_document_improvement_prompt(...)`

## 2. 一个重要说明

提示词虽然主要写在 `prompt_templates.py` 里，但系统行为并不是由这一个文件单独决定的。

真正的调用与衔接逻辑分散在这些模块中：

- [./src/improvement_engine.py](./src/improvement_engine.py:1)
- [./src/test_case_generator.py](./src/test_case_generator.py:1)
- [./src/oracle_generator.py](./src/oracle_generator.py:1)
- [./src/test_plan_document_generator.py](./src/test_plan_document_generator.py:1)
- [./src/test_suite_designer.py](./src/test_suite_designer.py:1)
- [./src/llm_execution.py](./src/llm_execution.py:1)
- [./src/ai_client.py](./src/ai_client.py:1)

这些模块负责：

- 决定什么阶段启用 LLM 增强
- 进行分批处理
- 控制并发数
- 解析 JSON 返回
- 将建议回写到现有工件中
- 在响应异常时执行回退逻辑

## 3. 整体设计思想

本工具并不是“完全靠提示词驱动”的系统，而是有意采用了 `local-first` 的设计。

总体模式是：

1. 先通过本地规则、启发式逻辑或轻量模型生成基础工件
2. 再在可选阶段把压缩后的摘要发送给 LLM 做增强
3. 对返回结果进行保守解析与合并
4. 尽量保留原有 ID 和追溯关系

因此，提示词在本项目中的主要作用是：

- 澄清
- 润色
- 补充
- 文档级改写

而不是替代整个测试设计主流程。

## 4. 为什么提示词都写得比较紧凑

本项目中的许多 prompt 并不是长篇自然语言上下文，而是使用紧凑的行式摘要格式。

这样做主要是为了：

- 减少 token 消耗
- 提高分批处理效率
- 降低 API 成本
- 方便结构化解析
- 把 LLM 的任务限制在较窄的职责范围内

例如工具通常会发送：

- requirement 摘要
- coverage ID 与简短描述
- test case ID 与关键字段
- 按 `suite_id` 分组后的 suite payload

而不是整张表全部展开并附带大量重复说明。

## 5. 提示词分组说明

当前提示词可以按功能划分为以下几类。

### 5.1 Requirement Structuring

用途：

- 将原始需求文本转换为结构化需求记录

主要提示词：

- `REQUIREMENT_STRUCTURING_SYSTEM`
- `COMPACT_REQUIREMENT_STRUCTURING_SYSTEM`

典型输出：

- 包含 action、condition、input、expected behavior 等字段的结构化 requirement 记录

存在原因：

- 原始需求文本过于自由，不利于后续风险分析、覆盖项识别和测试设计

### 5.2 Risk Analysis

用途：

- 生成需求级别的风险分析结果

主要提示词：

- `RISK_ANALYSIS_SYSTEM`
- `COMPACT_RISK_SYSTEM`

典型输出：

- impact
- likelihood
- risk score
- risk level
- 面向测试的风险说明

存在原因：

- 后续测试优先级与安排应基于风险，而不是只做机械枚举

### 5.3 Coverage Improvement

用途：

- 改进或补充本地生成的 coverage items

主要提示词：

- `COMPACT_COVERAGE_IMPROVEMENT_SYSTEM`

典型输出：

- 缺失的 coverage item
- 对已有 coverage 描述的改进
- 更好的 technique hint 或 notes

设计说明：

- 这一阶段并不只会“新增 coverage”，也允许在已有 coverage 较弱时直接改进它

### 5.4 Test Strategy Review

用途：

- 针对 coverage items 复核当前选定的测试技术

主要提示词：

- `TEST_STRATEGY_REVIEW_SYSTEM`

典型输出：

- 对现有 strategy 的说明或修正建议

存在原因：

- 本地规则选出的技术通常是可用的，但不一定说明充分，也不一定总是最清晰

### 5.5 Test Case Generation

用途：

- 基于 coverage 和 suite 上下文生成详细测试用例

主要提示词：

- `TEST_CASE_GENERATION_SYSTEM`

典型输出：

- 包含输入、步骤、预期结果、优先级与设计依据的 test case 记录

重要说明：

- 此阶段仍然受本地 `ID`、suite 归属和 coverage 追溯关系约束

### 5.6 Test Case Improvement

用途：

- 修改已有测试用例，或在确有缺口时补充新用例

主要提示词：

- `COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM`

典型输出：

- 针对现有 `test_case_id` 的修订行
- 必要时新增真正缺失的 test case

意义：

- LLM 不只是补充新 case，也会尝试改进已有 case 中表达模糊、步骤不清、预期结果不够具体的问题

### 5.7 Oracle Review

用途：

- 专门改进 `expected_result` 字段

主要提示词：

- `ORACLE_REVIEW_SYSTEM`

典型输出：

- 更清楚、更可观察的 expected result

为什么单独拆出来：

- 预期结果的精炼通常比整条 test case 更需要针对性
- 使用聚焦提示词，通常比让一个大 prompt 全量重写 test case 更可靠

### 5.8 Suite Minimization Review

用途：

- 复核优化后的 suite，判断哪些 case 可保留、哪些可删除

主要提示词：

- `SUITE_OPTIMIZATION_REVIEW_SYSTEM`
- `COMPACT_SUITE_MINIMIZATION_SYSTEM`

典型输出：

- `keep` 或 `drop`
- 精简原因

设计说明：

- 该阶段本身是保守的
- 目标不是重写整个 suite，而是在尽量不破坏 coverage 的前提下去除低价值冗余

### 5.9 State Model Improvement

用途：

- 改进推导出的状态模型或状态转移信息

主要提示词：

- `STATE_MODEL_IMPROVEMENT_SYSTEM`

典型输出：

- 结构化 state model JSON
- 更合理的 states、transitions、guards、events

存在原因：

- 仅靠本地浅层解析，很难完整恢复状态行为模型

### 5.10 Suite Metadata Improvement

用途：

- 改进 suite 名称、目标描述和设计依据表达

主要提示词：

- `SUITE_DESIGN_IMPROVEMENT_SYSTEM`

典型输出：

- 更清楚的 suite name
- 更准确的 suite objective
- 更明确的 design basis 表述

### 5.11 Test Plan Document Improvement

用途：

- 润色与增强生成后的 Markdown 测试计划文档

主要提示词：

- `TEST_PLAN_DOCUMENT_IMPROVEMENT_SYSTEM`

典型输出：

- 一整篇修订后的 Markdown 文档

重要说明：

- 与大多数结构化 prompt 不同，这一阶段通常返回全文，而不是 JSON patch
- 因此它主要用于文档表达优化，而不是关键 ID 的机器生成

## 6. 如何约束 LLM 输出

对于需要机器读取的阶段，prompt 通常会设置较严格的约束。

常见控制方式包括：

- 要求只输出 JSON
- 固定字段名
- 显式要求保留 ID
- 限定 LLM 允许改动的字段范围

之所以要这么做，是因为后续工件依赖这些关键字段：

- `requirement_id`
- `coverage_id`
- `suite_id`
- `test_case_id`

如果提示词无限制放开，追溯关系会很快变得不可靠。

## 7. 分批处理与并发

本项目不会把所有工件一次性打包成一个巨大请求发送给模型。
许多 LLM 阶段都采用了分批处理。

这样做的好处包括：

- 降低单次 prompt 体积
- 更容易隔离错误
- 某一批失败时仍可保留其他批次成果
- 可以通过 UI 配置并发数

典型应用场景包括：

- compact risk analysis batches
- coverage improvement batches
- test case improvement batches
- oracle review batches
- suite minimization batches

相关逻辑主要位于：

- [./src/llm_execution.py](./src/llm_execution.py:1)
- [./src/improvement_engine.py](./src/improvement_engine.py:1)

## 8. 回退与稳健性设计

本工具默认假设 LLM 响应可能失败、漂移，或者返回格式错误的 JSON。

因此，很多阶段都实现了：

- 响应解析检查
- 回退到本地原始工件
- 局部合并，而不是整表盲目覆盖

这在以下阶段尤其重要：

- compact JSON prompts
- oracle review
- suite minimization
- test case improvement

设计目标是提高实际可用性，而不是追求无限制生成。

## 9. 给评阅者的重点说明

如果从评审角度看，这个项目最关键的一点是：

- 它不是纯 prompt 驱动系统
- LLM 在这里只是本地测试设计流水线上的一个可选增强层

也就是说：

- requirements、risks、coverage、suites、cases 都有本地生成逻辑
- prompts 主要用于提升质量、清晰度或完整性
- 项目刻意保留了 traceability 和较强的输出控制

因此，本项目的提示词设计重点是：

- 紧凑
- 结构化输出
- 保守合并
- local-first 生成

## 10. 推荐阅读顺序

如果评阅者希望比较高效地看实现，建议按这个顺序阅读：

1. [./src/prompt_templates.py](./src/prompt_templates.py:1)
2. [./src/ai_client.py](./src/ai_client.py:1)
3. [./src/llm_execution.py](./src/llm_execution.py:1)
4. [./src/improvement_engine.py](./src/improvement_engine.py:1)
5. [./src/test_case_generator.py](./src/test_case_generator.py:1)
6. [./src/oracle_generator.py](./src/oracle_generator.py:1)
7. [./src/test_plan_document_generator.py](./src/test_plan_document_generator.py:1)

这样可以更快地把提示词定义、执行方式和结果合并逻辑串起来看懂。
