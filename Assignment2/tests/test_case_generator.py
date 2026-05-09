from src.coverage_identifier import identify_coverage_items
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies


def test_generate_test_cases_has_traceability():
    structured = structure_requirements(load_sample_requirements())
    risks = analyze_risks(structured)
    coverage = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage)
    test_cases = generate_test_cases(structured, coverage, strategies)
    assert {"requirement_id", "coverage_id", "technique"}.issubset(test_cases.columns)
    assert len(test_cases) == len(coverage)
