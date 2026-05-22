import hashlib
import re

import pandas as pd
import time
import streamlit as st

from src.ai_client import (
    available_models,
    available_provider_names,
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
from src.requirement_parser import enhance_requirements_with_llm, structure_requirements
from src.risk_analyzer import analyze_risks_with_llm_fallback
from src.state_modeler import (
    generate_optimized_transition_sequence,
    infer_state_model_from_requirements,
    improve_state_model_with_llm,
)
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases
from src.test_suite_designer import (
    assign_test_suites_to_cases,
    design_test_suites,
    improve_test_suites_with_llm,
)
from src.test_strategy_selector import select_strategies
from src.improvement_engine import (
    generate_improved_test_design_with_llm,
    improve_optimized_suite_with_llm,
    suggest_missing_coverage_with_llm,
)

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
        .muted-copy {
          color: #6f6b63;
          font-size: 0.94rem;
          line-height: 1.5;
          margin: 0 0 1.05rem;
        }
        .input-method-title {
          color: var(--ink);
          font-size: 0.98rem;
          font-weight: 560;
          margin: 0 0 .25rem;
        }
        .input-method-help {
          color: #6f6b63;
          font-size: 0.88rem;
          line-height: 1.45;
          margin: 0 0 .65rem;
        }
        .csv-sample {
          border: 1px solid var(--line);
          background: rgba(255, 255, 255, 0.58);
          border-radius: 8px;
          color: #3f3d38;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          font-size: 0.78rem;
          line-height: 1.55;
          margin: 0 0 .8rem;
          overflow-x: auto;
          padding: .72rem .8rem;
          white-space: pre;
        }
        div[data-testid="stMarkdownPre"] {
          border: 1px solid var(--line);
          background: rgba(255, 255, 255, 0.58);
          border-radius: 8px;
          color: #3f3d38;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          font-size: 0.78rem;
          line-height: 1.55;
          margin: 0 0 .8rem;
          overflow-x: auto;
          padding: .72rem .8rem;
          white-space: pre;
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
        div[data-testid="stFileUploader"] section {
          background: rgba(255, 255, 255, 0.58);
          border: 1px solid var(--line);
          border-radius: 8px;
        }
        div[data-testid="stTextArea"] textarea {
          background: rgba(255, 255, 255, 0.7);
          border: 1px solid var(--line);
          border-radius: 8px;
          color: var(--ink);
          font-size: 0.92rem;
          line-height: 1.45;
        }
        div[data-testid="stTextArea"] textarea::placeholder {
          color: #7a766f;
          opacity: 1;
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
    if "uploaded_requirements_signature" not in st.session_state:
        st.session_state.uploaded_requirements_signature = None
    if "last_export_paths" not in st.session_state:
        st.session_state.last_export_paths = None
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
    if "test_suites_draft" not in st.session_state:
        st.session_state.test_suites_draft = pd.DataFrame()
    if "test_cases_draft" not in st.session_state:
        st.session_state.test_cases_draft = pd.DataFrame()
    if "coverage_ai_improvement" not in st.session_state:
        st.session_state.coverage_ai_improvement = None
    if "ai_improvement_result" not in st.session_state:
        st.session_state.ai_improvement_result = None
    if "suite_minimization_result" not in st.session_state:
        st.session_state.suite_minimization_result = None
    if "suite_design_improvement" not in st.session_state:
        st.session_state.suite_design_improvement = None
    if "llm_batch_size" not in st.session_state:
        st.session_state.llm_batch_size = 25
    if "llm_concurrency" not in st.session_state:
        st.session_state.llm_concurrency = 4
    for key in [
        "structured_requirements",
        "risk_analysis",
        "coverage_items",
        "test_strategies",
        "test_suites",
        "test_cases",
        "optimized_test_cases",
        "state_transition_sequences",
        "traceability_matrix",
        "performance",
    ]:
        if key not in st.session_state:
            st.session_state[key] = pd.DataFrame()
    if "state_model" not in st.session_state:
        st.session_state.state_model = None


def empty_requirements() -> pd.DataFrame:
    return pd.DataFrame(columns=["requirement_id", "module", "requirement_text"])


def current_artifacts() -> dict[str, pd.DataFrame]:
    return {
        "requirements": st.session_state.requirements,
        "structured_requirements": st.session_state.structured_requirements,
        "risk_analysis": st.session_state.risk_analysis,
        "coverage_items": st.session_state.coverage_items,
        "test_strategies": st.session_state.test_strategies,
        "test_suites": st.session_state.test_suites,
        "test_cases": st.session_state.test_cases,
        "optimized_test_cases": st.session_state.optimized_test_cases,
        "state_transition_sequences": st.session_state.state_transition_sequences,
        "traceability_matrix": st.session_state.traceability_matrix,
        "performance": st.session_state.performance,
    }


def compact_structured_requirements() -> pd.DataFrame:
    columns = [
        "requirement_id",
        "module",
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


STRUCTURED_LIST_COLUMNS = {
    "input_fields",
    "data_ranges",
    "conditions",
    "actions",
    "expected_results",
}


def editable_structured_requirements() -> pd.DataFrame:
    editable = compact_structured_requirements()
    for column in STRUCTURED_LIST_COLUMNS:
        if column in editable.columns:
            editable[column] = editable[column].apply(_list_to_editor_text)
    return editable


def save_structured_requirements(edited: pd.DataFrame) -> None:
    if edited is None or edited.empty:
        st.warning("No structured requirements to save.")
        return

    normalized = edited.copy()
    for column in STRUCTURED_LIST_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].apply(_parse_editor_list)

    st.session_state.structured_requirements = normalized
    reset_downstream("structured")


def _list_to_editor_text(value) -> str:
    if isinstance(value, list):
        return "\n".join(str(item) for item in value if str(item).strip())
    if _is_empty_cell(value):
        return ""
    return str(value)


def _parse_editor_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if _is_empty_cell(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    separators = "\n" if "\n" in text else ";"
    return [item.strip() for item in text.split(separators) if item.strip()]


def _is_empty_cell(value) -> bool:
    if value is None:
        return True
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


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


def sort_risk_analysis(risk_analysis: pd.DataFrame, sort_option: str) -> pd.DataFrame:
    if risk_analysis is None or risk_analysis.empty:
        return pd.DataFrame()

    sorted_risks = risk_analysis.copy()
    level_order = {"High": 0, "Medium": 1, "Low": 2}

    if sort_option == "Risk level (High first)" and "risk_level" in sorted_risks.columns:
        sorted_risks["_risk_level_order"] = (
            sorted_risks["risk_level"].map(level_order).fillna(99)
        )
        sort_columns = ["_risk_level_order"]
        ascending = [True]
        if "risk_score" in sorted_risks.columns:
            sort_columns.append("risk_score")
            ascending.append(False)
        sorted_risks = sorted_risks.sort_values(
            sort_columns,
            ascending=ascending,
            kind="stable",
        ).drop(columns=["_risk_level_order"])
    elif sort_option == "Risk score (High first)" and "risk_score" in sorted_risks.columns:
        sorted_risks = sorted_risks.sort_values(
            "risk_score",
            ascending=False,
            kind="stable",
        )
    elif sort_option == "Risk score (Low first)" and "risk_score" in sorted_risks.columns:
        sorted_risks = sorted_risks.sort_values(
            "risk_score",
            ascending=True,
            kind="stable",
        )

    return sorted_risks.reset_index(drop=True)


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
            "test_suites",
            "test_suites_draft",
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
            "test_suites",
            "test_suites_draft",
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
            "test_suites",
            "test_suites_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "traceability_matrix",
        ],
        "strategy": [
            "test_suites",
            "test_suites_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "traceability_matrix",
        ],
    }
    for key in order.get(from_step, []):
        st.session_state[key] = pd.DataFrame()
    if from_step in {"requirements", "structured", "risk"}:
        st.session_state.state_model = None
    if from_step in {"requirements", "structured", "risk"}:
        st.session_state.coverage_ai_improvement = None
        st.session_state.ai_improvement_result = None
        st.session_state.suite_minimization_result = None
    if from_step == "strategy":
        st.session_state.ai_improvement_result = None
        st.session_state.suite_minimization_result = None


def structure_current_requirements() -> None:
    normalized, messages = normalize_requirements(st.session_state.requirements)
    st.session_state.requirements = normalized
    for message in messages:
        st.toast(message)

    if st.session_state.requirements.empty:
        st.warning("Please enter, upload, or load requirements first.")
        return

    structuring_time, structured = measure_time(
        structure_requirements,
        st.session_state.requirements,
        provider=st.session_state.selected_provider,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    st.session_state.structured_requirements = structured
    set_performance("requirement_structuring_seconds", structuring_time)
    reset_downstream("structured")


def enhance_current_requirements_with_llm() -> None:
    normalized, messages = normalize_requirements(st.session_state.requirements)
    st.session_state.requirements = normalized
    for message in messages:
        st.toast(message)

    if st.session_state.requirements.empty:
        st.warning("Please enter, upload, or load requirements first.")
        return

    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    structuring_time, structured = measure_time(
        enhance_requirements_with_llm,
        st.session_state.requirements,
        provider=st.session_state.selected_provider,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    st.session_state.structured_requirements = structured
    set_performance("llm_requirement_structuring_seconds", structuring_time)
    reset_downstream("structured")


def analyze_current_risks() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return

    t_start = time.time()
    risks, timing_details = analyze_risks_with_llm_fallback(
        st.session_state.structured_requirements,
        st.session_state.selected_provider,
        st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
        fast_mode=True,
    )
    risk_time = time.time() - t_start

    st.session_state.risk_analysis = risks
    st.session_state.risk_analysis_draft = risks.copy()
    st.session_state.risk_timing_details = timing_details
    set_performance("risk_analysis_seconds", risk_time)
    reset_downstream("risk")


def generate_current_coverage() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if st.session_state.risk_analysis.empty:
        st.warning("Please analyze risks first.")
        return

    coverage_time, coverage_items = measure_time(
        identify_coverage_items,
        st.session_state.structured_requirements,
        st.session_state.risk_analysis,
    )
    st.session_state.coverage_items = coverage_items
    st.session_state.coverage_items_draft = coverage_items.copy()
    st.session_state.coverage_ai_improvement = None
    set_performance("coverage_generation_seconds", coverage_time)
    reset_downstream("strategy")


def improve_current_coverage_with_llm() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if st.session_state.coverage_items.empty:
        st.warning("Please generate coverage first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    llm_time, missing_coverage = measure_time(
        suggest_missing_coverage_with_llm,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.selected_provider,
        st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    st.session_state.coverage_ai_improvement = missing_coverage
    set_performance("llm_coverage_improvement_seconds", llm_time)

    if missing_coverage.empty or "llm_error" in missing_coverage.columns:
        return

    base_columns = list(st.session_state.coverage_items.columns)
    additions = missing_coverage.copy()
    for column in base_columns:
        if column not in additions.columns:
            additions[column] = ""
    additions = additions[base_columns]
    enhanced = pd.concat(
        [st.session_state.coverage_items, additions],
        ignore_index=True,
    )
    st.session_state.coverage_items = enhanced
    st.session_state.coverage_items_draft = enhanced.copy()
    reset_downstream("strategy")


def generate_current_strategy(use_llm: bool = False) -> None:
    if st.session_state.coverage_items.empty:
        st.warning("Please generate coverage first.")
        return

    def build_strategy_artifacts() -> tuple[pd.DataFrame, pd.DataFrame]:
        strategies = select_strategies(
            st.session_state.coverage_items,
            provider=st.session_state.selected_provider,
            model=st.session_state.selected_model,
            use_llm=use_llm,
            batch_size=int(st.session_state.get("llm_batch_size", 25)),
            concurrency=int(st.session_state.get("llm_concurrency", 4)),
        )
        state_model = infer_state_model_from_requirements(st.session_state.structured_requirements)
        state_sequences = generate_optimized_transition_sequence(state_model)
        st.session_state.state_model = state_model
        return strategies, state_sequences

    strategy_time, artifacts = measure_time(build_strategy_artifacts)
    strategies, state_sequences = artifacts
    st.session_state.test_strategies = strategies
    st.session_state.test_strategies_draft = strategies.copy()
    st.session_state.state_transition_sequences = state_sequences
    set_performance(
        "llm_strategy_improvement_seconds" if use_llm else "strategy_generation_seconds",
        strategy_time,
    )
    reset_downstream("strategy")


def generate_current_test_suites() -> None:
    if st.session_state.test_strategies.empty:
        st.warning("Please generate strategy first.")
        return
    suite_time, suites = measure_time(
        design_test_suites,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.risk_analysis,
    )
    st.session_state.test_suites = suites
    st.session_state.test_suites_draft = suites.copy()
    st.session_state.suite_design_improvement = None
    st.session_state.test_cases = pd.DataFrame()
    st.session_state.test_cases_draft = pd.DataFrame()
    st.session_state.optimized_test_cases = pd.DataFrame()
    st.session_state.traceability_matrix = pd.DataFrame()
    set_performance("test_suite_design_seconds", suite_time)


def improve_current_test_suites_with_llm() -> None:
    if st.session_state.test_suites.empty:
        st.warning("Please generate test suites first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return
    llm_time, result = measure_time(
        improve_test_suites_with_llm,
        st.session_state.test_suites,
        st.session_state.coverage_items,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    improved = result.get("test_suites", pd.DataFrame())
    if not improved.empty:
        st.session_state.test_suites = improved
        st.session_state.test_suites_draft = improved.copy()
        if not st.session_state.test_cases.empty:
            st.session_state.test_cases = assign_test_suites_to_cases(
                st.session_state.test_cases,
                st.session_state.test_suites,
            )
            st.session_state.test_cases_draft = st.session_state.test_cases.copy()
            st.session_state.optimized_test_cases = optimize_suite(st.session_state.test_cases)
            st.session_state.traceability_matrix = build_traceability_matrix(
                st.session_state.structured_requirements,
                st.session_state.coverage_items,
                st.session_state.test_strategies,
                st.session_state.optimized_test_cases,
            )
    st.session_state.suite_design_improvement = result.get("suite_improvement_suggestions", pd.DataFrame())
    set_performance("llm_test_suite_design_improvement_seconds", llm_time)


def improve_current_state_model_with_llm() -> None:
    if st.session_state.structured_requirements.empty:
        st.warning("Please structure requirements first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    model_time, state_model = measure_time(
        improve_state_model_with_llm,
        st.session_state.structured_requirements,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        use_llm=True,
    )
    st.session_state.state_model = state_model
    st.session_state.state_transition_sequences = generate_optimized_transition_sequence(state_model)
    set_performance("llm_state_model_improvement_seconds", model_time)
    st.session_state.test_cases = pd.DataFrame()
    st.session_state.test_cases_draft = pd.DataFrame()
    st.session_state.optimized_test_cases = pd.DataFrame()
    st.session_state.traceability_matrix = pd.DataFrame()


def generate_current_test_cases() -> None:
    if st.session_state.coverage_items.empty or st.session_state.test_strategies.empty:
        st.warning("Please generate coverage and strategy first.")
        return
    if st.session_state.test_suites.empty:
        generate_current_test_suites()

    generation_time, test_cases = measure_time(
        generate_test_cases,
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.test_suites,
        include_state_tests=True,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        use_llm=False,
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
    st.session_state.ai_improvement_result = None
    st.session_state.suite_minimization_result = None
    set_performance("test_case_generation_seconds", generation_time)


def improve_current_optimized_suite_with_llm() -> None:
    if st.session_state.optimized_test_cases.empty:
        st.warning("Please generate an optimized test suite first.")
        return
    if not is_llm_enabled(st.session_state.selected_provider):
        st.warning("Selected LLM provider is not configured.")
        return

    llm_time, result = measure_time(
        improve_optimized_suite_with_llm,
        st.session_state.optimized_test_cases,
        st.session_state.test_suites,
        st.session_state.coverage_items,
        provider=st.session_state.selected_provider,
        model=st.session_state.selected_model,
        batch_size=int(st.session_state.get("llm_batch_size", 25)),
        concurrency=int(st.session_state.get("llm_concurrency", 4)),
    )
    optimized_cases = result.get("optimized_test_cases", pd.DataFrame())
    if not optimized_cases.empty:
        st.session_state.optimized_test_cases = optimized_cases
        st.session_state.traceability_matrix = build_traceability_matrix(
            st.session_state.structured_requirements,
            st.session_state.coverage_items,
            st.session_state.test_strategies,
            st.session_state.optimized_test_cases,
        )
    st.session_state.suite_minimization_result = result
    set_performance("llm_suite_minimization_seconds", llm_time)


def save_test_cases(test_cases: pd.DataFrame) -> None:
    st.session_state.test_cases = assign_test_suites_to_cases(
        test_cases.copy(),
        st.session_state.test_suites,
    )
    st.session_state.test_cases_draft = st.session_state.test_cases.copy()
    st.session_state.optimized_test_cases = optimize_suite(st.session_state.test_cases)
    st.session_state.ai_improvement_result = None
    st.session_state.suite_minimization_result = None
    st.session_state.traceability_matrix = build_traceability_matrix(
        st.session_state.structured_requirements,
        st.session_state.coverage_items,
        st.session_state.test_strategies,
        st.session_state.optimized_test_cases,
    )


def save_test_suites(test_suites: pd.DataFrame) -> None:
    st.session_state.test_suites = test_suites.copy()
    st.session_state.test_suites_draft = test_suites.copy()
    st.session_state.suite_design_improvement = None
    if not st.session_state.test_cases.empty:
        st.session_state.test_cases = assign_test_suites_to_cases(
            st.session_state.test_cases,
            st.session_state.test_suites,
        )
        st.session_state.test_cases_draft = st.session_state.test_cases.copy()
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
    st.session_state.coverage_ai_improvement = None
    st.session_state.test_strategies = pd.DataFrame()
    st.session_state.test_strategies_draft = pd.DataFrame()
    st.session_state.test_suites = pd.DataFrame()
    st.session_state.test_suites_draft = pd.DataFrame()
    reset_downstream("strategy")


def save_test_strategies(test_strategies: pd.DataFrame) -> None:
    st.session_state.test_strategies = test_strategies.copy()
    st.session_state.test_strategies_draft = test_strategies.copy()
    st.session_state.ai_improvement_result = None
    st.session_state.suite_minimization_result = None
    reset_downstream("strategy")


def render_llm_status(artifacts: dict[str, pd.DataFrame]) -> None:
    messages = []
    for artifact_name in [
        "risk_analysis",
        "test_strategies",
        "test_suites",
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
    module_prefix_pattern = re.compile(r"^\s*\[([^\]]+)\]\s*(.*)$")
    id_prefix_pattern = re.compile(r"^\s*((?:[A-Za-z]+-)+\d+)\s*(?::|\uFF1A|-)\s*(.*)$")

    for line in raw_text.splitlines():
        requirement_text = line.strip()
        if not requirement_text:
            continue

        module = "General"
        module_match = module_prefix_pattern.match(requirement_text)
        if module_match:
            module = module_match.group(1).strip() or "General"
            requirement_text = module_match.group(2).strip()

        match = id_prefix_pattern.match(requirement_text)
        if match:
            requirement_id = match.group(1).strip()
            requirement_text = match.group(2).strip()
        else:
            requirement_id = f"REQ-{len(rows) + 1:03d}"

        if not requirement_text:
            continue

        rows.append(
            {
                "requirement_id": requirement_id,
                "module": module,
                "requirement_text": requirement_text,
            }
        )
    return pd.DataFrame(rows, columns=["requirement_id", "module", "requirement_text"])


def render_export_paths(paths: dict[str, object]) -> None:
    rows = []
    for name, path in paths.items():
        path_text = str(path)
        normalized = path_text.replace("\\", "/")
        folder, _, filename = normalized.rpartition("/")
        rows.append(
            {
                "artifact": name,
                "file": filename or normalized,
                "folder": folder,
            }
        )
    st.dataframe(
        pd.DataFrame(rows),
        hide_index=True,
        use_container_width=True,
        column_config={
            "artifact": st.column_config.TextColumn("artifact", width="medium"),
            "file": st.column_config.TextColumn("file", width="large"),
            "folder": st.column_config.TextColumn("folder", width="large"),
        },
    )


def render_test_design_llm_summary(result: dict | None) -> None:
    if not result:
        return
    missing_cases = result.get("missing_test_cases", pd.DataFrame())
    if missing_cases.empty or "llm_error" in missing_cases.columns:
        st.info("LLM did not add missing test cases.")
        return
    st.success(f"Added {len(missing_cases)} missing test cases with LLM.")


def render_suite_minimization_summary(result: dict | None) -> None:
    if not result:
        return
    decisions = result.get("suite_minimization_decisions", pd.DataFrame())
    if decisions.empty:
        st.info("LLM minimization reviewed the suite; no redundant cases were removed.")
        return
    removed = int((decisions.get("status") == "applied").sum()) if "status" in decisions.columns else 0
    protected = int((decisions.get("status") == "protected").sum()) if "status" in decisions.columns else 0
    if removed or protected:
        st.success(
            f"LLM minimization removed {removed} redundant cases, "
            f"protected {protected} high-value cases."
        )
    else:
        st.info("LLM minimization reviewed the suite; no safe removals were applied.")


def render_performance_table(artifacts: dict[str, pd.DataFrame]) -> None:
    if not artifacts["performance"].empty:
        st.caption("Performance targets are tracked locally for reporting.")
        st.dataframe(artifacts["performance"], hide_index=True)


def state_model_to_dot(state_model: dict) -> str:
    lines = [
        "digraph StateModel {",
        '  rankdir=LR;',
        '  node [shape=box, style="rounded,filled", fillcolor="#FFFBEB", color="#D97706"];',
        '  edge [color="#1F2937"];',
    ]
    for state in state_model.get("states", []):
        safe_state = str(state).replace('"', '\\"')
        lines.append(f'  "{safe_state}";')
    for transition in state_model.get("transition_details", []):
        source = str(transition.get("source_state", "")).replace('"', '\\"')
        target = str(transition.get("target_state", "")).replace('"', '\\"')
        event = str(transition.get("event", "")).replace('"', '\\"')
        if len(event) > 60:
            event = event[:57] + "..."
        lines.append(f'  "{source}" -> "{target}" [label="{event}"];')
    lines.append("}")
    return "\n".join(lines)


def render_state_model_section() -> None:
    if st.session_state.structured_requirements.empty:
        return

    state_model = st.session_state.state_model or infer_state_model_from_requirements(
        st.session_state.structured_requirements
    )
    with st.expander("State Transition Model", expanded=False):
        st.caption(
            "Coverage criterion: All Transitions. The optimized sequence covers each selected transition once and resets only when transitions cannot be chained."
        )
        state_col, improve_col = st.columns([1, 1], gap="medium")
        with state_col:
            st.metric("States", len(state_model.get("states", [])))
        with improve_col:
            disabled = not is_llm_enabled(st.session_state.selected_provider)
            if st.button("Improve State Model With LLM", disabled=disabled):
                with st.spinner("Improving state model with LLM..."):
                    improve_current_state_model_with_llm()
                st.toast("LLM state model improvement completed.")
                st.rerun()
        st.graphviz_chart(state_model_to_dot(state_model))
        if not st.session_state.state_transition_sequences.empty:
            st.dataframe(st.session_state.state_transition_sequences, hide_index=True)


def render_risk_timing_details() -> None:
    timing = getattr(st.session_state, "risk_timing_details", None)
    if not timing:
        return

    with st.expander("Risk Analysis Timing Details", expanded=False):
        method = timing.get("method", "unknown")
        st.markdown(f"**Method:** {method}")

        if method == "llm_analysis":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Data Transformation", f"{timing.get('data_transformation_seconds', 0):.3f}s")
            with col2:
                st.metric("LLM Total", f"{timing.get('llm_total_seconds', 0):.3f}s")
            with col3:
                st.metric("Frame Conversion", f"{timing.get('frame_conversion_seconds', 0):.3f}s")

            batches = timing.get("batches", [])
            if batches:
                st.markdown("**LLM Batch Details:**")
                batch_data = []
                for i, bt in enumerate(batches):
                    batch_data.append({
                        "Batch": i + 1,
                        "Batch Size": bt.get("batch_size", 0),
                        "Prompt Chars": bt.get("prompt_chars", 0),
                        "Max Tokens": bt.get("max_tokens", 0),
                        "LLM Call (s)": f"{bt.get('llm_call_seconds', 0):.3f}",
                        "Prompt Prep (s)": f"{bt.get('prompt_preparation_seconds', 0):.3f}",
                        "Result Parse (s)": f"{bt.get('result_parsing_seconds', 0):.3f}",
                        "Batch Total (s)": f"{bt.get('batch_total_seconds', 0):.3f}",
                    })
                st.dataframe(pd.DataFrame(batch_data), hide_index=True)

            st.metric("Total Time", f"{timing.get('total_seconds', 0):.3f}s")

        elif method == "rule_fallback":
            st.metric("Rule Fallback Time", f"{timing.get('rule_fallback_total', 0):.3f}s")

        elif method == "rule_fallback_after_error":
            st.error(f"LLM Error: {timing.get('error', 'Unknown error')}")
            st.metric("Fallback Time", f"{timing.get('fallback_after_error_seconds', 0):.3f}s")


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
        st.markdown(
            '<p class="muted-copy">Import CSV requirements, paste plain text, or edit the table directly.</p>',
            unsafe_allow_html=True,
        )

        upload_col, text_col = st.columns([1, 1], gap="medium")
        with upload_col:
            st.markdown(
                '<div class="input-method-title">CSV upload</div>'
                '<p class="input-method-help">Use exactly three columns named '
                '<code>requirement_id</code>, <code>module</code>, and '
                '<code>requirement_text</code>.</p>'
                '<pre class="csv-sample">requirement_id,module,requirement_text\n'
                'FR-11,TodoItem / Functional,Users shall be able to add a new Todo item\n'
                'FR-12,TodoItem / Functional,Users shall be able to mark or unmark a Todo item</pre>',
                unsafe_allow_html=True,
            )
            uploaded_file = st.file_uploader(
                "Upload CSV requirements",
                type=["csv"],
                label_visibility="collapsed",
            )
            if uploaded_file is not None:
                uploaded_bytes = uploaded_file.getvalue()
                upload_signature = (
                    uploaded_file.name,
                    hashlib.sha256(uploaded_bytes).hexdigest(),
                )
                if upload_signature != st.session_state.uploaded_requirements_signature:
                    uploaded_requirements = pd.read_csv(
                        pd.io.common.BytesIO(uploaded_bytes)
                    )
                    required_columns = [
                        "requirement_id",
                        "module",
                        "requirement_text",
                    ]
                    if list(uploaded_requirements.columns) == required_columns and isinstance(
                        uploaded_requirements.index, pd.RangeIndex
                    ):
                        save_requirements(uploaded_requirements[required_columns].copy())
                        st.session_state.uploaded_requirements_signature = (
                            upload_signature
                        )
                        st.toast("CSV requirements loaded.")
                    else:
                        st.error(
                            "Invalid CSV format. Use exactly three columns named "
                            "requirement_id,module,requirement_text. If you need "
                            "a category such as Functional, include it inside module, "
                            "for example TodoItem / Functional."
                        )

        with text_col:
            st.markdown(
                '<div class="input-method-title">Plain text input</div>'
                '<p class="input-method-help">Optional format: '
                '<code>[Module] REQ-001: requirement text</code>. Missing modules '
                'default to General, and missing IDs are generated automatically.</p>',
                unsafe_allow_html=True,
            )
            raw_requirements = st.text_area(
                "Paste plain-text requirements",
                placeholder=(
                    "[Todo Creation] REQ-001: When the todo input is not empty, "
                    "the user can add a new todo item by clicking Add.\n"
                    "[Todo Filtering] REQ-002: The user can filter todos by All, "
                    "Active, and Completed."
                ),
                label_visibility="collapsed",
                height=110,
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
                        hide_index=True,
            column_order=["requirement_id", "module", "requirement_text"],
        )
        st.session_state.requirements_draft = edited
        if st.button("Save Edited Requirements"):
            save_requirements(st.session_state.requirements_draft)
            st.toast("Edited requirements saved.")

        local_col, llm_col = st.columns([1, 1], gap="medium")
        with local_col:
            if st.button("Structure Requirements", type="primary"):
                with st.spinner("Structuring requirements..."):
                    save_requirements(st.session_state.requirements_draft)
                    structure_current_requirements()
                if not st.session_state.structured_requirements.empty:
                    st.toast("Requirement structuring completed.")
        with llm_col:
            structure_llm_disabled = not is_llm_enabled(st.session_state.selected_provider)
            if st.button(
                "Improve Structuring With LLM",
                disabled=structure_llm_disabled,
            ):
                with st.spinner("Enhancing requirement structuring with LLM..."):
                    save_requirements(st.session_state.requirements_draft)
                    enhance_current_requirements_with_llm()
                if not st.session_state.structured_requirements.empty:
                    st.toast("LLM requirement structuring completed.")

        if not st.session_state.structured_requirements.empty:
            section_header("Structured Requirement Preview", "file")
            structured_editor = st.data_editor(
                editable_structured_requirements(),
                key="structured_requirements_editor",
                hide_index=True,
                use_container_width=True,
                column_config={
                    "input_fields": st.column_config.TextColumn(
                        "input_fields",
                        help="One recognized input field per line.",
                    ),
                    "data_ranges": st.column_config.TextColumn(
                        "data_ranges",
                        help="One recognized data range or boundary per line.",
                    ),
                    "conditions": st.column_config.TextColumn(
                        "conditions",
                        help="One recognized condition per line.",
                    ),
                    "actions": st.column_config.TextColumn(
                        "actions",
                        help="One recognized action per line.",
                    ),
                    "expected_results": st.column_config.TextColumn(
                        "expected_results",
                        help="One expected result per line.",
                    ),
                },
            )
            if st.button("Save Edited Structured Requirements"):
                save_structured_requirements(structured_editor)
                st.toast("Edited structured requirements saved.")

if page == "Risk Analysis":
    section_header("Risk Analysis", "risk")
    if st.button("Analyze Risks", type="primary"):
        with st.spinner("Analyzing risks..."):
            analyze_current_risks()
        artifacts = current_artifacts()
    if artifacts["risk_analysis"].empty:
        st.info("Structure requirements on the Requirement Input page, then run risk analysis.")
    else:
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
        edited_risks = st.data_editor(
            display_risk_analysis(),
            num_rows="dynamic",
            key=f"risk_analysis_editor_{sort_option}",
            hide_index=True,
            width="stretch",
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
        if st.button("Save Edited Risk Analysis"):
            save_risk_analysis(st.session_state.risk_analysis_draft)
            st.toast("Edited risk analysis saved.")
    render_performance_table(artifacts)
    render_risk_timing_details()

if page == "Coverage & Strategy":
    section_header("Coverage Items", "map")
    local_col, llm_col = st.columns([1, 1], gap="medium")
    with local_col:
        if st.button("Generate Coverage", type="primary"):
            with st.spinner("Generating local coverage items..."):
                if not st.session_state.risk_analysis_draft.empty:
                    save_risk_analysis(st.session_state.risk_analysis_draft)
                generate_current_coverage()
            artifacts = current_artifacts()
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
            artifacts = current_artifacts()
            st.toast(f"LLM coverage improvement completed. Added {max(after_count - before_count, 0)} coverage items.")
    if artifacts["coverage_items"].empty:
        st.info("Run requirement structuring and risk analysis first.")
    else:
        with st.form("coverage_items_edit_form"):
            edited_coverage = st.data_editor(
                st.session_state.coverage_items_draft,
                num_rows="dynamic",
                key="coverage_items_editor",
                                hide_index=True,
            )
            saved_coverage = st.form_submit_button(
                "Save Edited Coverage Items"
            )
        if saved_coverage:
            save_coverage_items(edited_coverage)
            artifacts = current_artifacts()
            st.toast("Edited coverage items saved. Regenerate strategy before test case generation.")

    coverage_improvement = st.session_state.get("coverage_ai_improvement")
    if coverage_improvement is not None:
        with st.expander("LLM Coverage Additions", expanded=False):
            if coverage_improvement.empty:
                st.info("LLM did not identify additional missing coverage items.")
            elif "llm_error" in coverage_improvement.columns:
                st.error(str(coverage_improvement["llm_error"].dropna().iloc[0]))
            else:
                st.metric("Added Items", len(coverage_improvement))
                st.dataframe(coverage_improvement, hide_index=True)

    section_header("Coverage Strategy", "map")
    strategy_col, strategy_llm_col = st.columns([1, 1], gap="medium")
    with strategy_col:
        strategy_disabled = artifacts["coverage_items"].empty
        if st.button("Generate Strategy", type="primary", disabled=strategy_disabled):
            with st.spinner("Generating local test strategy..."):
                if not st.session_state.coverage_items_draft.empty:
                    save_coverage_items(st.session_state.coverage_items_draft)
                generate_current_strategy(use_llm=False)
            artifacts = current_artifacts()
            st.toast("Coverage strategy generated.")
    with strategy_llm_col:
        strategy_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["coverage_items"].empty
        )
        if st.button("Improve Strategy With LLM", disabled=strategy_llm_disabled):
            with st.spinner("Reviewing strategy with LLM..."):
                if not st.session_state.coverage_items_draft.empty:
                    save_coverage_items(st.session_state.coverage_items_draft)
                generate_current_strategy(use_llm=True)
            artifacts = current_artifacts()
            st.toast("LLM strategy improvement completed.")

    if artifacts["test_strategies"].empty:
        st.info("Coverage strategy has not been generated yet.")
    else:
        with st.form("test_strategies_edit_form"):
            edited_strategies = st.data_editor(
                st.session_state.test_strategies_draft,
                num_rows="dynamic",
                key="test_strategies_editor",
                                hide_index=True,
            )
            saved_strategies = st.form_submit_button(
                "Save Edited Test Strategies"
            )
        if saved_strategies:
            save_test_strategies(edited_strategies)
            artifacts = current_artifacts()
            st.toast("Edited test strategies saved.")

    section_header("Test Suites", "case")
    suite_col, suite_llm_col = st.columns([1, 1], gap="medium")
    with suite_col:
        suite_disabled = artifacts["test_strategies"].empty
        if st.button("Generate Test Suites", type="primary", disabled=suite_disabled):
            with st.spinner("Generating local test suites..."):
                if not st.session_state.test_strategies_draft.empty:
                    save_test_strategies(st.session_state.test_strategies_draft)
                generate_current_test_suites()
            artifacts = current_artifacts()
            st.toast("Test suites generated.")
    with suite_llm_col:
        suite_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["test_suites"].empty
        )
        if st.button("Improve Test Suites With LLM", disabled=suite_llm_disabled):
            with st.spinner("Improving test suite metadata with LLM..."):
                improve_current_test_suites_with_llm()
            artifacts = current_artifacts()
            st.toast("LLM test suite improvement completed.")

    if artifacts["test_suites"].empty:
        st.info("Generate strategy first, then generate test suites.")
    else:
        with st.form("test_suites_edit_form"):
            edited_suites = st.data_editor(
                st.session_state.test_suites_draft,
                num_rows="dynamic",
                key="test_suites_editor",
                hide_index=True,
            )
            saved_suites = st.form_submit_button("Save Edited Test Suites")
        if saved_suites:
            save_test_suites(edited_suites)
            artifacts = current_artifacts()
            st.toast("Edited test suites saved.")

    suite_improvement = st.session_state.get("suite_design_improvement")
    if suite_improvement is not None and not suite_improvement.empty:
        with st.expander("LLM Test Suite Suggestions", expanded=False):
            st.dataframe(suite_improvement, hide_index=True)
    render_state_model_section()
    render_performance_table(artifacts)

if page == "Test Cases":
    section_header("Candidate Test Cases", "case")
    local_col, llm_col = st.columns([1, 1], gap="medium")
    with local_col:
        if st.button("Generate Test Cases", type="primary"):
            with st.spinner("Generating local test cases..."):
                generate_current_test_cases()
            artifacts = current_artifacts()
    with llm_col:
        test_llm_disabled = (
            not is_llm_enabled(st.session_state.selected_provider)
            or artifacts["test_cases"].empty
        )
        if st.button(
            "Improve Test Design With LLM",
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
                enhanced_cases = improvement_result.get("enhanced_test_cases", pd.DataFrame())
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
                        st.session_state.optimized_test_cases,
                    )
                set_performance("llm_test_design_improvement_seconds", llm_time)
            st.toast("LLM test design improvement completed.")
    if artifacts["test_cases"].empty:
        st.info("Generate coverage and strategy first, then generate test cases.")
    else:
        with st.form("test_cases_edit_form"):
            edited_cases = st.data_editor(
                st.session_state.test_cases_draft,
                num_rows="dynamic",
                key="test_cases_editor",
                                hide_index=True,
            )
            saved_cases = st.form_submit_button(
                "Save Edited Test Cases"
            )
        if saved_cases:
            save_test_cases(edited_cases)
            artifacts = current_artifacts()
            st.toast("Edited test cases saved.")
    if not artifacts["optimized_test_cases"].empty:
        section_header("Optimized Test Suite", "case")
        with st.expander("Optimized test suite", expanded=True):
            improve_suite_disabled = not is_llm_enabled(st.session_state.selected_provider)
            if st.button(
                "Improve Optimized Suite With LLM",
                disabled=improve_suite_disabled,
            ):
                with st.spinner("Reviewing optimized suite with LLM..."):
                    improve_current_optimized_suite_with_llm()
                artifacts = current_artifacts()
                st.toast("LLM optimized suite improvement completed.")
            render_suite_minimization_summary(
                st.session_state.get("suite_minimization_result")
            )
            st.dataframe(artifacts["optimized_test_cases"])
    section_header("Traceability Matrix", "map")
    if artifacts["traceability_matrix"].empty:
        st.info("Traceability matrix will appear after test case generation.")
    else:
        st.dataframe(artifacts["traceability_matrix"])
    if not artifacts["state_transition_sequences"].empty:
        with st.expander("Standalone state transition tests"):
            st.dataframe(artifacts["state_transition_sequences"])

    result = st.session_state.get("ai_improvement_result")
    if result:
        missing_cases = result.get("missing_test_cases", pd.DataFrame())
        enhanced_cases = result.get("enhanced_test_cases", pd.DataFrame())
        optimized_cases = result.get("optimized_test_cases", pd.DataFrame())
        if missing_cases.empty and enhanced_cases.empty and optimized_cases.empty:
            st.session_state.ai_improvement_result = None
            result = None

    if result:
        render_test_design_llm_summary(result)
    render_performance_table(artifacts)

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
                "test_suites",
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
            if not st.session_state.test_suites.empty:
                st.session_state.test_suites_draft = st.session_state.test_suites.copy()
            st.toast(f"Loaded {selected_project}")

    section_header("Export Artifacts", "save")
    artifacts = current_artifacts()
    if artifacts["test_cases"].empty:
        st.info("Generate test cases before exporting test design artifacts.")

    row1_cols = st.columns(3, gap="medium")
    with row1_cols[0]:
        if st.button("Export Risk Excel"):
            path = export_excel(
                {"risk_analysis": artifacts["risk_analysis"]}, "risk_analysis.xlsx"
            )
            st.toast(f"Saved to {path}")
    with row1_cols[1]:
        if st.button("Export Test Cases Excel"):
            path = export_excel(
                {"test_cases": artifacts["optimized_test_cases"]}, "test_cases.xlsx"
            )
            st.toast(f"Saved to {path}")
    with row1_cols[2]:
        if st.button("Export Traceability CSV"):
            path = export_csv(
                artifacts["traceability_matrix"], "traceability_matrix.csv"
            )
            st.toast(f"Saved to {path}")

    row2_cols = st.columns(3, gap="medium")
    with row2_cols[0]:
        if st.button("Export Project JSON"):
            state = build_project_state(
                st.session_state.project_name,
                st.session_state.selected_provider,
                st.session_state.selected_model,
                artifacts,
            )
            path = export_json(state, "test_suite_artifacts.json")
            st.toast(f"Saved to {path}")
    with row2_cols[1]:
        if st.button("Export Full Test Design Artifacts"):
            paths = export_test_artifacts(
                structured_requirements=artifacts["structured_requirements"],
                coverage_items=artifacts["coverage_items"],
                strategies=artifacts["test_strategies"],
                test_suites=artifacts["test_suites"],
                test_cases=artifacts["test_cases"],
                optimized_test_cases=artifacts["optimized_test_cases"],
                state_sequences=artifacts["state_transition_sequences"],
                prefix=st.session_state.project_name,
            )
            st.session_state.last_export_paths = paths
            st.toast("Full artifact export completed.")
    with row2_cols[2]:
        if st.button("Export Selenium/PyTest Draft"):
            path = export_selenium_pytest_draft(artifacts["optimized_test_cases"])
            st.toast(f"Saved to {path}")

    if st.session_state.last_export_paths:
        render_export_paths(st.session_state.last_export_paths)

    st.dataframe(artifacts["performance"], use_container_width=True)
