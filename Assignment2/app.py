import streamlit as st
import pandas as pd

from src.ai_client import chat_completion, is_llm_enabled
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.coverage_identifier import identify_coverage_items
from src.test_strategy_selector import select_strategies
from src.test_case_generator import generate_test_cases
from src.performance_tracker import measure_time
from src.prompt_templates import (
    COVERAGE_IMPROVEMENT_SYSTEM,
    coverage_improvement_prompt,
)

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

if page == "1. Requirement Input":
    st.subheader("Requirement Input")
    st.caption(
        "Mock data can be used before D/E provide the final TodoList requirements."
    )
    st.data_editor(
        st.session_state.requirements, num_rows="dynamic", use_container_width=True
    )

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
    structured = structure_requirements(st.session_state.requirements)
    risks = analyze_risks(structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    st.dataframe(coverage_items, use_container_width=True)
    st.dataframe(strategies, use_container_width=True)

if page == "4. Test Cases":
    st.subheader("Generated Test Cases")
    structured = structure_requirements(st.session_state.requirements)
    risks = analyze_risks(structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    elapsed, test_cases = measure_time(
        generate_test_cases, structured, coverage_items, strategies
    )
    st.write(f"Test case generation time: {elapsed:.4f}s")
    st.data_editor(test_cases, num_rows="dynamic", use_container_width=True)

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
        "Exporter scaffold is prepared in src/exporter.py. Implementing CSV export here for FR6."
    )
    from src.exporter import export_csv

    # 模拟把风险分析或测试用例导出
    structured = structure_requirements(st.session_state.requirements)
    risks = analyze_risks(structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    test_cases = generate_test_cases(structured, coverage_items, strategies)

    if st.button("Export Requirements & Risks (CSV)"):
        # 合并 requirement 和 risk 作为演示
        result_df = pd.merge(structured, risks, on="requirement_id")
        export_path = export_csv(result_df, "requirements_and_risks.csv")
        st.success(f"Exported to {export_path}")

    if st.button("Export Test Cases (CSV)"):
        export_path = export_csv(test_cases, "test_cases.csv")
        st.success(f"Exported to {export_path}")
