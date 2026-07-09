from typing import Optional

from pydantic import BaseModel


class SkillResponse(BaseModel):
    skill_name: str
    proficiency_level: Optional[str] = None
    years_of_experience: Optional[float] = None
    last_used: Optional[str] = None


class ProjectResponse(BaseModel):
    project_name: str
    client_name: Optional[str] = None
    domain: Optional[str] = None
    role_name: Optional[str] = None
    allocation_percentage: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class CertificationResponse(BaseModel):
    certification_name: str
    vendor: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    certification_status: Optional[str] = None


class ResumeResponse(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    #resume_text: Optional[str] = None


class EmployeeResponse(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    designation: Optional[str] = None
    experience_years: Optional[float] = None
    email: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    primary_skill: Optional[str] = None


class EmployeeProfileResponse(BaseModel):

    employee: EmployeeResponse

    skills: list[SkillResponse]

    projects: list[ProjectResponse]

    certifications: list[CertificationResponse]

    resume: Optional[ResumeResponse] = None

    summary: str