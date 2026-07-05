from app.repository.base_repository import BaseRepository
from app.schemas.employee_filter import EmployeeFilter

class EmployeeRepository(BaseRepository):

    ALLOWED_SORT_COLUMNS = {
        "employee_id": "e.employee_id",
        "first_name": "e.first_name",
        "last_name": "e.last_name",
        "designation": "e.designation",
        "location": "e.location",
        "experience_years": "e.experience_years",
        "domain": "e.domain",
        "joining_date": "e.joining_date",
        "utilization": "e.utilization",
        "employment_status": "e.employment_status"
    }

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
        filters: EmployeeFilter
    ):

        params = {}
        conditions = []

        # ---------------------------------------
        # WHERE CLAUSE
        # ---------------------------------------

        where_clause = ""

        if filters.search:
        
            conditions.append("""
                (
                    e.first_name ILIKE :search
                    OR e.last_name ILIKE :search
                    OR e.email ILIKE :search
                    OR e.designation ILIKE :search
                    OR e.location ILIKE :search
                    OR e.domain ILIKE :search
                    OR s.skill_name ILIKE :search
                )
            """)
        
            params["search"] = f"%{filters.search}%"
        # ---------------------------------------
        # LOCATION FILTER
        # ---------------------------------------

        if filters.location:
        
            conditions.append(
                "e.location ILIKE :location"
            )

            params["location"] = filters.location
        # ---------------------------------------
        # PRIMARY SKILL
        # ---------------------------------------

        if filters.skill:

            conditions.append(
                "s.skill_name ILIKE :skill"
            )

            params["skill"] = filters.skill


        # ---------------------------------------
        # DOMAIN
        # ---------------------------------------

        if filters.domain:

            conditions.append(
                "e.domain ILIKE :domain"
            )

            params["domain"] = filters.domain


        # ---------------------------------------
        # AVAILABILITY
        # ---------------------------------------

        if filters.availability:

            conditions.append(
                "e.availability = :availability"
            )

            params["availability"] = filters.availability


        # ---------------------------------------
        # EMPLOYMENT STATUS
        # ---------------------------------------

        if filters.employment_status:

            conditions.append(
                "e.employment_status ILIKE :employment_status"
            )

            params["employment_status"] = filters.employment_status


        # ---------------------------------------
        # MIN EXPERIENCE
        # ---------------------------------------

        if filters.min_experience is not None:

            conditions.append(
                "e.experience_years >= :min_experience"
            )

            params["min_experience"] = filters.min_experience


        # ---------------------------------------
        # MAX EXPERIENCE
        # ---------------------------------------

        if filters.max_experience is not None:

            conditions.append(
                "e.experience_years <= :max_experience"
            )

            params["max_experience"] = filters.max_experience



        # ---------------------------------------
        # BUILD WHERE CLAUSE
        # ---------------------------------------

        where_clause = ""

        if conditions:
        
            where_clause = "WHERE " + " AND ".join(conditions)
        # ---------------------------------------
        # SORTING
        # ---------------------------------------

        sort_column = self.ALLOWED_SORT_COLUMNS.get(
            filters.sort_by,
            "e.employee_id"
        )

        sort_order = (
            "DESC"
            if filters.sort_order.lower() == "desc"
            else "ASC"
        )

        # ---------------------------------------
        # DATA QUERY
        # ---------------------------------------

        data_sql = f"""
            {self.BASE_SELECT}

            {self.BASE_FROM}

            {where_clause}

            ORDER BY {sort_column} {sort_order}
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