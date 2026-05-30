# Assignment2 Project Brief

`Assignment2` is an AI-assisted software test design tool built with Python and Streamlit. It supports a requirement-driven workflow for generating structured requirements, risk analysis, coverage items, test strategies, state transition models, high-level test suites, candidate test cases, optimized execution suites, traceability matrices, and exportable test design artifacts.

The demonstration target is `simpletodolist`, a lightweight Todo List web application. The selected feature area is Todo Item Management, including adding, editing, deleting, completing, filtering, and clearing completed todo items. The implementation is domain-neutral: requirements can be imported from CSV, pasted as plain text, or edited directly in the UI.

## Workflow

1. Import, paste, or edit requirements.
2. Structure requirements into input fields, data ranges, conditions, actions, and expected results.
3. Analyze requirement risk and priority.
4. Generate coverage items and optionally improve missing coverage with LLM.
5. Generate test strategies and optionally review strategy selection with LLM.
6. Generate a state transition model and optimized transition sequences.
7. Generate high-level test suites.
8. Optionally refine suite descriptions with LLM.
9. Generate candidate test cases under the generated suites.
10. Optionally add missing test cases with LLM.
11. Generate and optionally improve the optimized execution suite.
12. Review the traceability matrix and export artifacts.

## Local Baseline and LLM Enhancement

The system separates deterministic local generation from optional LLM enhancement:

- Local logic provides fast, repeatable, traceable outputs.
- LLM calls are used for review, missing item discovery, semantic improvement, and suite minimization.
- LLM output is merged by local code instead of blindly replacing core artifacts.
- Downstream artifacts are reset when upstream data is edited, preserving consistency.
- Short UI notifications use toast messages, while tables remain focused on the generated artifacts.

This design keeps the workflow explainable for coursework: local rules guarantee a reproducible baseline, while LLM calls improve quality where semantic judgement is useful.

## LLM Performance Design

All major LLM features use shared performance settings from the sidebar:

- `LLM batch size`: controls how many requirements, coverage items, suites, or test cases are sent in one LLM batch.
- `LLM concurrency`: controls how many LLM batches can run in parallel.

LLM requests use a shared client with session reuse and connection pooling. DeepSeek calls run with deterministic settings, including `temperature = 0` and disabled thinking mode where supported. Backend logs include task labels such as `Risk Analysis`, `Coverage Improvement`, `Test Case Generation`, and `Suite LLM Improve`.

Risk analysis uses compact prompts and compact JSON responses. With the default settings (`LLM batch size = 25`, `LLM concurrency = 4`), a 100-requirement file is processed as four parallel LLM batches. Total runtime is mainly bounded by the slowest batch, not by the sum of all batch durations. Recent 3-4 second and earlier 5-6 second runs are both consistent with normal LLM service latency variation; the timing is an observed runtime, not a guaranteed algorithmic bound.

## Test Suite Design

The tool includes an explicit `Test Suites` stage between strategy selection and test case generation.

Local suite generation uses:

- `structured_requirements`
- `coverage_items`
- `test_strategies`
- `risk_analysis`
- `state_transition_sequences`

For requirement-driven coverage, the backend groups coverage items by:

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

The suite `risk_level` and `priority` are derived conservatively from grouped items. Coverage IDs are preserved explicitly, so generated test cases can be traced through:

```text
Requirement -> Coverage Item -> Test Strategy -> Test Suite -> Test Case
```

When optimized transition sequences exist, the tool also adds a state-transition suite. This suite links transition-derived coverage IDs such as `COV-STATE-...` to generated state-transition test cases.

The `Refine Suite Descriptions With LLM` action improves descriptive fields only:

- `suite_name`
- `suite_objective`
- `optimization_basis`

It does not rewrite structural fields such as `suite_id`, `coverage_ids`, `risk_level`, or `priority`. This keeps suite grouping and traceability stable while making the generated suite descriptions more suitable for the report.

## Test Case Generation

Generated test cases are treated as candidate test cases, not all mandatory execution cases. Candidate test case generation is suite-driven:

- Normal suites generate cases from their linked coverage items and selected techniques.
- State-transition suites generate cases from optimized transition sequences.
- Every generated case is assigned back to a suite through `coverage_id`.

To avoid combinatorial expansion, the generator limits cases per coverage item:

- Equivalence Partitioning: up to 2 cases.
- Decision Table Testing: up to 2 cases.
- Boundary Value Analysis: up to 4 cases.
- State Transition Testing: transition-sequence-driven cases.

The global candidate set also has a configurable upper bound through `AUTOTESTDESIGN_MAX_GENERATED_TEST_CASES`, defaulting to 1000. When the limit is reached, representative coverage is preserved first, then cases are prioritized by priority, risk level, and risk score.

For LLM-added missing cases, each batch can inspect multiple coverage items, but only a bounded number of missing cases is accepted per batch. The default is controlled by `AUTOTESTDESIGN_MAX_MISSING_TEST_CASES_PER_BATCH`, currently 8. When the LLM returns more than the limit, the backend selects suggestions by risk level, priority, technique value, and coverage diversity.

## Optimized Test Suite

The optimized suite is a recommended execution subset derived from candidate test cases. It is first produced locally through deterministic optimization:

- exact or near-structural duplicate removal,
- suite risk ordering,
- risk-based ordering,
- priority-based ordering,
- optional maximum-size minimization.

The `Improve Optimized Suite With LLM` action performs semantic minimization. The LLM does not rewrite test case content. It reviews suites independently and returns `keep` or `drop` decisions by `test_case_id`. The backend then validates the decisions locally and protects:

- high-risk test cases,
- high-priority test cases,
- the only test case for a `coverage_id`,
- at least one test case per suite.

The optimized suite supports the coursework optimization requirement by producing a smaller, prioritized execution set while preserving high-value coverage.

## Traceability Matrix

The traceability matrix is based on the complete candidate `test_cases` table, not the optimized execution subset.

This means:

- `test_cases.csv` and `traceability_matrix.csv` have matching design coverage scope.
- `optimized_test_suite.csv` may contain fewer rows because it is the recommended execution subset.
- Optimization does not remove evidence that the full generated design covers requirements, coverage items, strategies, suites, and test cases.

State-transition-derived test cases use the synthetic requirement ID `REQ-STATE-MODEL`. For readability, traceability rows for these cases are filled with:

- `requirement_text`: `State model derived requirement`
- `module`: the single detected module name, or `Cross-module behavior`
- `coverage_type`: `State Transition`
- `related_techniques`: `State Transition Testing`

## State Transition Modeling

The project includes a state transition modeling module. A local baseline model is inferred from structured requirements, and the UI displays:

- the state transition graph,
- the coverage criterion,
- optimized transition sequences.

The optional `Improve State Model With LLM` action can improve the generated model when local inference is too generic. The model remains structured data, and the graph is rendered locally from that data.

This module supports the coursework behavior-modeling requirement:

- behavior is represented as a state graph,
- coverage criteria are applied over that model,
- optimized transition sequences are generated from the model,
- transition-derived test cases are integrated into the suite and traceability workflow.

The transition sequence table is editable. After editing and saving it, downstream suites, test cases, optimized suites, and traceability are cleared and must be regenerated.

## Artifact Export

The export page focuses on generated test design artifacts, not local project state.

The user can choose one export format:

- `XLSX workbook`
- `CSV package`
- `JSON artifact`
- `Full package`

The exported artifacts include:

- `requirements_structured.csv`
- `risk_analysis.csv`
- `coverage_items.csv`
- `test_strategies.csv`
- `test_suites.csv`
- `test_cases.csv`
- `optimized_test_suite.csv`
- `traceability_matrix.csv`
- `state_transitions.csv`
- `test_design_artifacts.xlsx`
- `test_suite_artifacts.json`

CSV export writes one table per file. The XLSX workbook contains the same artifact tables as separate sheets. JSON export contains the same structured artifact data plus `state_model`.

The tool does not export Selenium/PyTest draft scripts and does not provide local project save/load persistence in the main workflow.

## Important Modules

- `Assignment2/app.py`: Streamlit UI and workflow integration.
- `Assignment2/src/ai_client.py`: LLM provider configuration, session reuse, request logging, and API calls.
- `Assignment2/src/llm_execution.py`: shared JSON parsing, batch execution, concurrency, and timing logs.
- `Assignment2/src/prompt_templates.py`: centralized prompt templates.
- `Assignment2/src/requirement_parser.py`: local and LLM requirement structuring.
- `Assignment2/src/risk_analyzer.py`: risk analysis with compact parallel LLM calls and rule fallback.
- `Assignment2/src/coverage_identifier.py`: local coverage item generation.
- `Assignment2/src/test_strategy_selector.py`: black-box and state-based strategy selection.
- `Assignment2/src/test_suite_designer.py`: suite generation, suite assignment, and LLM suite description refinement.
- `Assignment2/src/test_case_generator.py`: suite-driven candidate test case generation, LLM missing-case addition, and volume control.
- `Assignment2/src/state_modeler.py`: state transition model, graph data, and optimized transition sequence generation.
- `Assignment2/src/suite_optimizer.py`: deterministic suite prioritization, deduplication, and minimization.
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
