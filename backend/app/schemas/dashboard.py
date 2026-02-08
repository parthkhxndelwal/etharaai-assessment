"""Dashboard schemas"""

from typing import Dict
from pydantic import BaseModel, Field, ConfigDict


class DashboardSummary(BaseModel):
    """Schema for dashboard summary statistics"""
    
    total_employees: int = Field(..., description="Total number of employees")
    present_today: int = Field(..., description="Employees present today")
    absent_today: int = Field(..., description="Employees absent today")
    department_counts: Dict[str, int] = Field(..., description="Employee count by department")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "total_employees": 150,
                "present_today": 142,
                "absent_today": 8,
                "department_counts": {
                    "Engineering": 60,
                    "Sales": 40,
                    "HR": 20,
                    "Finance": 30
                }
            }
        }
    )


class DashboardResponse(BaseModel):
    """Schema for dashboard response"""
    
    success: bool = True
    data: DashboardSummary
    
    model_config = ConfigDict(from_attributes=True)
