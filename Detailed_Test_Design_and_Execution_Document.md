# Detailed Test Design and Execution Document

Content

# 1. Introduction ..............................................................................................................4

## 1.1 Purpose .................................................................................................................4

## 1.2 Scope ....................................................................................................................4

# 2. Detailed Test Case Design ....................................................................................... 5

## 2.1 Selected Feature / Module ................................................................................... 5

## 2.2 Test Design Workflow .........................................................................................5

## 2.3 Requirement and Risk Basis ................................................................................ 6

## 2.4 Coverage Item Identification ............................................................................... 7

## 2.5 Coverage Strategy and Test Design Techniques ................................................. 8

## 2.6 Test Suites and Cases ...........................................................................................9

## 2.7 Optimized Test Suite and Coverage Explanation .............................................. 10

## 2.8 Traceability ........................................................................................................ 10

## 2.9 Human Review and Editable Design Artifacts .................................................. 11

# 3. Test Tool Implementation ......................................................................................12

## 3.1 Framework Selection ......................................................................................... 12

## 3.2 Automation Target ............................................................................................. 12

## 3.3 Script Structure .................................................................................................. 13

## 3.4 Mapping from Optimized Test Cases to Automation ........................................ 14

## 3.5 Test Independence and Data Reset .................................................................... 14

## 3.6 Executability and Limitations ............................................................................ 14

# 4. Test Result Analysis .............................................................................................. 16

## 4.1 Execution Summary ...........................................................................................16

## 4.2 Passed / Failed / XFail Cases ............................................................................. 16

## 4.3 Defect or Deviation Analysis .............................................................................17

## 4.4 Coverage Effectiveness After Execution ........................................................... 18

## 4.5 Improvement Suggestions ..................................................................................19

# 5. Conclusion ............................................................................................................. 19

Appendix....................................................................................................................21

## Appendix A. Main Artifacts .................................................................................... 21

## Appendix B. Example Test Case Mapping ..............................................................21

# 1. Introduction

## 1.1 Purpose

This document presents the detailed test design and execution work for the selected Todo Item Management feature/module of the SimpleTodoList target application. The purpose of this document is to demonstrate how the developed AutoTestDesign tool was used to support systematic test design, including requirement structuring, risk analysis, coverage item identification, test strategy selection, test case generation, optimized test suite construction, and traceability management. In this document, Todo Item Management is treated as a major functional module of SimpleTodoList. It contains a coherent group of user-facing features, including adding a Todo item, toggling completion status, editing item text, deleting an item, toggling all items, filtering items by status, and clearing completed items. These behaviors represent the core workflow of the target application and provide sufficient complexity for applying multiple black-box testing techniques and structural testing techniques. The document also explains how the generated detailed test cases were mapped to executable automated tests using pytest and Selenium WebDriver. The final goal is to show not only the generated test cases, but also the reasoning behind the coverage strategy, the relationship between requirements and test cases, and the execution evidence obtained from the automated test run.

## 1.2 Scope

The scope of this detailed test design and execution document is limited to the Todo Item Management module of the SimpleTodoList application. The selected module focuses on the lifecycle and state changes of Todo items from the user interface perspective. The following functional requirements are covered in this document:

| requirement_id | requirement_text |
| --- | --- |
| REQ-1 | Users shall be able to add a new Todo item to a specified List; input consisting only of whitespace shall not create an item |
| REQ-2 | Users shall be able to mark or unmark a Todo item as completed |
| REQ-3 | Users shall be able to edit the text of a Todo item by double-clicking; saving an empty title shall delete the item |
| REQ-4 | Users shall be able to delete a single Todo item |
| REQ-5 | Users shall be able to toggle all Todo items to completed or active using a single control |
| REQ-6 | Users shall be able to filter Todo items by All Active or Completed status |
| REQ-7 | Users shall be able to clear all completed Todo items at once |

*Table 1 Requirements*

The test design covers functional behavior, input validation, boundary-related cases, condition-based behavior, selected abnormal UI states, and state transitions of Todo items. The generated test cases apply multiple black-box techniques, including Equivalence Partitioning, Boundary Value Analysis, and Decision Table Testing. In addition, State Transition Testing is used to model Todo item state changes. This document does not aim to provide a full-system test report for the entire SimpleTodoList application. Other modules, such as Admin authentication, Todo List management, backend API security, cross-module persistence risks, and non- functional testing such as performance or security testing, are outside the scope of this detailed test design document. Those areas are addressed at a higher level in the overall risk analysis report or test plan.

# 2. Detailed Test Case Design

## 2.1 Selected Feature / Module

The detailed test design selects Todo Item Management because it is one of the three major functional modules identified in the project risk analysis. This module covers the core user-facing Todo item operations, including create, update, delete, status switching, and filtering. Therefore, it is suitable for demonstrating requirement structuring, risk-based test design, black-box techniques, and state-based testing.

## 2.2 Test Design Workflow

The test design followed a step-by-step workflow supported by AutoTestDesign and reviewed by the human tester. The workflow started with the structured requirements of the selected module and ended with executable Selenium-based automated tests. Throughout this workflow, AutoTestDesign combined deterministic local generation with optional LLM-assisted review and improvement. In general, each major stage first produced a reproducible baseline artifact through local logic, and selected stages could then be refined, supplemented, or reviewed with LLM support. First, the Todo Item Management requirements were structured into fields such as input fields, conditions, actions, data ranges, and expected results. Second, risk analysis was performed to assign risk levels and identify which requirements should receive stronger test coverage. Third, baseline coverage items were generated from the structured requirements and risks. After coverage item identification, AutoTestDesign selected suitable test design techniques for different coverage types. Equivalence Partitioning was used for valid and invalid input classes and core functional scenarios. Boundary Value Analysis was used for empty, whitespace-only, and status boundary cases. Decision Table Testing was used where behavior depended on combinations of conditions. State Transition Testing was used to model Todo item lifecycle changes, such as active to completed, completed to active, view mode to edit mode, and existing item to deleted item. AutoTestDesign then grouped the selected coverage items and test strategies into test suites. Based on these suites, it generated detailed test cases with concrete steps, test data, and expected results. Optional LLM-assisted enhancement could be applied at multiple stages, including requirement structuring, risk analysis, coverage improvement, strategy review, suite description refinement, missing test case addition, state model improvement, and optimized suite review. After generation, the test cases were optimized to reduce redundant or highly similar cases while preserving the main requirement, risk, coverage, and technique coverage. The optimized cases were then reviewed and mapped to executable Selenium + pytest scenarios. The detailed outputs produced during this workflow, including the requirement list, risk analysis records, coverage items, test strategies, test suites, test cases, optimized suite, and traceability matrix, are maintained in the supporting workbook todoitem_test_design_artifacts.xlsx submitted together with this report.

## 2.3 Requirement and Risk Basis

The detailed test design for Todo Item Management is based on the structured requirement and risk artifacts generated by AutoTestDesign. The selected module was first decomposed into 7 functional requirements, covering the main user behaviors of Todo item creation, status switching, editing, deletion, bulk operation, filtering, and clearing completed items. Each requirement was associated with at least one product risk. The risk analysis considered both the likelihood of failure and the potential impact on the user-facing behavior of the Todo application. For example, whitespace-only input validation, double-click editing, filtering logic, bulk toggle behavior, and clear-completed behavior were treated as higher-priority areas because they involve input validation, state changes, or operations affecting multiple Todo items. The requirement and risk basis can be summarized as follows: the selected module contains 7 structured requirements, 7 requirement-level risks, and a complete mapping from requirements to risk-based coverage items. This provides the foundation for selecting test design techniques and generating test cases in the later steps.

## 2.4 Coverage Item Identification

Coverage item identification serves as the bridge between high-level requirements and concrete test cases. In this project, the local baseline coverage set was derived from structured requirement elements, including core functional behavior, input fields, decision conditions, and data-range or boundary concerns. In addition, an LLM- assisted coverage improvement step was used to automatically supplement possible missing coverage, especially for error-oriented and state-transition-oriented situations that were not fully captured by the deterministic baseline. For the Todo Item Management module, the final coverage set can be grouped into the following categories:

- Functional coverage items, such as adding a Todo item, editing a title, deleting an
item, toggling all items, applying a filter, and clearing completed items.

- Input coverage items, such as Todo text, title, item reference, control input,
completed-item input, and filter value.

- Boundary-related coverage items, such as whitespace-only input, empty title,
completed status, and filter states including All, Active, and Completed.

- Condition coverage items, such as whitespace input, double-click editing, saving an
empty title, general user actions, and filter selection.

- LLM-added error-oriented coverage items, such as clearing completed items when
no items are completed, deleting an already deleted item, editing an item that becomes unavailable, using an invalid filter value, or adding an item when the list is unavailable.

- LLM-added state-transition coverage items, such as repeated completion toggling
and toggle-all behavior when some items have already changed state. Representative examples include baseline items such as COV-001 for add-item behavior, COV-004 for the whitespace-only boundary, and COV-012 for double-click editing conditions, as well as LLM-added items such as COV-AI-002 for repeated completion toggling and COV-AI-007 for clearing completed items when no items are completed. The final design contains 36 coverage items for the selected module. This final coverage set provides a more detailed testing basis than the original 7 requirements because it decomposes high-level user requirements into smaller and more testable coverage obligations.

## 2.5 Coverage Strategy and Test Design Techniques

The coverage strategy was selected according to the nature of each coverage item. Since the assignment requires the use of multiple black-box techniques and white-box or structural techniques, the design combines specification-based testing with state- based structural modeling. This combination of techniques helps ensure that the test suite is not only broad in requirement coverage, but also systematic in test design reasoning. The selected techniques cover normal flows, invalid inputs, boundary conditions, condition combinations, and state-dependent behavior.

### 2.5.1 Black-box Techniques

Three main black-box techniques were applied in the test design. Equivalence Partitioning was used to divide the input and behavior space into representative classes. For example, Todo item text can be divided into valid non- empty text and invalid whitespace-only input. Filter values can be divided into valid filters such as All, Active, and Completed. This technique reduces redundant tests while preserving meaningful input coverage. Boundary Value Analysis was used for cases where behavior changes at or near a boundary. In this module, empty input, whitespace-only input, and empty edited title are important boundary-related cases. For example, saving a non-empty title should update the item, while saving an empty title should delete the item. Decision Table Testing was used for behavior that depends on combinations of conditions. For example, whether an item is visible after filtering depends on both the selected filter and the completed status of the item. Similarly, clearing completed items depends on whether completed items exist in the current list. Decision tables help make these combinations explicit and reduce the chance of missing condition interactions.

### 2.5.2 White-box / Structural Modeling Technique

State Transition Testing was used as the structural testing technique in this detailed design. Although automated execution is performed through the user interface, the state model describes the internal behavior of Todo items from the perspective of observable states and transitions. The generated state model represents the observable list-level states of the Todo Item Management module rather than the internal state of a single Todo item. This is appropriate for UI-level testing because many Todo item operations, such as filtering, toggle-all, and clear-completed, affect the visible state of the whole list.

![Diagram 1 List-level State Transition Model for Todo Item Management](assets/diagram_1_state_transition_model.jpeg)

*Diagram 1 List-level State Transition Model for Todo Item Management*

The main Todo item states include active, completed, editing, and deleted. The transitions include creating a new active item, toggling an active item to completed, toggling a completed item back to active, entering edit mode by double-clicking, saving a new non-empty title, saving an empty title that deletes the item, deleting an item through the delete control, and clearing completed items. This state-based model is useful because many Todo behaviors are not isolated one- step actions. They depend on the previous state of the item and the sequence of user operations. For example, a clear-completed operation only affects completed items, while filtering depends on the relationship between the selected filter and the current item state. Therefore, State Transition Testing complements the black-box techniques by covering behavior across sequences of actions.

## 2.6 Test Suites and Cases

In AutoTestDesign, test suites are generated before detailed test cases. Instead of producing a flat collection of isolated test cases directly from the requirements, the tool first organizes the identified coverage items and selected test design techniques into structured test suites. These suites then serve as the basis for generating detailed candidate test cases with concrete steps, test data, and expected results. This suite-driven design provides a clearer bridge from requirement-level coverage objectives to executable test cases. Related coverage items are grouped according to their testing concern and technique, which makes the generated artifacts easier to review, optimize, and trace. The suite design includes boundary-related suites, decision rule suites, partition suites, state behavior suites, and a dedicated state transition model suite. These suites reflect different testing concerns, including normal functional behavior, input partitions, boundary conditions, condition-based logic, abnormal or state-dependent behavior, and explicit state-transition coverage. In the final design, the 9 suites consist of 1 Boundary Suite, 1 Decision Rule Suite, 3 Partition Suites, 3 State Behavior Suites, and 1 dedicated State Transition Model Suite. Based on these suites, AutoTestDesign generated 78 candidate test cases, which were later optimized into a final execution subset of 57 test cases. Therefore, the suite structure is not only a reporting convenience, but also the intermediate design layer that drives detailed test case generation and later optimization. The State Transition Model Suite is especially important because it demonstrates the use of structural modeling in addition to black-box test design. It helps ensure that state-based behavior, such as completion toggling, editing, deletion, and clear- completed behavior, is preserved in the final test design.

## 2.7 Optimized Test Suite and Coverage Explanation

After the initial test generation, AutoTestDesign optimized the test suite to reduce redundancy while preserving the major coverage goals. The optimized suite contains 57 test cases. The optimization process did not simply remove test cases by quantity. Instead, it combined deterministic local rules and optional LLM-assisted semantic review to preserve requirement-related coverage, risk-sensitive cases, important coverage items, and high-value boundary, invalid, error, and state-transition scenarios while reducing redundant or highly similar cases. In addition to reducing redundant cases, the suite also supports risk-based prioritization by retaining risk-level information for the generated test cases. Testers can use this information to sort and review test cases according to risk level. The optimized suite still preserves coverage of all 7 requirements and all 9 test suites. It also preserves the use of multiple test design techniques, including Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, and State Transition Testing. Therefore, the optimized suite is more efficient than the original generated suite while still remaining suitable for detailed test execution.

## 2.8 Traceability

Traceability was maintained throughout the test design process. Each generated test case can be traced back to its related requirement, risk, coverage item, test strategy, and test suite. This traceability is important because it shows that the test cases were not created randomly; they were derived from explicit testing objectives. The traceability chain used in this project can be described as: Requirement → Risk → Coverage Item → Test Strategy → Test Suite → Test Case → Automated Scenario For example, the requirement for adding a Todo item is connected to the risk of missing input validation. This risk leads to coverage items for valid input, whitespace- only input, and boundary-related input behavior. These coverage items are then linked to techniques such as Equivalence Partitioning and Boundary Value Analysis. The generated test cases are finally mapped to Selenium scenarios that verify whether a valid item is created and whether whitespace-only input is rejected. The same traceability pattern is applied to editing, deleting, toggling, filtering, and clearing completed items. This supports both coverage evaluation and future maintenance, because if a requirement changes, the related coverage items and test cases can be identified quickly.

## 2.9 Human Review and Editable Design Artifacts

AutoTestDesign does not treat the generated test design as a fixed and unchangeable result. The generated requirements, risks, coverage items, test strategies, test suites, and test cases are displayed as editable structured artifacts, so that the tester can inspect, revise, add, or remove design items when necessary. In this project, human involvement mainly focused on confirming the selected module scope, checking whether the generated artifacts matched the requirements of Todo Item Management, understanding the optimized test suite, and mapping the optimized cases to executable Selenium + pytest scenarios. This interactive and editable workflow helps ensure that the final test design is not only automatically generated, but also understandable, reviewable, and maintainable by the tester.

# 3. Test Tool Implementation

## 3.1 Framework Selection

This project selected pytest + Selenium WebDriver as the automation framework for executing the detailed test cases of the Todo Item Management module. This choice matches the selected module because most Todo item behaviors are UI-driven, including adding items, toggling completion status, editing text, deleting items, filtering by status, and clearing completed items. Selenium WebDriver is suitable because it can simulate real user operations in a browser, such as typing, clicking, double-clicking, and verifying visible UI changes. pytest was selected as the execution engine because it supports fixtures, parameterized tests, clear assertions, and readable execution results. These features make it suitable for mapping the optimized AutoTestDesign test cases to executable automated scenarios. In this document, Selenium is used for browser-level interaction across functional behavior suites, input validation suites, boundary-related suites, condition- or decision-based suites, error-oriented suites, and the state transition suite, while pytest manages test setup, cleanup, parameterization, execution, and result reporting.

## 3.2 Automation Target

The automation target is the Todo Item Management module of SimpleTodoList. The automated tests execute the optimized test cases generated by AutoTestDesign through the browser UI. The test code directly uses the backend API only for setup and cleanup; while the actual feature verification is performed through Selenium WebDriver in the browser UI.

| Item | Description |
| --- | --- |
| Target application | SimpleTodoList |
| Selected feature/module | Todo Item Management |
| Test design tool | AutoTestDesign |
| Automation framework | pytest + Selenium WebDriver |
| Frontend URL | http://127.0.0.1:8000/todo.html#/&test-list |
| Backend API URL | http://127.0.0.1:5000/api |
| Default browser | Chrome |
| Main automation script | Assignment2/tests/test_todoitem_ui_selenium_full.py |
| Main test design source | Exported structured test artifacts generated by AutoTestDesign |

*Table 2 Target Description*

## 3.3 Script Structure

The automation script is organized into several logical parts.

# 1. Configuration

This part defines the frontend URL, backend API URL, browser type, and headless execution option. These settings make the script easier to run in different local environments.

# 2. Cleanup helpers

These helpers reset Todo data before each test by combining backend API requests with UI-level cleanup operations when necessary. They are used only for test setup and are not used as the main feature verification method.

# 3. pytest fixtures

The fixtures manage the browser lifecycle and test state. The driver fixture creates and closes the browser, the clean_state fixture resets the Todo list before each test case, and the page fixture provides access to the Page Object.

# 4. Page Object

The Page Object encapsulates common UI operations, such as adding an item, editing a title, toggling completion status, deleting an item, filtering by status, clearing completed items, and checking visible Todo items.

# 5. Scenario mapping and parameterized execution

Reusable scenario functions are mapped to the optimized AutoTestDesign test cases. pytest parameterization is then used to execute these mapped cases systematically while preserving the original test case IDs, suite IDs, and coverage IDs.

# 6. Guardrail completeness check

In addition to the parameterized execution of the 57 optimized test cases, the script includes one small guardrail test to verify that the mapping table still contains all expected optimized cases.

## 3.4 Mapping from Optimized Test Cases to Automation

The automation script uses a structured mapping to connect each optimized AutoTestDesign test case to an executable Selenium scenario. Each mapping keeps the original test case information, including the test case ID, suite ID, coverage ID, and the corresponding scenario function. This preserves traceability from the generated test design artifacts to the automated execution. Some optimized test cases share the same executable scenario because they have the same observable UI behavior, although they may come from different coverage items or test suites. For example, several cases related to safe handling of empty or unavailable controls can be executed through the same UI-level scenario while still keeping their original IDs and coverage references. The full mapping is maintained in the automation script rather than repeated in the report. This avoids duplicating a long table while still preserving traceability. The optimized suite itself contains 57 mapped test cases, and the script adds one separate guardrail test to verify mapping completeness.

## 3.5 Test Independence and Data Reset

Each automated test case must start from a known and stable state. During debugging, it was found that the backend reset helper and the UI page did not always operate on the same visible list state during automation, which could cause state pollution between test cases. To solve this problem, the final script combines backend cleanup with UI-level cleanup. Before each test case, the script first attempts to reset Todo data through the backend API. It then opens the Todo page, removes any remaining visible Todo items through the UI if necessary, reloads the page, and verifies that the visible Todo count is zero. The UI-level cleanup is only a setup step for test isolation. It is not used as the test oracle for the feature under test. Each actual test case still creates its own test data, performs the target action, and verifies the expected result independently.

## 3.6 Executability and Limitations

Most optimized test cases can be executed directly through the browser UI. Typical examples include adding a Todo item, rejecting whitespace-only input, toggling completion status, editing a title, deleting an item, filtering by status, toggling all items, and clearing completed items. However, a few generated cases describe abstract or abnormal conditions that are not directly exposed as simple UI operations. For these cases, automation uses practical UI-level approximations. For example, an invalid filter value can be tested by navigating to an invalid filter state, and toggle-all behavior on an empty list can be tested by verifying that the control is absent or unavailable and that the application remains usable. This approach keeps the intent of the original coverage items while making the cases executable in the current UI. The main limitation is that UI automation cannot fully simulate deeper internal failures, such as database-level faults, server crashes, or network interruption. These risks would require additional API-level, integration-level, or fault-injection tests in future work.

# 4. Test Result Analysis

## 4.1 Execution Summary

The final automated test execution was performed using the following command:

```powershell
pytest Assignment2\tests\test_todoitem_ui_selenium_full.py
```

Final result:

![Diagram 2 Test Result](assets/diagram_2_test_result.jpeg)

*Diagram 2 Test Result*

The 58 pytest items consist of:

- 57 optimized AutoTestDesign test cases: These are the mapped executable
scenarios from the optimized test suite generated by AutoTestDesign.

- 1 coverage-completeness guardrail test: This additional test verifies that the
automation mapping contains all 57 optimized test cases, ensuring no cases are inadvertently missing from the executable suite.

## 4.2 Passed / Failed / XFail Cases

| Result Type | Count | Explanation |
| --- | --- | --- |
| Passed | 58 | All automated pytest items passed |
| Failed | 0 | No failing test remained after debugging and stabilization |
| Skipped | 0 | No optimized test case was skipped |
| XFailed | 0 | No expected failure remained in the final run |
| XPassed | 0 | No unexpected pass occurred |

*Table 3 Passed / Failed / XFail Cases*

The final execution result shows that all optimized Todo Item Management test cases were successfully mapped and executed through Selenium + pytest. All 58 pytest items passed without any failures, skips, or expected failures.

## 4.3 Defect or Deviation Analysis

During debugging, several failures were initially observed, including edit-empty-title instability, whitespace-only input behavior, toggle-all on empty list, and clear- completed cleanup issues. Further analysis showed that the main remaining issue was not a product defect, but test isolation and UI interaction stability. Edit-empty-title behavior: Initially marked as potentially problematic, manual verification confirmed that when a Todo title is cleared and saved as empty, the item correctly disappears. The earlier failure was caused by unstable Selenium editing behavior rather than a product defect. The script was improved by:

- Using double-click to enter edit mode
- Waiting for the editable input to become interactable
- Using Ctrl+A + Backspace to reliably clear the field
- Pressing Enter to save
- Adding retry logic to reduce element not interactable or stale element errors
Toggle-all empty-list handling: The toggle-all control may not be present or may be disabled when the list is empty. This is expected behavior-the control should not be interactable in this state. The test verifies that attempting to toggle-all on an empty list is handled safely, with the application remaining usable and no items being created. Clear-completed functionality: Earlier cleanup failures occurred because clear- completed was temporarily used as a global cleanup helper, where the previous UI state was uncertain. In the final script:

- Setup cleanup deletes visible items one by one through the .destroy control
- Clear-completed functionality itself is tested through dedicated scenarios
- Three distinct scenarios verify: mixed active/completed items, all-completed items,
and no-completed-items cases State pollution issue: A key finding during debugging was that reset_todos() API call alone did not reliably clear the current list-scoped Todo data shown in the UI. This was resolved by combining backend API cleanup with UI-level cleanup to ensure test isolation.

## 4.4 Coverage Effectiveness After Execution

The final execution provides evidence that the optimized test suite was not only designed but also executable. The Selenium + pytest script maps all 57 optimized AutoTestDesign test cases to executable UI scenarios and adds one guardrail test to verify mapping completeness. The execution covers the major Todo Item behaviors:

| Behavior Area | Execution Evidence |
| --- | --- |
| Add item | Valid item creation and whitespace-only input rejection are tested |
| Toggle completed | Single toggle, repeated toggle, and active/completed state transitions are tested |
| Edit item | Non-empty title edit and empty-title delete behavior are tested |
| Delete item | Single item deletion and safe handling of already-deleted items are tested |
| Toggle all | All-active, all-completed, mixed-state, and empty-list cases are tested |
| Filter | All, Active, Completed, and invalid filter state handling are tested |
| Clear completed | Mixed active/completed, all-completed, and none-completed cases are tested |
| State transition | Optimized transition sequence from TR-001 to TR-011 is represented |

*Table 4 Execution Evidence for Todo Item Management Coverage*

The coverage effectiveness can be summarized as:

- Design-level coverage: Complete for REQ-1 to REQ-7, all 36 coverage items, and
all 9 test suites

- Technique coverage: Equivalence Partitioning, Boundary Value Analysis, Decision
*Table Testing, and State Transition Testing are all applied*

- Automation coverage: Full mapping of all 57 optimized test cases to executable
Selenium scenarios Therefore, the test execution demonstrates that the optimized suite is effective for validating the selected Todo Item Management feature at the UI level.

## 4.5 Improvement Suggestions

Although the final automation run passed, the following improvements are recommended:

# 1. Improve backend test reset API

Provide a list-scoped cleanup endpoint so that tests can reset the exact Todo list used by the UI without relying on UI fallback cleanup. This would eliminate the need for UI-level cleanup and improve test isolation reliability.

# 2. Add CI integration

Run the Selenium + pytest suite automatically in a CI pipeline to detect regressions after code changes. This would ensure continuous validation of the Todo Item Management feature.

# 3. Add browser matrix execution

Execute the suite in Chrome, Edge, and Firefox to improve cross-browser confidence. The current implementation supports multiple browsers through environment variables but has been primarily tested on Chrome.

# 4. Add code coverage or UI coverage measurement

Combine functional test results with code coverage or route coverage to provide stronger execution evidence. This would help identify potential gaps between test design and actual code execution.

# 5. Extend non-functional tests

Add usability, performance, persistence, and error-recovery tests for broader quality evaluation. The current focus is on functional behavior; non-functional aspects would provide more comprehensive quality assessment.

# 6. Improve AutoTestDesign abstraction handling

For abstract generated scenarios such as "list unavailable" or "database failure," allow the tool to generate clearer executable preconditions or mock-based execution instructions. This would improve the executability of edge-case scenarios that are difficult to trigger through UI alone.

# 7. Enhance test reporting

Integrate test reporting tools like Allure or pytest-html to generate more comprehensive and visually appealing reports that include screenshots, execution timelines, and traceability information.

# 5. Conclusion

This document presented the detailed test design and execution work for the selected Todo Item Management module of the SimpleTodoList target application. The selected module was treated as a major functional module because it covers the core Todo item workflow, including adding, editing, deleting, toggling, filtering, bulk toggling, and clearing completed items. Using AutoTestDesign, the module was decomposed into 7 structured requirements and 7 requirement-level risks. Based on these inputs, the tool generated 36 coverage items, selected appropriate test design techniques, organized the coverage items into 9 test suites, and generated 78 candidate test cases. The suite was then optimized into 57 test cases while preserving requirement coverage, risk-related coverage, test suite coverage, and technique diversity. The detailed test design applied multiple black-box testing techniques, including Equivalence Partitioning, Boundary Value Analysis, and Decision Table Testing. In addition, State Transition Testing was used as the structural modeling technique to cover state-dependent Todo item behavior, such as completion toggling, editing, deletion, and clear-completed behavior. For test execution, the optimized suite was mapped to executable Selenium + pytest scenarios. The final automation run collected 58 pytest items: 57 optimized AutoTestDesign test cases and 1 guardrail completeness test. All 58 items passed, with no failed, skipped, xfailed, or xpassed cases. This result shows that the optimized test suite was not only designed but also executable at the UI level. Overall, the final test design achieved complete coverage of the selected 7 requirements, all 36 coverage items, and all 9 test suites. The automation also preserved traceability from requirements, risks, coverage items, strategies, suites, and test cases to executable scenarios. However, the current work mainly focuses on UI- level functional validation. As possible future extensions, the testing scope could be expanded to API-level, integration-level, fault-injection, performance, or usability testing, in order to explore deeper internal failure modes such as database faults, server crashes, network interruption, and broader non-functional quality attributes.

# Appendix

## Appendix A. Main Artifacts

The main input and output artifacts used in this detailed test design and execution work are listed below. Most structured test design data are maintained in the supporting Excel workbook todoitem_test_design_artifacts.xlsx to avoid duplicating large tables in the report body.

| Artifact | Description |
| --- | --- |
| todoitem_test_design_artifacts.xlsx | Supporting workbook containing the structured requirements, risk analysis, coverage items, test strategies, test suites, generated test cases, optimized test suite, state transitions, and traceability matrix. |
| todoitem_test_suite_artifacts.json | Consolidated JSON export of the Todo Item Management test design artifacts for tool-generated results and traceability records. |
| todoitem_requirements_structured.csv | Structured requirement list for the Todo Item Management feature, including parsed fields such as actions, conditions, inputs, and expected results. |
| todoitem_risk_analysis.csv | Risk analysis output linking requirements to identified risks, risk levels, and priorities. |
| todoitem_coverage_items.csv | Coverage item list derived from the structured requirements and risks. |
| todoitem_test_strategies.csv | Selected test design strategies and techniques mapped to the coverage items. |
| todoitem_test_suites.csv | Generated test suite definitions showing how related coverage items were grouped into executable suites. |
| todoitem_test_cases.csv | Full generated candidate test case set before optimization. |

*Table 5 Export Artifacts*

## Appendix B. Example Test Case Mapping

The full mapping from optimized test cases to Selenium scenarios is maintained in the automation script. The following examples illustrate how optimized AutoTestDesign test cases are connected to executable UI scenarios while preserving traceability information. Only test cases retained in the optimized suite are included in the final Selenium mapping. Earlier generated cases that were removed or merged during optimization are not listed in this appendix.

| Optimized Test Case | Suite ID | Coverage ID | Selenium Scenario | Purpose |
| --- | --- | --- | --- | --- |
| TC-001 | TS-001 | COV-004 | s_add_whitespace_ignored | Verifies that whitespace-only input does not create a Todo item. |
| TC-019 | TS-002 | COV-029 | s_clear_completed_keeps_active | Verifies that clear completed removes completed items and keeps active items. |
| TC-035 | TS-004 | COV-018 | s_toggle_all_to_completed | Verifies that toggle-all changes all visible Todo items to completed. |
| TC-045 | TS-005 | COV-010 | s_edit_non_empty | Verifies that an existing Todo item can be edited to a new non-empty title. |
| TC-058 | TS-006 | COV-012 | s_double_click_enters_edit_mode | Verifies that double-clicking a Todo item enters edit mode. |
| TC-066 | TS-009 | COV-STATE-TR-001 | s_add_valid | Verifies the state-transition case in which a valid Todo item is created from the empty-list state. |

*Table 6 Example Test Case Mapping to Selenium Scenarios*
