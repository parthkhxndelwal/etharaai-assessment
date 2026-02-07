"""
Attendance API Schemas
Request and response models for attendance endpoints
"""

from datetime import datetime
from datetime import date as DateType
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


class AttendanceCreate(BaseModel):
    """Schema for marking attendance"""
    
    employee_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee identifier"
    )
    date: Union[DateType, datetime] = Field(..., description="Attendance date (YYYY-MM-DD)")
    status: Literal["Present", "Absent"] = Field(..., description="Attendance status")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")
    
    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "employee_id": "EMP-001",
                "date": "2026-02-07",
                "status": "Present"
            }
        }
    )
    
    @field_validator('employee_id')
    @classmethod
    def uppercase_employee_id(cls, v: str) -> str:
        """Convert employee_id to uppercase"""
        return v.upper().strip()
    
    @field_validator('date')
    @classmethod
    def convert_date_to_datetime(cls, v: Union[DateType, datetime]) -> datetime:
        """Convert date to datetime for BSON compatibility and validate not future"""
        # Convert date to datetime if needed
        if isinstance(v, DateType) and not isinstance(v, datetime):
            dt = datetime.combine(v, datetime.min.time())
        else:
            dt = v
        
        # Check if date is in the future
        today = datetime.combine(DateType.today(), datetime.min.time())
        if dt > today:
            raise ValueError('Attendance cannot be marked for future dates')
        
        return dt


class AttendanceUpdate(BaseModel):
    """Schema for updating attendance"""
    
    status: Literal["Present", "Absent"] = Field(..., description="Attendance status")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")
    
    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "status": "Absent"
            }
        }
    )


class AttendanceResponse(BaseModel):
    """Schema for attendance response"""
    
    id: str = Field(..., alias="_id", serialization_alias="id", description="MongoDB document ID")
    employee_id: str
    employee_name: Optional[str] = Field(None, description="Employee full name (populated from employee record)")
    date: DateType
    status: Literal["Present", "Absent"]
    notes: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={DateType: lambda v: v.isoformat()},
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "employee_id": "EMP-001",
                "date": "2026-02-07",
                "status": "Present",
                "created_at": "2026-02-07T10:00:00Z"
            }
        }
    )


class AttendanceFilter(BaseModel):
    """Schema for filtering attendance records"""
    
    employee_id: Optional[str] = Field(None, description="Filter by employee ID")
    date: Optional[DateType] = Field(None, description="Filter by specific date")
    start_date: Optional[DateType] = Field(None, description="Filter from this date")
    end_date: Optional[DateType] = Field(None, description="Filter until this date")
    status: Optional[Literal["Present", "Absent"]] = Field(None, description="Filter by status")
    
    model_config = ConfigDict(from_attributes=True)


class AttendanceListResponse(BaseModel):
    """Schema for attendance list response"""
    
    success: bool = True
    data: list[AttendanceResponse]
    total: int
    
    model_config = ConfigDict(
        from_attributes=True,
        # Ensure id is used instead of _id in JSON output
        ser_json_timedelta='float',
    )


class EmployeeAttendanceSummary(BaseModel):
    """Schema for employee attendance summary"""
    
    employee_id: str
    full_name: str
    present_days: int
    absent_days: int
    total_days: int
    attendance_percentage: float
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "employee_id": "EMP-001",
                "full_name": "Rajesh Kumar",
                "present_days": 18,
                "absent_days": 2,
                "total_days": 20,
                "attendance_percentage": 90.0
            }
        }
    )
