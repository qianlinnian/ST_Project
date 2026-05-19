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
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(cleaned[start : end + 1])
        raise


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
