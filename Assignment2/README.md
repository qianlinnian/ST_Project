# AutoTestDesign AI App

AutoTestDesign is a Streamlit-based test design workspace built for Assignment 2.
It supports a requirement-driven workflow for generating and refining:

- structured requirements
- risk analysis
- coverage items
- test strategies
- high-level test suites
- detailed test cases
- traceability matrices
- a Markdown Test Plan document

The current demonstration target is `../simpletodolist`, but the tool itself is designed to be domain-neutral and requirement-driven.

## 1. What The Tool Does

The application guides the user through the following workflow:

1. `Requirement Input`
2. `Risk Analysis`
3. `Coverage, Strategy & Model`
4. `Suites & Cases`
5. `Test Plan Document`
6. `Export`

The workflow is deliberately staged. Earlier artifacts become inputs to later artifacts, which makes the generated outputs traceable and easier to review.

## 2. Environment Setup

### 2.1 Python Dependencies

Install the required packages:

```powershell
pip install -r requirements.txt
```

Current Python package dependencies:

- `streamlit`
- `pandas`
- `openpyxl`
- `scikit-learn`
- `pytest`
- `python-dotenv`
- `requests`
- `spacy`

### 2.2 spaCy Model

The requirement processing flow uses spaCy. Install the English model separately:

```powershell
python -m spacy download en_core_web_sm
```

Why this is needed:

- `spacy` installs the NLP framework
- `en_core_web_sm` provides the English language model used by local requirement parsing

## 3. LLM Configuration

The tool is designed to work in two modes:

1. `local-first mode`
2. `local + LLM enhancement mode`

It can run without any external LLM API. In that case, the system still performs local rule-based or lightweight ML-based generation.

### 3.1 Configure `.env`

Copy the template:

```powershell
Copy-Item .env.example .env
```

Then fill in your API keys and endpoints.

The current `.env.example` assumes OpenAI-compatible chat completion endpoints:

```text
AUTOTESTDESIGN_LLM_PROVIDERS=deepseek,aliyun
AUTOTESTDESIGN_LLM_TIMEOUT=120
AUTOTESTDESIGN_LLM_LOG=1

AUTOTESTDESIGN_LLM_DEEPSEEK_API_KEY=
AUTOTESTDESIGN_LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
AUTOTESTDESIGN_LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro,deepseek-chat

AUTOTESTDESIGN_LLM_ALIYUN_API_KEY=
AUTOTESTDESIGN_LLM_ALIYUN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AUTOTESTDESIGN_LLM_ALIYUN_MODELS=qwen-plus,qwen-max,qwen3.5-plus
```

### 3.2 Runtime LLM Settings

Inside the Streamlit sidebar, the user can adjust:

- provider
- model
- LLM batch size
- LLM concurrency

These settings affect optional LLM-enhanced stages such as:

- coverage improvement
- strategy improvement
- test suite description improvement
- test case revision and supplementation
- oracle clarification for expected results
- optimized suite minimization review
- test plan document improvement

## 4. How To Start The App

Run the Streamlit application from the current project directory:

```powershell
streamlit run app.py
```

After startup:

1. open the Streamlit local URL shown in the terminal
2. provide or edit requirement inputs
3. follow the workflow page by page
4. export the generated artifacts when ready

## 5. How To Use The Workflow

### 5.1 Requirement Input

This page is used to:

- enter requirements manually
- load structured requirement rows
- normalize missing or duplicate requirement IDs
- structure requirements into fields such as inputs, conditions, actions, and expected results

### 5.2 Risk Analysis

This page produces requirement-level risk outputs, including:

- risk category
- impact
- likelihood
- risk score
- risk level
- test suggestion

### 5.3 Coverage, Strategy & Model

This page generates:

- coverage items
- selected test techniques for each coverage item
- state transition sequences derived from the requirement behavior model

### 5.4 Suites & Cases

This page generates:

- high-level test suites
- candidate test cases
- optimized test suites
- traceability matrix

### 5.5 Test Plan Document

This page generates an English Markdown test plan document based on:

- requirements
- risks
- coverage items
- test strategies
- test suites
- test cases
- state transition information

The document can be:

- previewed
- edited
- improved with LLM
- exported directly as Markdown

### 5.6 Export

The export page supports:

- `Markdown document`
- `XLSX workbook`
- `CSV package`
- `JSON artifact`
- `Full package`

## 6. Code Structure

The main project layout is:

```text
./
  app.py
  requirements.txt
  README.md
  .env.example
  app_ui/
  src/
  data/
  docs/
  exports/
  scripts/
  tests/
```

### 6.1 UI Layer

`app.py`

- Streamlit entry point
- sidebar workflow navigation
- provider/model selection
- top-level page routing

`app_ui/`

- `actions.py`: UI-triggered workflow actions
- `state.py`: session state initialization and downstream resets
- `components.py`: shared UI widgets and metrics
- `styles.py`: custom Streamlit styling
- `pages/`: individual workflow pages

Important page files:

- `requirement_input.py`
- `risk_analysis.py`
- `coverage_strategy.py`
- `test_cases.py`
- `test_plan_document.py`
- `export.py`

### 6.2 Core Logic Layer

`src/`

- `requirement_parser.py`: requirement structuring
- `nlp_processor.py`: local NLP support
- `risk_analyzer.py`: risk generation and fallback logic
- `ml_risk_model.py`: lightweight ML risk scaffolding
- `coverage_identifier.py`: coverage item generation
- `test_strategy_selector.py`: strategy/technique selection
- `state_modeler.py`: state model and transition sequence generation
- `test_suite_designer.py`: suite design and suite metadata improvement
- `test_case_generator.py`: detailed test case generation
- `oracle_generator.py`: expected-result clarification
- `suite_optimizer.py`: optimized suite reduction
- `test_plan_document_generator.py`: Markdown test plan generation
- `exporter.py`: export pipeline and traceability output
- `improvement_engine.py`: orchestration for LLM-enhanced review and refinement
- `ai_client.py`: provider/model abstraction
- `llm_execution.py`: batch execution, fallback, timeout, and concurrency handling

### 6.3 Test And Sample Assets

- `data/`: sample requirement inputs
- `docs/`: reference and template material
- `exports/`: generated artifacts
- `scripts/`: utility scripts, including pytest export cleanup
- `tests/`: regression tests for core logic

## 7. LLM Processing Strategy

This tool does not rely on the LLM for the entire pipeline.
Its design is intentionally `local-first`, with optional LLM enhancement layered on top.

### 7.1 Local-First Baseline

Most pipeline stages have a local or rule-based baseline:

- requirement normalization
- requirement structuring fallback
- risk analysis fallback
- coverage generation
- strategy selection
- state model generation
- suite generation
- test case generation
- export and traceability generation

This means the tool remains usable even when:

- no API key is configured
- the provider is unavailable
- an LLM response fails
- JSON parsing fails

### 7.2 LLM Enhancement

The LLM is mainly used to improve existing artifacts rather than replace them entirely.

Examples:

- improve weak coverage descriptions
- refine strategy descriptions
- revise weak or vague test cases
- clarify expected results
- improve test suite metadata
- review optimized suites for safe minimization
- polish the final test plan document

### 7.3 Batch Processing

To keep requests manageable, the system processes LLM tasks in batches.
This is especially important for:

- requirement structuring
- risk analysis
- coverage improvement
- test case improvement
- oracle review
- suite minimization

The implementation uses configurable:

- batch size
- concurrency
- timeout

This helps control:

- latency
- token usage
- provider rate-limit pressure
- error recovery behavior

### 7.4 Fallback And Robustness

When an LLM stage fails, the tool generally does not stop the whole workflow.
Instead, it either:

- falls back to local logic, or
- preserves the current artifact and records the LLM error

This behavior is visible in the UI through warning messages and retained local outputs.

### 7.5 Why This Design Was Chosen

This mixed design was chosen to balance:

- reproducibility
- traceability
- usability without cloud dependencies
- better wording and refinement when an LLM is available

In other words:

- local logic provides the stable baseline
- LLM review provides optional quality improvement

## 8. Test Plan Document Design

The current tool treats the test plan as a document artifact, not as an internal table-only object.

The Markdown test plan is generated from existing artifacts and includes sections such as:

- project scope
- test items
- high-level test suite design
- schedule/checklist
- organization structure
- selected frameworks and rationale
- cost estimation
- current artifact summary

This document is meant to support assignment submission and project reporting, while the detailed structured tables remain available elsewhere in the tool and export package.

## 9. Testing

Run the main regression test file with:

```powershell
python -m pytest tests/test_case_generator.py -q
```

Other test files are also available under `tests/`.

## 10. Utility Scripts

`scripts/cleanup_pytest_exports.ps1`

Purpose:

- remove generated `pytest_*` export files from `exports/`

Example:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\cleanup_pytest_exports.ps1
```

## 11. Notes

- The generated artifacts are design artifacts, not executable end-to-end test programs by themselves.
- Frameworks such as Selenium, PyTest, and JUnit are described in the generated test plan, but the tool itself does not directly execute browser automation.
- The Todo example is only a demonstration target. The pipeline is meant to generalize to other applications as long as the requirements are available in a suitable form.
