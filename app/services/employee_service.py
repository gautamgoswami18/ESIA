from app.repository.employee_repository import EmployeeRepository
from app.core.exceptions import ResourceNotFoundException
from app.schemas.employee_filter import EmployeeFilter


class EmployeeService:

    def __init__(self, db):
        self.repository = EmployeeRepository(db)

    def get_all(
        self,
        page: int,
        size: int,
        filters: EmployeeFilter
    ):
        """
        Get paginated list of employees.
        """
        #print("SERVICE SEARCH =", search)
        return self.repository.get_all(
            page,
            size,
            filters
        )

    def get_by_id(self, employee_id: int):
        """
        Get a single employee by ID.
        """
        employee = self.repository.get_by_id(employee_id)

        if employee is None:
            raise ResourceNotFoundException("Employee")

        return employee
    
    def get_resume_file(self, employee_id: int):
        return self.repository.get_resume_file(employee_id)