from pydantic import BaseModel, Field
from typing import Any, List


class Candidate(BaseModel):
    rank: int
    employee_id: int
    name: str
    role: str
    experience: str
    match_score: float
    semantic_score: float = 0
    score_band: str = ""
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    matched_requirements: List[str] = Field(default_factory=list)
    missing_requirements: List[str] = Field(default_factory=list)
    matching_skills: List[str]
    reason: str


class AIResponse(BaseModel):
    query: str
    best_candidate: Candidate
    other_candidates: List[Candidate]
    recommendation: str
