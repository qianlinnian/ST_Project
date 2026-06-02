import streamlit as st


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
          grid-template-columns: repeat(5, minmax(0, 1fr));
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
