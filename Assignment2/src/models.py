from dataclasses import dataclass


@dataclass
class Requirement:
    requirement_id: str
    module: str
    requirement_text: str


@dataclass
class RiskRecord:
    requirement_id: str
    risk_score: float
    risk_level: str


@dataclass
class CoverageItem:
    coverage_id: str
    requirement_id: str
    description: str


@dataclass
class TestStrategy:
    coverage_id: str
    technique: str


@dataclass
class TestCase:
    test_case_id: str
    requirement_id: str
    coverage_id: str
    technique: str
    steps: str
    expected_result: str
    priority: str
