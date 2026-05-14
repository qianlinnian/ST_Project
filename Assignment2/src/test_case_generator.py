from __future__ import annotations

import json
import re
from typing import Any

import pandas as pd

from src.ai_client import chat_completion, is_llm_enabled
from src.oracle_generator import generate_expected_result, improve_oracles_with_llm
from src.prompt_templates import TEST_CASE_IMPROVEMENT_SYSTEM, test_case_generation_prompt, test_case_improvement_prompt
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


def _clean_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())


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


def _llm_generate(requirements: pd.DataFrame, coverage: pd.DataFrame, strategies: pd.DataFrame, provider: str, model: str | None) -> pd.DataFrame:
    prompt = test_case_generation_prompt(requirements.to_string(index=False), coverage.to_string(index=False), strategies.to_string(index=False))
    parsed = _clean_json(chat_completion(TEST_CASE_IMPROVEMENT_SYSTEM, prompt, provider=provider, model=model))
    data = pd.DataFrame(parsed.get("test_cases", []))
    if data.empty:
        raise ValueError("LLM returned no test_cases")
    for col in REQUIRED_COLUMNS:
        if col not in data.columns:
            data[col] = ""
    return data[REQUIRED_COLUMNS]


def improve_test_cases_with_llm(test_cases: pd.DataFrame, provider: str | None = None, model: str | None = None, use_llm: bool = True) -> pd.DataFrame:
    if test_cases.empty or not use_llm or not provider or not is_llm_enabled(provider):
        return test_cases.copy()
    improved = test_cases.copy()
    try:
        parsed = _clean_json(chat_completion(TEST_CASE_IMPROVEMENT_SYSTEM, test_case_improvement_prompt(improved.to_string(index=False)), provider=provider, model=model))
    except Exception as exc:
        improved["improvement_llm_error"] = str(exc)
        return improved
    reviews = {r.get("test_case_id"): r for r in parsed.get("case_reviews", [])}
    improved["llm_review_issue"] = improved["test_case_id"].map(lambda cid: reviews.get(cid, {}).get("issue", ""))
    improved["llm_suggested_revision"] = improved["test_case_id"].map(lambda cid: reviews.get(cid, {}).get("suggested_revision", ""))
    return improved


def generate_test_cases(requirements: pd.DataFrame, coverage: pd.DataFrame, strategies: pd.DataFrame,
                        include_state_tests: bool = True, provider: str | None = None,
                        model: str | None = None, use_llm: bool = True) -> pd.DataFrame:
    if use_llm and provider and is_llm_enabled(provider):
        try:
            generated = _llm_generate(requirements, coverage, strategies, provider, model)
            return improve_oracles_with_llm(generated, provider=provider, model=model, use_llm=True)
        except Exception:
            pass
    return _fallback(requirements, coverage, strategies, include_state_tests)
