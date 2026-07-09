from pydantic import BaseModel


class DashboardResponse(BaseModel):

    summary: dict

    top_skills: list

    experience_distribution: list

    certifications: list