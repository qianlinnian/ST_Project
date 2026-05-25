import pandas as pd
import streamlit as st

from src.ai_client import is_llm_enabled
from src.exporter import build_traceability_matrix
from src.improvement_engine import generate_improved_test_design_with_llm
from src.performance_tracker import measure_time
from src.suite_optimizer import optimize_suite
from src.test_suite_designer import assign_test_suites_to_cases

from app_ui.actions import (
    generate_current_test_cases,
    generate_current_test_suites,
    improve_current_optimized_suite_with_llm,
    improve_current_test_suites_with_llm,
    save_test_cases,
    save_test_strategies,
    save_test_suites,
)
from app_ui.components import render_performance_table, section_header
from app_ui.state import (
    editor_safe_frame,
    queue_toast,
    rerun_with_toast,
    set_performance,
)


def render_test_cases_page(artifacts: dict[str, pd.DataFrame]) -> None:
    section_header("Test Suites", "case")
    suite_col, suite_llm_col = st.columns([1, 1], gap="medium")
    with suite_col:
        suite_disabled = artifacts["test_strategies"].empty
        if st.button("Generate Test Suites", type="primary", disabled=suite_disabled):
            with st.spinner("Generating local test suites..."):
                if not st.session_state.test_strategies_draft.empty:
                    save_test_strategies(st.session_state.test_strategies_draft)
                generate_current_test_suites()
            rerun_with_toast("Test suites generated.")
    with suite_llm_col:
        suite_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["test_suites"].empty
        )
        if st.button("Refine Suite Descriptions With LLM", disabled=suite_llm_disabled):
            with st.spinner("Improving test suite metadata with LLM..."):
                improve_current_test_suites_with_llm()
            rerun_with_toast("LLM test suite improvement completed.")

    if artifacts["test_suites"].empty:
        st.info("Generate strategy first, then generate test suites.")
    else:
        with st.form("test_suites_edit_form"):
            edited_suites = st.data_editor(
                editor_safe_frame(st.session_state.test_suites_draft),
                num_rows="dynamic",
                key="test_suites_editor",
                hide_index=True,
            )
            saved_suites = st.form_submit_button("Save Edited Test Suites")
        if saved_suites:
            save_test_suites(edited_suites)
            rerun_with_toast("Edited test suites saved.")

    suite_improvement = st.session_state.get("suite_design_improvement")
    if suite_improvement is not None and not suite_improvement.empty:
        with st.expander("LLM Test Suite Suggestions", expanded=False):
            st.dataframe(editor_safe_frame(suite_improvement), hide_index=True)

    section_header("Candidate Test Cases", "case")
    local_col, llm_col = st.columns([1, 1], gap="medium")
    with local_col:
        test_case_disabled = (
            artifacts["coverage_items"].empty
            or artifacts["test_strategies"].empty
            or artifacts["test_suites"].empty
        )
        if st.button(
            "Generate Test Cases", type="primary", disabled=test_case_disabled
        ):
            with st.spinner("Generating local test cases..."):
                generate_current_test_cases()
            rerun_with_toast("Test cases generated.")
    with llm_col:
        test_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["test_cases"].empty
        )
        if st.button(
            "Improve Test Design With LLM",
            disabled=test_llm_disabled,
        ):
            with st.spinner("Generating LLM improvement suggestions..."):
                llm_time, improvement_result = measure_time(
                    generate_improved_test_design_with_llm,
                    artifacts["structured_requirements"],
                    artifacts["coverage_items"],
                    artifacts["test_strategies"],
                    artifacts["test_cases"],
                    st.session_state.selected_provider,
                    st.session_state.selected_model,
                    batch_size=int(st.session_state.get("llm_batch_size", 25)),
                    concurrency=int(st.session_state.get("llm_concurrency", 4)),
                    test_suites=st.session_state.test_suites,
                )
                st.session_state.ai_improvement_result = improvement_result
                missing_cases = improvement_result.get(
                    "missing_test_cases", pd.DataFrame()
                )
                enhanced_cases = improvement_result.get(
                    "enhanced_test_cases", pd.DataFrame()
                )
                if not enhanced_cases.empty:
                    enhanced_cases = assign_test_suites_to_cases(
                        enhanced_cases,
                        st.session_state.test_suites,
                    )
                    st.session_state.test_cases = enhanced_cases
                    st.session_state.test_cases_draft = enhanced_cases.copy()
                    st.session_state.optimized_test_cases = improvement_result.get(
                        "optimized_test_cases",
                        optimize_suite(enhanced_cases),
                    )
                    st.session_state.optimized_test_cases = assign_test_suites_to_cases(
                        st.session_state.optimized_test_cases,
                        st.session_state.test_suites,
                    )
                    st.session_state.suite_minimization_result = None
                    st.session_state.traceability_matrix = build_traceability_matrix(
                        st.session_state.structured_requirements,
                        st.session_state.coverage_items,
                        st.session_state.test_strategies,
                        st.session_state.test_cases,
                    )
                set_performance("llm_test_design_improvement_seconds", llm_time)
                if missing_cases.empty or "llm_error" in missing_cases.columns:
                    queue_toast("LLM did not add missing test cases.")
                else:
                    queue_toast(
                        f"Added {len(missing_cases)} missing test cases with LLM."
                    )
            rerun_with_toast("LLM test design improvement completed.")
    if artifacts["test_cases"].empty:
        if artifacts["test_suites"].empty:
            st.info(
                "Generate coverage, strategy, and test suites first, then generate test cases."
            )
        else:
            st.info("Generate test cases to continue.")
    else:
        with st.form("test_cases_edit_form"):
            edited_cases = st.data_editor(
                editor_safe_frame(st.session_state.test_cases_draft),
                num_rows="dynamic",
                key="test_cases_editor",
                hide_index=True,
            )
            saved_cases = st.form_submit_button("Save Edited Test Cases")
        if saved_cases:
            save_test_cases(edited_cases)
            rerun_with_toast("Edited test cases saved.")
    if not artifacts["optimized_test_cases"].empty:
        section_header("Optimized Test Suite", "case")
        with st.expander("Optimized test suite", expanded=True):
            improve_suite_disabled = not is_llm_enabled(
                st.session_state.selected_provider
            )
            if st.button(
                "Improve Optimized Suite With LLM",
                disabled=improve_suite_disabled,
            ):
                with st.spinner("Reviewing optimized suite with LLM..."):
                    improve_current_optimized_suite_with_llm()
                rerun_with_toast("LLM optimized suite improvement completed.")
            st.dataframe(editor_safe_frame(artifacts["optimized_test_cases"]))
    section_header("Traceability Matrix", "map")
    if artifacts["traceability_matrix"].empty:
        st.info("Traceability matrix will appear after test case generation.")
    else:
        st.dataframe(editor_safe_frame(artifacts["traceability_matrix"]))
    result = st.session_state.get("ai_improvement_result")
    if result:
        missing_cases = result.get("missing_test_cases", pd.DataFrame())
        enhanced_cases = result.get("enhanced_test_cases", pd.DataFrame())
        optimized_cases = result.get("optimized_test_cases", pd.DataFrame())
        if missing_cases.empty and enhanced_cases.empty and optimized_cases.empty:
            st.session_state.ai_improvement_result = None
            result = None

    render_performance_table(artifacts)
