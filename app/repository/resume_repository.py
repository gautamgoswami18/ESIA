from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository


class ResumeRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):

        sql = text("""

            SELECT

                rm.resume_id,
                rm.employee_id,

                e.first_name,
                e.last_name,
                e.designation,

                rm.file_name,
                rm.file_path,
                rm.version,
                rm.embedding_status,
                rm.upload_date

            FROM esia.resume_metadata rm

            INNER JOIN esia.employees e

                ON rm.employee_id = e.employee_id

            ORDER BY rm.employee_id

        """)

        return self.fetch_all(sql)

    def get_by_employee_id(self, employee_id: int):

        sql = text("""

            SELECT

                rm.resume_id,
                rm.employee_id,

                e.first_name,
                e.last_name,
                e.designation,

                rm.file_name,
                rm.file_path,
                rm.version,
                rm.embedding_status,
                rm.upload_date

            FROM esia.resume_metadata rm

            INNER JOIN esia.employees e

                ON rm.employee_id = e.employee_id

            WHERE rm.employee_id = :employee_id

        """)

        return self.fetch_one(
            sql,
            {"employee_id": employee_id}
        )