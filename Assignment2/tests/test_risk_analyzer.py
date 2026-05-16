from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks, analyze_risks_with_llm_fallback


def test_analyze_risks_returns_levels():
    structured = structure_requirements(load_sample_requirements())
    risks = analyze_risks(structured)
    assert {
        "risk_id",
        "requirement_id",
        "risk_category",
        "risk_description",
        "impact",
        "likelihood",
        "risk_score",
        "risk_level",
        "reason",
        "test_suggestion",
    }.issubset(risks.columns)
    assert not risks.empty


def test_analyze_risks_with_llm_fallback_uses_rules_without_provider():
    structured = structure_requirements(load_sample_requirements())
    risks = analyze_risks_with_llm_fallback(structured, provider=None)
    assert {"risk_score", "risk_level", "source"}.issubset(risks.columns)
    assert not risks.empty
