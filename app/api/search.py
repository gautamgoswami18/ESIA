from fastapi import APIRouter

from pydantic import BaseModel

from app.schemas.response import APIResponse
from app.services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/resumes")
def search_resumes(request: SearchRequest):

    service = SearchService()

    result = service.search_resumes(
        query=request.query,
        top_k=request.top_k
    )

    return APIResponse(
        success=True,
        message="Matching resumes fetched successfully.",
        data=result
    )