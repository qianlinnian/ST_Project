# Prompt Design

This document is owned by A.

A maintains the shared prompt structure, output format constraints, API usage assumptions, fallback behavior, and review rules. B and C provide domain-specific testing rules for their modules.

## Ownership

| Area | Content Provider | Prompt Maintainer |
| --- | --- | --- |
| Requirement structuring | B | A |
| Risk explanation | B | A |
| Coverage identification | B | A |
| Test strategy selection | C | A |
| Test case generation | C | A |
| Oracle generation | C | A |
| Improvement suggestions | B/C | A |

## Prompt Design Principles

- Prompts must be derived from testing concepts, not written as generic chat requests.
- Prompts must request structured output whenever the tool needs to parse the response.
- LLM output is advisory and must be reviewed by the human tester.
- If API calls fail or the output cannot be parsed, the tool falls back to local rules.
- Prompt versions and major changes should be recorded for the final report.
