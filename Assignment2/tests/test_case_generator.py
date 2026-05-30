import pandas as pd
import json

from src.coverage_identifier import identify_coverage_items
from src.exporter import build_traceability_matrix, export_test_artifacts
from src.improvement_engine import _apply_suite_minimization
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.state_modeler import (
    generate_all_transitions_sequence,
    generate_optimized_transition_sequence,
    infer_state_model_from_requirements,
)
from src.suite_optimizer import optimize_suite
from src.test_suite_designer import _apply_suite_improvements, design_test_suites
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies


def _pipeline():
    structured = structure_requirements(load_sample_requirements())
    risks = analyze_risks(structured)
    coverage = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage)
    state_sequences = generate_optimized_transition_sequence(
        infer_state_model_from_requirements(structured)
    )
    suites = design_test_suites(structured, coverage, strategies, risks, state_sequences)
    test_cases = generate_test_cases(structured, coverage, strategies, suites, state_sequences)
    return structured, coverage, strategies, suites, test_cases


def test_generate_test_cases_has_traceability():
    _, coverage, _, _, test_cases = _pipeline()
    assert {"requirement_id", "coverage_id", "technique"}.issubset(test_cases.columns)
    assert len(test_cases) >= len(coverage)


def test_generated_cases_include_named_test_techniques():
    _, _, _, _, test_cases = _pipeline()
    assert "technique" in test_cases.columns
    assert test_cases["technique"].astype(str).str.strip().ne("").all()


def test_generated_cases_include_black_box_and_state_techniques():
    _, _, _, _, test_cases = _pipeline()
    techniques = set(test_cases["technique"])
    assert "Equivalence Partitioning" in techniques or "Boundary Value Analysis" in techniques
    assert "State Transition Testing" in techniques


def test_state_transition_sequences_cover_all_transitions():
    transitions = generate_all_transitions_sequence()
    assert {"source_state", "event", "target_state", "expected_result","coverage_id",}.issubset(transitions.columns)
    assert transitions["coverage_id"].astype(str).str.startswith("COV-STATE-TR-").all()
    assert len(transitions) >= 3


def test_optimized_transition_sequence_keeps_coverage_goal_and_removes_duplicates():
    state_model = {
        "states": ["Initial State", "Active State"],
        "transition_details": [
            {
                "transition_id": "TR-001",
                "source_state": "Initial State",
                "event": "create item",
                "target_state": "Active State",
                "guard": "valid data",
                "test_data": "valid todo",
            },
            {
                "transition_id": "TR-001-DUP",
                "source_state": "Initial State",
                "event": "create item",
                "target_state": "Active State",
                "guard": "valid data",
                "test_data": "valid todo",
            },
        ],
    }
    sequence = generate_optimized_transition_sequence(state_model)
    assert len(sequence) == 1
    assert sequence.iloc[0]["coverage_goal"] == "All Transitions"
    assert sequence.iloc[0]["coverage_id"] == "COV-STATE-TR-001"
    assert "optimization_rule" in sequence.columns


def test_optimize_suite_keeps_traceability_columns():
    _, _, _, _, test_cases = _pipeline()
    optimized = optimize_suite(test_cases)
    assert {"test_case_id", "requirement_id", "coverage_id"}.issubset(optimized.columns)
    assert len(optimized) <= len(test_cases)


def test_design_test_suites_groups_coverage_and_links_cases():
    _, coverage, _, suites, test_cases = _pipeline()
    assert {"suite_id", "suite_name", "coverage_ids", "techniques"}.issubset(suites.columns)
    suite_coverage = set()
    for value in suites["coverage_ids"]:
        suite_coverage.update(part.strip() for part in str(value).split(";") if part.strip())
    assert set(coverage["coverage_id"]).issubset(suite_coverage)
    assert {"suite_id", "suite_name"}.issubset(test_cases.columns)
    assert test_cases["suite_id"].astype(str).str.strip().ne("").all()
    assert test_cases["suite_name"].astype(str).str.strip().ne("").all()
    assert (suites["suite_name"] == "State Transition Model Suite").any()
    assert test_cases["coverage_id"].astype(str).str.startswith("COV-STATE-").any()


def test_test_suite_ids_are_stable_for_same_inputs():
    structured, coverage, strategies, _, _ = _pipeline()
    risks = analyze_risks(structured)
    first = design_test_suites(structured, coverage, strategies, risks)
    second = design_test_suites(structured, coverage, strategies, risks)
    assert first[["suite_id", "suite_name", "coverage_ids"]].to_dict("records") == second[
        ["suite_id", "suite_name", "coverage_ids"]
    ].to_dict("records")


def test_llm_suite_improvement_only_changes_description_fields():
    _, _, _, suites, _ = _pipeline()
    suggestions = suites[["suite_id"]].head(1).copy()
    suggestions["suggested_suite_name"] = "Improved Suite Name"
    suggestions["suggested_objective"] = "Improved objective."
    suggestions["suggested_optimization_basis"] = "Improved basis."
    suggestions["related_coverage_ids"] = [["COV-DO-NOT-APPLY"]]
    improved = _apply_suite_improvements(suites, suggestions)
    preserved = ["suite_id", "module", "risk_level", "priority", "coverage_ids", "techniques", "coverage_types"]
    assert improved[preserved].to_dict("records") == suites[preserved].to_dict("records")
    assert improved.loc[0, "suite_name"] == "Improved Suite Name"


def test_suite_minimization_protects_high_value_unique_coverage_and_nonempty_suite():
    cases = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "suite_id": "TS-001",
                "coverage_id": "COV-001",
                "priority": "High",
                "risk_level": "Medium",
                "risk_score": 3,
                "test_data": "a",
                "expected_result": "ok",
            },
            {
                "test_case_id": "TC-002",
                "suite_id": "TS-001",
                "coverage_id": "COV-001",
                "priority": "Low",
                "risk_level": "Low",
                "risk_score": 1,
                "test_data": "duplicate",
                "expected_result": "ok",
            },
            {
                "test_case_id": "TC-003",
                "suite_id": "TS-002",
                "coverage_id": "COV-002",
                "priority": "Low",
                "risk_level": "High",
                "risk_score": 5,
                "test_data": "b",
                "expected_result": "ok",
            },
            {
                "test_case_id": "TC-004",
                "suite_id": "TS-003",
                "coverage_id": "COV-003",
                "priority": "Low",
                "risk_level": "Low",
                "risk_score": 1,
                "test_data": "only suite case",
                "expected_result": "ok",
            },
        ]
    )
    decisions = pd.DataFrame(
        [
            {"test_case_id": "TC-001", "decision": "drop"},
            {"test_case_id": "TC-002", "decision": "drop"},
            {"test_case_id": "TC-003", "decision": "drop"},
            {"test_case_id": "TC-004", "decision": "drop"},
        ]
    )
    minimized = _apply_suite_minimization(cases, decisions)
    kept_ids = set(minimized["test_case_id"])
    assert {"TC-001", "TC-003", "TC-004"}.issubset(kept_ids)
    assert set(cases["suite_id"]).issubset(set(minimized["suite_id"]))


def test_traceability_matrix_links_requirement_coverage_strategy_and_cases():
    structured, coverage, strategies, _, test_cases = _pipeline()
    matrix = build_traceability_matrix(structured, coverage, strategies, test_cases)
    assert {"requirement_id", "coverage_id", "suite_id", "suite_name", "test_case_id", "technique"}.issubset(matrix.columns)
    assert len(matrix) == len(test_cases)


def test_traceability_matrix_labels_state_model_derived_rows():
    structured = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-1",
                "module": "TodoItem",
                "requirement_text": "Users can manage todo items.",
            }
        ]
    )
    test_cases = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "suite_id": "TS-001",
                "suite_name": "TodoItem All Transitions Suite",
                "requirement_id": "REQ-STATE-MODEL",
                "coverage_id": "COV-STATE-TR-001",
                "technique": "State Transition Testing",
            }
        ]
    )
    matrix = build_traceability_matrix(
        structured,
        pd.DataFrame(),
        pd.DataFrame(),
        test_cases,
    )
    row = matrix.iloc[0]
    assert row["requirement_text"] == "State model derived requirement"
    assert row["module"] == "TodoItem"
    assert row["coverage_description"] == "State transition coverage derived from the generated behavior model"


def test_export_names_candidate_cases_and_optimized_suite_separately():
    structured, coverage, strategies, suites, test_cases = _pipeline()
    risks = analyze_risks(structured)
    state_sequences = generate_optimized_transition_sequence(
        infer_state_model_from_requirements(structured)
    )
    state_model = infer_state_model_from_requirements(structured)
    optimized = optimize_suite(test_cases).head(max(len(test_cases) - 1, 1)).reset_index(drop=True)
    paths = export_test_artifacts(
        structured,
        coverage,
        strategies,
        test_cases,
        optimized_test_cases=optimized,
        risk_analysis=risks,
        test_suites=suites,
        state_sequences=state_sequences,
        state_model=state_model,
        prefix="pytest_suite_contract",
    )
    assert paths["risk_analysis_csv"].name.endswith("_risk_analysis.csv")
    assert paths["state_transitions_csv"].name.endswith("_state_transitions.csv")
    assert paths["test_cases_csv"].name.endswith("_test_cases.csv")
    assert paths["optimized_test_suite_csv"].name.endswith("_optimized_test_suite.csv")
    exported_risks = pd.read_csv(paths["risk_analysis_csv"])
    exported_candidates = pd.read_csv(paths["test_cases_csv"])
    exported_optimized = pd.read_csv(paths["optimized_test_suite_csv"])
    exported_traceability = pd.read_csv(paths["traceability_csv"])
    exported_state_transitions = pd.read_csv(paths["state_transitions_csv"])
    assert len(exported_risks) == len(risks)
    assert len(exported_candidates) == len(test_cases)
    assert len(exported_optimized) == len(optimized)
    assert len(exported_traceability) == len(test_cases)
    assert "coverage_id" in exported_state_transitions.columns
    assert exported_state_transitions["coverage_id"].astype(str).str.startswith("COV-STATE-TR-").all()
    payload = json.loads(paths["test_suite_json"].read_text(encoding="utf-8"))
    assert {
        "risk_analysis",
        "test_suites",
        "test_cases",
        "optimized_test_cases",
        "state_transition_sequences",
        "state_model",
    }.issubset(payload)
    assert len(payload["risk_analysis"]) == len(risks)
    assert len(payload["state_transition_sequences"]) == len(state_sequences)
