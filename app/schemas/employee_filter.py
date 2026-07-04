from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
class EmployeeFilter(BaseModel):

    search: Optional[str] = None
    location: Optional[str] = None
    skill: Optional[str] = None
    domain: Optional[str] = None
    availability: Optional[str] = None
    employment_status: Optional[str] = None

    min_experience: Optional[float] = None
    max_experience: Optional[float] = None

    sort_by: str = "employee_id"
    sort_order: str = "asc"

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, value):
        if value.lower() not in ["asc", "desc"]:
            raise ValueError("sort_order must be asc or desc")
        return value.lower()

    @field_validator("sort_by")
    @classmethod
    def validate_sort_by(cls, value):

        allowed = {
            "employee_id",
            "first_name",
            "last_name",
            "designation",
            "location",
            "experience_years",
            "domain",
            "joining_date",
            "utilization",
            "employment_status"
        }

        if value not in allowed:
            raise ValueError(f"Invalid sort_by '{value}'")

        return value

    @field_validator("employment_status")
    @classmethod
    def validate_status(cls, value):

        if value is None:
            return value

        allowed = {
            "active",
            "inactive",
            "bench",
            "notice"
        }

        if value.lower() not in allowed:
            raise ValueError("Invalid employment_status")

        return value

    @model_validator(mode="after")
    def validate_experience(self):

        if (
            self.min_experience is not None
            and self.max_experience is not None
            and self.min_experience > self.max_experience
        ):
            raise ValueError(
                "min_experience cannot be greater than max_experience"
            )

        return self