import pandas as pd
import streamlit as st

from src.ai_client import is_llm_enabled
from src.state_modeler import infer_state_model_from_requirements

from app_ui.actions import (
    improve_current_state_model_with_llm,
    save_state_transition_sequences,
)
from app_ui.state import editor_safe_frame, rerun_with_toast


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
        if isinstance(artifact, pd.DataFrame) and not artifact.empty and "llm_error" in artifact.columns:
            errors = [
                str(error)
                for error in artifact["llm_error"].dropna().unique()
                if str(error)
            ]
            for error in errors:
                messages.append(f"{artifact_name}: {error}")
    if messages:
        st.warning(
            "LLM call did not complete successfully. Local rule fallback was used.\n\n"
            + "\n\n".join(messages)
            + "\n\nTry a faster model, switch provider, check API quota/permissions, "
            "or increase AUTOTESTDESIGN_LLM_TIMEOUT in .env."
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
          <div class="metric-card"><div class="metric-label">Test Suites</div><div class="metric-value">{len(artifacts["test_suites"])}</div></div>
          <div class="metric-card"><div class="metric-label">Test Cases</div><div class="metric-value">{len(artifacts["test_cases"])}</div></div>
          <div class="metric-card"><div class="metric-label">High Risk</div><div class="metric-value" style="{risk_color_style}">{high_risk_count}</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
        editor_safe_frame(pd.DataFrame(rows)),
        hide_index=True,
        use_container_width=True,
        column_config={
            "artifact": st.column_config.TextColumn("artifact", width="medium"),
            "file": st.column_config.TextColumn("file", width="large"),
            "folder": st.column_config.TextColumn("folder", width="large"),
        },
    )


def render_performance_table(artifacts: dict[str, pd.DataFrame]) -> None:
    if not artifacts["performance"].empty:
        st.caption("Performance targets are tracked locally for reporting.")
        st.dataframe(editor_safe_frame(artifacts["performance"]), hide_index=True)


def state_model_to_dot(state_model: dict) -> str:
    lines = [
        "digraph StateModel {",
        "  rankdir=LR;",
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


@st.fragment
def _render_state_transition_sequences_editor() -> None:
    with st.form("state_transition_sequences_editor_form"):
        edited_sequences = st.data_editor(
            editor_safe_frame(st.session_state.state_transition_sequences_draft),
            num_rows="dynamic",
            key="state_transition_sequences_editor",
            hide_index=True,
        )
        saved = st.form_submit_button("Save Edited State Transition Sequences")
    if saved:
        st.session_state.state_transition_sequences_draft = edited_sequences
        save_state_transition_sequences(edited_sequences)
        rerun_with_toast(
            "Edited state transition sequences saved. Regenerate test suites and test cases."
        )


def render_state_model_section() -> None:
    if (
        st.session_state.structured_requirements.empty
        or st.session_state.test_strategies.empty
    ):
        return

    state_model = st.session_state.state_model or infer_state_model_from_requirements(
        st.session_state.structured_requirements
    )
    with st.expander("State Transition Model", expanded=True):
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
                rerun_with_toast("LLM state model improvement completed.")
        st.graphviz_chart(state_model_to_dot(state_model))
        if not st.session_state.state_transition_sequences.empty:
            _render_state_transition_sequences_editor()


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
                st.metric(
                    "Data Transformation",
                    f"{timing.get('data_transformation_seconds', 0):.3f}s",
                )
            with col2:
                st.metric("LLM Total", f"{timing.get('llm_total_seconds', 0):.3f}s")
            with col3:
                st.metric(
                    "Frame Conversion",
                    f"{timing.get('frame_conversion_seconds', 0):.3f}s",
                )

            batches = timing.get("batches", [])
            if batches:
                st.markdown("**LLM Batch Details:**")
                batch_data = []
                for i, bt in enumerate(batches):
                    batch_data.append(
                        {
                            "Batch": i + 1,
                            "Batch Size": bt.get("batch_size", 0),
                            "Prompt Chars": bt.get("prompt_chars", 0),
                            "Max Tokens": bt.get("max_tokens", 0),
                            "LLM Call (s)": f"{bt.get('llm_call_seconds', 0):.3f}",
                            "Prompt Prep (s)": f"{bt.get('prompt_preparation_seconds', 0):.3f}",
                            "Result Parse (s)": f"{bt.get('result_parsing_seconds', 0):.3f}",
                            "Batch Total (s)": f"{bt.get('batch_total_seconds', 0):.3f}",
                        }
                    )
                st.dataframe(
                    editor_safe_frame(pd.DataFrame(batch_data)), hide_index=True
                )

            st.metric("Total Time", f"{timing.get('total_seconds', 0):.3f}s")

        elif method == "rule_fallback":
            st.metric(
                "Rule Fallback Time", f"{timing.get('rule_fallback_total', 0):.3f}s"
            )

        elif method == "rule_fallback_after_error":
            st.error(f"LLM Error: {timing.get('error', 'Unknown error')}")
            st.metric(
                "Fallback Time", f"{timing.get('fallback_after_error_seconds', 0):.3f}s"
            )
