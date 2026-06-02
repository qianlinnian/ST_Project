from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import chat_completion, is_llm_enabled
from src.prompt_templates import (
    TEST_PLAN_DOCUMENT_IMPROVEMENT_SYSTEM,
    test_plan_document_improvement_prompt,
)
from src.test_suite_designer import design_test_suites


def _split_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    separator = ";" if ";" in text else ","
    return [part.strip() for part in text.split(separator) if part.strip()]


def _summarise_test_items(structured_requirements: pd.DataFrame) -> tuple[list[str], list[str]]:
    modules = sorted(
        {
            str(value).strip()
            for value in structured_requirements.get("module", pd.Series(dtype=str)).dropna()
            if str(value).strip()
        }
    )
    requirement_texts = [
        str(value).strip()
        for value in structured_requirements.get("requirement_text", pd.Series(dtype=str)).dropna().tolist()
        if str(value).strip()
    ]
    functional = modules[:8] if modules else ["Core application behavior"]
    non_functional: list[str] = []
    for text in requirement_texts:
        lowered = text.lower()
        if any(keyword in lowered for keyword in ["persist", "reload", "save", "recover"]):
            non_functional.append("Basic reliability and persistence behavior")
        if any(keyword in lowered for keyword in ["error", "reject", "invalid", "safe"]):
            non_functional.append("Validation and safe failure handling")
    if not non_functional:
        non_functional = ["Risk-driven reliability and validation concerns"]
    return functional, sorted(set(non_functional))


def _scope_lines(
    structured_requirements: pd.DataFrame,
    risk_analysis: pd.DataFrame,
) -> list[str]:
    requirement_texts = [
        str(value).strip()
        for value in structured_requirements.get("requirement_text", pd.Series(dtype=str)).dropna().tolist()
        if str(value).strip()
    ]
    in_scope = [
        "Design testing activities for the functional behavior, input constraints, state changes, and exception handling explicitly stated in the current requirements.",
        "Prioritize high-risk requirements and preserve traceability across requirements, coverage items, test suites, and test cases.",
    ]
    mentions_validation = any(
        any(keyword in text.lower() for keyword in ["invalid", "reject", "error", "empty", "boundary"])
        for text in requirement_texts
    )
    if mentions_validation:
        in_scope.append("Give explicit attention to input validation, boundary conditions, and error handling when these are stated in the requirements.")

    high_risk = int((risk_analysis.get("risk_level", pd.Series(dtype=str)).astype(str) == "High").sum())
    if high_risk:
        in_scope.append(f"The current baseline contains {high_risk} high-risk requirement(s), and their related test activities are included in the priority scope.")

    out_scope = [
        "Fine-grained non-functional characteristics that are not explicitly stated in the current requirements are outside the main scope of this testing cycle.",
        "If dedicated security, performance, compatibility, or operational constraints are not stated in the requirements, they are mentioned only at a general risk level and are not expanded into detailed test design.",
    ]
    return [
        "Testing background and overall objectives:",
        *[f"- {line}" for line in in_scope],
        "",
        "Items outside the detailed scope of this test plan:",
        *[f"- {line}" for line in out_scope],
    ]


def _component_summary(functional_items: list[str]) -> list[str]:
    if not functional_items:
        return ["- Major system components will be refined further when more detailed requirements or architecture notes are available."]
    return [f"- Major business component: {item}" for item in functional_items]


def _suite_rows(suites: pd.DataFrame) -> list[str]:
    rows: list[str] = []
    for _, row in suites.iterrows():
        rows.append(
            "| "
            + " | ".join(
                [
                    str(row.get("suite_id", "")).strip() or "TBD",
                    str(row.get("suite_name", "")).strip() or "Unnamed suite",
                    str(row.get("risk_level", "")).strip() or "Medium",
                    str(row.get("techniques", "")).strip() or "TBD",
                    str(row.get("suite_objective", "")).strip() or "TBD",
                ]
            )
            + " |"
        )
    if not rows:
        rows.append("| TBD | Pending suite generation | Medium | TBD | Generate suites after coverage and strategy are available. |")
    return rows


def _schedule_rows(
    suites: pd.DataFrame,
    risk_analysis: pd.DataFrame,
) -> list[str]:
    high_suite_count = 0
    if not suites.empty and "risk_level" in suites.columns:
        high_suite_count = int((suites["risk_level"].astype(str) == "High").sum())
    high_req_count = int((risk_analysis.get("risk_level", pd.Series(dtype=str)).astype(str) == "High").sum())
    return [
        "| Phase | Focus | Checkpoint |",
        "| --- | --- | --- |",
        f"| Requirement and risk review | Confirm the test boundary and identify high-risk requirements | Structured requirements completed and {high_req_count} high-risk requirement(s) identified |",
        "| Coverage and strategy design | Select test techniques for major coverage targets | Coverage items and test strategies reviewed and accepted |",
        f"| Test suite design | Prioritize high-risk suites and confirm suite objectives | {len(suites)} suite(s) generated, including {high_suite_count} high-risk suite(s) |",
        "| Test case design and review | Produce executable and traceable test cases | Test cases and traceability matrix generated and checked |",
        "| Export and reporting | Deliver the final document and structured artifacts | Markdown test plan, suites, cases, and traceability exported |",
    ]


def _derive_suite_design(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    test_strategies: pd.DataFrame,
    risk_analysis: pd.DataFrame,
    state_transition_sequences: pd.DataFrame,
    test_suites: pd.DataFrame | None,
) -> pd.DataFrame:
    if test_suites is not None and not test_suites.empty:
        return test_suites.copy()
    return design_test_suites(
        structured_requirements,
        coverage_items,
        test_strategies,
        risk_analysis,
        state_transition_sequences,
    )


def _framework_section(test_suites: pd.DataFrame) -> list[tuple[str, str]]:
    techniques = " ".join(
        test_suites.get("techniques", pd.Series(dtype=str)).astype(str).tolist()
    ).lower()
    items = [
        (
            "PyTest",
            "Used as the main execution framework for automated tests, assertions, regression organization, and result reporting.",
        )
    ]
    if any(keyword in techniques for keyword in ["state transition", "boundary", "decision", "equivalence"]):
        items.append(
            (
                "Selenium",
                "Used for browser-level interaction and end-to-end workflow validation when the target application includes user-facing scenarios.",
            )
        )
    items.append(
        (
            "JUnit",
            "Can be used as a complementary framework for unit-level or component-level regression checks when the target application includes Java-side tests.",
        )
    )
    return items


def _cost_estimate(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    test_suites: pd.DataFrame,
    test_cases: pd.DataFrame,
) -> tuple[pd.DataFrame, float]:
    req_count = len(structured_requirements)
    cov_count = len(coverage_items)
    suite_count = len(test_suites)
    case_count = len(test_cases)
    rows = [
        ("Requirement analysis and risk assessment", max(0.5, round(req_count * 0.10, 1))),
        ("Coverage and test strategy design", max(0.5, round(cov_count * 0.04, 1))),
        ("Test suite and state-behavior design", max(0.5, round(suite_count * 0.15, 1))),
        ("Test case generation and review", max(0.5, round(case_count * 0.03, 1))),
        ("Result consolidation and document export", 0.5),
    ]
    cost_table = pd.DataFrame(rows, columns=["Work Item", "Estimated Person-Days"])
    total = float(cost_table["Estimated Person-Days"].sum())
    return cost_table, total


def _org_chart_mermaid() -> str:
    return "\n".join(
        [
            "```mermaid",
            "flowchart TD",
            '  TL["Test Lead"] --> RA["Risk & Coverage Analyst"]',
            '  TL --> SD["Suite Designer"]',
            '  TL --> AE["Automation Engineer"]',
            '  TL --> RV["Reviewer / Reporter"]',
            "```",
        ]
    )


def _org_chart_responsibilities() -> list[tuple[str, str]]:
    return [
        ("Test Lead", "Owns the overall test plan, milestone checks, and final review."),
        ("Risk & Coverage Analyst", "Analyzes requirements, risks, and coverage to keep the scope complete."),
        ("Suite Designer", "Designs high-level test suites, selects techniques, and defines suite objectives."),
        ("Automation Engineer", "Turns the test design into executable tests and integrates them with the selected frameworks."),
        ("Reviewer / Reporter", "Checks traceability, consolidates evidence, and prepares the final outputs."),
    ]


def generate_test_plan_document(
    project_name: str,
    structured_requirements: pd.DataFrame,
    risk_analysis: pd.DataFrame,
    coverage_items: pd.DataFrame,
    test_strategies: pd.DataFrame,
    state_transition_sequences: pd.DataFrame | None = None,
    test_suites: pd.DataFrame | None = None,
    test_cases: pd.DataFrame | None = None,
) -> str:
    suites = _derive_suite_design(
        structured_requirements,
        coverage_items,
        test_strategies,
        risk_analysis,
        state_transition_sequences if state_transition_sequences is not None else pd.DataFrame(),
        test_suites,
    )
    cases = test_cases if test_cases is not None else pd.DataFrame()
    functional_items, non_functional_items = _summarise_test_items(structured_requirements)
    cost_table, total_hours = _cost_estimate(structured_requirements, coverage_items, suites, cases)
    frameworks = _framework_section(suites)
    responsibilities = _org_chart_responsibilities()
    high_risk = int(
        (
            risk_analysis.get("risk_level", pd.Series(dtype=str)).astype(str) == "High"
        ).sum()
    )
    suite_rows = _suite_rows(suites)
    schedule_rows = _schedule_rows(suites, risk_analysis)
    framework_rows = [
        "| Framework / Tool | Rationale |",
        "| --- | --- |",
        *[f"| {name} | {reason} |" for name, reason in frameworks],
    ]
    responsibility_rows = [
        "| Role | Responsibility |",
        "| --- | --- |",
        *[f"| {role} | {responsibility} |" for role, responsibility in responsibilities],
    ]
    cost_rows = [
        "| Work Item | Estimated Person-Days |",
        "| --- | ---: |",
        *[
            f"| {row['Work Item']} | {float(row['Estimated Person-Days']):.1f} |"
            for _, row in cost_table.iterrows()
        ],
        f"| **Total** | **{total_hours:.1f}** |",
    ]

    return "\n".join(
        [
            f"# {project_name} Test Plan",
            "",
            "## 1. Project Scope",
            f"This test plan covers the testing activities for `{project_name}`. The current baseline contains "
            f"{len(structured_requirements)} structured requirement(s), {len(coverage_items)} coverage item(s), "
            f"{len(suites)} test suite(s), and {high_risk} high-risk requirement(s).",
            "",
            "This plan is based on the current requirement baseline, the corresponding risk analysis, and the identified coverage items.",
            "",
            *_scope_lines(structured_requirements, risk_analysis),
            "",
            "## 2. Test Items",
            "Major functional characteristics:",
            *[f"- {item}" for item in functional_items],
            "",
            "Major non-functional or cross-cutting concerns:",
            *[f"- {item}" for item in non_functional_items],
            "",
            "System architecture and major component description (abstracted from the available requirements):",
            *_component_summary(functional_items),
            "",
            "## 3. High-Level Test Suite Design",
            "The following test suites are derived from requirements, risk analysis, coverage items, and selected techniques. Only the core fields are retained in this document to support later detailed design.",
            "For each suite, the selected technique reflects the coverage focus and the associated risk level of the underlying requirement set.",
            "",
            f"The number of suites listed below is consistent with the suites table: {len(suites)} suite(s).",
            "",
            "| Suite ID | Suite Name | Risk Level | Techniques | Objective |",
            "| --- | --- | --- | --- | --- |",
            *suite_rows,
            "",
            "## 4. Schedule / Checklist",
            *schedule_rows,
            "",
            "## 5. Organization Structure",
            "### Responsibility Summary",
            *responsibility_rows,
            "",
            "### Organization Chart",
            _org_chart_mermaid(),
            "",
            "## 6. Selected Test Frameworks and Rationale",
            *framework_rows,
            "",
            "## 7. Cost Estimation",
            "The following estimate is expressed in person-days based on the current testing arrangement, suite volume, and test case design effort. It is intended for planning and for comparison with a manual test design baseline.",
            "",
            *cost_rows,
            "",
            "## 8. Current Artifact Summary",
            f"- Structured requirements: {len(structured_requirements)}",
            f"- Risks: {len(risk_analysis)}",
            f"- Coverage items: {len(coverage_items)}",
            f"- State transition sequences: {len(state_transition_sequences) if state_transition_sequences is not None else 0}",
            f"- Test suites: {len(suites)}",
            f"- Test cases: {len(cases)}",
        ]
    ).strip() + "\n"


def improve_test_plan_document_with_llm(
    document_markdown: str,
    project_name: str,
    structured_requirements: pd.DataFrame,
    risk_analysis: pd.DataFrame,
    coverage_items: pd.DataFrame,
    test_strategies: pd.DataFrame,
    test_suites: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
) -> str:
    if not document_markdown.strip() or not use_llm or not provider or not is_llm_enabled(provider):
        return document_markdown

    user_prompt = test_plan_document_improvement_prompt(
        project_name=project_name,
        document_markdown=document_markdown,
        structured_requirements=structured_requirements,
        risk_analysis=risk_analysis,
        coverage_items=coverage_items,
        test_strategies=test_strategies,
        test_suites=test_suites,
    )
    improved = chat_completion(
        TEST_PLAN_DOCUMENT_IMPROVEMENT_SYSTEM,
        user_prompt,
        provider=provider,
        model=model,
        max_tokens=3200,
        task_label="Test Plan Document Improvement",
    ).strip()
    return improved or document_markdown
