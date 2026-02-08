"""Attendance endpoints"""

from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, status, Query

from ..schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceListResponse
)
from ..schemas.common import APIResponse
from ..services.auth_service import get_current_user
from ..services import attendance_service


router = APIRouter()


@router.post(
    "",
    response_model=APIResponse[AttendanceResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Mark Attendance"
)
async def mark_attendance(
    attendance_data: AttendanceCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark attendance for an employee
    
    - **employee_id**: Employee identifier
    - **date**: Attendance date (YYYY-MM-DD format)
    - **status**: Attendance status (Present or Absent)
    
    Returns the created attendance record.
    
    **Note**: Only one attendance record can be created per employee per day.
    """
    record = await attendance_service.mark_attendance(attendance_data)
    
    return APIResponse(
        success=True,
        data=AttendanceResponse(**record),
        message="Attendance marked successfully"
    )


@router.get(
    "",
    response_model=AttendanceListResponse,
    summary="List Attendance Records"
)
async def list_attendance(
    employee_id: Optional[str] = Query(None, description="Filter by employee ID"),
    date: Optional[date] = Query(None, description="Filter by specific date"),
    start_date: Optional[date] = Query(None, description="Filter from this date"),
    end_date: Optional[date] = Query(None, description="Filter until this date"),
    status: Optional[str] = Query(None, description="Filter by status (Present/Absent)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all attendance records with optional filters
    
    - **employee_id**: Filter by employee ID (optional)
    - **date**: Filter by specific date (optional)
    - **start_date**: Filter from this date (optional)
    - **end_date**: Filter until this date (optional)
    - **status**: Filter by status - Present or Absent (optional)
    
    Returns list of attendance records matching the filters.
    
    **Caching**: Results are cached for 60 seconds.
    """
    records = await attendance_service.get_all_attendance(
        employee_id=employee_id,
        date_filter=date,
        start_date=start_date,
        end_date=end_date,
        status_filter=status
    )
    
    attendance_responses = [AttendanceResponse(**record) for record in records]
    
    return AttendanceListResponse(
        success=True,
        data=attendance_responses,
        total=len(attendance_responses)
    )


@router.get(
    "/{employee_id}",
    response_model=AttendanceListResponse,
    summary="Get Employee Attendance"
)
async def get_employee_attendance(
    employee_id: str,
    start_date: Optional[date] = Query(None, description="Filter from this date"),
    end_date: Optional[date] = Query(None, description="Filter until this date"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get attendance records for a specific employee
    
    - **employee_id**: Employee identifier (in path)
    - **start_date**: Filter from this date (optional)
    - **end_date**: Filter until this date (optional)
    
    Returns list of attendance records for the employee.
    
    **Caching**: Results are cached for 60 seconds.
    """
    records = await attendance_service.get_employee_attendance(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )
    
    attendance_responses = [AttendanceResponse(**record) for record in records]
    
    return AttendanceListResponse(
        success=True,
        data=attendance_responses,
        total=len(attendance_responses)
    )


@router.put(
    "/{record_id}",
    response_model=APIResponse[AttendanceResponse],
    summary="Update Attendance"
)
async def update_attendance(
    record_id: str,
    attendance_data: AttendanceUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an attendance record
    
    - **record_id**: Attendance record ID (in path)
    - **status**: New attendance status (Present or Absent)
    
    Returns the updated attendance record.
    """
    record = await attendance_service.update_attendance(record_id, attendance_data)
    
    return APIResponse(
        success=True,
        data=AttendanceResponse(**record),
        message="Attendance updated successfully"
    )


@router.delete(
    "/{record_id}",
    response_model=APIResponse,
    summary="Delete Attendance"
)
async def delete_attendance(
    record_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an attendance record
    
    - **record_id**: Attendance record ID
    
    Deletes the attendance record.
    
    **Warning**: This action cannot be undone.
    """
    await attendance_service.delete_attendance(record_id)
    
    return APIResponse(
        success=True,
        data=None,
        message="Attendance record deleted successfully"
    )
