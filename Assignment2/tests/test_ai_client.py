from src.ai_client import is_llm_enabled, load_provider


def test_load_provider_without_key_returns_none(monkeypatch):
    monkeypatch.delenv("AUTOTESTDESIGN_LLM_DEEPSEEK_API_KEY", raising=False)
    assert load_provider("deepseek") is None


def test_is_llm_enabled_false_without_keys(monkeypatch):
    monkeypatch.delenv("AUTOTESTDESIGN_LLM_DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("AUTOTESTDESIGN_LLM_ALIYUN_API_KEY", raising=False)
    assert is_llm_enabled("deepseek") is False
