import json
from pathlib import Path

import pandas as pd

from src.coverage_identifier import identify_coverage_items
from src.exporter import STATE_TRANSITION_COLUMNS, build_traceability_matrix, ensure_columns, export_test_artifacts
from src.improvement_engine import merge_coverage_improvements
from src.improvement_engine import merge_test_case_improvements
from src.improvement_engine import improve_optimized_suite_with_llm
from src.improvement_engine import review_and_improve_coverage_with_llm
from src.improvement_engine import _apply_suite_minimization
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.state_modeler import (
    build_state_model,
    build_state_model_from_sequences,
    generate_all_transitions_sequence,
    generate_optimized_transition_sequence,
    infer_state_model_from_requirements,
)
from src.suite_optimizer import optimize_suite
from src.test_plan_document_generator import generate_test_plan_document
from src.test_suite_designer import _apply_suite_improvements, design_test_suites
from src.test_case_generator import _parse_missing_test_cases, generate_test_cases
from src.test_strategy_selector import select_strategies


def _sample_requirements() -> pd.DataFrame:
    path = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "todo_item_requirement.csv"
    )
    return pd.read_csv(path)


def _pipeline():
    structured = structure_requirements(_sample_requirements())
    risks = analyze_risks(structured)
    coverage = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage)
    state_sequences = generate_optimized_transition_sequence(
        infer_state_model_from_requirements(structured)
    )
    suites = design_test_suites(
        structured,
        coverage,
        strategies,
        risks,
        state_sequences,
    )
    test_cases = generate_test_cases(structured, coverage, strategies, suites, state_sequences)
    test_plan_document = generate_test_plan_document(
        "sample_project",
        structured,
        risks,
        coverage,
        strategies,
        state_sequences,
        suites,
        test_cases,
    )
    return structured, coverage, strategies, suites, test_cases, test_plan_document


def test_generate_test_cases_has_traceability():
    _, coverage, _, _, test_cases, _ = _pipeline()
    assert {"requirement_id", "coverage_id", "technique"}.issubset(test_cases.columns)
    assert len(test_cases) >= len(coverage)


def test_generated_cases_include_named_test_techniques():
    _, _, _, _, test_cases, _ = _pipeline()
    assert "technique" in test_cases.columns
    assert test_cases["technique"].astype(str).str.strip().ne("").all()


def test_generated_cases_include_black_box_and_state_techniques():
    _, _, _, _, test_cases, _ = _pipeline()
    techniques = set(test_cases["technique"])
    assert "Equivalence Partitioning" in techniques or "Boundary Value Analysis" in techniques
    assert "State Transition Testing" in techniques


def test_state_transition_sequences_cover_all_transitions():
    transitions = generate_all_transitions_sequence()
    assert {"source_state", "event", "target_state", "expected_result","coverage_id",}.issubset(transitions.columns)
    assert transitions["coverage_id"].astype(str).str.startswith("COV-STATE-TR-").all()
    assert len(transitions) >= 3


def test_state_transition_expected_results_describe_successful_business_transitions():
    state_model = {
        "states": ["Editing", "Active", "Deleted"],
        "transition_details": [
            {
                "transition_id": "TR-005",
                "source_state": "Editing",
                "event": "save title (non-empty after trim)",
                "target_state": "Active",
                "guard": "newTitle is not empty after trimming",
                "test_data": "newTitle: 'Buy milk'",
            },
            {
                "transition_id": "TR-006",
                "source_state": "Editing",
                "event": "save title (empty after trim)",
                "target_state": "Deleted",
                "guard": "newTitle after trimming is empty",
                "test_data": "newTitle: '   '",
            },
        ],
    }
    transitions = generate_optimized_transition_sequence(state_model)
    assert "saved successfully" in transitions.iloc[0]["expected_result"]
    assert "deletes the todo item" in transitions.iloc[1]["expected_result"]


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


def test_build_state_model_adds_states_found_in_transitions():
    state_model = build_state_model(
        states=["Active", "Completed", "Editing"],
        transitions=[
            {
                "transition_id": "TR-001",
                "source_state": "Completed",
                "event": "delete",
                "target_state": "Deleted",
            }
        ],
    )
    assert state_model["states"] == ["Active", "Completed", "Editing", "Deleted"]


def test_build_state_model_from_sequences_syncs_states_with_targets():
    sequences = pd.DataFrame(
        [
            {
                "transition_id": "TR-001",
                "coverage_id": "COV-STATE-TR-001",
                "source_state": "Completed",
                "event": "delete",
                "target_state": "Deleted",
                "guard": "todo exists",
                "test_data": "",
            }
        ]
    )
    state_model = build_state_model_from_sequences(sequences, states=["Active", "Completed"])
    assert state_model["states"] == ["Active", "Completed", "Deleted"]


def test_build_state_model_from_empty_sequences_does_not_restore_default_transitions():
    sequences = pd.DataFrame(columns=STATE_TRANSITION_COLUMNS)
    state_model = build_state_model_from_sequences(sequences, states=["Active"])
    assert state_model["states"] == ["Active"]
    assert state_model["transition_details"] == []


def test_ensure_columns_backfills_missing_state_transition_fields_for_nonempty_frames():
    partial = pd.DataFrame([{"sequence_id": "OPT-TRANS-001", "transition_id": "TR-001"}])
    normalized = ensure_columns(partial, STATE_TRANSITION_COLUMNS)
    assert list(normalized.columns[: len(STATE_TRANSITION_COLUMNS)]) == STATE_TRANSITION_COLUMNS
    assert pd.isna(normalized.loc[0, "coverage_id"])
    assert pd.isna(normalized.loc[0, "coverage_goal"])


def test_optimize_suite_keeps_traceability_columns():
    _, _, _, _, test_cases, _ = _pipeline()
    optimized = optimize_suite(test_cases)
    assert {"test_case_id", "requirement_id", "coverage_id"}.issubset(optimized.columns)
    assert len(optimized) <= len(test_cases)


def test_design_test_suites_groups_coverage_and_links_cases():
    _, coverage, _, suites, test_cases, _ = _pipeline()
    assert {"suite_id", "suite_name", "coverage_ids", "techniques"}.issubset(suites.columns)
    suite_coverage = set()
    for value in suites["coverage_ids"]:
        suite_coverage.update(part.strip() for part in str(value).split(";") if part.strip())
    assert set(coverage["coverage_id"]).issubset(suite_coverage)
    assert {"suite_id", "suite_name"}.issubset(test_cases.columns)
    assert test_cases["suite_id"].astype(str).str.strip().ne("").all()
    assert test_cases["suite_name"].astype(str).str.strip().ne("").all()
    assert suites["techniques"].astype(str).str.contains("State Transition Testing").any()


def test_design_test_suites_include_state_transition_sequence_coverage_ids():
    structured = structure_requirements(_sample_requirements())
    risks = analyze_risks(structured)
    coverage = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage)
    state_sequences = generate_optimized_transition_sequence(
        infer_state_model_from_requirements(structured)
    )
    suites = design_test_suites(
        structured,
        coverage,
        strategies,
        risks,
        state_sequences,
    )
    suite_coverage = set()
    for value in suites["coverage_ids"]:
        suite_coverage.update(part.strip() for part in str(value).split(";") if part.strip())
    state_ids = set(state_sequences["coverage_id"].astype(str))
    assert state_ids.issubset(suite_coverage)


def test_state_transition_suite_name_is_fixed():
    structured = structure_requirements(_sample_requirements())
    risks = analyze_risks(structured)
    coverage = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage)
    state_sequences = generate_optimized_transition_sequence(
        infer_state_model_from_requirements(structured)
    )
    suites = design_test_suites(
        structured,
        coverage,
        strategies,
        risks,
        state_sequences,
    )
    state_suites = suites[
        suites["techniques"].astype(str).str.contains("State Transition Testing", na=False)
    ]
    assert not state_suites.empty
    assert (state_suites["suite_name"] == "State Transition Model Suite").all()


def test_test_suite_ids_are_stable_for_same_inputs():
    structured, coverage, strategies, _, _, _ = _pipeline()
    risks = analyze_risks(structured)
    first = design_test_suites(structured, coverage, strategies, risks)
    second = design_test_suites(structured, coverage, strategies, risks)
    assert first[["suite_id", "suite_name", "coverage_ids"]].to_dict("records") == second[
        ["suite_id", "suite_name", "coverage_ids"]
    ].to_dict("records")


def test_generate_test_plan_document_contains_required_sections():
    structured = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-001",
                "module": "Todo",
                "requirement_text": "System shall reject empty title.",
            }
        ]
    )
    risks = pd.DataFrame([{"risk_id": "R-001", "requirement_id": "REQ-001", "risk_level": "High"}])
    coverage = pd.DataFrame(
        [
            {
                "coverage_id": "COV-001",
                "requirement_id": "REQ-001",
                "description": "Reject empty title input",
                "coverage_type": "Input",
                "risk_level": "High",
                "related_techniques": ["Equivalence Partitioning"],
            }
        ]
    )
    strategies = pd.DataFrame([{"coverage_id": "COV-001", "technique": "Equivalence Partitioning"}])
    suites = design_test_suites(structured, coverage, strategies, risks)
    document = generate_test_plan_document(
        "todo_app",
        structured,
        risks,
        coverage,
        strategies,
        pd.DataFrame(),
        suites,
        pd.DataFrame(),
    )
    assert "# todo_app Test Plan" in document
    assert "## 1. Project Scope" in document
    assert "## 3. High-Level Test Suite Design" in document
    assert "## 5. Organization Structure" in document
    assert "## 7. Cost Estimation" in document
    assert "```mermaid" in document
    assert "Items outside the detailed scope of this test plan" in document


def test_generate_test_plan_document_uses_existing_suites_when_available():
    structured = pd.DataFrame([{"requirement_id": "REQ-001", "module": "Todo", "requirement_text": "Create item."}])
    risks = pd.DataFrame([{"risk_id": "R-001", "requirement_id": "REQ-001", "risk_level": "Medium"}])
    coverage = pd.DataFrame([{"coverage_id": "COV-001", "requirement_id": "REQ-001", "description": "Create valid item", "coverage_type": "Functional", "risk_level": "Medium"}])
    strategies = pd.DataFrame([{"coverage_id": "COV-001", "technique": "Equivalence Partitioning"}])
    suites = pd.DataFrame(
        [
            {
                "suite_id": "TS-777",
                "suite_name": "Custom Todo Suite",
                "module": "Todo",
                "risk_level": "Medium",
                "priority": "Medium",
                "coverage_ids": "COV-001",
                "techniques": "Equivalence Partitioning",
                "coverage_types": "Functional",
                "suite_objective": "Use the custom suite row.",
                "optimization_basis": "manual",
            }
        ]
    )
    document = generate_test_plan_document(
        "todo_app",
        structured,
        risks,
        coverage,
        strategies,
        pd.DataFrame(),
        suites,
        pd.DataFrame(),
    )
    assert "TS-777" in document
    assert "Custom Todo Suite" in document


def test_generate_test_plan_document_lists_all_suite_rows_with_core_fields():
    structured = pd.DataFrame([{"requirement_id": "REQ-001", "module": "Todo", "requirement_text": "Create item."}])
    risks = pd.DataFrame([{"risk_id": "R-001", "requirement_id": "REQ-001", "risk_level": "Medium"}])
    coverage = pd.DataFrame([{"coverage_id": "COV-001", "requirement_id": "REQ-001", "description": "Create valid item", "coverage_type": "Functional", "risk_level": "Medium"}])
    strategies = pd.DataFrame([{"coverage_id": "COV-001", "technique": "Equivalence Partitioning"}])
    suites = pd.DataFrame(
        [
            {
                "suite_id": "TS-001",
                "suite_name": "Suite A",
                "module": "Todo",
                "risk_level": "High",
                "priority": "High",
                "coverage_ids": "COV-001",
                "techniques": "Equivalence Partitioning",
                "coverage_types": "Functional",
                "suite_objective": "Objective A",
                "optimization_basis": "risk",
            },
            {
                "suite_id": "TS-002",
                "suite_name": "Suite B",
                "module": "Todo",
                "risk_level": "Medium",
                "priority": "Medium",
                "coverage_ids": "COV-002",
                "techniques": "Boundary Value Analysis",
                "coverage_types": "Boundary",
                "suite_objective": "Objective B",
                "optimization_basis": "risk",
            },
        ]
    )
    document = generate_test_plan_document(
        "todo_app",
        structured,
        risks,
        coverage,
        strategies,
        pd.DataFrame(),
        suites,
        pd.DataFrame(),
    )
    assert "The number of suites listed below is consistent with the suites table: 2 suite(s)." in document
    assert document.count("| TS-001 |") == 1
    assert document.count("| TS-002 |") == 1


def test_llm_suite_improvement_only_changes_description_fields():
    _, _, _, suites, _, _ = _pipeline()
    suggestions = suites[["suite_id"]].head(1).copy()
    suggestions["suggested_suite_name"] = "Improved Suite Name"
    suggestions["suggested_objective"] = "Improved objective."
    suggestions["suggested_optimization_basis"] = "Improved basis."
    suggestions["related_coverage_ids"] = [["COV-DO-NOT-APPLY"]]
    improved = _apply_suite_improvements(suites, suggestions)
    preserved = ["suite_id", "module", "risk_level", "priority", "coverage_ids", "techniques", "coverage_types"]
    assert improved[preserved].to_dict("records") == suites[preserved].to_dict("records")
    assert improved.loc[0, "suite_name"] == "Improved Suite Name"


def test_merge_test_case_improvements_updates_existing_case_by_test_case_id():
    existing = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "requirement_id": "REQ-001",
                "coverage_id": "COV-001",
                "technique": "Equivalence Partitioning",
                "test_data": "valid input",
                "steps": "1. Do action",
                "expected_result": "Works.",
                "priority": "Medium",
                "risk_score": 3.0,
                "risk_level": "Medium",
                "coverage_type": "Functional",
                "automation_candidate": "Partial",
                "source": "Rule fallback",
                "design_basis": "Initial",
                "llm_reason": "",
            }
        ]
    )
    suggested = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "requirement_id": "REQ-001",
                "coverage_id": "COV-001",
                "technique": "Equivalence Partitioning",
                "coverage_type": "Functional",
                "test_data": "title='Buy milk'",
                "steps": "1. Submit valid title. 2. Observe saved item.",
                "expected_result": "The todo item is saved and displayed in the list.",
                "priority": "Medium",
                "risk_score": 3.0,
                "risk_level": "Medium",
                "design_basis": "LLM revised",
                "llm_reason": "clearer expected result",
                "source": "LLM updated",
            }
        ]
    )
    merged, stats = merge_test_case_improvements(existing, suggested)
    assert merged.loc[0, "expected_result"] == "The todo item is saved and displayed in the list."
    assert merged.loc[0, "source"] == "LLM updated"
    assert stats["reviewed"] == 1
    assert stats["added"] == 0


def test_parse_missing_test_cases_repairs_shifted_test_case_id_format():
    parsed = {
        "m": [
            [
                "REQ-TODO-011",
                "TC-001",
                "COV-011",
                "Equivalence Partitioning",
                "Functional",
                "valid title",
                "1. Submit title. 2. Observe list.",
                "The item is added to the list.",
                "Medium",
                "Medium",
                "clearer expected result",
            ]
        ]
    }
    repaired = _parse_missing_test_cases(parsed, batch_size=1)
    assert repaired.iloc[0]["test_case_id"] == "TC-001"
    assert repaired.iloc[0]["requirement_id"] == "REQ-TODO-011"
    assert repaired.iloc[0]["coverage_id"] == "COV-011"


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
    structured, coverage, strategies, _, test_cases, _ = _pipeline()
    matrix = build_traceability_matrix(structured, coverage, strategies, test_cases)
    assert list(matrix.columns) == [
        "requirement_id",
        "requirement_text",
        "requirement_type",
        "coverage_id",
        "coverage_description",
        "suite_id",
        "suite_name",
        "test_case_id",
        "technique",
        "risk_level",
    ]
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
    assert row["requirement_type"] == "derived"
    assert row["coverage_description"] == "State transition coverage derived from the generated behavior model"


def test_traceability_matrix_labels_original_rows():
    structured = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-1",
                "module": "TodoItem",
                "requirement_text": "Users can update the title.",
            }
        ]
    )
    coverage = pd.DataFrame([{"coverage_id": "COV-1", "requirement_id": "REQ-1", "description": "Update title"}])
    strategies = pd.DataFrame([{"coverage_id": "COV-1", "technique": "Equivalence Partitioning"}])
    test_cases = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "suite_id": "TS-001",
                "suite_name": "Title Update Suite",
                "requirement_id": "REQ-1",
                "coverage_id": "COV-1",
                "technique": "Equivalence Partitioning",
                "risk_level": "Medium",
            }
        ]
    )
    matrix = build_traceability_matrix(structured, coverage, strategies, test_cases)
    assert matrix.iloc[0]["requirement_type"] == "original"


def test_traceability_matrix_prefers_requirement_id_mapped_from_coverage():
    structured = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-1",
                "module": "TodoItem",
                "requirement_text": "Users can update the title.",
            }
        ]
    )
    coverage = pd.DataFrame(
        [{"coverage_id": "COV-1", "requirement_id": "REQ-1", "description": "Update title"}]
    )
    strategies = pd.DataFrame([{"coverage_id": "COV-1", "technique": "Equivalence Partitioning"}])
    test_cases = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "suite_id": "TS-001",
                "suite_name": "Title Update Suite",
                "requirement_id": "REQ-WRONG",
                "coverage_id": "COV-1",
                "technique": "Equivalence Partitioning",
                "risk_level": "Medium",
            }
        ]
    )
    matrix = build_traceability_matrix(structured, coverage, strategies, test_cases)
    assert matrix.iloc[0]["requirement_id"] == "REQ-1"
    assert matrix.iloc[0]["suite_id"] == "TS-001"


def test_traceability_matrix_tolerates_test_cases_missing_coverage_id_column():
    structured = pd.DataFrame([{"requirement_id": "REQ-1", "module": "M", "requirement_text": "R"}])
    coverage = pd.DataFrame([{"coverage_id": "C1", "requirement_id": "REQ-1", "description": "d"}])
    strategies = pd.DataFrame([{"coverage_id": "C1", "technique": "Equivalence Partitioning"}])
    test_cases = pd.DataFrame([{"test_case_id": "TC-1", "requirement_id": "REQ-1"}])
    matrix = build_traceability_matrix(structured, coverage, strategies, test_cases)
    assert list(matrix["test_case_id"]) == ["TC-1"]


def test_export_backfills_missing_nonempty_coverage_and_strategy_columns():
    structured = pd.DataFrame([{"requirement_id": "REQ-1", "module": "M", "requirement_text": "R"}])
    coverage = pd.DataFrame([{"requirement_id": "REQ-1", "description": "d"}])
    strategies = pd.DataFrame([{"requirement_id": "REQ-1", "technique": "Equivalence Partitioning"}])
    test_cases = pd.DataFrame([{"test_case_id": "TC-1", "requirement_id": "REQ-1"}])
    paths = export_test_artifacts(
        structured,
        coverage,
        strategies,
        test_cases,
        prefix="pytest_schema_backfill",
        export_format="csv",
    )
    exported_coverage = pd.read_csv(paths["coverage_csv"])
    exported_strategies = pd.read_csv(paths["strategies_csv"])
    assert "coverage_id" in exported_coverage.columns
    assert "coverage_id" in exported_strategies.columns


def test_export_names_candidate_cases_and_optimized_suite_separately():
    structured, coverage, strategies, suites, test_cases, test_plan_document = _pipeline()
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
        test_plan_document=test_plan_document,
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
        "test_plan_document",
        "test_suites",
        "test_cases",
        "optimized_test_cases",
        "state_transition_sequences",
        "state_model",
    }.issubset(payload)
    assert len(payload["risk_analysis"]) == len(risks)
    assert payload["test_plan_document"].startswith("# sample_project Test Plan")
    assert len(payload["state_transition_sequences"]) == len(state_sequences)


def test_generate_test_cases_preserves_specific_boundary_values_and_expected_results():
    requirements = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-TODO-004",
                "module": "Todo Validation",
                "requirement_text": "The system shall reject a Todo item title longer than 100 characters during creation or editing.",
                "data_ranges": "title:string",
                "expected_results": "todo item not saved; error shown",
            }
        ]
    )
    coverage = pd.DataFrame(
        [
            {
                "coverage_id": "COV-019",
                "requirement_id": "REQ-TODO-004",
                "description": "Test title exactly 100 characters and 101 characters to verify boundary rejection",
                "coverage_type": "Boundary",
                "risk_level": "Medium",
            }
        ]
    )
    strategies = pd.DataFrame(
        [
            {
                "coverage_id": "COV-019",
                "technique": "Boundary Value Analysis",
            }
        ]
    )
    cases = generate_test_cases(requirements, coverage, strategies, include_state_tests=False, use_llm=False)
    assert cases["test_data"].astype(str).str.contains("100 characters").any()
    assert cases["test_data"].astype(str).str.contains("101 characters").any()
    assert cases["expected_result"].astype(str).str.contains("101-character title is rejected").any()


def test_generate_test_cases_moves_trim_empty_editing_scenario_to_delete_requirement():
    requirements = pd.DataFrame(
        [
            {"requirement_id": "REQ-TODO-007", "requirement_text": "Users shall be able to update the title of an existing Todo item."},
            {"requirement_id": "REQ-TODO-008", "requirement_text": "The system shall delete a Todo item when the edited title is saved as empty after trimming."},
        ]
    )
    coverage = pd.DataFrame(
        [
            {
                "coverage_id": "COV-069",
                "requirement_id": "REQ-TODO-007",
                "description": "Test updating title with a string that after trimming becomes empty (e.g., '   ')",
                "coverage_type": "Input",
                "risk_level": "Medium",
            }
        ]
    )
    strategies = pd.DataFrame([{"coverage_id": "COV-069", "technique": "Equivalence Partitioning"}])
    cases = generate_test_cases(requirements, coverage, strategies, include_state_tests=False, use_llm=False)
    assert (cases["requirement_id"] == "REQ-TODO-008").all()
    assert cases["expected_result"].astype(str).str.contains("deleted").all()


def test_merge_coverage_improvements_adds_specific_scenario_instead_of_replacing_generic_input_coverage():
    existing = pd.DataFrame(
        [
            {
                "coverage_id": "COV-030",
                "requirement_id": "REQ-TODO-007",
                "description": "Test input field 'newTitle' with valid and invalid data",
                "coverage_type": "Input",
                "risk_level": "Medium",
                "related_techniques": ["Equivalence Partitioning"],
                "tags": ["input"],
                "notes": "",
                "source": "Rule",
            }
        ]
    )
    suggested = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-TODO-007",
                "description": "Test updating title with a string that after trimming becomes empty (e.g., '   ')",
                "coverage_type": "Input",
                "risk_level": "Medium",
                "related_techniques": ["Equivalence Partitioning"],
                "tags": ["input"],
                "notes": "",
                "reason": "specific scenario",
                "source": "LLM added",
            }
        ]
    )
    merged, stats = merge_coverage_improvements(existing, suggested)
    assert len(merged) == 2
    assert stats["added"] == 1


def test_coverage_improvements_inherit_requirement_risk_when_llm_omits_it(monkeypatch):
    requirements = pd.DataFrame(
        [
            {
                "requirement_id": "REQ-TODO-008",
                "risk_level": "High",
                "requirement_text": "Delete item when edited title becomes empty after trimming.",
            }
        ]
    )
    coverage_items = pd.DataFrame(
        [
            {
                "coverage_id": "COV-035",
                "requirement_id": "REQ-TODO-008",
                "description": "Verify core behavior: delete todo item",
                "coverage_type": "Functional",
                "risk_level": "High",
            }
        ]
    )

    def fake_enabled(_provider):
        return True

    def fake_completion(*args, **kwargs):
        return {
            "m": [
                [
                    "REQ-TODO-008",
                    "Error",
                    "Verify deletion occurs when edited title is saved as empty after trimming, and confirm item is removed from list",
                    ["Error Guessing"],
                    "Missing verification of actual deletion outcome",
                ]
            ],
            "s": "summary",
        }

    monkeypatch.setattr("src.improvement_engine.is_llm_enabled", fake_enabled)
    monkeypatch.setattr("src.improvement_engine.call_json_completion", fake_completion)

    improved = review_and_improve_coverage_with_llm(
        requirements,
        coverage_items,
        provider="fake",
        model="fake",
        use_llm=True,
        batch_size=1,
        concurrency=1,
    )
    assert improved.iloc[0]["risk_level"] == "High"


def test_improve_optimized_suite_forwards_batch_size_to_parallel_runner(monkeypatch):
    optimized_test_cases = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "suite_id": "TS-001",
                "coverage_id": "COV-001",
                "risk_level": "Medium",
                "priority": "Medium",
            },
            {
                "test_case_id": "TC-002",
                "suite_id": "TS-002",
                "coverage_id": "COV-002",
                "risk_level": "Medium",
                "priority": "Medium",
            },
        ]
    )
    test_suites = pd.DataFrame(
        [
            {"suite_id": "TS-001", "suite_name": "Suite 1"},
            {"suite_id": "TS-002", "suite_name": "Suite 2"},
        ]
    )
    coverage_items = pd.DataFrame(
        [
            {"coverage_id": "COV-001"},
            {"coverage_id": "COV-002"},
        ]
    )
    captured: dict[str, int] = {}

    monkeypatch.setattr("src.improvement_engine.is_llm_enabled", lambda _provider: True)
    monkeypatch.setattr(
        "src.improvement_engine.optimize_suite",
        lambda cases: cases.copy(),
    )

    def fake_run_parallel_batches(
        items,
        batch_size,
        concurrency,
        process_batch,
        fallback_batch=None,
        task_label=None,
    ):
        captured["batch_size"] = batch_size
        captured["concurrency"] = concurrency
        return ([{"keep": [], "drop": []}], [])

    monkeypatch.setattr(
        "src.improvement_engine.run_parallel_batches",
        fake_run_parallel_batches,
    )

    improve_optimized_suite_with_llm(
        optimized_test_cases,
        test_suites=test_suites,
        coverage_items=coverage_items,
        provider="fake",
        model="fake",
        batch_size=3,
        concurrency=2,
    )

    assert captured["batch_size"] == 3
    assert captured["concurrency"] == 2


def test_improve_optimized_suite_uses_all_suite_groups_when_batch_size_is_not_passed(monkeypatch):
    optimized_test_cases = pd.DataFrame(
        [
            {
                "test_case_id": "TC-001",
                "suite_id": "TS-001",
                "coverage_id": "COV-001",
                "risk_level": "Medium",
                "priority": "Medium",
            }
        ]
    )
    captured: dict[str, int] = {}

    monkeypatch.setattr("src.improvement_engine.is_llm_enabled", lambda _provider: True)
    monkeypatch.setattr(
        "src.improvement_engine.optimize_suite",
        lambda cases: cases.copy(),
    )

    def fake_run_parallel_batches(
        items,
        batch_size,
        concurrency,
        process_batch,
        fallback_batch=None,
        task_label=None,
    ):
        captured["batch_size"] = batch_size
        return ([{"keep": [], "drop": []}], [])

    monkeypatch.setattr(
        "src.improvement_engine.run_parallel_batches",
        fake_run_parallel_batches,
    )

    improve_optimized_suite_with_llm(
        optimized_test_cases,
        provider="fake",
        model="fake",
        batch_size=None,
        concurrency=2,
    )

    assert captured["batch_size"] == 1


def test_improve_optimized_suite_reviews_every_suite_in_batch(monkeypatch):
    optimized_test_cases = pd.DataFrame(
        [
            {"test_case_id": "TC-001", "suite_id": "TS-001", "coverage_id": "COV-001", "risk_level": "Medium", "priority": "Medium"},
            {"test_case_id": "TC-002", "suite_id": "TS-002", "coverage_id": "COV-002", "risk_level": "Medium", "priority": "Medium"},
        ]
    )
    seen_suite_ids: list[str] = []

    monkeypatch.setattr("src.improvement_engine.is_llm_enabled", lambda _provider: True)
    monkeypatch.setattr("src.improvement_engine.optimize_suite", lambda cases: cases.copy())
    monkeypatch.setattr(
        "src.improvement_engine.call_json_completion",
        lambda _system, user_prompt, **_kwargs: (
            seen_suite_ids.append(user_prompt.split("|")[1]) or {"keep": [], "drop": []}
        ),
    )

    result = improve_optimized_suite_with_llm(
        optimized_test_cases,
        provider="fake",
        model="fake",
        batch_size=2,
        concurrency=1,
    )

    assert seen_suite_ids == ["TS-001", "TS-002"]
    assert "suite_minimization_decisions" in result
