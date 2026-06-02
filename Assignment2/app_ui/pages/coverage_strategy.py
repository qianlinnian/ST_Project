import pandas as pd
import streamlit as st

from src.ai_client import is_llm_enabled

from app_ui.actions import (
    generate_current_coverage,
    handle_strategy_generation,
    improve_current_coverage_with_llm,
    save_coverage_items,
    save_risk_analysis,
    save_test_strategies,
)
from app_ui.components import (
    render_performance_table,
    render_state_model_section,
    section_header,
)
from app_ui.state import editor_safe_frame, rerun_with_toast

VISIBLE_COVERAGE_COLUMNS = [
    "coverage_id",
    "requirement_id",
    "coverage_type",
    "description",
    "risk_level",
    "source",
]

VISIBLE_STRATEGY_COLUMNS = [
    "coverage_id",
    "requirement_id",
    "coverage_type",
    "technique",
    "strategy_reason",
    "source",
]


@st.fragment
def _render_coverage_items_editor() -> None:
    coverage_draft = editor_safe_frame(st.session_state.coverage_items_draft)
    with st.form("coverage_items_editor_form"):
        edited_coverage = st.data_editor(
            coverage_draft,
            num_rows="dynamic",
            column_order=[
                column
                for column in VISIBLE_COVERAGE_COLUMNS
                if column in coverage_draft.columns
            ],
            key="coverage_items_editor",
            hide_index=True,
        )
        saved = st.form_submit_button("Save Edited Coverage Items")
    if saved:
        st.session_state.coverage_items_draft = edited_coverage
        save_coverage_items(edited_coverage)
        rerun_with_toast(
            "Edited coverage items saved. Regenerate strategy before test case generation."
        )


@st.fragment
def _render_test_strategies_editor() -> None:
    strategies_draft = editor_safe_frame(st.session_state.test_strategies_draft)
    with st.form("test_strategies_editor_form"):
        edited_strategies = st.data_editor(
            strategies_draft,
            num_rows="dynamic",
            column_order=[
                column
                for column in VISIBLE_STRATEGY_COLUMNS
                if column in strategies_draft.columns
            ],
            key="test_strategies_editor",
            hide_index=True,
        )
        saved = st.form_submit_button("Save Edited Test Strategies")
    if saved:
        st.session_state.test_strategies_draft = edited_strategies
        save_test_strategies(edited_strategies)
        rerun_with_toast("Edited test strategies saved.")


def render_coverage_strategy_page(artifacts: dict[str, pd.DataFrame]) -> None:
    section_header("Coverage Items", "map")
    local_col, llm_col = st.columns([1, 1], gap="medium")
    with local_col:
        if st.button("Generate Coverage", type="primary"):
            with st.spinner("Generating local coverage items..."):
                if not st.session_state.risk_analysis_draft.empty:
                    save_risk_analysis(st.session_state.risk_analysis_draft)
                generate_current_coverage()
            rerun_with_toast("Coverage items generated.")
    with llm_col:
        coverage_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["coverage_items"].empty
        )
        if st.button(
            "Improve Coverage With LLM",
            disabled=coverage_llm_disabled,
        ):
            with st.spinner("Reviewing and improving existing coverage with LLM..."):
                improve_current_coverage_with_llm()
                improvement_stats = st.session_state.get("coverage_ai_improvement")
                reviewed = 0
                added = 0
                if isinstance(improvement_stats, pd.DataFrame) and not improvement_stats.empty:
                    reviewed = int(improvement_stats.iloc[0].get("reviewed", 0) or 0)
                    added = int(improvement_stats.iloc[0].get("added", 0) or 0)
            rerun_with_toast(
                f"LLM coverage improvement completed. Reviewed {reviewed}, added {added}."
            )
    if artifacts["coverage_items"].empty:
        st.info("Run requirement structuring and risk analysis first.")
    else:
        _render_coverage_items_editor()

    coverage_improvement = st.session_state.get("coverage_ai_improvement")
    if coverage_improvement is not None and isinstance(coverage_improvement, pd.DataFrame):
        if not coverage_improvement.empty and "llm_error" in coverage_improvement.columns:
            st.error(str(coverage_improvement["llm_error"].dropna().iloc[0]))

    section_header("Coverage Strategy", "map")
    strategy_col, strategy_llm_col = st.columns([1, 1], gap="medium")
    with strategy_col:
        strategy_disabled = artifacts["coverage_items"].empty
        if st.button(
            "Generate Strategy",
            type="primary",
            disabled=strategy_disabled,
        ):
            with st.spinner("Generating coverage strategy..."):
                handle_strategy_generation(use_llm=False)
            rerun_with_toast("Coverage strategy generated.")
    with strategy_llm_col:
        strategy_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["coverage_items"].empty
        )
        if st.button(
            "Improve Strategy With LLM",
            disabled=strategy_llm_disabled,
        ):
            with st.spinner("Improving coverage strategy with LLM..."):
                handle_strategy_generation(use_llm=True)
            rerun_with_toast("LLM strategy improvement completed.")

    if artifacts["test_strategies"].empty:
        st.info("Coverage strategy has not been generated yet.")
    else:
        _render_test_strategies_editor()

    render_state_model_section()
    render_performance_table(artifacts)
