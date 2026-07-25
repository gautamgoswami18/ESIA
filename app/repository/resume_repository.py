import json

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.repository.base_repository import BaseRepository



class ResumeRepository(BaseRepository):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):

        sql = text("""

            SELECT

                rm.resume_id,
                rm.employee_id,

                e.first_name,
                e.last_name,
                e.designation,

                rm.file_name,
                rm.file_path,
                rm.embedding_status

            FROM esia.resume_metadata rm

            INNER JOIN esia.employees e

                ON rm.employee_id = e.employee_id

            ORDER BY rm.employee_id

        """)

        return self.fetch_all(sql)

    def get_by_employee_id(self, employee_id: int):

        sql = text("""

            SELECT

                rm.resume_id,
                rm.employee_id,

                e.first_name,
                e.last_name,
                e.designation,
                e.email,
                e.location, 
                e.experience_years,     
                rm.file_name,
                rm.file_path,
                
                rm.embedding_status

            FROM esia.resume_metadata rm

            INNER JOIN esia.employees e

                ON rm.employee_id = e.employee_id

            WHERE rm.employee_id = :employee_id

        """)

        return self.fetch_one(
             sql,
            {"employee_id": employee_id}
        )
    
    def get_resume_metadata(self, employee_id: int):
        
        sql = """
            SELECT
                resume_id,
                embedding_status,
                file_name,
                file_path,
                resume_text
            FROM esia.resume_metadata
            WHERE employee_id = :employee_id
        """
    
        return self.fetch_one(
            sql,
            {"employee_id": employee_id}
        )
    
    def update_resume(
        self,
        employee_id: int,
        file_name: str,
        file_path: str,
        resume_text: str
    ):
        sql = """
            UPDATE esia.resume_metadata
            SET
                file_name = :file_name,
                file_path = :file_path,
                resume_text = :resume_text,
                embedding_status = FALSE
            WHERE employee_id = :employee_id
        """

        self.execute(
            text(sql),
            {
                "employee_id": employee_id,
                "file_name": file_name,
                "file_path": file_path,
                "resume_text": resume_text
            }
        )

    def update_embedding_status(
        self,
        employee_id: int,
        status: bool,
    ):
        sql = """
            UPDATE esia.resume_metadata
            SET embedding_status = :status
            WHERE employee_id = :employee_id
        """

        self.execute(
            text(sql),
            {
                "employee_id": employee_id,
                "status": status
            }
        )

    def get_all_employee_ids(self):

        sql = """
            SELECT
                employee_id
            FROM esia.resume_metadata
            ORDER BY employee_id
        """

        return self.fetch_all(sql)  

    def create_resume(
        self,
        employee_id: int,
        file_name: str,
        file_path: str
    ):
        """
        Create a new resume metadata record.
        If the employee already has a resume,
        overwrite the existing metadata.
        """

        sql = text("""
            INSERT INTO esia.resume_metadata
            (
                employee_id,
                file_name,
                file_path,
                embedding_status,
                resume_text
            )
            VALUES
            (
                :employee_id,
                :file_name,
                :file_path,
                FALSE,
                NULL
            )

            ON CONFLICT (employee_id)

            DO UPDATE SET

                file_name = EXCLUDED.file_name,
                file_path = EXCLUDED.file_path,
                embedding_status = FALSE,
                resume_text = NULL
        """)

        self.execute(
            sql,
            {
                "employee_id": employee_id,
                "file_name": file_name,
                "file_path": file_path
            }
        )  

    def save_ai_profile(
        self,
        employee_id: int,
        summary: str,
        profile_json: str
    ):
        """
        Insert or update AI generated employee profile.
        """

        sql = text("""
            INSERT INTO esia.employee_ai_profile
            (
                employee_id,
                summary,
                profile_json,
                generated_at
            )
            VALUES
            (
                :employee_id,
                :summary,
                CAST(:profile_json AS jsonb),
                CURRENT_TIMESTAMP
            )

            ON CONFLICT (employee_id)

            DO UPDATE SET

                summary = EXCLUDED.summary,
                profile_json = EXCLUDED.profile_json,
                generated_at = CURRENT_TIMESTAMP
        """)

        self.execute(
            sql,
            {
                "employee_id": employee_id,
                "summary": summary,
                "profile_json": profile_json
            }
        ) 

        
    def save_ai_entities(
        self,
        employee_id: int,
        entities: list
    ):
        """
        Save all AI extracted entities.
        Existing entities are deleted before inserting new ones.
        """

        # Delete existing entities
        self.delete_ai_entities(employee_id)

        sql = text("""
            INSERT INTO esia.employee_ai_entities
            (
                employee_id,
                entity_type,
                entity_name,
                entity_category,
                confidence_score,
                entity_metadata,
                created_at
            )
            VALUES
            (
                :employee_id,
                :entity_type,
                :entity_name,
                :entity_category,
                :confidence_score,
                CAST(:entity_metadata AS jsonb),
                CURRENT_TIMESTAMP
            )
        """)

        for entity in entities:

            self.execute(
                sql,
                {
                    "employee_id": employee_id,
                    "entity_type": entity["entity_type"],
                    "entity_name": entity["entity_name"],
                    "entity_category": entity.get("entity_category"),
                    "confidence_score": entity.get("confidence_score", 1.0),
                    "entity_metadata": json.dumps(
                        entity.get("entity_metadata", {})
                    )
                }
            )  



    def get_ai_entities(
        self,
        employee_id: int
    ):
        """
        Fetch all AI extracted entities for an employee.
        """

        sql = text("""
            SELECT
                entity_id,
                employee_id,
                entity_type,
                entity_name,
                entity_category,
                confidence_score,
                entity_metadata,
                created_at
            FROM esia.employee_ai_entities
            WHERE employee_id = :employee_id
            ORDER BY entity_type, entity_name
        """)

        return self.fetch_all(
            sql,
            {
                "employee_id": employee_id
            }
        ) 

    def delete_ai_entities(
        self,
        employee_id: int
    ):
        """
        Delete all AI extracted entities for an employee.
        """
    
        sql = text("""
            DELETE FROM esia.employee_ai_entities
            WHERE employee_id = :employee_id
        """)
    
        self.execute(
            sql,
            {
                "employee_id": employee_id
            }
        ) 



    def save_resume_metadata(
        self,
        employee_id: int,
        file_name: str,
        file_path: str,
        resume_text: str
    ):

        sql = """
            INSERT INTO esia.resume_metadata
            (
                employee_id,
                file_name,
                file_path,
                embedding_status,
                resume_text
            )
            VALUES
            (
                :employee_id,
                :file_name,
                :file_path,
                FALSE,
                :resume_text
            )

            ON CONFLICT (employee_id)

            DO UPDATE SET

                file_name = EXCLUDED.file_name,
                file_path = EXCLUDED.file_path,
                embedding_status = FALSE,
                resume_text = EXCLUDED.resume_text

            RETURNING resume_id
        """

        return self.fetch_one(
            sql,
            {
                "employee_id": employee_id,
                "file_name": file_name,
                "file_path": file_path,
                "resume_text": resume_text
            }
        )            
    
    def get_ai_profile(
        self,
        employee_id: int
    ):
        """
        Fetch AI generated employee profile.
        """

        sql = text("""
            SELECT
                employee_id,
                summary,
                profile_json,
                generated_at
            FROM esia.employee_ai_profile
            WHERE employee_id = :employee_id
        """)

        return self.fetch_one(
            sql,
            {
                "employee_id": employee_id
            }
        )   


    def delete_ai_profile(
        self,
        employee_id: int
    ):
        """
        Delete AI profile for an employee.
        Used before regenerating profile if required.
        """

        sql = text("""
            DELETE FROM esia.employee_ai_profile
            WHERE employee_id = :employee_id
        """)

        self.execute(
            sql,
            {
                "employee_id": employee_id
            }
        )  

