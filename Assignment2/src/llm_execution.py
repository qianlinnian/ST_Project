from __future__ import annotations

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable, Iterable, TypeVar

from src.ai_client import chat_completion

T = TypeVar("T")
R = TypeVar("R")


@dataclass
class LLMBatchResult:
    batch_index: int
    result: Any
    timing: dict[str, Any]


def env_int(name: str, default: int, min_value: int, max_value: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(min_value, min(max_value, value))


def llm_json_mode_enabled() -> bool:
    return os.getenv("AUTOTESTDESIGN_LLM_JSON_MODE", "0").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def clean_json(text: str) -> dict:
    cleaned = str(text or "").strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    cleaned = cleaned.strip()
    errors = []
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        errors.append(exc)

    repaired = repair_json_tail(cleaned)
    try:
        parsed = json.loads(repaired)
        print("[AutoTestDesign][LLM][JSON_REPAIR] repaired JSON tail", flush=True)
        return parsed
    except json.JSONDecodeError as exc:
        errors.append(exc)

    candidate = cleaned
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = cleaned[start : end + 1]

    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        errors.append(exc)

    repaired = repair_json_tail(candidate)
    try:
        parsed = json.loads(repaired)
        print("[AutoTestDesign][LLM][JSON_REPAIR] repaired JSON tail", flush=True)
        return parsed
    except json.JSONDecodeError as exc:
        errors.append(exc)
        positions = ", ".join(
            f"pos={error.pos}, line={error.lineno}, col={error.colno}"
            for error in errors
        )
        print(
            "[AutoTestDesign][LLM][JSON_ERROR] "
            f"len={len(cleaned)}, attempts={len(errors)}, {positions}",
            flush=True,
        )
        print("[AutoTestDesign][LLM][JSON_TAIL]", flush=True)
        print(cleaned[-800:], flush=True)
        raise exc


def repair_json_tail(text: str) -> str:
    repaired = str(text or "").strip()
    while repaired.endswith("```"):
        repaired = repaired[:-3].rstrip()
    while repaired.endswith(","):
        repaired = repaired[:-1].rstrip()

    open_square = repaired.count("[")
    close_square = repaired.count("]")
    open_curly = repaired.count("{")
    close_curly = repaired.count("}")

    missing_square = open_square - close_square
    missing_curly = open_curly - close_curly

    if missing_square > 0 and repaired.endswith("}"):
        repaired = repaired[:-1] + ("]" * missing_square) + "}"
        missing_square = 0

    if missing_square > 0:
        repaired += "]" * missing_square

    if missing_curly > 0:
        repaired += "}" * missing_curly

    return repaired


def call_json_completion(
    system_prompt: str,
    user_prompt: str,
    provider: str,
    model: str | None = None,
    max_tokens: int | None = None,
    response_format: dict | None = None,
) -> dict:
    if response_format is None and llm_json_mode_enabled():
        response_format = {"type": "json_object"}

    return clean_json(
        chat_completion(
            system_prompt,
            user_prompt,
            provider=provider,
            model=model,
            max_tokens=max_tokens,
            response_format=response_format,
        )
    )


def chunk_items(items: list[T], batch_size: int) -> list[list[T]]:
    return [items[i : i + batch_size] for i in range(0, len(items), batch_size)]


def run_parallel_batches(
    items: Iterable[T],
    batch_size: int,
    concurrency: int,
    process_batch: Callable[[int, list[T]], R],
    fallback_batch: Callable[[int, list[T], Exception], R] | None = None,
) -> tuple[list[R], list[dict[str, Any]]]:
    batches = chunk_items(list(items), max(1, int(batch_size)))
    if not batches:
        return [], []

    max_workers = min(max(1, int(concurrency)), len(batches))
    results_by_index: dict[int, R] = {}
    timings_by_index: dict[int, dict[str, Any]] = {}

    def timed_process(batch_index: int, batch: list[T]) -> LLMBatchResult:
        started = time.perf_counter()
        result = process_batch(batch_index, batch)
        elapsed = time.perf_counter() - started
        return LLMBatchResult(
            batch_index=batch_index,
            result=result,
            timing={
                "batch_index": batch_index,
                "batch_size": len(batch),
                "batch_total_seconds": elapsed,
            },
        )

    if max_workers <= 1:
        for batch_index, batch in enumerate(batches):
            try:
                batch_result = timed_process(batch_index, batch)
                results_by_index[batch_index] = batch_result.result
                timings_by_index[batch_index] = batch_result.timing
            except Exception as exc:
                if fallback_batch is None:
                    raise
                started = time.perf_counter()
                results_by_index[batch_index] = fallback_batch(batch_index, batch, exc)
                timings_by_index[batch_index] = {
                    "batch_index": batch_index,
                    "batch_size": len(batch),
                    "fallback": True,
                    "fallback_seconds": time.perf_counter() - started,
                    "error": f"{type(exc).__name__}: {exc}",
                }
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_batch = {
                executor.submit(timed_process, batch_index, batch): (batch_index, batch)
                for batch_index, batch in enumerate(batches)
            }
            for future in as_completed(future_to_batch):
                batch_index, batch = future_to_batch[future]
                try:
                    batch_result = future.result()
                    results_by_index[batch_index] = batch_result.result
                    timings_by_index[batch_index] = batch_result.timing
                except Exception as exc:
                    if fallback_batch is None:
                        raise
                    started = time.perf_counter()
                    results_by_index[batch_index] = fallback_batch(batch_index, batch, exc)
                    timings_by_index[batch_index] = {
                        "batch_index": batch_index,
                        "batch_size": len(batch),
                        "fallback": True,
                        "fallback_seconds": time.perf_counter() - started,
                        "error": f"{type(exc).__name__}: {exc}",
                    }

    ordered_results = [results_by_index[i] for i in range(len(batches))]
    ordered_timings = [timings_by_index[i] for i in range(len(batches))]
    return ordered_results, ordered_timings
