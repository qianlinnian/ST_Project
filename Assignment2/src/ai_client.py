import os
from dataclasses import dataclass
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    timeout: int = 30


def load_llm_config() -> Optional[LLMConfig]:
    api_key = os.getenv("AUTOTESTDESIGN_LLM_API_KEY", "").strip()
    if not api_key:
        return None

    return LLMConfig(
        api_key=api_key,
        base_url=os.getenv(
            "AUTOTESTDESIGN_LLM_BASE_URL",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ).rstrip("/"),
        model=os.getenv("AUTOTESTDESIGN_LLM_MODEL", "deepseek-v4-flash"),
        timeout=int(os.getenv("AUTOTESTDESIGN_LLM_TIMEOUT", "30")),
    )


def is_llm_enabled() -> bool:
    return load_llm_config() is not None


def chat_completion(system_prompt: str, user_prompt: str) -> str:
    config = load_llm_config()
    if config is None:
        raise RuntimeError("LLM API is not configured. Please check your .env file.")

    response = requests.post(
        f"{config.base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.model,
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
