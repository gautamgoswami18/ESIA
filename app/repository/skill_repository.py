from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository


class SkillRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)


    def get_employee_skills(self, employee_id: int):

        sql = """
            SELECT
                s.skill_name,
                es.proficiency_level,
                es.years_of_experience,
                es.last_used
            FROM esia.employee_skills es
            INNER JOIN esia.skills s
                ON s.skill_id = es.skill_id
            WHERE es.employee_id = :employee_id
            ORDER BY
                es.years_of_experience DESC,
                s.skill_name
        """

        return self.fetch_all(
            sql,
            {"employee_id": employee_id}
        )