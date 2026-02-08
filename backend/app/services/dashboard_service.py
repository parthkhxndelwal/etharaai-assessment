"""Dashboard analytics service"""

from datetime import date, datetime
from typing import List, Dict

from ..database import get_employees_collection, get_attendance_collection
from ..cache import cache_get, cache_set
from ..schemas.dashboard import DashboardSummary
from ..schemas.attendance import EmployeeAttendanceSummary


async def get_dashboard_summary() -> DashboardSummary:
    """
    Get dashboard summary statistics
    
    Returns:
        Dashboard summary with counts and metrics
    """
    # Try cache first
    cache_key = "dashboard:summary"
    cached_data = await cache_get(cache_key)
    if cached_data:
        return DashboardSummary(**cached_data)
    
    employees_collection = get_employees_collection()
    attendance_collection = get_attendance_collection()
    
    # Get total employees
    total_employees = await employees_collection.count_documents({})
    
    # Get today's attendance (convert date to datetime for BSON compatibility)
    today = datetime.combine(date.today(), datetime.min.time())
    present_today = await attendance_collection.count_documents({
        "date": today,
        "status": "Present"
    })
    
    absent_today = await attendance_collection.count_documents({
        "date": today,
        "status": "Absent"
    })
    
    # Get department counts
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        }
    ]
    
    dept_cursor = employees_collection.aggregate(pipeline)
    dept_results = await dept_cursor.to_list(length=100)
    
    department_counts = {item["_id"]: item["count"] for item in dept_results}
    
    # Create summary
    summary = DashboardSummary(
        total_employees=total_employees,
        present_today=present_today,
        absent_today=absent_today,
        department_counts=department_counts
    )
    
    # Cache result
    await cache_set(cache_key, summary.model_dump(), ttl=30)
    
    return summary


async def get_attendance_summary() -> List[EmployeeAttendanceSummary]:
    """
    Get per-employee attendance summary
    
    Returns:
        List of employee attendance summaries with present/absent days
    """
    # Try cache first
    cache_key = "dashboard:attendance_summary"
    cached_data = await cache_get(cache_key)
    if cached_data:
        return [EmployeeAttendanceSummary(**item) for item in cached_data]
    
    employees_collection = get_employees_collection()
    attendance_collection = get_attendance_collection()
    
    # Get all employees
    employees_cursor = employees_collection.find({})
    employees = await employees_cursor.to_list(length=1000)
    
    summaries = []
    
    for employee in employees:
        employee_id = employee["employee_id"]
        
        # Count present days
        present_days = await attendance_collection.count_documents({
            "employee_id": employee_id,
            "status": "Present"
        })
        
        # Count absent days
        absent_days = await attendance_collection.count_documents({
            "employee_id": employee_id,
            "status": "Absent"
        })
        
        total_days = present_days + absent_days
        
        # Calculate attendance percentage
        if total_days > 0:
            attendance_percentage = round((present_days / total_days) * 100, 2)
        else:
            attendance_percentage = 0.0
        
        summary = EmployeeAttendanceSummary(
            employee_id=employee_id,
            full_name=employee["full_name"],
            present_days=present_days,
            absent_days=absent_days,
            total_days=total_days,
            attendance_percentage=attendance_percentage
        )
        
        summaries.append(summary)
    
    # Sort by attendance percentage (descending)
    summaries.sort(key=lambda x: x.attendance_percentage, reverse=True)
    
    # Cache result
    cache_data = [s.model_dump() for s in summaries]
    await cache_set(cache_key, cache_data, ttl=60)
    
    return summaries
