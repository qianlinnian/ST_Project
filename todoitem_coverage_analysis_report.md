# Todo Item Management 测试设计覆盖审计说明

> 本文档整理自本次对话中的所有结论，可直接作为测试报告中“Test Coverage Analysis / Coverage Evaluation / Limitations of Automation”部分的基础文本使用。  
> 被测 feature：**Todo Item Management**。  
> 目标应用：**SimpleTodoList / simpletodolist**。  
> 测试设计工具：**AutoTestDesign**。  
> 自动化执行框架：**pytest + Selenium WebDriver**。

---

## 1. 总体结论

对于选定的 **Todo Item Management** feature，AutoTestDesign 生成的**测试设计产物在设计层面覆盖较完整**：需求、风险、覆盖项、测试策略、测试套件和原始测试用例之间可以追溯。

但是，需要区分两个层次：

| 层次 | 是否覆盖满 | 说明 |
|---|---:|---|
| 需求覆盖 | 基本满 | REQ-1 ~ REQ-7 都有风险、覆盖项、测试策略、测试用例 |
| 风险覆盖 | 针对 Todo Item Management 基本满 | 全项目风险不全覆盖，但本详细测试只选 Todo Item Management，这是合理的 |
| 覆盖项设计 | 满 | 36 个 coverage items 在完整 test cases 中都有覆盖 |
| 测试套件设计 | 满 | 9 个 test suites 都有测试用例，optimized suite 也保留 9 个 suites |
| 技术使用 | 满足要求 | 使用了 Equivalence Partitioning、Boundary Value Analysis、Decision Table Testing、State Transition Testing |
| optimized suite | 需求级和套件级覆盖保留，但 coverage item 级不完全直接保留 | 少数低风险 coverage item 没有作为独立 optimized case 保留，而是通过相关状态转换或条件测试间接覆盖 |
| Selenium 自动化脚本 | 没有覆盖满 | 当前脚本只自动化了部分代表性高价值 UI 场景，不是全部 57 个 optimized test cases |

**一句话结论：**

> 你们的“用例设计覆盖”可以说是充分、基本完整的；但“自动化执行脚本覆盖”不能说覆盖满，只能说是 optimized suite 的代表性自动化子集。

---

## 2. 作业要求对照

Assignment2.pdf 对本项目的关键要求包括：

1. AutoTestDesign 工具需要支持需求输入与结构化解析。
2. 工具需要进行风险分析和优先级评估。
3. 工具需要使用至少三种核心黑盒测试技术，例如：
   - Equivalence Partitioning
   - Boundary Value Analysis
   - Decision Tables
4. 工具可选支持白盒/结构化建模，例如 State Transition Diagram，并生成满足某种覆盖准则的优化测试序列。
5. 工具需要导出结构化测试产物，例如 JSON、Excel、CSV。
6. 测试工具实现部分需要选择一个测试框架在目标应用上执行测试，例如 Selenium、JUnit、pytest。

本次 Todo Item Management 的产物与这些要求的对应关系如下：

| Assignment2 要求 | 当前产物是否满足 | 说明 |
|---|---:|---|
| 需求结构化 | 是 | `todoitem_requirements_structured.csv` 包含 7 条结构化需求 |
| 风险分析 | 是 | `todoitem_risk_analysis.csv` 为每个需求分配 risk score / risk level |
| 黑盒测试设计 | 是 | 使用 EP、BVA、Decision Table Testing |
| 白盒/结构化建模 | 基本满足 | 使用 State Transition Model Suite，覆盖 TR-001 ~ TR-011 |
| 输出导出 | 是 | 输出 CSV、JSON、XLSX 等结构化 artifact |
| 测试套件优化 | 是 | 原始 78 个 test cases 优化为 57 个 optimized test cases |
| 自动化执行 | 部分满足 | pytest + Selenium 实现了部分 UI 场景，但不是全部 optimized cases |

---

## 3. 文件与统计概览

本次覆盖审计基于以下 AutoTestDesign 导出文件：

| 文件 | 含义 | 数量 |
|---|---:|---:|
| `todoitem_requirements_structured.csv` | 结构化需求 | 7 |
| `todoitem_risk_analysis.csv` | feature-level 风险项 | 7 |
| `todoitem_coverage_items.csv` | 覆盖项 | 36 |
| `todoitem_test_strategies.csv` | 覆盖项对应测试策略 | 36 |
| `todoitem_test_suites.csv` | 测试套件 | 9 |
| `todoitem_test_cases.csv` | 原始生成测试用例 | 78 |
| `todoitem_optimized_test_suite.csv` | 优化后测试用例 | 57 |
| `todoitem_traceability_matrix.csv` | 追溯矩阵 | 78 |
| `todoitem_state_transitions.csv` | 状态转换序列 | 11 |

---

## 4. 需求覆盖检查

Todo Item Management 被结构化为 7 条需求：

| Requirement | 功能点 | 风险覆盖 | 覆盖项覆盖 | 测试策略覆盖 | 测试用例覆盖 |
|---|---|---:|---:|---:|---:|
| REQ-1 | 添加 Todo；空白输入不应创建 item | 1 | 5 | 5 | 10 |
| REQ-2 | 标记 / 取消标记 completed | 1 | 5 | 5 | 9 |
| REQ-3 | 双击编辑；空标题保存则删除 | 1 | 7 | 7 | 13 |
| REQ-4 | 删除单个 Todo item | 1 | 4 | 4 | 6 |
| REQ-5 | toggle all completed / active | 1 | 4 | 4 | 6 |
| REQ-6 | All / Active / Completed 筛选 | 1 | 7 | 7 | 16 |
| REQ-7 | clear all completed | 1 | 4 | 4 | 7 |


检查结果：

```text
需求总数：7
风险覆盖需求数：7 / 7
覆盖项覆盖需求数：7 / 7
测试策略覆盖需求数：7 / 7
测试用例覆盖需求数：7 / 7
缺失需求：[]
```

结论：**REQ-1 ~ REQ-7 在风险、覆盖项、测试策略、测试用例层面均有覆盖，需求级覆盖可以认为是完整的。**

---

## 5. 风险覆盖检查

### 5.1 AutoTestDesign 生成的 feature-level 风险

AutoTestDesign 针对 Todo Item Management 生成了 7 条风险，每条风险对应一条需求：

| Risk ID | Requirement | Risk Level | Risk Score | Reason |
|---|---|---:|---:|---|
| RSK-1 | REQ-1 | Medium | 4 | whitespace input validation missing |
| RSK-2 | REQ-2 | Low | 1 | basic toggle functionality |
| RSK-3 | REQ-3 | Medium | 4 | double-click edit risk |
| RSK-4 | REQ-4 | Low | 1 | simple delete operation |
| RSK-5 | REQ-5 | Medium | 4 | bulk toggle complexity |
| RSK-6 | REQ-6 | Medium | 4 | filter logic risk |
| RSK-7 | REQ-7 | Medium | 4 | bulk delete risk |


结论：**对于选定 feature 的功能风险，REQ-1 ~ REQ-7 均有风险记录，风险覆盖是完整的。**

### 5.2 与同学手工 risk_analysis.md 的关系

同学手工整理的 `risk_analysis.md` 是**整个 SimpleTodoList 项目的风险分析报告**，它覆盖 Admin 身份认证、Todo List 管理、Todo 条目操作、后端 API、跨模块安全和持久化等多个部分。

你们本次详细测试报告只选择一个 feature：**Todo Item Management**。因此不需要覆盖整个项目风险，只需要解释：

> 本详细测试设计聚焦于 Todo 条目操作模块；Admin 登录、List 管理、API 安全、全局数据持久化等风险属于项目级风险分析范围，不纳入本 feature-level detailed test design 的完整覆盖目标。

手工风险中与 Todo Item Management 直接相关的主要风险如下：

| 手工风险 | 含义 | 当前设计产物覆盖情况 |
|---|---|---|
| R-09 | Todo 编辑为空值后的处理分支不一致 | 已覆盖：REQ-3、COV-013、COV-014、编辑空标题删除 |
| R-10 | All / Active / Completed 筛选结果与计数不同步 | 已覆盖：REQ-6、COV-021 ~ COV-026、filter 相关测试 |
| R-11 | toggle-all 与 clear-completed 在边界状态下异常 | 已覆盖：REQ-5、REQ-7、COV-018 ~ COV-020、COV-027 ~ COV-029、COV-AI-005、COV-AI-007 |
| R-12 | localStorage 容量 / 持久化失败 | 部分相关；偏非功能/跨模块，不是本次 TodoItem 主功能设计重点 |
| R-15 | 刷新后列表上下文恢复问题 | 部分相关；属于状态恢复/跨列表场景，不是当前 7 条 TodoItem 核心需求主线 |
| R-16 / R-17 | API 无认证、Any 类型校验 | 不属于 Todo Item Management UI 主功能详细设计，可放入 Test Plan 或后续 API/security testing |

---

## 6. 覆盖项覆盖检查

### 6.1 完整设计覆盖

AutoTestDesign 为 Todo Item Management 生成了 36 个 coverage items：

```text
COV-001 ~ COV-029：基础功能、输入、条件、边界覆盖项
COV-AI-001 ~ COV-AI-007：LLM / reviewer 补充的错误处理和状态转换覆盖项
```

覆盖项按需求分布如下：

| Requirement | Coverage Item 数量 |
|---|---:|
| REQ-1 | 5 |
| REQ-2 | 5 |
| REQ-3 | 7 |
| REQ-4 | 4 |
| REQ-5 | 4 |
| REQ-6 | 7 |
| REQ-7 | 4 |


完整测试设计检查结果：

```text
Coverage items 总数：36
被 test_cases 覆盖：36 / 36
被 test_strategies 覆盖：36 / 36
被 traceability_matrix 覆盖：36 / 36
未被原始 test_cases 覆盖的 coverage items：[]
```

结论：**在原始完整测试设计层面，36 / 36 个 coverage items 均已覆盖。**

### 6.2 optimized suite 中未直接保留的 coverage items

优化后，以下 5 个 coverage items 没有作为独立 optimized test case 直接保留：

```text
COV-005
COV-006
COV-008
COV-015
COV-016
```

它们主要是 REQ-2 / REQ-4 的低风险 toggle/delete 基础功能和输入类覆盖项：

| Coverage Item | Requirement | 含义 | optimized suite 中的处理方式 |
|---|---|---|---|
| COV-005 | REQ-2 | Verify core behavior: toggle completed | 未作为独立 optimized case 保留；核心 toggle 行为被 COV-007、COV-AI-002、COV-STATE-TR-003 等状态转换/条件测试执行到 |
| COV-006 | REQ-2 | Test input field 'item' with valid and invalid data | valid item toggle 被状态转换测试覆盖；invalid item 通过 UI 不易直接构造，因此只能说部分/间接覆盖 |
| COV-008 | REQ-2 | completed status 边界 | completed / active 两个状态由重复 toggle 和状态转换测试覆盖 |
| COV-015 | REQ-4 | Verify core behavior: delete item | 删除核心行为被 COV-017 和 COV-STATE-TR-006 覆盖 |
| COV-016 | REQ-4 | Test input field 'item' with valid and invalid data | valid item 删除被 delete transition 覆盖；invalid/already deleted item 由错误状态测试部分覆盖 |

这并不等于这些 coverage items 被“完全等价替代”。更准确的说法是：

> After optimization, requirement-level behavior remains covered. However, several low-risk coverage items are no longer retained as standalone optimized test cases. Their core behaviors are indirectly exercised by higher-value state-transition or condition-based tests.

中文解释：

> 优化后，需求级行为仍然覆盖；但少数低风险 coverage item 没有作为独立测试用例保留，而是通过其他状态转换测试或条件测试顺带执行到其核心行为。因此不能说 optimized suite 直接覆盖 36 / 36 coverage items，只能说完整设计覆盖 36 / 36，而 optimized suite 保留了需求级和套件级覆盖。

---

## 7. 测试套件覆盖检查

AutoTestDesign 生成了 9 个测试套件，optimized suite 中 9 个 suite 均保留。

| Suite ID | Suite Name | Technique | 原始 test cases | Optimized test cases |
|---|---|---|---:|---:|
| TS-001 | TodoItem Boundary Suite | Boundary Value Analysis | 18 | 5 |
| TS-002 | TodoItem Decision Rule Suite | Decision Table Testing | 2 | 2 |
| TS-003 | TodoItem Partition Suite | Equivalence Partitioning | 6 | 6 |
| TS-004 | TodoItem Partition Suite | Equivalence Partitioning | 14 | 10 |
| TS-005 | TodoItem Partition Suite | Equivalence Partitioning | 16 | 12 |
| TS-006 | TodoItem State Behavior Suite | State Transition Testing | 4 | 4 |
| TS-007 | TodoItem State Behavior Suite | State Transition Testing | 5 | 5 |
| TS-008 | TodoItem State Behavior Suite | State Transition Testing | 2 | 2 |
| TS-009 | State Transition Model Suite | State Transition Testing | 11 | 11 |


检查结果：

```text
Test suites 总数：9
原始 test cases 覆盖 suites：9 / 9
optimized suite 覆盖 suites：9 / 9
```

结论：**测试套件层面满覆盖。**

---

## 8. 测试技术覆盖检查

### 8.1 原始测试用例中的技术分布

| Technique | 原始 test cases 数量 |
|---|---:|
| Boundary Value Analysis | 18 |
| Decision Table Testing | 2 |
| Equivalence Partitioning | 36 |
| State Transition Testing | 22 |


### 8.2 优化测试套件中的技术分布

| Technique | Optimized test cases 数量 |
|---|---:|
| Boundary Value Analysis | 5 |
| Decision Table Testing | 2 |
| Equivalence Partitioning | 28 |
| State Transition Testing | 22 |


### 8.3 黑盒技术是否满足 Assignment2 要求

Assignment2 要求至少使用三种核心黑盒测试技术。本次设计包含：

| 技术 | 类型 | 是否使用 | 说明 |
|---|---|---:|---|
| Equivalence Partitioning | 黑盒 | 是 | 用于 add、edit、filter、clear completed 等有效/无效类别 |
| Boundary Value Analysis | 黑盒 | 是 | 用于 whitespace-only、empty title、All/Active/Completed 等边界状态 |
| Decision Table Testing | 黑盒 | 是 | 用于条件/动作组合，如 clear completed、user action、save empty 等 |
| Error Guessing / Reviewer Supplement | 经验型补充 | 是 | COV-AI-001 ~ COV-AI-007 补充边界与异常场景 |

结论：**黑盒技术要求满足。**

### 8.4 白盒 / 结构化建模是否满足

本项目的白盒/结构化建模主要体现为 **State Transition Model**：

```text
State transitions：11 条
状态转换覆盖准则：All Transitions
对应套件：TS-009 State Transition Model Suite
对应 optimized test cases：11 个
```

需要注意：State Transition Testing 在 ISTQB 体系中通常也可以归为 specification-based technique，但在本项目中，它被用于 Assignment2 FR 4.0 所要求的 “White-Box Test Modeling / State Transition Diagram” 场景，即从 Todo item 生命周期和状态处理逻辑出发建立结构化行为模型，并生成覆盖全部转换的优化序列。

建议报告中写成：

> Although state transition testing is often treated as a specification-based technique in ISTQB, in this project it is used as the required structural behavioral model for FR 4.0 because the transitions are derived from the internal Todo item state handling logic and used to generate an optimized all-transitions test sequence.

中文解释：

> 虽然状态转换测试在 ISTQB 中常被归为规格说明类技术，但本项目将其作为 FR 4.0 要求的结构化行为建模证据：基于 Todo item 的内部状态处理逻辑，建立状态转换模型，并按 All Transitions 准则生成优化测试序列。

---

## 9. State Transition Model 覆盖检查

状态转换模型包含 11 条转换，覆盖 Empty List、List with Items、All Completed、Filtered View 等状态间的关键路径。

| Transition ID | Source State | Event | Target State |
|---|---|---|---|
| TR-001 | Empty List | Add valid item | List with Items |
| TR-003 | List with Items | Toggle item completed | List with Items |
| TR-004 | List with Items | Edit item title to non-empty | List with Items |
| TR-005 | List with Items | Edit item title to empty | List with Items |
| TR-006 | List with Items | Delete single item | List with Items |
| TR-007 | List with Items | Toggle all to completed | All Completed |
| TR-008 | All Completed | Toggle all to active | List with Items |
| TR-009 | List with Items | Filter by Active | Filtered View |
| TR-010 | Filtered View | Filter by All | List with Items |
| TR-002 | Empty List | Add whitespace item | Empty List |
| TR-011 | All Completed | Clear completed | Empty List |


结论：**状态转换模型本身覆盖了 TR-001 ~ TR-011，TS-009 也包含 11 个 optimized test cases，用于覆盖这些转换。**

---

## 10. 自动化执行覆盖检查

当前 Selenium + pytest 脚本不是完整自动化全部 optimized suite，而是实现了其中一部分高价值 UI 场景。

检测到 pytest 测试函数数量：**11**。

| pytest function | 说明 |
|---|---|
| `test_tc066_add_valid_item_from_empty_list` | 添加有效 Todo item |
| `test_tc067_toggle_item_completed` | toggle completed |
| `test_tc068_edit_item_title_to_non_empty` | 编辑为非空标题 |
| `test_tc069_edit_item_title_to_empty_removes_item` | 编辑为空标题并删除 |
| `test_tc070_delete_single_item` | 删除单个 item |
| `test_tc071_toggle_all_to_completed` | toggle all to completed |
| `test_tc072_filter_active_only_shows_incomplete_items` | filter active / 或命名需检查 |
| `test_tc073_filter_completed_only_shows_completed_items` | filter completed |
| `test_tc074_clear_completed_keeps_active_items` | clear completed |
| `test_invalid_blank_and_whitespace_input_are_ignored` | 空白输入不应创建 item |
| `test_filter_round_trip_preserves_completed_state` | All / Active / Completed filter round trip |


与 optimized suite 对比：

```text
Optimized test cases：57
Selenium pytest functions：11
```

因此，自动化覆盖不是 57 / 57。当前自动化脚本主要覆盖 TS-009 状态转换模型和核心 UI 主路径。

另外，根据运行日志，当前脚本执行结果曾出现：

```text
8 passed, 3 failed
```

失败项主要包括：

1. `test_tc068_edit_item_title_to_non_empty`：edit 输入框发生 stale element reference。
2. `test_tc069_edit_item_title_to_empty_removes_item`：同样属于 edit 操作定位/刷新问题。
3. `test_invalid_blank_and_whitespace_input_are_ignored`：whitespace-only 输入仍然创建 item，可能是产品缺陷，也可能是测试触发方式与实现不一致。

结论：**自动化执行层面没有覆盖满，并且当前还存在失败用例。报告中应诚实写成“representative automation subset”，而不是“full automation coverage”。**

---

## 11. 关于 toggle completed 的解释

`toggle completed` 指的是切换 Todo item 的完成状态：

```text
未完成 Active  -> 已完成 Completed
已完成 Completed -> 未完成 Active
```

因此，完整测试应该验证两个方向：

1. active -> completed
2. completed -> active

如果测试只点击一次 checkbox，只覆盖了 mark completed；如果再次点击并断言恢复 active，才完整覆盖 mark / unmark completed。

---

## 12. 关于未直接保留 coverage items 的解释

之前提到 COV-005、COV-006、COV-008、COV-015、COV-016 没有出现在 optimized suite 中。这里的意思不是“这些覆盖项消失了也完全没关系”，而是：

```text
完整设计层面：这些 coverage item 是存在的，并且被原始 test cases 覆盖。
优化后：它们没有作为独立 optimized test case 保留。
但：它们对应的核心需求行为在其他更高价值测试中被顺带执行到。
```

例如：

- COV-005 的 toggle completed 核心行为，会在状态转换 TR-003、重复 toggle 测试、user action 条件测试中被执行到。
- COV-015 的 delete item 核心行为，会在 delete transition 和 delete user-action 测试中被执行到。
- COV-006 / COV-016 这类 input-oriented coverage item 只能说部分/间接覆盖，因为 invalid item 在 UI 层不容易直接构造。

最稳的报告写法是：

> The full generated test design covers all 36 coverage items. After optimization, the suite preserves complete requirement-level and test-suite-level coverage, while reducing several low-risk coverage items as standalone cases. Their core behaviors are indirectly covered by state-transition or condition-based tests.

中文：

> 完整生成的测试设计覆盖了全部 36 个 coverage items。优化后，测试套件保留了需求级和测试套件级覆盖，但减少了若干低风险 coverage items 作为独立用例的保留。这些覆盖项的核心行为通过状态转换或条件测试被间接覆盖。

---

## 13. 可直接放入报告的英文总结段

```text
For the selected Todo Item Management feature, the AutoTestDesign tool produced complete design-level coverage. Seven structured requirements (REQ-1 to REQ-7) were identified, and each requirement was linked to at least one product risk, multiple coverage items, test strategies, and generated test cases. In total, the design artifacts include 7 risks, 36 coverage items, 9 test suites, 78 generated test cases, 57 optimized test cases, and 11 state-transition test sequences.

The test design applies multiple black-box techniques required by the assignment, including Equivalence Partitioning, Boundary Value Analysis, and Decision Table Testing. In addition, State Transition Testing is used as the white-box / structure-based modeling technique for the Todo item lifecycle. The state model covers the main states and transitions of Todo items, and the optimized State Transition Model Suite is generated under the All Transitions coverage criterion.

Therefore, the design-level coverage of requirements, risks, coverage items, test strategies, and test suites is complete for the selected Todo Item Management feature. However, the Selenium + pytest implementation is a representative automation subset rather than a full automation of all optimized test cases. It automates selected high-priority UI scenarios, mainly from the state-transition suite, while the remaining optimized cases are kept as manual tests or future automation candidates.
```

---

## 14. 可直接放入报告的中文总结段

```text
对于选定的 Todo Item Management 特性，AutoTestDesign 生成的测试设计产物在设计层面实现了较完整的覆盖。7 条结构化需求（REQ-1 至 REQ-7）均被关联到至少一个产品风险、多个覆盖项、测试策略以及生成测试用例。整体产物包括 7 条风险、36 个覆盖项、9 个测试套件、78 个原始测试用例、57 个优化测试用例以及 11 条状态转换测试序列。

本次测试设计使用了多种黑盒测试技术，包括等价类划分、边界值分析和决策表测试，满足 Assignment2 对黑盒测试技术的要求。同时，项目使用状态转换测试作为 Todo item 生命周期的结构化/白盒建模技术。状态模型覆盖 Todo item 的主要状态和转换，并按照 All Transitions 覆盖准则生成优化测试序列。

因此，对于 Todo Item Management 这一选定特性，需求、风险、覆盖项、测试策略和测试套件在设计层面覆盖较完整。然而，Selenium + pytest 自动化实现只是优化测试套件中的代表性自动化子集，并未自动化全部 optimized test cases。自动化脚本主要覆盖状态转换套件中的高优先级 UI 场景，剩余优化测试用例可作为手工测试或后续自动化扩展对象。
```

---

## 15. 报告中推荐使用的最终表述

最推荐你在报告里使用这句话作为最终判断：

> 测试设计层面可以认为覆盖充分；自动化执行层面是代表性子集，不是完整自动化覆盖。

英文版本：

> The test design achieves sufficient design-level coverage, while the Selenium automation is a representative execution subset rather than full automation coverage.

---

## 16. 附：覆盖审计结果摘要

```text
Requirements: 7
Risks: 7
Coverage Items: 36
Test Strategies: 36
Test Suites: 9
Original Test Cases: 78
Optimized Test Cases: 57
Traceability Matrix Rows: 78
State Transitions: 11

Requirement-level coverage: complete for REQ-1 ~ REQ-7
Risk-level coverage: complete for selected Todo Item Management feature
Coverage-item design coverage: complete in full generated test cases
Suite-level coverage: complete, TS-001 ~ TS-009 retained
Technique coverage: EP, BVA, Decision Table, State Transition all used
Optimized suite: requirement-level and suite-level coverage preserved; several low-risk coverage items not retained as standalone optimized cases
Selenium automation: partial / representative subset, not full automation of all optimized test cases
```
