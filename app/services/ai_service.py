from app.ai.rag_chain import RAGChain
from app.repository.resume_repository import ResumeRepository
from app.core.exceptions import ResourceNotFoundException
from sqlalchemy.orm import Session
from app.ai.rag_factory import RAGFactory
from app.llm.provider_factory import ProviderFactory
import json
import re

class AIService:

    def __init__(self, db):
        self.db = db
        self.repository = ResumeRepository(db)
        self.rag = None
        self.llm_provider = ProviderFactory.get_provider()

    def _get_rag(self):

        if self.rag is None:
            self.rag = RAGFactory.get_rag(db=self.db)

        return self.rag
    
    def search_resume(
        self,
        question: str
    ):

        return self._get_rag().ask(question)
    
    def resume_summary(
        self,
        employee_id: int
    ):

        resume = self.repository.get_resume_metadata(employee_id)
        if resume is None:
            raise ResourceNotFoundException("resume")

        if not resume:
            raise ValueError("Resume not found.")

        if not resume.get("resume_text"):
            raise ValueError("Resume has not been parsed yet.")

        return self._get_rag().summarize_resume(
            resume["resume_text"]
        )

    def compare_candidates(
        self,
        employee1: int,
        employee2: int
    ):

        resume1 = self.repository.get_resume_metadata(employee1)

        resume2 = self.repository.get_resume_metadata(employee2)
        if resume1 is None or resume2 is None:
            raise ResourceNotFoundException(
                f"{'resume1' if resume1 is None else ''}"
                f"{', ' if resume1 is None and resume2 is None else ''}"
                f"{'resume2' if resume2 is None else ''} not found"
            )    
        if not resume1:
            raise ValueError(
                f"Resume not found for Employee {employee1}"
            )

        if not resume2:
            raise ValueError(
                f"Resume not found for Employee {employee2}"
            )

        if not resume1.get("resume_text"):
            raise ValueError(
                f"Resume not parsed for Employee {employee1}"
            )

        if not resume2.get("resume_text"):
            raise ValueError(
                f"Resume not parsed for Employee {employee2}"
            )

        return self._get_rag().compare_candidates(
            resume1["resume_text"],
            resume2["resume_text"]
        )

    def generate_response(
        self,
        prompt: str
    ) -> str:

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        return self.llm_provider.generate(
            prompt,
            json_mode=True
        )


    def parse_ai_resume_response(
        self,
        ai_response: str
    ) -> dict:

        if not ai_response:
            raise ValueError("AI returned an empty response.")

        response = ai_response.strip()

        response = re.sub(
            r"^```json",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"^```",
            "",
            response
        )

        response = re.sub(
            r"```$",
            "",
            response
        )

        response = response.strip()

        try:
            return json.loads(response)

        except json.JSONDecodeError as ex:

            raise ValueError(
                f"Invalid JSON returned by AI.\n\n{response}"
            ) from ex
