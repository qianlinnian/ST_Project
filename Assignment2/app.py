import pandas as pd
import streamlit as st

from src.ai_client import available_models, available_provider_names, chat_completion, is_llm_enabled
from src.coverage_identifier import identify_coverage_items
from src.exporter import export_csv, export_excel, export_json
from src.performance_tracker import measure_time
from src.persistence import build_project_state, list_projects, load_project, save_project
from src.prompt_templates import COVERAGE_IMPROVEMENT_SYSTEM, coverage_improvement_prompt
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies


st.set_page_config(page_title="AutoTestDesign", layout="wide")


def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {
          --surface: #f7f5f0;
          --panel: #ffffff;
          --ink: #1d1d1b;
          --muted: #6f6b63;
          --line: #ded9cf;
          --accent: #2f5d50;
          --accent-soft: #e6eee9;
        }
        .stApp {
          background: linear-gradient(180deg, #faf9f5 0%, var(--surface) 100%);
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
          background: #f1eee7;
          border-right: 1px solid var(--line);
        }
        [data-testid="stSidebar"] .stRadio > label {
          color: var(--muted);
          font-size: 0.86rem;
        }
        .hero {
          border: 1px solid var(--line);
          background: rgba(255, 255, 255, 0.74);
          border-radius: 8px;
          padding: 1.25rem 1.35rem;
          margin-bottom: 1.1rem;
          box-shadow: 0 18px 50px rgba(34, 31, 26, 0.06);
        }
        .eyebrow {
          color: var(--accent);
          font-size: 0.78rem;
          font-weight: 650;
          letter-spacing: .08em;
          text-transform: uppercase;
          margin-bottom: .35rem;
        }
        .subtle {
          color: var(--muted);
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
          border: 1px solid var(--line);
          background: rgba(255,255,255,.68);
          border-radius: 8px;
          padding: .9rem 1rem;
        }
        .metric-label {
          color: var(--muted);
          font-size: .78rem;
          margin-bottom: .35rem;
        }
        .metric-value {
          color: var(--ink);
          font-size: 1.25rem;
          font-weight: 620;
        }
        .section-card {
          border: 1px solid var(--line);
          background: rgba(255,255,255,.72);
          border-radius: 8px;
          padding: 1rem 1.05rem;
          margin-bottom: 1rem;
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
          color: var(--accent);
        }
        .stButton>button, .stDownloadButton>button {
          border-radius: 6px;
          border: 1px solid #cfc8bc;
          background: #ffffff;
          color: var(--ink);
          padding: .48rem .8rem;
          font-weight: 520;
        }
        .stButton>button:hover, .stDownloadButton>button:hover {
          border-color: var(--accent);
          color: var(--accent);
          background: var(--accent-soft);
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
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = available_models(st.session_state.get("selected_provider", "deepseek"))[0]
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = available_provider_names()[0]
    if "project_name" not in st.session_state:
        st.session_state.project_name = "simpletodolist"


def compute_artifacts() -> dict[str, pd.DataFrame]:
    requirements = st.session_state.requirements
    structuring_time, structured = measure_time(structure_requirements, requirements)
    risk_time, risks = measure_time(analyze_risks, structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    generation_time, test_cases = measure_time(generate_test_cases, structured, coverage_items, strategies)
    performance = pd.DataFrame(
        [
            {"metric": "requirement_structuring_seconds", "value": round(structuring_time, 4)},
            {"metric": "risk_analysis_seconds", "value": round(risk_time, 4)},
            {"metric": "test_case_generation_seconds", "value": round(generation_time, 4)},
        ]
    )
    traceability = test_cases[["test_case_id", "requirement_id", "coverage_id", "technique"]].copy()
    return {
        "requirements": requirements,
        "structured_requirements": structured,
        "risk_analysis": risks,
        "coverage_items": coverage_items,
        "test_strategies": strategies,
        "test_cases": test_cases,
        "traceability_matrix": traceability,
        "performance": performance,
    }


def render_metrics(artifacts: dict[str, pd.DataFrame]) -> None:
    risk_values = artifacts["risk_analysis"]["risk_level"].value_counts().to_dict()
    st.markdown(
        f"""
        <div class="metric-row">
          <div class="metric-card"><div class="metric-label">Requirements</div><div class="metric-value">{len(artifacts["requirements"])}</div></div>
          <div class="metric-card"><div class="metric-label">Coverage Items</div><div class="metric-value">{len(artifacts["coverage_items"])}</div></div>
          <div class="metric-card"><div class="metric-label">Test Cases</div><div class="metric-value">{len(artifacts["test_cases"])}</div></div>
          <div class="metric-card"><div class="metric-label">High Risk</div><div class="metric-value">{risk_values.get("High", 0)}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_style()
init_state()

with st.sidebar:
    st.markdown("### AutoTestDesign")
    page = st.radio(
        "Workflow",
        [
            "Requirement Input",
            "Structuring & Risk",
            "Coverage & Strategy",
            "Test Cases",
            "AI Review",
            "Persistence & Export",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.session_state.project_name = st.text_input("Project", st.session_state.project_name)
    providers = available_provider_names()
    st.session_state.selected_provider = st.selectbox(
        "Provider",
        providers,
        index=providers.index(st.session_state.selected_provider)
        if st.session_state.selected_provider in providers
        else 0,
    )
    models = available_models(st.session_state.selected_provider)
    st.session_state.selected_model = st.selectbox(
        "Model",
        models,
        index=models.index(st.session_state.selected_model)
        if st.session_state.selected_model in models
        else 0,
    )
    st.caption("Provider and model are used by optional LLM review.")

artifacts = compute_artifacts()

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">AI-assisted test design</div>
      <h1>AutoTestDesign</h1>
      <p class="subtle">A calm workspace for requirement analysis, risk-based prioritization, coverage review, and traceable test design.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
render_metrics(artifacts)

if page == "Requirement Input":
    with st.container():
        section_header("Requirement Input", "file")
        st.caption("Use mock requirements until the final TodoList requirements are delivered.")
        edited = st.data_editor(
            st.session_state.requirements,
            num_rows="dynamic",
            width="stretch",
            key="requirements_editor",
        )
        st.session_state.requirements = edited

if page == "Structuring & Risk":
    section_header("Requirement Structuring", "file")
    st.dataframe(artifacts["structured_requirements"], width="stretch")
    section_header("Risk Analysis", "risk")
    st.dataframe(artifacts["risk_analysis"], width="stretch")
    st.caption("Performance targets are tracked locally for reporting.")
    st.dataframe(artifacts["performance"], width="stretch")

if page == "Coverage & Strategy":
    section_header("Coverage Items", "map")
    st.dataframe(artifacts["coverage_items"], width="stretch")
    section_header("Coverage Strategy", "map")
    st.dataframe(artifacts["test_strategies"], width="stretch")

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

if page == "AI Review":
    section_header("AI Coverage Review", "ai")
    st.write(f"Selected provider: `{st.session_state.selected_provider}`")
    st.write(f"Selected model: `{st.session_state.selected_model}`")
    if not is_llm_enabled(st.session_state.selected_provider):
        st.info("Selected provider is not configured. Local rules remain available. Copy .env.example to .env to enable model calls.")
    else:
        user_prompt = coverage_improvement_prompt(
            artifacts["structured_requirements"][["requirement_id", "requirement_text"]].to_string(index=False),
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
                st.text_area("AI suggestions", result, height=300)
            except Exception as exc:
                st.error(f"AI review failed: {exc}")

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
        selected_project = st.selectbox("Saved projects", projects) if projects else None
        if selected_project and st.button("Load Project"):
            loaded = load_project(selected_project)
            st.session_state.project_name = loaded.get("project_name", st.session_state.project_name)
            st.session_state.selected_provider = loaded.get("selected_provider", st.session_state.selected_provider)
            st.session_state.selected_model = loaded.get("selected_model", st.session_state.selected_model)
            requirements_records = loaded.get("artifacts", {}).get("requirements", [])
            if requirements_records:
                st.session_state.requirements = pd.DataFrame(requirements_records)
            st.success(f"Loaded {selected_project}")

    section_header("Export Artifacts", "save")
    export_left, export_mid, export_right, export_json_col = st.columns(4, gap="medium")
    with export_left:
        if st.button("Export Risk Excel"):
            path = export_excel({"risk_analysis": artifacts["risk_analysis"]}, "risk_analysis.xlsx")
            st.success(f"Saved to {path}")
    with export_mid:
        if st.button("Export Test Cases Excel"):
            path = export_excel({"test_cases": artifacts["test_cases"]}, "test_cases.xlsx")
            st.success(f"Saved to {path}")
    with export_right:
        if st.button("Export Traceability CSV"):
            path = export_csv(artifacts["traceability_matrix"], "traceability_matrix.csv")
            st.success(f"Saved to {path}")
    with export_json_col:
        if st.button("Export Project JSON"):
            state = build_project_state(
                st.session_state.project_name,
                st.session_state.selected_provider,
                st.session_state.selected_model,
                artifacts,
            )
            path = export_json(state, "test_suite_artifacts.json")
            st.success(f"Saved to {path}")

    st.dataframe(artifacts["performance"], width="stretch")
