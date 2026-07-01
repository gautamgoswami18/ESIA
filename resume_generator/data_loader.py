"""
===========================================================
Employee Data Loader
Loads all employee data from PostgreSQL
===========================================================
"""

from .database import get_connection
from .models import (
    Employee,
    Skill,
    Project,
    Certification,
    Training,
)


class DataLoader:

    def __init__(self):
        self.conn = get_connection()

    # --------------------------------------------------
    # Public Method
    # --------------------------------------------------

    def load_employees(self):

        employees = self._get_employee_master()

        for emp in employees.values():

            emp.skills = self._get_employee_skills(emp.employee_id)

            emp.projects = self._get_employee_projects(emp.employee_id)

            ##emp.certifications = self._get_employee_certifications(emp.employee_id)

            emp.trainings = self._get_employee_training(emp.employee_id)

            # Primary Skill
            for skill in emp.skills:
                if skill.is_primary:
                    emp.primary_skill = skill.skill_name
                    break

        return list(employees.values())

    # --------------------------------------------------
    # Employee Master
    # --------------------------------------------------

    def _get_employee_master(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                designation,
                location,
                experience_years,
                domain,
                joining_date,
                utilization,
                availability
            FROM employees
            ORDER BY employee_id
        """)

        employees = {}

        for row in cursor.fetchall():

            emp = Employee(

                employee_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                designation=row[4],
                location=row[5],
                experience_years=row[6],
                domain=row[7],
                joining_date=str(row[8]),
                utilization=row[9],
                availability=row[10]

            )

            employees[emp.employee_id] = emp

        cursor.close()

        return employees

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    def _get_employee_skills(self, employee_id):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT

                s.skill_name,

                s.category,

                es.proficiency_level,

                es.years_of_experience,

                es.is_primary

            FROM employee_skills es

            JOIN skills s
              ON es.skill_id = s.skill_id

            WHERE es.employee_id=%s

            ORDER BY es.is_primary DESC,
                     s.skill_name
        """, (employee_id,))

        skills = []

        for row in cursor.fetchall():

            skills.append(

                Skill(

                    skill_name=row[0],
                    category=row[1],
                    proficiency=row[2],
                    years=float(row[3]),
                    is_primary=row[4]

                )

            )

        cursor.close()

        return skills

    # --------------------------------------------------
    # Projects
    # --------------------------------------------------

    def _get_employee_projects(self, employee_id):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                p.project_name,

                p.client_name,

                p.domain,

                p.technology_stack,

                ep.role_name,

                ep.start_date,

                ep.end_date,

                ep.billing_status

            FROM employee_projects ep

            JOIN projects p
                 ON ep.project_id=p.project_id

            WHERE ep.employee_id=%s

            ORDER BY ep.start_date DESC

        """, (employee_id,))

        projects = []

        for row in cursor.fetchall():

            projects.append(

                Project(

                    project_name=row[0],
                    client_name=row[1],
                    domain=row[2],
                    technology_stack=row[3],
                    role_name=row[4],
                    start_date=str(row[5]),
                    end_date=str(row[6]),
                    billing_status=row[7]

                )

            )

        cursor.close()

        return projects

    # --------------------------------------------------
    # Certifications
    # --------------------------------------------------

    def _get_employee_certifications(self, employee_id):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                c.certification_name,

                ec.issue_date,

                ec.expiry_date,

                ec.certification_status,

                ec.certification_score

            FROM employee_certifications ec

            JOIN certifications c

              ON ec.certification_id=c.certification_id

            WHERE ec.employee_id=%s

        """, (employee_id,))

        certs = []

        for row in cursor.fetchall():

            certs.append(

                Certification(

                    certification_name=row[0],

                    issue_date=str(row[1]),

                    expiry_date=str(row[2]),

                    status=row[3],

                    score=row[4]

                )

            )

        cursor.close()

        return certs

    # --------------------------------------------------
    # Training
    # --------------------------------------------------

    def _get_employee_training(self, employee_id):

        cursor = self.conn.cursor()

        cursor.execute("""

            SELECT

                tc.course_name,

                tc.provider,

                tc.technology,

                et.completion_date,

                et.score

            FROM employee_training et

            JOIN training_catalog tc

                 ON tc.training_id=et.training_id

            WHERE et.employee_id=%s

        """, (employee_id,))

        trainings = []

        for row in cursor.fetchall():

            trainings.append(

                Training(

                    course_name=row[0],

                    provider=row[1],

                    technology=row[2],

                    completion_date=str(row[3]),

                    score=row[4] if row[4] else 0

                )

            )

        cursor.close()

        return trainings

    # --------------------------------------------------

    def close(self):

        self.conn.close()