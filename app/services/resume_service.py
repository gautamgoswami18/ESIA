from sqlalchemy.orm import Session

from app.repository.resume_repository import ResumeRepository


class ResumeService:

    def __init__(self, db: Session):
        self.repository = ResumeRepository(db)

    def get_all(self):
        return self.repository.get_all()

    def get_by_employee_id(self, employee_id: int):
        return self.repository.get_by_employee_id(employee_id)