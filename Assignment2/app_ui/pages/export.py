import pandas as pd
import streamlit as st

from src.exporter import export_test_artifacts

from app_ui.components import render_export_paths, section_header
from app_ui.state import current_artifacts, editor_safe_frame


def render_export_page(artifacts: dict[str, pd.DataFrame]) -> None:
    section_header("Export Artifacts", "save")
    artifacts = current_artifacts()
    if artifacts["test_cases"].empty:
        st.info("Generate test cases before exporting test design artifacts.")

    format_map = {
        "XLSX workbook": "xlsx",
        "CSV package": "csv",
        "JSON artifact": "json",
        "Full package": "mixed",
    }
    artifact_cols = st.columns([1.8, 0.8], gap="medium", vertical_alignment="bottom")
    with artifact_cols[0]:
        selected_format = st.selectbox(
            "Test artifact format",
            list(format_map.keys()),
            key="test_artifact_export_format",
        )
    with artifact_cols[1]:
        if st.button(
            "Export Test Design Artifacts", type="primary", use_container_width=True
        ):
            paths = export_test_artifacts(
                structured_requirements=artifacts["structured_requirements"],
                risk_analysis=artifacts["risk_analysis"],
                coverage_items=artifacts["coverage_items"],
                strategies=artifacts["test_strategies"],
                test_suites=artifacts["test_suites"],
                test_cases=artifacts["test_cases"],
                optimized_test_cases=artifacts["optimized_test_cases"],
                state_sequences=artifacts["state_transition_sequences"],
                state_model=st.session_state.state_model,
                prefix=st.session_state.project_name,
                export_format=format_map[selected_format],
            )
            st.session_state.last_export_paths = paths
            st.toast("Test artifact export completed.")
    st.caption("Exports generated test design artifacts, not local project state.")

    if st.session_state.last_export_paths:
        render_export_paths(st.session_state.last_export_paths)
