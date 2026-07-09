from app.repository.employee_repository import EmployeeRepository
from app.repository.skill_repository import SkillRepository
from app.repository.project_repository import ProjectRepository
from app.repository.certification_repository import CertificationRepository
from app.repository.resume_repository import ResumeRepository

from app.services.ai_service import AIService


class EmployeeProfileService:

    def __init__(self, db):

        self.employee_repo = EmployeeRepository(db)

        self.skill_repo = SkillRepository(db)

        self.project_repo = ProjectRepository(db)

        self.certification_repo = CertificationRepository(db)

        self.resume_repo = ResumeRepository(db)

        self.ai_service = AIService(db)


    def get_employee_profile(
    self,
    employee_id: int
    ):

        employee = self.employee_repo.get_by_id(employee_id)

        if employee is None:
            return None
        
        skills = self.skill_repo.get_employee_skills(employee_id)

        projects = self.project_repo.get_employee_projects(employee_id)

        certifications = self.certification_repo.get_employee_certifications(employee_id)

        resume = self.resume_repo.get_resume_metadata(employee_id)

        summary = self.ai_service.resume_summary(employee_id)

        return {

            "employee": employee,

            "skills": skills,

            "projects": projects,

            "certifications": certifications,

            "resume": {

                "file_name": resume.get("file_name"),

                "file_path": resume.get("file_path")

            } if resume else None,

            "summary": summary

        }    