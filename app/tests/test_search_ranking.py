import unittest

from app.ai.search_grounding import ground_search_response
from app.services.search_service import SearchService


class FakeSearchRepository:

    def search_resumes(self, query: str, top_k: int):
        return {
            "ids": [["1002_0", "1002_1", "1001_0", "1003_0"]],
            "metadatas": [[
                {"employee_id": 1002},
                {"employee_id": 1002},
                {"employee_id": 1001},
                {"employee_id": 1003},
            ]],
            "documents": [[
                "PROFESSIONAL EXPERIENCE\nKiran AWS project",
                "AWS delivery details\nTRAINING",
                "PROFESSIONAL EXPERIENCE\nPriya AWS project\nTRAINING",
                "Third resume chunk",
            ]],
            "distances": [[0.4, 0.2, 0.3, 1.0]],
        }


class FakeEmployeeRepository:

    EMPLOYEES = {
        1001: {
            "first_name": "Priya",
            "last_name": "Singh",
            "designation": "Technical Lead",
            "experience_years": 11.6,
            "employment_status": "Active",
            "availability": None,
        },
        1002: {
            "first_name": "Kiran",
            "last_name": "Nair",
            "designation": "Lead Software Engineer",
            "experience_years": 6.4,
            "employment_status": "Active",
            "availability": None,
        },
        1003: {
            "first_name": "Manoj",
            "last_name": "Sharma",
            "designation": "Software Engineer",
            "experience_years": 3.0,
            "employment_status": "Active",
            "availability": None,
        },
    }

    def get_by_id(self, employee_id: int):
        return self.EMPLOYEES.get(employee_id)


class SearchRankingTests(unittest.TestCase):

    def setUp(self):
        self.service = SearchService(
            repository=FakeSearchRepository(),
            employee_repository=FakeEmployeeRepository(),
        )

    def test_search_groups_chunks_and_ranks_distinct_employees(self):
        candidates = self.service.search_resumes("AWS", top_k=3)

        self.assertEqual(
            [candidate["employee_id"] for candidate in candidates],
            [1002, 1001, 1003],
        )
        self.assertEqual(
            [candidate["rank"] for candidate in candidates],
            [1, 2, 3],
        )
        self.assertEqual(candidates[0]["name"], "Kiran Nair")
        self.assertEqual(candidates[0]["semantic_score"], 83.3)
        self.assertEqual(candidates[0]["match_score"], 95.1)
        self.assertEqual(
            candidates[0]["matched_requirements"],
            ["AWS"],
        )
        self.assertIn(
            "PROFESSIONAL EXPERIENCE",
            candidates[0]["resume_text"],
        )
        self.assertIn(
            "AWS delivery details",
            candidates[0]["resume_text"],
        )

    def test_grounding_rejects_llm_identity_rank_and_score_changes(self):
        candidates = self.service.search_resumes("AWS", top_k=2)
        generated = {
            "best_candidate": {
                "rank": 1,
                "employee_id": 1001,
                "name": "Wrong name",
                "match_score": 99,
                "matching_skills": ["AWS"],
                "reason": "Priya evidence",
            },
            "other_candidates": [
                {
                    "rank": 2,
                    "employee_id": 1002,
                    "name": "Employee",
                    "match_score": 1,
                    "matching_skills": ["AWS", "Docker"],
                    "reason": "Kiran evidence",
                }
            ],
            "recommendation": "Wrong recommendation",
        }

        result = ground_search_response(
            "Find AWS employees",
            candidates,
            generated,
        )

        self.assertEqual(result["best_candidate"]["employee_id"], 1002)
        self.assertEqual(result["best_candidate"]["name"], "Kiran Nair")
        self.assertEqual(result["best_candidate"]["match_score"], 95.1)
        self.assertEqual(
            result["best_candidate"]["reason"],
            "Kiran evidence",
        )
        self.assertEqual(
            result["other_candidates"][0]["employee_id"],
            1001,
        )
        self.assertIn(
            "Kiran Nair has the highest job-fit score",
            result["recommendation"],
        )

    def test_distance_score_is_monotonic_and_bounded(self):
        self.assertEqual(SearchService.score_from_distance(0), 100)
        self.assertGreater(
            SearchService.score_from_distance(0.2),
            SearchService.score_from_distance(0.8),
        )
        self.assertEqual(
            SearchService.score_from_distance(float("inf")),
            0,
        )


if __name__ == "__main__":
    unittest.main()
