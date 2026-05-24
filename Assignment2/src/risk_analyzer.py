import pandas as pd
from typing import List, Tuple
import json
import time

from src.models import Requirement, RiskRecord
from src.ai_client import chat_completion, is_llm_enabled
from src.prompt_templates import (
    COMPACT_RISK_SYSTEM,
    RISK_ANALYSIS_SYSTEM,
    compact_risk_prompt,
    risk_analysis_batch_prompt,
)

import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def _repair_trailing_json(cleaned: str) -> str:
    """
    Repair common LLM JSON tail errors for compact risk format.

    Expected shape:
    {"r":[[id,category,impact,likelihood,reason],...]}

    Common bad endings:
    1. ... "reason"]}     -> missing one ]
    2. ... "reason"]}     -> should be ... "reason"]]}
    3. ... "reason"]}]}   -> extra }
    4. ... "reason"]}]}   -> should be ... "reason"]]}
    """
    text = str(cleaned or "").strip()

    # 去掉 markdown 尾部或多余逗号
    while text.endswith("```"):
        text = text[:-3].rstrip()

    while text.endswith(","):
        text = text[:-1].rstrip()

    if not text.startswith("{"):
        return text

    # 针对 compact risk JSON，优先根据最后一个完整 item 修复尾部。
    # 找到最后一个 "]]" 之前的内容不可靠，所以这里从最后一个完整 array item 的 "]" 处截断。
    # 例如：
    # {"r":[["A","F",1,1,"x"],["B","I",2,1,"y"]}]}
    # 最后一个 item 结束在最后一个 ]，后面如果是错误的 }]}，统一重建为 ]}
    if text.startswith('{"r":[') or text.startswith('{"r": ['):
        last_item_end = text.rfind("]")
        if last_item_end != -1:
            prefix = text[: last_item_end + 1]

            # prefix 应该是 {"r":[ ... last item ]
            # compact 格式最后必须补上 ]} 关闭 r 数组和 root object
            repaired = prefix + "]}"

            # 如果 prefix 本身已经是完整的 {"r":[...]}，上面可能多补。
            # 所以先试 repaired，如果失败再走通用逻辑。
            try:
                json.loads(repaired)
                return repaired
            except Exception:
                pass

    # 通用修复：平衡括号数量
    open_square = text.count("[")
    close_square = text.count("]")
    open_curly = text.count("{")
    close_curly = text.count("}")

    missing_square = open_square - close_square
    missing_curly = open_curly - close_curly

    # 如果少 ] 且最后有 }，把 ] 插到最后一个 } 前面
    if missing_square > 0 and text.endswith("}"):
        text = text[:-1] + ("]" * missing_square) + "}"

    # 如果少 }，补 }
    open_curly = text.count("{")
    close_curly = text.count("}")
    missing_curly = open_curly - close_curly
    if missing_curly > 0:
        text = text + ("}" * missing_curly)

    # 如果还少 ]，补 ]
    open_square = text.count("[")
    close_square = text.count("]")
    missing_square = open_square - close_square
    if missing_square > 0:
        text = text + ("]" * missing_square)

    return text


def _clean_json(text: str) -> dict:
    cleaned = str(text or "").strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()

    errors = []

    # 第一次：原文直接解析
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        errors.append(exc)

    # 第二次：截取第一个 { 到最后一个 }
    candidate = cleaned
    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start != -1 and end != -1 and end > start:
        candidate = cleaned[start : end + 1]

    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        errors.append(exc)

    # 第三次：修复尾部括号
    repaired = _repair_trailing_json(candidate)

    try:
        parsed = json.loads(repaired)
        print("[AutoTestDesign][Risk][JSON_REPAIR] repaired trailing JSON brackets")
        return parsed
    except json.JSONDecodeError as exc:
        errors.append(exc)

        positions = ", ".join(
            f"pos={e.pos}, line={e.lineno}, col={e.colno}" for e in errors
        )

        print(
            "[AutoTestDesign][Risk][JSON_ERROR] "
            f"len={len(cleaned)}, attempts={len(errors)}, {positions}"
        )
        print("[AutoTestDesign][Risk][JSON_TAIL]")
        print(cleaned[-500:])
        print("[AutoTestDesign][Risk][JSON_REPAIRED_TAIL]")
        print(repaired[-500:])

        raise exc


def _risk_level(score: int) -> str:
    if score >= 6:
        return "High"
    if score >= 3:
        return "Medium"
    return "Low"

def _env_int(name: str, default: int, min_value: int, max_value: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(min_value, min(max_value, value))


def _clamp_int(value, default: int = 2, low: int = 1, high: int = 3) -> int:
    try:
        value = int(value)
    except Exception:
        value = default
    return max(low, min(high, value))


def _risk_category_from_code(value) -> str:
    text = str(value or "").strip().lower()

    if text in {"s", "sec", "security"}:
        return "security"
    if text in {"r", "rel", "reliability"}:
        return "reliability"
    if text in {"i", "ui", "interaction", "interaction capability"}:
        return "interaction capability"
    if text in {"f", "func", "functional", "functional suitability"}:
        return "functional suitability"

    return "functional suitability"


def _risk_id_for(requirement_id: str) -> str:
    requirement_id = str(requirement_id)
    if "-" in requirement_id:
        return f"RSK-{requirement_id.split('-')[-1]}"
    return f"RSK-{requirement_id}"


def _rule_values_for_text(text: str) -> tuple[str, int, int, str]:
    lower = str(text or "").lower()
    risk_category = _classify_risk_category(lower)

    impact = (
        3
        if any(
            word in lower
            for word in ["delete", "reject", "refresh", "persist", "save"]
        )
        else 2
    )

    likelihood = (
        3
        if any(
            word in lower
            for word in ["empty", "limit", "100", "completed", "toggle", "filter"]
        )
        else 2
    )

    return risk_category, impact, likelihood, _risk_reason(impact, likelihood, lower)


def _make_risk_record(
    req: Requirement,
    risk_category: str,
    impact: int,
    likelihood: int,
    reason: str,
    risk_description: str | None = None,
    test_suggestion: str | None = None,
) -> RiskRecord:
    score = impact * likelihood
    risk_category = risk_category or "functional suitability"

    return RiskRecord(
        risk_id=_risk_id_for(req.requirement_id),
        requirement_id=req.requirement_id,
        risk_category=risk_category,
        risk_description=risk_description or _describe_risk(risk_category),
        impact=impact,
        likelihood=likelihood,
        risk_score=score,
        risk_level=_risk_level(score),
        reason=reason or "Analyzed by compact LLM prompt.",
        test_suggestion=test_suggestion or _test_suggestion(risk_category),
    )


def _risk_max_tokens(batch_size: int, fast_mode: bool = True) -> int:
    configured = os.getenv("AUTOTESTDESIGN_RISK_MAX_TOKENS", "").strip()
    if configured:
        return _env_int("AUTOTESTDESIGN_RISK_MAX_TOKENS", 800, 80, 4096)

    if fast_mode:
        return max(800, 80 * batch_size + 500)

    return max(1200, 120 * batch_size + 800)


def _parse_compact_items_from_text(text: str) -> dict:
    """
    Fallback parser for compact LLM output.

    It extracts items like:
    ["REQ-TODO-050","F",1,1,"filter visibility"]

    This is useful when the outer JSON brackets are broken.
    """
    import re

    by_id = {}

    pattern = re.compile(
        r'\[\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*([123])\s*,\s*([123])\s*,\s*"([^"]*)"\s*\]'
    )

    for match in pattern.finditer(str(text or "")):
        requirement_id = match.group(1).strip()
        category = _risk_category_from_code(match.group(2))
        impact = _clamp_int(match.group(3))
        likelihood = _clamp_int(match.group(4))
        reason = match.group(5).strip() or "Compact LLM classification"

        if requirement_id:
            by_id[requirement_id] = {
                "risk_category": category,
                "impact": impact,
                "likelihood": likelihood,
                "reason": reason,
            }

    return by_id


def _parse_llm_risk_records(parsed: dict, batch: List[Requirement]) -> List[RiskRecord]:
    by_id: dict[str, dict] = {}

    # Fast compact format:
    # {"r":[["REQ-001","F",2,2,"basic behavior"], ...]}
    if isinstance(parsed.get("r"), list):
        for item in parsed.get("r", []):
            if isinstance(item, list):
                if len(item) < 4:
                    continue
                requirement_id = str(item[0]).strip()
                category = _risk_category_from_code(item[1])
                impact = _clamp_int(item[2])
                likelihood = _clamp_int(item[3])
                reason = str(item[4]).strip() if len(item) >= 5 else "Compact LLM classification"

                by_id[requirement_id] = {
                    "risk_category": category,
                    "impact": impact,
                    "likelihood": likelihood,
                    "reason": reason,
                }

            elif isinstance(item, dict):
                requirement_id = str(
                    item.get("id")
                    or item.get("requirement_id")
                    or ""
                ).strip()

                if not requirement_id:
                    continue

                category = _risk_category_from_code(
                    item.get("c")
                    or item.get("category")
                    or item.get("risk_category")
                )
                impact = _clamp_int(item.get("i") or item.get("impact"))
                likelihood = _clamp_int(item.get("l") or item.get("likelihood"))
                reason = str(
                    item.get("r")
                    or item.get("reason")
                    or "Compact LLM classification"
                ).strip()

                by_id[requirement_id] = {
                    "risk_category": category,
                    "impact": impact,
                    "likelihood": likelihood,
                    "reason": reason,
                }

    # Old verbose format:
    # {"risk_analyses":[{...}, ...]}
    else:
        for item in parsed.get("risk_analyses", []):
            requirement_id = str(item.get("requirement_id", "")).strip()
            if not requirement_id:
                continue

            by_id[requirement_id] = {
                "risk_category": item.get("risk_category", "functional suitability"),
                "risk_description": item.get("risk_description"),
                "impact": _clamp_int(item.get("impact")),
                "likelihood": _clamp_int(item.get("likelihood")),
                "reason": item.get("reason", "Analyzed by LLM in batch."),
                "test_suggestion": item.get("test_suggestion", ""),
            }

    records = []

    for req in batch:
        item = by_id.get(req.requirement_id)

        # 如果某条漏了，不要让整批失败，直接用本地规则兜底
        if item is None:
            category, impact, likelihood, reason = _rule_values_for_text(req.requirement_text)
            records.append(
                _make_risk_record(
                    req=req,
                    risk_category=category,
                    impact=impact,
                    likelihood=likelihood,
                    reason=f"Rule fallback: {reason}",
                )
            )
            continue

        category = _risk_category_from_code(item.get("risk_category"))
        impact = _clamp_int(item.get("impact"))
        likelihood = _clamp_int(item.get("likelihood"))
        reason = str(item.get("reason", "Analyzed by LLM.")).strip()

        records.append(
            _make_risk_record(
                req=req,
                risk_category=category,
                impact=impact,
                likelihood=likelihood,
                reason=reason,
                risk_description=item.get("risk_description"),
                test_suggestion=item.get("test_suggestion"),
            )
        )

    return records


def _analyze_one_batch_with_llm(
    batch_index: int,
    batch: List[Requirement],
    provider: str,
    model: str | None,
    fast_mode: bool = True,
) -> tuple[int, List[RiskRecord], dict]:
    batch_time = {
        "batch_index": batch_index,
        "batch_size": len(batch),
    }

    t_batch_start = time.perf_counter()

    t_prompt_start = time.perf_counter()

    if fast_mode:
        system_prompt = COMPACT_RISK_SYSTEM
        text_limit = _env_int("AUTOTESTDESIGN_RISK_TEXT_LIMIT", 300, 80, 2000)
        prompt = compact_risk_prompt(batch, text_limit=text_limit)
    else:
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
        system_prompt = RISK_ANALYSIS_SYSTEM
        prompt = risk_analysis_batch_prompt("\n---\n".join(reqs_text))

    batch_time["prompt_preparation_seconds"] = time.perf_counter() - t_prompt_start
    batch_time["prompt_chars"] = len(prompt)

    max_tokens = _risk_max_tokens(len(batch), fast_mode=fast_mode)
    batch_time["max_tokens"] = max_tokens

    json_mode_enabled = os.getenv(
        "AUTOTESTDESIGN_LLM_JSON_MODE", "0"
    ).strip().lower() in {"1", "true", "yes"}

    response_format = {"type": "json_object"} if json_mode_enabled else None

    t_llm_start = time.perf_counter()

    content = chat_completion(
        system_prompt,
        prompt,
        provider=provider,
        model=model,
        max_tokens=max_tokens,
        response_format=response_format,
        task_label="Risk Analysis",
    )

    batch_time["llm_call_seconds"] = time.perf_counter() - t_llm_start
    batch_time["response_chars"] = len(str(content or ""))

    t_parse_start = time.perf_counter()

    try:
        parsed = _clean_json(content)
        records = _parse_llm_risk_records(parsed, batch)

    except Exception as exc:
        # 如果 JSON 外层坏了，尝试从 compact 文本里直接提取每条记录
        compact_items = _parse_compact_items_from_text(content)

        if compact_items:
            print(
                f"[AutoTestDesign][Risk][REGEX_REPAIR] "
                f"batch={batch_index}, extracted={len(compact_items)} items"
            )

            parsed = {"r": []}
            for req in batch:
                item = compact_items.get(req.requirement_id)
                if item:
                    parsed["r"].append(
                        [
                            req.requirement_id,
                            item["risk_category"],
                            item["impact"],
                            item["likelihood"],
                            item["reason"],
                        ]
                    )

            records = _parse_llm_risk_records(parsed, batch)

        else:
            batch_time["result_parsing_seconds"] = time.perf_counter() - t_parse_start
            batch_time["batch_total_seconds"] = time.perf_counter() - t_batch_start
            batch_time["error"] = str(exc)
            batch_time["response_tail"] = str(content or "")[-500:]

            print(
                f"[AutoTestDesign][Risk][BATCH_ERROR] batch={batch_index}, "
                f"response_chars={batch_time['response_chars']}, "
                f"max_tokens={max_tokens}, error={type(exc).__name__}: {exc}"
            )
            print("[AutoTestDesign][Risk][BATCH_RESPONSE_TAIL]")
            print(batch_time["response_tail"])

            raise

    batch_time["result_parsing_seconds"] = time.perf_counter() - t_parse_start
    batch_time["batch_total_seconds"] = time.perf_counter() - t_batch_start

    return batch_index, records, batch_time


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
    batch_size: int | None = None,
    concurrency: int | None = None,
    fast_mode: bool = True,
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
        print(f"[TIMING][Risk Analysis] 数据转换耗时: {timing_details['data_transformation_seconds']:.3f}s")

        t_llm_start = time.time()
        records, batch_times = analyze_requirements_risks(
            requirements,
            provider=provider,
            model=model,
            batch_size=batch_size,
            concurrency=concurrency,
            return_batch_times=True,
            fast_mode=fast_mode,
        )
        timing_details["llm_total_seconds"] = time.time() - t_llm_start
        timing_details["batches"] = batch_times
        timing_details["batch_size"] = batch_size
        timing_details["concurrency"] = concurrency
        timing_details["fast_mode"] = fast_mode
        print(f"[TIMING][Risk Analysis] LLM调用总耗时: {timing_details['llm_total_seconds']:.3f}s")
        for i, bt in enumerate(batch_times):
            if bt.get("fallback"):
                print(
                    f"[TIMING][Risk Analysis]   Batch {i+1}: LLM失败，使用规则兜底 "
                    f"(处理 {bt['batch_size']} 条需求, "
                    f"fallback耗时 {bt.get('fallback_seconds', 0.0):.3f}s, "
                    f"error={bt.get('error', '')})"
                )
            else:
                print(
                    f"[TIMING][Risk Analysis]   Batch {i+1}: {bt['llm_call_seconds']:.3f}s "
                    f"(处理 {bt['batch_size']} 条需求, "
                    f"response_chars={bt.get('response_chars', 'unknown')}, "
                    f"max_tokens={bt.get('max_tokens', 'unknown')})"
                )

        t_convert_start = time.time()
        risks = _risk_records_to_frame(records, source="LLM prompt analysis")
        timing_details["frame_conversion_seconds"] = time.time() - t_convert_start
        print(f"[TIMING][Risk Analysis] 结果转换DataFrame耗时: {timing_details['frame_conversion_seconds']:.3f}s")

        if risks.empty:
            raise ValueError("LLM returned no risk_analyses")

        timing_details["total_seconds"] = time.time() - t_start
        print(f"[TIMING][Risk Analysis] 风险分析总耗时: {timing_details['total_seconds']:.3f}s")
        return risks, timing_details

    except Exception as exc:
        t_fallback_start = time.time()
        fallback = analyze_risks(structured_requirements)
        timing_details["fallback_after_error_seconds"] = time.time() - t_fallback_start
        timing_details["error"] = str(exc)
        timing_details["method"] = "rule_fallback_after_error"
        print(f"[TIMING][Risk Analysis] LLM失败，回调规则方法耗时: {timing_details['fallback_after_error_seconds']:.3f}s")
        print(f"[AutoTestDesign][Risk][ERROR] LLM risk analysis failed: {type(exc).__name__}: {exc}")
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
    batch_size: int | None = None,
    concurrency: int | None = None,
    return_batch_times: bool = False,
    fast_mode: bool = True,
) -> List[RiskRecord] | tuple[List[RiskRecord], list[dict]]:
    if not provider:
        raise ValueError("provider is required for LLM risk analysis")

    batch_size = batch_size or _env_int(
        "AUTOTESTDESIGN_LLM_BATCH_SIZE",
        default=25,
        min_value=1,
        max_value=100,
    )

    concurrency = concurrency or _env_int(
        "AUTOTESTDESIGN_LLM_CONCURRENCY",
        default=4,
        min_value=1,
        max_value=16,
    )

    batches: list[tuple[int, List[Requirement]]] = []
    for start in range(0, len(requirements), batch_size):
        batch_index = start // batch_size
        batches.append((batch_index, requirements[start : start + batch_size]))

    if not batches:
        if return_batch_times:
            return [], []
        return []

    records_by_batch: dict[int, List[RiskRecord]] = {}
    batch_times_by_index: dict[int, dict] = {}

    max_workers = min(concurrency, len(batches))

    # 单批或 concurrency=1 时走串行，方便调试
    if max_workers <= 1:
        for batch_index, batch in batches:
            idx, batch_records, batch_time = _analyze_one_batch_with_llm(
                batch_index=batch_index,
                batch=batch,
                provider=provider,
                model=model,
                fast_mode=fast_mode,
            )
            records_by_batch[idx] = batch_records
            batch_times_by_index[idx] = batch_time

    # 多批并发
    else:
        # 构建 batch_index -> batch 的映射，供异常时兜底使用
        batch_map: dict[int, List[Requirement]] = {bi: b for bi, b in batches}
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_index = {
                executor.submit(
                    _analyze_one_batch_with_llm,
                    batch_index,
                    batch,
                    provider,
                    model,
                    fast_mode,
                ): batch_index
                for batch_index, batch in batches
            }

            for future in as_completed(future_to_index):
                original_idx = future_to_index[future]
                try:
                    idx, batch_records, batch_time = future.result()
                    records_by_batch[idx] = batch_records
                    batch_times_by_index[idx] = batch_time
                except Exception as exc:
                    print(
                        f"[AutoTestDesign][Risk][WARN] Batch {original_idx} LLM call failed: "
                        f"{type(exc).__name__}: {exc} — using rule fallback for this batch"
                    )

                    # 单批失败，降级为规则方法，不影响其他批次
                    fallback_batch = batch_map.get(original_idx, [])

                    t_fallback_start = time.perf_counter()
                    fallback_records = []
                    for req in fallback_batch:
                        cat, imp, lik, rsn = _rule_values_for_text(req.requirement_text)
                        fallback_records.append(
                            _make_risk_record(
                                req=req,
                                risk_category=cat,
                                impact=imp,
                                likelihood=lik,
                                reason=f"Rule fallback (batch error): {rsn}",
                            )
                        )
                    fallback_seconds = time.perf_counter() - t_fallback_start

                    records_by_batch[original_idx] = fallback_records

                    # 注意：这里拿不到失败 future 内部真实耗时，因为异常已经抛出来了。
                    # 但至少不要误导为 0 秒，标记为 -1，并单独记录 fallback 耗时。
                    batch_times_by_index[original_idx] = {
                        "batch_index": original_idx,
                        "batch_size": len(fallback_batch),
                        "llm_call_seconds": -1.0,
                        "fallback_seconds": fallback_seconds,
                        "error": f"{type(exc).__name__}: {exc}",
                        "fallback": True,
                    }

    records: List[RiskRecord] = []
    batch_times: list[dict] = []

    for batch_index, _ in sorted(batches, key=lambda item: item[0]):
        records.extend(records_by_batch[batch_index])
        batch_times.append(batch_times_by_index[batch_index])

    if return_batch_times:
        return records, batch_times

    return records
