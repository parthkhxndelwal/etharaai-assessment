"""
Authentication Service
Handles user authentication, JWT tokens, and Google OAuth
"""

from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from google.auth.transport import requests
from google.oauth2 import id_token
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..config import settings
from ..database import get_users_collection
from ..models.user import User
from ..schemas.auth import TokenData, UserResponse


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional token expiration time
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


async def verify_google_token(token: str) -> dict:
    """
    Verify Google ID token and extract user info
    
    Args:
        token: Google ID token
    
    Returns:
        User info from Google
    
    Raises:
        HTTPException: If token is invalid
    """
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.google_client_id
        )
        
        # Token is valid, extract user info
        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "google_id": idinfo.get("sub"),
            "picture": idinfo.get("picture")
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with email and password
    
    Args:
        email: User email
        password: Plain text password
    
    Returns:
        User document if authentication successful, None otherwise
    """
    users_collection = get_users_collection()
    user = await users_collection.find_one({"email": email.lower()})
    
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Get current user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
    
    Returns:
        User document
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        token_data = TokenData(email=email)
    
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    users_collection = get_users_collection()
    user = await users_collection.find_one({"email": token_data.email})
    
    if user is None:
        raise credentials_exception
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def seed_admin_user():
    """
    Create default admin user if not exists
    Called during application startup
    """
    users_collection = get_users_collection()
    
    # Check if admin user exists
    admin_exists = await users_collection.find_one({"email": settings.admin_email.lower()})
    
    if not admin_exists:
        # Create admin user
        admin_user = {
            "email": settings.admin_email.lower(),
            "hashed_password": get_password_hash(settings.admin_password),
            "full_name": settings.admin_name,
            "role": "admin",
            "is_active": True,
            "google_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await users_collection.insert_one(admin_user)
        print(f"✅ Admin user created: {settings.admin_email}")
    else:
        print(f"✅ Admin user already exists: {settings.admin_email}")


async def create_or_update_google_user(google_info: dict) -> dict:
    """
    Create or update user from Google OAuth info
    
    Args:
        google_info: User info from Google
    
    Returns:
        User document
    """
    users_collection = get_users_collection()
    email = google_info["email"].lower()
    
    # Check if user exists
    user = await users_collection.find_one({"email": email})
    
    if user:
        # Update Google ID if not set
        if not user.get("google_id"):
            await users_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "google_id": google_info["google_id"],
                        "updated_at": datetime.utcnow()
                    }
                }
            )
        
        return await users_collection.find_one({"email": email})
    
    else:
        # Create new user from Google info
        new_user = {
            "email": email,
            "hashed_password": get_password_hash(""),  # No password for Google users
            "full_name": google_info.get("name", "User"),
            "role": "admin",  # Default role
            "is_active": True,
            "google_id": google_info["google_id"],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await users_collection.insert_one(new_user)
        return await users_collection.find_one({"_id": result.inserted_id})
