from app.repository.employee_repository import EmployeeRepository
from app.core.exceptions import ResourceNotFoundException
from app.schemas.employee_filter import EmployeeFilter
from app.repository.skill_repository import SkillRepository
from app.repository.project_repository import ProjectRepository
from app.repository.certification_repository import CertificationRepository
from app.repository.resume_repository import ResumeRepository
from app.services.ai_service import AIService



class EmployeeService:

    def __init__(self, db):
        self.repository = EmployeeRepository(db)
        self.skill_repo = SkillRepository(db)
        self.project_repo = ProjectRepository(db)
        self.certification_repo = CertificationRepository(db)
        self.resume_repo = ResumeRepository(db)
        self.ai_service = AIService(db)

    def get_all(
        self,
        page: int,
        size: int,
        filters: EmployeeFilter
    ):
        """
        Get paginated list of employees.
        """
        #print("SERVICE SEARCH =", search)
        return self.repository.get_all(
            page,
            size,
            filters
        )

    def get_by_id(self, employee_id: int):
        """
        Get a single employee by ID.
        """
        employee = self.repository.get_by_id(employee_id)

        if employee is None:
            raise ResourceNotFoundException("Employee")

        return employee
    
    def get_resume_file(self, employee_id: int):
        return self.repository.get_resume_metadata(employee_id)
    
    def get_employee_profile(
    self,
    employee_id: int
    ):
    
        employee = self.employee_repo.get_by_id(employee_id)
    
        if not employee:
            return None
    
        skills = self.skill_repo.get_employee_skills(employee_id)
    
        projects = self.project_repo.get_employee_projects(employee_id)
    
        certifications = self.certification_repo.get_employee_certifications(
            employee_id
        )
    
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