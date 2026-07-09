from api_client import APIClient


class DashboardService:

    def __init__(self):
        self.client = APIClient()

    def get_dashboard(self) -> dict:
        """
        Returns complete dashboard data.
        """
        return self.client.get("/dashboard")