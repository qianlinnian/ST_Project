import pandas as pd
import streamlit as st

# A 层入口：app.py 只负责页面、持久化、模型选择和模块结果集成。
from src.ai_client import available_models, available_provider_names, chat_completion, is_llm_enabled
from src.coverage_identifier import identify_coverage_items
from src.exporter import export_csv, export_excel, export_json
from src.performance_tracker import measure_time
from src.persistence import build_project_state, list_projects, load_project, save_project
from src.prompt_templates import COVERAGE_IMPROVEMENT_SYSTEM, coverage_improvement_prompt
from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements
from src.risk_analyzer import analyze_risks
from src.state_modeler import generate_all_transitions_sequence
from src.suite_optimizer import optimize_suite
from src.test_case_generator import generate_test_cases
from src.test_strategy_selector import select_strategies


st.set_page_config(page_title="AutoTestDesign", layout="wide")


def inject_style() -> None:
    """注入 Streamlit 页面的整体视觉样式。"""
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
    """返回内联 SVG 图标，避免在界面中使用 emoji。"""
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
    """渲染统一样式的区块标题。"""
    st.markdown(
        f'<div class="section-title">{line_icon(icon)}<span>{title}</span></div>',
        unsafe_allow_html=True,
    )


def init_state() -> None:
    """初始化 Streamlit 会话状态，避免页面切换时数据丢失。"""
    if "requirements" not in st.session_state:
        st.session_state.requirements = load_sample_requirements()
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = available_provider_names()[0]
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = available_models(st.session_state.selected_provider)[0]
    if "project_name" not in st.session_state:
        st.session_state.project_name = "simpletodolist"


def compute_artifacts() -> dict[str, pd.DataFrame]:
    """执行从需求到测试设计的当前流水线。

    这里是 A 的页面层和 B/C 功能模块之间的集成点。
    B 负责需求、风险和覆盖项；C 负责测试策略和测试用例。
    """
    requirements = st.session_state.requirements
    structuring_time, structured = measure_time(structure_requirements, requirements)
    risk_time, risks = measure_time(analyze_risks, structured)
    coverage_items = identify_coverage_items(structured, risks)
    strategies = select_strategies(coverage_items)
    generation_time, test_cases = measure_time(generate_test_cases, structured, coverage_items, strategies)
    optimized_cases = optimize_suite(test_cases)
    state_sequences = generate_all_transitions_sequence()
    performance = pd.DataFrame(
        [
            {"metric": "requirement_structuring_seconds", "value": round(structuring_time, 4)},
            {"metric": "risk_analysis_seconds", "value": round(risk_time, 4)},
            {"metric": "test_case_generation_seconds", "value": round(generation_time, 4)},
        ]
    )
    traceability = optimized_cases[["test_case_id", "requirement_id", "coverage_id", "technique"]].copy()
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
    """在页面顶部展示项目级统计指标。"""
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


def requirements_from_text(raw_text: str) -> pd.DataFrame:
    """把文本框里的多行需求转换成需求表。每一行视为一条需求。"""
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


inject_style()
init_state()

# 侧边栏控制全局工作流状态：当前页面、项目名、模型服务商和模型。
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

# 页面顶部展示项目说明和统计指标；这里只展示，不修改项目数据。
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
    # 可编辑需求输入表。开发阶段默认使用 mock TodoList 需求。
    with st.container():
        section_header("Requirement Input", "file")
        st.caption("支持 CSV 上传、纯文本输入和表格手动编辑。D/E 正式需求完成前可先使用 mock 数据。")

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
                    st.error("CSV must include requirement_id, module, and requirement_text columns.")

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

if page == "Structuring & Risk":
    # B 负责的输出：结构化需求和风险分析。
    section_header("Requirement Structuring", "file")
    st.dataframe(artifacts["structured_requirements"], width="stretch")
    section_header("Risk Analysis", "risk")
    st.dataframe(artifacts["risk_analysis"], width="stretch")
    st.caption("Performance targets are tracked locally for reporting.")
    st.dataframe(artifacts["performance"], width="stretch")

if page == "Coverage & Strategy":
    # B/C 交接点：B 提供覆盖项，C 选择测试策略。
    section_header("Coverage Items", "map")
    st.dataframe(artifacts["coverage_items"], width="stretch")
    section_header("Coverage Strategy", "map")
    st.dataframe(artifacts["test_strategies"], width="stretch")
    with st.expander("State transition model sequences"):
        st.dataframe(artifacts["state_transition_sequences"], width="stretch")

if page == "Test Cases":
    # C 负责的输出：测试用例。表格可编辑，用于交互式审查。
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

if page == "AI Review":
    # 可选的大模型审查。即使没有配置 API key，本地规则流程也能继续使用。
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
    # 保存/加载用于保留本地项目状态；导出用于生成报告可用的测试工件。
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
            path = export_excel({"test_cases": artifacts["optimized_test_cases"]}, "test_cases.xlsx")
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
