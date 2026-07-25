import unittest
from unittest.mock import patch

from app.ai.resume_chunker import ResumeChunker
from app.services.resume_service import ResumeService


class FakeResumeRepository:

    def __init__(self):
        self.statuses = []

    def update_embedding_status(
        self,
        employee_id: int,
        status: bool,
    ):
        self.statuses.append((employee_id, status))


class FakeChromaService:

    def __init__(self, fail_upsert: bool = False):
        self.fail_upsert = fail_upsert
        self.deleted = []
        self.added = []

    def get_profile(self, employee_id: int):
        return None

    def delete_resume(self, employee_id: int):
        self.deleted.append(employee_id)

    def add_resume(
        self,
        employee_id: int,
        chunks: list[str],
        embeddings: list[list[float]],
    ):
        if self.fail_upsert:
            raise RuntimeError("Chroma upsert failed")
        self.added.append((employee_id, chunks, embeddings))


class ResumeReindexTests(unittest.TestCase):

    def test_chunker_rejects_boilerplate_only_chunks(self):
        self.assertFalse(ResumeChunker._is_indexable("Employee profile:"))
        self.assertFalse(ResumeChunker._is_indexable(" Resume text: \n"))
        self.assertTrue(
            ResumeChunker._is_indexable(
                "Java developer with Spring Boot experience"
            )
        )

    @patch(
        "app.services.resume_service.EmbeddingGenerator.generate_embedding",
        return_value=[0.1, 0.2],
    )
    def test_status_becomes_true_only_after_chroma_success(
        self,
        _embedding,
    ):
        repository = FakeResumeRepository()
        chroma = FakeChromaService()
        service = ResumeService.__new__(ResumeService)
        service.repository = repository

        with patch(
            "app.services.resume_service.ChromaService",
            return_value=chroma,
        ):
            count = service._replace_chroma_index(
                employee_id=1002,
                resume_text=(
                    "Java developer with Spring Boot and PostgreSQL "
                    "experience."
                ),
            )

        self.assertEqual(count, 1)
        self.assertEqual(
            repository.statuses,
            [(1002, False), (1002, True)],
        )
        self.assertEqual(chroma.deleted, [1002])
        self.assertEqual(chroma.added[0][0], 1002)

    @patch(
        "app.services.resume_service.EmbeddingGenerator.generate_embedding",
        return_value=[0.1, 0.2],
    )
    def test_status_stays_false_when_chroma_upsert_fails(
        self,
        _embedding,
    ):
        repository = FakeResumeRepository()
        chroma = FakeChromaService(fail_upsert=True)
        service = ResumeService.__new__(ResumeService)
        service.repository = repository

        with patch(
            "app.services.resume_service.ChromaService",
            return_value=chroma,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Chroma upsert failed",
            ):
                service._replace_chroma_index(
                    employee_id=1002,
                    resume_text=(
                        "Java developer with Spring Boot and PostgreSQL "
                        "experience."
                    ),
                )

        self.assertEqual(repository.statuses, [(1002, False)])


if __name__ == "__main__":
    unittest.main()
