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


RISK_ORDER = {"High": 0, "Medium": 1, "Low": 2}
PRIORITY_ORDER = {"High": 0, "Medium": 1, "Low": 2}
VISIBLE_TEST_SUITE_COLUMNS = [
    "suite_id",
    "suite_name",
    "suite_objective",
    "coverage_ids",
    "techniques",
    "risk_level",
    "source",
    "llm_changes",
]
VISIBLE_TEST_CASE_COLUMNS = [
    "test_case_id",
    "suite_id",
    "requirement_id",
    "coverage_id",
    "precondition",
    "test_data",
    "steps",
    "expected_result",
    "source",
]
VISIBLE_OPTIMIZED_TEST_CASE_COLUMNS = [
    "test_case_id",
    "suite_id",
    "requirement_id",
    "coverage_id",
    "precondition",
    "test_data",
    "steps",
    "expected_result",
    "risk_level",
    "source",
]


def _coverage_count(value: object) -> int:
    return len([item.strip() for item in str(value or "").split(";") if item.strip()])


def _sort_test_suites_by_risk(test_suites: pd.DataFrame) -> pd.DataFrame:
    if test_suites.empty:
        return test_suites.copy()

    data = test_suites.copy()
    risk_levels = (
        data["risk_level"]
        if "risk_level" in data.columns
        else pd.Series("Medium", index=data.index, dtype=str)
    )
    priorities = (
        data["priority"]
        if "priority" in data.columns
        else pd.Series("Medium", index=data.index, dtype=str)
    )
    coverage_ids = (
        data["coverage_ids"]
        if "coverage_ids" in data.columns
        else pd.Series("", index=data.index, dtype=str)
    )
    suite_ids = (
        data["suite_id"]
        if "suite_id" in data.columns
        else pd.Series("", index=data.index, dtype=str)
    )

    data["_risk_order"] = risk_levels.map(RISK_ORDER).fillna(3)
    data["_priority_order"] = priorities.map(PRIORITY_ORDER).fillna(3)
    data["_coverage_count"] = coverage_ids.apply(_coverage_count)
    data["_suite_id_sort"] = suite_ids.astype(str)

    data = data.sort_values(
        ["_risk_order", "_priority_order", "_coverage_count", "_suite_id_sort"],
        ascending=[True, True, False, True],
        kind="stable",
    )
    return data.drop(
        columns=["_risk_order", "_priority_order", "_coverage_count", "_suite_id_sort"]
    ).reset_index(drop=True)


def _sort_test_suites_by_id(test_suites: pd.DataFrame) -> pd.DataFrame:
    if test_suites.empty or "suite_id" not in test_suites.columns:
        return test_suites.copy()
    return (
        test_suites.assign(_suite_id_sort=test_suites["suite_id"].astype(str))
        .sort_values("_suite_id_sort", ascending=True, kind="stable")
        .drop(columns=["_suite_id_sort"])
        .reset_index(drop=True)
    )


def _sort_test_suites(test_suites: pd.DataFrame, sort_option: str) -> pd.DataFrame:
    if sort_option == "Risk (High first)":
        return _sort_test_suites_by_risk(test_suites)
    return _sort_test_suites_by_id(test_suites)


def _sort_optimized_cases_by_risk(test_cases: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases.copy()

    data = test_cases.copy()
    suite_risk_levels = (
        data["suite_risk_level"]
        if "suite_risk_level" in data.columns
        else data.get("risk_level", pd.Series("Medium", index=data.index, dtype=str))
    )
    suite_priorities = (
        data["suite_priority"]
        if "suite_priority" in data.columns
        else data.get("priority", pd.Series("Medium", index=data.index, dtype=str))
    )
    risk_levels = data.get("risk_level", pd.Series("Medium", index=data.index, dtype=str))
    risk_scores = data.get("risk_score", pd.Series(0, index=data.index, dtype=float))
    suite_ids = data.get("suite_id", pd.Series("", index=data.index, dtype=str))

    data["_suite_risk_order"] = suite_risk_levels.map(RISK_ORDER).fillna(3)
    data["_suite_priority_order"] = suite_priorities.map(PRIORITY_ORDER).fillna(3)
    data["_risk_level_order"] = risk_levels.map(RISK_ORDER).fillna(3)
    data["_risk_score_order"] = pd.to_numeric(risk_scores, errors="coerce").fillna(0)
    data["_suite_id_sort"] = suite_ids.astype(str)

    data = data.sort_values(
        [
            "_suite_risk_order",
            "_suite_priority_order",
            "_risk_level_order",
            "_risk_score_order",
            "_suite_id_sort",
        ],
        ascending=[True, True, True, False, True],
        kind="stable",
    )
    return data.drop(
        columns=[
            "_suite_risk_order",
            "_suite_priority_order",
            "_risk_level_order",
            "_risk_score_order",
            "_suite_id_sort",
        ]
    ).reset_index(drop=True)


def _sort_optimized_cases_by_id(test_cases: pd.DataFrame) -> pd.DataFrame:
    if test_cases.empty:
        return test_cases.copy()

    data = test_cases.copy()
    if "suite_id" in data.columns:
        data["_suite_id_sort"] = data["suite_id"].astype(str)
    else:
        data["_suite_id_sort"] = ""
    if "test_case_id" in data.columns:
        data["_test_case_id_sort"] = data["test_case_id"].astype(str)
    else:
        data["_test_case_id_sort"] = ""

    return (
        data.sort_values(
            ["_suite_id_sort", "_test_case_id_sort"],
            ascending=[True, True],
            kind="stable",
        )
        .drop(columns=["_suite_id_sort", "_test_case_id_sort"])
        .reset_index(drop=True)
    )


def _sort_optimized_cases(test_cases: pd.DataFrame, sort_option: str) -> pd.DataFrame:
    if sort_option == "Risk (High first)":
        return _sort_optimized_cases_by_risk(test_cases)
    return _sort_optimized_cases_by_id(test_cases)


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
        suite_sort_option = st.selectbox(
            "Sort test suites by",
            [
                "Risk (High first)",
                "Suite ID (Ascending)",
            ],
            index=0,
        )
        sorted_suites = _sort_test_suites(
            st.session_state.test_suites_draft,
            suite_sort_option,
        )
        with st.form("test_suites_edit_form"):
            visible_suite_columns = [
                column
                for column in VISIBLE_TEST_SUITE_COLUMNS
                if column in sorted_suites.columns
            ]
            edited_suites = st.data_editor(
                editor_safe_frame(sorted_suites),
                num_rows="dynamic",
                key=f"test_suites_editor_{suite_sort_option}",
                hide_index=True,
                column_order=visible_suite_columns if visible_suite_columns else None,
            )
            saved_suites = st.form_submit_button("Save Edited Test Suites")
        if saved_suites:
            save_test_suites(edited_suites)
            rerun_with_toast("Edited test suites saved.")

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
            rerun_with_toast(
                f"Generated {len(st.session_state.test_cases)} candidate test cases."
            )
    with llm_col:
        test_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["test_cases"].empty
        )
        if st.button(
            "Review And Improve Test Cases With LLM",
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
                improvement_stats = improvement_result.get(
                    "test_case_improvement_stats", pd.DataFrame()
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
                    reviewed = 0
                    added = 0
                    if isinstance(improvement_stats, pd.DataFrame) and not improvement_stats.empty:
                        reviewed = int(improvement_stats.iloc[0].get("reviewed", 0) or 0)
                        added = int(improvement_stats.iloc[0].get("added", 0) or 0)
                    queue_toast(
                        f"LLM test design improvement completed. Reviewed {reviewed}, added {added}."
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
            visible_columns = [
                column
                for column in VISIBLE_TEST_CASE_COLUMNS
                if column in st.session_state.test_cases_draft.columns
            ]
            edited_cases = st.data_editor(
                editor_safe_frame(st.session_state.test_cases_draft),
                num_rows="dynamic",
                key="test_cases_editor",
                hide_index=True,
                column_order=visible_columns if visible_columns else None,
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
            optimized_sort_option = st.selectbox(
                "Sort optimized suite by",
                [
                    "Risk (High first)",
                    "ID (Ascending)",
                ],
                index=0,
            )
            if st.button(
                "Improve Optimized Suite With LLM",
                disabled=improve_suite_disabled,
            ):
                with st.spinner("Reviewing optimized suite with LLM..."):
                    improve_current_optimized_suite_with_llm()
                rerun_with_toast("LLM optimized suite improvement completed.")
            visible_optimized_columns = [
                column
                for column in VISIBLE_OPTIMIZED_TEST_CASE_COLUMNS
                if column in st.session_state.optimized_test_cases.columns
            ]
            st.dataframe(
                editor_safe_frame(
                    _sort_optimized_cases(
                        st.session_state.optimized_test_cases,
                        optimized_sort_option,
                    )
                ),
                column_order=visible_optimized_columns if visible_optimized_columns else None,
            )
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
