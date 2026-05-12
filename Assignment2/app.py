import pandas as pd
import streamlit as st

from src.ai_client import (
    available_models,
    available_provider_names,
    chat_completion,
    is_llm_enabled,
)
from src.coverage_identifier import identify_coverage_items
from src.exporter import (
    build_traceability_matrix,
    export_csv,
    export_excel,
    export_json,
    export_selenium_pytest_draft,
    export_test_artifacts,
)
from src.performance_tracker import measure_time
from src.persistence import (
    build_project_state,
    list_projects,
    load_project,
    save_project,
)
from src.prompt_templates import (
    COVERAGE_IMPROVEMENT_SYSTEM,
    coverage_improvement_prompt,
)
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.state_modeler import generate_all_transitions_sequence
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies

st.set_page_config(page_title="AutoTestDesign", layout="wide")

PAGE_OPTIONS = [
    "Requirement Input",
    "Structuring & Risk",
    "Coverage & Strategy",
    "Test Cases",
    "AI Review",
    "Persistence & Export",
]


def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {
          --main-bg: #FFFBEB;
          --panel: #FFFFFF;
          --ink: #1d1d1b;
          --primary: #F59E0B;
          --primary-soft: rgba(245, 158, 11, 0.15);
          --secondary: #EF4444;
          --success: #059669;
          
          --sidebar-bg: #FEF3C7;
          --sidebar-sel-bg: #FBBF24;
          --sidebar-sel-text: #78350F;
          --sidebar-unsel-text: #92400E;
          
          --line: #ded9cf;
        }
        .stApp {
          background: var(--main-bg);
          color: var(--ink);
        }
        #MainMenu, footer {
          visibility: hidden;
        }
        [data-testid="stDecoration"] {
          display: none;
        }
        div.block-container {
          padding-top: 2.1rem;
          padding-bottom: 2.8rem;
          max-width: 1220px;
        }
        h1, h2, h3 {
          letter-spacing: 0;
          color: var(--ink);
        }
        h1 {
          font-size: 2.2rem;
          font-weight: 600;
          margin-bottom: 0.25rem;
        }
        h2, h3 {
          font-weight: 560;
        }
        [data-testid="stSidebar"] {
          background-color: var(--sidebar-bg);
          background-image: 
            linear-gradient(rgba(251, 191, 36, 0.15) 1px, transparent 1px),
            linear-gradient(90deg, rgba(251, 191, 36, 0.15) 1px, transparent 1px);
          background-size: 20px 20px;
          border-right: 1px solid rgba(251, 191, 36, 0.3);
        }
        [data-testid="stSidebar"] * {
          color: var(--sidebar-unsel-text) !important;
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
          background: transparent;
          border-radius: 6px;
          padding: 0.25rem 0.5rem;
          margin-bottom: 0.25rem;
          transition: background 0.2s;
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
          background: rgba(251, 191, 36, 0.3);
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
        [data-testid="stSidebar"] div[data-testid="stRadio"] input:checked + div {
          background-color: transparent !important;
        }
        [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] *,
        [data-testid="stSidebar"] div[data-testid="stRadio"] input:checked + div * {
          color: var(--sidebar-sel-text) !important;
          font-weight: 600;
        }
        .hero {
          border: 1px solid var(--line);
          background: var(--panel);
          border-radius: 8px;
          padding: 1.25rem 1.35rem;
          margin-bottom: 1.1rem;
          box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.05), 0 2px 4px -1px rgba(245, 158, 11, 0.03);
        }
        .eyebrow {
          color: var(--primary);
          font-size: 0.78rem;
          font-weight: 650;
          letter-spacing: .08em;
          text-transform: uppercase;
          margin-bottom: .35rem;
        }
        .subtle {
          color: #6f6b63;
          font-size: 0.98rem;
          line-height: 1.55;
          margin: 0;
        }
        .metric-row {
          display: grid;
          grid-template-columns: repeat(4, minmax(0, 1fr));
          gap: 0.8rem;
          margin: 1rem 0 1.15rem;
        }
        .metric-card {
          border: 1px solid rgba(245, 158, 11, 0.2);
          background: var(--panel);
          border-radius: 8px;
          padding: .9rem 1rem;
          box-shadow: 0 4px 6px -1px rgba(245, 158, 11, 0.05);
        }
        .metric-label {
          color: #6f6b63;
          font-size: .78rem;
          margin-bottom: .35rem;
        }
        .metric-value {
          color: var(--ink);
          font-size: 1.25rem;
          font-weight: 620;
        }
        .section-title {
          display: flex;
          align-items: center;
          gap: .45rem;
          font-size: 1rem;
          font-weight: 620;
          margin-bottom: .65rem;
        }
        .line-icon {
          width: 18px;
          height: 18px;
          color: var(--primary);
        }
        .stButton>button, .stDownloadButton>button {
          border-radius: 6px;
          border: 1px solid #cfc8bc;
          background: var(--panel);
          color: var(--ink);
          padding: .48rem .8rem;
          font-weight: 520;
        }
        .stButton>button:hover, .stDownloadButton>button:hover {
          border-color: var(--primary);
          color: var(--primary);
          background: var(--primary-soft);
        }
        [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
          border: 1px solid var(--line);
          border-radius: 8px;
          overflow: hidden;
        }
        @media (max-width: 800px) {
          div.block-container { padding: 1.25rem .9rem 2rem; }
          .metric-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .hero { padding: 1rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def line_icon(name: str) -> str:
    icons = {
        "file": '<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7z"/><path d="M14 2v5h5"/></svg>',
        "risk": '<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3 2 20h20L12 3z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
        "map": '<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 18l-6 3V6l6-3 6 3 6-3v15l-6 3-6-3z"/><path d="M9 3v15"/><path d="M15 6v15"/></svg>',
        "case": '<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M10 6h4"/><path d="M9 2h6l1 4H8l1-4z"/><rect x="4" y="6" width="16" height="16" rx="2"/></svg>',
        "ai": '<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2v4"/><path d="M12 18v4"/><path d="M4.93 4.93l2.83 2.83"/><path d="M16.24 16.24l2.83 2.83"/><path d="M2 12h4"/><path d="M18 12h4"/><circle cx="12" cy="12" r="4"/></svg>',
        "save": '<svg class="line-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><path d="M17 21v-8H7v8"/><path d="M7 3v5h8"/></svg>',
    }
    return icons.get(name, icons["file"])


def section_header(title: str, icon: str) -> None:
    st.markdown(
        f'<div class="section-title">{line_icon(icon)}<span>{title}</span></div>',
        unsafe_allow_html=True,
    )


def init_state() -> None:
    if "requirements" not in st.session_state:
        st.session_state.requirements = load_sample_requirements()
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = available_provider_names()[0]
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = available_models(
            st.session_state.selected_provider
        )[0]
    if "project_name" not in st.session_state:
        st.session_state.project_name = "simpletodolist"
    if "current_page" not in st.session_state:
        st.session_state.current_page = PAGE_OPTIONS[0]
    if st.session_state.current_page not in PAGE_OPTIONS:
        st.session_state.current_page = PAGE_OPTIONS[0]


def go_to_page(page_name: str) -> None:
    st.session_state.current_page = page_name


def render_next_step(label: str, target_page: str) -> None:
    st.divider()
    _, action_col, _ = st.columns([1, 2, 1])
    with action_col:
        st.button(
            label,
            type="primary",
            use_container_width=True,
            on_click=go_to_page,
            args=(target_page,),
        )


def compute_artifacts() -> dict[str, pd.DataFrame]:
    requirements = st.session_state.requirements
    structuring_time, structured = measure_time(structure_requirements, requirements)
    risk_time, risks = measure_time(analyze_risks, structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    generation_time, test_cases = measure_time(
        generate_test_cases, structured, coverage_items, strategies
    )
    optimized_cases = optimize_suite(test_cases)
    state_sequences = generate_all_transitions_sequence()
    traceability = build_traceability_matrix(
        structured,
        coverage_items,
        strategies,
        optimized_cases,
    )
    performance = pd.DataFrame(
        [
            {
                "metric": "requirement_structuring_seconds",
                "value": round(structuring_time, 4),
            },
            {"metric": "risk_analysis_seconds", "value": round(risk_time, 4)},
            {
                "metric": "test_case_generation_seconds",
                "value": round(generation_time, 4),
            },
        ]
    )
    return {
        "requirements": requirements,
        "structured_requirements": structured,
        "risk_analysis": risks,
        "coverage_items": coverage_items,
        "test_strategies": strategies,
        "test_cases": test_cases,
        "optimized_test_cases": optimized_cases,
        "state_transition_sequences": state_sequences,
        "traceability_matrix": traceability,
        "performance": performance,
    }


def render_metrics(artifacts: dict[str, pd.DataFrame]) -> None:
    risk_values = artifacts["risk_analysis"]["risk_level"].value_counts().to_dict()
    high_risk_count = risk_values.get("High", 0)
    risk_color_style = (
        "color: var(--secondary);" if high_risk_count > 0 else "color: var(--success);"
    )
    st.markdown(
        f"""
        <div class="metric-row">
          <div class="metric-card"><div class="metric-label">Requirements</div><div class="metric-value">{len(artifacts["requirements"])}</div></div>
          <div class="metric-card"><div class="metric-label">Coverage Items</div><div class="metric-value">{len(artifacts["coverage_items"])}</div></div>
          <div class="metric-card"><div class="metric-label">Test Cases</div><div class="metric-value">{len(artifacts["test_cases"])}</div></div>
          <div class="metric-card"><div class="metric-label">High Risk</div><div class="metric-value" style="{risk_color_style}">{high_risk_count}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def requirements_from_text(raw_text: str) -> pd.DataFrame:
    rows = []
    for index, line in enumerate(raw_text.splitlines(), start=1):
        requirement_text = line.strip()
        if not requirement_text:
            continue
        rows.append(
            {
                "requirement_id": f"REQ-TODO-{index:03d}",
                "module": "Todo",
                "requirement_text": requirement_text,
            }
        )
    return pd.DataFrame(rows, columns=["requirement_id", "module", "requirement_text"])


def render_export_paths(paths: dict[str, object]) -> None:
    st.code("\n".join(f"{name}: {path}" for name, path in paths.items()))


inject_style()
init_state()

with st.sidebar:
    st.markdown("### 🛠️ AutoTestDesign Workflow")
    page = st.radio(
        "Workflow",
        PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(st.session_state.current_page),
        key="current_page",
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
    st.caption("Provider and model are used by optional LLM review.")

artifacts = compute_artifacts()

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI-assisted test design</div>
    <h1>🛠️ AutoTestDesign Workflow</h1>
      <p class="subtle">A calm workspace for requirement analysis, risk-based prioritization, coverage review, and traceable test design.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
render_metrics(artifacts)

if page == "Requirement Input":
    with st.container():
        section_header("Requirement Input", "file")
        st.caption(
            "Import CSV requirements, paste plain text, or edit the table directly."
        )

        upload_col, text_col = st.columns([1, 1], gap="medium")
        with upload_col:
            uploaded_file = st.file_uploader("Upload CSV requirements", type=["csv"])
            if uploaded_file is not None:
                uploaded_requirements = pd.read_csv(uploaded_file)
                required_columns = {"requirement_id", "module", "requirement_text"}
                if required_columns.issubset(uploaded_requirements.columns):
                    st.session_state.requirements = uploaded_requirements[
                        ["requirement_id", "module", "requirement_text"]
                    ].copy()
                    st.success("CSV requirements loaded.")
                else:
                    st.error(
                        "CSV must include requirement_id, module, and requirement_text columns."
                    )

        with text_col:
            raw_requirements = st.text_area(
                "Paste plain-text requirements",
                placeholder="One requirement per line.",
                height=120,
            )
            if st.button("Use Text Requirements"):
                parsed_requirements = requirements_from_text(raw_requirements)
                if parsed_requirements.empty:
                    st.warning("Please enter at least one requirement.")
                else:
                    st.session_state.requirements = parsed_requirements
                    st.success("Text requirements converted to table.")

        edited = st.data_editor(
            st.session_state.requirements,
            num_rows="dynamic",
            width="stretch",
            key="requirements_editor",
        )
        st.session_state.requirements = edited
        render_next_step(
            "Next: Structure Requirements and Analyze Risk",
            "Structuring & Risk",
        )

if page == "Structuring & Risk":
    section_header("Requirement Structuring", "file")
    st.dataframe(artifacts["structured_requirements"], width="stretch")
    section_header("Risk Analysis", "risk")
    st.dataframe(artifacts["risk_analysis"], width="stretch")
    st.caption("Performance targets are tracked locally for reporting.")
    st.dataframe(artifacts["performance"], width="stretch")
    render_next_step(
        "Next: Identify Coverage and Select Strategy",
        "Coverage & Strategy",
    )

if page == "Coverage & Strategy":
    section_header("Coverage Items", "map")
    st.dataframe(artifacts["coverage_items"], width="stretch")
    section_header("Coverage Strategy", "map")
    st.dataframe(artifacts["test_strategies"], width="stretch")
    with st.expander("State transition model sequences"):
        st.dataframe(artifacts["state_transition_sequences"], width="stretch")
    render_next_step("Next: Generate and Review Test Cases", "Test Cases")

if page == "Test Cases":
    section_header("Generated Test Cases", "case")
    edited_cases = st.data_editor(
        artifacts["test_cases"],
        num_rows="dynamic",
        width="stretch",
        key="test_cases_editor",
    )
    artifacts["test_cases"] = edited_cases
    section_header("Traceability Matrix", "map")
    st.dataframe(artifacts["traceability_matrix"], width="stretch")
    with st.expander("Optimized test suite"):
        st.dataframe(artifacts["optimized_test_cases"], width="stretch")
    with st.expander("Standalone state transition tests"):
        st.dataframe(artifacts["state_transition_sequences"], width="stretch")
    render_next_step("Next: Run Optional AI Review", "AI Review")

if page == "AI Review":
    section_header("AI Coverage Review", "ai")
    st.markdown(
        f"<p style='font-size: 18px;'>Selected provider: <strong style='font-size: 20px; background-color: transparent; color: brown; padding: 4px 8px; border-radius: 4px;'>{st.session_state.selected_provider}</strong></p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='font-size: 18px;'>Selected model: <strong style='font-size: 20px; background-color: transparent; color: brown; padding: 4px 8px; border-radius: 4px;'>{st.session_state.selected_model}</strong></p>",
        unsafe_allow_html=True,
    )
    if not is_llm_enabled(st.session_state.selected_provider):
        st.info(
            "Selected provider is not configured. Local rules remain available. Copy .env.example to .env to enable model calls."
        )
    else:
        user_prompt = coverage_improvement_prompt(
            artifacts["structured_requirements"][
                ["requirement_id", "requirement_text"]
            ].to_string(index=False),
            artifacts["coverage_items"].to_string(index=False),
        )
        if st.button("Review Coverage"):
            try:
                result = chat_completion(
                    COVERAGE_IMPROVEMENT_SYSTEM,
                    user_prompt,
                    provider=st.session_state.selected_provider,
                    model=st.session_state.selected_model,
                )
                st.markdown("#### AI suggestions")
                st.markdown(result)
                with st.expander("Raw AI response"):
                    st.text_area("Raw output", result, height=240)
            except Exception as exc:
                st.error(f"AI review failed: {exc}")
    render_next_step("Next: Save and Export Artifacts", "Persistence & Export")

if page == "Persistence & Export":
    section_header("Local Project Persistence", "save")
    left, right = st.columns([1, 1], gap="medium")
    with left:
        if st.button("Save Project"):
            state = build_project_state(
                st.session_state.project_name,
                st.session_state.selected_provider,
                st.session_state.selected_model,
                artifacts,
            )
            path = save_project(state, f"{st.session_state.project_name}_project.json")
            st.success(f"Saved to {path}")
    with right:
        projects = list_projects()
        selected_project = (
            st.selectbox("Saved projects", projects) if projects else None
        )
        if selected_project and st.button("Load Project"):
            loaded = load_project(selected_project)
            st.session_state.project_name = loaded.get(
                "project_name", st.session_state.project_name
            )
            st.session_state.selected_provider = loaded.get(
                "selected_provider", st.session_state.selected_provider
            )
            st.session_state.selected_model = loaded.get(
                "selected_model", st.session_state.selected_model
            )
            requirements_records = loaded.get("artifacts", {}).get("requirements", [])
            if requirements_records:
                st.session_state.requirements = pd.DataFrame(requirements_records)
            st.success(f"Loaded {selected_project}")

    section_header("Export Artifacts", "save")
    row1_cols = st.columns(3, gap="medium")
    with row1_cols[0]:
        if st.button("Export Risk Excel", use_container_width=True):
            path = export_excel(
                {"risk_analysis": artifacts["risk_analysis"]}, "risk_analysis.xlsx"
            )
            st.success(f"Saved to {path}")
    with row1_cols[1]:
        if st.button("Export Test Cases Excel", use_container_width=True):
            path = export_excel(
                {"test_cases": artifacts["optimized_test_cases"]}, "test_cases.xlsx"
            )
            st.success(f"Saved to {path}")
    with row1_cols[2]:
        if st.button("Export Traceability CSV", use_container_width=True):
            path = export_csv(
                artifacts["traceability_matrix"], "traceability_matrix.csv"
            )
            st.success(f"Saved to {path}")

    row2_cols = st.columns(3, gap="medium")
    with row2_cols[0]:
        if st.button("Export Project JSON", use_container_width=True):
            state = build_project_state(
                st.session_state.project_name,
                st.session_state.selected_provider,
                st.session_state.selected_model,
                artifacts,
            )
            path = export_json(state, "test_suite_artifacts.json")
            st.success(f"Saved to {path}")
    with row2_cols[1]:
        if st.button("Export Full Test Design Artifacts", use_container_width=True):
            paths = export_test_artifacts(
                structured_requirements=artifacts["structured_requirements"],
                coverage_items=artifacts["coverage_items"],
                strategies=artifacts["test_strategies"],
                test_cases=artifacts["optimized_test_cases"],
                state_sequences=artifacts["state_transition_sequences"],
                prefix=st.session_state.project_name,
            )
            st.success("Full artifact export completed.")
            render_export_paths(paths)
    with row2_cols[2]:
        if st.button("Export Selenium/PyTest Draft", use_container_width=True):
            path = export_selenium_pytest_draft(artifacts["optimized_test_cases"])
            st.success(f"Saved to {path}")

    st.dataframe(artifacts["performance"], width="stretch")
