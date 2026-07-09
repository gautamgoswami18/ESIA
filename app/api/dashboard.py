from fastapi import APIRouter, Depends
from app.core.dependencies import get_dashboard_service

from app.services.dashboard_service import DashboardService
from app.schemas.dashboard_schema import DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)
@router.get(
    "",
    response_model=DashboardResponse
)
def get_dashboard(
    service: DashboardService = Depends(get_dashboard_service)
 ):
    return service.get_dashboard()
"""
@router.get("/summary")
def summary(
   service: DashboardService = Depends(get_dashboard_service)
):
    return service.get_summary()

@router.get("/top-skills")
def top_skills(
    service: DashboardService = Depends(get_dashboard_service)
):
    return service.get_top_skills()

@router.get("/experience-distribution")
def experience_distribution(
   service: DashboardService = Depends(get_dashboard_service)
):
    return service.get_experience_distribution()

@router.get("/certifications")
def certifications(
   service: DashboardService = Depends(get_dashboard_service)
):
    return service.get_certification_stats()

    """