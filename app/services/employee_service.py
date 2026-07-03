from app.repository.employee_repository import EmployeeRepository
from app.core.exceptions import ResourceNotFoundException


class EmployeeService:

    def __init__(self, db):
        self.repository = EmployeeRepository(db)

    def get_all(
        self,
        page: int,
        size: int,
        search: str | None = None
    ):
        """
        Get paginated list of employees.
        """
        #print("SERVICE SEARCH =", search)
        return self.repository.get_all(
            page,
            size,
            search
        )

    def get_by_id(self, employee_id: int):
        """
        Get a single employee by ID.
        """
        employee = self.repository.get_by_id(employee_id)

        if employee is None:
            raise ResourceNotFoundException("Employee")

        return employee