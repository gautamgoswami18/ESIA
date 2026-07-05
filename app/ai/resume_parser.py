import fitz  # PyMuPDF
from pathlib import Path


class ResumeParser:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from a PDF resume.

        Args:
            file_path: Absolute path of the PDF file.

        Returns:
            Extracted text as a string.
        """

        pdf_path = Path(file_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"Resume file not found: {file_path}"
            )

        text = ""

        with fitz.open(pdf_path) as document:

            for page in document:
                text += page.get_text()

        return ResumeParser.clean_text(text)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted resume text.
        """

        if not text:
            return ""

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)