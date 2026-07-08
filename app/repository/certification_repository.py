from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository


class CertificationRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)


def get_employee_certifications(self, employee_id: int):

    sql = """
        SELECT
            certification_name,
            issuing_organization,
            issue_date,
            expiry_date
        FROM esia.employee_certifications
        WHERE employee_id = :employee_id
        ORDER BY issue_date DESC
    """

    return self.fetch_all(
        sql,
        {"employee_id": employee_id}
    )