from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ai_request import AIRequest
from app.schemas.ai_response import AIResponse

from app.services.ai_service import AIService
from app.schemas.resume_summary import ResumeSummaryResponse
from app.schemas.candidate_compare_schema import CandidateComparisonResponse
from app.database import get_db

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post(
    "/search",
    response_model=AIResponse
)
def search_resume(request: AIRequest):

    service = AIService()

    return service.search_resume(request.question)

@router.get(
    "/resume-summary/{employee_id}",
    response_model=ResumeSummaryResponse
)
def resume_summary(
    employee_id: int,
     db: Session = Depends(get_db)
):
    service = AIService(db)
    
    summary = service.resume_summary(employee_id)

    return ResumeSummaryResponse(
        employee_id=employee_id,
        summary=summary
    )


@router.get(
    "/compare",
    response_model=CandidateComparisonResponse
)
def compare_candidates(
    emp1: int,
    emp2: int,
    db: Session = Depends(get_db)
):

    service = AIService(db)

    result = service.compare_candidates(
        emp1,
        emp2
    )

    return CandidateComparisonResponse(
        comparison=result
    )
"""
@router.post("/intent")
def detect_intent(
    request: AIRequest
):

    service = AIService()

    intent = service.detect_intent(
        request.question
    )

    return {
        "intent": intent
    }

"""