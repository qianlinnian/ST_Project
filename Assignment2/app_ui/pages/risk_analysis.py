import pandas as pd
import streamlit as st

from app_ui.actions import analyze_current_risks, save_risk_analysis
from app_ui.components import (
    render_performance_table,
    render_risk_timing_details,
    section_header,
)
from app_ui.state import (
    display_risk_analysis,
    editor_safe_frame,
    rerun_with_toast,
    sort_risk_analysis,
)


@st.fragment
def _render_risk_analysis_editor() -> None:
    sort_option = st.selectbox(
        "Sort risk table",
        [
            "Original order",
            "Risk level (High first)",
            "Risk score (High first)",
            "Risk score (Low first)",
        ],
        index=0,
    )
    st.session_state.risk_analysis_draft = sort_risk_analysis(
        st.session_state.risk_analysis_draft,
        sort_option,
    )
    with st.form(f"risk_analysis_editor_form_{sort_option}"):
        edited_risks = st.data_editor(
            editor_safe_frame(display_risk_analysis()),
            num_rows="dynamic",
            key=f"risk_analysis_editor_{sort_option}",
            hide_index=True,
            width="stretch",
        )
        saved = st.form_submit_button("Save Edited Risk Analysis")
    if saved:
        preserved = st.session_state.risk_analysis_draft[
            [
                column
                for column in ["risk_id", "impact", "likelihood"]
                if column in st.session_state.risk_analysis_draft.columns
            ]
        ].reset_index(drop=True)
        edited_risks = edited_risks.reset_index(drop=True)
        st.session_state.risk_analysis_draft = pd.concat(
            [preserved, edited_risks], axis=1
        )
        save_risk_analysis(st.session_state.risk_analysis_draft)
        rerun_with_toast("Edited risk analysis saved.")


def render_risk_analysis_page(artifacts: dict[str, pd.DataFrame]) -> None:
    section_header("Risk Analysis", "risk")
    if st.button("Analyze Risks", type="primary"):
        with st.spinner("Analyzing risks..."):
            analyze_current_risks()
        rerun_with_toast("Risk analysis completed.")
    if artifacts["risk_analysis"].empty:
        st.info(
            "Structure requirements on the Requirement Input page, then run risk analysis."
        )
    else:
        _render_risk_analysis_editor()
    render_performance_table(artifacts)
    render_risk_timing_details()
