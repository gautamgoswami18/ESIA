from sqlalchemy.orm import Session

from app.repository.resume_repository import ResumeRepository
from app.repository.employee_repository import EmployeeRepository
from app.ai.resume_parser import ResumeParser
from app.ai.embedding_generator import EmbeddingGenerator
from app.ai.chroma_service import ChromaService
from app.ai.resume_chunker import ResumeChunker
from app.services.resume_matcher import ResumeMatcher
from app.schemas.resume import ResumeProcessResponse
from app.services.process_manager import ProcessManager
from app.services.ai_service import AIService
from app.utils.resume_storage import ResumeFileStorage
from app.ai.prompt import build_resume_extraction_prompt
from pathlib import Path
import uuid
import json
import re

from pydantic import ValidationError

from app.schemas.employee_profile_schema import (
    EmployeeProfileResponse
)

class ResumeService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = ResumeRepository(db)
        self.parser = ResumeParser()
        self.embedding_generator = EmbeddingGenerator()
        self.ai_service = AIService(db)

    def get_all(self):
        return self.repository.get_all()


    def get_by_employee_id(self, employee_id: int):
        return self.repository.get_by_employee_id(employee_id)


    def get_resume_metadata(self, employee_id: int):
        return self.repository.get_resume_metadata(employee_id)
    
    def parse_resume(self, employee_id: int):

        # Step 1: Fetch resume metadata
        resume = self.repository.get_resume_metadata(employee_id)
    
        if not resume:
            raise ValueError("Resume not found")
    
        # Step 2: Extract text from PDF
        resume_text = ResumeParser.extract_text(
            resume["file_path"]
        )
    
        # Step 3: Save extracted text
        self.repository.update_resume_text(
            employee_id,
            resume_text
        )
    
        return {
            "employee_id": employee_id,
            "file_name": resume["file_name"],
            "pages_parsed": len(resume_text.split("\n")),
            "status": "Completed"
        } 

    def generate_embedding(self, employee_id: int):

        # Fetch resume
        resume = self.repository.get_resume_metadata(employee_id)

        if not resume:
            raise ValueError(
                f"Resume not found for employee {employee_id}"
            )

        resume_text = resume.get("resume_text")

        if not resume_text:
            raise ValueError(
                "Resume has not been parsed yet."
            )

        chunk_count = self._replace_chroma_index(
            employee_id=employee_id,
            resume_text=resume_text,
        )

        return {
            "employee_id": employee_id,
            "chunks": chunk_count,
            "status": "Embedding generated successfully."
        }

    def process_all_resumes(self) -> dict:
        records = self.repository.get_all_employee_ids()
        succeeded = []
        failures = []

        for record in records:
            employee_id = int(record["employee_id"])
            try:
                resume = self.repository.get_resume_metadata(employee_id)
                if not resume:
                    raise ValueError("Resume metadata was not found.")
                if not (resume.get("resume_text") or "").strip():
                    self.parse_resume(employee_id)

                result = self.generate_embedding(employee_id)
                succeeded.append(
                    {
                        "employee_id": employee_id,
                        "chunks": result["chunks"],
                    }
                )
            except Exception as ex:
                self.repository.update_embedding_status(
                    employee_id,
                    False,
                )
                failures.append(
                    {
                        "employee_id": employee_id,
                        "error": str(ex),
                    }
                )

        return {
            "total": len(records),
            "succeeded": len(succeeded),
            "failed": len(failures),
            "indexed": succeeded,
            "failures": failures,
        }
    


    def process_resume(
        self,
        uploaded_file
    ) -> ResumeProcessResponse:

        if not uploaded_file.filename:
            raise ValueError("A PDF resume file is required.")

        if Path(uploaded_file.filename).suffix.lower() != ".pdf":
            raise ValueError("Only PDF resumes are supported.")

        file_content = uploaded_file.file.read(10 * 1024 * 1024 + 1)

        if not file_content:
            raise ValueError("The uploaded resume is empty.")

        if len(file_content) > 10 * 1024 * 1024:
            raise ValueError("The uploaded resume exceeds the 10 MB limit.")

        if not file_content.startswith(b"%PDF"):
            raise ValueError("The uploaded file is not a valid PDF.")

        # ==========================================================
        # Generate Process Id
        # ==========================================================

        process_id = str(uuid.uuid4())

        # ==========================================================
        # Create Temp Folder
        # ==========================================================

        temp_folder = Path("documents/temp")

        temp_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================================
        # Save Uploaded PDF
        # ==========================================================

        pdf_path = temp_folder / f"{process_id}.pdf"

        with open(pdf_path, "wb") as file:

            file.write(file_content)

        # ==========================================================
        # Extract Resume Text
        # ==========================================================

        resume_text = ResumeParser.extract_text(
            str(pdf_path)
        )

        # ==========================================================
        # Save Extracted Text
        # ==========================================================

        text_path = temp_folder / f"{process_id}.txt"

        with open(
            text_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                resume_text
            )

        # ==========================================================
        # Build Employee Profile using AI
        # ==========================================================

        employee_profile = self.build_resume(
            resume_text
        )

        # build_resume() should return
        # EmployeeProfileResponse

        # ==========================================================
        # Match Employee
        # ==========================================================

        matcher = ResumeMatcher(
            self.db
        )

        match_result = matcher.match_employee(
            employee_profile
        )

        
        ProcessManager.save(

            process_id,

            {
            
                "employee_profile": employee_profile,

                "match_result": match_result,

                "resume_text": resume_text,

                "pdf_path": str(pdf_path),

                "text_path": str(text_path)

            }

        )

        # ==========================================================
        # Return Response
        # ==========================================================

        return ResumeProcessResponse(

            process_id=process_id,

            matched=match_result["matched"],

            confidence=match_result["confidence"],

            action=match_result["action"],

            employee_profile=employee_profile
        )
    def build_resume(
        self,
        resume_text: str
    ) -> EmployeeProfileResponse:

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text is empty. Unable to build employee profile."
            )

        prompt = build_resume_extraction_prompt(
            resume_text
        )


        ai_response = self.ai_service.generate_response(
            prompt=prompt
        )

        response_data = self.ai_service.parse_ai_resume_response(
            ai_response=ai_response
        )

        for skill in response_data.get("skills", []):
            if isinstance(skill, dict) and not skill.get("name"):
                skill["name"] = (
                    skill.get("skill_name")
                    or skill.get("technology")
                    or ""
                )

        for project in response_data.get("projects", []):
            if not isinstance(project, dict):
                continue
            project["name"] = (
                project.get("name")
                or project.get("project_name")
                or project.get("title")
                or ""
            )
            project["client"] = (
                project.get("client")
                or project.get("client_name")
            )
            project["role"] = (
                project.get("role")
                or project.get("role_name")
            )

        for certification in response_data.get("certifications", []):
            if not isinstance(certification, dict):
                continue
            certification["name"] = (
                certification.get("name")
                or certification.get("certification_name")
                or certification.get("title")
                or ""
            )
            certification["issuing_organization"] = (
                certification.get("issuing_organization")
                or certification.get("vendor")
                or certification.get("provider")
            )

        for training in response_data.get("training", []):
            if not isinstance(training, dict):
                continue
            training["name"] = (
                training.get("name")
                or training.get("course")
                or training.get("course_name")
                or training.get("title")
                or ""
            )

        try:

            employee_profile = EmployeeProfileResponse.model_validate(
                response_data
            )

            employee_profile.skills = [
                item
                for item in employee_profile.skills
                if item.name and item.name.strip(" -")
            ]
            employee_profile.projects = [
                item
                for item in employee_profile.projects
                if item.name and item.name.strip(" -")
            ]
            employee_profile.certifications = [
                item
                for item in employee_profile.certifications
                if item.name and item.name.strip(" -")
            ]
            employee_profile.training = [
                item
                for item in employee_profile.training
                if item.name and item.name.strip(" -")
            ]

        except ValidationError as ex:

            raise ValueError(
                f"AI returned an invalid employee profile: {str(ex)}"
            ) from ex

        return employee_profile
    
    def _generate_ai_profile(
        self,
        resume_text: str
    ) -> dict:
        """
        Generate structured AI profile from resume using Groq.
        """

        profile = self.ai_service.llm_provider.extract_resume_profile(
            resume_text
        )

        if not profile:
            raise ValueError(
                "Failed to generate AI profile."
            )

        return profile
    
    def upload_resume(
        self,
        employee_id: int,
        uploaded_file
    ):

        if EmployeeRepository(self.db).get_by_id(employee_id) is None:
            raise ValueError(
                f"Employee {employee_id} was not found."
            )

        processed = self.process_resume(uploaded_file)
        process = ProcessManager.get(processed.process_id)

        process["match_result"] = {
            "matched": True,
            "confidence": 100,
            "employee_id": employee_id,
            "action": "UPDATE"
        }

        return self.save_resume(
            processed.process_id
        )


    def save_resume(
        self,
        process_id: str
    ):

        process = ProcessManager.get(
            process_id
        )

        employee_profile = process["employee_profile"]
        match_result = process["match_result"]

        # ==========================================
        # Save Employee
        # ==========================================

        if match_result["matched"]:
            employee_id = match_result["employee_id"]
            EmployeeRepository(self.db).update_employee(
                employee_id,
                employee_profile
            )
        else:
            employee_id = self.save_employee(employee_profile)

        # ==========================================
        # Save Resume Metadata
        # ==========================================

        self.save_resume_metadata(
            employee_id,
            process
        )

        # ==========================================
        # Index into ChromaDB
        # ==========================================

        self.index_employee_in_chromadb(
            employee_id,
            process
        )

        # ==========================================
        # Cleanup
        # ==========================================

        self.cleanup_temp_files(
            process
        )

        ProcessManager.remove(
            process_id
        )

        # ==========================================
        # Return
        # ==========================================

        return {

            "employee_id": employee_id,

            "message": "Employee saved successfully."

        }  
    

    def save_employee(
        self,
        employee
    ) -> int:
    
        employee_repository = EmployeeRepository(self.db)
    
        existing_employee = employee_repository.get_employee_by_email(
            employee.email
        )
    
        if existing_employee:
        
            employee_repository.update_employee(
                existing_employee["employee_id"],
                employee
            )
    
            return existing_employee["employee_id"]
    
        return employee_repository.create_employee(
            employee
        )
    
    def save_resume_metadata(
        self,
        employee_id: int,
        process: dict
    ):

        resume_repository = ResumeRepository(self.db)

        source_pdf_path = Path(process["pdf_path"])

        resume_text = process["resume_text"]

        existing_resume = resume_repository.get_resume_metadata(
            employee_id
        )

        employee_profile = process["employee_profile"]
        if isinstance(employee_profile, dict):
            first_name = employee_profile.get("first_name")
            last_name = employee_profile.get("last_name")
        else:
            first_name = getattr(
                employee_profile,
                "first_name",
                None,
            )
            last_name = getattr(
                employee_profile,
                "last_name",
                None,
            )

        employee_name = " ".join(
            part
            for part in (
                first_name,
                last_name,
            )
            if part
        )

        permanent_pdf_path = ResumeFileStorage().store(
            employee_id=employee_id,
            employee_name=employee_name,
            source_pdf_path=source_pdf_path,
            previous_file_path=(
                existing_resume.get("file_path")
                if existing_resume
                else None
            ),
        )

        file_name = permanent_pdf_path.name

        return resume_repository.save_resume_metadata(

            employee_id=employee_id,

            file_name=file_name,

            file_path=str(permanent_pdf_path),

            resume_text=resume_text

        )
    
    def index_employee_in_chromadb(
        self,
        employee_id: int,
        process: dict
    ):
        return self._replace_chroma_index(
            employee_id=employee_id,
            resume_text=process["resume_text"],
            employee_profile=process["employee_profile"],
        )

    def _replace_chroma_index(
        self,
        employee_id: int,
        resume_text: str,
        employee_profile=None,
    ) -> int:
        chunks = ResumeChunker.chunk(resume_text)
        if not chunks:
            raise ValueError(
                f"Resume for employee {employee_id} produced no valid chunks."
            )

        embeddings = [
            EmbeddingGenerator.generate_embedding(chunk)
            for chunk in chunks
        ]

        chroma = ChromaService()
        profile = (
            employee_profile
            if employee_profile is not None
            else chroma.get_profile(employee_id)
        )
        profile_json = None
        profile_embedding = None

        if profile is not None:
            if hasattr(profile, "model_dump"):
                profile = profile.model_dump(mode="json")
            profile_json = json.dumps(
                profile,
                ensure_ascii=False,
                default=str,
            )
            profile_embedding = EmbeddingGenerator.generate_embedding(
                profile_json
            )

        # Mark pending before replacing Chroma. It becomes indexed only after
        # all required resume/profile upserts complete successfully.
        self.repository.update_embedding_status(employee_id, False)

        chroma.delete_resume(employee_id)
        chroma.add_resume(
            employee_id=employee_id,
            chunks=chunks,
            embeddings=embeddings,
        )

        if profile_json is not None and profile_embedding is not None:
            chroma.add_profile(
                employee_id=employee_id,
                profile_json=profile_json,
                embedding=profile_embedding,
            )

        self.repository.update_embedding_status(employee_id, True)
        return len(chunks)


    def cleanup_temp_files(
        self,
        process: dict
    ):

        pdf_path = process["pdf_path"]

        text_path = process["text_path"]

        if Path(pdf_path).exists():

            Path(pdf_path).unlink()

        if Path(text_path).exists():

            Path(text_path).unlink()       
