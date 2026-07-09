from app.repository.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):

        self.dashboard_repo = DashboardRepository(db)

    def get_summary(self):
        print("Calling Summary API")
        return self.dashboard_repo.get_summary()

    def get_top_skills(self):

        return self.dashboard_repo.get_top_skills()

    def get_experience_distribution(self):

        return self.dashboard_repo.get_experience_distribution()

    def get_certification_stats(self):

        return self.dashboard_repo.get_certification_stats()
    
    def get_dashboard(self):

        return {

            "summary": self.dashboard_repo.get_summary(),

            "top_skills": self.get_top_skills(),

            "experience_distribution": self.get_experience_distribution(),

            "certifications": self.get_certification_stats()

        }