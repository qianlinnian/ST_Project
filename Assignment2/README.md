# AutoTestDesign AI App

This project is a Streamlit-based AutoTestDesign tool for Assignment 2.

Target application:

- `../simpletodolist`

Main responsibilities:

- Import requirements.
- Structure requirements with lightweight NLP.
- Analyze risk with a lightweight AI/ML model.
- Identify coverage items.
- Generate black-box and state-based test designs.
- Generate editable expected results.
- Optimize and export test suites.

## Setup

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Optional LLM API

The tool can run without an external LLM API. In that mode, it uses local rules and lightweight ML scaffolding.

To enable optional AI review:

```powershell
Copy-Item .env.example .env
```

Then fill in:

```text
AUTOTESTDESIGN_LLM_PROVIDERS=deepseek,aliyun

AUTOTESTDESIGN_LLM_DEEPSEEK_API_KEY=
AUTOTESTDESIGN_LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
AUTOTESTDESIGN_LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro,deepseek-chat

AUTOTESTDESIGN_LLM_ALIYUN_API_KEY=
AUTOTESTDESIGN_LLM_ALIYUN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
AUTOTESTDESIGN_LLM_ALIYUN_MODELS=qwen-plus,qwen-max,qwen3.5-plus
```

Each provider should expose an OpenAI-compatible `/chat/completions` interface. The Streamlit sidebar lets the tester switch provider and model before running optional AI review.

## Project Structure

```text
Assignment2/
  app.py
  requirements.txt
  src/
  data/
  exports/
  docs/
  tests/
```

## Notes

The test execution framework, such as Selenium with PyTest, is documented in the test plan and detailed test execution document. The AutoTestDesign tool does not need to run Selenium internally.
