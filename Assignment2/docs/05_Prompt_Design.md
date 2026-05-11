# Prompt Design

This document is owned by A.

A maintains the shared prompt structure, output format constraints, API usage assumptions, fallback behavior, and review rules. B and C provide domain-specific testing rules and field definitions for their modules.

## Ownership

| Area | Content Provider | Prompt Maintainer |
| --- | --- | --- |
| Requirement structuring | B | A |
| Risk explanation | B | A |
| Coverage identification / improvement | B | A |
| Test strategy review | C | A |
| Test case improvement | C | A |
| Oracle / Expected Result review | C | A |
| Test suite optimization review | C | A |

## Prompt Design Principles

- Prompts are derived from the actual B/C module fields, not from generic chat requests.
- Prompts preserve traceability fields such as `requirement_id`, `coverage_id`, and `test_case_id`.
- Prompts request structured JSON-like output when the tool may parse or store the response.
- LLM output is advisory and must be reviewed by the human tester before being accepted.
- If API calls fail or the output cannot be parsed, the tool falls back to local rules.
- Prompt versions and major changes should be recorded for the final report.

## B Module Fields

### Requirement Structuring

Input:

- `requirement_id`
- `module`
- `requirement_text`

Output fields:

- `input_fields`
- `data_ranges`
- `conditions`
- `actions`
- `expected_results`

Prompt purpose:

- Review whether the requirement has been structured completely.
- Suggest missing input fields, ranges, conditions, actions, or expected results.
- Do not replace B's parser directly without human review.

### Risk Analysis

Output fields:

- `requirement_id`
- `impact`
- `probability`
- `risk_score`
- `risk_level`
- `reason`

Prompt purpose:

- Explain risk scoring in ISTQB terms.
- Check whether `risk_level` is reasonable.
- Provide a human-readable rationale for the risk analysis report.

### Coverage Items

Output fields:

- `coverage_id`
- `requirement_id`
- `description`
- `coverage_type`
- `risk_level`
- `related_techniques`
- `tags`
- `notes`

Prompt purpose:

- Review whether coverage items fully cover requirements and structured fields.
- Suggest missing coverage items with requirement traceability.
- Do not duplicate existing coverage items.

## C Module Fields

### Test Strategy

Output fields:

- `coverage_id`
- `requirement_id`
- `coverage_type`
- `risk_level`
- `technique`
- `technique_standard`
- `strategy_reason`

Available techniques:

- `Equivalence Partitioning`
- `Boundary Value Analysis`
- `Decision Table Testing`
- `State Transition Testing`

Prompt purpose:

- Review whether the chosen technique fits each coverage item.
- Suggest technique changes with a clear reason.
- Preserve `coverage_id` and `requirement_id`.

### Test Cases

Output fields:

- `test_case_id`
- `requirement_id`
- `coverage_id`
- `technique`
- `technique_standard`
- `precondition`
- `test_data`
- `steps`
- `expected_result`
- `priority`
- `risk_score`
- `risk_level`
- `coverage_type`
- `automation_candidate`
- `source`
- `design_basis`

Prompt purpose:

- Review generated test cases for clarity and traceability.
- Suggest improvements to test data, steps, expected result, or design basis.
- Do not invent new IDs unless the user asks for missing cases.

### Oracle / Expected Result

Prompt purpose:

- Review whether `expected_result` is observable and testable.
- Align expected results with requirement text, test data, and selected technique.
- Avoid vague results such as "works correctly".

### Test Suite Optimization

Prompt purpose:

- Review whether optimized test cases preserve high-risk and high-value coverage.
- Identify possible over-removal or duplicate cases.
- Explain prioritization and minimization decisions.

## Implemented Templates

The current prompt template file is:

```text
src/prompt_templates.py
```

It contains:

- `requirement_structuring_prompt`
- `risk_explanation_prompt`
- `coverage_improvement_prompt`
- `test_strategy_review_prompt`
- `test_case_improvement_prompt`
- `oracle_review_prompt`
- `suite_optimization_review_prompt`

## Current Integration

The Streamlit app currently calls the coverage review prompt from the `AI Review` page:

```text
COVERAGE_IMPROVEMENT_SYSTEM
coverage_improvement_prompt(...)
```

Other prompts are prepared for later UI buttons or B/C module integration.
