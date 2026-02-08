"""
Configuration Management
Loads environment variables using pydantic-settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Sutra HRMS"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # MongoDB
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db_name: str = "sutra_hrms"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT Authentication
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # Admin User
    admin_email: str = "admin@sutra.com"
    admin_password: str = "admin123"
    admin_name: str = "System Administrator"
    
    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_auth_per_minute: int = 10
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()
