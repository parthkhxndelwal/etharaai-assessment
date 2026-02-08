"""Common response schemas"""

from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel, Field, ConfigDict


T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper"""
    
    success: bool = Field(default=True, description="Request success status")
    data: Optional[T] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Response message")
    
    model_config = ConfigDict(from_attributes=True)


class ErrorDetail(BaseModel):
    """Error detail model"""
    
    field: Optional[str] = Field(None, description="Field with error")
    message: str = Field(..., description="Error message")
    type: Optional[str] = Field(None, description="Error type")


class ErrorResponse(BaseModel):
    """Error response model"""
    
    success: bool = Field(default=False, description="Request success status")
    detail: str = Field(..., description="Error detail message")
    errors: Optional[List[ErrorDetail]] = Field(None, description="List of validation errors")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "detail": "Validation error",
                "errors": [
                    {
                        "field": "email",
                        "message": "Invalid email format",
                        "type": "value_error"
                    }
                ]
            }
        }
    )


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper"""
    
    success: bool = Field(default=True)
    data: List[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total count")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=50, description="Items per page")
    
    model_config = ConfigDict(from_attributes=True)
