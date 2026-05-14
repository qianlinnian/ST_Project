from src.coverage_identifier import identify_coverage_items
from src.exporter import build_traceability_matrix
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.state_modeler import generate_all_transitions_sequence
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies


def _pipeline():
    structured = structure_requirements(load_sample_requirements())
    risks = analyze_risks(structured)
    coverage = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage)
    test_cases = generate_test_cases(structured, coverage, strategies)
    return structured, coverage, strategies, test_cases


def test_generate_test_cases_has_traceability():
    _, coverage, _, test_cases = _pipeline()
    assert {"requirement_id", "coverage_id", "technique"}.issubset(test_cases.columns)
    assert len(test_cases) >= len(coverage)


def test_generated_cases_include_istqb_technique_metadata():
    _, _, _, test_cases = _pipeline()
    assert "technique_standard" in test_cases.columns
    assert test_cases["technique_standard"].str.contains("ISO/IEC/IEEE 29119-4", regex=False).any()


def test_generated_cases_include_black_box_and_state_techniques():
    _, _, _, test_cases = _pipeline()
    techniques = set(test_cases["technique"])
    assert "Equivalence Partitioning" in techniques or "Boundary Value Analysis" in techniques
    assert "State Transition Testing" in techniques


def test_state_transition_sequences_cover_all_transitions():
    transitions = generate_all_transitions_sequence()
    assert {"source_state", "event", "target_state", "expected_result"}.issubset(transitions.columns)
    assert len(transitions) >= 3


def test_optimize_suite_keeps_traceability_columns():
    _, _, _, test_cases = _pipeline()
    optimized = optimize_suite(test_cases)
    assert {"test_case_id", "requirement_id", "coverage_id"}.issubset(optimized.columns)
    assert len(optimized) <= len(test_cases)


def test_traceability_matrix_links_requirement_coverage_strategy_and_cases():
    structured, coverage, strategies, test_cases = _pipeline()
    matrix = build_traceability_matrix(structured, coverage, strategies, test_cases)
    assert {"requirement_id", "coverage_id", "test_case_id", "technique"}.issubset(matrix.columns)
    assert len(matrix) == len(test_cases)
