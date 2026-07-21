from sqlalchemy.orm import Session

from app.graph.graph_service import GraphService
from app.schemas.esira_schema import ESIRAResponse

class ESIRAService:

    def __init__(self, db: Session):
        self.graph_service = GraphService(db)

    async def ask(self, question: str)-> ESIRAResponse:
        try:
            return await self.graph_service.ask(question)
         
        except Exception as ex:
            return ESIRAResponse(
                intent="ERROR",
                content_type="text",
                answer=str(ex)
            )