from sqlalchemy.orm import Session

from app.repository.resume_repository import ResumeRepository
from app.ai.resume_parser import ResumeParser
from app.ai.embedding_generator import EmbeddingGenerator


class ResumeService:

    def __init__(self, db: Session):
        self.repository = ResumeRepository(db)
        self.parser = ResumeParser()
        self.embedding_generator = EmbeddingGenerator()

    def get_all(self):
        return self.repository.get_all()

    def get_by_employee_id(self, employee_id: int):
        return self.repository.get_by_employee_id(employee_id)
    
    def get_resume_file(self, employee_id: int):
        return self.repository.get_resume_file(employee_id)
    
    def parse_resume(self, employee_id: int):

        # Step 1: Fetch resume metadata
        resume = self.repository.get_resume_file(employee_id)
    
        if not resume:
            raise ValueError("Resume not found")
    
        # Step 2: Extract text from PDF
        resume_text = ResumeParser.extract_text(
            resume["file_path"]
        )
    
        # Step 3: Save extracted text
        self.repository.update_resume_text(
            employee_id,
            resume_text
        )
    
        return {
            "employee_id": employee_id,
            "file_name": resume["file_name"],
            "pages_parsed": len(resume_text.split("\n")),
            "status": "Completed"
        } 

    def generate_embedding(self, employee_id: int):

        resume = self.repository.get_resume_file(employee_id)

        if not resume:
            return None

        resume_text = resume.get("resume_text")

        if not resume_text:
            raise ValueError(
                "Resume has not been parsed yet."
            )

        embedding = self.embedding_generator.generate_embedding(
            resume_text
        )

        return {
            "employee_id": employee_id,
            "dimensions": len(embedding),
            "embedding": embedding
        }     