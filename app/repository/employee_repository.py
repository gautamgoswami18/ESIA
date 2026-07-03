from app.repository.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):

    BASE_SELECT = """
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            e.email,
            e.designation,
            e.location,
            e.experience_years,
            e.domain,
            s.skill_name AS primary_skill,
            e.utilization,
            e.availability,
            e.joining_date,
            e.employment_status
    """

    BASE_FROM = """
        FROM esia.employees e

        LEFT JOIN esia.skills s
            ON e.primary_skill_id = s.skill_id
    """

    # ---------------------------------------------------
    # GET ALL EMPLOYEES
    # ---------------------------------------------------

    def get_all(
        self,
        page: int,
        size: int,
        search: str | None = None
    ):

        params = {}

        # ---------------------------------------
        # WHERE CLAUSE
        # ---------------------------------------

        where_clause = ""

        if search:

            where_clause = """
                WHERE (
                    e.first_name ILIKE :search
                    OR e.last_name ILIKE :search
                    OR e.email ILIKE :search
                    OR e.designation ILIKE :search
                    OR e.location ILIKE :search
                    OR e.domain ILIKE :search
                    OR s.skill_name ILIKE :search
                )
            """

            params["search"] = f"%{search}%"

        # ---------------------------------------
        # DATA QUERY
        # ---------------------------------------

        data_sql = f"""
            {self.BASE_SELECT}

            {self.BASE_FROM}

            {where_clause}

            ORDER BY e.employee_id
        """

        # ---------------------------------------
        # COUNT QUERY
        # ---------------------------------------

        count_sql = f"""
            SELECT COUNT(*)

            {self.BASE_FROM}

            {where_clause}
        """

        # ---------------------------------------
        # PAGINATION
        # ---------------------------------------

        return self.paginate(
            data_sql=data_sql,
            count_sql=count_sql,
            page=page,
            size=size,
            params=params
        )

    # ---------------------------------------------------
    # GET EMPLOYEE BY ID
    # ---------------------------------------------------

    def get_by_id(self, employee_id: int):

        sql = f"""
            {self.BASE_SELECT}

            {self.BASE_FROM}

            WHERE e.employee_id = :employee_id
        """

        result = self.fetch_one(
            sql,
            {"employee_id": employee_id}
        )

        return result