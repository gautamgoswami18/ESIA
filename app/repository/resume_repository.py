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
    
    def get_resume_metadata(self, employee_id: int):
        
        sql = """
            SELECT
                file_name,
                file_path,
                resume_text
            FROM esia.resume_metadata
            WHERE employee_id = :employee_id
        """
    
        return self.fetch_one(
            sql,
            {"employee_id": employee_id}
        )
    
    def update_resume_text(
    self,
    employee_id: int,
    resume_text: str
    ):
    
        sql = """
            UPDATE esia.resume_metadata
            SET
                resume_text = :resume_text
            WHERE employee_id = :employee_id
        """
    
        self.execute(
            text(sql),
            {
                "employee_id": employee_id,
                "resume_text": resume_text
            }
        )

    def get_all_resume_employees(self):

        sql = """
            SELECT
                employee_id
            FROM esia.resume_metadata
            ORDER BY employee_id
        """

        return self.fetch_all(sql)    