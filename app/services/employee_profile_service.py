from app.ai.chroma_service import ChromaService
from app.repository.employee_repository import EmployeeRepository
from app.repository.resume_repository import ResumeRepository


class EmployeeProfileService:

    def __init__(self, db):
        self.employee_repo = EmployeeRepository(db)
        self.resume_repo = ResumeRepository(db)
        self.chroma = ChromaService()

    def get_employee_profile(self, employee_id: int):
        employee = self.employee_repo.get_by_id(employee_id)
        if employee is None:
            return None

        resume = self.resume_repo.get_resume_metadata(employee_id)
        profile = self.chroma.get_profile(employee_id) or {}

        return {
            "employee": employee,
            "primary_skill": profile.get("primary_skill"),
            "skills": profile.get("skills") or [],
            "projects": profile.get("projects") or [],
            "certifications": profile.get("certifications") or [],
            "training": profile.get("training") or [],
            "resume": {
                "file_name": resume.get("file_name"),
                "file_path": resume.get("file_path"),
                "embedding_status": resume.get("embedding_status"),
            } if resume else None,
            "summary": profile.get("summary") or "",
        }
