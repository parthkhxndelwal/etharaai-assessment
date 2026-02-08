"""Attendance business logic"""

from datetime import datetime, date
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, status

from ..database import get_attendance_collection, get_employees_collection
from ..cache import cache_get, cache_set, cache_delete, cache_delete_pattern
from ..schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from ..services.employee_service import generate_cache_key


async def mark_attendance(attendance_data: AttendanceCreate) -> dict:
    """
    Mark attendance for an employee
    
    Args:
        attendance_data: Attendance creation data
    
    Returns:
        Created attendance document
    
    Raises:
        HTTPException: If employee not found or attendance already marked
    """
    employees_collection = get_employees_collection()
    attendance_collection = get_attendance_collection()
    
    # Check if employee exists
    employee = await employees_collection.find_one({"employee_id": attendance_data.employee_id})
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{attendance_data.employee_id}' not found"
        )
    
    # Check if attendance already marked for this date
    existing = await attendance_collection.find_one({
        "employee_id": attendance_data.employee_id,
        "date": attendance_data.date
    })
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Attendance already marked for employee '{attendance_data.employee_id}' on {attendance_data.date}"
        )
    
    # Create attendance document
    attendance_dict = attendance_data.model_dump()
    attendance_dict["created_at"] = datetime.utcnow()
    
    # Insert into database
    result = await attendance_collection.insert_one(attendance_dict)
    
    # Get created attendance
    created_attendance = await attendance_collection.find_one({"_id": result.inserted_id})
    created_attendance["_id"] = str(created_attendance["_id"])
    
    # Invalidate caches
    await cache_delete_pattern("attendance:*")
    await cache_delete_pattern("dashboard:*")
    
    return created_attendance


async def get_all_attendance(
    employee_id: Optional[str] = None,
    date_filter: Optional[date] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status_filter: Optional[str] = None
) -> List[dict]:
    """
    Get attendance records with optional filters
    
    Args:
        employee_id: Filter by employee ID
        date_filter: Filter by specific date
        start_date: Filter from this date
        end_date: Filter until this date
        status_filter: Filter by status (Present/Absent)
    
    Returns:
        List of attendance documents
    """
    # Generate cache key
    cache_key = generate_cache_key(
        "attendance:list",
        employee_id=employee_id,
        date=str(date_filter) if date_filter else None,
        start_date=str(start_date) if start_date else None,
        end_date=str(end_date) if end_date else None,
        status=status_filter
    )
    
    # Try cache first
    cached_data = await cache_get(cache_key)
    if cached_data:
        return cached_data
    
    attendance_collection = get_attendance_collection()
    
    # Build query - convert date objects to datetime for BSON compatibility
    query = {}
    if employee_id:
        query["employee_id"] = employee_id
    if date_filter:
        query["date"] = datetime.combine(date_filter, datetime.min.time()) if isinstance(date_filter, date) and not isinstance(date_filter, datetime) else date_filter
    elif start_date or end_date:
        date_query = {}
        if start_date:
            date_query["$gte"] = datetime.combine(start_date, datetime.min.time()) if isinstance(start_date, date) and not isinstance(start_date, datetime) else start_date
        if end_date:
            date_query["$lte"] = datetime.combine(end_date, datetime.min.time()) if isinstance(end_date, date) and not isinstance(end_date, datetime) else end_date
        if date_query:
            query["date"] = date_query
    if status_filter:
        query["status"] = status_filter
    
    # Fetch attendance records
    cursor = attendance_collection.find(query).sort("date", -1)
    records = await cursor.to_list(length=1000)
    
    # Convert ObjectId to string and enrich with employee names
    employees_collection = get_employees_collection()
    for record in records:
        record["_id"] = str(record["_id"])
        # Look up employee name
        employee = await employees_collection.find_one({"employee_id": record["employee_id"]}, {"full_name": 1})
        if employee:
            record["employee_name"] = employee.get("full_name")
    
    # Cache results
    await cache_set(cache_key, records, ttl=60)
    
    return records


async def get_employee_attendance(
    employee_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[dict]:
    """
    Get attendance records for a specific employee
    
    Args:
        employee_id: Employee identifier
        start_date: Filter from this date
        end_date: Filter until this date
    
    Returns:
        List of attendance documents
    
    Raises:
        HTTPException: If employee not found
    """
    employees_collection = get_employees_collection()
    
    # Check if employee exists
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    return await get_all_attendance(
        employee_id=employee_id,
        start_date=start_date,
        end_date=end_date
    )


async def update_attendance(record_id: str, attendance_data: AttendanceUpdate) -> dict:
    """
    Update an attendance record
    
    Args:
        record_id: Attendance record ID
        attendance_data: Attendance update data
    
    Returns:
        Updated attendance document
    
    Raises:
        HTTPException: If record not found
    """
    attendance_collection = get_attendance_collection()
    
    try:
        object_id = ObjectId(record_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid record ID format"
        )
    
    # Check if record exists
    existing = await attendance_collection.find_one({"_id": object_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record not found"
        )
    
    # Update record
    await attendance_collection.update_one(
        {"_id": object_id},
        {"$set": {"status": attendance_data.status}}
    )
    
    # Get updated record
    updated_record = await attendance_collection.find_one({"_id": object_id})
    updated_record["_id"] = str(updated_record["_id"])
    
    # Invalidate caches
    await cache_delete_pattern("attendance:*")
    await cache_delete_pattern("dashboard:*")
    
    return updated_record


async def delete_attendance(record_id: str) -> bool:
    """
    Delete an attendance record
    
    Args:
        record_id: Attendance record ID
    
    Returns:
        True if deleted
    
    Raises:
        HTTPException: If record not found
    """
    attendance_collection = get_attendance_collection()
    
    try:
        object_id = ObjectId(record_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid record ID format"
        )
    
    # Check if record exists
    existing = await attendance_collection.find_one({"_id": object_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record not found"
        )
    
    # Delete record
    await attendance_collection.delete_one({"_id": object_id})
    
    # Invalidate caches
    await cache_delete_pattern("attendance:*")
    await cache_delete_pattern("dashboard:*")
    
    return True
