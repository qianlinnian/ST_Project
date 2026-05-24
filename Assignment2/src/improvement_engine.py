from __future__ import annotations

from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.prompt_templates import (
    COMPACT_COVERAGE_IMPROVEMENT_SYSTEM,
    COMPACT_SUITE_MINIMIZATION_SYSTEM,
    SUITE_OPTIMIZATION_REVIEW_SYSTEM,
    compact_coverage_improvement_prompt,
    compact_suite_minimization_prompt,
    suite_optimization_review_prompt,
)
from src.suite_optimizer import optimize_suite
from src.test_suite_designer import assign_test_suites_to_cases
from src.test_case_generator import (
    limit_generated_test_case_volume,
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

        prompt = compact_coverage_improvement_prompt(batch_requirements, batch_coverage)
        parsed = call_json_completion(
            COMPACT_COVERAGE_IMPROVEMENT_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=min(4096, max(900, len(batch) * 100 + 500)),
            task_label="Coverage Improvement",
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
        task_label="Coverage Improvement",
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
            task_label="Suite Optimization Review",
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


def improve_optimized_suite_with_llm(
    optimized_test_cases: pd.DataFrame,
    test_suites: pd.DataFrame | None = None,
    coverage_items: pd.DataFrame | None = None,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> dict[str, pd.DataFrame]:
    if (
        optimized_test_cases.empty
        or not use_llm
        or not provider
        or not is_llm_enabled(provider)
    ):
        return {
            "optimized_test_cases": optimized_test_cases.copy(),
            "suite_minimization_decisions": pd.DataFrame(),
        }

    local_suite = optimize_suite(optimized_test_cases)
    suite_batches = _suite_minimization_groups(local_suite, test_suites, coverage_items)

    def review_batch(_batch_index: int, batch: list[dict]) -> dict[str, Any]:
        suite_payload = batch[0]
        parsed = call_json_completion(
            COMPACT_SUITE_MINIMIZATION_SYSTEM,
            compact_suite_minimization_prompt(suite_payload),
            provider=provider,
            model=model,
            max_tokens=max(700, 80 * len(suite_payload.get("test_cases", [])) + 300),
            task_label="Suite LLM Minimization",
        )
        return parsed

    def fallback_batch(_batch_index: int, _batch: list[dict], exc: Exception) -> dict[str, Any]:
        return {"keep": [], "drop": [], "llm_error": str(exc)}

    batch_results, _ = run_parallel_batches(
        suite_batches,
        batch_size=1,
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=review_batch,
        fallback_batch=fallback_batch,
        task_label="Suite LLM Minimization",
    )

    decisions = _parse_suite_minimization_decisions(batch_results)
    minimized = _apply_suite_minimization(local_suite, decisions)
    decisions = _annotate_suite_minimization_decisions(decisions, local_suite, minimized)
    return {
        "optimized_test_cases": minimized,
        "suite_minimization_decisions": decisions,
    }


def _suite_minimization_groups(
    test_cases: pd.DataFrame,
    test_suites: pd.DataFrame | None = None,
    coverage_items: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    if test_cases.empty:
        return []
    suite_lookup = (
        test_suites.set_index("suite_id").to_dict("index")
        if test_suites is not None and not test_suites.empty and "suite_id" in test_suites.columns
        else {}
    )
    coverage_lookup = (
        coverage_items.set_index("coverage_id").to_dict("index")
        if coverage_items is not None and not coverage_items.empty and "coverage_id" in coverage_items.columns
        else {}
    )
    group_column = "suite_id" if "suite_id" in test_cases.columns and test_cases["suite_id"].astype(str).str.strip().any() else None
    groups = test_cases.groupby(group_column, sort=False) if group_column else [("UNASSIGNED", test_cases)]
    payloads = []
    for suite_id, group in groups:
        suite_id = str(suite_id)
        suite = suite_lookup.get(suite_id, {})
        coverage_ids = sorted(set(group.get("coverage_id", pd.Series(dtype=str)).astype(str)))
        payloads.append(
            {
                "suite_id": suite_id,
                "suite_name": suite.get("suite_name", group.iloc[0].get("suite_name", "") if "suite_name" in group.columns else ""),
                "suite_objective": suite.get("suite_objective", ""),
                "suite_risk_level": suite.get("risk_level", group.iloc[0].get("suite_risk_level", "") if "suite_risk_level" in group.columns else ""),
                "coverage_items": [
                    {"coverage_id": coverage_id, **coverage_lookup.get(coverage_id, {})}
                    for coverage_id in coverage_ids
                ],
                "test_cases": group.to_dict("records"),
            }
        )
    return payloads


def _parse_suite_minimization_decisions(batch_results: list[dict]) -> pd.DataFrame:
    rows = []
    for parsed in batch_results:
        if parsed.get("llm_error"):
            rows.append(
                {
                    "test_case_id": "",
                    "decision": "error",
                    "reason": parsed.get("llm_error", ""),
                }
            )
            continue
        for test_case_id in parsed.get("keep", []):
            rows.append(
                {
                    "test_case_id": test_case_id,
                    "decision": "keep",
                    "reason": "LLM marked as useful",
                }
            )
        for item in parsed.get("drop", []):
            if isinstance(item, list) and item:
                rows.append(
                    {
                        "test_case_id": item[0],
                        "decision": "drop",
                        "reason": item[1] if len(item) > 1 else "",
                    }
                )
    return pd.DataFrame(rows)


def _apply_suite_minimization(
    optimized_test_cases: pd.DataFrame, decisions: pd.DataFrame
) -> pd.DataFrame:
    if optimized_test_cases.empty or decisions.empty:
        return optimized_test_cases.copy()

    drop_ids = {
        str(row.get("test_case_id", ""))
        for _, row in decisions.iterrows()
        if row.get("decision") == "drop" and str(row.get("test_case_id", "")).strip()
    }
    if not drop_ids:
        return optimized_test_cases.copy()

    protected_ids = _protected_test_case_ids(optimized_test_cases)
    safe_drop_ids = drop_ids - protected_ids
    minimized = optimized_test_cases[
        ~optimized_test_cases["test_case_id"].astype(str).isin(safe_drop_ids)
    ].copy()
    if "suite_id" in optimized_test_cases.columns and "suite_id" in minimized.columns:
        missing_suite_ids = set(optimized_test_cases["suite_id"].astype(str)) - set(minimized["suite_id"].astype(str))
        if missing_suite_ids:
            rescue = optimized_test_cases[
                optimized_test_cases["suite_id"].astype(str).isin(missing_suite_ids)
            ].groupby("suite_id", sort=False).head(1)
            minimized = pd.concat([minimized, rescue], ignore_index=True)
    return optimize_suite(minimized)


def _annotate_suite_minimization_decisions(
    decisions: pd.DataFrame,
    before: pd.DataFrame,
    after: pd.DataFrame,
) -> pd.DataFrame:
    if decisions.empty:
        return decisions
    annotated = decisions.copy()
    before_ids = set(before.get("test_case_id", pd.Series(dtype=str)).astype(str))
    after_ids = set(after.get("test_case_id", pd.Series(dtype=str)).astype(str))

    def status(row: pd.Series) -> str:
        test_case_id = str(row.get("test_case_id", "")).strip()
        if row.get("decision") == "error":
            return "error"
        if not test_case_id or test_case_id not in before_ids:
            return "not_found"
        if row.get("decision") == "drop":
            return "applied" if test_case_id not in after_ids else "protected"
        return "kept"

    annotated["status"] = annotated.apply(status, axis=1)
    return annotated


def _protected_test_case_ids(test_cases: pd.DataFrame) -> set[str]:
    protected = set()
    if test_cases.empty or "test_case_id" not in test_cases.columns:
        return protected
    if "risk_level" in test_cases.columns:
        protected.update(
            test_cases[test_cases["risk_level"] == "High"]["test_case_id"].astype(str)
        )
    if "priority" in test_cases.columns:
        protected.update(
            test_cases[test_cases["priority"] == "High"]["test_case_id"].astype(str)
        )
    if "coverage_id" in test_cases.columns:
        coverage_counts = test_cases.groupby("coverage_id")["test_case_id"].transform("count")
        protected.update(test_cases[coverage_counts <= 1]["test_case_id"].astype(str))
    return protected


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
    test_suites: pd.DataFrame | None = None,
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
        enhanced_cases = renumber_test_case_ids(limit_generated_test_case_volume(enhanced_cases))
    if test_suites is not None:
        enhanced_cases = assign_test_suites_to_cases(enhanced_cases, test_suites)

    optimized_cases = optimize_suite(enhanced_cases)
    return {
        "missing_test_cases": missing_cases,
        "enhanced_test_cases": enhanced_cases,
        "optimized_test_cases": optimized_cases,
    }
