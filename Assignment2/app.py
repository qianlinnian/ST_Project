import streamlit as st

from src.ai_client import available_models, available_provider_names

from app_ui.components import render_llm_status, render_metrics
from app_ui.pages.coverage_strategy import render_coverage_strategy_page
from app_ui.pages.export import render_export_page
from app_ui.pages.requirement_input import render_requirement_input_page
from app_ui.pages.risk_analysis import render_risk_analysis_page
from app_ui.pages.test_cases import render_test_cases_page
from app_ui.state import (
    current_artifacts,
    flush_pending_toasts,
    init_state,
)
from app_ui.styles import inject_style


st.set_page_config(page_title="AutoTestDesign", layout="wide")


def render_sidebar() -> str:
    with st.sidebar:
        st.markdown("### AutoTestDesign Workflow")
        page = st.radio(
            "Workflow",
            [
                "Requirement Input",
                "Risk Analysis",
                "Coverage & Strategy",
                "Test Cases",
                "Export",
            ],
            label_visibility="collapsed",
        )
        st.divider()
        st.session_state.project_name = st.text_input(
            "Project", st.session_state.project_name
        )
        providers = available_provider_names()
        st.session_state.selected_provider = st.selectbox(
            "Provider",
            providers,
            index=(
                providers.index(st.session_state.selected_provider)
                if st.session_state.selected_provider in providers
                else 0
            ),
        )
        models = available_models(st.session_state.selected_provider)
        st.session_state.selected_model = st.selectbox(
            "Model",
            models,
            index=(
                models.index(st.session_state.selected_model)
                if st.session_state.selected_model in models
                else 0
            ),
        )
        with st.expander("Performance Settings", expanded=False):
            st.session_state.llm_batch_size = st.number_input(
                "LLM batch size",
                min_value=1,
                max_value=100,
                value=int(st.session_state.llm_batch_size),
                step=1,
            )
            st.session_state.llm_concurrency = st.number_input(
                "LLM concurrency",
                min_value=1,
                max_value=16,
                value=int(st.session_state.llm_concurrency),
                step=1,
            )
        st.caption(
            "Provider and model are used by optional LLM prompt-based strategy, test case, oracle, and improvement functions."
        )
    return page


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">AI-assisted test design</div>
        <h1>AutoTestDesign Workflow</h1>
          <p class="subtle">A general-purpose workspace for requirement analysis, risk-based prioritization, coverage review, and prompt-assisted traceable test design. TodoList can be used as a demonstration target, but the generator is requirement-driven and domain-neutral.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page(page: str, artifacts) -> None:
    if page == "Requirement Input":
        render_requirement_input_page(artifacts)
    if page == "Risk Analysis":
        render_risk_analysis_page(artifacts)
    if page == "Coverage & Strategy":
        render_coverage_strategy_page(artifacts)
    if page == "Test Cases":
        render_test_cases_page(artifacts)
    if page == "Export":
        render_export_page(artifacts)


def main() -> None:
    inject_style()
    init_state()
    flush_pending_toasts()

    page = render_sidebar()
    render_hero()

    artifacts = current_artifacts()
    metrics_slot = None
    llm_status_slot = None
    if page != "Requirement Input":
        metrics_slot = st.empty()
        llm_status_slot = st.empty()
        with metrics_slot.container():
            render_metrics(artifacts)
        with llm_status_slot.container():
            render_llm_status(artifacts)

    render_page(page, artifacts)

    if metrics_slot is not None and llm_status_slot is not None:
        refreshed_artifacts = current_artifacts()
        with metrics_slot.container():
            render_metrics(refreshed_artifacts)
        with llm_status_slot.container():
            render_llm_status(refreshed_artifacts)


main()
