from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository


class CertificationRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)


    def get_employee_certifications(self, employee_id: int):

        sql = """
            SELECT
                c.certification_name,
				c.vendor,
                ec.issue_date,
                ec.expiry_date,
				ec.certification_status
            FROM esia.employee_certifications ec Inner JOIN esia.certifications c
			ON c.certification_id=ec.certification_id
            WHERE employee_id = :employee_id
            ORDER BY issue_date DESC
        """

        return self.fetch_all(
            sql,
            {"employee_id": employee_id}
        )