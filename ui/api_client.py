from __future__ import annotations

from typing import Any

import requests

from config import API_BASE_URL


class APIError(RuntimeError):
    """A user-safe representation of a backend request failure."""


class APIClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    @staticmethod
    def _message(response: requests.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return response.text or f"HTTP {response.status_code}"

        if isinstance(payload, dict):
            detail = payload.get("detail")
            if detail:
                return str(detail)
            message = payload.get("message")
            if message:
                return str(message)
        return str(payload)

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        timeout: int = 100,
    ) -> dict:
        try:
            response = self.session.get(
                f"{API_BASE_URL}{endpoint}",
                params=params,
                timeout=timeout,
            )
            if not response.ok:
                raise APIError(self._message(response))
            return response.json()
        except requests.exceptions.RequestException as ex:
            raise APIError(
                "Unable to connect to the ESIA backend. "
                "Confirm FastAPI is running on port 8000."
            ) from ex

    def post(
        self,
        endpoint: str,
        payload: dict | None = None,
        timeout: int = 180,
    ) -> dict:
        try:
            response = self.session.post(
                f"{API_BASE_URL}{endpoint}",
                json=payload or {},
                timeout=timeout,
            )
            if not response.ok:
                raise APIError(self._message(response))
            return response.json()
        except requests.exceptions.RequestException as ex:
            raise APIError(
                "Unable to connect to the ESIA backend. "
                "Confirm FastAPI is running on port 8000."
            ) from ex

    def process_resume(self, uploaded_file) -> dict:
        if uploaded_file is None:
            raise APIError("Please select a PDF resume.")

        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            raise APIError("The selected resume is empty.")

        try:
            response = requests.post(
                f"{API_BASE_URL}/resume/process",
                files={
                    "file": (
                        uploaded_file.name,
                        file_bytes,
                        "application/pdf",
                    )
                },
                headers={"Accept": "application/json"},
                timeout=300,
            )
            if not response.ok:
                raise APIError(self._message(response))
            return response.json()
        except requests.exceptions.Timeout as ex:
            raise APIError(
                "Resume processing timed out. Please try again."
            ) from ex
        except requests.exceptions.RequestException as ex:
            raise APIError(
                "Unable to connect to the ESIA backend. "
                "Confirm FastAPI is running on port 8000."
            ) from ex

    @staticmethod
    def download_url(employee_id: int) -> str:
        return f"{API_BASE_URL}/resume/{employee_id}/download"
