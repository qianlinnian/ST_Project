import os
import re
from dataclasses import dataclass
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()


@dataclass
class LLMProvider:
    name: str
    api_key: str
    base_url: str
    models: list[str]
    timeout: int = 30


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
    timeout = int(os.getenv(_env_key(provider, "TIMEOUT"), os.getenv("AUTOTESTDESIGN_LLM_TIMEOUT", "30")))

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


def chat_completion(
    system_prompt: str,
    user_prompt: str,
    provider: str,
    model: Optional[str] = None,
) -> str:
    config = load_provider(provider)
    if config is None:
        raise RuntimeError(
            f"LLM provider '{provider}' is not configured. Create Assignment2/.env from .env.example."
        )

    response = requests.post(
        f"{config.base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model or config.models[0],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        },
        timeout=config.timeout,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
