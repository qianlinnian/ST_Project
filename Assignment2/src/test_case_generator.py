from __future__ import annotations

import re
from typing import Any

import pandas as pd

from src.ai_client import is_llm_enabled
from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.oracle_generator import generate_expected_result, improve_oracles_with_llm
from src.prompt_templates import (
    COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM,
    TEST_CASE_GENERATION_SYSTEM,
    test_case_generation_prompt as build_test_case_generation_prompt,
)
from src.state_modeler import infer_state_model_from_requirements, generate_state_transition_tests
from src.test_strategy_selector import TECHNIQUE_STANDARDS

PRIORITY_BY_RISK = {"High": "High", "Medium": "Medium", "Low": "Low"}
RISK_SCORE_BY_LEVEL = {"High": 5.0, "Medium": 3.0, "Low": 1.0}
REQUIRED_COLUMNS = [
    "test_case_id", "requirement_id", "coverage_id", "technique", "technique_standard",
    "precondition", "test_data", "steps", "expected_result", "priority", "risk_score",
    "risk_level", "coverage_type", "automation_candidate", "source", "design_basis",
]


def _as_text(value: Any) -> str:
    return ", ".join(str(item) for item in value) if isinstance(value, list) else str(value or "")


def _find_requirement(requirements: pd.DataFrame, requirement_id: str) -> dict:
    if requirements.empty or "requirement_id" not in requirements.columns:
        return {}
    matches = requirements[requirements["requirement_id"] == requirement_id]
    return {} if matches.empty else matches.iloc[0].to_dict()


def _bounds(*texts: str) -> tuple[int | None, int | None]:
    combined = " ".join(texts).lower()
    match = re.search(r"(\d+)\s*(?:-|to|~|–)\s*(\d+)", combined)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        return min(a, b), max(a, b)
    min_value = max_value = None
    for number in [int(value) for value in re.findall(r"\b\d+\b", combined)]:
        pos = combined.find(str(number))
        local = combined[max(0, pos - 30): pos + 40]
        if any(k in local for k in ["min", "minimum", "least", "lower"]):
            min_value = number
        if any(k in local for k in ["max", "maximum", "limit", "upper", "no more"]):
            max_value = number
    return min_value, max_value


def _hint(req: dict) -> str:
    expected = req.get("expected_results", "")
    return str(expected[0]) if isinstance(expected, list) and expected else str(expected or "")


def _case(idx: int, req_id: str, cov_id: str, tech: str, cov: dict, req: dict, data: str, steps: str,
          expected: str | None = None, source: str = "Rule fallback", basis: str = "") -> dict:
    risk = str(cov.get("risk_level") or "Medium")
    req_text = _as_text(req.get("requirement_text", ""))
    cov_text = _as_text(cov.get("description", ""))
    return {
        "test_case_id": f"TC-{idx:03d}",
        "requirement_id": req_id,
        "coverage_id": cov_id,
        "technique": tech,
        "technique_standard": TECHNIQUE_STANDARDS.get(tech, "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4"),
        "precondition": "The system under test is available and the relevant feature can be exercised.",
        "test_data": data,
        "steps": steps,
        "expected_result": expected or generate_expected_result(req_text, data, tech, cov_text, _hint(req)),
        "priority": PRIORITY_BY_RISK.get(risk, "Medium"),
        "risk_score": RISK_SCORE_BY_LEVEL.get(risk, 3.0),
        "risk_level": risk,
        "coverage_type": cov.get("coverage_type", "Functional"),
        "automation_candidate": "Partial",
        "source": source,
        "design_basis": basis or cov_text or req_text,
    }


def _ep(start: int, req_id: str, cov_id: str, cov: dict, req: dict) -> list[dict]:
    basis = _as_text(cov.get("description", "")) or _as_text(req.get("requirement_text", ""))
    return [
        _case(start, req_id, cov_id, "Equivalence Partitioning", cov, req,
              "Representative valid partition data derived from the requirement",
              "1. Prepare representative valid data\n2. Execute the related action\n3. Observe the system response",
              source="Rule fallback - EP valid partition", basis=f"Valid equivalence partition for: {basis}"),
        _case(start + 1, req_id, cov_id, "Equivalence Partitioning", cov, req,
              "Representative invalid partition data derived from the requirement",
              "1. Prepare representative invalid data\n2. Execute the related action\n3. Observe validation, rejection, or safe handling",
              source="Rule fallback - EP invalid partition", basis=f"Invalid equivalence partition for: {basis}"),
    ]


def _bva(start: int, req_id: str, cov_id: str, cov: dict, req: dict) -> list[dict]:
    lo, hi = _bounds(_as_text(req.get("requirement_text", "")), _as_text(req.get("data_ranges", "")), _as_text(cov.get("description", "")))
    values = []
    values += [(str(max(lo - 1, 0)), "just below minimum"), (str(lo), "on minimum"), (str(lo + 1), "just above minimum")] if lo is not None else [("below lower boundary", "generic lower invalid boundary"), ("on lower boundary", "generic lower valid boundary")]
    values += [(str(max(hi - 1, 0)), "just below maximum"), (str(hi), "on maximum"), (str(hi + 1), "just above maximum")] if hi is not None else [("above upper boundary", "generic upper boundary review")]
    rows, seen = [], set()
    for value, label in values:
        if (value, label) in seen:
            continue
        seen.add((value, label))
        rows.append(_case(start + len(rows), req_id, cov_id, "Boundary Value Analysis", cov, req,
                          f"Boundary value: {value} ({label})",
                          "1. Prepare data at the boundary point\n2. Execute the related action\n3. Verify the boundary rule",
                          source="Rule fallback - BVA",
                          basis="Values are selected on and around identifiable or inferred boundaries."))
    return rows


def _decision(start: int, req_id: str, cov_id: str, cov: dict, req: dict) -> list[dict]:
    rules = [
        ("All required conditions are true", "The permitted action is completed successfully."),
        ("At least one required condition is false", "The action is rejected or the alternative specified outcome occurs."),
        ("Invalid or conflicting condition combination", "The system handles the combination safely and consistently."),
    ]
    return [_case(start + i, req_id, cov_id, "Decision Table Testing", cov, req,
                  f"Rule {i + 1}: {cond}",
                  "1. Establish the condition combination\n2. Execute the action\n3. Verify the expected outcome",
                  expected=exp, source="Rule fallback - Decision Table",
                  basis=f"Decision rule based on requirement conditions: {cond}") for i, (cond, exp) in enumerate(rules)]


def _state(start: int, req_id: str, cov_id: str, cov: dict, state_model: dict) -> list[dict]:
    rows = generate_state_transition_tests(req_id, cov_id, start, state_model=state_model).to_dict("records")
    for row in rows:
        risk = cov.get("risk_level", row.get("risk_level", "Medium"))
        row.update({"coverage_type": cov.get("coverage_type", "State Transition"), "risk_level": risk,
                    "priority": PRIORITY_BY_RISK.get(risk, row.get("priority", "High")),
                    "risk_score": RISK_SCORE_BY_LEVEL.get(risk, row.get("risk_score", 3.0))})
    return rows


def _fallback(requirements: pd.DataFrame, coverage: pd.DataFrame, strategies: pd.DataFrame, include_state: bool) -> pd.DataFrame:
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}
    state_model = infer_state_model_from_requirements(requirements)
    rows, counter = [], 1
    for _, cov_row in coverage.iterrows():
        cov = cov_row.to_dict()
        req_id, cov_id = cov.get("requirement_id", ""), cov.get("coverage_id", "")
        req = _find_requirement(requirements, req_id)
        tech = strategy_map.get(cov_id, {}).get("technique", "Equivalence Partitioning")
        generated = _bva(counter, req_id, cov_id, cov, req) if tech == "Boundary Value Analysis" else _decision(counter, req_id, cov_id, cov, req) if tech == "Decision Table Testing" else _state(counter, req_id, cov_id, cov, state_model) if tech == "State Transition Testing" else _ep(counter, req_id, cov_id, cov, req)
        rows.extend(generated)
        counter += len(generated)
    if include_state and not any(r.get("technique") == "State Transition Testing" for r in rows):
        rows.extend(generate_state_transition_tests(start_index=counter, state_model=state_model).to_dict("records"))
    return pd.DataFrame(rows, columns=REQUIRED_COLUMNS)


def _normalise_test_case_frame(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    for col in REQUIRED_COLUMNS:
        if col not in data.columns:
            data[col] = ""
    extra_columns = [col for col in data.columns if col not in REQUIRED_COLUMNS]
    return data[REQUIRED_COLUMNS + extra_columns]


def _renumber_test_cases(test_cases: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases
    renumbered = test_cases.copy()
    renumbered["test_case_id"] = [f"TC-{index:03d}" for index in range(1, len(renumbered) + 1)]
    return renumbered


def _llm_generate(
    requirements: pd.DataFrame,
    coverage: pd.DataFrame,
    strategies: pd.DataFrame,
    provider: str,
    model: str | None,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    coverage_records = coverage.to_dict("records")
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}

    def generate_batch(_batch_index: int, batch: list[dict]) -> pd.DataFrame:
        batch_coverage = pd.DataFrame(batch)
        requirement_ids = {
            str(row.get("requirement_id", ""))
            for row in batch
            if str(row.get("requirement_id", "")).strip()
        }
        batch_requirements = requirements[
            requirements["requirement_id"].astype(str).isin(requirement_ids)
        ] if "requirement_id" in requirements.columns else requirements
        batch_strategies = pd.DataFrame(
            [
                {"coverage_id": row.get("coverage_id"), **strategy_map.get(row.get("coverage_id"), {})}
                for row in batch
            ]
        )
        prompt = build_test_case_generation_prompt(
            batch_requirements.to_string(index=False),
            batch_coverage.to_string(index=False),
            batch_strategies.to_string(index=False),
        )
        parsed = call_json_completion(
            TEST_CASE_GENERATION_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=max(1200, 450 * len(batch)),
        )
        data = _normalise_test_case_frame(pd.DataFrame(parsed.get("test_cases", [])))
        if data.empty:
            raise ValueError("LLM returned no test_cases")
        return data

    def fallback_batch(_batch_index: int, batch: list[dict], exc: Exception) -> pd.DataFrame:
        batch_coverage = pd.DataFrame(batch)
        batch_cases = _fallback(requirements, batch_coverage, strategies, include_state=False)
        batch_cases["llm_error"] = str(exc)
        batch_cases["source"] = batch_cases["source"].astype(str) + " after LLM batch fallback"
        return batch_cases

    generated_batches, _ = run_parallel_batches(
        coverage_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=generate_batch,
        fallback_batch=fallback_batch,
    )
    data = pd.concat(generated_batches, ignore_index=True) if generated_batches else pd.DataFrame()
    data = _normalise_test_case_frame(data)
    if data.empty:
        raise ValueError("LLM returned no test_cases")
    return _renumber_test_cases(data)


def suggest_missing_test_cases_with_llm(
    requirements: pd.DataFrame,
    coverage: pd.DataFrame,
    strategies: pd.DataFrame,
    existing_test_cases: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    if (
        coverage.empty
        or existing_test_cases.empty
        or not use_llm
        or not provider
        or not is_llm_enabled(provider)
    ):
        return pd.DataFrame(columns=REQUIRED_COLUMNS + ["llm_reason"])

    coverage_records = coverage.to_dict("records")
    strategy_map = strategies.set_index("coverage_id").to_dict("index") if not strategies.empty else {}

    def review_batch(_batch_index: int, batch: list[dict]) -> pd.DataFrame:
        prompt = _missing_test_case_prompt(batch, requirements, strategy_map, existing_test_cases)
        parsed = call_json_completion(
            COMPACT_TEST_CASE_IMPROVEMENT_SYSTEM,
            prompt,
            provider=provider,
            model=model,
            max_tokens=max(600, 90 * len(batch) + 300),
        )
        return _parse_missing_test_cases(parsed, len(batch))

    def fallback_batch(_batch_index: int, _batch: list[dict], exc: Exception) -> pd.DataFrame:
        return pd.DataFrame([{"llm_error": str(exc)}])

    suggested_batches, _ = run_parallel_batches(
        coverage_records,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=review_batch,
        fallback_batch=fallback_batch,
    )
    data = pd.concat(suggested_batches, ignore_index=True) if suggested_batches else pd.DataFrame()
    if data.empty:
        return pd.DataFrame(columns=REQUIRED_COLUMNS + ["llm_reason"])
    for col in REQUIRED_COLUMNS:
        if col not in data.columns:
            data[col] = ""
    return data[REQUIRED_COLUMNS + [col for col in data.columns if col not in REQUIRED_COLUMNS]]


def _missing_test_case_prompt(
    coverage_batch: list[dict],
    requirements: pd.DataFrame,
    strategy_map: dict,
    existing_test_cases: pd.DataFrame,
) -> str:
    requirement_ids = {
        str(row.get("requirement_id", "")).strip()
        for row in coverage_batch
        if str(row.get("requirement_id", "")).strip()
    }
    coverage_ids = {
        str(row.get("coverage_id", "")).strip()
        for row in coverage_batch
        if str(row.get("coverage_id", "")).strip()
    }
    req_rows = requirements[
        requirements["requirement_id"].astype(str).isin(requirement_ids)
    ] if "requirement_id" in requirements.columns else requirements
    case_rows = existing_test_cases[
        existing_test_cases["coverage_id"].astype(str).isin(coverage_ids)
    ] if "coverage_id" in existing_test_cases.columns else existing_test_cases

    lines = ["REQ|id|text"]
    for _, row in req_rows.iterrows():
        lines.append(f"REQ|{_compact_text(row.get('requirement_id', ''), 60)}|{_compact_text(row.get('requirement_text', ''), 260)}")

    lines.append("COV|id|req|type|desc|tech|risk")
    for row in coverage_batch:
        cov_id = str(row.get("coverage_id", ""))
        strategy = strategy_map.get(cov_id, {})
        technique = strategy.get("technique", row.get("related_techniques", ""))
        lines.append(
            "|".join(
                [
                    "COV",
                    _compact_text(cov_id, 60),
                    _compact_text(row.get("requirement_id", ""), 60),
                    _compact_text(row.get("coverage_type", ""), 60),
                    _compact_text(row.get("description", ""), 180),
                    _compact_text(technique, 80),
                    _compact_text(row.get("risk_level", "Medium"), 40),
                ]
            )
        )

    lines.append("EXISTING|id|cov|tech|data|expected")
    for _, row in case_rows.iterrows():
        lines.append(
            "|".join(
                [
                    "EXISTING",
                    _compact_text(row.get("test_case_id", ""), 40),
                    _compact_text(row.get("coverage_id", ""), 60),
                    _compact_text(row.get("technique", ""), 80),
                    _compact_text(row.get("test_data", ""), 140),
                    _compact_text(row.get("expected_result", ""), 180),
                ]
            )
        )
    return "\n".join(lines)


def _parse_missing_test_cases(parsed: dict, batch_size: int) -> pd.DataFrame:
    rows = []
    if isinstance(parsed.get("m"), list):
        for index, item in enumerate(parsed.get("m", []), start=1):
            if not isinstance(item, list) or len(item) < 6:
                continue
            risk_level = str(item[7] if len(item) > 7 else "Medium")
            rows.append(
                {
                    "test_case_id": f"TC-AI-{index:03d}",
                    "requirement_id": item[0],
                    "coverage_id": item[1],
                    "technique": item[2],
                    "technique_standard": TECHNIQUE_STANDARDS.get(str(item[2]), "ISTQB Foundation Level / ISO/IEC/IEEE 29119-4"),
                    "precondition": "The system under test is available and the relevant feature can be exercised.",
                    "test_data": item[3],
                    "steps": item[4],
                    "expected_result": item[5],
                    "priority": item[6] if len(item) > 6 else risk_level,
                    "risk_score": RISK_SCORE_BY_LEVEL.get(risk_level, 3.0),
                    "risk_level": risk_level,
                    "coverage_type": "",
                    "automation_candidate": "Partial",
                    "source": "LLM missing test case suggestion",
                    "design_basis": "LLM identified missing coverage in existing test cases.",
                    "llm_reason": item[8] if len(item) > 8 else "",
                }
            )
    return pd.DataFrame(rows)


def renumber_test_case_ids(test_cases: pd.DataFrame, prefix: str = "TC") -> pd.DataFrame:
    if test_cases.empty:
        return test_cases.copy()
    renumbered = test_cases.copy()
    renumbered["test_case_id"] = [
        f"{prefix}-{index:03d}" for index in range(1, len(renumbered) + 1)
    ]
    return renumbered


def _compact_text(value, limit: int) -> str:
    text = " ".join(str(value or "").split())
    if len(text) > limit:
        text = text[:limit]
    return text


def generate_test_cases(requirements: pd.DataFrame, coverage: pd.DataFrame, strategies: pd.DataFrame,
                        include_state_tests: bool = True, provider: str | None = None,
                        model: str | None = None, use_llm: bool = True,
                        batch_size: int | None = None,
                        concurrency: int | None = None) -> pd.DataFrame:
    if use_llm and provider and is_llm_enabled(provider):
        try:
            generated = _llm_generate(
                requirements,
                coverage,
                strategies,
                provider,
                model,
                batch_size=batch_size,
                concurrency=concurrency,
            )
            return improve_oracles_with_llm(
                generated,
                provider=provider,
                model=model,
                use_llm=True,
                batch_size=batch_size,
                concurrency=concurrency,
            )
        except Exception as exc:
            fallback = _fallback(requirements, coverage, strategies, include_state_tests)
            fallback["llm_error"] = str(exc)
            fallback["source"] = fallback["source"].astype(str) + " after LLM fallback"
            return fallback
    return _fallback(requirements, coverage, strategies, include_state_tests)
