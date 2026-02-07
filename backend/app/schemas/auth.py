"""
Authentication API Schemas
Request and response models for auth endpoints
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    """Schema for email/password login"""
    
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")
    
    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "email": "admin@sutra.com",
                "password": "admin123"
            }
        }
    )


class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth login"""
    
    credential: str = Field(..., description="Google ID token from OAuth response")
    
    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            "example": {
                "credential": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
            }
        }
    )


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    
    success: bool = True
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: "UserResponse" = Field(..., description="User information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "email": "admin@sutra.com",
                    "full_name": "System Administrator",
                    "role": "admin"
                }
            }
        }
    )


class UserResponse(BaseModel):
    """Schema for user information response"""
    
    email: str
    full_name: str
    role: str
    is_active: bool = True
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "admin@sutra.com",
                "full_name": "System Administrator",
                "role": "admin",
                "is_active": True
            }
        }
    )


class TokenData(BaseModel):
    """Schema for JWT token payload data"""
    
    email: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
