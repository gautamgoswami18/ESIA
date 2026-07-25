import tempfile
import unittest
from pathlib import Path

from app.utils.resume_storage import ResumeFileStorage


class ResumeFileStorageTests(unittest.TestCase):

    def test_second_upload_replaces_first_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_one = root / "first.pdf"
            source_two = root / "second.pdf"
            resume_folder = root / "documents" / "resumes"

            source_one.write_bytes(b"%PDF-first")
            source_two.write_bytes(b"%PDF-second")

            storage = ResumeFileStorage(resume_folder)

            first_path = storage.store(
                1002,
                "Kiran Nair",
                source_one,
            )
            second_path = storage.store(
                1002,
                "Kiran Nair",
                source_two,
                previous_file_path=first_path,
            )

            self.assertEqual(first_path, second_path)
            self.assertEqual(second_path.name, "EMP1002_Kiran_Nair.pdf")
            self.assertEqual(second_path.read_bytes(), b"%PDF-second")
            self.assertEqual(
                list(resume_folder.glob("*.pdf")),
                [second_path],
            )

    def test_store_removes_legacy_process_named_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "replacement.pdf"
            resume_folder = root / "documents" / "resumes"
            resume_folder.mkdir(parents=True)

            source.write_bytes(b"%PDF-replacement")
            legacy = resume_folder / "employee_1002_process-id.pdf"
            legacy.write_bytes(b"%PDF-old")
            previous_format = resume_folder / "employee_1002.pdf"
            previous_format.write_bytes(b"%PDF-previous-format")

            result = ResumeFileStorage(resume_folder).store(
                1002,
                "Kiran Nair",
                source,
                previous_file_path=legacy,
            )

            self.assertFalse(legacy.exists())
            self.assertFalse(previous_format.exists())
            self.assertEqual(result.read_bytes(), b"%PDF-replacement")
            self.assertEqual(
                list(resume_folder.glob("*.pdf")),
                [result],
            )

    def test_store_never_deletes_another_employees_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "replacement.pdf"
            resume_folder = root / "documents" / "resumes"
            resume_folder.mkdir(parents=True)

            source.write_bytes(b"%PDF-replacement")
            other_employee = resume_folder / "employee_2001.pdf"
            other_employee.write_bytes(b"%PDF-other")

            result = ResumeFileStorage(resume_folder).store(
                1002,
                "Kiran Nair",
                source,
                previous_file_path=other_employee,
            )

            self.assertTrue(other_employee.exists())
            self.assertEqual(result.read_bytes(), b"%PDF-replacement")

    def test_name_change_removes_the_previous_employee_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_one = root / "first.pdf"
            source_two = root / "second.pdf"
            resume_folder = root / "documents" / "resumes"

            source_one.write_bytes(b"%PDF-first")
            source_two.write_bytes(b"%PDF-second")

            storage = ResumeFileStorage(resume_folder)
            previous = storage.store(
                1002,
                "Kiran Nair",
                source_one,
            )
            current = storage.store(
                1002,
                "Kiran Kumar Nair",
                source_two,
                previous_file_path=previous,
            )

            self.assertFalse(previous.exists())
            self.assertEqual(
                current.name,
                "EMP1002_Kiran_Kumar_Nair.pdf",
            )
            self.assertEqual(
                list(resume_folder.glob("*.pdf")),
                [current],
            )


if __name__ == "__main__":
    unittest.main()
