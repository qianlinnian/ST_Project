import streamlit as st

from src.ai_client import is_llm_enabled

from app_ui.actions import (
    generate_current_test_plan_document,
    improve_current_test_plan_document_with_llm,
    save_test_plan_document,
)
from app_ui.components import render_performance_table, section_header
from app_ui.state import rerun_with_toast


def _organization_chart_dot() -> str:
    return "\n".join(
        [
            "digraph TestPlanOrg {",
            "  rankdir=TB;",
            '  node [shape=box, style="rounded,filled", fillcolor="#FFFBEB", color="#D97706"];',
            '  "Test Lead" -> "Risk & Coverage Analyst";',
            '  "Test Lead" -> "Suite Designer";',
            '  "Test Lead" -> "Automation Engineer";',
            '  "Test Lead" -> "Reviewer / Reporter";',
            "}",
        ]
    )


@st.fragment
def _render_test_plan_document_editor() -> None:
    with st.form("test_plan_document_editor_form"):
        edited_document = st.text_area(
            "Markdown test plan document",
            value=str(st.session_state.get("test_plan_document_draft", "") or ""),
            key="test_plan_document_editor",
            height=520,
        )
        saved = st.form_submit_button("Save Edited Test Plan Document")
    if saved:
        st.session_state.test_plan_document_draft = edited_document
        save_test_plan_document(edited_document)
        rerun_with_toast("Edited test plan document saved.")


def render_test_plan_document_page(artifacts: dict[str, object]) -> None:
    section_header("Test Plan Document", "file")
    plan_col, plan_llm_col, export_col = st.columns([1, 1, 1], gap="medium")
    with plan_col:
        plan_disabled = (
            artifacts["coverage_items"].empty
            or artifacts["test_strategies"].empty
            or artifacts["state_transition_sequences"].empty
        )
        if st.button(
            "Generate Test Plan Document",
            type="primary",
            disabled=plan_disabled,
            use_container_width=True,
        ):
            with st.spinner("Generating markdown test plan document..."):
                generate_current_test_plan_document()
            rerun_with_toast("Test plan document generated.")
    with plan_llm_col:
        plan_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or not str(artifacts.get("test_plan_document", "")).strip()
        )
        if st.button(
            "Improve Test Plan Document With LLM",
            disabled=plan_llm_disabled,
            use_container_width=True,
        ):
            with st.spinner("Improving test plan document with LLM..."):
                improve_current_test_plan_document_with_llm()
            rerun_with_toast("LLM test plan document improvement completed.")
    with export_col:
        export_name = f"{str(st.session_state.project_name).strip() or 'autotestdesign'}_test_plan.md"
        st.download_button(
            "Export Test Plan Markdown",
            data=str(st.session_state.get("test_plan_document", "") or ""),
            file_name=export_name,
            mime="text/markdown",
            disabled=not str(artifacts.get("test_plan_document", "")).strip(),
            use_container_width=True,
        )

    if not str(artifacts.get("test_plan_document", "")).strip():
        st.info(
            "Generate coverage, strategy, and the state model first. If test suites or test cases already exist, they will be summarised in the document."
        )
    else:
        st.graphviz_chart(_organization_chart_dot())
        preview_tab, source_tab = st.tabs(["Rendered Preview", "Markdown Source"])
        with preview_tab:
            st.markdown(str(st.session_state.get("test_plan_document", "") or ""))
        with source_tab:
            _render_test_plan_document_editor()

    render_performance_table(artifacts)
