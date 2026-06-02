import os
import re
import time
import json
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Optional, Generator

import requests
from dotenv import load_dotenv

import threading
from requests.adapters import HTTPAdapter

load_dotenv()

_THREAD_LOCAL = threading.local()

def _get_http_session() -> requests.Session:
    session = getattr(_THREAD_LOCAL, "session", None)
    if session is None:
        session = requests.Session()
        adapter = HTTPAdapter(
            pool_connections=32,
            pool_maxsize=32,
            max_retries=0,
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        _THREAD_LOCAL.session = session
    return session

@dataclass
class LLMProvider:
    name: str
    api_key: str
    base_url: str
    models: list[str]
    timeout: int = 30


class LLMCallError(RuntimeError):
    pass


def _llm_log_enabled() -> bool:
    return os.getenv("AUTOTESTDESIGN_LLM_LOG", "1").strip().lower() not in {
        "0",
        "false",
        "no",
    }


def _log_llm_event(message: str) -> None:
    if _llm_log_enabled():
        print(f"[AutoTestDesign][LLM] {message}", flush=True)


def _env_key(provider: str, suffix: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]", "_", provider).upper()
    return f"AUTOTESTDESIGN_LLM_{normalized}_{suffix}"


def _split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def configured_provider_names() -> list[str]:
    configured = os.getenv("AUTOTESTDESIGN_LLM_PROVIDERS", "").strip()
    if configured:
        return _split_csv(configured)

    return ["deepseek", "aliyun"]


def load_provider(provider: str) -> Optional[LLMProvider]:
    api_key = os.getenv(_env_key(provider, "API_KEY"), "").strip()
    base_url = os.getenv(_env_key(provider, "BASE_URL"), "").strip().rstrip("/")
    models = _split_csv(os.getenv(_env_key(provider, "MODELS"), ""))
    timeout = int(os.getenv(_env_key(provider, "TIMEOUT"), os.getenv("AUTOTESTDESIGN_LLM_TIMEOUT", "120")))

    if not api_key or not base_url or not models:
        return None

    return LLMProvider(
        name=provider,
        api_key=api_key,
        base_url=base_url,
        models=models,
        timeout=timeout,
    )


def configured_providers() -> dict[str, Optional[LLMProvider]]:
    return {name: load_provider(name) for name in configured_provider_names()}


def available_provider_names() -> list[str]:
    return configured_provider_names()


def available_models(provider: Optional[str] = None) -> list[str]:
    provider_name = provider or available_provider_names()[0]
    configured = load_provider(provider_name)
    if configured is not None:
        return configured.models

    fallback_models = {
        "deepseek": ["deepseek-v4-flash", "deepseek-v4-pro", "deepseek-chat"],
        "aliyun": ["qwen-plus", "qwen-max", "qwen3.5-plus"],
        "openai": ["gpt-4o-mini", "gpt-4.1-mini"],
    }
    return fallback_models.get(provider_name, ["gpt-4o-mini"])


def is_llm_enabled(provider: Optional[str] = None) -> bool:
    if provider:
        return load_provider(provider) is not None
    return any(load_provider(name) is not None for name in available_provider_names())


def _build_payload(
    selected_model: str,
    system_prompt: str,
    user_prompt: str,
    provider_name: str,
    max_tokens: Optional[int] = None,
    response_format: Optional[dict] = None,
) -> dict:
    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0,
    }
    
    if max_tokens is not None:
        payload["max_tokens"] = int(max_tokens)

    if response_format is not None:
        payload["response_format"] = response_format
    
    # 禁用各模型深度思考/推理模式以提升响应速度
    if provider_name == "deepseek":
        payload["thinking"] = {"type": "disabled"}
    if provider_name == "zhipu":
        payload["thinking"] = {"type": "disabled"}
    if provider_name == "siliconflow":
        if "deepseek" in selected_model.lower() or "r1" in selected_model.lower():
            payload["thinking"] = {"type": "disabled"}
    return payload


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    provider: str,
    model: Optional[str] = None,
    max_tokens: Optional[int] = None,
    response_format: Optional[dict] = None,
    task_label: Optional[str] = None,
) -> str:
    config = load_provider(provider)
    if config is None:
        _log_llm_event(f"configuration missing provider={provider}")
        raise LLMCallError(
            f"LLM provider '{provider}' is not configured. Create .env from .env.example."
        )

    selected_model = model or config.models[0]
    endpoint_host = urlparse(config.base_url).netloc or config.base_url
    started = time.perf_counter()
    _log_llm_event(
        "request start "
        f"{f'task={task_label} ' if task_label else ''}"
        f"provider={config.name} model={selected_model} host={endpoint_host} "
        f"timeout={config.timeout}s system_chars={len(system_prompt)} "
        f"user_chars={len(user_prompt)}"
    )

    try:
        payload = _build_payload(
            selected_model,
            system_prompt,
            user_prompt,
            config.name,
            max_tokens=max_tokens,
            response_format=response_format,
        )
        
        response = _get_http_session().post(
            f"{config.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=config.timeout,
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "request success "
            f"{f'task={task_label} ' if task_label else ''}"
            f"provider={config.name} model={selected_model} "
            f"elapsed={elapsed:.2f}s response_chars={len(content)}"
        )
        return content
    except requests.exceptions.HTTPError as exc:
        elapsed = time.perf_counter() - started
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        detail = exc.response.text[:300] if exc.response is not None else str(exc)
        if status_code in {401, 403}:
            reason = "API key is invalid, unauthorized, or the model permission is not enabled."
        elif status_code in {402, 429}:
            reason = "The provider rejected the request because of quota, balance, or rate limit."
        else:
            reason = "The provider returned an HTTP error."
        _log_llm_event(
            "request http_error "
            f"provider={config.name} model={selected_model} "
            f"status={status_code} elapsed={elapsed:.2f}s"
        )
        raise LLMCallError(f"{reason} status={status_code}. detail={detail}") from exc
    except requests.exceptions.Timeout as exc:
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "request timeout "
            f"provider={config.name} model={selected_model} "
            f"elapsed={elapsed:.2f}s timeout={config.timeout}s"
        )
        raise LLMCallError(
            f"LLM request timed out after {config.timeout} seconds. Local fallback can still be used."
        ) from exc
    except requests.exceptions.RequestException as exc:
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "request failed "
            f"provider={config.name} model={selected_model} elapsed={elapsed:.2f}s error={exc}"
        )
        raise LLMCallError(f"LLM request failed: {exc}") from exc
    except (KeyError, IndexError, ValueError) as exc:
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "response invalid "
            f"provider={config.name} model={selected_model} elapsed={elapsed:.2f}s error={exc}"
        )
        raise LLMCallError(
            f"LLM response format is invalid or incomplete: {exc}"
        ) from exc


def chat_completion_stream(
    system_prompt: str,
    user_prompt: str,
    provider: str,
    model: Optional[str] = None,
) -> Generator[str, None, None]:
    config = load_provider(provider)
    if config is None:
        _log_llm_event(f"configuration missing provider={provider}")
        raise LLMCallError(
            f"LLM provider '{provider}' is not configured. Create .env from .env.example."
        )

    selected_model = model or config.models[0]
    endpoint_host = urlparse(config.base_url).netloc or config.base_url
    started = time.perf_counter()
    _log_llm_event(
        "request start (stream) "
        f"provider={config.name} model={selected_model} host={endpoint_host} "
        f"timeout={config.timeout}s system_chars={len(system_prompt)} "
        f"user_chars={len(user_prompt)}"
    )

    try:
        payload = _build_payload(selected_model, system_prompt, user_prompt, config.name)
        payload["stream"] = True
        response = _get_http_session().post(
            f"{config.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=config.timeout,
            stream=True,
        )
        response.raise_for_status()

        full_content = []
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")
                if line_str.startswith("data: "):
                    data_str = line_str[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                chunk = delta["content"]
                                full_content.append(chunk)
                                yield chunk
                    except json.JSONDecodeError:
                        continue

        elapsed = time.perf_counter() - started
        _log_llm_event(
            "request success (stream) "
            f"provider={config.name} model={selected_model} "
            f"elapsed={elapsed:.2f}s response_chars={len(''.join(full_content))}"
        )
    except requests.exceptions.HTTPError as exc:
        elapsed = time.perf_counter() - started
        status_code = exc.response.status_code if exc.response is not None else "unknown"
        detail = exc.response.text[:300] if exc.response is not None else str(exc)
        if status_code in {401, 403}:
            reason = "API key is invalid, unauthorized, or the model permission is not enabled."
        elif status_code in {402, 429}:
            reason = "The provider rejected the request because of quota, balance, or rate limit."
        else:
            reason = "The provider returned an HTTP error."
        _log_llm_event(
            "request http_error (stream) "
            f"provider={config.name} model={selected_model} "
            f"status={status_code} elapsed={elapsed:.2f}s"
        )
        raise LLMCallError(f"{reason} status={status_code}. detail={detail}") from exc
    except requests.exceptions.Timeout as exc:
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "request timeout (stream) "
            f"provider={config.name} model={selected_model} "
            f"elapsed={elapsed:.2f}s timeout={config.timeout}s"
        )
        raise LLMCallError(
            f"LLM request timed out after {config.timeout} seconds. Local fallback can still be used."
        ) from exc
    except requests.exceptions.RequestException as exc:
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "request failed (stream) "
            f"provider={config.name} model={selected_model} elapsed={elapsed:.2f}s error={exc}"
        )
        raise LLMCallError(f"LLM request failed: {exc}") from exc
    except (KeyError, IndexError, ValueError) as exc:
        elapsed = time.perf_counter() - started
        _log_llm_event(
            "response invalid (stream) "
            f"provider={config.name} model={selected_model} elapsed={elapsed:.2f}s error={exc}"
        )
        raise LLMCallError(
            f"LLM response format is invalid or incomplete: {exc}"
        ) from exc
