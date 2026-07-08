from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository


class ProjectRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)




def get_employee_projects(self, employee_id: int):

    sql = """
        SELECT
            p.project_name,
            p.client_name,
            p.domain,
            ep.role,
            ep.start_date,
            ep.end_date
        FROM esia.employee_projects ep
        INNER JOIN esia.projects p
            ON p.project_id = ep.project_id
        WHERE ep.employee_id = :employee_id
        ORDER BY ep.end_date DESC NULLS LAST
    """

    return self.fetch_all(
        sql,
        {"employee_id": employee_id}
    )