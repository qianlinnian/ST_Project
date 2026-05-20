from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.prompt_templates import (
    COMPACT_COVERAGE_IMPROVEMENT_SYSTEM,
    SUITE_OPTIMIZATION_REVIEW_SYSTEM,
    suite_optimization_review_prompt,
)
from src.suite_optimizer import optimize_suite
from src.test_case_generator import (
    renumber_test_case_ids,
    suggest_missing_test_cases_with_llm,
)
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

    requirement_records = requirements.to_dict("records")
    if not requirement_records:
        return pd.DataFrame(columns=coverage_items.columns.tolist() + ["reason"])

    def review_batch(_batch_index: int, batch: list[dict]) -> dict[str, Any]:
        batch_requirements = pd.DataFrame(batch)
        requirement_ids = {
            str(row.get("requirement_id", "")).strip()
            for row in batch
            if str(row.get("requirement_id", "")).strip()
        }
        if "requirement_id" in coverage_items.columns:
            batch_coverage = coverage_items[
                coverage_items["requirement_id"].astype(str).isin(requirement_ids)
            ]
        else:
            batch_coverage = coverage_items

        prompt = _compact_coverage_improvement_prompt(batch_requirements, batch_coverage)
        parsed = call_json_completion(
            COMPACT_COVERAGE_IMPROVEMENT_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=min(4096, max(900, len(batch) * 100 + 500)),
        )
        return parsed

    def fallback_batch(_batch_index: int, _batch: list[dict], exc: Exception) -> dict[str, Any]:
        return {
            "missing_coverage_items": [],
            "review_summary": f"LLM coverage review batch failed: {exc}",
            "llm_error": str(exc),
        }

    batch_results, _ = run_parallel_batches(
        requirement_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=review_batch,
        fallback_batch=fallback_batch,
    )

    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    errors = []
    for parsed in batch_results:
        if parsed.get("llm_error"):
            errors.append(str(parsed["llm_error"]))
        missing_items = _parse_missing_coverage_items(parsed)
        for item in missing_items:
            key = (
                str(item.get("requirement_id", "")),
                str(item.get("coverage_type", "Functional")),
                str(item.get("description", "")),
            )
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                {
                    "coverage_id": _next_coverage_id(coverage_items, len(rows) + 1),
                    "requirement_id": item.get("requirement_id", ""),
                    "description": item.get("description", ""),
                    "coverage_type": item.get("coverage_type", "Functional"),
                    "risk_level": item.get("risk_level", "Medium"),
                    "related_techniques": item.get("related_techniques", []),
                    "tags": ["llm-suggested"],
                    "notes": item.get("review_summary", parsed.get("s", "")),
                    "reason": item.get("reason", ""),
                }
            )
    if not rows and errors:
        return pd.DataFrame([{"llm_error": "; ".join(errors)}])
    return pd.DataFrame(rows)


def _compact_coverage_improvement_prompt(
    requirements: pd.DataFrame, coverage_items: pd.DataFrame
) -> str:
    lines = ["REQ|id|text|risk"]
    risk_by_req = {}
    if "requirement_id" in coverage_items.columns and "risk_level" in coverage_items.columns:
        risk_by_req = coverage_items.groupby("requirement_id")["risk_level"].first().to_dict()

    for _, row in requirements.iterrows():
        req_id = str(row.get("requirement_id", "")).strip()
        text = _compact_text(row.get("requirement_text", ""), 280)
        risk = str(risk_by_req.get(req_id, row.get("risk_level", "Medium")))
        lines.append(f"REQ|{req_id}|{text}|{risk}")

    lines.append("COV|id|req|type|desc|tech")
    for _, row in coverage_items.iterrows():
        coverage_id = str(row.get("coverage_id", "")).strip()
        req_id = str(row.get("requirement_id", "")).strip()
        coverage_type = str(row.get("coverage_type", "Functional")).strip()
        desc = _compact_text(row.get("description", ""), 180)
        tech = _compact_text(row.get("related_techniques", ""), 120)
        lines.append(f"COV|{coverage_id}|{req_id}|{coverage_type}|{desc}|{tech}")

    return "\n".join(lines)


def _compact_text(value, limit: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) > limit:
        text = text[:limit]
    return text


def _parse_missing_coverage_items(parsed: dict) -> list[dict[str, Any]]:
    if isinstance(parsed.get("m"), list):
        items = []
        for item in parsed.get("m", []):
            if not isinstance(item, list) or len(item) < 3:
                continue
            items.append(
                {
                    "requirement_id": item[0],
                    "coverage_type": item[1] if len(item) > 1 else "Functional",
                    "description": item[2] if len(item) > 2 else "",
                    "related_techniques": item[3] if len(item) > 3 else [],
                    "reason": item[4] if len(item) > 4 else "",
                    "review_summary": parsed.get("s", ""),
                }
            )
        return items

    items = []
    for item in parsed.get("missing_coverage_items", []):
        if isinstance(item, dict):
            copied = dict(item)
            copied["review_summary"] = parsed.get("review_summary", "")
            items.append(copied)
    return items


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
    strategies: pd.DataFrame,
    existing_test_cases: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> dict[str, pd.DataFrame]:
    missing_cases = suggest_missing_test_cases_with_llm(
        requirements,
        coverage_items,
        strategies,
        existing_test_cases,
        provider,
        model,
        use_llm,
        batch_size=batch_size,
        concurrency=concurrency,
    )
    if missing_cases.empty or "llm_error" in missing_cases.columns:
        enhanced_cases = existing_test_cases.copy()
    else:
        base_columns = list(existing_test_cases.columns)
        additions = missing_cases.copy()
        for column in base_columns:
            if column not in additions.columns:
                additions[column] = ""
        additions = additions[base_columns + [col for col in additions.columns if col not in base_columns]]
        enhanced_cases = pd.concat([existing_test_cases, additions], ignore_index=True)
        enhanced_cases = renumber_test_case_ids(enhanced_cases)

    optimized_cases = optimize_suite(enhanced_cases)
    return {
        "missing_test_cases": missing_cases,
        "enhanced_test_cases": enhanced_cases,
        "optimized_test_cases": optimized_cases,
    }
