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
AUTOTESTDESIGN_LLM_API_KEY=
AUTOTESTDESIGN_LLM_BASE_URL=
AUTOTESTDESIGN_LLM_MODEL=
```

The API should be compatible with the `/chat/completions` interface.

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
