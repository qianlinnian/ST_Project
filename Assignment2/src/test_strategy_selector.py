from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.prompt_templates import (
    TEST_STRATEGY_REVIEW_SYSTEM,
    test_strategy_review_prompt as build_test_strategy_review_prompt,
)


TECHNIQUE_STANDARDS = {
    "Equivalence Partitioning": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 equivalence partitioning",
    "Boundary Value Analysis": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 boundary value analysis",
    "Decision Table Testing": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 decision table testing",
    "State Transition Testing": "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4 state transition testing",
}


def _as_text(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    return str(value or "")


def _coverage_text(row: pd.Series) -> str:
    values = [
        row.get("description", ""),
        row.get("coverage_item", ""),
        row.get("coverage_type", ""),
        row.get("tags", ""),
        row.get("related_techniques", ""),
        row.get("notes", ""),
    ]
    return " ".join(_as_text(value).lower() for value in values if value is not None)


def _fallback_strategy(row: pd.Series) -> tuple[str, str]:
    text = _coverage_text(row)

    if any(keyword in text for keyword in ["state", "transition", "lifecycle", "workflow", "event", "mode"]):
        return (
            "State Transition Testing",
            "Fallback rule: coverage describes states, events, or lifecycle behaviour, so state transition testing is suitable.",
        )

    if any(keyword in text for keyword in ["boundary", "range", "limit", "minimum", "maximum", "threshold", "length", "empty", "zero"]):
        return (
            "Boundary Value Analysis",
            "Fallback rule: coverage describes a boundary, range, limit, threshold, or empty/zero value.",
        )

    if any(keyword in text for keyword in ["condition", "combination", "rule", "decision", "if", "when", "valid and", "valid or"]):
        return (
            "Decision Table Testing",
            "Fallback rule: coverage depends on combinations of conditions and actions.",
        )

    return (
        "Equivalence Partitioning",
        "Fallback rule: representative valid and invalid partitions are appropriate for general functional or input coverage.",
    )


def _fallback_strategies(coverage_items: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in coverage_items.iterrows():
        technique, reason = _fallback_strategy(row)
        rows.append(
            {
                "coverage_id": row["coverage_id"],
                "requirement_id": row.get("requirement_id", ""),
                "coverage_type": row.get("coverage_type", "Functional"),
                "risk_level": row.get("risk_level", "Medium"),
                "technique": technique,
                "technique_standard": TECHNIQUE_STANDARDS[technique],
                "strategy_reason": reason,
                "source": "Rule fallback",
            }
        )
    return pd.DataFrame(rows)


def _llm_refine_strategies(
    coverage_items: pd.DataFrame,
    strategies: pd.DataFrame,
    provider: str,
    model: str | None = None,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    coverage_records = coverage_items.to_dict("records")
    strategy_by_coverage = strategies.set_index("coverage_id").to_dict("index")

    def review_batch(_batch_index: int, batch: list[dict]) -> list[dict]:
        batch_coverage = pd.DataFrame(batch)
        batch_strategies = pd.DataFrame(
            [
                {"coverage_id": row.get("coverage_id"), **strategy_by_coverage.get(row.get("coverage_id"), {})}
                for row in batch
            ]
        )
        prompt = build_test_strategy_review_prompt(
            batch_coverage.to_string(index=False),
            batch_strategies.to_string(index=False),
        )
        parsed = call_json_completion(
            TEST_STRATEGY_REVIEW_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=max(600, 180 * len(batch)),
            task_label="Strategy Review",
        )
        return parsed.get("strategy_reviews", [])

    def fallback_batch(_batch_index: int, _batch: list[dict], _exc: Exception) -> list[dict]:
        return []

    review_batches, _ = run_parallel_batches(
        coverage_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=review_batch,
        fallback_batch=fallback_batch,
        task_label="Strategy Review",
    )
    reviews = [review for batch_reviews in review_batches for review in batch_reviews]

    refined = strategies.copy()
    for review in reviews:
        coverage_id = review.get("coverage_id")
        recommended = review.get("recommended_technique")
        if recommended not in TECHNIQUE_STANDARDS:
            continue
        mask = refined["coverage_id"] == coverage_id
        if not mask.any():
            continue
        refined.loc[mask, "technique"] = recommended
        refined.loc[mask, "technique_standard"] = TECHNIQUE_STANDARDS[recommended]
        refined.loc[mask, "strategy_reason"] = review.get("recommendation_reason", refined.loc[mask, "strategy_reason"].iloc[0])
        refined.loc[mask, "source"] = "LLM prompt review"
    return refined


def select_strategies(
    coverage_items: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    strategies = _fallback_strategies(coverage_items)
    if use_llm and provider and is_llm_enabled(provider):
        try:
            return _llm_refine_strategies(
                coverage_items,
                strategies,
                provider=provider,
                model=model,
                batch_size=batch_size,
                concurrency=concurrency,
            )
        except Exception as exc:
            strategies["llm_error"] = str(exc)
    return strategies
