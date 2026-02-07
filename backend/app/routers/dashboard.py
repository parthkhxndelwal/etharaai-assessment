"""
Dashboard Router
Analytics and summary endpoints
"""

from typing import List
from fastapi import APIRouter, Depends

from ..schemas.dashboard import DashboardSummary, DashboardResponse
from ..schemas.attendance import EmployeeAttendanceSummary
from ..schemas.common import APIResponse
from ..services.auth_service import get_current_user
from ..services import dashboard_service


router = APIRouter()


@router.get(
    "/summary",
    response_model=DashboardResponse,
    summary="Get Dashboard Summary"
)
async def get_summary(current_user: dict = Depends(get_current_user)):
    """
    Get dashboard summary statistics
    
    Returns:
    - **total_employees**: Total number of employees in the system
    - **present_today**: Number of employees marked present today
    - **absent_today**: Number of employees marked absent today
    - **department_counts**: Employee count grouped by department
    
    **Caching**: Results are cached for 30 seconds to optimize performance.
    
    Use this endpoint to populate the main dashboard view with key metrics.
    """
    summary = await dashboard_service.get_dashboard_summary()
    
    return DashboardResponse(
        success=True,
        data=summary
    )


@router.get(
    "/attendance-summary",
    response_model=APIResponse[List[EmployeeAttendanceSummary]],
    summary="Get Attendance Summary by Employee"
)
async def get_attendance_summary(current_user: dict = Depends(get_current_user)):
    """
    Get per-employee attendance summary
    
    Returns a list of all employees with their attendance metrics:
    - **employee_id**: Employee identifier
    - **full_name**: Employee name
    - **present_days**: Total days marked present
    - **absent_days**: Total days marked absent
    - **total_days**: Total attendance records
    - **attendance_percentage**: Percentage of present days
    
    Results are sorted by attendance percentage (highest first).
    
    **Caching**: Results are cached for 60 seconds.
    
    Use this endpoint to display attendance performance across all employees.
    """
    summaries = await dashboard_service.get_attendance_summary()
    
    return APIResponse(
        success=True,
        data=summaries,
        message=f"Retrieved attendance summary for {len(summaries)} employees"
    )
