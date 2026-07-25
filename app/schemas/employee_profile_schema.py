from typing import Any

from pydantic import BaseModel, Field


class SkillResponse(BaseModel):

    name: str
    category: str | None = None
    proficiency: str | None = None
    years_of_experience: float | None = None


class ProjectResponse(BaseModel):

    name: str
    client: str | None = None
    domain: str | None = None
    description: str | None = None
    role: str | None = None
    technologies: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)


class CertificationResponse(BaseModel):

    name: str
    issuing_organization: str | None = None
    issue_date: str | None = None
    expiry_date: str | None = None
    credential_id: str | None = None


class TrainingResponse(BaseModel):

    name: str
    technology: str | None = None
    provider: str | None = None
    score: str | float | None = None


class EmployeeProfileResponse(BaseModel):

    first_name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None

    designation: str | None = None
    department: str | None = None
    location: str | None = None

    experience_years: float = 0.0
    primary_skill: str | None = None

    skills: list[SkillResponse] = Field(default_factory=list)
    projects: list[ProjectResponse] = Field(default_factory=list)
    certifications: list[CertificationResponse] = Field(
        default_factory=list
    )
    training: list[TrainingResponse] = Field(default_factory=list)

    summary: str | None = None
