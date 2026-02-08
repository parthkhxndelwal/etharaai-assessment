"""
Authentication Router
Endpoints for login and user info
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config import settings
from ..schemas.auth import LoginRequest, TokenResponse, UserResponse
from ..services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user
)


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=TokenResponse)
@limiter.limit(f"{settings.rate_limit_auth_per_minute}/minute")
async def login(request: Request, login_data: LoginRequest):
    """
    Email/Password Login
    
    Authenticate with email and password and receive a JWT token.
    
    - **email**: User email address
    - **password**: User password
    
    Returns JWT access token and user information.
    """
    # Authenticate user
    user = await authenticate_user(login_data.email, login_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["email"]})
    
    # Prepare user response
    user_response = UserResponse(
        email=user["email"],
        full_name=user["full_name"],
        role=user["role"],
        is_active=user.get("is_active", True)
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get Current User
    
    Retrieve information about the currently authenticated user.
    
    Requires valid JWT token in Authorization header.
    """
    return UserResponse(
        email=current_user["email"],
        full_name=current_user["full_name"],
        role=current_user["role"],
        is_active=current_user.get("is_active", True)
    )
