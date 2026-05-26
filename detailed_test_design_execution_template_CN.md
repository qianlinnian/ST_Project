# 详细测试设计与执行文档模板（中文版）

> 使用说明：
> 1. 第一部分是**纯模板**，适合直接复制为正式报告骨架。
> 2. 第二部分是**带推荐撰写内容的模板填充版**，已经结合当前项目的 Todo Item Management、AutoTestDesign 产物、Selenium + pytest 自动化脚本和最终测试结果进行推荐写作。
> 3. 文中 `[待填写：...]` 表示需要你们按小组实际情况补充，例如 Team ID、成员姓名、学号、仓库路径、运行环境版本等。
> 4. 如果最终报告要求英文提交，可以先使用本中文版理清逻辑，再翻译成英文版。

---

# 第一部分：纯模板

# 详细测试设计与执行文档

## 封面

- 项目名称：`[待填写：项目名称]`
- 交付物名称：详细测试设计与执行文档
- 目标应用：`[待填写：目标应用名称]`
- 选定功能 / 模块：`[待填写：选定的功能或模块]`
- 小组编号：`[待填写：Team ID]`
- 小组成员：`[待填写：姓名与学号]`
- 提交日期：`[待填写：提交日期]`

---

## 1. 引言

### 1.1 文档目的

`[说明本文档目的：针对选定 feature/module，使用 AutoTestDesign 工具完成详细测试设计，并基于设计结果实现测试执行。]`

### 1.2 测试范围

`[说明测试对象、测试模块、覆盖功能、不覆盖范围。]`

### 1.3 测试环境

`[列出前端地址、后端地址、测试框架、浏览器、主要脚本、主要导出文件。]`

### 1.4 文档结构

`[说明本文档后续章节结构：测试设计、工具实现、执行结果、覆盖评价、限制与改进。]`

---

## 2. 详细测试用例设计

### 2.1 选定功能 / 模块

`[说明为什么选择该功能模块，以及该模块为什么适合展示测试设计技术。]`

### 2.2 需求与风险依据

`[说明测试用例设计基于哪些结构化需求、风险分析、覆盖项、测试策略和测试用例导出文件。]`

### 2.3 测试设计流程

`[说明从需求输入到测试用例生成、人工审查、优化、自动化映射的流程。]`

### 2.4 覆盖项识别

`[说明覆盖项如何从功能、输入、条件、异常场景、状态转换中识别出来。]`

### 2.5 覆盖策略与测试设计技术

`[说明每类覆盖项选择了什么测试技术，以及为什么选择。]`

#### 2.5.1 黑盒测试技术

`[说明等价划分、边界值分析、决策表测试等黑盒技术的使用。]`

#### 2.5.2 白盒 / 结构化建模技术

`[说明状态转换测试或其他结构化/白盒建模技术的使用。]`

### 2.6 测试套件结构

`[说明 AutoTestDesign 生成的 test suites 划分，以及每个 suite 的主要测试技术和目标。]`

### 2.7 优化测试套件与覆盖说明

`[说明原始测试用例数量、优化后测试用例数量，以及优化保留了哪些覆盖目标。]`

### 2.8 需求、覆盖项、测试用例之间的追溯关系

`[说明如何通过 traceability matrix 证明需求、风险、覆盖项、测试策略、测试用例之间可追溯。]`

### 2.9 人工审查与改进证据

`[说明测试人员如何审查、修改、补充覆盖项、策略或测试用例，并给出改进证据。]`

---

## 3. 测试工具实现

### 3.1 测试框架选择

`[说明为什么选择 Selenium、pytest 或其他测试框架。]`

### 3.2 自动化测试目标

`[说明自动化脚本覆盖哪些 optimized test cases，是否覆盖全部优化用例。]`

### 3.3 脚本结构

`[说明测试脚本的 Page Object、fixture、测试数据、参数化用例、helper 函数等结构。]`

### 3.4 优化测试用例到自动化场景的映射

`[说明每个 optimized test case 如何映射到可执行 UI 场景，哪些场景可以复用。]`

### 3.5 测试独立性与数据重置

`[说明如何保证每个测试开始前状态一致，例如 API 清理、UI 清理、页面刷新和断言初始状态。]`

### 3.6 可执行性与限制

`[说明脚本运行方式、环境依赖、仍存在的限制或不能完全自动验证的内容。]`

---

## 4. 测试结果分析

### 4.1 执行概要

`[给出 pytest 执行结果，例如 collected items、passed、failed、execution time。]`

### 4.2 通过、失败、跳过与预期失败用例

`[说明是否存在 failed / skipped / xfailed，以及这些结果的原因。]`

### 4.3 缺陷或偏差分析

`[说明测试执行中发现的产品缺陷、测试脚本问题或需求实现偏差。]`

### 4.4 执行后的覆盖有效性评价

`[说明测试执行结果如何支持需求覆盖、风险覆盖、覆盖项覆盖和测试技术覆盖。]`

### 4.5 改进建议

`[说明后续可以改进的方向，例如更强的 oracle、更稳定的测试数据隔离、补充非功能测试等。]`

---

## 5. 结论

`[总结本详细测试设计与执行工作的价值、覆盖程度、自动化结果和局限性。]`

---

## 附录

### 附录 A：主要测试产物清单

`[列出 CSV、JSON、XLSX、pytest 脚本、测试结果日志等文件。]`

### 附录 B：运行命令

`[给出启动前端、后端和执行 pytest 的命令。]`

### 附录 C：术语表

`[解释 requirement、risk、coverage item、test strategy、test suite、traceability matrix 等术语。]`

---

# 第二部分：带推荐撰写内容的模板填充版

# 详细测试设计与执行文档

## 封面

- 项目名称：AutoTestDesign for SimpleTodoList Testing
- 交付物名称：详细测试设计与执行文档
- 目标应用：SimpleTodoList
- 选定功能 / 模块：Todo Item Management
- 小组编号：`[待填写：Team ID]`
- 小组成员：`[待填写：姓名与学号]`
- 提交日期：`[待填写：提交日期]`

---

## 1. 引言

### 1.1 文档目的

本文档是 Assignment 2 第四项交付物“Detailed Test Design and Execution Document”的中文版写作模板。本文档聚焦于目标应用 SimpleTodoList 中的一个主要功能模块，即 **Todo Item Management**。文档目标是说明本组如何使用 AutoTestDesign 工具完成需求结构化、风险分析、覆盖项识别、测试策略选择、测试用例生成、优化测试套件构造，以及基于 Selenium + pytest 的自动化执行。

本文档不是对 AutoTestDesign 工具本身进行测试，而是使用该工具对自选目标应用的一个功能模块进行详细测试设计与执行。这样的范围划分与 Assignment 2 对交付物的要求保持一致：风险分析报告、测试计划以及详细测试设计与执行文档均应面向目标应用，而不是面向 AutoTestDesign 工具本身。

### 1.2 测试范围

本详细测试设计的范围限定为 SimpleTodoList 应用中的 **Todo Item Management** 功能。该功能包含 Todo 条目的新增、完成状态切换、编辑、删除、全选切换、状态筛选以及清除已完成条目等核心行为。

本测试范围覆盖以下需求：

| Requirement ID | 功能说明 |
|---|---|
| REQ-1 | 用户能够新增 Todo item；只包含空白字符的输入不应创建 item |
| REQ-2 | 用户能够标记或取消标记 Todo item 为 completed |
| REQ-3 | 用户能够通过双击编辑 Todo item；保存空标题时应删除该 item |
| REQ-4 | 用户能够删除单个 Todo item |
| REQ-5 | 用户能够使用单一控件将所有 Todo items 切换为 completed 或 active |
| REQ-6 | 用户能够按 All、Active、Completed 状态筛选 Todo items |
| REQ-7 | 用户能够一次性清除所有 completed Todo items |

本详细测试设计不覆盖 Admin 身份认证、Todo List 管理、后端 API 安全、全局项目风险等内容。这些内容属于完整项目风险分析或测试计划范围，而不属于本交付物中选定 feature/module 的详细测试设计范围。

### 1.3 测试环境

推荐在报告中写明如下测试环境。具体版本可由小组按实际运行结果补充。

| 项目 | 推荐填写内容 |
|---|---|
| 目标应用 | SimpleTodoList |
| 被测模块 | Todo Item Management |
| 前端地址 | `http://127.0.0.1:8000/todo.html#/&test-list` |
| 后端 API 地址 | `http://127.0.0.1:5000/api` |
| 自动化框架 | pytest + Selenium WebDriver |
| 浏览器 | Chrome / Edge / Firefox，按实际使用填写 |
| 测试脚本 | `test_todoitem_ui_selenium_full.py` |
| 结构化需求文件 | `todoitem_requirements_structured.csv` |
| 风险分析文件 | `todoitem_risk_analysis.csv` |
| 覆盖项文件 | `todoitem_coverage_items.csv` |
| 测试策略文件 | `todoitem_test_strategies.csv` |
| 测试套件文件 | `todoitem_test_suites.csv` |
| 原始测试用例文件 | `todoitem_test_cases.csv` |
| 优化测试套件文件 | `todoitem_optimized_test_suite.csv` |
| 追溯矩阵文件 | `todoitem_traceability_matrix.csv` |
| 状态转换文件 | `todoitem_state_transitions.csv` |

### 1.4 文档结构

本文档后续结构如下。第二章说明详细测试用例设计过程，包括选定模块、需求与风险依据、覆盖项识别、测试技术选择、测试套件结构、优化测试套件以及追溯关系。第三章说明测试工具实现，包括框架选择、脚本结构、自动化映射、测试数据重置和可执行性。第四章说明测试结果分析，包括执行概要、通过情况、缺陷或偏差分析、覆盖有效性评价和改进建议。第五章给出总结。附录列出主要测试产物、运行命令和术语表。

---

## 2. 详细测试用例设计

### 2.1 选定功能 / 模块

本项目选择 **Todo Item Management** 作为详细测试设计对象。选择该模块的原因如下：

第一，该模块是 SimpleTodoList 应用的核心功能之一，直接体现用户对待办事项的主要操作流程。第二，该模块包含多种典型输入、状态和条件组合，例如空白输入、completed / active 状态、All / Active / Completed 筛选、批量切换和批量删除，适合展示黑盒测试设计技术。第三，该模块具有明显的状态变化，例如 active 与 completed 之间的切换、view mode 与 edit mode 之间的切换、existing 与 deleted 之间的变化，因此也适合展示状态转换测试等结构化建模技术。

因此，Todo Item Management 能够较好地覆盖 Assignment 2 对详细测试设计的要求：使用多种黑盒测试技术，同时使用白盒或结构化建模技术，并通过自动化脚本执行设计出的测试用例。

### 2.2 需求与风险依据

本测试设计基于 AutoTestDesign 工具生成并经过人工审查的结构化测试产物。主要输入与证据如下：

| 文件 | 作用 |
|---|---|
| `todoitem_requirements_structured.csv` | 将 Todo Item Management 需求拆解为结构化需求，包括输入字段、数据范围、条件、动作和期望结果 |
| `todoitem_risk_analysis.csv` | 为每条需求分配风险评分、风险等级和测试建议 |
| `todoitem_coverage_items.csv` | 从需求、风险、输入、条件、边界和状态行为中识别覆盖项 |
| `todoitem_test_strategies.csv` | 为每个覆盖项选择测试策略和测试设计技术 |
| `todoitem_test_cases.csv` | 生成原始测试用例集合 |
| `todoitem_optimized_test_suite.csv` | 基于风险和覆盖效率优化后的测试用例集合 |
| `todoitem_traceability_matrix.csv` | 记录需求、风险、覆盖项、测试策略、测试套件和测试用例之间的追溯关系 |
| `todoitem_state_transitions.csv` | 记录状态转换模型相关的测试序列 |

从需求层面看，Todo Item Management 被结构化为 7 条需求，即 REQ-1 至 REQ-7。每条需求均具有对应风险、覆盖项、测试策略和测试用例。因此，需求级覆盖是完整的。

从风险层面看，AutoTestDesign 为每条需求生成了一条 feature-level 风险：

| Risk ID | Requirement ID | Risk Level | Risk Score | 风险原因 |
|---|---|---:|---:|---|
| RSK-1 | REQ-1 | Medium | 4 | 空白输入校验可能缺失 |
| RSK-2 | REQ-2 | Low | 1 | 基础 toggle 功能风险较低 |
| RSK-3 | REQ-3 | Medium | 4 | 双击编辑和空标题保存存在分支风险 |
| RSK-4 | REQ-4 | Low | 1 | 单项删除操作逻辑较简单 |
| RSK-5 | REQ-5 | Medium | 4 | 批量 toggle 逻辑存在状态复杂性 |
| RSK-6 | REQ-6 | Medium | 4 | 筛选逻辑可能与显示或计数不同步 |
| RSK-7 | REQ-7 | Medium | 4 | 批量清除 completed items 存在边界状态风险 |

这些风险用于指导测试优先级和测试技术选择。中风险需求需要更充分的覆盖，低风险需求也保留基本功能和状态覆盖。

### 2.3 测试设计流程

本项目采用如下详细测试设计流程：

1. **需求输入与结构化**：将 Todo Item Management 的自然语言需求输入 AutoTestDesign，由工具提取 requirement id、input fields、data ranges、conditions、actions 和 expected results。
2. **风险分析与优先级评估**：工具根据需求复杂度、输入校验、状态依赖和潜在失效影响，为每条需求生成 risk score 和 risk level。
3. **覆盖项识别**：工具从功能行为、输入字段、数据范围、条件分支、边界情况、异常场景和状态转换中识别 coverage items。
4. **覆盖策略选择**：工具为每个 coverage item 推荐测试技术，例如 Equivalence Partitioning、Boundary Value Analysis、Decision Table Testing、State Transition Testing 和 Error Guessing。
5. **测试用例生成**：工具根据覆盖项与策略生成原始测试用例，并建立需求到测试用例的追溯关系。
6. **人工审查与修订**：测试人员检查生成结果，确认技术选择是否合理，并补充状态转换相关测试套件和可执行场景映射。
7. **测试套件优化**：基于风险和覆盖效率，将原始测试用例优化为较小但仍保留关键覆盖目标的 optimized test suite。
8. **自动化映射与执行**：将 optimized test suite 映射为 Selenium + pytest UI 自动化测试，最终执行并分析结果。

该流程符合“Concept → Coverage Item Identification → Coverage Strategy & Method → Test Cases and Traceability → Prompt Design → Result Analysis → Improvement with Evidence”的思路，体现了工具自动生成与人工审查改进相结合的过程。

### 2.4 覆盖项识别

AutoTestDesign 针对 Todo Item Management 识别出 36 个 coverage items。这些覆盖项可分为以下类型：

| 覆盖类型 | 说明 | 示例 |
|---|---|---|
| Functional | 验证核心功能行为是否正确 | add item、toggle completed、edit title、delete item、apply filter |
| Input | 验证输入字段的有效和无效数据 | title input、filter input、control input |
| Condition | 验证用户动作或条件分支 | double-click、save empty、select filter、user action |
| Boundary | 验证边界输入或边界状态 | whitespace only、empty title、All / Active / Completed filter values |
| Error | 验证异常或不可用状态 | empty list 下 clear completed、invalid filter value、already deleted item |
| State Transition | 验证状态变化序列 | active → completed、completed → active、view → edit、existing → deleted |

这些覆盖项不是简单地罗列功能点，而是从需求中的输入、条件、动作、预期结果和风险点推导出来。因此，它们能够支持从需求到测试用例的系统化设计。

### 2.5 覆盖策略与测试设计技术

本项目使用多种测试设计技术来覆盖不同类型的 coverage items。整体策略如下：

| 测试技术 | 类型 | 适用对象 | 在本项目中的作用 |
|---|---|---|---|
| Equivalence Partitioning | 黑盒 | 有效 / 无效输入类别、核心功能行为 | 用于 add、toggle、edit、delete、filter 等基本行为和输入类别 |
| Boundary Value Analysis | 黑盒 | 边界输入或边界状态 | 用于 whitespace only、empty title、filter values 等边界情况 |
| Decision Table Testing | 黑盒 | 多条件组合或业务规则组合 | 用于筛选、状态和操作条件组合的验证 |
| State Transition Testing | 白盒 / 结构化建模 | 状态依赖行为 | 用于 active/completed、view/edit、existing/deleted 等状态转换 |
| Error Guessing | 经验型技术 | 异常或边缘场景 | 用于空列表、已删除 item、invalid control 等错误场景 |

这样设计的好处是，不同覆盖项不会机械地使用同一种测试技术，而是根据覆盖项性质选择更合适的方法。例如，输入类别使用等价划分，边界输入使用边界值分析，状态依赖行为使用状态转换测试。

#### 2.5.1 黑盒测试技术

本项目使用了至少三种核心黑盒测试技术：Equivalence Partitioning、Boundary Value Analysis 和 Decision Table Testing。

**Equivalence Partitioning** 用于将输入和功能行为划分为有效类与无效类。例如，对于新增 Todo item，可以划分为有效文本输入、空字符串输入、空白字符输入等类别。对于 filter 控件，可以划分为 All、Active、Completed 和 invalid filter value 等类别。

**Boundary Value Analysis** 用于验证边界条件。例如，REQ-1 中“只包含空白字符的输入不应创建 item”属于输入边界；REQ-3 中“保存空标题应删除 item”属于编辑标题的边界；REQ-6 中 All、Active、Completed 三种筛选状态也可作为状态选择边界进行验证。

**Decision Table Testing** 用于处理条件组合。例如，Todo item 的显示结果取决于 item 状态和当前 filter；clear completed 的结果取决于是否存在 completed items；toggle all 的结果取决于当前列表是否为空、是否有 active items、是否有 completed items。这些组合适合通过决策表思想进行覆盖。

#### 2.5.2 白盒 / 结构化建模技术

本项目使用 **State Transition Testing** 作为白盒或结构化建模技术。虽然 Selenium UI 测试主要从用户界面观察行为，但状态转换模型关注的是系统内部可观察状态之间的变化，因此可以作为结构化建模技术使用。

Todo Item Management 中的关键状态包括：

| 状态对象 | 状态 |
|---|---|
| Todo item 完成状态 | active、completed |
| Todo item 编辑状态 | view mode、edit mode |
| Todo item 存在状态 | existing、deleted |
| 列表筛选状态 | All、Active、Completed |

典型状态转换包括：

| Transition ID | 状态转换 | 触发动作 | 预期结果 |
|---|---|---|---|
| TR-001 | empty list → item exists | add item | 新 item 出现在列表中 |
| TR-002 | active → completed | toggle item | item 标记为 completed |
| TR-003 | completed → active | toggle item again | item 恢复为 active |
| TR-004 | view mode → edit mode | double-click item | 出现编辑输入框 |
| TR-005 | edit mode → view mode | save non-empty title | 标题更新并退出编辑 |
| TR-006 | existing → deleted | save empty title 或 delete | item 从列表中消失 |
| TR-007 | mixed list → completed-only removed | clear completed | completed items 被清除 |

通过状态转换测试，可以覆盖普通输入测试难以表达的连续状态变化，例如反复 toggle、编辑后删除、筛选状态变化后的显示一致性等。

### 2.6 测试套件结构

AutoTestDesign 将测试用例组织为多个 test suites。推荐在报告中按以下方式描述：

| Suite ID | Suite Name | 主要目标 | 主要技术 |
|---|---|---|---|
| TS-001 | Requirement Functional Suite | 覆盖各需求的核心功能行为 | Equivalence Partitioning |
| TS-002 | Input Validation Suite | 覆盖输入字段的有效和无效类别 | Equivalence Partitioning、BVA |
| TS-003 | Boundary Suite | 覆盖空白输入、空标题、筛选值等边界 | Boundary Value Analysis |
| TS-004 | Decision / Condition Suite | 覆盖条件组合和操作组合 | Decision Table Testing |
| TS-005 | State Transition Suite | 覆盖 active/completed、view/edit、existing/deleted 等状态变化 | State Transition Testing |
| TS-006 | Error Handling Suite | 覆盖空列表、invalid value、already deleted 等异常场景 | Error Guessing |
| TS-007 | Regression Suite | 保留关键回归测试场景 | 风险与覆盖组合 |
| TS-008 | Optimized Execution Suite | 用较少用例保持关键覆盖 | 风险优先与覆盖优化 |
| TS-009 | Automation Mapping Suite | 将优化测试用例映射到 Selenium 场景 | pytest + Selenium |

实际报告中应以你们 `todoitem_test_suites.csv` 中的 suite 名称为准。如果表中名称与 CSV 不完全一致，建议使用 CSV 的真实名称，并在说明中解释它们对应的测试目标。

### 2.7 优化测试套件与覆盖说明

AutoTestDesign 先生成原始测试用例集合，再基于风险和覆盖效率生成 optimized test suite。当前 Todo Item Management 的测试设计结果如下：

| 项目 | 数量 |
|---|---:|
| 结构化需求 | 7 |
| 风险项 | 7 |
| 覆盖项 | 36 |
| 测试策略 | 36 |
| 原始测试用例 | 78 |
| 优化后测试用例 | 57 |
| 状态转换序列 | 11 |

优化的目标不是简单减少用例数量，而是在保留需求覆盖、风险覆盖、套件覆盖和关键状态覆盖的前提下，减少重复或相似的测试场景。优化后，57 个 test cases 仍覆盖 REQ-1 至 REQ-7，并保留了中风险需求的关键场景，例如 whitespace input、empty title edit、filter behavior、toggle all、clear completed 和状态转换行为。

需要注意的是，某些 coverage items 在 optimized suite 中可能不再以独立测试用例形式出现，而是被包含在更综合的场景中。例如，toggle completed 的状态转换测试可能同时覆盖 completed status 边界；filter 的综合场景可能同时覆盖 All、Active 和 Completed 三个筛选值。因此，在报告中应区分“独立用例覆盖”和“场景内间接覆盖”。

### 2.8 需求、覆盖项、测试用例之间的追溯关系

本项目通过 `todoitem_traceability_matrix.csv` 建立追溯关系。追溯链可以表示为：

```text
Requirement → Risk → Coverage Item → Test Strategy → Test Suite → Test Case → Automated Scenario → Execution Result
```

例如：

| Requirement | Risk | Coverage Item | Strategy | Test Case / Scenario | Expected Result |
|---|---|---|---|---|---|
| REQ-1 | RSK-1 | whitespace input boundary | BVA / EP | 输入只包含空白字符 | 不创建 Todo item |
| REQ-2 | RSK-2 | toggle completed state | State Transition Testing | active → completed → active | 状态正确切换 |
| REQ-3 | RSK-3 | save empty title | BVA / EP | 编辑 item 并保存空标题 | item 被删除 |
| REQ-6 | RSK-6 | filter values | EP / Decision Table | All / Active / Completed 筛选 | 显示结果与状态一致 |
| REQ-7 | RSK-7 | clear completed | EP / Error Guessing | 清除已完成 items | completed items 被移除，active items 保留 |

该追溯关系证明测试用例不是随意编写的，而是由需求和风险驱动，并且每个测试用例都可以回溯到明确的覆盖目标和测试技术。

### 2.9 人工审查与改进证据

Assignment 2 强调 AutoTestDesign 工具应支持 designer 的交互式审查和修改。因此，报告中应明确说明人工参与过程。

推荐写法如下：

在 AutoTestDesign 初始生成测试产物后，测试人员对 coverage items、test strategies 和 generated test cases 进行了人工审查。审查重点包括：

1. 检查 REQ-1 至 REQ-7 是否均有风险、覆盖项、测试策略和测试用例。
2. 检查黑盒技术是否覆盖 Equivalence Partitioning、Boundary Value Analysis 和 Decision Table Testing。
3. 检查是否补充了结构化 / 白盒建模技术，即 State Transition Testing。
4. 检查 optimized suite 是否保留关键风险和关键功能路径。
5. 检查 Selenium 自动化场景是否能够实际操作 UI，而不是只停留在抽象测试用例描述。

人工审查后，测试人员补充和确认了状态转换相关 suite，并将 57 个 optimized test cases 映射到可执行的 Selenium + pytest 场景中。此外，调试过程中发现测试状态隔离问题，因此补充了 UI 层清理逻辑，以保证每个测试用例开始前均处于稳定空列表状态。这些修改体现了 designer 对测试设计有效性的交互式验证和改进。

---

## 3. 测试工具实现

### 3.1 测试框架选择

本项目选择 **pytest + Selenium WebDriver** 作为测试执行框架。

选择 pytest 的原因包括：

- 支持简洁的测试函数和断言语法；
- 支持 fixture 管理测试环境和测试数据；
- 支持参数化测试，适合将多个 generated test cases 映射到统一执行框架；
- 输出结果清晰，便于统计 passed、failed、skipped 和 execution time。

选择 Selenium WebDriver 的原因包括：

- Todo Item Management 是 Web UI 功能，核心行为需要通过浏览器交互验证；
- Selenium 能够模拟用户真实操作，例如输入、点击、双击、键盘提交、鼠标悬停和筛选链接点击；
- Selenium 适合验证 UI 层可观察结果，例如 item 是否出现、是否被标记 completed、筛选结果是否正确、删除后是否消失。

因此，pytest 负责测试组织和执行，Selenium 负责浏览器级 UI 操作，两者结合适合本项目的详细测试执行需求。

### 3.2 自动化测试目标

自动化脚本 `test_todoitem_ui_selenium_full.py` 的目标是将 AutoTestDesign 生成的 optimized test suite 映射为可执行 UI 测试。

当前脚本覆盖：

```text
57 个 optimized AutoTestDesign test cases
+ 1 个 completeness guardrail test
= 58 个 pytest items
```

其中，57 个 optimized test cases 对应 `todoitem_optimized_test_suite.csv` 中的测试用例；额外的 guardrail test 用于确认脚本中的 `CASES` 列表确实包含全部 57 个 optimized cases，防止自动化脚本遗漏设计用例。

因此，最终自动化执行不是简单的代表性子集，而是对 optimized suite 的完整自动化映射。

### 3.3 脚本结构

测试脚本主要由以下部分组成：

| 结构 | 作用 |
|---|---|
| 配置常量 | 定义 `FRONTEND_URL`、`API_BASE_URL`、浏览器类型和 headless 模式 |
| API helper | 通过后端 API 查询和删除 Todo 数据，用于测试前清理 |
| Selenium driver fixture | 创建和关闭浏览器实例 |
| clean_state fixture | 在每个测试前重置数据和页面状态 |
| TodoPage Page Object | 封装 add、toggle、edit、delete、filter、clear completed 等 UI 操作 |
| scenario functions | 将具体测试场景封装为可复用函数 |
| CASES 列表 | 保存 57 个 optimized test cases 到 scenario 的映射 |
| 参数化 pytest 测试 | 遍历 CASES 并执行对应场景 |
| guardrail test | 验证 optimized cases 数量完整性 |

Page Object 的使用使测试脚本更易维护。例如，测试用例不直接操作 CSS selector，而是调用 `page.add()`、`page.toggle()`、`page.edit()`、`page.clear_completed()` 等方法。这样当 UI selector 或交互方式发生变化时，只需要修改 Page Object，而不需要修改大量测试用例。

### 3.4 优化测试用例到自动化场景的映射

由于 AutoTestDesign 生成的部分测试用例在 UI 层具有相同或相似的可观察行为，因此自动化脚本采用“测试用例 ID → scenario function”的映射方式。

例如：

| 测试设计目标 | 自动化场景 |
|---|---|
| 验证有效新增 item | 输入文本并断言 item 出现在列表中 |
| 验证空白输入不创建 item | 输入空白字符并断言 count 仍为 0 |
| 验证 toggle completed | 新增 item，点击 toggle，断言 completed 状态变化 |
| 验证重复 toggle | active → completed → active，断言最终状态恢复 |
| 验证编辑标题 | 双击 label，修改 title，按 Enter 保存，断言文本更新 |
| 验证空标题编辑删除 | 双击编辑，清空 title，保存，断言 item 消失 |
| 验证 delete item | 鼠标悬停，点击 destroy，断言 item 消失 |
| 验证 filter | 构造 active 和 completed items，点击 All / Active / Completed，断言显示列表正确 |
| 验证 clear completed | 构造 mixed list，点击 clear completed，断言 completed 被清除而 active 保留 |
| 验证 empty-list safe behavior | 空列表下尝试 toggle all 或 clear completed，断言应用不崩溃且列表仍为空 |

这种映射方式既保留了每个 optimized test case 的身份和追溯关系，又避免重复编写完全相同的 Selenium 操作代码。

### 3.5 测试独立性与数据重置

测试独立性是自动化执行中的关键问题。每个测试用例都必须在稳定且可预测的初始状态下运行，否则前一个测试遗留的数据可能影响后一个测试结果。

本项目最初使用后端 API 清理数据，即调用 `reset_todos()` 删除 API 中的 todos。但调试过程中发现，API 清理后当前页面 test-list 中仍可能显示遗留 items，说明 API 清理范围与页面当前 list scope 之间可能存在不一致。

因此，最终脚本采用双重清理策略：

1. 首先调用后端 API 删除已存在 todos；
2. 然后打开 Todo 页面；
3. 使用 UI 层删除当前页面仍可见的 Todo items；
4. 再次 reload 页面；
5. 断言当前 visible count 为 0。

这不是“通过 UI 清理来逃避功能问题”，而是测试 setup 的一部分。UI 清理只用于保证每个测试开始前状态为空，不作为被测功能是否通过的 oracle。真正的测试断言仍然在各个 scenario 中完成，例如新增后应出现 item、删除后应消失、clear completed 后应只保留 active items。

### 3.6 可执行性与限制

推荐运行方式如下：

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py
```

如果需要保存完整日志，可使用：

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py -q -rA --tb=short > pytest_full_output.txt 2>&1
```

或在 PowerShell 中边显示边保存：

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py -q -rA --tb=short 2>&1 | Tee-Object -FilePath pytest_full_output.txt
```

当前自动化脚本的主要限制包括：

- 主要验证 UI 层可观察结果，不能完全替代后端 API 层或数据库层测试；
- 对浏览器、前端服务和后端服务的可用性有依赖；
- 某些 UI 行为需要等待和重试，例如双击编辑、清空输入框和鼠标悬停删除；
- 非功能测试如性能、安全性、可访问性和兼容性不在本详细测试脚本范围内。

---

## 4. 测试结果分析

### 4.1 执行概要

最终 Selenium + pytest 自动化执行结果如下：

```text
collected 58 items
58 passed
execution time: 117.05 seconds
```

这 58 个 pytest items 包括：

```text
57 个 optimized AutoTestDesign test cases
+ 1 个 completeness guardrail test
```

因此，自动化执行结果表明：当前 optimized suite 的 57 个测试用例已经成功映射到 pytest + Selenium 脚本，并且全部通过执行。

### 4.2 通过、失败、跳过与预期失败用例

最终执行结果中：

| 结果类型 | 数量 | 说明 |
|---|---:|---|
| Passed | 58 | 所有测试项均通过 |
| Failed | 0 | 无失败用例 |
| Skipped | 0 | 无跳过用例 |
| XFailed | 0 | 无预期失败用例 |

在调试早期，曾经出现过 edit empty title、whitespace-only input、toggle all empty 和 clear completed 相关失败。后续分析表明，这些问题主要来自 Selenium 操作稳定性或测试数据隔离问题，而不是最终产品功能缺陷。通过改进 `edit()` 操作、增加重试、完善 UI 清理和初始状态断言后，最终所有测试通过。

### 4.3 缺陷或偏差分析

本轮最终执行没有保留 failed 或 xfailed 用例，因此没有尚未解决的自动化失败项。不过调试过程中发现了几个值得记录的偏差或工程问题：

1. **测试状态隔离问题**：单独运行某些测试可以通过，但完整运行时失败，说明测试之间存在状态污染。最终通过 API 清理 + UI 清理 + reload + assert count 为 0 的方式解决。
2. **编辑空标题的 Selenium 操作稳定性问题**：最初误以为编辑空标题不删除 item 是产品缺陷，后经手工验证发现产品行为正确，真正问题是 Selenium 清空输入框和保存动作不稳定。最终通过 Ctrl+A、Backspace、Enter 和 retry 机制解决。
3. **空列表下控件不存在的合理行为**：当列表为空时，toggle all、filter 和 clear completed 控件可能不显示。测试脚本不应强制点击不存在控件，而应验证应用在 empty-list 状态下保持稳定且不产生错误数据。

这些分析说明，测试结果分析不仅要记录最终 pass/fail，也要解释测试脚本和测试环境在调试过程中如何被改进。

### 4.4 执行后的覆盖有效性评价

最终测试执行支持以下覆盖结论：

| 覆盖维度 | 结论 |
|---|---|
| 需求覆盖 | REQ-1 至 REQ-7 均有测试用例和自动化执行场景 |
| 风险覆盖 | RSK-1 至 RSK-7 均被对应测试覆盖，中风险需求获得重点覆盖 |
| 覆盖项覆盖 | 36 个 coverage items 在设计层面均有测试用例覆盖，optimized suite 保留关键覆盖目标 |
| 测试套件覆盖 | 9 个 test suites 均在设计层面具有测试用例，optimized suite 覆盖主要 suite 目标 |
| 技术覆盖 | 使用 EP、BVA、Decision Table Testing、State Transition Testing 和 Error Guessing |
| 自动化覆盖 | 57 个 optimized test cases 全部映射到 Selenium + pytest，并额外使用 1 个 guardrail test 检查完整性 |

因此，本项目的详细测试设计在设计层面和执行层面均较完整。需要注意的是，“完整”指的是对选定 feature，即 Todo Item Management 的完整覆盖，而不是对整个 SimpleTodoList 项目的所有模块完整覆盖。

### 4.5 改进建议

后续可从以下方向进一步改进：

1. **补充 API 层测试**：当前自动化主要是 UI 测试，可以增加 REST API 层测试，用于验证后端数据创建、更新、删除和持久化。
2. **补充非功能测试**：例如性能测试、安全性测试、兼容性测试和可用性测试。
3. **增强测试 oracle**：除了检查 UI 文本和 class，还可以检查 API 返回数据或数据库状态，提高断言可信度。
4. **完善测试报告自动生成**：将 pytest 结果自动导出为 HTML 或 JUnit XML，并与 traceability matrix 关联。
5. **增强 AutoTestDesign 工具交互能力**：允许 tester 在 UI 中更方便地修改 coverage items、test strategies 和 generated test cases，并保存修改历史。

---

## 5. 结论

本详细测试设计与执行文档说明了如何使用 AutoTestDesign 工具对 SimpleTodoList 的 Todo Item Management 功能进行系统化测试设计和自动化执行。

从设计层面看，REQ-1 至 REQ-7 均具有对应风险、覆盖项、测试策略、测试用例和追溯关系。测试设计使用了 Equivalence Partitioning、Boundary Value Analysis、Decision Table Testing 等多种黑盒测试技术，并使用 State Transition Testing 作为结构化 / 白盒建模技术，满足 Assignment 2 对测试技术的要求。

从执行层面看，优化后的 57 个 test cases 已全部映射到 Selenium + pytest 自动化脚本，并通过一个额外的 guardrail test 检查自动化映射完整性。最终 pytest 共收集 58 个测试项，执行结果为 58 passed。

因此，对于选定的 Todo Item Management feature，本项目实现了从需求、风险、覆盖项、测试策略、测试用例、自动化场景到执行结果的完整证据链。该工作能够证明 AutoTestDesign 工具在目标应用测试中的有效性，同时也展示了人工审查和自动化执行在提高测试设计质量方面的重要作用。

---

## 附录 A：主要测试产物清单

| 文件名 | 说明 |
|---|---|
| `todoitem_requirements_structured.csv` | 结构化需求 |
| `todoitem_risk_analysis.csv` | 风险分析结果 |
| `todoitem_coverage_items.csv` | 覆盖项 |
| `todoitem_test_strategies.csv` | 测试策略 |
| `todoitem_test_suites.csv` | 测试套件 |
| `todoitem_test_cases.csv` | 原始测试用例 |
| `todoitem_optimized_test_suite.csv` | 优化后测试用例 |
| `todoitem_traceability_matrix.csv` | 追溯矩阵 |
| `todoitem_state_transitions.csv` | 状态转换序列 |
| `todoitem_test_suite_artifacts.json` | 综合 JSON 产物 |
| `todoitem_test_design_artifacts.xlsx` | Excel 测试设计产物 |
| `test_todoitem_ui_selenium_full.py` | Selenium + pytest 自动化脚本 |
| `todoitem_coverage_analysis_report.md` | 覆盖分析说明 |
| `selenium_pytest_debug_summary.md` | Selenium + pytest 调试总结 |

---

## 附录 B：运行命令

### 启动前端

```powershell
[待填写：你们实际启动前端服务的命令]
```

### 启动后端

```powershell
[待填写：你们实际启动 FastAPI / 后端服务的命令]
```

### 执行 Selenium + pytest 测试

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py
```

### 保存完整 pytest 日志

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py -q -rA --tb=short > pytest_full_output.txt 2>&1
```

---

## 附录 C：术语表

| 术语 | 说明 |
|---|---|
| Requirement | 被测功能的结构化需求 |
| Risk | 功能可能失效的产品风险 |
| Risk Score | 风险分值，通常由影响度和可能性计算得到 |
| Coverage Item | 需要被测试覆盖的具体对象，例如输入、条件、边界、状态或功能行为 |
| Test Strategy | 针对覆盖项选择的测试设计方法 |
| Test Case | 由覆盖项和测试策略推导出的具体测试用例 |
| Test Suite | 按测试目标或技术组织的一组测试用例 |
| Optimized Test Suite | 基于风险和覆盖效率优化后的测试用例集合 |
| Traceability Matrix | 记录需求、风险、覆盖项、测试策略、测试套件和测试用例之间关系的矩阵 |
| State Transition Testing | 通过状态和状态变化设计测试用例的结构化测试技术 |
| Selenium WebDriver | 用于浏览器 UI 自动化测试的工具 |
| pytest | Python 测试框架，用于组织、执行和报告测试结果 |
