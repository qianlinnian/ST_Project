# Assignment2 Project Brief

`Assignment2` is an AI-assisted software test design tool built with Python and Streamlit. It supports a requirement-driven workflow for generating risk analysis, coverage items, test strategies, state transition models, high-level test suites, candidate test cases, optimized test suites, traceability matrices, and exportable project artifacts.

The demonstration target is `simpletodolist`, a lightweight Todo List web application. The tested feature area is Todo Item Management, including adding, editing, deleting, completing, filtering, clearing completed todos, and persistence behavior. The implementation is domain-neutral: requirements can be imported from CSV, plain text, or edited table input.

## Workflow

1. Import or edit requirements.
2. Structure requirements into input fields, data ranges, conditions, actions, and expected results.
3. Manually edit and save structured requirement fields when local or LLM extraction needs correction.
4. Analyze requirement risk and priority.
5. Generate coverage items and optionally improve missing coverage with LLM.
6. Select black-box or state-based test design strategies, with optional LLM review.
7. Generate the state transition model and optimized transition sequences.
8. Generate high-level test suites and optionally improve suite metadata with LLM.
9. Generate candidate test cases under those test suites.
10. Add missing test cases with LLM when useful.
11. Generate and optionally improve the optimized test suite.
12. Generate traceability matrix and export artifacts.

## Local Baseline and LLM Enhancement

The system intentionally separates deterministic local generation from optional LLM enhancement:

- Local baseline logic provides fast, repeatable, traceable outputs.
- LLM enhancement is used for review, missing item discovery, semantic improvement, and minimization.
- LLM output is merged by local code instead of blindly replacing core artifacts.
- Downstream artifacts are reset when upstream data is edited, preserving consistency.

This design makes the workflow explainable for coursework: local rules guarantee a reproducible baseline, while LLM calls improve quality where semantic judgement is useful.

## LLM Performance Design

All major LLM features use shared performance settings from the sidebar:

- `LLM batch size`: controls how many requirements, coverage items, or test cases are sent in one LLM batch.
- `LLM concurrency`: controls how many LLM batches can run in parallel.

LLM requests use a shared client with session reuse and connection pooling. DeepSeek calls run with deterministic settings, including `temperature = 0` and disabled thinking mode where supported. Backend logs include task labels such as `Risk Analysis`, `Coverage Improvement`, `Test Case Generation`, and `Suite LLM Minimization`, making timing output easier to interpret.

Risk analysis uses a compact prompt and compact JSON response format. With the default settings (`LLM batch size = 25`, `LLM concurrency = 4`), a 100-requirement file is processed as four parallel LLM batches. The total risk-analysis time is therefore mainly bounded by the slowest batch, not by the sum of all four batch durations. Recent local runs have usually completed the LLM risk-analysis stage in about 3-4 seconds for the 100-requirement TodoList sample, but this is an observed runtime under current provider/network conditions rather than a guaranteed algorithmic bound. Earlier 5-6 second runs used the same compact parallel design and are consistent with normal LLM service latency variation.

Test suite improvement and state model improvement follow the same shared LLM execution pattern as the rest of the system. The only intentional exception is suite-level optimized-suite minimization, which reviews one suite per LLM batch because the prompt must include all candidate cases within that suite.

Example:

```text
[AutoTestDesign][LLM] request start task=Risk Analysis provider=deepseek ...
[TIMING][Risk Analysis] Batch 1: 3.426s (processing 25 items)
[TIMING][Coverage Improvement] Batch 2: 18.504s (processing 25 items)
```

## Test Suite Design

The tool includes an explicit `Test Suites` stage between strategy selection and test case generation.

Local suite generation uses:

- `structured_requirements`
- `coverage_items`
- `test_strategies`
- `risk_analysis`
- `state_transition_sequences`

For requirement-driven coverage, the backend groups items by:

```text
module + technique + coverage_type
```

Each group becomes one suite with fields such as:

- `suite_id`
- `suite_name`
- `module`
- `risk_level`
- `priority`
- `coverage_ids`
- `techniques`
- `coverage_types`
- `suite_objective`
- `optimization_basis`
- `source`

The suite `risk_level` and `priority` are derived conservatively from grouped items. Coverage IDs are preserved explicitly, so every generated test case can be traced through:

```text
Requirement -> Coverage Item -> Test Suite -> Test Case
```

The state modeling result is also integrated into suite design. When optimized transition sequences exist, the tool adds a `State Transition Model Suite`. This suite represents the coursework FR 4.0 behavior-modeling part and links transition-derived coverage IDs such as `COV-STATE-...` to later candidate test cases.

An optional `Improve Test Suites With LLM` action does not rewrite structural fields. The LLM can improve descriptive metadata only, while local validation preserves:

- `suite_id`
- `coverage_ids`
- traceability consistency

## Test Case Volume Control

Generated test cases are treated as candidate test cases, not all mandatory execution cases. To avoid combinatorial expansion, the generator limits the number of cases produced for each coverage item:

- Equivalence Partitioning: up to 2 cases.
- Decision Table Testing: up to 2 cases.
- Boundary Value Analysis: up to 4 cases.
- State Transition Testing: transition-sequence-driven cases linked to the state-model suite.

The global candidate set also has a configurable upper bound through `AUTOTESTDESIGN_MAX_GENERATED_TEST_CASES`, defaulting to 1000. When the limit is reached, the system preserves representative coverage first, then prioritizes by priority, risk level, and risk score.

For LLM-added missing test cases, each LLM batch can inspect the configured number of coverage items, but only a bounded number of missing test cases is accepted per batch. The default is controlled by `AUTOTESTDESIGN_MAX_MISSING_TEST_CASES_PER_BATCH`, currently 8. When the LLM returns more than the limit, the backend selects the best suggestions by risk level, priority, technique value, and coverage diversity instead of simply taking the first items.

Candidate test case generation is suite-driven. Normal suites generate cases from their linked coverage items and selected techniques. The state-model suite generates cases from optimized transition sequences, then maps them back into the same suite/test-case/traceability chain.

## Optimized Test Suite

The `Optimized test suite` is first produced locally through deterministic optimization:

- exact or near-structural duplicate removal,
- suite risk ordering,
- risk-based ordering,
- priority-based ordering,
- optional maximum-size minimization.

An optional `Improve Optimized Suite With LLM` button performs semantic minimization. The LLM does not rewrite the test case table. It reviews suites independently and returns only `keep` or `drop` decisions by `test_case_id`. The backend then validates the decisions locally and protects:

- high-risk test cases,
- high-priority test cases,
- the only test case for a `coverage_id`,
- at least one test case per suite.

The UI shows a short summary such as:

```text
LLM minimization removed 34 redundant cases, protected 5 high-value cases.
```

Detailed LLM decision tables are not displayed in the main workflow to keep the page focused on final artifacts.

## State Transition Modeling

The project includes a state transition modeling module. A local baseline model is inferred from structured requirements, and the UI displays:

- the state transition graph,
- the coverage criterion,
- optimized transition sequences.

There is also an optional `Improve State Model With LLM` action for improving the model when local inference is too generic. The model content remains structured data, and the graph is rendered locally from that data.

In the context of this coursework, this module is used as the FR 4.0 white-box modeling component:

- the internal behavior is represented explicitly as a state graph,
- coverage criteria are applied over that model,
- optimized transition sequences are generated from the model.

This supports behavior modeling and optimized sequence generation without requiring source-code branch or statement coverage analysis.

The transition sequence table is editable in the UI. After editing and saving it, downstream suites, test cases, and traceability are cleared and must be regenerated to keep artifacts consistent.

## Artifact Export

The export page focuses on generated test design artifacts instead of local project save/load.

The user can choose a unified export format:

- `XLSX`
- `CSV`
- `JSON`
- full package: `CSV` tables plus one `XLSX` workbook and one `JSON` artifact

The exported artifacts distinguish clearly between:

- `test_suites.csv`: high-level suite design
- `test_cases.csv`: candidate test cases
- `optimized_test_suite.csv`: final optimized suite
- `risk_analysis.csv`: risk scores and risk levels
- `state_transitions.csv`: state-model transition sequences

The Excel workbook contains the same artifact tables as separate sheets. JSON export also includes `state_transition_sequences` and `state_model`, making the exported package suitable for structured review or downstream tooling.

## Important Modules

- `Assignment2/app.py`: Streamlit UI and workflow integration.
- `Assignment2/src/ai_client.py`: LLM provider configuration, session reuse, request logging, and API calls.
- `Assignment2/src/llm_execution.py`: shared JSON parsing, batch execution, concurrency, and timing logs.
- `Assignment2/src/prompt_templates.py`: centralized prompt templates.
- `Assignment2/src/requirement_parser.py`: local and LLM requirement structuring.
- `Assignment2/src/risk_analyzer.py`: risk analysis with compact parallel LLM calls and rule fallback.
- `Assignment2/src/coverage_identifier.py`: local coverage item generation.
- `Assignment2/src/test_strategy_selector.py`: black-box and state-based test strategy selection.
- `Assignment2/src/test_suite_designer.py`: local suite generation, suite assignment, and LLM suite metadata improvement.
- `Assignment2/src/test_case_generator.py`: suite-driven candidate test case generation, LLM missing-case addition, and volume control.
- `Assignment2/src/state_modeler.py`: state transition model, graph data, and optimized transition sequence generation.
- `Assignment2/src/suite_optimizer.py`: deterministic test suite prioritization, deduplication, and minimization.
- `Assignment2/src/improvement_engine.py`: LLM-based coverage improvement, test design improvement, and suite minimization.
- `Assignment2/src/exporter.py`: CSV, JSON, Excel, and traceability export.

## Supported Test Design Techniques

- Equivalence Partitioning
- Boundary Value Analysis
- Decision Table Testing
- State Transition Testing

## Run

To run the Streamlit app:

```powershell
cd D:\course\ST\ST_Project
pip install -r Assignment2\requirements.txt
streamlit run Assignment2\app.py
```

## Recent Focus

- Separated local generation actions from LLM improvement actions.
- Added editable structured requirement output.
- Added compact prompts, batching, concurrency, connection reuse, and task-labeled LLM timing logs.
- Improved coverage identification and LLM missing coverage merge behavior.
- Added state transition graph visualization and LLM state model improvement.
- Added explicit high-level test suite design before candidate test case generation.
- Integrated state transition sequences into suite design and suite-driven test case generation.
- Limited test case explosion with per-technique and global candidate limits.
- Added LLM missing test case selection with risk-aware and coverage-diverse acceptance.
- Added LLM semantic minimization for optimized suites using keep/drop decisions with suite-level protection rules.
- Added editable state transition sequence tables and unified export format choices.
- Simplified the Test Cases page by replacing detailed LLM result tables with concise summaries.
- Removed local project persistence, selected-artifact export, and Selenium/PyTest draft generation from the main tool workflow.
- Centralized active LLM prompt templates in `src/prompt_templates.py`.
