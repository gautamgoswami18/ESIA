from api_client import APIClient


class EmployeeService:

    def __init__(self):
        self.client = APIClient()

    def get_employees(self, page=1, size=20):

        response = self.client.get(
            "/employees",
            params={
                "page": page,
                "size": size
            }
        )

        return response["data"]

    def get_employee_profile(self, employee_id):

        response = self.client.get(
            f"/employees/{employee_id}/profile"
        )
        print(response)
        return response["data"]