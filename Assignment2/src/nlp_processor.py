import json
from typing import Dict, List

from src.ai_client import chat_completion
from src.prompt_templates import REQUIREMENT_STRUCTURING_SYSTEM


def extract_requirement_parts(requirement_text: str) -> Dict[str, List[str]]:
    """
    使用 LLM 将原始需求文本解析为结构化的测试信息。
    严格遵循 Requirement dataclass 的字段定义。
    """
    if not requirement_text or not requirement_text.strip():
        return _empty_structure()

    try:
        user_prompt = f"""Requirement ID: [待填充]
Requirement Text:
{requirement_text}"""

        response_text = chat_completion(
            system_prompt=REQUIREMENT_STRUCTURING_SYSTEM,
            user_prompt=user_prompt
        )

        # 清理可能的 Markdown 代码块
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        parsed = json.loads(cleaned.strip())

        return {
            "input_fields": parsed.get("input_fields", []),
            "data_ranges": parsed.get("data_ranges", []),
            "conditions": parsed.get("conditions", []),
            "actions": parsed.get("actions", []),
            "expected_results": parsed.get("expected_results", [])
        }

    except (json.JSONDecodeError, KeyError, Exception) as e:
        print(f"[Warning] Failed to parse requirement structure: {e}")
        print(f"Raw response: {response_text[:300]}...")
        return _empty_structure()


def _empty_structure() -> Dict[str, List[str]]:
    """返回空结构，作为失败时的 fallback"""
    return {
        "input_fields": [],
        "data_ranges": [],
        "conditions": [],
        "actions": [],
        "expected_results": []
    }