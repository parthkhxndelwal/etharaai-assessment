"""Employee endpoints"""

from typing import Optional
from fastapi import APIRouter, Depends, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeListResponse
from ..schemas.common import APIResponse
from ..services.auth_service import get_current_user
from ..services import employee_service


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "",
    response_model=APIResponse[EmployeeResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee"
)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new employee
    
    - **employee_id**: Unique employee identifier (e.g., EMP-001, must be uppercase alphanumeric with hyphens)
    - **full_name**: Employee full name
    - **email**: Employee email address (must be unique)
    - **department**: Department name
    
    Returns the created employee record.
    
    **Note**: Employee ID and email must be unique across the system.
    """
    employee = await employee_service.create_employee(employee_data)
    
    return APIResponse(
        success=True,
        data=EmployeeResponse(**employee),
        message="Employee created successfully"
    )


@router.get(
    "",
    response_model=EmployeeListResponse,
    summary="List Employees"
)
async def list_employees(
    department: Optional[str] = None,
    search: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all employees with optional filters
    
    - **department**: Filter by department name (optional)
    - **search**: Search in employee names (optional, uses text search)
    
    Returns list of all employees matching the filters.
    
    **Caching**: Results are cached for 60 seconds.
    """
    employees = await employee_service.get_all_employees(department=department, search=search)
    
    employee_responses = [EmployeeResponse(**emp) for emp in employees]
    
    return EmployeeListResponse(
        success=True,
        data=employee_responses,
        total=len(employee_responses)
    )


@router.get(
    "/{employee_id}",
    response_model=APIResponse[EmployeeResponse],
    summary="Get Employee"
)
async def get_employee(
    employee_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a single employee by ID
    
    - **employee_id**: Employee identifier
    
    Returns the employee record.
    
    **Caching**: Individual employee data is cached for 5 minutes.
    """
    employee = await employee_service.get_employee_by_id(employee_id)
    
    return APIResponse(
        success=True,
        data=EmployeeResponse(**employee),
        message="Employee retrieved successfully"
    )


@router.put(
    "/{employee_id}",
    response_model=APIResponse[EmployeeResponse],
    summary="Update Employee"
)
async def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing employee
    
    - **employee_id**: Employee identifier (in path)
    - **full_name**: New full name (optional)
    - **email**: New email address (optional, must be unique)
    - **department**: New department (optional)
    
    Returns the updated employee record.
    
    **Note**: Only provided fields will be updated. Employee ID cannot be changed.
    """
    employee = await employee_service.update_employee(employee_id, employee_data)
    
    return APIResponse(
        success=True,
        data=EmployeeResponse(**employee),
        message="Employee updated successfully"
    )


@router.delete(
    "/{employee_id}",
    response_model=APIResponse,
    summary="Delete Employee"
)
async def delete_employee(
    employee_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an employee
    
    - **employee_id**: Employee identifier
    
    Deletes the employee and all associated attendance records.
    
    **Warning**: This action cannot be undone.
    """
    await employee_service.delete_employee(employee_id)
    
    return APIResponse(
        success=True,
        data=None,
        message=f"Employee {employee_id} and associated records deleted successfully"
    )
