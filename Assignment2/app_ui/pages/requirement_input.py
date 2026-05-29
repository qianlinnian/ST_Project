import hashlib

import pandas as pd
import streamlit as st
from pandas.errors import ParserError

from src.ai_client import is_llm_enabled

from app_ui.actions import (
    enhance_current_requirements_with_llm,
    structure_current_requirements,
)
from app_ui.components import section_header
from app_ui.state import (
    editable_structured_requirements,
    editor_safe_frame,
    requirements_from_text,
    save_requirements,
    save_structured_requirements,
)


REQUIRED_REQUIREMENT_COLUMNS = [
    "requirement_id",
    "module",
    "requirement_text",
]


def _format_csv_upload_error(error: Exception) -> str:
    if isinstance(error, ParserError):
        return (
            "CSV parsing failed. The file must contain exactly three comma-separated "
            "columns: requirement_id, module, requirement_text. "
            "If requirement_text contains commas, wrap the full text in double quotes. "
            f"Details: {error}"
        )
    return f"Failed to read CSV file. Details: {error}"


def render_requirement_input_page(artifacts: dict[str, pd.DataFrame]) -> None:
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
                "<code>requirement_id</code>, <code>module</code>, and "
                "<code>requirement_text</code>.</p>"
                '<pre class="csv-sample">requirement_id,module,requirement_text\n'
                "FR-11,TodoItem,Users shall be able to add a new Todo item\n"
                "FR-12,TodoItem,Users shall be able to mark or unmark a Todo item</pre>",
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
                    try:
                        uploaded_requirements = pd.read_csv(
                            pd.io.common.BytesIO(uploaded_bytes)
                        )
                    except Exception as error:
                        st.error(_format_csv_upload_error(error))
                    else:
                        if list(
                            uploaded_requirements.columns
                        ) == REQUIRED_REQUIREMENT_COLUMNS and isinstance(
                            uploaded_requirements.index, pd.RangeIndex
                        ):
                            save_requirements(
                                uploaded_requirements[
                                    REQUIRED_REQUIREMENT_COLUMNS
                                ].copy()
                            )
                            st.session_state.uploaded_requirements_signature = (
                                upload_signature
                            )
                            st.toast("CSV requirements loaded.")
                        else:
                            actual_columns = ", ".join(
                                map(str, uploaded_requirements.columns.tolist())
                            )
                            if not actual_columns:
                                actual_columns = "(none)"
                            st.error(
                                "Invalid CSV format. Use exactly three columns named "
                                "requirement_id,module,requirement_text. "
                                f"Detected columns: {actual_columns}. "
                                "If requirement_text contains commas, wrap it in "
                                'double quotes.'
                            )

        with text_col:
            st.markdown(
                '<div class="input-method-title">Plain text input</div>'
                '<p class="input-method-help">Optional format: '
                "<code>[Module] REQ-001: requirement text</code>. Missing modules "
                "default to General, and missing IDs are generated automatically.</p>",
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
                try:
                    parsed_requirements = requirements_from_text(raw_requirements)
                except Exception as error:
                    st.error(
                        "Failed to parse text requirements. Use one requirement per "
                        "line, optionally in the format [Module] REQ-001: text. "
                        f"Details: {error}"
                    )
                else:
                    if parsed_requirements.empty:
                        st.warning(
                            "Please enter at least one requirement. "
                            "Each non-empty line will be treated as one requirement."
                        )
                    else:
                        save_requirements(parsed_requirements)
                        st.toast("Text requirements converted to table.")

        edited = st.data_editor(
            editor_safe_frame(st.session_state.requirements_draft),
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
            structure_llm_disabled = not is_llm_enabled(
                st.session_state.selected_provider
            )
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
                editor_safe_frame(editable_structured_requirements()),
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
