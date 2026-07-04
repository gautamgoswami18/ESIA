from fastapi import Query
from app.schemas.employee_filter import EmployeeFilter


def get_employee_filters(
    search: str | None = Query(None),
    location: str | None = Query(None),
    skill: str | None = Query(None),
    domain: str | None = Query(None),
    availability: str | None = Query(None),
    employment_status: str | None = Query(None),
    min_experience: float | None = Query(None, ge=0),
    max_experience: float | None = Query(None, ge=0),
    sort_by: str = Query("employee_id"),
    sort_order: str = Query("asc"),
) -> EmployeeFilter:

    return EmployeeFilter(
        search=search,
        location=location,
        skill=skill,
        domain=domain,
        availability=availability,
        employment_status=employment_status,
        min_experience=min_experience,
        max_experience=max_experience,
        sort_by=sort_by,
        sort_order=sort_order,
    )