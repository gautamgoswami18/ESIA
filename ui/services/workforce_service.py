from __future__ import annotations

from typing import Any

from api_client import APIClient


class WorkforceService:
    """Thin UI adapter around the existing FastAPI contracts."""

    def __init__(self):
        self.client = APIClient()

    def employees(
        self,
        page: int = 1,
        size: int = 20,
        **filters: Any,
    ) -> dict:
        params = {"page": page, "size": size}
        params.update(
            {
                key: value
                for key, value in filters.items()
                if value not in (None, "", "All")
            }
        )
        return self.client.get("/employees/", params=params)

    def employee(self, employee_id: int) -> dict:
        return self.client.get(f"/employees/{employee_id}")

    def employee_profile(self, employee_id: int) -> dict:
        return self.client.get(f"/employees/{employee_id}/profile")

    def resumes(self) -> dict:
        return self.client.get("/resume/")

    def resume(self, employee_id: int) -> dict:
        return self.client.get(f"/resume/{employee_id}")

    def reindex(self, employee_id: int) -> dict:
        return self.client.post(f"/resume/{employee_id}/embedding")

    def parse_resume(self, employee_id: int) -> dict:
        return self.client.post(f"/resume/{employee_id}/parse")

    def save_resume(self, process_id: str) -> dict:
        return self.client.post(
            "/resume/save",
            {"process_id": process_id},
            timeout=300,
        )

    def ask(self, question: str) -> dict:
        return self.client.post(
            "/esira/esiraChat",
            {"question": question},
            timeout=300,
        )
