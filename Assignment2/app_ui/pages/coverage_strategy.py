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
            with st.spinner("Reviewing and merging missing coverage with LLM..."):
                before_count = len(st.session_state.coverage_items)
                improve_current_coverage_with_llm()
                after_count = len(st.session_state.coverage_items)
            rerun_with_toast(
                f"LLM coverage improvement completed. Added {max(after_count - before_count, 0)} coverage items."
            )
    if artifacts["coverage_items"].empty:
        st.info("Run requirement structuring and risk analysis first.")
    else:
        with st.form("coverage_items_edit_form"):
            edited_coverage = st.data_editor(
                editor_safe_frame(st.session_state.coverage_items_draft),
                num_rows="dynamic",
                key="coverage_items_editor",
                hide_index=True,
            )
            saved_coverage = st.form_submit_button("Save Edited Coverage Items")
        if saved_coverage:
            save_coverage_items(edited_coverage)
            rerun_with_toast(
                "Edited coverage items saved. Regenerate strategy before test case generation."
            )

    coverage_improvement = st.session_state.get("coverage_ai_improvement")
    if coverage_improvement is not None:
        with st.expander("LLM Coverage Additions", expanded=False):
            if coverage_improvement.empty:
                st.info("LLM did not identify additional missing coverage items.")
            elif "llm_error" in coverage_improvement.columns:
                st.error(str(coverage_improvement["llm_error"].dropna().iloc[0]))
            else:
                st.metric("Added Items", len(coverage_improvement))
                st.dataframe(editor_safe_frame(coverage_improvement), hide_index=True)

    section_header("Coverage Strategy", "map")
    strategy_col, strategy_llm_col = st.columns([1, 1], gap="medium")
    with strategy_col:
        strategy_disabled = artifacts["coverage_items"].empty
        st.button(
            "Generate Strategy",
            type="primary",
            disabled=strategy_disabled,
            on_click=handle_strategy_generation,
            kwargs={"use_llm": False},
        )
    with strategy_llm_col:
        strategy_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["coverage_items"].empty
        )
        st.button(
            "Improve Strategy With LLM",
            disabled=strategy_llm_disabled,
            on_click=handle_strategy_generation,
            kwargs={"use_llm": True},
        )

    if artifacts["test_strategies"].empty:
        st.info("Coverage strategy has not been generated yet.")
    else:
        with st.form("test_strategies_edit_form"):
            edited_strategies = st.data_editor(
                editor_safe_frame(st.session_state.test_strategies_draft),
                num_rows="dynamic",
                key="test_strategies_editor",
                hide_index=True,
            )
            saved_strategies = st.form_submit_button("Save Edited Test Strategies")
        if saved_strategies:
            save_test_strategies(edited_strategies)
            rerun_with_toast("Edited test strategies saved.")

    render_state_model_section()
    render_performance_table(artifacts)
