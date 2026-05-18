import json
import re
from typing import Dict, List

from src.ai_client import chat_completion
from src.prompt_templates import (
    REQUIREMENT_STRUCTURING_SYSTEM,
    requirement_structuring_prompt,
)

try:
    import spacy

    nlp = spacy.load("en_core_web_sm")
except (ImportError, OSError):
    nlp = None


def extract_requirement_parts(
    requirement_text: str, force_llm: bool = False, provider: str = "openai"
) -> Dict[str, List[str]]:
    """
    使用规则识别+spacy识别，之后LLM兜底。
    """
    if requirement_text is None:
        return _empty_structure()
    if not isinstance(requirement_text, str):
        try:
            if requirement_text != requirement_text:
                return _empty_structure()
        except Exception:
            return _empty_structure()
        requirement_text = str(requirement_text)
    requirement_text = requirement_text.strip()
    if not requirement_text:
        return _empty_structure()

    if not force_llm:
        local_result = _spacy_rule_based_structure(requirement_text)
        # 简单检查本地识别是否足够丰富，比如有action和expected_results，若满足则直接返回，无需请求LLM
        if (
            local_result["actions"]
            or local_result["conditions"]
            or local_result["data_ranges"]
        ):
            return local_result

    # LLM兜底
    response_text = ""
    try:
        response_text = chat_completion(
            system_prompt=REQUIREMENT_STRUCTURING_SYSTEM,
            user_prompt=requirement_structuring_prompt(requirement_text),
            provider=provider,
        )

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
            "expected_results": parsed.get("expected_results", []),
        }

    except Exception as exc:
        print(f"[Warning] Failed to parse requirement structure: {exc}")
        if response_text:
            print(f"Raw response: {response_text[:300]}...")
        return _spacy_rule_based_structure(requirement_text)


def _spacy_rule_based_structure(requirement_text: str) -> Dict[str, List[str]]:
    result = _rule_based_structure(requirement_text)
    if nlp is not None:
        doc = nlp(requirement_text)
        # 用 spacy 增强输入字段和条件
        for chunk in doc.noun_chunks:
            if chunk.text.lower() not in [item.lower() for item in result["input_fields"]]:
                # Add important nouns
                if len(chunk.text) > 2:
                    result["input_fields"].append(chunk.text)
    return result


def _rule_based_structure(requirement_text: str) -> Dict[str, List[str]]:
    text = requirement_text.lower()
    result = _empty_structure()

    if any(word in text for word in ["todo", "text", "input", "item"]):
        result["input_fields"].append("Todo text")

    ranges = re.findall(
        r"\d+\s*(?:-|to|~)\s*\d+|\d+\s*(?:characters?|chars?)",
        requirement_text,
        flags=re.I,
    )
    result["data_ranges"].extend(ranges)

    condition_keywords = {
        "empty": "Todo text is empty",
        "non-empty": "Todo text is non-empty",
        "completed": "Todo is completed",
        "complete": "Todo is completed",
        "exists": "Todo exists",
        "refresh": "Page is refreshed",
        "delete": "Todo exists before deletion",
    }
    for keyword, condition in condition_keywords.items():
        if keyword in text and condition not in result["conditions"]:
            result["conditions"].append(condition)

    action_keywords = {
        "create": "Create Todo",
        "add": "Create Todo",
        "delete": "Delete Todo",
        "remove": "Delete Todo",
        "complete": "Mark Todo as completed",
        "toggle": "Toggle Todo completion state",
        "refresh": "Refresh page",
        "save": "Persist Todo list",
        "display": "Display Todo list",
    }
    for keyword, action in action_keywords.items():
        if keyword in text and action not in result["actions"]:
            result["actions"].append(action)

    if any(word in text for word in ["reject", "not", "empty"]):
        result["expected_results"].append(
            "Invalid input is rejected and no invalid Todo is created"
        )
    elif any(word in text for word in ["delete", "remove"]):
        result["expected_results"].append("The selected Todo is removed from the list")
    elif any(word in text for word in ["complete", "completed", "toggle"]):
        result["expected_results"].append("The Todo completion state is updated")
    elif any(word in text for word in ["refresh", "persist", "save"]):
        result["expected_results"].append("Todo list data is preserved as required")
    elif any(word in text for word in ["create", "add"]):
        result["expected_results"].append("A valid Todo is created and displayed")

    return result


def _empty_structure() -> Dict[str, List[str]]:
    return {
        "input_fields": [],
        "data_ranges": [],
        "conditions": [],
        "actions": [],
        "expected_results": [],
    }
