from __future__ import annotations

import json
from typing import Any

import pandas as pd

from src.ai_client import chat_completion, is_llm_enabled
from src.prompt_templates import TEST_STRATEGY_REVIEW_SYSTEM, test_strategy_review_prompt


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


def _clean_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())


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
) -> pd.DataFrame:
    prompt = test_strategy_review_prompt(
        coverage_items.to_string(index=False),
        strategies.to_string(index=False),
    )
    response = chat_completion(TEST_STRATEGY_REVIEW_SYSTEM, prompt, provider=provider, model=model)
    parsed = _clean_json(response)
    reviews = parsed.get("strategy_reviews", [])
    if not reviews:
        return strategies

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
) -> pd.DataFrame:
    strategies = _fallback_strategies(coverage_items)
    if use_llm and provider and is_llm_enabled(provider):
        try:
            return _llm_refine_strategies(coverage_items, strategies, provider=provider, model=model)
        except Exception as exc:
            strategies["llm_error"] = str(exc)
    return strategies
