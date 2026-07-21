import mcp

from app.database import SessionLocal
from app.services.ai_service import AIService

def search_employee(question: str):
    print(">>>>>>>>>> search_employee called <<<<<<<<<<")
    """
    Search employees using natural language.
    """

    db = SessionLocal()

    try:
        service = AIService(db)

        return service.search_resume(question)

    finally:
        db.close()