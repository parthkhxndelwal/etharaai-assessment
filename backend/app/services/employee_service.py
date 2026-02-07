"""
Employee Service
Business logic for employee management with caching
"""

from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, status

from ..database import get_employees_collection, get_attendance_collection
from ..cache import cache_get, cache_set, cache_delete, cache_delete_pattern
from ..schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
import hashlib
import json


def generate_cache_key(prefix: str, **kwargs) -> str:
    """Generate a cache key from prefix and parameters"""
    if not kwargs:
        return prefix
    
    # Create a stable hash from parameters
    params_str = json.dumps(kwargs, sort_keys=True)
    params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
    return f"{prefix}:{params_hash}"


async def create_employee(employee_data: EmployeeCreate) -> dict:
    """
    Create a new employee
    
    Args:
        employee_data: Employee creation data
    
    Returns:
        Created employee document
    
    Raises:
        HTTPException: If employee_id or email already exists
    """
    employees_collection = get_employees_collection()
    
    # Check if employee_id already exists
    existing_id = await employees_collection.find_one({"employee_id": employee_data.employee_id})
    if existing_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with ID '{employee_data.employee_id}' already exists"
        )
    
    # Check if email already exists
    existing_email = await employees_collection.find_one({"email": employee_data.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Employee with email '{employee_data.email}' already exists"
        )
    
    # Create employee document
    employee_dict = employee_data.model_dump()
    employee_dict["created_at"] = datetime.utcnow()
    employee_dict["updated_at"] = datetime.utcnow()
    
    # Insert into database
    result = await employees_collection.insert_one(employee_dict)
    
    # Get created employee
    created_employee = await employees_collection.find_one({"_id": result.inserted_id})
    
    # Invalidate list cache
    await cache_delete_pattern("employees:list:*")
    
    # Cache individual employee
    created_employee["_id"] = str(created_employee["_id"])
    await cache_set(f"employee:{employee_data.employee_id}", created_employee, ttl=300)
    
    return created_employee


async def get_all_employees(department: Optional[str] = None, search: Optional[str] = None) -> List[dict]:
    """
    Get all employees with optional filters
    
    Args:
        department: Filter by department
        search: Search in employee name
    
    Returns:
        List of employee documents
    """
    # Generate cache key
    cache_key = generate_cache_key("employees:list", department=department, search=search)
    
    # Try cache first
    cached_data = await cache_get(cache_key)
    if cached_data:
        return cached_data
    
    employees_collection = get_employees_collection()
    
    # Build query
    query = {}
    if department:
        query["department"] = department
    if search:
        query["$text"] = {"$search": search}
    
    # Fetch employees
    cursor = employees_collection.find(query).sort("created_at", -1)
    employees = await cursor.to_list(length=1000)
    
    # Convert ObjectId to string
    for emp in employees:
        emp["_id"] = str(emp["_id"])
    
    # Cache results
    await cache_set(cache_key, employees, ttl=60)
    
    return employees


async def get_employee_by_id(employee_id: str) -> dict:
    """
    Get a single employee by ID
    
    Args:
        employee_id: Employee identifier
    
    Returns:
        Employee document
    
    Raises:
        HTTPException: If employee not found
    """
    # Try cache first
    cache_key = f"employee:{employee_id}"
    cached_data = await cache_get(cache_key)
    if cached_data:
        return cached_data
    
    employees_collection = get_employees_collection()
    employee = await employees_collection.find_one({"employee_id": employee_id})
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    # Convert ObjectId to string
    employee["_id"] = str(employee["_id"])
    
    # Cache result
    await cache_set(cache_key, employee, ttl=300)
    
    return employee


async def update_employee(employee_id: str, employee_data: EmployeeUpdate) -> dict:
    """
    Update an employee
    
    Args:
        employee_id: Employee identifier
        employee_data: Employee update data
    
    Returns:
        Updated employee document
    
    Raises:
        HTTPException: If employee not found or email conflict
    """
    employees_collection = get_employees_collection()
    
    # Check if employee exists
    existing_employee = await employees_collection.find_one({"employee_id": employee_id})
    if not existing_employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    # If email is being updated, check for conflicts
    if employee_data.email and employee_data.email != existing_employee["email"]:
        email_exists = await employees_collection.find_one({
            "email": employee_data.email,
            "employee_id": {"$ne": employee_id}
        })
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Employee with email '{employee_data.email}' already exists"
            )
    
    # Build update data
    update_data = {k: v for k, v in employee_data.model_dump(exclude_unset=True).items()}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        
        # Update in database
        await employees_collection.update_one(
            {"employee_id": employee_id},
            {"$set": update_data}
        )
    
    # Get updated employee
    updated_employee = await employees_collection.find_one({"employee_id": employee_id})
    updated_employee["_id"] = str(updated_employee["_id"])
    
    # Invalidate caches
    await cache_delete(f"employee:{employee_id}")
    await cache_delete_pattern("employees:list:*")
    
    return updated_employee


async def delete_employee(employee_id: str) -> bool:
    """
    Delete an employee and their attendance records
    
    Args:
        employee_id: Employee identifier
    
    Returns:
        True if deleted
    
    Raises:
        HTTPException: If employee not found
    """
    employees_collection = get_employees_collection()
    attendance_collection = get_attendance_collection()
    
    # Check if employee exists
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID '{employee_id}' not found"
        )
    
    # Delete employee
    await employees_collection.delete_one({"employee_id": employee_id})
    
    # Delete associated attendance records
    await attendance_collection.delete_many({"employee_id": employee_id})
    
    # Invalidate caches
    await cache_delete(f"employee:{employee_id}")
    await cache_delete_pattern("employees:list:*")
    await cache_delete_pattern("attendance:*")
    await cache_delete_pattern("dashboard:*")
    
    return True
