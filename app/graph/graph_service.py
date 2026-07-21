from sqlalchemy.orm import Session

from app.graph.esira_graph import ESIRAGraph
from app.services.ai_service import AIService


class GraphService:

    def __init__(self, db: Session):
        self.ai_service = AIService(db)
        self.graph = ESIRAGraph(self.ai_service)

    async def ask(self, question: str):

        return await self.graph.invoke(question)