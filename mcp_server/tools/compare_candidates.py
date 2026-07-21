import mcp

from app.database import SessionLocal
from app.services.ai_service import AIService


def compare_candidates(
    employee1: int,
    employee2: int
):
    print(">>>>>>>>>> compare_candidates called <<<<<<<<<<")
    
    """
    Compare two candidates.
    """

    db = SessionLocal()

    try:
        service = AIService(db)

        return service.compare_candidates(
            employee1,
            employee2
        )

    finally:
        db.close()