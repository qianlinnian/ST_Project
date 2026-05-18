import pandas as pd
from typing import List, Tuple
import json
import time

from src.models import Requirement, RiskRecord
from src.ai_client import chat_completion, is_llm_enabled
from src.prompt_templates import RISK_ANALYSIS_SYSTEM, risk_analysis_batch_prompt


def _clean_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return json.loads(cleaned.strip())


def _risk_level(score: int) -> str:
    if score >= 7:
        return "High"
    if score >= 4:
        return "Medium"
    return "Low"


def analyze_risks(structured_requirements: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in structured_requirements.iterrows():
        text = row["requirement_text"].lower()
        req_id = row["requirement_id"]
        risk_category = _classify_risk_category(text)
        impact = (
            3
            if any(
                word in text
                for word in ["delete", "reject", "refresh", "persist", "save"]
            )
            else 2
        )
        likelihood = (
            3
            if any(
                word in text
                for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
            )
            else 2
        )
        score = likelihood * impact

        rows.append(
            {
                "risk_id": f"RSK-{str(req_id).split('-')[-1]}",
                "requirement_id": req_id,
                "risk_category": risk_category,
                "risk_description": _describe_risk(risk_category),
                "impact": impact,
                "likelihood": likelihood,
                "risk_score": score,
                "risk_level": _risk_level(score),
                "reason": _risk_reason(impact, likelihood, text),
                "test_suggestion": _test_suggestion(risk_category),
                "source": "Rule fallback",
            }
        )
    return pd.DataFrame(rows)


def _structured_frame_to_requirements(
    structured_requirements: pd.DataFrame,
) -> List[Requirement]:
    requirements = []
    for _, row in structured_requirements.iterrows():
        requirements.append(
            Requirement(
                requirement_id=str(row.get("requirement_id", "")),
                requirement_text=str(row.get("requirement_text", "")),
                module=str(row.get("module", "")),
                input_fields=row.get("input_fields", []),
                data_ranges=row.get("data_ranges", []),
                conditions=row.get("conditions", []),
                actions=row.get("actions", []),
                expected_results=row.get("expected_results", []),
            )
        )
    return requirements


def _risk_records_to_frame(records: List[RiskRecord], source: str) -> pd.DataFrame:
    rows = []
    for record in records:
        row = record.to_dict()
        row["source"] = source
        rows.append(row)
    return pd.DataFrame(rows)


def analyze_risks_with_llm_fallback(
    structured_requirements: pd.DataFrame,
    provider: str | None = None,
    model: str | None = None,
    use_llm: bool = True,
) -> Tuple[pd.DataFrame, dict]:
    timing_details = {}

    if (
        structured_requirements.empty
        or not use_llm
        or not provider
        or not is_llm_enabled(provider)
    ):
        t0 = time.time()
        result = analyze_risks(structured_requirements)
        timing_details["rule_fallback_total"] = time.time() - t0
        timing_details["method"] = "rule_fallback"
        return result, timing_details

    t_start = time.time()
    timing_details["method"] = "llm_analysis"
    timing_details["batches"] = []

    try:
        t_transform_start = time.time()
        requirements = _structured_frame_to_requirements(structured_requirements)
        timing_details["data_transformation_seconds"] = time.time() - t_transform_start
        print(f"[TIMING] 数据转换耗时: {timing_details['data_transformation_seconds']:.3f}s")

        t_llm_start = time.time()
        records, batch_times = analyze_requirements_risks(
            requirements,
            provider=provider,
            model=model,
            return_batch_times=True,
        )
        timing_details["llm_total_seconds"] = time.time() - t_llm_start
        timing_details["batches"] = batch_times
        print(f"[TIMING] LLM调用总耗时: {timing_details['llm_total_seconds']:.3f}s")
        for i, bt in enumerate(batch_times):
            print(f"[TIMING]   Batch {i+1}: {bt['llm_call_seconds']:.3f}s (处理 {bt['batch_size']} 条需求)")

        t_convert_start = time.time()
        risks = _risk_records_to_frame(records, source="LLM prompt analysis")
        timing_details["frame_conversion_seconds"] = time.time() - t_convert_start
        print(f"[TIMING] 结果转换DataFrame耗时: {timing_details['frame_conversion_seconds']:.3f}s")

        if risks.empty:
            raise ValueError("LLM returned no risk_analyses")

        timing_details["total_seconds"] = time.time() - t_start
        print(f"[TIMING] 风险分析总耗时: {timing_details['total_seconds']:.3f}s")
        return risks, timing_details

    except Exception as exc:
        t_fallback_start = time.time()
        fallback = analyze_risks(structured_requirements)
        timing_details["fallback_after_error_seconds"] = time.time() - t_fallback_start
        timing_details["error"] = str(exc)
        timing_details["method"] = "rule_fallback_after_error"
        print(f"[TIMING] LLM失败，回调规则方法耗时: {timing_details['fallback_after_error_seconds']:.3f}s")
        fallback["llm_error"] = str(exc)
        fallback["source"] = "Rule fallback after LLM failure"
        return fallback, timing_details


def _classify_risk_category(text: str) -> str:
    if any(
        word in text for word in ["credential", "password", "login", "admin", "auth"]
    ):
        return "security"
    if any(
        word in text
        for word in ["refresh", "persist", "save", "localstorage", "storage"]
    ):
        return "reliability"
    if any(
        word in text for word in ["filter", "active", "completed", "display", "view"]
    ):
        return "interaction capability"
    if any(
        word in text for word in ["limit", "100", "empty", "blank", "input", "invalid"]
    ):
        return "functional suitability"
    return "functional suitability"


def _describe_risk(risk_category: str) -> str:
    descriptions = {
        "security": "Authentication or protected access behavior may be bypassed or handled incorrectly.",
        "reliability": "Todo data or state may not be preserved consistently across operations.",
        "interaction capability": "The UI may display an incorrect Todo state or filter result.",
        "functional suitability": "The feature may not satisfy the required Todo behavior or input validation rule.",
    }
    return descriptions.get(risk_category, descriptions["functional suitability"])


def _risk_reason(impact: int, likelihood: int, text: str) -> str:
    signals = []
    if any(word in text for word in ["delete", "reject", "persist", "save", "refresh"]):
        signals.append("high-impact keyword")
    if any(
        word in text for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
    ):
        signals.append("error-prone condition or state keyword")
    signal_text = ", ".join(signals) if signals else "basic functional behavior"
    return f"Impact={impact}, Likelihood={likelihood}; derived from {signal_text}."


def _test_suggestion(risk_category: str) -> str:
    suggestions = {
        "security": "Include negative and unauthorized access tests.",
        "reliability": "Include persistence and recovery-oriented tests.",
        "interaction capability": "Include UI state, filtering, and transition tests.",
        "functional suitability": "Include valid, invalid, and boundary input tests.",
    }
    return suggestions.get(risk_category, suggestions["functional suitability"])


def analyze_requirements_risks(
    requirements: List[Requirement],
    provider: str,
    model: str | None = None,
    batch_size: int = 8,
    return_batch_times: bool = False,
) -> List[RiskRecord]:
    if not provider:
        raise ValueError("provider is required for LLM risk analysis")

    records = []
    batch_times = []

    for i in range(0, len(requirements), batch_size):
        batch = requirements[i : i + batch_size]
        batch_time = {"batch_index": i // batch_size, "batch_size": len(batch)}

        t_batch_start = time.time()

        reqs_text = []
        for req in batch:
            reqs_text.append(
                f"Requirement ID: {req.requirement_id}\n"
                f"Content: {req.requirement_text}\n"
                f"Input fields: {req.input_fields}\n"
                f"Data ranges: {req.data_ranges}\n"
                f"Conditions: {req.conditions}\n"
                f"Actions: {req.actions}\n"
                f"Expected results: {req.expected_results}\n"
            )

        t_prompt_start = time.time()
        prompt = risk_analysis_batch_prompt("\n---\n".join(reqs_text))
        batch_time["prompt_preparation_seconds"] = time.time() - t_prompt_start

        t_llm_start = time.time()
        parsed = _clean_json(
            chat_completion(
                RISK_ANALYSIS_SYSTEM,
                prompt,
                provider=provider,
                model=model,
            )
        )
        batch_time["llm_call_seconds"] = time.time() - t_llm_start

        t_parse_start = time.time()
        analyses = parsed.get("risk_analyses", [])
        analysis_dict = {
            str(item.get("requirement_id", "")).strip(): item for item in analyses
        }

        for req in batch:
            item = analysis_dict.get(req.requirement_id)
            if item is None:
                raise ValueError(
                    f"LLM response missing risk analysis for {req.requirement_id}"
                )

            risk_category = item.get("risk_category", "functional suitability")
            risk_description = item.get(
                "risk_description", "No description provided."
            )
            likelihood = min(max(int(item.get("likelihood", 1)), 1), 3)
            impact = min(max(int(item.get("impact", 1)), 1), 3)
            score = likelihood * impact

            records.append(
                RiskRecord(
                    risk_id=(
                        f"RSK-{req.requirement_id.split('-')[-1]}"
                        if "-" in req.requirement_id
                        else f"RSK-{req.requirement_id}"
                    ),
                    requirement_id=req.requirement_id,
                    risk_category=risk_category,
                    risk_description=risk_description,
                    impact=impact,
                    likelihood=likelihood,
                    risk_score=score,
                    risk_level=_risk_level(score),
                    reason=item.get("reason", "Analyzed by LLM in batch."),
                    test_suggestion=item.get("test_suggestion", ""),
                )
            )
        batch_time["result_parsing_seconds"] = time.time() - t_parse_start
        batch_time["batch_total_seconds"] = time.time() - t_batch_start

        if return_batch_times:
            batch_times.append(batch_time)

    if return_batch_times:
        return records, batch_times
    return records
