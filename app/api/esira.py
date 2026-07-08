from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.esira_service import ESIRAService

from app.schemas.esira_schema import (
    ESIRARequest,
    ESIRAResponse
)

from app.services.esira_service import ESIRAService

router = APIRouter(
    prefix="/esira",
    tags=["ESIRA"]
)

@router.post("/esiraChat")
def ask(request: ESIRARequest, db: Session = Depends(get_db)):

    service = ESIRAService(db)

    return service.ask(request.question)