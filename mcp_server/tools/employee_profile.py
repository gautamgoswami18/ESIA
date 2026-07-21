import mcp

from app.database import SessionLocal
from app.services.employee_profile_service import EmployeeProfileService


def employee_profile(employee_id: int):
    print(">>>>>>>>>> employee_profile called <<<<<<<<<<")
    """
    Return complete employee profile.
    """

    db = SessionLocal()

    try:
        service = EmployeeProfileService(db)

        return service.get_employee_profile(employee_id)

    finally:
        db.close()