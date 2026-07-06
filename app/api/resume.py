from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.response import APIResponse
from app.services.resume_service import ResumeService
from pathlib import Path
from fastapi.responses import FileResponse
from app.core.exceptions import ResourceNotFoundException
from app.ai.embedding_generator import EmbeddingGenerator

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


@router.get("/{employee_id}/download")
def download_resume(
    employee_id: int,
    db: Session = Depends(get_db)
):
    service = ResumeService(db)

    resume = service.get_resume_file(employee_id)
    
    if resume is None:
        raise ResourceNotFoundException("Resume")

    # ESIA project root
    BASE_DIR = Path(__file__).resolve().parents[2]
    
    # Full absolute path
    file_path = BASE_DIR / resume["file_path"]
    
    if not file_path.exists():
        raise ResourceNotFoundException("Resume file")

    return FileResponse(
        path=str(file_path),
        filename=resume["file_name"],
        media_type="application/pdf"
    )


@router.post("/{employee_id}/parse")
def parse_resume(
    employee_id: int,
    db: Session = Depends(get_db)
):
    service = ResumeService(db)

    result = service.parse_resume(employee_id)
    return APIResponse(
            success=True,
            message="Resume parsed successfully.",
            data=result
        )
    
@router.post("/{employee_id}/embedding")
def generate_embedding(
    employee_id: int,
    db: Session = Depends(get_db)
):
    service = ResumeService(db)

    try:
        result = service.generate_embedding(employee_id)

        return APIResponse(
            success=True,
            message="Embedding generated successfully.",
            data=result
        )

    except ValueError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )
    
@router.post(
    "/process-all",
    summary="Parse and Generate Embeddings for All Resumes"
)
def process_all_resumes(
    db: Session = Depends(get_db)
):

    service = ResumeService(db)

    result = service.process_all_resumes()

    return {
        "success": True,
        "message": "Resume processing completed successfully.",
        "data": result
    }