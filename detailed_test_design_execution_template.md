# Detailed Test Design and Execution Document 模板与推荐填充

> 使用说明：
> 1. 第一部分是**纯模板**，适合直接复制为正式报告骨架。
> 2. 第二部分是**带推荐撰写内容的填充版**，已经结合当前 Todo Item Management、AutoTestDesign 产物、Selenium + pytest 脚本和最终调试结果进行推荐写作。
> 3. 第二部分中的英文段落可以直接放入英文报告；中文说明用于帮助你理解每节应该写什么。
> 4. 文中 `[TODO: ...]` 表示需要你们按小组实际信息补充，例如 Team ID、成员姓名、仓库路径、运行环境版本等。

---

# Part A. 纯模板

# Detailed Test Design and Execution Document

## Cover Page

- Project: `[TODO: Project Name]`
- Deliverable: Detailed Test Design and Execution Document
- Target Application: `[TODO: Target Application]`
- Selected Feature / Module: `[TODO: Selected Feature / Module]`
- Team ID: `[TODO: Team ID]`
- Team Members: `[TODO: Names and Student IDs]`
- Date: `[TODO: Submission Date]`

---

## 1. Introduction

### 1.1 Purpose

`[说明本文档目的：针对选定 feature/module，使用 AutoTestDesign 工具完成详细测试设计，并基于设计结果实现测试执行。]`

### 1.2 Scope

`[说明测试对象、测试模块、覆盖功能、不覆盖范围。]`

### 1.3 Test Environment

`[列出前端地址、后端地址、测试框架、浏览器、主要脚本、主要导出文件。]`

### 1.4 Document Structure

`[说明本文档后续章节结构：测试设计、工具实现、执行结果、覆盖评价、限制与改进。]`

---

## 2. Detailed Test Case Design

### 2.1 Selected Feature / Module

`[说明为什么选择该功能模块，以及该模块为什么适合展示测试设计技术。]`

### 2.2 Requirement and Risk Basis

`[说明测试用例设计基于哪些结构化需求、风险分析、覆盖项、测试策略和测试用例导出文件。]`

### 2.3 Test Design Workflow

`[说明从需求输入到测试用例生成、人工审查、优化、自动化映射的流程。]`

### 2.4 Coverage Item Identification

`[说明覆盖项如何从功能、输入、条件、异常场景、状态转换中识别出来。]`

### 2.5 Coverage Strategy and Test Design Techniques

`[说明每类覆盖项选择了什么测试技术，以及为什么选择。]`

#### 2.5.1 Black-box Techniques

`[说明等价划分、边界值分析、决策表测试等黑盒技术的使用。]`

#### 2.5.2 White-box / Structural Modeling Technique

`[说明状态转换测试或其他结构化/白盒建模技术的使用。]`

### 2.6 Test Case Suite Structure

`[说明 AutoTestDesign 生成的 test suites 划分，以及每个 suite 的主要测试技术和目标。]`

### 2.7 Optimized Test Suite and Coverage Explanation

`[说明原始用例数量、优化后用例数量、优化依据，以及优化后覆盖是否仍然保留。]`

### 2.8 Traceability

`[说明 Requirement -> Risk -> Coverage Item -> Strategy -> Test Suite -> Test Case -> Automation 的追溯链。]`

### 2.9 Human Review and Improvement Evidence

`[说明人类 tester 如何参与审查、修改和改进 coverage items、strategies、test cases 或 automation mapping。]`

---

## 3. Test Tool Implementation

### 3.1 Framework Selection

`[说明为什么选择 pytest、Selenium、API helper、浏览器等。]`

### 3.2 Automation Target

`[列出被测前端页面、后端 API、测试脚本、优化测试套件来源。]`

### 3.3 Script Structure

`[说明脚本结构：配置、清理 helper、pytest fixtures、Page Object、atomic scenarios、CASES 映射、参数化执行。]`

### 3.4 Mapping from Optimized Test Cases to Automation

`[说明每个 optimized test case 如何映射到 test_case_id、suite_id、coverage_id、scenario function。]`

### 3.5 Test Independence and Data Reset

`[说明每个测试前如何清理状态，为什么 UI-level cleanup 是测试隔离而不是测试 oracle。]`

### 3.6 Executability and Limitations

`[说明哪些场景可直接 UI 自动化，哪些抽象异常场景采用 UI 层近似实现，以及限制。]`

---

## 4. Test Result Analysis

### 4.1 Execution Summary

`[说明 pytest 收集了多少测试项、通过多少、失败多少、执行时间。]`

### 4.2 Passed / Failed / XFail Cases

`[总结 passed、failed、skipped、xfail、xpassed 的数量和意义。]`

### 4.3 Defect or Deviation Analysis

`[说明执行中发现的问题是产品缺陷、需求偏差、脚本不稳定，还是测试环境隔离问题。]`

### 4.4 Coverage Effectiveness After Execution

`[说明执行结果如何证明设计覆盖和自动化映射有效。]`

### 4.5 Improvement Suggestions

`[说明后续可改进方向，例如 API 清理接口、覆盖率报告、更多浏览器、CI 集成等。]`

---

## 5. Conclusion

`[总结选定 feature 的设计覆盖、技术覆盖、自动化执行结果和剩余限制。]`

---

## Appendix A. Main Artifacts

`[列出所有输入/输出文件。]`

## Appendix B. Example Test Case Mapping

`[放少量 test case 到 scenario 的映射示例。]`

## Appendix C. Execution Command and Output

`[放运行命令和最终 pytest 输出。]`

---

# Part B. 带推荐撰写内容的模板填充

# Detailed Test Design and Execution Document

## Cover Page

**Project:** AutoTestDesign-based Testing for SimpleTodoList  
**Deliverable:** Detailed Test Design and Execution Document  
**Target Application:** SimpleTodoList  
**Selected Feature / Module:** Todo Item Management  
**Team ID:** `[TODO: Team ID]`  
**Team Members:** `[TODO: Names and Student IDs]`  
**Date:** `[TODO: Submission Date]`

**推荐说明：**  
封面页要明确这是 Assignment 2 的第 4 个交付物，即 Detailed Test Design and Execution Document。注意不要写成“测试 AutoTestDesign 工具本身”，而要写成“使用 AutoTestDesign 工具测试自选目标应用 SimpleTodoList”。

---

## 1. Introduction

### 1.1 Purpose

**推荐撰写内容：**

This document presents the detailed test design and execution work for the selected **Todo Item Management** feature of the SimpleTodoList target application. The test cases were designed using the developed **AutoTestDesign** tool, which supports requirement structuring, risk analysis, coverage item identification, test strategy selection, test case generation, test suite optimization, and export of structured test artifacts.

The purpose of this document is to demonstrate how the generated test design artifacts are traced from requirements and risks to coverage items, test strategies, test suites, detailed test cases, and Selenium-based automated execution. The document also explains the selected black-box and structural testing techniques, the implementation of pytest + Selenium test scripts, and the final execution result of the optimized test suite.

**中文说明：**  
这一节要回答“这份文档是干什么的”。建议直接点明三件事：

1. 被测对象是 SimpleTodoList，不是 AutoTestDesign 工具本身。
2. 选定 feature 是 Todo Item Management。
3. 本文档证明从需求到覆盖项、策略、用例、自动化、结果的完整证据链。

---

### 1.2 Scope

**推荐撰写内容：**

The scope of this detailed test design is limited to the **Todo Item Management** feature of SimpleTodoList. The covered behaviors include:

- adding a new Todo item;
- rejecting whitespace-only input;
- marking and unmarking a Todo item as completed;
- editing the title of a Todo item;
- deleting a Todo item when the edited title is empty;
- deleting a single Todo item;
- toggling all Todo items between active and completed states;
- filtering Todo items by All, Active, and Completed views;
- clearing all completed Todo items;
- handling selected invalid or abnormal UI states safely.

This document does not aim to fully test other modules of the application, such as Admin authentication, Todo List management, backend API security, or whole-system persistence risks. Those areas are covered by the broader risk analysis report and test plan. The current deliverable focuses on detailed test design and execution for one major feature/module, as required by the assignment.

**中文说明：**  
这一节要主动划清范围。你们只测 Todo Item Management 是合理的，因为 Assignment 2 第 4 项要求的是“one major feature/module”。这里要避免老师误以为你们漏测了 Admin、List Management、API 安全等模块。

---

### 1.3 Test Environment

**推荐撰写内容：**

| Item | Description |
|---|---|
| Target application | SimpleTodoList |
| Selected module | Todo Item Management |
| Frontend URL | `http://127.0.0.1:8000/todo.html#/&test-list` |
| Backend API URL | `http://127.0.0.1:5000/api` |
| Automation framework | pytest + Selenium WebDriver |
| Browser | Chrome by default; Edge/Firefox supported through environment variable |
| Main script | `Assignment2/tests/test_todoitem_ui_selenium_full.py` |
| Main optimized suite input | `todoitem_optimized_test_suite.csv` |
| Main design artifacts | CSV / JSON / XLSX files exported by AutoTestDesign |

**中文说明：**  
这一节可以写成表格，简洁清楚。注意你们的脚本中确实有 `FRONTEND_URL`、`API_BASE_URL`、`BROWSER`、`HEADLESS` 等配置项，所以这里写环境变量支持是合理的。

---

### 1.4 Document Structure

**推荐撰写内容：**

The remainder of this document is organized as follows. Section 2 explains the detailed test case design process, including the selected feature, requirement and risk basis, coverage item identification, test design techniques, suite structure, optimization, traceability, and human review evidence. Section 3 describes the Selenium + pytest implementation, including framework selection, script structure, test case mapping, and test independence. Section 4 summarizes the execution results and analyzes coverage effectiveness after execution. Section 5 concludes the document and highlights the main achievements and remaining limitations.

**中文说明：**  
这一节就是告诉读者后面怎么读，不需要太长。

---

## 2. Detailed Test Case Design

### 2.1 Selected Feature / Module

**推荐撰写内容：**

The selected feature for detailed test design is **Todo Item Management**. This feature is the core user-facing function of SimpleTodoList and contains multiple behaviors suitable for systematic test design, including input validation, CRUD operations, item status changes, filtering, bulk operations, and state-dependent UI behavior.

This feature was selected because it allows the testing process to demonstrate multiple required testing techniques. Equivalence Partitioning and Boundary Value Analysis can be applied to Todo item inputs and empty-title cases. Decision Table Testing can be applied to conditional behavior such as clearing completed items. State Transition Testing can be applied to the lifecycle of Todo items, such as transitions from an empty list to a list with items, from active to completed, and from all completed to empty after clearing completed items.

**中文说明：**  
这里要强调 Todo Item Management 是核心功能，而且它天然适合展示黑盒 + 白盒/结构化技术。不要只写“我们选择了 Todo Item”，要写为什么它适合作为详细测试对象。

---

### 2.2 Requirement and Risk Basis

**推荐撰写内容：**

The detailed test design is based on structured artifacts exported by AutoTestDesign. These artifacts provide the basis for requirement coverage, risk-based prioritization, coverage item identification, test strategy selection, test case generation, optimization, and traceability.

| Artifact | Purpose in This Document |
|---|---|
| `todoitem_requirements_structured.csv` | Stores structured Todo Item requirements, including input fields, data ranges, conditions, actions, and expected results. |
| `todoitem_risk_analysis.csv` | Assigns risk score and risk level to each Todo Item requirement. |
| `todoitem_coverage_items.csv` | Defines coverage targets derived from requirements, risks, input conditions, boundaries, and state behaviors. |
| `todoitem_test_strategies.csv` | Maps coverage items to selected test design techniques such as EP, BVA, Decision Table Testing, and State Transition Testing. |
| `todoitem_test_suites.csv` | Groups test cases into test suites according to risk, coverage type, and testing technique. |
| `todoitem_test_cases.csv` | Contains the full generated candidate test cases before optimization. |
| `todoitem_optimized_test_suite.csv` | Contains the optimized execution set used as the main automation mapping source. |
| `todoitem_traceability_matrix.csv` | Provides traceability from requirements and coverage items to generated test cases. |
| `todoitem_state_transitions.csv` | Defines the state transition model and optimized transition sequence for Todo Item behavior. |

The selected feature contains seven structured requirements, from **REQ-1** to **REQ-7**, covering add, toggle, edit, delete, toggle-all, filter, and clear-completed behaviors. Each requirement is associated with at least one risk item and multiple coverage items.

**中文说明：**  
这一节是“证据链”的入口。建议不要把 CSV 内容全部贴上来，而是用表格说明每个 artifact 的作用。老师看重的是你们的用例不是凭空写的，而是由需求、风险、覆盖项、策略逐层推导出来的。

---

### 2.3 Test Design Workflow

**推荐撰写内容：**

The test design followed the workflow below:

1. Import Todo Item Management requirements into AutoTestDesign.
2. Structure each requirement into input fields, data ranges, conditions, actions, and expected results.
3. Perform risk analysis and assign risk score and test priority.
4. Identify coverage items from functional behavior, input partitions, boundary conditions, decision conditions, abnormal scenarios, and state transitions.
5. Select appropriate coverage strategies and test design techniques for each coverage item.
6. Generate detailed candidate test cases.
7. Generate and review the traceability matrix.
8. Optimize the test suite based on risk level, coverage efficiency, and duplicate reduction.
9. Map optimized test cases to executable Selenium UI scenarios.
10. Execute the mapped suite using pytest and analyze the results.

| Step | Input | Output |
|---|---|---|
| Requirement structuring | Todo feature descriptions | Structured requirements |
| Risk analysis | Structured requirements | Risk scores and priorities |
| Coverage identification | Requirements + risks | Coverage items |
| Strategy selection | Coverage items | Test techniques |
| Test generation | Coverage items + strategies | Candidate test cases |
| Optimization | Candidate cases + risk/coverage criteria | Optimized test suite |
| Automation mapping | Optimized cases | Selenium scenario functions |
| Execution | Selenium script | pytest result summary |

**中文说明：**  
这一节要强行对齐 Assignment2 的 “Concept -> Coverage Item Identification -> Coverage Strategy & Method -> Test Cases and Traceability -> results analysis -> improvement with evidence”。这样老师能明显看到你们按作业要求做了。

---

### 2.4 Coverage Item Identification

**推荐撰写内容：**

Coverage items were identified from multiple perspectives to ensure that the generated test design covers both normal and abnormal Todo Item behaviors.

| Coverage Area | Example Coverage Items | Related Requirement |
|---|---|---|
| Add item | Add valid item; reject whitespace-only item | REQ-1 |
| Toggle status | Change active item to completed; change completed item back to active | REQ-2 |
| Edit item | Edit to non-empty title; edit to empty title | REQ-3 |
| Delete item | Delete a single existing item; safely handle already deleted item | REQ-4 |
| Toggle all | Toggle all active items to completed; toggle all completed items back to active; handle empty list safely | REQ-5 |
| Filter | Show all items; show active items; show completed items; handle invalid filter safely | REQ-6 |
| Clear completed | Clear completed items while keeping active items; clear when all items are completed; handle no-completed-item case safely | REQ-7 |
| State transition | Empty List -> List with Items; List with Items -> All Completed; All Completed -> Empty List; List with Items -> Filtered View | REQ-1 to REQ-7 |

The coverage items include functional coverage, input coverage, boundary coverage, condition coverage, error-handling coverage, and state-transition coverage. This helps avoid limiting the test design to only happy-path UI actions.

**中文说明：**  
这一节是覆盖充分性的核心。建议明确写 coverage item 不只是“功能点”，还包括 input、boundary、condition、error、state transition。

---

### 2.5 Coverage Strategy and Test Design Techniques

**推荐撰写内容：**

The coverage strategy was selected according to the nature of each coverage item. Input-oriented coverage items were mainly tested by Equivalence Partitioning and Boundary Value Analysis. Conditional behavior was tested by Decision Table Testing. State-dependent Todo behavior was tested by State Transition Testing.

The test design uses multiple black-box testing techniques and one structural modeling technique, satisfying the assignment requirement that the selected feature/module should be tested using multiple black-box techniques and also white-box or structure-based techniques.

**中文说明：**  
这里先总说，再分 2.5.1 和 2.5.2。注意 Assignment2 明确要求 multiple black-box techniques and also white-box techniques，因此这节要写得很明确。

---

#### 2.5.1 Black-box Techniques

**推荐撰写内容：**

The following black-box testing techniques were applied:

| Technique | Why It Was Used | Example in Todo Item Management |
|---|---|---|
| Equivalence Partitioning | To divide inputs or actions into valid and invalid classes. | Valid Todo text vs whitespace-only Todo text; valid filter vs invalid filter. |
| Boundary Value Analysis | To test boundary conditions around empty, whitespace, or minimal input. | Empty edited title; whitespace-only item input. |
| Decision Table Testing | To model behavior controlled by combinations of conditions. | Clear completed when completed items exist vs when no item is completed. |

For example, Todo item input can be divided into valid non-empty text and invalid whitespace-only input. The edit title behavior includes a boundary case where saving an empty title should delete the item. The clear-completed behavior depends on whether completed items exist, which makes it suitable for decision-rule testing.

**中文说明：**  
这里建议用表格，老师很容易看出你们用了三种黑盒技术：EP、BVA、Decision Table。

---

#### 2.5.2 White-box / Structural Modeling Technique

**推荐撰写内容：**

State Transition Testing was used as the structural modeling technique for Todo Item Management. Although the tests are executed through the UI, the model focuses on the internal behavior of the Todo item lifecycle and the transitions caused by user actions.

| State | Meaning |
|---|---|
| Empty List | No Todo item exists in the current list. |
| List with Items | At least one active or completed Todo item exists. |
| All Completed | All visible Todo items are completed. |
| Filtered View | The user is viewing All, Active, or Completed filtered results. |

| Transition | Event / Action |
|---|---|
| Empty List -> List with Items | Add a valid Todo item. |
| List with Items -> All Completed | Toggle all items to completed. |
| All Completed -> Empty List | Clear completed items. |
| List with Items -> Filtered View | Apply Active or Completed filter. |
| List with Items -> List with Items | Edit, toggle, or delete a subset of items. |

The state transition suite validates optimized transition sequences, including transitions TR-001 to TR-011. This provides structural coverage beyond simple input-output examples.

**中文说明：**  
这里把 State Transition Testing 写成 white-box / structural modeling technique。严格讲 UI 自动化是黑盒执行，但你们设计层面使用了结构化状态模型，所以可以这样写：execution through UI, design based on structural state model。

---

### 2.6 Test Case Suite Structure

**推荐撰写内容：**

AutoTestDesign organized the generated test cases into multiple test suites according to coverage type, risk, and test design technique.

| Suite ID | Suite Type | Main Technique | Main Objective |
|---|---|---|---|
| TS-001 | Boundary Suite | Boundary Value Analysis | Validate boundary-related Todo input and edit cases. |
| TS-002 | Decision Rule Suite | Decision Table Testing | Validate condition-dependent behavior such as clear completed. |
| TS-003 | Partition Suite | Equivalence Partitioning | Validate valid and invalid condition classes. |
| TS-004 | Core Behavior Partition Suite | Equivalence Partitioning | Validate core behavior classes for major Todo actions. |
| TS-005 | Input Partition Suite | Equivalence Partitioning | Validate input/control partitions. |
| TS-006 | State Behavior Suite | State Transition Testing | Validate state-dependent user actions. |
| TS-007 | Error / State Behavior Suite | State Transition Testing / Error-oriented testing | Validate safe handling of abnormal states. |
| TS-008 | LLM Missing Case State Suite | State Transition Testing | Validate additional state cases suggested during review. |
| TS-009 | State Transition Model Suite | State Transition Testing | Validate optimized transition sequence for state model coverage. |

This structure ensures that the generated tests are not a flat list of UI actions. Instead, each suite has a clear design purpose and is linked to coverage criteria and testing techniques.

**中文说明：**  
这一节不用贴 57 条用例。只解释 suite 结构即可。重点是证明你们的用例分组有设计依据。

---

### 2.7 Optimized Test Suite and Coverage Explanation

**推荐撰写内容：**

AutoTestDesign first generated a full set of candidate test cases and then produced an optimized test suite based on risk and coverage efficiency. The optimized suite reduces redundant cases while preserving requirement-level and suite-level coverage for the selected Todo Item Management feature.

| Check Item | Result |
|---|---|
| Structured requirements | REQ-1 to REQ-7 covered |
| Risk coverage | Each requirement has an associated risk item |
| Coverage items | Coverage items derived from functions, inputs, conditions, boundaries, errors, and states |
| Strategy coverage | EP, BVA, Decision Table Testing, and State Transition Testing used |
| Test suite coverage | TS-001 to TS-009 retained |
| Optimized test cases | 57 optimized cases used for automation mapping |
| State transitions | 11 state-transition sequences included |
| Automation mapping | All 57 optimized cases mapped to Selenium scenarios |

The optimized suite is therefore suitable as the execution basis because it keeps the most important requirement, risk, and suite coverage while reducing duplicate or low-value test cases.

**中文说明：**  
这里要写“优化不是偷工减料”，而是 risk-based / coverage-based reduction。你们最终脚本已经把 57 个 optimized cases 都映射了，所以这里可以写 all 57 optimized cases mapped to Selenium scenarios。

---

### 2.8 Traceability

**推荐撰写内容：**

Traceability is maintained across the whole test design process:

```text
Requirement -> Risk -> Coverage Item -> Strategy -> Test Suite -> Test Case -> Selenium Scenario
```

| Traceability Level | Artifact / Evidence |
|---|---|
| Requirement | `todoitem_requirements_structured.csv` |
| Risk | `todoitem_risk_analysis.csv` |
| Coverage Item | `todoitem_coverage_items.csv` |
| Strategy | `todoitem_test_strategies.csv` |
| Test Suite | `todoitem_test_suites.csv` |
| Test Case | `todoitem_test_cases.csv` and `todoitem_optimized_test_suite.csv` |
| Traceability Matrix | `todoitem_traceability_matrix.csv` |
| Automation | `test_todoitem_ui_selenium_full.py` |

For automated execution, the Selenium script preserves this traceability by mapping each optimized test case ID to a suite ID, coverage ID, and executable scenario function. This makes it possible to explain not only whether a test passed, but also which requirement, coverage item, and strategy the test supports.

**中文说明：**  
这一节是很重要的评分点。Assignment2 的 “Test Cases and Traceability of Their Design” 就是要你们写这个。建议保留这条链。

---

### 2.9 Human Review and Improvement Evidence

**推荐撰写内容：**

The test design was not treated as a fully automatic one-shot output. Human review was performed after the initial AutoTestDesign generation. The review focused on whether the generated coverage items, strategies, optimized cases, and automation mappings were meaningful and executable for the actual Todo UI.

Several improvements were made during review and debugging:

1. State transition coverage was emphasized to better represent the Todo item lifecycle.
2. Empty-list behavior for toggle-all was clarified as a safe invalid-control scenario.
3. Clear completed behavior was separated from test setup cleanup to avoid confusing setup actions with test oracle assertions.
4. Edit-empty-title behavior was rechecked manually and then stabilized in Selenium by improving the edit operation.
5. UI-level cleanup was introduced only as a test isolation mechanism when backend reset did not reliably clear the current list-scoped UI data.
6. A guardrail test was added to verify that the automation mapping contains all 57 optimized test cases.

These changes demonstrate interactive design review and evidence-based improvement. They also show that the tester participated in reviewing, revising, and validating the tool-generated design items instead of accepting the generated output blindly.

**中文说明：**  
这一节建议一定加。Assignment2 特别强调 designer’s participation 和 interactive review。你们可以把这次调试过程写成“人工审查与改进证据”，这会比只写“LLM 自动生成”强很多。

---

## 3. Test Tool Implementation

### 3.1 Framework Selection

**推荐撰写内容：**

The automated execution was implemented using **pytest + Selenium WebDriver**.

| Tool / Component | Role |
|---|---|
| pytest | Test runner, fixture management, parameterized execution, and result reporting. |
| Selenium WebDriver | Browser-based UI automation that simulates user interactions. |
| Page Object Pattern | Encapsulates UI operations such as add, edit, toggle, delete, filter, and clear completed. |
| Backend API helper | Attempts to reset Todo data before each test. |
| UI cleanup fallback | Deletes visible Todo items before each test to guarantee test isolation. |
| Chrome / Edge / Firefox | Browser execution targets supported by the script. |

pytest was selected because it supports fixtures, parameterized tests, and concise execution reports. Selenium was selected because the target application is a web application and the test cases need to validate user-visible UI behavior.

**中文说明：**  
这里重点解释为什么选 pytest + Selenium。不要只说“我们用了 Selenium”，要说它和目标应用、UI 操作、pytest 参数化之间的关系。

---

### 3.2 Automation Target

**推荐撰写内容：**

The automation targets the Todo Item page and the supporting backend API used during test setup.

| Target | Value |
|---|---|
| Frontend page | `http://127.0.0.1:8000/todo.html#/&test-list` |
| Backend API | `http://127.0.0.1:5000/api` |
| Test script | `Assignment2/tests/test_todoitem_ui_selenium_full.py` |
| Optimized suite source | `todoitem_optimized_test_suite.csv` |
| Number of optimized cases | 57 |
| Number of pytest items | 58, including 57 optimized cases and 1 guardrail test |

**中文说明：**  
这里把自动化目标写清楚。尤其要说明 58 个 pytest items 不是 58 个 optimized cases，而是 57 个 optimized cases + 1 个 guardrail。

---

### 3.3 Script Structure

**推荐撰写内容：**

The Selenium script is structured into the following parts:

1. **Configuration**
   - `FRONTEND_URL`
   - `API_BASE_URL`
   - `BROWSER`
   - `HEADLESS`

2. **Backend cleanup helpers**
   - `api_request()`
   - `reset_todos()`

3. **pytest fixtures**
   - `driver()` creates and closes the browser.
   - `clean_state()` resets the test state before every case.
   - `page()` provides the Page Object.

4. **Page Object**
   - `add()` / `add_raw()`
   - `edit()`
   - `delete()`
   - `toggle()`
   - `toggle_all_once()` / `toggle_all_if_present()`
   - `filter_all()` / `filter_active()` / `filter_completed()` / `filter_invalid()`
   - `clear_completed()` / `clear_completed_if_present()`
   - assertion helpers such as `assert_visible()` and `assert_count()`

5. **Atomic UI scenario functions**
   - Each scenario function implements one reusable UI behavior, such as adding a valid item, ignoring whitespace input, toggling completed status, editing empty title, filtering active items, or clearing completed items.

6. **Optimized suite mapping**
   - The `CASES` list maps each optimized test case ID to a suite ID, coverage ID, and scenario function.

7. **Parameterized pytest execution**
   - One pytest parameterized item is executed for each optimized test case.
   - A guardrail test verifies that the mapping contains all 57 optimized cases.

**中文说明：**  
这一节要体现工程结构。建议用编号列表，不需要贴完整代码。

---

### 3.4 Mapping from Optimized Test Cases to Automation

**推荐撰写内容：**

The automation script uses a `CASES` list to map each optimized AutoTestDesign test case to an executable Selenium scenario. Each mapping entry contains:

- `test_case_id`
- `suite_id`
- `coverage_id`
- executable scenario function
- pytest display ID

Example mapping entries are shown below:

| Test Case ID | Suite ID | Coverage ID | Selenium Scenario |
|---|---|---|---|
| TC-066 | TS-009 | COV-STATE-TR-001 | Add valid item |
| TC-067 | TS-009 | COV-STATE-TR-003 | Toggle item completed |
| TC-068 | TS-009 | COV-STATE-TR-004 | Edit title to non-empty |
| TC-069 | TS-009 | COV-STATE-TR-005 | Edit title to empty and delete item |
| TC-070 | TS-009 | COV-STATE-TR-006 | Delete single item |
| TC-071 | TS-009 | COV-STATE-TR-007 | Toggle all to completed |
| TC-075 | TS-009 | COV-STATE-TR-002 | Add whitespace input and verify ignored |
| TC-076 | TS-009 | COV-STATE-TR-011 | Clear completed from all-completed state |

The complete mapping is maintained in the script rather than repeated in full in this document. This avoids duplication while preserving traceability through IDs.

**中文说明：**  
这里不建议贴 57 条完整映射，太长。贴 8 条示例即可，然后说明完整映射在脚本 CASES 中。

---

### 3.5 Test Independence and Data Reset

**推荐撰写内容：**

Each test case must start from a deterministic state. Initially, the script used the backend helper `reset_todos()` to delete existing Todo data. During debugging, it was found that backend cleanup did not always remove the current list-scoped Todo items shown on the UI. This caused state pollution between tests.

To solve this, the final script performs the following setup before each test:

1. Try to reset Todo data through the backend API.
2. Open the Todo Item page for the current test list.
3. If any visible Todo items remain, delete them one by one through the UI destroy control.
4. Reload the page.
5. Assert that the visible Todo count is zero.

This UI-level cleanup is used only as a **test isolation setup step**. It is not used as the oracle for the feature under test. Each actual test scenario still creates its own test data, performs the target action, and verifies the expected result independently.

**推荐英文总结句：**

Due to list-scoped API cleanup limitations during automation setup, UI-level cleanup was used before each test to guarantee test isolation. This cleanup is not part of the test oracle; it is only a setup step to ensure that each automated case starts from a known empty Todo list.

**中文说明：**  
这一节是你之前最担心的“是不是耍小聪明”。报告里要主动解释：UI 清理是 test isolation，不是测试断言。Clear completed 功能本身有独立测试，不是靠清理步骤混过去。

---

### 3.6 Executability and Limitations

**推荐撰写内容：**

Most optimized test cases can be executed directly through the UI. However, some generated cases describe abstract or abnormal conditions that are not directly exposed as simple UI operations. For these cases, the automation uses practical UI-level approximations while preserving the original test case ID, suite ID, and coverage ID.

Examples include:

| Abstract Generated Condition | Automation Approximation |
|---|---|
| List full or unavailable | Add many Todo items and verify the app still handles another add safely. |
| Editing an already deleted item | Delete the item first and then verify the app remains usable. |
| Invalid filter value | Navigate to an invalid hash/filter state and verify safe handling. |
| Toggle all on empty list | Verify that no toggle-all control is available or clickable, and the app remains usable. |

These approximations are acceptable because they keep the intent of the original coverage item while making the test executable through the current UI. The limitation is that some deeper internal failure modes, such as database-level failure or API unavailability, are not fully simulated in the UI automation.

**中文说明：**  
这里要诚实写限制。不是所有抽象异常都能 100% 通过 UI 构造，所以用“UI-level approximation”解释。这样比假装全部完美更可信。

---

## 4. Test Result Analysis

### 4.1 Execution Summary

**推荐撰写内容：**

The final automated test execution was performed using the following command:

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py
```

Final result:

```text
collected 58 items
Assignment2\tests\test_todoitem_ui_selenium_full.py ................. [ 29%]
.........................................                             [100%]

====================== 58 passed in 117.05s (0:01:57) ======================
```

The 58 pytest items consist of:

- 57 optimized AutoTestDesign test cases;
- 1 coverage-completeness guardrail test.

**中文说明：**  
这里直接放最终结果。注意写清楚 58 = 57 + 1。

---

### 4.2 Passed / Failed / XFail Cases

**推荐撰写内容：**

| Result Type | Count | Explanation |
|---|---:|---|
| Passed | 58 | All automated pytest items passed. |
| Failed | 0 | No failing test remained after debugging and stabilization. |
| Skipped | 0 | No optimized test case was skipped. |
| XFailed | 0 | No expected failure remained in the final run. |
| XPassed | 0 | No unexpected pass occurred. |

The final execution result shows that all optimized Todo Item Management test cases were successfully mapped and executed through Selenium + pytest.

**中文说明：**  
这一节要强调最终没有 xfail。之前脚本中可能有 KNOWN_DEFECT 标记，但最终结果是 58 passed，没有 xfailed。

---

### 4.3 Defect or Deviation Analysis

**推荐撰写内容：**

During debugging, several failures were initially observed, including edit-empty-title instability, whitespace-only input behavior, toggle-all on empty list, and clear-completed cleanup issues. Further analysis showed that the main remaining issue was not a product defect, but test isolation and UI interaction stability.

The edit-empty-title behavior was manually verified: when a Todo title is cleared and saved as empty, the item disappears as expected. Therefore, the earlier failure was caused by unstable Selenium editing behavior rather than a product defect. The script was improved by using double click, waiting for the editable input, selecting all text, clearing the field, and pressing Enter.

The toggle-all empty-list and invalid-control cases were clarified as safe-handling scenarios. In an empty list, the toggle-all control may not be present, and the expected behavior is that the application remains usable and no Todo item is created accidentally.

The clear-completed functionality was also tested independently. Earlier cleanup failures occurred because clear-completed was temporarily used as a global cleanup helper, where the previous UI state was uncertain. In the final script, setup cleanup deletes visible items one by one, while clear-completed itself is still tested through dedicated scenarios.

**中文说明：**  
这一节要区分产品缺陷和测试脚本/隔离问题。不要把之前的调试失败写成产品 bug。

---

### 4.4 Coverage Effectiveness After Execution

**推荐撰写内容：**

The final execution provides evidence that the optimized test suite was not only designed but also executable. The Selenium + pytest script maps all 57 optimized AutoTestDesign test cases to executable UI scenarios and adds one guardrail test to verify mapping completeness.

The execution covers the major Todo Item behaviors:

| Behavior Area | Execution Evidence |
|---|---|
| Add item | Valid item and whitespace-only invalid input are tested. |
| Toggle completed | Single toggle, repeated toggle, and active/completed transitions are tested. |
| Edit item | Non-empty edit and empty-title delete behavior are tested. |
| Delete item | Single delete and already-deleted safe handling are tested. |
| Toggle all | All-active, all-completed, mixed-state, and empty-list cases are tested. |
| Filter | All, Active, Completed, and invalid filter cases are tested. |
| Clear completed | Mixed active/completed, all-completed, and none-completed cases are tested. |
| State transition | Optimized transition sequence from TR-001 to TR-011 is represented. |

Therefore, the test execution demonstrates that the optimized suite is effective for validating the selected Todo Item Management feature at the UI level.

**中文说明：**  
这一节不要只写“全部通过”，还要解释“通过说明了什么”。建议用行为覆盖表格。

---

### 4.5 Improvement Suggestions

**推荐撰写内容：**

Although the final automation run passed, the following improvements are recommended:

1. **Improve backend test reset API**  
   Provide a list-scoped cleanup endpoint so that tests can reset the exact Todo list used by the UI without relying on UI fallback cleanup.

2. **Add CI integration**  
   Run the Selenium + pytest suite automatically in a CI pipeline to detect regressions after code changes.

3. **Add browser matrix execution**  
   Execute the suite in Chrome, Edge, and Firefox to improve cross-browser confidence.

4. **Add code coverage or UI coverage measurement**  
   Combine functional test results with code coverage or route coverage to provide stronger execution evidence.

5. **Extend non-functional tests**  
   Add usability, performance, persistence, and error-recovery tests for broader quality evaluation.

6. **Improve AutoTestDesign abstraction handling**  
   For abstract generated scenarios such as “list unavailable” or “database failure,” allow the tool to generate clearer executable preconditions or mock-based execution instructions.

**中文说明：**  
这一节要体现 in-depth analysis。不要只写“以后继续优化”，要具体写可执行改进方向。

---

## 5. Conclusion

**推荐撰写内容：**

This document presented the detailed test design and execution work for the Todo Item Management feature of SimpleTodoList. The AutoTestDesign tool generated structured requirements, risk analysis, coverage items, test strategies, test suites, candidate test cases, optimized test cases, and traceability artifacts. The design applied multiple black-box techniques, including Equivalence Partitioning, Boundary Value Analysis, and Decision Table Testing. It also applied State Transition Testing as a structural modeling technique for Todo item lifecycle behavior.

The optimized suite contains 57 test cases, and the final Selenium + pytest implementation maps all 57 optimized cases to executable UI scenarios. Together with one guardrail test, pytest collected 58 items and all 58 passed successfully. This demonstrates that the selected feature has strong design-level coverage and executable automation evidence.

The main limitation is that some abstract abnormal conditions are approximated through UI-level executable scenarios rather than simulated at a lower system level. Future work should improve list-scoped backend cleanup, add CI and cross-browser execution, and extend non-functional testing.

**中文说明：**  
结论建议分三层：设计层覆盖、自动化执行结果、限制与后续改进。

---

## Appendix A. Main Artifacts

**推荐撰写内容：**

| Artifact | Description |
|---|---|
| `todoitem_requirements_structured.csv` | Structured Todo Item requirements. |
| `todoitem_risk_analysis.csv` | Risk analysis for Todo Item requirements. |
| `todoitem_coverage_items.csv` | Coverage items identified from requirements and risks. |
| `todoitem_test_strategies.csv` | Test design techniques selected for coverage items. |
| `todoitem_test_suites.csv` | Test suites grouped by coverage and technique. |
| `todoitem_test_cases.csv` | Full generated candidate test cases. |
| `todoitem_optimized_test_suite.csv` | Optimized executable test suite. |
| `todoitem_traceability_matrix.csv` | Traceability matrix from requirements to test cases. |
| `todoitem_state_transitions.csv` | State transition model and transition sequence. |
| `todoitem_test_suite_artifacts.json` | Consolidated JSON artifact. |
| `todoitem_test_design_artifacts.xlsx` | Consolidated Excel artifact. |
| `test_todoitem_ui_selenium_full.py` | Selenium + pytest automation script. |
| `selenium_pytest_debug_summary.md` | Debugging and final execution summary. |

---

## Appendix B. Example Test Case Mapping

**推荐撰写内容：**

| Test Case ID | Suite ID | Coverage ID | Scenario Function | Purpose |
|---|---|---|---|---|
| TC-066 | TS-009 | COV-STATE-TR-001 | `s_add_valid` | Add valid Todo item. |
| TC-075 | TS-009 | COV-STATE-TR-002 | `s_add_whitespace_ignored` | Verify whitespace-only input is ignored. |
| TC-067 | TS-009 | COV-STATE-TR-003 | `s_toggle_completed_once` | Toggle item from active to completed. |
| TC-068 | TS-009 | COV-STATE-TR-004 | `s_edit_non_empty` | Edit item title to a valid non-empty title. |
| TC-069 | TS-009 | COV-STATE-TR-005 | `s_edit_empty_deletes` | Verify empty edited title deletes item. |
| TC-070 | TS-009 | COV-STATE-TR-006 | `s_delete_single_item` | Delete one Todo item. |
| TC-071 | TS-009 | COV-STATE-TR-007 | `s_toggle_all_to_completed` | Toggle all items to completed. |
| TC-076 | TS-009 | COV-STATE-TR-011 | `s_clear_completed_all_completed_empty` | Clear completed items from all-completed state. |

---

## Appendix C. Execution Command and Output

**推荐撰写内容：**

Command:

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py
```

Output:

```text
=========================== test session starts ============================
platform win32 -- Python 3.11.15, pytest-9.0.2, pluggy-1.6.0
collected 58 items

Assignment2\tests\test_todoitem_ui_selenium_full.py ................. [ 29%]
.........................................                             [100%]

====================== 58 passed in 117.05s (0:01:57) ======================
```

---

## Appendix D. 推荐放入报告的核心英文段落

The Selenium + pytest script maps all 57 optimized AutoTestDesign test cases for the Todo Item Management feature, plus one guardrail test that verifies mapping completeness. During debugging, the main issue was not the functional behavior itself, but test isolation: the backend reset helper did not reliably clear the current list-scoped Todo data shown in the UI. To ensure each case starts from a deterministic empty list, the final script performs UI-level cleanup before each test by deleting any visible Todo items. This cleanup is treated only as test setup and is not used as a test oracle.

After improving test isolation and stabilizing UI actions such as edit, toggle-all, and clear-completed flows, the final execution collected 58 pytest items and all 58 passed successfully. This demonstrates that the automated implementation fully executes the optimized test suite mapping for the selected Todo Item Management feature.

---

## Appendix E. 推荐放入报告的核心中文理解

最终 Selenium + pytest 脚本映射了 Todo Item Management 的 57 个 AutoTestDesign 优化测试用例，并额外包含 1 个用于检查映射完整性的 guardrail 测试。调试过程中发现，主要问题不是功能行为本身，而是测试隔离不稳定：后端 `reset_todos()` 没有可靠清空当前页面 `test-list` 中实际显示的 Todo 数据。因此最终脚本在每个测试开始前通过 UI 删除当前可见 Todo items，从而保证每个测试都从确定的空列表状态开始。该 UI 清理只作为测试环境准备步骤，不作为被测功能是否通过的判定依据。

在改进测试隔离并稳定 edit、toggle-all、clear-completed 等 UI 操作后，最终执行共收集 58 个 pytest items，并且 58 个全部通过。这说明自动化实现已经完整执行了选定 Todo Item Management feature 的 optimized suite 映射。
