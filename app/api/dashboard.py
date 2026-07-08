from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary")
def summary(
    db: Session = Depends(get_db)
):

    service = DashboardService(db)

    return service.get_summary()

@router.get("/top-skills")
def top_skills(
    db: Session = Depends(get_db)
):

    service = DashboardService(db)

    return service.get_top_skills()

@router.get("/experience-distribution")
def experience_distribution(
    db: Session = Depends(get_db)
):

    service = DashboardService(db)

    return service.get_experience_distribution()

@router.get("/certifications")
def certifications(
    db: Session = Depends(get_db)
):

    service = DashboardService(db)

    return service.get_certification_stats()