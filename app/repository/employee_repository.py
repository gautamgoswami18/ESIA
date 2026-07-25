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
        "joining_date": "e.joining_date",
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
            NULL::text AS domain,
            NULL::text AS primary_skill,
            NULL::integer AS utilization,
            NULL::text AS availability,
            e.joining_date,
            e.employment_status
    """

    BASE_FROM = """
        FROM esia.employees e

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

        # ---------------------------------------
        # DESIGNATION
        # ---------------------------------------

        designation = filters.designation or filters.domain

        if designation:

            conditions.append(
                "e.designation ILIKE :designation"
            )

            params["designation"] = designation


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
    
    def get_employee_by_email(
        self,
        email: str
    ):

        sql = """
            SELECT
                employee_id,
                first_name,
                last_name,
                email,
                designation,
                experience_years,
                location
            FROM esia.employees
            WHERE LOWER(email) = LOWER(:email)
        """

        return self.fetch_one(
            sql,
            {
                "email": email
            }
        )

    def get_employee_by_name(
        self,
        first_name: str,
        last_name: str | None
    ):

        sql = """
            SELECT employee_id
            FROM esia.employees
            WHERE LOWER(first_name) = LOWER(:first_name)
              AND LOWER(COALESCE(last_name, '')) =
                  LOWER(COALESCE(:last_name, ''))
            ORDER BY employee_id
            LIMIT 1
        """

        return self.fetch_one(
            sql,
            {
                "first_name": first_name,
                "last_name": last_name
            }
        )
    
    
        
    def create_employee(
        self,
        employee
    ) -> int:
    
        sql = """
            INSERT INTO esia.employees
            (
                first_name,
                last_name,
                email,
                designation,
                experience_years,
                location
            )
            VALUES
            (
                :first_name,
                :last_name,
                :email,
                :designation,
                :experience_years,
                :location
            )
            RETURNING employee_id;
        """
    
        result = self.fetch_one(
            sql,
            {
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "designation": employee.designation,
                "experience_years": employee.experience_years,
                "location": employee.location
            }
        )
    
        return result["employee_id"]
    
    def get_employee_by_email(
        self,
        email: str
    ):

        sql = """
            SELECT
                employee_id
            FROM esia.employees
            WHERE LOWER(email) = LOWER(:email)
        """

        return self.fetch_one(
            sql,
            {
                "email": email
            }
        )
    
    def update_employee(
        self,
        employee_id: int,
        employee
    ):

        sql = """
            UPDATE esia.employees
            SET

                first_name = :first_name,

                last_name = :last_name,

                email = :email,

                designation = :designation,

                experience_years = :experience_years,

                location = :location

            WHERE employee_id = :employee_id
        """

        self.execute(
            sql,
            {

                "employee_id": employee_id,

                "first_name": employee.first_name,

                "last_name": employee.last_name,

                "email": employee.email,

                "designation": employee.designation,

                "experience_years": employee.experience_years,

                "location": employee.location

            }
        )

    def save_employee(
        self,
        employee
    ) -> int:

        repository = EmployeeRepository(
            self.db
        )

        existing = repository.get_employee_by_email(
            employee.email
        )

        if existing:

            repository.update_employee(
                existing["employee_id"],
                employee
            )

            return existing["employee_id"]

        return repository.create_employee(
            employee
        )    
