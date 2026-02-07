"""
User Model
Represents admin user structure in MongoDB
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    """User database model"""
    
    email: EmailStr = Field(..., description="User email address")
    hashed_password: str = Field(..., description="Hashed password")
    full_name: str = Field(..., max_length=100, description="Full name")
    role: str = Field(default="admin", max_length=20, description="User role")
    is_active: bool = Field(default=True, description="Active status")
    google_id: Optional[str] = Field(None, description="Google OAuth ID")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "admin@sutra.com",
                "full_name": "System Administrator",
                "role": "admin",
                "is_active": True,
                "created_at": "2026-02-07T10:00:00",
                "updated_at": "2026-02-07T10:00:00"
            }
        }
    )
