import pandas as pd
import streamlit as st

from src.ai_client import chat_completion, is_llm_enabled
from src.coverage_identifier import identify_coverage_items
from src.performance_tracker import measure_time
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


st.set_page_config(page_title="AutoTestDesign AI App", layout="wide")
st.title("AutoTestDesign AI App")

st.sidebar.header("Workflow")
page = st.sidebar.radio(
    "Step",
    [
        "1. Requirement Input",
        "2. Structuring & Risk",
        "3. Coverage & Strategy",
        "4. Test Cases",
        "5. AI Review",
        "6. Export",
    ],
)

if "requirements" not in st.session_state:
    st.session_state.requirements = load_sample_requirements()


def build_pipeline_outputs():
    structured = structure_requirements(st.session_state.requirements)
    risks = analyze_risks(structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    test_cases = generate_test_cases(structured, coverage_items, strategies)
    optimized_cases = optimize_suite(test_cases)
    state_sequences = generate_all_transitions_sequence()
    return structured, risks, coverage_items, strategies, test_cases, optimized_cases, state_sequences


if page == "1. Requirement Input":
    st.subheader("Requirement Input")
    st.caption(
        "Mock data can be used before D/E provide the final TodoList requirements."
    )
    edited_requirements = st.data_editor(
        st.session_state.requirements, num_rows="dynamic", use_container_width=True
    )
    st.session_state.requirements = edited_requirements

if page == "2. Structuring & Risk":
    st.subheader("Requirement Structuring and Risk Analysis")
    elapsed, structured = measure_time(
        structure_requirements, st.session_state.requirements
    )
    _, risks = measure_time(analyze_risks, structured)
    st.write(f"Requirement structuring time: {elapsed:.4f}s")
    st.dataframe(structured, use_container_width=True)
    st.dataframe(risks, use_container_width=True)

if page == "3. Coverage & Strategy":
    st.subheader("Coverage Items and Test Strategies")
    structured, risks, coverage_items, strategies, _, _, state_sequences = build_pipeline_outputs()
    st.caption(
        "Strategies use ISTQB Foundation Level terminology and ISO/IEC/IEEE 29119-4 detailed test techniques."
    )
    st.dataframe(coverage_items, use_container_width=True)
    st.dataframe(strategies, use_container_width=True)
    with st.expander("State transition model sequences"):
        st.dataframe(state_sequences, use_container_width=True)

if page == "4. Test Cases":
    st.subheader("Generated Test Cases")
    structured = structure_requirements(st.session_state.requirements)
    risks = analyze_risks(structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    elapsed, test_cases = measure_time(
        generate_test_cases, structured, coverage_items, strategies
    )
    optimized_cases = optimize_suite(test_cases)
    state_sequences = generate_all_transitions_sequence()

    st.write(f"Test case generation time: {elapsed:.4f}s")
    st.caption("Generated cases include equivalence partitioning, boundary value analysis, decision table testing, and state transition testing where applicable.")
    st.data_editor(test_cases, num_rows="dynamic", use_container_width=True)

    with st.expander("Optimized test suite"):
        st.dataframe(optimized_cases, use_container_width=True)

    with st.expander("Standalone state transition tests"):
        st.dataframe(state_sequences, use_container_width=True)

if page == "5. AI Review":
    st.subheader("Optional AI Review")
    if not is_llm_enabled():
        st.warning(
            "LLM API is not configured. Copy .env.example to .env and fill in API values to enable this page."
        )
    else:
        structured = structure_requirements(st.session_state.requirements)
        risks = analyze_risks(structured)
        coverage_items = identify_coverage_items(structured, risks)
        user_prompt = coverage_improvement_prompt(
            structured[["requirement_id", "requirement_text"]].to_string(index=False),
            coverage_items.to_string(index=False),
        )
        if st.button("Review Coverage with LLM"):
            try:
                result = chat_completion(COVERAGE_IMPROVEMENT_SYSTEM, user_prompt)
                st.text_area("AI suggestions", result, height=300)
            except Exception as exc:
                st.error(f"AI review failed: {exc}")

if page == "6. Export":
    st.subheader("Export")
    st.info(
        "Export supports CSV, JSON, Excel, traceability matrix, and a PyTest draft scaffold."
    )
    from src.exporter import (
        build_traceability_matrix,
        export_csv,
        export_json,
        export_pytest_draft,
        export_test_artifacts,
    )

    structured, risks, coverage_items, strategies, test_cases, optimized_cases, state_sequences = build_pipeline_outputs()
    traceability = build_traceability_matrix(structured, coverage_items, strategies, optimized_cases)

    st.dataframe(traceability, use_container_width=True)

    if st.button("Export Requirements & Risks (CSV)"):
        result_df = pd.merge(structured, risks, on="requirement_id")
        export_path = export_csv(result_df, "requirements_and_risks.csv")
        st.success(f"Exported to {export_path}")

    if st.button("Export Test Cases (CSV)"):
        export_path = export_csv(optimized_cases, "test_cases.csv")
        st.success(f"Exported to {export_path}")

    if st.button("Export Test Suite (JSON)"):
        export_path = export_json(optimized_cases, "test_suite.json")
        st.success(f"Exported to {export_path}")

    if st.button("Export All Test Design Artifacts"):
        artifacts = export_test_artifacts(
            structured,
            coverage_items,
            strategies,
            optimized_cases,
            state_sequences=state_sequences,
        )
        for name, path in artifacts.items():
            st.success(f"{name}: {path}")

    if st.button("Export PyTest Draft"):
        export_path = export_pytest_draft(optimized_cases)
        st.success(f"Exported to {export_path}")
