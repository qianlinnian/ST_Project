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
from src.risk_analyzer import analyze_risks_with_llm_fallback
from src.state_modeler import (
    generate_all_transitions_sequence,
    infer_state_model_from_requirements,
)
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies
from src.improvement_engine import generate_improved_test_design_with_llm

st.set_page_config(page_title="AutoTestDesign", layout="wide")


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
        st.session_state.requirements = empty_requirements()
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = available_provider_names()[0]
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = available_models(
            st.session_state.selected_provider
        )[0]
    if "project_name" not in st.session_state:
        st.session_state.project_name = "sample_project"
    if "requirements_draft" not in st.session_state:
        st.session_state.requirements_draft = st.session_state.requirements.copy()
    if "risk_analysis_draft" not in st.session_state:
        st.session_state.risk_analysis_draft = pd.DataFrame()
    if "coverage_items_draft" not in st.session_state:
        st.session_state.coverage_items_draft = pd.DataFrame()
    if "test_strategies_draft" not in st.session_state:
        st.session_state.test_strategies_draft = pd.DataFrame()
    if "test_cases_draft" not in st.session_state:
        st.session_state.test_cases_draft = pd.DataFrame()
    for key in [
        "structured_requirements",
        "risk_analysis",
        "coverage_items",
        "test_strategies",
        "test_cases",
        "optimized_test_cases",
        "state_transition_sequences",
        "traceability_matrix",
        "performance",
    ]:
        if key not in st.session_state:
            st.session_state[key] = pd.DataFrame()


def empty_requirements() -> pd.DataFrame:
    return pd.DataFrame(columns=["requirement_id", "module", "requirement_text"])


def current_artifacts() -> dict[str, pd.DataFrame]:
    return {
        "requirements": st.session_state.requirements,
        "structured_requirements": st.session_state.structured_requirements,
        "risk_analysis": st.session_state.risk_analysis,
        "coverage_items": st.session_state.coverage_items,
        "test_strategies": st.session_state.test_strategies,
        "test_cases": st.session_state.test_cases,
        "optimized_test_cases": st.session_state.optimized_test_cases,
        "state_transition_sequences": st.session_state.state_transition_sequences,
        "traceability_matrix": st.session_state.traceability_matrix,
        "performance": st.session_state.performance,
    }


def compact_structured_requirements() -> pd.DataFrame:
    columns = [
        "requirement_id",
        "requirement_text",
        "input_fields",
        "data_ranges",
        "conditions",
        "actions",
        "expected_results",
    ]
    available_columns = [
        column
        for column in columns
        if column in st.session_state.structured_requirements.columns
    ]
    return st.session_state.structured_requirements[available_columns].copy()


def display_risk_analysis() -> pd.DataFrame:
    hidden_columns = {"risk_id", "impact", "likelihood"}
    return st.session_state.risk_analysis_draft.drop(
        columns=[
            column
            for column in hidden_columns
            if column in st.session_state.risk_analysis_draft.columns
        ],
        errors="ignore",
    ).copy()


def normalize_requirements(requirements: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    messages = []
    rows = []
    used_ids = set()
    next_id = 1

    required_columns = ["requirement_id", "module", "requirement_text"]
    if requirements is None or requirements.empty:
        return empty_requirements(), messages

    for _, row in requirements.iterrows():
        requirement_text = row.get("requirement_text", "")
        if requirement_text is None or requirement_text != requirement_text:
            requirement_text = ""
        requirement_text = str(requirement_text).strip()
        if not requirement_text:
            continue

        module = row.get("module", "")
        if module is None or module != module or not str(module).strip():
            module = "General"
        else:
            module = str(module).strip()

        raw_id = row.get("requirement_id", "")
        if raw_id is None or raw_id != raw_id or not str(raw_id).strip():
            requirement_id = f"REQ-{next_id:03d}"
            next_id += 1
            messages.append(f"Filled missing requirement id with {requirement_id}.")
        else:
            requirement_id = str(raw_id).strip()

        original_id = requirement_id
        suffix = 2
        while requirement_id in used_ids:
            requirement_id = f"{original_id}-{suffix}"
            suffix += 1
        if requirement_id != original_id:
            messages.append(
                f"Renamed duplicate requirement id {original_id} to {requirement_id}."
            )

        used_ids.add(requirement_id)
        rows.append(
            {
                "requirement_id": requirement_id,
                "module": module,
                "requirement_text": requirement_text,
            }
        )

    return pd.DataFrame(rows, columns=required_columns), messages


def save_requirements(requirements: pd.DataFrame) -> None:
    normalized, messages = normalize_requirements(requirements)
    st.session_state.requirements = normalized
    st.session_state.requirements_draft = normalized.copy()
    reset_downstream("requirements")
    for message in messages:
        st.toast(message)


def set_performance(metric: str, value: float) -> None:
    performance = st.session_state.performance
    row = pd.DataFrame([{"metric": metric, "value": round(value, 4)}])
    if performance.empty or "metric" not in performance.columns:
        st.session_state.performance = row
        return

    performance = performance[performance["metric"] != metric]
    st.session_state.performance = pd.concat([performance, row], ignore_index=True)


def reset_downstream(from_step: str) -> None:
    order = {
        "requirements": [
            "structured_requirements",
            "risk_analysis",
            "risk_analysis_draft",
            "coverage_items",
            "coverage_items_draft",
            "test_strategies",
            "test_strategies_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "traceability_matrix",
            "performance",
        ],
        "structured": [
            "risk_analysis",
            "risk_analysis_draft",
            "coverage_items",
            "coverage_items_draft",
            "test_strategies",
            "test_strategies_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "traceability_matrix",
        ],
        "risk": [
            "coverage_items",
            "coverage_items_draft",
            "test_strategies",
            "test_strategies_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "traceability_matrix",
        ],
        "strategy": [
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "traceability_matrix",
        ],
    }
    for key in order.get(from_step, []):
        st.session_state[key] = pd.DataFrame()


def structure_current_requirements() -> None:
    normalized, messages = normalize_requirements(st.session_state.requirements)
    st.session_state.requirements = normalized
    for message in messages:
        st.toast(message)

    if st.session_state.requirements.empty:
        st.warning("Please enter, upload, or load requirements first.")
        return

    structuring_time, structured = measure_time(
        structure_requirements, st.session_state.requirements
    )
    st.session_state.structured_requirements = structured
    set_performance("requirement_structuring_seconds", structuring_time)
    reset_downstream("structured")


def analyze_current_risks() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return

    risk_time, risks = measure_time(
        analyze_risks_with_llm_fallback,
        st.session_state.structured_requirements,
        st.session_state.selected_provider,
        st.session_state.selected_model,
    )
    st.session_state.risk_analysis = risks
    st.session_state.risk_analysis_draft = risks.copy()
    set_performance("risk_analysis_seconds", risk_time)
    reset_downstream("risk")


def generate_current_strategy() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if st.session_state.risk_analysis.empty:
        st.warning("Please analyze risks first.")
        return

    coverage_items = identify_coverage_items(
        st.session_state.structured_requirements,
        st.session_state.risk_analysis,
    )
    provider = st.session_state.selected_provider
    model = st.session_state.selected_model
    strategies = select_strategies(coverage_items, provider=provider, model=model)
    state_sequences = generate_all_transitions_sequence(
        infer_state_model_from_requirements(st.session_state.structured_requirements)
    )
    st.session_state.coverage_items = coverage_items
    st.session_state.test_strategies = strategies
    st.session_state.coverage_items_draft = coverage_items.copy()
    st.session_state.test_strategies_draft = strategies.copy()
    st.session_state.state_transition_sequences = state_sequences
    reset_downstream("strategy")


def generate_current_test_cases() -> None:
    if st.session_state.coverage_items.empty or st.session_state.test_strategies.empty:
        st.warning("Please generate coverage and strategy first.")
        return

    generation_time, test_cases = measure_time(
        generate_test_cases,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        True,
        st.session_state.selected_provider,
        st.session_state.selected_model,
    )
    optimized_cases = optimize_suite(test_cases)
    traceability = build_traceability_matrix(
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        optimized_cases,
    )
    st.session_state.test_cases = test_cases
    st.session_state.test_cases_draft = test_cases.copy()
    st.session_state.optimized_test_cases = optimized_cases
    st.session_state.traceability_matrix = traceability
    set_performance("test_case_generation_seconds", generation_time)


def save_test_cases(test_cases: pd.DataFrame) -> None:
    st.session_state.test_cases = test_cases.copy()
    st.session_state.test_cases_draft = test_cases.copy()
    st.session_state.optimized_test_cases = optimize_suite(st.session_state.test_cases)
    st.session_state.traceability_matrix = build_traceability_matrix(
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.optimized_test_cases,
    )


def save_risk_analysis(risk_analysis: pd.DataFrame) -> None:
    st.session_state.risk_analysis = risk_analysis.copy()
    st.session_state.risk_analysis_draft = risk_analysis.copy()
    reset_downstream("risk")


def save_coverage_items(coverage_items: pd.DataFrame) -> None:
    st.session_state.coverage_items = coverage_items.copy()
    st.session_state.coverage_items_draft = coverage_items.copy()
    st.session_state.test_strategies = pd.DataFrame()
    st.session_state.test_strategies_draft = pd.DataFrame()
    reset_downstream("strategy")


def save_test_strategies(test_strategies: pd.DataFrame) -> None:
    st.session_state.test_strategies = test_strategies.copy()
    st.session_state.test_strategies_draft = test_strategies.copy()
    reset_downstream("strategy")


def render_llm_status(artifacts: dict[str, pd.DataFrame]) -> None:
    messages = []
    for artifact_name in [
        "risk_analysis",
        "test_strategies",
        "test_cases",
        "optimized_test_cases",
    ]:
        artifact = artifacts.get(artifact_name, pd.DataFrame())
        if not artifact.empty and "llm_error" in artifact.columns:
            errors = [str(error) for error in artifact["llm_error"].dropna().unique() if str(error)]
            for error in errors:
                messages.append(f"{artifact_name}: {error}")
    if messages:
        st.warning(
            "LLM call did not complete successfully. Local rule fallback was used.\n\n"
            + "\n\n".join(messages)
            + "\n\nTry a faster model, switch provider, check API quota/permissions, "
            "or increase AUTOTESTDESIGN_LLM_TIMEOUT in Assignment2/.env."
        )


def render_metrics(artifacts: dict[str, pd.DataFrame]) -> None:
    risk_values = (
        artifacts["risk_analysis"]["risk_level"].value_counts().to_dict()
        if not artifacts["risk_analysis"].empty
        and "risk_level" in artifacts["risk_analysis"].columns
        else {}
    )
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
                "requirement_id": f"REQ-{index:03d}",
                "module": "General",
                "requirement_text": requirement_text,
            }
        )
    return pd.DataFrame(rows, columns=["requirement_id", "module", "requirement_text"])


def render_export_paths(paths: dict[str, object]) -> None:
    st.code("\n".join(f"{name}: {path}" for name, path in paths.items()))


def render_ai_text_result(key: str, text: str) -> None:
    st.session_state[key] = text
    st.markdown(text)


inject_style()
init_state()

with st.sidebar:
    st.markdown("### AutoTestDesign Workflow")
    page = st.radio(
        "Workflow",
        [
            "Requirement Input",
            "Risk Analysis",
            "Coverage & Strategy",
            "Test Cases",
            "Persistence & Export",
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
    st.caption("Provider and model are used by optional LLM prompt-based strategy, test case, oracle, and improvement functions.")

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

artifacts = current_artifacts()
if page != "Requirement Input":
    render_metrics(artifacts)
    render_llm_status(artifacts)

if page == "Requirement Input":
    with st.container():
        section_header("Requirement Input", "file")
        st.caption(
            "Import CSV requirements, paste plain text, or edit the table directly."
        )

        if st.button("Load Sample Requirements", width="stretch"):
            save_requirements(load_sample_requirements())
            st.toast("Sample requirements loaded.")

        upload_col, text_col = st.columns([1, 1], gap="medium")
        with upload_col:
            uploaded_file = st.file_uploader("Upload CSV requirements", type=["csv"])
            if uploaded_file is not None:
                uploaded_requirements = pd.read_csv(uploaded_file)
                required_columns = {"requirement_id", "module", "requirement_text"}
                if required_columns.issubset(uploaded_requirements.columns):
                    save_requirements(
                        uploaded_requirements[
                            ["requirement_id", "module", "requirement_text"]
                        ].copy()
                    )
                    st.toast("CSV requirements loaded.")
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
                    save_requirements(parsed_requirements)
                    st.toast("Text requirements converted to table.")

        edited = st.data_editor(
            st.session_state.requirements_draft,
            num_rows="dynamic",
            key="requirements_editor",
            width="stretch",
            hide_index=True,
            column_order=["requirement_id", "module", "requirement_text"],
        )
        st.session_state.requirements_draft = edited
        if st.button("Save Edited Requirements", width="stretch"):
            save_requirements(st.session_state.requirements_draft)
            st.toast("Edited requirements saved.")

        if st.button("Structure Requirements", type="primary", width="stretch"):
            with st.spinner("Structuring requirements..."):
                save_requirements(st.session_state.requirements_draft)
                structure_current_requirements()
            if not st.session_state.structured_requirements.empty:
                st.toast("Requirement structuring completed.")

        if not st.session_state.structured_requirements.empty:
            section_header("Structured Requirement Preview", "file")
            st.dataframe(compact_structured_requirements(), width="stretch")

if page == "Risk Analysis":
    section_header("Risk Analysis", "risk")
    if st.button("Analyze Risks", type="primary", width="stretch"):
        with st.spinner("Analyzing risks..."):
            analyze_current_risks()
        artifacts = current_artifacts()
    if artifacts["risk_analysis"].empty:
        st.info("Structure requirements on the Requirement Input page, then run risk analysis.")
    else:
        edited_risks = st.data_editor(
            display_risk_analysis(),
            num_rows="dynamic",
            key="risk_analysis_editor",
            width="stretch",
            hide_index=True,
        )
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
        if st.button("Save Edited Risk Analysis", width="stretch"):
            save_risk_analysis(st.session_state.risk_analysis_draft)
            st.toast("Edited risk analysis saved.")
    if not artifacts["performance"].empty:
        st.caption("Performance targets are tracked locally for reporting.")
        st.dataframe(artifacts["performance"])

if page == "Coverage & Strategy":
    section_header("Coverage Items", "map")
    if st.button("Generate Coverage & Strategy", type="primary", width="stretch"):
        with st.spinner("Generating coverage items and strategy..."):
            if not st.session_state.risk_analysis_draft.empty:
                save_risk_analysis(st.session_state.risk_analysis_draft)
            generate_current_strategy()
        artifacts = current_artifacts()
    if artifacts["coverage_items"].empty:
        st.info("Run requirement structuring and risk analysis first.")
    else:
        with st.form("coverage_items_edit_form"):
            edited_coverage = st.data_editor(
                st.session_state.coverage_items_draft,
                num_rows="dynamic",
                key="coverage_items_editor",
                width="stretch",
                hide_index=True,
            )
            saved_coverage = st.form_submit_button(
                "Save Edited Coverage Items", width="stretch"
            )
        if saved_coverage:
            save_coverage_items(edited_coverage)
            artifacts = current_artifacts()
            st.toast("Edited coverage items saved. Regenerate strategy before test case generation.")
    section_header("Coverage Strategy", "map")
    if artifacts["test_strategies"].empty:
        st.info("Coverage strategy has not been generated yet.")
    else:
        with st.form("test_strategies_edit_form"):
            edited_strategies = st.data_editor(
                st.session_state.test_strategies_draft,
                num_rows="dynamic",
                key="test_strategies_editor",
                width="stretch",
                hide_index=True,
            )
            saved_strategies = st.form_submit_button(
                "Save Edited Test Strategies", width="stretch"
            )
        if saved_strategies:
            save_test_strategies(edited_strategies)
            artifacts = current_artifacts()
            st.toast("Edited test strategies saved.")
    if not artifacts["state_transition_sequences"].empty:
        with st.expander("State transition model sequences"):
            st.dataframe(artifacts["state_transition_sequences"])

    section_header("AI Coverage Review", "ai")
    if not is_llm_enabled(st.session_state.selected_provider):
        st.info("Selected provider is not configured. Local rules remain available.")
    elif artifacts["coverage_items"].empty:
        st.info("Generate coverage items before running AI coverage review.")
    else:
        if st.button("Review Coverage With AI", width="stretch"):
            try:
                user_prompt = coverage_improvement_prompt(
                    artifacts["structured_requirements"][
                        ["requirement_id", "requirement_text"]
                    ].to_string(index=False),
                    artifacts["coverage_items"].to_string(index=False),
                )
                result = chat_completion(
                    COVERAGE_IMPROVEMENT_SYSTEM,
                    user_prompt,
                    provider=st.session_state.selected_provider,
                    model=st.session_state.selected_model,
                )
                render_ai_text_result("coverage_ai_review", result)
            except Exception as exc:
                st.error(f"AI coverage review failed: {exc}")
        elif st.session_state.get("coverage_ai_review"):
            st.markdown(st.session_state.coverage_ai_review)

if page == "Test Cases":
    section_header("Generated Test Cases", "case")
    if st.button("Generate Test Cases", type="primary", width="stretch"):
        with st.spinner("Generating test cases with LLM-first pipeline and rule fallback..."):
            generate_current_test_cases()
        artifacts = current_artifacts()
    if artifacts["test_cases"].empty:
        st.info("Generate coverage and strategy first, then generate test cases.")
    else:
        with st.form("test_cases_edit_form"):
            edited_cases = st.data_editor(
                st.session_state.test_cases_draft,
                num_rows="dynamic",
                key="test_cases_editor",
                width="stretch",
                hide_index=True,
            )
            saved_cases = st.form_submit_button(
                "Save Edited Test Cases", width="stretch"
            )
        if saved_cases:
            save_test_cases(edited_cases)
            artifacts = current_artifacts()
            st.toast("Edited test cases saved.")
    section_header("Traceability Matrix", "map")
    if artifacts["traceability_matrix"].empty:
        st.info("Traceability matrix will appear after test case generation.")
    else:
        st.dataframe(artifacts["traceability_matrix"])
    if not artifacts["optimized_test_cases"].empty:
        with st.expander("Optimized test suite"):
            st.dataframe(artifacts["optimized_test_cases"])
    if not artifacts["state_transition_sequences"].empty:
        with st.expander("Standalone state transition tests"):
            st.dataframe(artifacts["state_transition_sequences"])

    section_header("AI Test Design Improvement", "ai")
    if not is_llm_enabled(st.session_state.selected_provider):
        st.info(
            "Selected provider is not configured. Local rules remain available. Copy .env.example to .env to enable model calls."
        )
    elif artifacts["test_cases"].empty:
        st.info("Generate test cases before running AI improvement.")
    else:
        if st.button("Generate AI Improvement Suggestions", width="stretch"):
            with st.spinner("Generating AI improvement suggestions..."):
                result = generate_improved_test_design_with_llm(
                    artifacts["structured_requirements"],
                    artifacts["coverage_items"],
                    artifacts["test_cases"],
                    provider=st.session_state.selected_provider,
                    model=st.session_state.selected_model,
                )
            st.session_state.ai_improvement_result = result

        result = st.session_state.get("ai_improvement_result")
        if result:
            with st.expander("Missing coverage suggestions", expanded=True):
                st.dataframe(result["missing_coverage"])
            with st.expander("Improved or additional test cases", expanded=True):
                st.dataframe(result["suggested_test_cases"])
            if "suite_optimization_review" in result:
                with st.expander("Suite optimization review", expanded=True):
                    st.dataframe(result["suite_optimization_review"])

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
            st.toast(f"Saved to {path}")
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
                save_requirements(pd.DataFrame(requirements_records))
            for artifact_key in [
                "structured_requirements",
                "risk_analysis",
                "coverage_items",
                "test_strategies",
                "test_cases",
                "optimized_test_cases",
                "state_transition_sequences",
                "traceability_matrix",
                "performance",
            ]:
                records = loaded.get("artifacts", {}).get(artifact_key, [])
                if records:
                    st.session_state[artifact_key] = pd.DataFrame(records)
            if not st.session_state.test_cases.empty:
                st.session_state.test_cases_draft = st.session_state.test_cases.copy()
            st.toast(f"Loaded {selected_project}")

    section_header("Export Artifacts", "save")
    artifacts = current_artifacts()
    if artifacts["test_cases"].empty:
        st.info("Generate test cases before exporting test design artifacts.")

    row1_cols = st.columns(3, gap="medium")
    with row1_cols[0]:
        if st.button("Export Risk Excel", width="stretch"):
            path = export_excel(
                {"risk_analysis": artifacts["risk_analysis"]}, "risk_analysis.xlsx"
            )
            st.toast(f"Saved to {path}")
    with row1_cols[1]:
        if st.button("Export Test Cases Excel", width="stretch"):
            path = export_excel(
                {"test_cases": artifacts["optimized_test_cases"]}, "test_cases.xlsx"
            )
            st.toast(f"Saved to {path}")
    with row1_cols[2]:
        if st.button("Export Traceability CSV", width="stretch"):
            path = export_csv(
                artifacts["traceability_matrix"], "traceability_matrix.csv"
            )
            st.toast(f"Saved to {path}")

    row2_cols = st.columns(3, gap="medium")
    with row2_cols[0]:
        if st.button("Export Project JSON", width="stretch"):
            state = build_project_state(
                st.session_state.project_name,
                st.session_state.selected_provider,
                st.session_state.selected_model,
                artifacts,
            )
            path = export_json(state, "test_suite_artifacts.json")
            st.toast(f"Saved to {path}")
    with row2_cols[1]:
        if st.button("Export Full Test Design Artifacts", width="stretch"):
            paths = export_test_artifacts(
                structured_requirements=artifacts["structured_requirements"],
                coverage_items=artifacts["coverage_items"],
                strategies=artifacts["test_strategies"],
                test_cases=artifacts["optimized_test_cases"],
                state_sequences=artifacts["state_transition_sequences"],
                prefix=st.session_state.project_name,
            )
            st.toast("Full artifact export completed.")
            render_export_paths(paths)
    with row2_cols[2]:
        if st.button("Export Selenium/PyTest Draft", width="stretch"):
            path = export_selenium_pytest_draft(artifacts["optimized_test_cases"])
            st.toast(f"Saved to {path}")

    st.dataframe(artifacts["performance"])
