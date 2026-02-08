"""Employee schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator


class EmployeeCreate(BaseModel):
    """Schema for creating a new employee"""
    
    employee_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique employee identifier (e.g., EMP-001)",
        pattern=r"^[A-Z0-9\-]+$"
    )
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Employee full name"
    )
    email: EmailStr = Field(..., description="Employee email address")
    department: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Department name"
    )
    position: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Job position/title"
    )
    
    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "employee_id": "EMP-001",
                "full_name": "Rajesh Kumar",
                "email": "rajesh.kumar@company.com",
                "department": "Engineering",
                "position": "Senior Software Engineer"
            }
        }
    )
    
    @field_validator('full_name', 'department', 'position')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip leading/trailing whitespace"""
        return v.strip()
    
    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        """Convert email to lowercase"""
        return v.lower()
    
    @field_validator('employee_id')
    @classmethod
    def uppercase_employee_id(cls, v: str) -> str:
        """Convert employee_id to uppercase"""
        return v.upper().strip()


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee"""
    
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=2, max_length=50)
    position: Optional[str] = Field(None, min_length=2, max_length=100)
    
    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "full_name": "Rajesh Kumar Singh",
                "department": "Senior Engineering"
            }
        }
    )
    
    @field_validator('full_name', 'department', 'position')
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Strip leading/trailing whitespace"""
        return v.strip() if v else v
    
    @field_validator('email')
    @classmethod
    def lowercase_email(cls, v: Optional[str]) -> Optional[str]:
        """Convert email to lowercase"""
        return v.lower() if v else v


class EmployeeResponse(BaseModel):
    """Schema for employee response"""
    
    id: str = Field(..., alias="_id", description="MongoDB document ID")
    employee_id: str
    full_name: str
    email: str
    department: str
    position: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "employee_id": "EMP-001",
                "full_name": "Rajesh Kumar",
                "email": "rajesh.kumar@company.com",
                "department": "Engineering",
                "position": "Senior Software Engineer",
                "created_at": "2026-02-07T10:00:00Z",
                "updated_at": "2026-02-07T10:00:00Z"
            }
        }
    )


class EmployeeListResponse(BaseModel):
    """Schema for employee list response"""
    
    success: bool = True
    data: list[EmployeeResponse]
    total: int
    
    model_config = ConfigDict(from_attributes=True)
