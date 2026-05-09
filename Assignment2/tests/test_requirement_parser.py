from src.requirement_loader import load_sample_requirements
from src.requirement_parser import structure_requirements


def test_structure_requirements_adds_fields():
    requirements = load_sample_requirements()
    structured = structure_requirements(requirements)
    assert "input_fields" in structured.columns
    assert len(structured) == len(requirements)
