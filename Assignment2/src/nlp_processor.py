def extract_requirement_parts(requirement_text: str) -> dict:
    text = requirement_text.lower()
    return {
        "input_fields": "todo text" if "text" in text or "todo" in text else "",
        "data_ranges": "non-empty / empty / length boundary" if "text" in text else "",
        "conditions": "derived from requirement text",
        "expected_actions": "derived from requirement text",
    }
