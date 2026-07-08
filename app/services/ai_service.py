from app.ai.rag_chain import RAGChain
from app.repository.resume_repository import ResumeRepository
from app.core.exceptions import ResourceNotFoundException
from sqlalchemy.orm import Session

class AIService:

    def __init__(self, db):
        self.db = db
        self.repository = ResumeRepository(db)
        self.rag = RAGChain()
    
    def search_resume(
        self,
        question: str
    ):

        return self.rag.ask(question)
    
    def resume_summary(
        self,
        employee_id: int
    ):

        resume = self.repository.get_resume_metadata(employee_id)
        if resume is None:
            raise ResourceNotFoundException("resume")

        if not resume:
            raise ValueError("Resume not found.")

        if not resume.get("resume_text"):
            raise ValueError("Resume has not been parsed yet.")

        return self.rag.summarize_resume(
            resume["resume_text"]
        )
    
    def compare_candidates(
        self,
        employee1: int,
        employee2: int
    ):

        resume1 = self.repository.get_resume_metadata(employee1)

        resume2 = self.repository.get_resume_metadata(employee2)
        if resume1 is None or resume2 is None:
            raise ResourceNotFoundException(
                f"{'resume1' if resume1 is None else ''}"
                f"{', ' if resume1 is None and resume2 is None else ''}"
                f"{'resume2' if resume2 is None else ''} not found"
            )    
        if not resume1:
            raise ValueError(
                f"Resume not found for Employee {employee1}"
            )

        if not resume2:
            raise ValueError(
                f"Resume not found for Employee {employee2}"
            )

        if not resume1.get("resume_text"):
            raise ValueError(
                f"Resume not parsed for Employee {employee1}"
            )

        if not resume2.get("resume_text"):
            raise ValueError(
                f"Resume not parsed for Employee {employee2}"
            )

        return self.rag.compare_candidates(
            resume1["resume_text"],
            resume2["resume_text"]
        )