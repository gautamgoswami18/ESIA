from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class EmployeeResponse(BaseModel):

    employee_id: int

    first_name: str

    last_name: str

    email: EmailStr

    designation: Optional[str]

    location: Optional[str]

    experience_years: Optional[float]

    domain: Optional[str]

    primary_skill: Optional[str]

    utilization: Optional[int]

    availability: Optional[str]

    joining_date: Optional[date]

    employment_status: Optional[str]

    class Config:
        from_attributes = True