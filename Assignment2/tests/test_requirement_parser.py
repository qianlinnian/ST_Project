from pathlib import Path

import pandas as pd

from src.requirement_parser import structure_requirements


def test_structure_requirements_adds_fields():
    requirements = pd.read_csv(
        Path(__file__).resolve().parents[1] / "data" / "todo_item_requirement.csv"
    )
    structured = structure_requirements(requirements)
    assert "input_fields" in structured.columns
    assert len(structured) == len(requirements)
