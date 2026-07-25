from __future__ import annotations

import os
import re
import shutil
import uuid
from pathlib import Path


class ResumeFileStorage:
    """Stores exactly one deterministic PDF for each employee."""

    def __init__(
        self,
        resume_folder: str | Path = "documents/resumes",
    ):
        self.resume_folder = Path(resume_folder)

    def store(
        self,
        employee_id: int,
        employee_name: str,
        source_pdf_path: str | Path,
        previous_file_path: str | Path | None = None,
    ) -> Path:
        source = Path(source_pdf_path)

        if not source.is_file():
            raise ValueError(f"Resume source file was not found: {source}")

        if source.suffix.lower() != ".pdf":
            raise ValueError("Only PDF resumes can be stored.")

        self.resume_folder.mkdir(parents=True, exist_ok=True)

        safe_employee_name = self._safe_employee_name(employee_name)
        destination = self.resume_folder / (
            f"EMP{employee_id}_{safe_employee_name}.pdf"
        )
        temporary = self.resume_folder / (
            f".{destination.name}.{uuid.uuid4().hex}.tmp"
        )

        try:
            shutil.copy2(source, temporary)
            os.replace(temporary, destination)
        finally:
            temporary.unlink(missing_ok=True)

        self._remove_stale_files(
            employee_id=employee_id,
            destination=destination,
            previous_file_path=previous_file_path,
        )

        return destination

    def _remove_stale_files(
        self,
        employee_id: int,
        destination: Path,
        previous_file_path: str | Path | None,
    ) -> None:
        folder = self.resume_folder.resolve()
        destination_resolved = destination.resolve()
        candidates = list(
            self.resume_folder.glob(f"employee_{employee_id}_*.pdf")
        )
        candidates.extend(
            self.resume_folder.glob(f"{employee_id}_employee_*.pdf")
        )
        candidates.extend(
            self.resume_folder.glob(f"EMP{employee_id}_employee_*.pdf")
        )
        candidates.extend(
            self.resume_folder.glob(f"EMP{employee_id}_*.pdf")
        )
        candidates.append(
            self.resume_folder / f"{employee_id}_employee.pdf"
        )
        candidates.append(
            self.resume_folder / f"employee_{employee_id}.pdf"
        )

        if previous_file_path:
            previous = Path(previous_file_path)
            if not previous.is_absolute():
                previous = Path.cwd() / previous

            previous = previous.resolve()
            is_employee_file = (
                previous.name == destination.name
                or previous.name == f"employee_{employee_id}.pdf"
                or previous.name == f"{employee_id}_employee.pdf"
                or previous.name.startswith(f"employee_{employee_id}_")
                or previous.name.startswith(f"{employee_id}_employee_")
                or previous.name.startswith(
                    f"EMP{employee_id}_employee_"
                )
                or previous.name.startswith(f"EMP{employee_id}_")
            )
            if (
                previous.parent == folder
                and previous.suffix.lower() == ".pdf"
                and is_employee_file
            ):
                candidates.append(previous)

        for candidate in candidates:
            resolved_candidate = candidate.resolve()
            if (
                resolved_candidate.parent == folder
                and resolved_candidate != destination_resolved
                and resolved_candidate.is_file()
            ):
                resolved_candidate.unlink()

    @staticmethod
    def _safe_employee_name(employee_name: str) -> str:
        normalized = re.sub(
            r"[^\w-]+",
            "_",
            (employee_name or "").strip(),
            flags=re.UNICODE,
        )
        normalized = re.sub(r"_+", "_", normalized).strip("_-")
        return normalized or "Employee"
