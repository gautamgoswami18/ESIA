from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.esira_service import ESIRAService
from app.schemas.esira_schema import ESIRARequest
from app.schemas.esira_schema import ESIRAResponse


router = APIRouter(
    prefix="/esira",
    tags=["ESIRA"]
)


@router.post(
    "/esiraChat",
    response_model=ESIRAResponse
)
def ask(
    request: ESIRARequest,
    db: Session = Depends(get_db)
):

    service = ESIRAService(db)

    return service.ask(request.question)