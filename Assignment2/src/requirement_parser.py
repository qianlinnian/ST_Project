import pandas as pd
from typing import List

from src.llm_execution import call_json_completion, env_int, run_parallel_batches
from src.nlp_processor import (
    extract_requirement_parts,
    extract_requirement_parts_local,
    is_requirement_structure_sufficient,
)
from src.models import Requirement
from src.prompt_templates import (
    COMPACT_REQUIREMENT_STRUCTURING_SYSTEM,
    compact_requirement_structuring_prompt,
)


def structure_requirements(
    requirements: pd.DataFrame,
    provider: str = "openai",
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    """
    为 DataFrame 显示/调试用途，结构化需求文本。
    注意：此函数主要用于展示，实际解析建议使用 parse_requirements。
    """
    structured_rows: list[dict] = []
    llm_needed: list[dict] = []

    for output_index, (_, row) in enumerate(requirements.iterrows()):
        requirement_text = row.get("requirement_text", "")
        if requirement_text is None or requirement_text != requirement_text:
            requirement_text = ""
        requirement_text = str(requirement_text).strip()
        if not requirement_text:
            continue

        parts = extract_requirement_parts_local(requirement_text)
        row_dict = _structured_row(row, requirement_text, parts)
        structured_rows.append(row_dict)

        if not is_requirement_structure_sufficient(parts):
            llm_needed.append(
                {
                    "output_index": len(structured_rows) - 1,
                    "requirement_id": str(row.get("requirement_id", output_index + 1)),
                    "requirement_text": requirement_text,
                    "local_parts": parts,
                }
            )

    if llm_needed:
        def structure_llm_batch(_batch_index: int, batch: list[dict]) -> list[dict]:
            parsed = call_json_completion(
                COMPACT_REQUIREMENT_STRUCTURING_SYSTEM,
                compact_requirement_structuring_prompt(batch),
                provider=provider,
                max_tokens=max(600, 120 * len(batch) + 400),
                task_label="Requirement Structuring Fallback",
            )
            by_id = _parse_compact_requirement_parts(parsed)
            results = []
            for item in batch:
                parts = by_id.get(str(item["requirement_id"]), {})
                results.append(
                    {
                        "output_index": item["output_index"],
                        "parts": _normalise_parts(parts) if parts else item["local_parts"],
                    }
                )
            return results

        def fallback_llm_batch(
            _batch_index: int, batch: list[dict], _exc: Exception
        ) -> list[dict]:
            return [
                {"output_index": item["output_index"], "parts": item["local_parts"]}
                for item in batch
            ]

        llm_batch_results, _ = run_parallel_batches(
            llm_needed,
            batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
            concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
            process_batch=structure_llm_batch,
            fallback_batch=fallback_llm_batch,
            task_label="Requirement Structuring Fallback",
        )

        for batch_result in llm_batch_results:
            for item in batch_result:
                structured_rows[item["output_index"]].update(item["parts"])

    return pd.DataFrame(structured_rows)


def enhance_requirements_with_llm(
    requirements: pd.DataFrame,
    provider: str,
    batch_size: int | None = None,
    concurrency: int | None = None,
) -> pd.DataFrame:
    """Structure every requirement with LLM, falling back to local extraction per failed batch."""
    llm_items: list[dict] = []
    structured_rows: list[dict] = []

    for output_index, (_, row) in enumerate(requirements.iterrows()):
        requirement_text = row.get("requirement_text", "")
        if requirement_text is None or requirement_text != requirement_text:
            requirement_text = ""
        requirement_text = str(requirement_text).strip()
        if not requirement_text:
            continue

        local_parts = extract_requirement_parts_local(requirement_text)
        structured_rows.append(_structured_row(row, requirement_text, local_parts))
        llm_items.append(
            {
                "output_index": len(structured_rows) - 1,
                "requirement_id": str(row.get("requirement_id", output_index + 1)),
                "requirement_text": requirement_text,
                "local_parts": local_parts,
            }
        )

    if not llm_items:
        return pd.DataFrame(structured_rows)

    def enhance_batch(_batch_index: int, batch: list[dict]) -> list[dict]:
        parsed = call_json_completion(
            COMPACT_REQUIREMENT_STRUCTURING_SYSTEM,
            compact_requirement_structuring_prompt(batch),
            provider=provider,
            max_tokens=max(600, 120 * len(batch) + 400),
            task_label="Requirement Structuring Enhancement",
        )
        by_id = _parse_compact_requirement_parts(parsed)
        results = []
        for item in batch:
            parts = by_id.get(str(item["requirement_id"]), {})
            results.append(
                {
                    "output_index": item["output_index"],
                    "parts": _normalise_parts(parts) if parts else item["local_parts"],
                }
            )
        return results

    def fallback_batch(
        _batch_index: int, batch: list[dict], _exc: Exception
    ) -> list[dict]:
        return [
            {"output_index": item["output_index"], "parts": item["local_parts"]}
            for item in batch
        ]

    llm_batch_results, _ = run_parallel_batches(
        llm_items,
        batch_size=batch_size or env_int("AUTOTESTDESIGN_LLM_BATCH_SIZE", 25, 1, 100),
        concurrency=concurrency or env_int("AUTOTESTDESIGN_LLM_CONCURRENCY", 4, 1, 16),
        process_batch=enhance_batch,
        fallback_batch=fallback_batch,
        task_label="Requirement Structuring Enhancement",
    )

    for batch_result in llm_batch_results:
        for item in batch_result:
            structured_rows[item["output_index"]].update(item["parts"])

    return pd.DataFrame(structured_rows)


def _structured_row(row: pd.Series, requirement_text: str, parts: dict) -> dict:
    row_dict = row.to_dict()
    row_dict["requirement_text"] = requirement_text
    row_dict.update(_normalise_parts(parts))
    return row_dict


def _normalise_parts(parts: dict) -> dict:
    return {
        "input_fields": parts.get("input_fields", []),
        "data_ranges": parts.get("data_ranges", []),
        "conditions": parts.get("conditions", []),
        "actions": parts.get("actions", []),
        "expected_results": parts.get("expected_results", []),
    }


def _parse_compact_requirement_parts(parsed: dict) -> dict[str, dict]:
    by_id: dict[str, dict] = {}

    if isinstance(parsed.get("r"), list):
        for item in parsed.get("r", []):
            if not isinstance(item, list) or len(item) < 6:
                continue
            requirement_id = str(item[0]).strip()
            if not requirement_id:
                continue
            by_id[requirement_id] = {
                "input_fields": _ensure_list(item[1]),
                "data_ranges": _ensure_list(item[2]),
                "conditions": _ensure_list(item[3]),
                "actions": _ensure_list(item[4]),
                "expected_results": _ensure_list(item[5]),
            }
        return by_id

    for item in parsed.get("requirements", []):
        if isinstance(item, dict):
            requirement_id = str(item.get("requirement_id", "")).strip()
            if requirement_id:
                by_id[requirement_id] = _normalise_parts(item)
    return by_id


def _ensure_list(value) -> list:
    if isinstance(value, list):
        return value
    if value in {None, ""}:
        return []
    return [str(value)]


def parse_requirements(
    requirements_data: List[dict], provider: str = "openai"
) -> List[Requirement]:
    """
    将原始需求数据解析为 Requirement 对象列表（核心解析函数）。
    """
    parsed_reqs = []
    for data in requirements_data:
        req_id = data.get("requirement_id", f"REQ_{len(parsed_reqs)+1}")
        req_text = data.get("requirement_text", "")
        if req_text is None or req_text != req_text:
            req_text = ""
        req_text = str(req_text).strip()
        module = data.get("module", "")

        if not req_text:
            continue  # 跳过空需求

        parts = extract_requirement_parts(req_text, provider=provider)
        
        req = Requirement(
            requirement_id=req_id,
            requirement_text=req_text,
            module=module,
            input_fields=parts.get("input_fields", []),
            data_ranges=parts.get("data_ranges", []),
            conditions=parts.get("conditions", []),
            actions=parts.get("actions", []),
            expected_results=parts.get("expected_results", [])
        )
        parsed_reqs.append(req)
        
    return parsed_reqs
