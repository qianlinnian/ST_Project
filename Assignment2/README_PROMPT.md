# Prompt Guide For AutoTestDesign

This document explains how prompts are organized and used in the current project.
It is intended as a reviewer-facing supplement to the source code so that instructors or TAs can understand the project's prompt design without reading every implementation file first.

## 1. Primary Prompt Storage Path

The main prompt definitions are stored in:

- [./src/prompt_templates.py](./src/prompt_templates.py:1)

This file contains:

- `SYSTEM` prompt constants
- prompt builder functions that convert current artifacts into compact LLM input text

Examples include:

- `COMPACT_REQUIREMENT_STRUCTURING_SYSTEM`
- `COMPACT_RISK_SYSTEM`
- `COMPACT_COVERAGE_IMPROVEMENT_SYSTEM`
- `COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM`
- `ORACLE_REVIEW_SYSTEM`
- `COMPACT_SUITE_MINIMIZATION_SYSTEM`
- `TEST_PLAN_DOCUMENT_IMPROVEMENT_SYSTEM`

and related builder functions such as:

- `compact_requirement_structuring_prompt(...)`
- `compact_risk_prompt(...)`
- `compact_coverage_improvement_prompt(...)`
- `missing_test_case_prompt(...)`
- `oracle_review_prompt(...)`
- `compact_suite_minimization_prompt(...)`
- `test_plan_document_improvement_prompt(...)`

## 2. Important Clarification

Prompts are mainly stored in `prompt_templates.py`, but prompt text alone does not define system behavior.

Actual orchestration is distributed across several modules:

- [./src/improvement_engine.py](./src/improvement_engine.py:1)
- [./src/test_case_generator.py](./src/test_case_generator.py:1)
- [./src/oracle_generator.py](./src/oracle_generator.py:1)
- [./src/test_plan_document_generator.py](./src/test_plan_document_generator.py:1)
- [./src/test_suite_designer.py](./src/test_suite_designer.py:1)
- [./src/llm_execution.py](./src/llm_execution.py:1)
- [./src/ai_client.py](./src/ai_client.py:1)

These modules are responsible for:

- deciding when LLM enhancement is used
- batching requests
- choosing concurrency
- parsing JSON outputs
- merging suggestions back into artifacts
- applying fallback logic if the response is invalid

## 3. Overall Prompting Philosophy

The tool does not rely on prompting alone. Its design is intentionally `local-first`.

The general pattern is:

1. generate a baseline artifact locally using rules, heuristics, or lightweight models
2. optionally send a compact summary to an LLM for refinement
3. validate or merge the result conservatively
4. preserve IDs and traceability whenever possible

This means the prompts are used mainly for:

- clarification
- refinement
- supplementation
- formal document polishing

They are not intended to replace the entire test design pipeline.

## 4. Why The Prompts Are Compact

Many prompts in this project use a compact serialization format instead of large natural-language contexts.

This is done to:

- reduce token usage
- improve batch throughput
- lower API cost
- make parsing easier
- keep LLM tasks focused on one narrow responsibility

For example, the tool often sends compact rows such as:

- requirement summaries
- coverage IDs and coverage descriptions
- test case IDs with short fields
- suite payloads grouped by `suite_id`

instead of sending full tables with repeated explanatory text.

## 5. Prompt Categories

The current prompts can be grouped by function.

### 5.1 Requirement Structuring

Purpose:

- convert raw requirement text into structured requirement rows

Main prompts:

- `REQUIREMENT_STRUCTURING_SYSTEM`
- `COMPACT_REQUIREMENT_STRUCTURING_SYSTEM`

Typical output:

- structured requirement records with fields such as action, condition, input, and expected behavior

Why it exists:

- raw requirement statements are often too unstructured for later risk, coverage, and suite generation

### 5.2 Risk Analysis

Purpose:

- produce requirement-level risk assessments

Main prompts:

- `RISK_ANALYSIS_SYSTEM`
- `COMPACT_RISK_SYSTEM`

Typical output:

- impact
- likelihood
- risk score
- risk level
- test-oriented risk reasoning

Why it exists:

- later prioritization and schedule decisions should be risk-driven rather than purely enumerative

### 5.3 Coverage Improvement

Purpose:

- improve or supplement locally generated coverage items

Main prompt:

- `COMPACT_COVERAGE_IMPROVEMENT_SYSTEM`

Typical output:

- missing coverage items
- revised descriptions for weak coverage rows
- improved technique hints or notes

Design note:

- this prompt is not limited to adding new coverage rows; it may also improve an existing row if the current description is weak

### 5.4 Test Strategy Review

Purpose:

- review selected test techniques against current coverage items

Main prompt:

- `TEST_STRATEGY_REVIEW_SYSTEM`

Typical output:

- comments or improved strategy suggestions for the selected techniques

Why it exists:

- locally selected techniques may be acceptable but not always well justified or clearly explained

### 5.5 Test Case Generation

Purpose:

- generate detailed candidate test cases from coverage and suite context

Main prompt:

- `TEST_CASE_GENERATION_SYSTEM`

Typical output:

- test case rows with inputs, steps, expected results, priorities, and design basis

Important note:

- this stage is still constrained by local IDs, suite assignments, and coverage traceability

### 5.6 Test Case Improvement

Purpose:

- revise existing test cases or add truly missing ones

Main prompt:

- `COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM`

Typical output:

- improved rows for existing `test_case_id`s
- optionally new cases when a real gap remains

Why it matters:

- the LLM is encouraged not only to add cases, but also to clarify weak existing content such as vague steps or incomplete expected results

### 5.7 Oracle Review

Purpose:

- improve the `expected_result` field specifically

Main prompt:

- `ORACLE_REVIEW_SYSTEM`

Typical output:

- clearer, more observable expected results

Why this stage is separate:

- expected results often need more precision than the rest of the case row
- a focused prompt improves reliability compared with asking one broad prompt to rewrite the entire test case

### 5.8 Suite Minimization Review

Purpose:

- review optimized suites for redundancy and decide which cases should remain

Main prompts:

- `SUITE_OPTIMIZATION_REVIEW_SYSTEM`
- `COMPACT_SUITE_MINIMIZATION_SYSTEM`

Typical output:

- `keep` or `drop` decisions
- short reasons for minimization

Design note:

- this is intentionally conservative
- the goal is not to redesign the whole suite, but to remove low-value redundancy without breaking coverage too aggressively

### 5.9 State Model Improvement

Purpose:

- improve the inferred state-based behavior model

Main prompt:

- `STATE_MODEL_IMPROVEMENT_SYSTEM`

Typical output:

- structured state model JSON
- improved states, transitions, guards, or events

Why it exists:

- state-related testing is difficult to derive perfectly from simple local parsing alone

### 5.10 Suite Metadata Improvement

Purpose:

- improve suite naming, objective wording, and design-basis clarity

Main prompt:

- `SUITE_DESIGN_IMPROVEMENT_SYSTEM`

Typical output:

- revised suite names
- clearer suite objectives
- improved design basis wording

### 5.11 Test Plan Document Improvement

Purpose:

- polish the generated Markdown test plan document

Main prompt:

- `TEST_PLAN_DOCUMENT_IMPROVEMENT_SYSTEM`

Typical output:

- a revised full Markdown document

Important note:

- unlike most structured prompts, this stage returns the full document rather than a small JSON patch
- it is therefore used for wording improvement and document polishing, not for machine-critical ID generation

## 6. How Prompt Outputs Are Controlled

For machine-readable stages, the prompts are intentionally strict.

Common controls include:

- JSON-only output instructions
- fixed field names
- explicit ID preservation
- limits on the kinds of fields the LLM may change

This is important because later artifacts depend on:

- `requirement_id`
- `coverage_id`
- `suite_id`
- `test_case_id`

If prompts were unconstrained, traceability would degrade quickly.

## 7. Batch Processing And Concurrency

The project does not send all artifacts in one giant request.
Instead, many LLM stages use batching.

This design supports:

- lower prompt size per request
- better error isolation
- partial success even if one batch fails
- configurable concurrency from the UI

Typical examples include:

- compact risk analysis batches
- coverage improvement batches
- test case improvement batches
- oracle review batches
- suite minimization batches

This logic is implemented mainly in:

- [./src/llm_execution.py](./src/llm_execution.py:1)
- [./src/improvement_engine.py](./src/improvement_engine.py:1)

## 8. Fallback And Reliability Strategy

The tool assumes LLM responses can fail, drift, or return malformed JSON.

Because of that, many stages include:

- response parsing checks
- fallback to original local artifacts
- partial merge instead of blind overwrite

This is especially important for:

- compact JSON prompts
- oracle review
- suite minimization
- test case improvement

The goal is practical robustness rather than unrestricted generation.

## 9. Reviewer Notes

For grading or project review, the key point is:

- the system is not prompt-only
- the LLM is used as an optional enhancement layer over a local test-design pipeline

In other words:

- requirements, risks, coverage, suites, and cases all have local generation logic
- prompts are mainly used to improve quality, clarity, or completeness
- the project deliberately preserves traceability and controlled outputs

This is why prompt design here emphasizes:

- compactness
- structured outputs
- conservative merging
- local-first generation

## 10. Recommended Code Reading Order

If a reviewer wants to inspect the implementation efficiently, this order is recommended:

1. [./src/prompt_templates.py](./src/prompt_templates.py:1)
2. [./src/ai_client.py](./src/ai_client.py:1)
3. [./src/llm_execution.py](./src/llm_execution.py:1)
4. [./src/improvement_engine.py](./src/improvement_engine.py:1)
5. [./src/test_case_generator.py](./src/test_case_generator.py:1)
6. [./src/oracle_generator.py](./src/oracle_generator.py:1)
7. [./src/test_plan_document_generator.py](./src/test_plan_document_generator.py:1)

This sequence makes the prompt definitions, execution model, and merge behavior easier to understand together.
