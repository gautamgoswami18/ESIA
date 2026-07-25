import json

import chromadb


class ChromaService:

    RESUME_COLLECTION = "employee_resumes"
    PROFILE_COLLECTION = "employee_resume_profiles"

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name=self.RESUME_COLLECTION
        )
        self.profile_collection = self.client.get_or_create_collection(
            name=self.PROFILE_COLLECTION
        )

    def add_resume(
        self,
        employee_id: int,
        chunks: list[str],
        embeddings: list[list[float]],
    ):
        if not chunks:
            raise ValueError("Resume produced no indexable chunks.")

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Resume chunks and embeddings must have equal lengths."
            )

        self.collection.upsert(
            ids=[
                f"{employee_id}_{index}"
                for index in range(len(chunks))
            ],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[
                {
                    "employee_id": employee_id,
                    "chunk_id": index,
                    "content_type": "resume_chunk",
                    "schema_version": 1,
                }
                for index in range(len(chunks))
            ],
        )

    def add_profile(
        self,
        employee_id: int,
        profile_json: str,
        embedding: list[float],
    ) -> None:
        self.profile_collection.upsert(
            ids=[str(employee_id)],
            documents=[profile_json],
            embeddings=[embedding],
            metadatas=[
                {
                    "employee_id": employee_id,
                    "content_type": "structured_profile",
                    "schema_version": 1,
                }
            ],
        )

    def get_profile(self, employee_id: int) -> dict | None:
        result = self.profile_collection.get(
            ids=[str(employee_id)],
            include=["documents"],
        )
        documents = result.get("documents") or []

        if documents:
            return self._parse_profile_json(documents[0])

        return self._get_legacy_profile(employee_id)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

    def delete_resume(self, employee_id: int) -> None:
        self.collection.delete(
            where={"employee_id": employee_id}
        )

    def delete_profile(self, employee_id: int) -> None:
        self.profile_collection.delete(
            where={"employee_id": employee_id}
        )

    def _get_legacy_profile(
        self,
        employee_id: int,
    ) -> dict | None:
        result = self.collection.get(
            where={"employee_id": employee_id},
            include=["metadatas", "documents"],
        )
        rows = sorted(
            zip(
                result.get("metadatas") or [],
                result.get("documents") or [],
            ),
            key=lambda row: (row[0] or {}).get("chunk_id", -1),
        )
        chunks = [document or "" for _, document in rows]

        if not chunks or not any(
            "Employee profile:" in chunk
            for chunk in chunks
        ):
            return None

        merged = chunks[0]
        for chunk in chunks[1:]:
            overlap = self._overlap_size(merged, chunk)
            merged += chunk[overlap:]

        marker = merged.find("Employee profile:")
        json_start = merged.find("{", marker)
        if marker < 0 or json_start < 0:
            return None

        try:
            profile, _ = json.JSONDecoder().raw_decode(
                merged[json_start:]
            )
        except json.JSONDecodeError:
            return None

        return profile if isinstance(profile, dict) else None

    @staticmethod
    def _overlap_size(left: str, right: str) -> int:
        maximum = min(500, len(left), len(right))
        for size in range(maximum, 0, -1):
            if left.endswith(right[:size]):
                return size
        return 0

    @staticmethod
    def _parse_profile_json(document: str) -> dict | None:
        try:
            profile = json.loads(document)
        except (json.JSONDecodeError, TypeError):
            return None
        return profile if isinstance(profile, dict) else None
