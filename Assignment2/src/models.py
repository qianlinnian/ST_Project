from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Requirement:
    requirement_id: str
    requirement_text: str
    module: str = ""
    input_fields: List[str] = field(default_factory=list)
    data_ranges: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)


@dataclass
class RiskRecord:
    requirement_id: str
    risk_description: str
    risk_id: str = ""
    risk_category: str = "functional suitability"
    impact: int = 1  # 1, 2, or 3
    likelihood: int = 1  # 1, 2, or 3
    risk_score: int = 1  # likelihood * impact
    risk_level: str = "Low"  # High, Medium, Low
    reason: str = ""
    test_suggestion: str = ""

    def to_dict(self) -> dict:
        """Convert to dict for JSON/CSV export (FR 6.0)"""
        return {
            "risk_id": self.risk_id,
            "requirement_id": self.requirement_id,
            "risk_description": self.risk_description,
            "risk_category": self.risk_category,
            "impact": self.impact,
            "likelihood": self.likelihood,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "reason": self.reason,
            "test_suggestion": self.test_suggestion,
        }


@dataclass
class CoverageItem:
    """Test coverage item for traceability and test design (aligned with ISTQB)."""

    coverage_id: str  # COV-001
    requirement_id: str  # Traceability
    description: str  # Clear description of what needs to be covered

    # 推荐核心扩展字段
    coverage_type: str = (
        "Functional"  # Functional, Input, Boundary, Condition, Error, etc.
    )
    risk_level: str = "Medium"  # High, Medium, Low （直接来自 RiskRecord）

    # 可选但强烈推荐的字段
    related_techniques: List[str] = field(
        default_factory=list
    )  # e.g. ["EP", "BVA", "Decision Table"]
    tags: List[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert to dict for JSON/CSV export (FR 6.0)"""
        return {
            "coverage_id": self.coverage_id,
            "requirement_id": self.requirement_id,
            "description": self.description,
            "coverage_type": self.coverage_type,
            "risk_level": self.risk_level,
            "related_techniques": self.related_techniques,
            "tags": self.tags,
            "notes": self.notes,
        }


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
    precondition: str
    test_data: str
    steps: str
    expected_result: str
    priority: str
    risk_score: float
