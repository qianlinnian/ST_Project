import json
import re

import pandas as pd
import streamlit as st

from src.ai_client import available_models, available_provider_names


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
    if "test_plan_document_draft" not in st.session_state:
        st.session_state.test_plan_document_draft = ""
    if "test_suites_draft" not in st.session_state:
        st.session_state.test_suites_draft = pd.DataFrame()
    if "test_cases_draft" not in st.session_state:
        st.session_state.test_cases_draft = pd.DataFrame()
    if "state_transition_sequences_draft" not in st.session_state:
        st.session_state.state_transition_sequences_draft = pd.DataFrame()
    if "coverage_ai_improvement" not in st.session_state:
        st.session_state.coverage_ai_improvement = None
    if "ai_improvement_result" not in st.session_state:
        st.session_state.ai_improvement_result = None
    if "suite_minimization_result" not in st.session_state:
        st.session_state.suite_minimization_result = None
    if "suite_design_improvement" not in st.session_state:
        st.session_state.suite_design_improvement = None
    if "pending_toasts" not in st.session_state:
        st.session_state.pending_toasts = []
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
    if "test_plan_document" not in st.session_state:
        st.session_state.test_plan_document = ""


def queue_toast(message: str) -> None:
    st.session_state.pending_toasts.append(message)


def rerun_with_toast(message: str) -> None:
    queue_toast(message)
    st.rerun()


def flush_pending_toasts() -> None:
    pending = list(st.session_state.get("pending_toasts", []))
    st.session_state.pending_toasts = []
    for message in pending:
        st.toast(message)


def empty_requirements() -> pd.DataFrame:
    return pd.DataFrame(columns=["requirement_id", "module", "requirement_text"])


def current_artifacts() -> dict[str, object]:
    return {
        "requirements": st.session_state.requirements,
        "structured_requirements": st.session_state.structured_requirements,
        "risk_analysis": st.session_state.risk_analysis,
        "coverage_items": st.session_state.coverage_items,
        "test_strategies": st.session_state.test_strategies,
        "test_plan_document": st.session_state.test_plan_document,
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


def format_cell_value(value) -> str:
    if isinstance(value, (list, dict, tuple, set)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except TypeError:
            return str(value)
    return "" if pd.isna(value) else str(value)


def editor_safe_frame(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return data.copy()
    safe = data.copy()
    for column in safe.columns:
        if (
            safe[column]
            .map(lambda value: isinstance(value, (list, dict, tuple, set)))
            .any()
        ):
            safe[column] = safe[column].map(format_cell_value)
    return safe


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

    if (
        sort_option == "Risk level (High first)"
        and "risk_level" in sorted_risks.columns
    ):
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
    elif (
        sort_option == "Risk score (High first)"
        and "risk_score" in sorted_risks.columns
    ):
        sorted_risks = sorted_risks.sort_values(
            "risk_score",
            ascending=False,
            kind="stable",
        )
    elif (
        sort_option == "Risk score (Low first)" and "risk_score" in sorted_risks.columns
    ):
        sorted_risks = sorted_risks.sort_values(
            "risk_score",
            ascending=True,
            kind="stable",
        )

    return sorted_risks.reset_index(drop=True)


def normalize_requirements(
    requirements: pd.DataFrame,
) -> tuple[pd.DataFrame, list[str]]:
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
    text_keys = {"test_plan_document", "test_plan_document_draft"}
    order = {
        "requirements": [
            "structured_requirements",
            "risk_analysis",
            "risk_analysis_draft",
            "coverage_items",
            "coverage_items_draft",
            "test_strategies",
            "test_strategies_draft",
            "test_plan_document",
            "test_plan_document_draft",
            "test_suites",
            "test_suites_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "state_transition_sequences_draft",
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
            "test_plan_document",
            "test_plan_document_draft",
            "test_suites",
            "test_suites_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "state_transition_sequences_draft",
            "traceability_matrix",
        ],
        "risk": [
            "coverage_items",
            "coverage_items_draft",
            "test_strategies",
            "test_strategies_draft",
            "test_plan_document",
            "test_plan_document_draft",
            "test_suites",
            "test_suites_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "state_transition_sequences",
            "state_transition_sequences_draft",
            "traceability_matrix",
        ],
        "strategy": [
            "test_plan_document",
            "test_plan_document_draft",
            "test_suites",
            "test_suites_draft",
            "test_cases",
            "test_cases_draft",
            "optimized_test_cases",
            "traceability_matrix",
        ],
    }
    for key in order.get(from_step, []):
        st.session_state[key] = "" if key in text_keys else pd.DataFrame()
    if from_step in {"requirements", "structured", "risk"}:
        st.session_state.state_model = None
    if from_step in {"requirements", "structured", "risk"}:
        st.session_state.coverage_ai_improvement = None
        st.session_state.ai_improvement_result = None
        st.session_state.suite_minimization_result = None
    if from_step == "strategy":
        st.session_state.ai_improvement_result = None
        st.session_state.suite_minimization_result = None


def requirements_from_text(raw_text: str) -> pd.DataFrame:
    rows = []
    bullet_prefix_pattern = re.compile(r"^\s*(?:[-*•]+|\d+[.)])\s*")
    module_prefix_pattern = re.compile(r"^\s*\[([^\]]+)\]\s*(.*)$")
    id_prefix_pattern = re.compile(r"^\s*((?:[A-Za-z]+-)+\d+)\s*(?::|\uFF1A|-)\s*(.*)$")

    for line in raw_text.splitlines():
        requirement_text = bullet_prefix_pattern.sub("", line).strip()
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
