from app.repository.base_repository import BaseRepository


class DashboardRepository(BaseRepository):

    def __init__(self, db):
        super().__init__(db)



    def get_summary(self):

        sql = """
            SELECT

                (SELECT COUNT(*) FROM esia.employees) employees,

                (SELECT COUNT(*) FROM esia.skills) skills,

                (SELECT COUNT(*) FROM esia.projects) projects,

                (SELECT COUNT(*) FROM esia.resume_metadata) resumes,

                (SELECT COUNT(*) FROM esia.employee_certifications) certifications
        """

        return self.fetch_one(sql)  

    def get_top_skills(self):

        sql = """

            SELECT

                s.skill_name,

                COUNT(*) employee_count

            FROM esia.employee_skills es

            JOIN esia.skills s

                ON s.skill_id = es.skill_id

            GROUP BY s.skill_name

            ORDER BY employee_count DESC

            LIMIT 10

        """

        return self.fetch_all(sql)  
    

    def get_experience_distribution(self):

        sql = """

        SELECT

            CASE

                WHEN experience_years < 2 THEN '0-2 Years'

                WHEN experience_years < 5 THEN '2-5 Years'

                WHEN experience_years < 8 THEN '5-8 Years'

                ELSE '8+ Years'

            END experience_range,

            COUNT(*) employee_count

        FROM esia.employees

        GROUP BY experience_range

        ORDER BY experience_range

        """

        return self.fetch_all(sql)
    
    def get_certification_stats(self):

        sql = """
            SELECT
                c.certification_name,
                COUNT(ec.employee_id) AS total
            FROM esia.employee_certifications ec
            INNER JOIN esia.certifications c
                ON c.certification_id = ec.certification_id
            GROUP BY
                c.certification_name
            ORDER BY total DESC
            LIMIT 10
        """

        return self.fetch_all(sql)
