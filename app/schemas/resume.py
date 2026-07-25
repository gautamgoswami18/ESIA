from typing import Optional

from pydantic import BaseModel

from app.schemas.employee_profile_schema import EmployeeProfileResponse


class ResumeProcessResponse(BaseModel):

    process_id: str

    matched: bool

    confidence: float

    action: str

    employee_profile: EmployeeProfileResponse


class ResumeSaveRequest(BaseModel):

    action: str

    employee_id: Optional[int] = None

    employee_profile: EmployeeProfileResponse
