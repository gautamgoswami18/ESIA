from api_client import APIClient


class DashboardService:

    def __init__(self):

        self.client = APIClient()

    def get_summary(self):

        return self.client.get(
            "/dashboard/summary"
        )

    def get_top_skills(self):

        return self.client.get(
            "/dashboard/top-skills"
        )

    def get_experience_distribution(self):

        return self.client.get(
            "/dashboard/experience-distribution"
        )

    def get_certifications(self):

        return self.client.get(
            "/dashboard/certifications"
        )