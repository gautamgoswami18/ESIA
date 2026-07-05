from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.employee_service import EmployeeService
from app.schemas.response import APIResponse
from app.schemas.employee_filter import EmployeeFilter
from app.dependencies.employee_filters import get_employee_filters

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.get("/")
def get_employees(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    filters: EmployeeFilter = Depends(get_employee_filters),
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)

    result = service.get_all(page, size, filters)
    
    return APIResponse(
        success=True,
        message="Employees fetched successfully",
        data=result["items"],
        pagination=result["pagination"]
    )

@router.get("/{employee_id}")
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    service = EmployeeService(db)

    employee = service.get_by_id(employee_id)

    return APIResponse(
        success=True,
        message="Employee fetched successfully",
        data=employee
    )