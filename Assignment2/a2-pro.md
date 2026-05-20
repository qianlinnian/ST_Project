# Assignment2 Project Brief

`Assignment2` is an AI-assisted software test design tool built with Python and Streamlit. It supports a requirement-driven workflow for generating risk analysis, coverage items, test strategies, test cases, optimized test suites, traceability matrices, and exportable project artifacts.

The demonstration target is `simpletodolist`, a lightweight Todo List web application. The tested feature area is Todo Item Management, including adding, editing, deleting, completing, filtering, clearing completed todos, and persistence behavior. The implementation is domain-neutral: requirements can be imported from CSV, plain text, or edited table input.

## Workflow

1. Import or edit requirements.
2. Structure requirements into input fields, data ranges, conditions, actions, and expected results.
3. Manually edit and save structured requirement fields when local or LLM extraction needs correction.
4. Analyze requirement risk and priority.
5. Generate coverage items and optionally improve missing coverage with LLM.
6. Select black-box or state-based test design strategies, with optional LLM review.
7. Generate candidate test cases.
8. Add missing test cases with LLM when useful.
9. Generate and optionally improve the optimized test suite.
10. Generate traceability matrix and export artifacts.

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

Example:

```text
[AutoTestDesign][LLM] request start task=Risk Analysis provider=deepseek ...
[TIMING][Risk Analysis] Batch 1: 4.026s (processing 25 items)
[TIMING][Coverage Improvement] Batch 2: 18.504s (processing 25 items)
```

## Test Case Volume Control

Generated test cases are treated as candidate test cases, not all mandatory execution cases. To avoid combinatorial expansion, the generator limits the number of cases produced for each coverage item:

- Equivalence Partitioning: up to 2 cases.
- Decision Table Testing: up to 2 cases.
- Boundary Value Analysis: up to 4 cases.
- State Transition Testing: up to 1 representative case per state coverage item.

The global candidate set also has a configurable upper bound through `AUTOTESTDESIGN_MAX_GENERATED_TEST_CASES`, defaulting to 1000. When the limit is reached, the system preserves representative coverage first, then prioritizes by priority, risk level, and risk score.

For LLM-added missing test cases, each LLM batch can inspect the configured number of coverage items, but only a bounded number of missing test cases is accepted per batch. The default is controlled by `AUTOTESTDESIGN_MAX_MISSING_TEST_CASES_PER_BATCH`, currently 8. When the LLM returns more than the limit, the backend selects the best suggestions by risk level, priority, technique value, and coverage diversity instead of simply taking the first items.

## Optimized Test Suite

The `Optimized test suite` is first produced locally through deterministic optimization:

- exact or near-structural duplicate removal,
- risk-based ordering,
- priority-based ordering,
- optional maximum-size minimization.

An optional `Improve Optimized Suite With LLM` button performs semantic minimization. The LLM does not rewrite the test case table. It reviews small batches and returns only `keep` or `drop` decisions by `test_case_id`. The backend then validates the decisions locally and protects:

- high-risk test cases,
- high-priority test cases,
- the only test case for a `coverage_id`.

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

There is also an optional `Improve State Model With LLM` action for improving the model when local inference is too generic. This supports the coursework requirement for behavior modeling and optimized sequence generation without requiring source-code white-box analysis.

## Important Modules

- `Assignment2/app.py`: Streamlit UI and workflow integration.
- `Assignment2/src/ai_client.py`: LLM provider configuration, session reuse, request logging, and API calls.
- `Assignment2/src/llm_execution.py`: shared JSON parsing, batch execution, concurrency, and timing logs.
- `Assignment2/src/prompt_templates.py`: centralized prompt templates.
- `Assignment2/src/requirement_parser.py`: local and LLM requirement structuring.
- `Assignment2/src/risk_analyzer.py`: risk analysis with compact parallel LLM calls and rule fallback.
- `Assignment2/src/coverage_identifier.py`: local coverage item generation.
- `Assignment2/src/test_strategy_selector.py`: black-box and state-based test strategy selection.
- `Assignment2/src/test_case_generator.py`: candidate test case generation, LLM missing-case addition, and volume control.
- `Assignment2/src/state_modeler.py`: state transition model, graph data, and optimized transition sequence generation.
- `Assignment2/src/suite_optimizer.py`: deterministic test suite prioritization, deduplication, and minimization.
- `Assignment2/src/improvement_engine.py`: LLM-based coverage improvement, test design improvement, and suite minimization.
- `Assignment2/src/exporter.py`: CSV, JSON, Excel, traceability, and draft test export.

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
- Limited test case explosion with per-technique and global candidate limits.
- Added LLM missing test case selection with risk-aware and coverage-diverse acceptance.
- Added LLM semantic minimization for optimized suites using keep/drop decisions.
- Simplified the Test Cases page by replacing detailed LLM result tables with concise summaries.
