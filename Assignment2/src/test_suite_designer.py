from __future__ import annotations

from typing import Any
import re

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.prompt_templates import (
    SUITE_DESIGN_IMPROVEMENT_SYSTEM,
    suite_improvement_prompt,
)


RISK_ORDER = {"High": 0, "Medium": 1, "Low": 2}
RISK_SCORE = {"High": 5.0, "Medium": 3.0, "Low": 1.0}
SUITE_COLUMNS = [
    "suite_id",
    "suite_name",
    "module",
    "risk_level",
    "priority",
    "coverage_ids",
    "techniques",
    "coverage_types",
    "suite_objective",
    "optimization_basis",
    "source",
    "llm_changes",
]

def _split_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    if ";" in text:
        return [part.strip() for part in text.split(";") if part.strip()]
    return [part.strip() for part in text.split(",") if part.strip()]


def _state_sequence_coverage_id(sequence: pd.Series | dict, offset: int) -> str:
    transition_id = str(sequence.get("transition_id", "")).strip()
    if transition_id:
        suffix = re.sub(r"[^A-Za-z0-9]+", "-", transition_id).strip("-").upper()
        return f"COV-STATE-{suffix}" if suffix else f"COV-STATE-{offset:03d}"
    return f"COV-STATE-{offset:03d}"


def _best_risk(values: list[str]) -> str:
    if not values:
        return "Medium"
    return sorted(values, key=lambda value: RISK_ORDER.get(str(value), 3))[0]


def _suite_name(module: str, technique: str, coverage_type: str) -> str:
    module_name = module or "General"
    if technique == "State Transition Testing":
        suffix = "State Behavior Suite"
    elif technique == "Decision Table Testing":
        suffix = "Decision Rule Suite"
    elif technique == "Boundary Value Analysis":
        suffix = "Boundary Suite"
    elif technique == "Equivalence Partitioning":
        suffix = "Partition Suite"
    else:
        suffix = f"{coverage_type or 'Functional'} Suite"
    return f"{module_name} {suffix}"


def _suite_objective(module: str, techniques: list[str], coverage_types: list[str]) -> str:
    technique_text = ", ".join(techniques) or "selected black-box techniques"
    coverage_text = ", ".join(coverage_types) or "functional coverage"
    return (
        f"Validate {module or 'the target module'} behavior using {technique_text} "
        f"for {coverage_text} coverage, prioritized by requirement risk and coverage value."
    )


def design_test_suites(
    structured_requirements: pd.DataFrame,
    coverage_items: pd.DataFrame,
    test_strategies: pd.DataFrame,
    risk_analysis: pd.DataFrame,
    state_transition_sequences: pd.DataFrame | None = None,
) -> pd.DataFrame:
    if coverage_items.empty and (state_transition_sequences is None or state_transition_sequences.empty):
        return pd.DataFrame(columns=SUITE_COLUMNS)

    requirements = (
        structured_requirements.set_index("requirement_id").to_dict("index")
        if not structured_requirements.empty and "requirement_id" in structured_requirements.columns
        else {}
    )
    risks = (
        risk_analysis.set_index("requirement_id").to_dict("index")
        if not risk_analysis.empty and "requirement_id" in risk_analysis.columns
        else {}
    )
    strategies = (
        test_strategies.set_index("coverage_id").to_dict("index")
        if not test_strategies.empty and "coverage_id" in test_strategies.columns
        else {}
    )

    rows = []
    for _, coverage_row in coverage_items.iterrows():
        coverage = coverage_row.to_dict()
        coverage_id = str(coverage.get("coverage_id", "")).strip()
        requirement_id = str(coverage.get("requirement_id", "")).strip()
        strategy = strategies.get(coverage_id, {})
        requirement = requirements.get(requirement_id, {})
        risk = risks.get(requirement_id, {})
        related_techniques = _split_values(coverage.get("related_techniques"))
        technique = str(
            strategy.get("technique")
            or (related_techniques[0] if related_techniques else "")
            or "Equivalence Partitioning"
        )
        module = str(requirement.get("module") or coverage.get("module") or "General").strip() or "General"
        coverage_type = str(coverage.get("coverage_type") or strategy.get("coverage_type") or "Functional").strip()
        risk_level = str(coverage.get("risk_level") or risk.get("risk_level") or "Medium")
        rows.append(
            {
                "coverage_id": coverage_id,
                "module": module,
                "technique": technique,
                "coverage_type": coverage_type,
                "risk_level": risk_level,
                "risk_score": risk.get("risk_score", RISK_SCORE.get(risk_level, 3.0)),
            }
        )

    grouped = pd.DataFrame(rows)

    suite_rows = []
    if not grouped.empty:
        for index, ((module, technique, coverage_type), group) in enumerate(
            grouped.groupby(["module", "technique", "coverage_type"], sort=True),
            start=1,
        ):
            risk_level = _best_risk([str(value) for value in group["risk_level"].tolist()])
            coverage_ids = sorted(set(group["coverage_id"].astype(str)))
            techniques = sorted(set(group["technique"].astype(str)))
            coverage_types = sorted(set(group["coverage_type"].astype(str)))
            suite_rows.append(
                {
                    "suite_id": f"TS-{len(suite_rows) + 1:03d}",
                    "suite_name": _suite_name(str(module), str(technique), str(coverage_type)),
                    "module": module,
                    "risk_level": risk_level,
                    "priority": risk_level,
                    "coverage_ids": "; ".join(coverage_ids),
                    "techniques": "; ".join(techniques),
                    "coverage_types": "; ".join(coverage_types),
                    "suite_objective": _suite_objective(str(module), techniques, coverage_types),
                    "optimization_basis": "risk-based and coverage-based prioritization",
                    "source": "Rule fallback",
                    "llm_changes": "",
                }
            )

    if state_transition_sequences is not None and not state_transition_sequences.empty:
        state_module = _state_suite_module(structured_requirements)
        coverage_goals = sorted(
            {
                str(value)
                for value in state_transition_sequences.get("coverage_goal", pd.Series(dtype=str)).dropna()
                if str(value).strip()
            }
        )
        sequence_coverage_ids = [
            _state_sequence_coverage_id(sequence, offset)
            for offset, (_, sequence) in enumerate(state_transition_sequences.iterrows(), start=1)
        ]
        transition_ids = sorted(
            {
                str(value)
                for value in state_transition_sequences.get("transition_id", pd.Series(dtype=str)).dropna()
                if str(value).strip()
            }
        )
        suite_rows.append(
            {
                "suite_id": f"TS-{len(suite_rows) + 1:03d}",
                "suite_name": "State Transition Model Suite",
                "module": state_module,
                "risk_level": "Medium",
                "priority": "Medium",
                "coverage_ids": "; ".join(sequence_coverage_ids),
                "techniques": "State Transition Testing",
                "coverage_types": "State Transition",
                "suite_objective": (
                    "Validate behavior represented by the state transition model "
                    f"using {', '.join(coverage_goals) or 'state/transition coverage'}."
                ),
                "optimization_basis": (
                    "coverage-criterion-based optimized transition sequence"
                    + (f"; transitions: {'; '.join(transition_ids)}" if transition_ids else "")
                ),
                "source": "Rule fallback - State transition model",
                "llm_changes": "",
            }
        )
    return pd.DataFrame(suite_rows, columns=SUITE_COLUMNS)


def improve_test_suites_with_llm(
    test_suites: pd.DataFrame,
    coverage_items: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> dict[str, pd.DataFrame]:
    if (
        test_suites.empty
        or not use_llm
        or not provider
        or not is_llm_enabled(provider)
    ):
        return {"test_suites": test_suites.copy(), "suite_improvement_suggestions": pd.DataFrame()}

    suite_records = test_suites.to_dict("records")
    coverage_lookup = (
        coverage_items.set_index("coverage_id").to_dict("index")
        if not coverage_items.empty and "coverage_id" in coverage_items.columns
        else {}
    )

    def improve_batch(_batch_index: int, batch: list[dict]) -> dict[str, Any]:
        return call_json_completion(
            SUITE_DESIGN_IMPROVEMENT_SYSTEM,
            suite_improvement_prompt(batch, coverage_lookup),
            provider=provider,
            model=model,
            max_tokens=max(700, 220 * len(batch) + 300),
            task_label="Test Suite Design Improvement",
        )

    def fallback_batch(_batch_index: int, _batch: list[dict], exc: Exception) -> dict[str, Any]:
        return {"suggestions": [], "llm_error": str(exc)}

    batch_results, _ = run_parallel_batches(
        suite_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=improve_batch,
        fallback_batch=fallback_batch,
        task_label="Test Suite Design Improvement",
    )
    suggestions = _parse_suite_improvements(batch_results)
    improved = _apply_suite_improvements(test_suites, suggestions)
    return {"test_suites": improved, "suite_improvement_suggestions": suggestions}


def _parse_suite_improvements(batch_results: list[dict]) -> pd.DataFrame:
    rows = []
    for parsed in batch_results:
        if parsed.get("llm_error"):
            rows.append({"suite_id": "", "action": "error", "reason": parsed.get("llm_error", "")})
            continue
        for item in parsed.get("suggestions", []):
            if not isinstance(item, dict):
                continue
            rows.append(
                {
                    "suite_id": item.get("suite_id", ""),
                    "action": item.get("action", ""),
                    "reason": item.get("reason", ""),
                    "suggested_suite_name": item.get("suggested_suite_name", ""),
                    "suggested_objective": item.get("suggested_objective", ""),
                    "suggested_optimization_basis": item.get("suggested_optimization_basis", ""),
                    "related_coverage_ids": item.get("related_coverage_ids", []),
                }
            )
    return pd.DataFrame(rows)


def _apply_suite_improvements(test_suites: pd.DataFrame, suggestions: pd.DataFrame) -> pd.DataFrame:
    if test_suites.empty or suggestions.empty or "suite_id" not in test_suites.columns:
        return test_suites.copy()
    improved = test_suites.copy()
    if "llm_changes" not in improved.columns:
        improved["llm_changes"] = ""
    valid_suite_ids = set(improved["suite_id"].astype(str))
    for _, suggestion in suggestions.iterrows():
        suite_id = str(suggestion.get("suite_id", "")).strip()
        if suite_id not in valid_suite_ids:
            continue
        mask = improved["suite_id"].astype(str) == suite_id
        name = str(suggestion.get("suggested_suite_name", "")).strip()
        objective = str(suggestion.get("suggested_objective", "")).strip()
        basis = str(suggestion.get("suggested_optimization_basis", "")).strip()
        changes: list[str] = []
        current_row = improved.loc[mask].iloc[0]
        if name:
            old_name = str(current_row.get("suite_name", "")).strip()
            improved.loc[mask, "suite_name"] = name
            if name != old_name:
                changes.append("suite_name updated")
        if objective:
            old_objective = str(current_row.get("suite_objective", "")).strip()
            improved.loc[mask, "suite_objective"] = objective
            if objective != old_objective:
                changes.append("suite_objective updated")
        if basis:
            old_basis = str(current_row.get("optimization_basis", "")).strip()
            improved.loc[mask, "optimization_basis"] = basis
            if basis != old_basis:
                changes.append("optimization_basis updated")
        if changes:
            improved.loc[mask, "source"] = "LLM updated"
            improved.loc[mask, "llm_changes"] = "; ".join(changes)
    return improved


def assign_test_suites_to_cases(test_cases: pd.DataFrame, test_suites: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases.copy()
    assigned = test_cases.copy()
    for column in ["suite_id", "suite_name", "suite_risk_level", "suite_priority"]:
        if column not in assigned.columns:
            assigned[column] = ""
    if test_suites.empty or "coverage_ids" not in test_suites.columns:
        return assigned

    coverage_to_suite: dict[str, dict[str, str]] = {}
    for _, suite in test_suites.iterrows():
        for coverage_id in _split_values(suite.get("coverage_ids", "")):
            coverage_to_suite[str(coverage_id)] = {
                "suite_id": str(suite.get("suite_id", "")),
                "suite_name": str(suite.get("suite_name", "")),
                "suite_risk_level": str(suite.get("risk_level", "")),
                "suite_priority": str(suite.get("priority", "")),
            }

    for index, row in assigned.iterrows():
        suite = coverage_to_suite.get(str(row.get("coverage_id", "")))
        if not suite:
            continue
        for column, value in suite.items():
            assigned.at[index, column] = value
    return assigned


def _state_suite_module(structured_requirements: pd.DataFrame) -> str:
    if structured_requirements.empty or "module" not in structured_requirements.columns:
        return "Cross-module behavior"
    modules = sorted(
        {
            str(value).strip()
            for value in structured_requirements["module"].dropna()
            if str(value).strip()
        }
    )
    if not modules:
        return "Cross-module behavior"
    if len(modules) == 1:
        return modules[0]
    return "Cross-module behavior"

