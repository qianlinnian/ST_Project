from src.ai_client import load_llm_config


def test_load_llm_config_without_key_returns_none(monkeypatch):
    monkeypatch.delenv("AUTOTESTDESIGN_LLM_API_KEY", raising=False)
    assert load_llm_config() is None
