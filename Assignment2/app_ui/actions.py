import time

import pandas as pd
import streamlit as st

from src.ai_client import is_llm_enabled
from src.coverage_identifier import identify_coverage_items
from src.exporter import (
    COVERAGE_ITEM_COLUMNS,
    RISK_ANALYSIS_COLUMNS,
    STATE_TRANSITION_COLUMNS,
    TEST_CASE_COLUMNS,
    TEST_STRATEGY_COLUMNS,
    TEST_SUITE_COLUMNS,
    build_traceability_matrix,
    ensure_columns,
)
from src.improvement_engine import (
    improve_optimized_suite_with_llm,
    merge_coverage_improvements,
    review_and_improve_coverage_with_llm,
)
from src.performance_tracker import measure_time
from src.requirement_parser import enhance_requirements_with_llm, structure_requirements
from src.risk_analyzer import analyze_risks_with_llm_fallback
from src.state_modeler import (
    build_state_model_from_sequences,
    generate_optimized_transition_sequence,
    infer_state_model_from_requirements,
    improve_state_model_with_llm,
)
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases
from src.test_plan_document_generator import (
    generate_test_plan_document,
    improve_test_plan_document_with_llm,
)
from src.test_suite_designer import (
    assign_test_suites_to_cases,
    design_test_suites,
    improve_test_suites_with_llm,
)
from src.test_strategy_selector import select_strategies

from app_ui.state import (
    normalize_requirements,
    queue_toast,
    reset_downstream,
    set_performance,
)


def structure_current_requirements() -> None:
    normalized, messages = normalize_requirements(st.session_state.requirements)
    st.session_state.requirements = normalized
    for message in messages:
        st.toast(message)

    if st.session_state.requirements.empty:
        st.warning("Please enter, upload, or load requirements first.")
        return

    structuring_time, structured = measure_time(
        structure_requirements,
        st.session_state.requirements,
        provider=st.session_state.selected_provider,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    st.session_state.structured_requirements = structured
    set_performance("requirement_structuring_seconds", structuring_time)
    reset_downstream("structured")


def enhance_current_requirements_with_llm() -> None:
    normalized, messages = normalize_requirements(st.session_state.requirements)
    st.session_state.requirements = normalized
    for message in messages:
        st.toast(message)

    if st.session_state.requirements.empty:
        st.warning("Please enter, upload, or load requirements first.")
        return

    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    structuring_time, structured = measure_time(
        enhance_requirements_with_llm,
        st.session_state.requirements,
        provider=st.session_state.selected_provider,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    st.session_state.structured_requirements = structured
    set_performance("llm_requirement_structuring_seconds", structuring_time)
    reset_downstream("structured")


def analyze_current_risks() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return

    t_start = time.time()
    risks, timing_details = analyze_risks_with_llm_fallback(
        st.session_state.structured_requirements,
        st.session_state.selected_provider,
        st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
        fast_mode=True,
    )
    risk_time = time.time() - t_start

    st.session_state.risk_analysis = risks
    st.session_state.risk_analysis_draft = risks.copy()
    st.session_state.risk_timing_details = timing_details
    set_performance("risk_analysis_seconds", risk_time)
    reset_downstream("risk")


def generate_current_coverage() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if st.session_state.risk_analysis.empty:
        st.warning("Please analyze risks first.")
        return

    coverage_time, coverage_items = measure_time(
        identify_coverage_items,
        st.session_state.structured_requirements,
        st.session_state.risk_analysis,
    )
    st.session_state.coverage_items = coverage_items
    st.session_state.coverage_items_draft = coverage_items.copy()
    st.session_state.coverage_ai_improvement = None
    set_performance("coverage_generation_seconds", coverage_time)
    reset_downstream("strategy")


def improve_current_coverage_with_llm() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if st.session_state.coverage_items.empty:
        st.warning("Please generate coverage first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    llm_time, suggested_coverage = measure_time(
        review_and_improve_coverage_with_llm,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.selected_provider,
        st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    st.session_state.coverage_ai_improvement = suggested_coverage
    set_performance("llm_coverage_improvement_seconds", llm_time)

    if suggested_coverage.empty or "llm_error" in suggested_coverage.columns:
        return

    enhanced, stats = merge_coverage_improvements(
        st.session_state.coverage_items,
        suggested_coverage,
    )
    st.session_state.coverage_items = enhanced
    st.session_state.coverage_items_draft = enhanced.copy()
    st.session_state.coverage_ai_improvement = pd.DataFrame([stats])
    reset_downstream("strategy")


def generate_current_strategy(use_llm: bool = False) -> None:
    if st.session_state.coverage_items.empty:
        st.warning("Please generate coverage first.")
        return

    def build_strategy_artifacts() -> tuple[pd.DataFrame, pd.DataFrame]:
        strategies = select_strategies(
            st.session_state.coverage_items,
            provider=st.session_state.selected_provider,
            model=st.session_state.selected_model,
            use_llm=use_llm,
            batch_size=int(st.session_state.get("llm_batch_size", 25)),
            concurrency=int(st.session_state.get("llm_concurrency", 4)),
        )
        state_model = infer_state_model_from_requirements(
            st.session_state.structured_requirements
        )
        state_sequences = generate_optimized_transition_sequence(state_model)
        st.session_state.state_model = state_model
        return strategies, state_sequences

    strategy_time, artifacts = measure_time(build_strategy_artifacts)
    strategies, state_sequences = artifacts
    st.session_state.test_strategies = strategies
    st.session_state.test_strategies_draft = strategies.copy()
    st.session_state.state_transition_sequences = state_sequences
    st.session_state.state_transition_sequences_draft = state_sequences.copy()
    set_performance(
        (
            "llm_strategy_improvement_seconds"
            if use_llm
            else "strategy_generation_seconds"
        ),
        strategy_time,
    )
    reset_downstream("strategy")


def generate_current_test_plan_document() -> None:
    if st.session_state.coverage_items.empty or st.session_state.test_strategies.empty:
        st.warning("Please generate coverage and strategy first.")
        return

    document_time, document_markdown = measure_time(
        generate_test_plan_document,
        st.session_state.project_name,
        st.session_state.structured_requirements,
        st.session_state.risk_analysis,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.state_transition_sequences,
        st.session_state.test_suites,
        st.session_state.test_cases,
    )
    st.session_state.test_plan_document = document_markdown
    st.session_state.test_plan_document_draft = document_markdown
    set_performance("test_plan_document_generation_seconds", document_time)


def improve_current_test_plan_document_with_llm() -> None:
    if not str(st.session_state.get("test_plan_document", "")).strip():
        st.warning("Please generate the test plan document first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    llm_time, improved = measure_time(
        improve_test_plan_document_with_llm,
        st.session_state.test_plan_document,
        st.session_state.project_name,
        st.session_state.structured_requirements,
        st.session_state.risk_analysis,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.test_suites,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        use_llm=True,
    )
    if str(improved).strip():
        st.session_state.test_plan_document = improved
        st.session_state.test_plan_document_draft = improved
    set_performance("llm_test_plan_document_improvement_seconds", llm_time)


def handle_strategy_generation(use_llm: bool = False) -> None:
    if not st.session_state.coverage_items_draft.empty:
        save_coverage_items(st.session_state.coverage_items_draft)
    generate_current_strategy(use_llm=use_llm)
    st.toast(
        "LLM strategy improvement completed."
        if use_llm
        else "Coverage strategy generated."
    )


def generate_current_test_suites() -> None:
    if st.session_state.coverage_items.empty or st.session_state.test_strategies.empty:
        st.warning("Please generate coverage and strategy first.")
        return
    suite_time, suites = measure_time(
        design_test_suites,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.risk_analysis,
        st.session_state.state_transition_sequences,
    )
    st.session_state.test_suites = suites
    st.session_state.test_suites_draft = suites.copy()
    st.session_state.suite_design_improvement = None
    st.session_state.test_cases = pd.DataFrame()
    st.session_state.test_cases_draft = pd.DataFrame()
    st.session_state.optimized_test_cases = pd.DataFrame()
    st.session_state.traceability_matrix = pd.DataFrame()
    set_performance("test_suite_design_seconds", suite_time)


def improve_current_test_suites_with_llm() -> None:
    if st.session_state.test_suites.empty:
        st.warning("Please generate test suites first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return
    llm_time, result = measure_time(
        improve_test_suites_with_llm,
        st.session_state.test_suites,
        st.session_state.coverage_items,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    improved = result.get("test_suites", pd.DataFrame())
    if not improved.empty:
        st.session_state.test_suites = improved
        st.session_state.test_suites_draft = improved.copy()
        if not st.session_state.test_cases.empty:
            st.session_state.test_cases = assign_test_suites_to_cases(
                st.session_state.test_cases,
                st.session_state.test_suites,
            )
            st.session_state.test_cases_draft = st.session_state.test_cases.copy()
            st.session_state.optimized_test_cases = optimize_suite(
                st.session_state.test_cases
            )
            st.session_state.traceability_matrix = build_traceability_matrix(
                st.session_state.structured_requirements,
                st.session_state.coverage_items,
                st.session_state.test_strategies,
                st.session_state.test_cases,
            )
    st.session_state.suite_design_improvement = pd.DataFrame()
    set_performance("llm_test_suite_design_improvement_seconds", llm_time)


def improve_current_state_model_with_llm() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    model_time, state_model = measure_time(
        improve_state_model_with_llm,
        st.session_state.structured_requirements,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        use_llm=True,
    )
    st.session_state.state_model = state_model
    st.session_state.state_transition_sequences = (
        generate_optimized_transition_sequence(state_model)
    )
    st.session_state.state_transition_sequences_draft = (
        st.session_state.state_transition_sequences.copy()
    )
    set_performance("llm_state_model_improvement_seconds", model_time)
    st.session_state.test_cases = pd.DataFrame()
    st.session_state.test_cases_draft = pd.DataFrame()
    st.session_state.optimized_test_cases = pd.DataFrame()
    st.session_state.traceability_matrix = pd.DataFrame()


def save_state_transition_sequences(state_sequences: pd.DataFrame) -> None:
    normalized_sequences = ensure_columns(state_sequences, STATE_TRANSITION_COLUMNS)
    st.session_state.state_transition_sequences = normalized_sequences.copy()
    st.session_state.state_transition_sequences_draft = normalized_sequences.copy()
    existing_states = None
    if isinstance(st.session_state.state_model, dict):
        existing_states = st.session_state.state_model.get("states", [])
    st.session_state.state_model = build_state_model_from_sequences(
        normalized_sequences,
        states=existing_states,
    )
    st.session_state.test_suites = pd.DataFrame()
    st.session_state.test_suites_draft = pd.DataFrame()
    st.session_state.test_cases = pd.DataFrame()
    st.session_state.test_cases_draft = pd.DataFrame()
    st.session_state.optimized_test_cases = pd.DataFrame()
    st.session_state.traceability_matrix = pd.DataFrame()
    st.session_state.ai_improvement_result = None
    st.session_state.suite_design_improvement = None
    st.session_state.suite_minimization_result = None


def generate_current_test_cases() -> None:
    if st.session_state.coverage_items.empty or st.session_state.test_strategies.empty:
        st.warning("Please generate coverage and strategy first.")
        return
    if st.session_state.test_suites.empty:
        generate_current_test_suites()

    generation_time, test_cases = measure_time(
        generate_test_cases,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.test_suites,
        st.session_state.state_transition_sequences,
        include_state_tests=True,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        use_llm=False,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    optimized_cases = optimize_suite(test_cases)
    traceability = build_traceability_matrix(
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        test_cases,
    )
    st.session_state.test_cases = test_cases
    st.session_state.test_cases_draft = test_cases.copy()
    st.session_state.optimized_test_cases = optimized_cases
    st.session_state.traceability_matrix = traceability
    st.session_state.ai_improvement_result = None
    st.session_state.suite_minimization_result = None
    set_performance("test_case_generation_seconds", generation_time)


def improve_current_optimized_suite_with_llm() -> None:
    if st.session_state.optimized_test_cases.empty:
        st.warning("Please generate an optimized test suite first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    llm_time, result = measure_time(
        improve_optimized_suite_with_llm,
        st.session_state.optimized_test_cases,
        st.session_state.test_suites,
        st.session_state.coverage_items,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    optimized_cases = result.get("optimized_test_cases", pd.DataFrame())
    if not optimized_cases.empty:
        st.session_state.optimized_test_cases = optimized_cases
    st.session_state.suite_minimization_result = result
    set_performance("llm_suite_improve_seconds", llm_time)
    decisions = result.get("suite_minimization_decisions", pd.DataFrame())
    if decisions.empty:
        queue_toast(
            "LLM reviewed the optimized suite; no redundant cases were removed."
        )
        return
    removed = (
        int((decisions.get("status") == "applied").sum())
        if "status" in decisions.columns
        else 0
    )
    protected = (
        int((decisions.get("status") == "protected").sum())
        if "status" in decisions.columns
        else 0
    )
    if removed or protected:
        queue_toast(
            f"LLM minimization removed {removed} redundant cases, "
            f"protected {protected} high-value cases."
        )
    else:
        queue_toast("LLM reviewed the optimized suite; no safe removals were applied.")


def save_test_cases(test_cases: pd.DataFrame) -> None:
    st.session_state.test_cases = assign_test_suites_to_cases(
        ensure_columns(test_cases, TEST_CASE_COLUMNS),
        st.session_state.test_suites,
    )
    st.session_state.test_cases_draft = st.session_state.test_cases.copy()
    st.session_state.optimized_test_cases = optimize_suite(st.session_state.test_cases)
    st.session_state.ai_improvement_result = None
    st.session_state.suite_minimization_result = None
    st.session_state.traceability_matrix = build_traceability_matrix(
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.test_cases,
    )


def save_optimized_test_cases(optimized_test_cases: pd.DataFrame) -> None:
    st.session_state.optimized_test_cases = assign_test_suites_to_cases(
        ensure_columns(optimized_test_cases, TEST_CASE_COLUMNS),
        st.session_state.test_suites,
    )
    st.session_state.suite_minimization_result = None


def save_test_suites(test_suites: pd.DataFrame) -> None:
    normalized_suites = ensure_columns(test_suites, TEST_SUITE_COLUMNS)
    st.session_state.test_suites = normalized_suites.copy()
    st.session_state.test_suites_draft = normalized_suites.copy()
    st.session_state.suite_design_improvement = None
    if not st.session_state.test_cases.empty:
        st.session_state.test_cases = assign_test_suites_to_cases(
            st.session_state.test_cases,
            st.session_state.test_suites,
        )
        st.session_state.test_cases_draft = st.session_state.test_cases.copy()
        st.session_state.optimized_test_cases = optimize_suite(
            st.session_state.test_cases
        )
        st.session_state.traceability_matrix = build_traceability_matrix(
            st.session_state.structured_requirements,
            st.session_state.coverage_items,
            st.session_state.test_strategies,
            st.session_state.test_cases,
        )
    st.session_state.test_plan_document = ""
    st.session_state.test_plan_document_draft = ""


def save_risk_analysis(risk_analysis: pd.DataFrame) -> None:
    normalized_risks = ensure_columns(risk_analysis, RISK_ANALYSIS_COLUMNS)
    st.session_state.risk_analysis = normalized_risks.copy()
    st.session_state.risk_analysis_draft = normalized_risks.copy()
    reset_downstream("risk")


def save_coverage_items(coverage_items: pd.DataFrame) -> None:
    normalized_coverage = ensure_columns(coverage_items, COVERAGE_ITEM_COLUMNS)
    st.session_state.coverage_items = normalized_coverage.copy()
    st.session_state.coverage_items_draft = normalized_coverage.copy()
    st.session_state.coverage_ai_improvement = None
    st.session_state.test_strategies = pd.DataFrame()
    st.session_state.test_strategies_draft = pd.DataFrame()
    st.session_state.test_suites = pd.DataFrame()
    st.session_state.test_suites_draft = pd.DataFrame()
    reset_downstream("strategy")


def save_test_strategies(test_strategies: pd.DataFrame) -> None:
    normalized_strategies = ensure_columns(test_strategies, TEST_STRATEGY_COLUMNS)
    st.session_state.test_strategies = normalized_strategies.copy()
    st.session_state.test_strategies_draft = normalized_strategies.copy()
    st.session_state.ai_improvement_result = None
    st.session_state.suite_minimization_result = None
    reset_downstream("strategy")


def save_test_plan_document(document_markdown: str) -> None:
    st.session_state.test_plan_document = str(document_markdown or "")
    st.session_state.test_plan_document_draft = str(document_markdown or "")
