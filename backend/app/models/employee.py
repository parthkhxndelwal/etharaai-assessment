"""
Employee Model
Represents employee document structure in MongoDB
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class Employee(BaseModel):
    """Employee database model"""
    
    employee_id: str = Field(..., max_length=50, description="Unique employee identifier")
    full_name: str = Field(..., max_length=100, description="Employee full name")
    email: EmailStr = Field(..., description="Employee email address")
    department: str = Field(..., max_length=50, description="Department name")
    position: str = Field(..., max_length=100, description="Job position/title")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "employee_id": "EMP-001",
                "full_name": "Rajesh Kumar",
                "email": "rajesh.kumar@company.com",
                "department": "Engineering",
                "position": "Senior Software Engineer",
                "created_at": "2026-02-07T10:00:00",
                "updated_at": "2026-02-07T10:00:00"
            }
        }
    )
