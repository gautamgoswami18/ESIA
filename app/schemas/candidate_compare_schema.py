from pydantic import BaseModel


class CandidateComparisonResponse(BaseModel):
    comparison: str