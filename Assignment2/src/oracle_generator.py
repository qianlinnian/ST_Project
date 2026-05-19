from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.prompt_templates import ORACLE_REVIEW_SYSTEM, oracle_review_prompt


def _normalise(value: Any) -> str:
    return str(value or "").strip().lower()


def generate_expected_result(
    requirement_text: str = "",
    test_data: str = "",
    technique: str = "",
    action: str = "",
    expected_hint: str = "",
) -> str:
    hint = str(expected_hint or "").strip()
    if hint:
        return hint

    combined = " ".join(
        [
            _normalise(requirement_text),
            _normalise(test_data),
            _normalise(technique),
            _normalise(action),
        ]
    )

    if any(keyword in combined for keyword in ["invalid", "empty", "blank", "below minimum", "above maximum", "outside"]):
        return "The system rejects or safely handles the invalid input; no invalid state or invalid data is committed."

    if "boundary" in combined or "limit" in combined or "threshold" in combined:
        return "The observable result is consistent with the specified boundary rule for the selected boundary value."

    if "decision table" in combined or "condition" in combined or "combination" in combined:
        return "The observable result matches the expected action for the specified condition combination."

    if "state transition" in combined or "source state" in combined or "target state" in combined:
        return "The system reaches the expected target state after the event, or rejects an invalid transition without corrupting state."

    if "valid" in combined or "equivalence" in combined:
        return "The system accepts the representative valid input or behaviour and produces the requirement-consistent observable output."

    return f"The observable result satisfies the requirement under the specified test data: {requirement_text}"


def improve_oracles_with_llm(
    test_cases: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    if test_cases.empty or not use_llm or not provider or not is_llm_enabled(provider):
        return test_cases.copy()

    improved = test_cases.copy()

    def review_batch(_batch_index: int, batch: list[dict]) -> list[dict]:
        prompt = oracle_review_prompt(pd.DataFrame(batch).to_string(index=False))
        parsed = call_json_completion(
            ORACLE_REVIEW_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=max(800, 180 * len(batch)),
        )
        return parsed.get("oracle_reviews", [])

    def fallback_batch(_batch_index: int, batch: list[dict], exc: Exception) -> list[dict]:
        return [
            {
                "test_case_id": row.get("test_case_id", ""),
                "improved_expected_result": "",
                "reason": f"LLM oracle review failed: {exc}",
            }
            for row in batch
        ]

    review_batches, _ = run_parallel_batches(
        improved.to_dict("records"),
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=review_batch,
        fallback_batch=fallback_batch,
    )

    for review in [item for batch in review_batches for item in batch]:
        test_case_id = review.get("test_case_id")
        improved_result = review.get("improved_expected_result")
        if not test_case_id or not improved_result:
            continue
        mask = improved["test_case_id"] == test_case_id
        if mask.any():
            improved.loc[mask, "expected_result"] = improved_result
            improved.loc[mask, "oracle_source"] = "LLM prompt review"
    return improved
