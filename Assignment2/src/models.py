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
    impact: float = 0.0  # 业务影响、安全影响、财务影响等 (0.0-1.0)
    probability: float = 0.0  # 缺陷发生的可能性 / Likelihood (0.0-1.0)
    risk_score: float = 0.0  # 通常 = impact * probability，或加权
    risk_level: str = "Low"  # High, Medium, Low
    reason: str = ""


@dataclass
class CoverageItem:
    """Test coverage item for traceability and test design (aligned with ISTQB)."""
    
    coverage_id: str                    # COV-001
    requirement_id: str                 # Traceability
    description: str                    # Clear description of what needs to be covered
    
    # 推荐核心扩展字段
    coverage_type: str = "Functional"   # Functional, Input, Boundary, Condition, Error, etc.
    risk_level: str = "Medium"          # High, Medium, Low （直接来自 RiskRecord）
    
    # 可选但强烈推荐的字段
    related_techniques: List[str] = field(default_factory=list)  # e.g. ["EP", "BVA", "Decision Table"]
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
