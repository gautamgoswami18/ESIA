import mcp

from app.database import SessionLocal
from app.services.ai_service import AIService


def resume_summary(employee_id: int):
    print(">>>>>>>>>> resume_summary called <<<<<<<<<<")
    """
    Generate resume summary.
    """

    db = SessionLocal()

    try:
        service = AIService(db)

        return service.resume_summary(employee_id)

    finally:
        db.close()