from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion
from src.prompt_templates import (
    COVERAGE_IMPROVEMENT_SYSTEM,
    SUITE_OPTIMIZATION_REVIEW_SYSTEM,
    coverage_improvement_prompt,
    suite_optimization_review_prompt,
)
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases, improve_test_cases_with_llm
from src.test_strategy_selector import select_strategies


def _next_coverage_id(existing: pd.DataFrame, offset: int) -> str:
    return f"COV-AI-{offset:03d}"


def suggest_missing_coverage_with_llm(
    requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    if not use_llm or not provider or not is_llm_enabled(provider):
        return pd.DataFrame(columns=coverage_items.columns.tolist() + ["reason"])

    try:
        prompt = coverage_improvement_prompt(
            requirements.to_string(index=False),
            coverage_items.to_string(index=False),
        )
        parsed = call_json_completion(
            COVERAGE_IMPROVEMENT_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=1800,
        )
    except Exception as exc:
        return pd.DataFrame([{"llm_error": str(exc)}])

    rows: list[dict[str, Any]] = []
    for index, item in enumerate(parsed.get("missing_coverage_items", []), start=1):
        rows.append(
            {
                "coverage_id": _next_coverage_id(coverage_items, index),
                "requirement_id": item.get("requirement_id", ""),
                "description": item.get("description", ""),
                "coverage_type": item.get("coverage_type", "Functional"),
                "risk_level": item.get("risk_level", "Medium"),
                "related_techniques": item.get("related_techniques", []),
                "tags": ["llm-suggested"],
                "notes": parsed.get("review_summary", ""),
                "reason": item.get("reason", ""),
            }
        )
    return pd.DataFrame(rows)


def review_suite_optimization_with_llm(
    test_cases: pd.DataFrame,
    optimized_test_cases: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    if (
        not use_llm
        or not provider
        or not is_llm_enabled(provider)
        or test_cases.empty
        or optimized_test_cases.empty
    ):
        return pd.DataFrame(
            columns=["optimization_review", "coverage_risks", "recommended_changes"]
        )

    try:
        prompt = suite_optimization_review_prompt(
            test_cases.to_string(index=False),
            optimized_test_cases.to_string(index=False),
        )
        parsed = call_json_completion(
            SUITE_OPTIMIZATION_REVIEW_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=1000,
        )
    except Exception as exc:
        return pd.DataFrame([{"llm_error": str(exc)}])

    return pd.DataFrame(
        [
            {
                "optimization_review": parsed.get("optimization_review", ""),
                "coverage_risks": parsed.get("coverage_risks", []),
                "recommended_changes": parsed.get("recommended_changes", []),
            }
        ]
    )


def generate_improved_test_design_with_llm(
    requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    existing_test_cases: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> dict[str, pd.DataFrame]:
    missing_coverage = suggest_missing_coverage_with_llm(
        requirements,
        coverage_items,
        provider,
        model,
        use_llm,
        batch_size=batch_size,
        concurrency=concurrency,
    )
    if missing_coverage.empty or "llm_error" in missing_coverage.columns:
        improved_cases = improve_test_cases_with_llm(
            existing_test_cases,
            provider,
            model,
            use_llm,
            batch_size=batch_size,
            concurrency=concurrency,
        )
        optimized_cases = optimize_suite(improved_cases)
        suite_review = review_suite_optimization_with_llm(
            improved_cases,
            optimized_cases,
            provider,
            model,
            use_llm,
            batch_size=batch_size,
            concurrency=concurrency,
        )
        return {
            "missing_coverage": missing_coverage,
            "suggested_test_cases": improved_cases,
            "suite_optimization_review": suite_review,
        }

    combined_coverage = pd.concat([coverage_items, missing_coverage[coverage_items.columns]], ignore_index=True)
    strategies = select_strategies(
        combined_coverage,
        provider=provider,
        model=model,
        use_llm=use_llm,
        batch_size=batch_size,
        concurrency=concurrency,
    )
    suggested_cases = generate_test_cases(
        requirements,
        missing_coverage[coverage_items.columns],
        strategies,
        provider=provider,
        model=model,
        use_llm=use_llm,
        batch_size=batch_size,
        concurrency=concurrency,
    )
    improved_cases = improve_test_cases_with_llm(
        pd.concat([existing_test_cases, suggested_cases], ignore_index=True),
        provider,
        model,
        use_llm,
        batch_size=batch_size,
        concurrency=concurrency,
    )
    optimized_cases = optimize_suite(improved_cases)
    suite_review = review_suite_optimization_with_llm(
        improved_cases,
        optimized_cases,
        provider,
        model,
        use_llm,
        batch_size=batch_size,
        concurrency=concurrency,
    )
    return {
        "missing_coverage": missing_coverage,
        "suggested_test_cases": improved_cases,
        "suite_optimization_review": suite_review,
    }
