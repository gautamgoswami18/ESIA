from collections import OrderedDict
from typing import Any

from app.repository.employee_repository import EmployeeRepository
from app.repository.search_repository import SearchRepository
from app.services.job_fit_score_service import JobFitScoreService


class SearchService:

    def __init__(
        self,
        db=None,
        repository=None,
        employee_repository=None,
    ):
        self.repository = repository or SearchRepository()
        self.employee_repository = (
            employee_repository
            or (EmployeeRepository(db) if db is not None else None)
        )

    def search_resumes(
        self,
        query: str,
        top_k: int = 5
    ):
        if not query or not query.strip():
            return []
        if top_k < 1:
            return []

        results = self.repository.search_resumes(
            query=query,
            # Retrieve a wider semantic pool, then apply explainable job-fit
            # reranking at employee level.
            top_k=max(top_k * 40, 120),
        )

        ids = self._first_batch(results.get("ids"))
        metadatas = self._first_batch(results.get("metadatas"))
        documents = self._first_batch(results.get("documents"))
        distances = self._first_batch(results.get("distances"))

        employees: OrderedDict[Any, dict] = OrderedDict()

        for index, result_id in enumerate(ids):
            metadata = (
                metadatas[index]
                if index < len(metadatas) and metadatas[index]
                else {}
            )
            employee_id = self._employee_id(metadata, result_id)
            if employee_id is None:
                continue

            distance = self._distance_at(distances, index)
            document = (
                str(documents[index])
                if index < len(documents) and documents[index]
                else ""
            )

            candidate = employees.setdefault(
                employee_id,
                {
                    "employee_id": employee_id,
                    "distance": distance,
                    "resume_chunks": [],
                },
            )
            candidate["distance"] = min(
                candidate["distance"],
                distance,
            )
            if document and document not in candidate["resume_chunks"]:
                candidate["resume_chunks"].append(document)

        candidate_pool = sorted(
            employees.values(),
            key=lambda candidate: candidate["distance"],
        )[:max(top_k * 5, 15)]

        response = []
        for candidate in candidate_pool:
            employee = self._get_employee(candidate["employee_id"])
            name = self._employee_name(employee)
            experience = self._experience(employee)
            distance = candidate["distance"]
            resume_text = self._employee_resume_text(candidate)
            semantic_score = self.score_from_distance(distance)

            item = {
                "employee_id": candidate["employee_id"],
                "name": name,
                "role": (employee or {}).get("designation") or "",
                "experience": experience,
                "experience_years": (
                    (employee or {}).get("experience_years")
                ),
                "employment_status": (
                    (employee or {}).get("employment_status") or ""
                ),
                "availability": (
                    (employee or {}).get("availability") or ""
                ),
                "distance": round(distance, 4),
                "semantic_score": semantic_score,
                "resume_text": resume_text[:12000],
            }
            item.update(
                JobFitScoreService.score(
                    query=query,
                    candidate=item,
                )
            )
            response.append(item)

        response.sort(
            key=lambda candidate: (
                -candidate["match_score"],
                candidate["distance"],
            )
        )
        response = response[:top_k]
        for rank, candidate in enumerate(response, start=1):
            candidate["rank"] = rank

        return response

    @staticmethod
    def score_from_distance(distance: float) -> float:
        """Return a stable, monotonic relevance percentage for an L2 distance."""
        safe_distance = max(0.0, float(distance))
        score = round(100.0 / (1.0 + safe_distance), 1)
        return max(0, min(score, 100))

    @staticmethod
    def _first_batch(value) -> list:
        if not value:
            return []
        first = value[0]
        return first if isinstance(first, list) else list(value)

    @staticmethod
    def _distance_at(distances: list, index: int) -> float:
        if index >= len(distances) or distances[index] is None:
            return float("inf")
        try:
            return max(0.0, float(distances[index]))
        except (TypeError, ValueError):
            return float("inf")

    @staticmethod
    def _employee_id(metadata: dict, result_id) -> int | str | None:
        employee_id = metadata.get("employee_id")
        if employee_id is None and result_id is not None:
            employee_id = str(result_id).split("_", 1)[0]
        if employee_id in (None, ""):
            return None
        try:
            return int(employee_id)
        except (TypeError, ValueError):
            return str(employee_id)

    def _get_employee(self, employee_id) -> dict | None:
        if self.employee_repository is None:
            return None
        try:
            return self.employee_repository.get_by_id(int(employee_id))
        except (TypeError, ValueError):
            return None

    def _employee_resume_text(self, candidate: dict) -> str:
        getter = getattr(
            self.repository,
            "get_employee_documents",
            None,
        )
        documents = []
        if callable(getter):
            try:
                documents = getter(candidate["employee_id"])
            except Exception:
                documents = []
        if not documents:
            documents = candidate.get("resume_chunks") or []
        return "\n\n".join(
            str(document)
            for document in documents
            if document
        )

    @staticmethod
    def _employee_name(employee: dict | None) -> str:
        if not employee:
            return ""
        return " ".join(
            str(value).strip()
            for value in (
                employee.get("first_name"),
                employee.get("last_name"),
            )
            if value and str(value).strip()
        )

    @staticmethod
    def _experience(employee: dict | None) -> str:
        if not employee:
            return ""
        value = employee.get("experience_years")
        if value is None:
            return ""
        try:
            years = float(value)
        except (TypeError, ValueError):
            return str(value)
        formatted = f"{years:.1f}".rstrip("0").rstrip(".")
        return f"{formatted} years"
