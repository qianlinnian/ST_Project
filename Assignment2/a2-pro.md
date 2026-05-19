# Assignment2 Project Brief

This project is `Assignment2`, an AI-assisted software test design tool built with Python and Streamlit.

The selected target system is `simpletodolist`, a lightweight Todo List web application. The main tested feature is Todo Item Management, including adding, editing, deleting, completing, filtering, clearing completed todos, and persistence behavior.

The tool takes software requirements as input and generates a test design package for the selected feature/module. The main workflow is:

1. Import or edit requirements from CSV, plain text, or table input.
2. Structure requirements into fields such as input fields, data ranges, conditions, actions, and expected results.
3. Perform risk analysis and priority assignment.
4. Identify coverage items.
5. Select test design strategies.
6. Generate test cases and an optimized test suite.
7. Generate traceability matrix and export artifacts.

The implementation separates local baseline generation and LLM enhancement:

- Local generation is used for fast and deterministic baseline output.
- LLM calls are used as an optional enhancement layer for review, improvement, and explanation.
- Performance time is tracked separately for local generation and LLM enhancement.

Important modules:

- `Assignment2/app.py`: Streamlit UI and workflow integration.
- `Assignment2/src/ai_client.py`: LLM provider configuration and API calls.
- `Assignment2/src/requirement_parser.py`: requirement structuring pipeline.
- `Assignment2/src/risk_analyzer.py`: risk analysis with LLM fallback support.
- `Assignment2/src/coverage_identifier.py`: coverage item generation.
- `Assignment2/src/test_strategy_selector.py`: black-box test strategy selection.
- `Assignment2/src/test_case_generator.py`: test case generation.
- `Assignment2/src/state_modeler.py`: state transition model and optimized transition sequence generation.
- `Assignment2/src/improvement_engine.py`: LLM-based coverage and test design improvement.
- `Assignment2/src/exporter.py`: CSV, JSON, Excel, traceability, and draft test export.

Supported test design techniques include:

- Equivalence Partitioning
- Boundary Value Analysis
- Decision Table Testing
- State Transition Testing

Current LLM providers are configured through `.env`, mainly DeepSeek and Alibaba Cloud/Qwen. DeepSeek thinking mode is configurable and can be disabled to reduce latency.

To run the Streamlit app:

```powershell
cd D:\course\ST\ST_Project
pip install -r Assignment2\requirements.txt
streamlit run Assignment2\app.py
```

Recent focus:

- Separate local generation buttons from LLM improvement buttons.
- Track local and LLM execution time separately.
- Improve compatibility by pinning dependency versions in `Assignment2/requirements.txt`.
- Reduce LLM latency by disabling DeepSeek thinking mode and discussing prompt/call optimization.
