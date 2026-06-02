from pathlib import Path

import pandas as pd

from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks, analyze_risks_with_llm_fallback, _risk_level


def _sample_requirements() -> pd.DataFrame:
    return pd.read_csv(
        Path(__file__).resolve().parents[1] / "data" / "todo_item_requirement.csv"
    )


def test_analyze_risks_returns_levels():
    structured = structure_requirements(_sample_requirements())
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
    structured = structure_requirements(_sample_requirements())
    risks, timing_details = analyze_risks_with_llm_fallback(structured, provider=None)
    assert {"risk_score", "risk_level", "source"}.issubset(risks.columns)
    assert not risks.empty
    assert timing_details["method"] == "rule_fallback"


def test_risk_level_matches_matrix_boundaries():
    assert _risk_level(1) == "Low"
    assert _risk_level(2) == "Low"
    assert _risk_level(3) == "Medium"
    assert _risk_level(4) == "Medium"
    assert _risk_level(6) == "High"
    assert _risk_level(9) == "High"
