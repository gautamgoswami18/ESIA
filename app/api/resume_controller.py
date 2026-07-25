from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.response import APIResponse
from app.schemas.save_resume import SaveResumeRequest
from app.services.resume_service import ResumeService

router = APIRouter()


@router.post("/save")
def save_resume(
    request: SaveResumeRequest,
    db: Session = Depends(get_db)
):

    service = ResumeService(db)

    try:

        result = service.save_resume(
            request.process_id
        )

        return APIResponse(
            success=True,
            message="Employee saved successfully.",
            data=result
        )

    except Exception as ex:

        raise HTTPException(
            status_code=500,
            detail=str(ex)
        )