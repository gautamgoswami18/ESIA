from pydantic import BaseModel


class ResumeSummaryResponse(BaseModel):
    employee_id: int
    summary: str