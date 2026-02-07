"""
Attendance Model
Represents attendance record structure in MongoDB
"""

from datetime import datetime, date
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class Attendance(BaseModel):
    """Attendance database model"""
    
    employee_id: str = Field(..., max_length=50, description="Employee identifier")
    date: datetime = Field(..., description="Attendance date")
    status: Literal["Present", "Absent"] = Field(..., description="Attendance status")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "employee_id": "EMP-001",
                "date": "2026-02-07",
                "status": "Present",
                "created_at": "2026-02-07T10:00:00"
            }
        }
    )
