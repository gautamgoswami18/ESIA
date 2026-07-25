from typing import Optional

from sqlalchemy.orm import Session

from app.repository.employee_repository import EmployeeRepository


class ResumeMatcher:

    def __init__(self, db: Session):

        self.db = db
        self.employee_repository = EmployeeRepository(db)

    def match_employee(
        self,
        profile
    ) -> dict:
        """
        Match employee using extracted AI profile.

        Returns:
            {
                "matched": True/False,
                "confidence": 98,
                "employee_id": 1001,
                "action": "UPDATE" | "CREATE"
            }
        """

        # ---------------------------------------------------
        # 1. Match by Email (Highest Priority)
        # ---------------------------------------------------

        if profile.email:

            employee = self.employee_repository.get_employee_by_email(
                profile.email
            )

            if employee:

                return {
                    "matched": True,
                    "confidence": 100,
                    "employee_id": employee["employee_id"],
                    "action": "UPDATE"
                }

        # ---------------------------------------------------
        # 2. Match by Name
        # ---------------------------------------------------

        employee = self.employee_repository.get_employee_by_name(
            first_name=profile.first_name,
            last_name=profile.last_name
        )

        if employee:

            return {
                "matched": True,
                "confidence": 95,
                "employee_id": employee["employee_id"],
                "action": "UPDATE"
            }

        # ---------------------------------------------------
        # 3. New Employee
        # ---------------------------------------------------

        return {
            "matched": False,
            "confidence": 0,
            "employee_id": None,
            "action": "CREATE"
        }
