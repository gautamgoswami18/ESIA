import unittest

from app.services.job_fit_score_service import JobFitScoreService


class JobFitScoreTests(unittest.TestCase):

    def test_full_skill_and_role_match_produces_strong_fit(self):
        result = JobFitScoreService.score(
            "find java developer",
            {
                "role": "Associate Software Engineer",
                "experience_years": 2,
                "semantic_score": 46.5,
                "resume_text": (
                    "PROFESSIONAL SUMMARY\nSoftware engineer\n"
                    "PROFESSIONAL EXPERIENCE\nTechnology\nJava\n"
                    "Built Spring Boot applications.\nTRAINING"
                ),
            },
        )

        self.assertEqual(result["matched_requirements"], ["Java"])
        self.assertEqual(result["missing_requirements"], [])
        self.assertEqual(result["score_breakdown"]["role"], 100)
        self.assertEqual(result["match_score"], 86.6)
        self.assertEqual(result["score_band"], "Strong")

    def test_current_role_changes_fit_without_changing_skill_evidence(self):
        developer = JobFitScoreService.score(
            "find java developer",
            {
                "role": "Software Engineer",
                "semantic_score": 46.5,
                "resume_text": (
                    "PROFESSIONAL EXPERIENCE\n"
                    "Java application development.\nTRAINING"
                ),
            },
        )
        manager = JobFitScoreService.score(
            "find java developer",
            {
                "role": "Engineering Manager",
                "semantic_score": 46.5,
                "resume_text": (
                    "PROFESSIONAL EXPERIENCE\n"
                    "Java application development.\nTRAINING"
                ),
            },
        )

        self.assertGreater(
            developer["match_score"],
            manager["match_score"],
        )
        self.assertEqual(
            manager["score_breakdown"]["role"],
            50,
        )

    def test_missing_multi_skill_requirement_is_visible(self):
        result = JobFitScoreService.score(
            "find java developer with react knowledge and AI knowledge",
            {
                "role": "Senior Software Engineer",
                "semantic_score": 50,
                "resume_text": (
                    "PROFESSIONAL EXPERIENCE\n"
                    "Java and React application development.\nTRAINING"
                ),
            },
        )

        self.assertEqual(
            result["matched_requirements"],
            ["Java", "React"],
        )
        self.assertEqual(result["missing_requirements"], ["AI"])
        self.assertEqual(
            result["score_breakdown"]["requirements"],
            66.7,
        )
        self.assertEqual(result["match_score"], 67.5)
        self.assertEqual(result["score_band"], "Good")

    def test_ai_does_not_match_inside_unrelated_words(self):
        result = JobFitScoreService.score(
            "find employee with AI knowledge",
            {
                "role": "Training Coordinator",
                "semantic_score": 50,
                "resume_text": "Responsible for training administration.",
            },
        )

        self.assertEqual(result["matched_requirements"], [])
        self.assertEqual(result["missing_requirements"], ["AI"])

    def test_explicit_experience_requirement_affects_score(self):
        junior = JobFitScoreService.score(
            "find java developer with 5+ years experience",
            {
                "role": "Software Engineer",
                "experience_years": 3,
                "semantic_score": 50,
                "resume_text": "Java development.",
            },
        )
        experienced = JobFitScoreService.score(
            "find java developer with 5+ years experience",
            {
                "role": "Software Engineer",
                "experience_years": 6,
                "semantic_score": 50,
                "resume_text": "Java development.",
            },
        )

        self.assertEqual(
            junior["score_breakdown"]["experience"],
            60,
        )
        self.assertEqual(
            experienced["score_breakdown"]["experience"],
            100,
        )
        self.assertGreater(
            experienced["match_score"],
            junior["match_score"],
        )


if __name__ == "__main__":
    unittest.main()
