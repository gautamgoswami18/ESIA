from pydantic import BaseModel
from typing import List


class Candidate(BaseModel):
    rank: int
    name: str
    role: str
    experience: str
    match_score: int
    matching_skills: List[str]
    reason: str


class AIResponse(BaseModel):
    query: str
    best_candidate: Candidate
    other_candidates: List[Candidate]
    recommendation: str