from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.response import APIResponse
from app.services.resume_service import ResumeService

router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


@router.get("/")
def get_resumes(db: Session = Depends(get_db)):

    service = ResumeService(db)

    resumes = service.get_all()

    return APIResponse(
        success=True,
        message="Resumes fetched successfully",
        data=resumes
    )


@router.get("/{employee_id}")
def get_resume(
    employee_id: int,
    db: Session = Depends(get_db)
):

    service = ResumeService(db)

    resume = service.get_by_employee_id(employee_id)

    if resume is None:

        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    return APIResponse(
        success=True,
        message="Resume fetched successfully",
        data=resume
    )