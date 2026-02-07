"""
Sutra HRMS - Main FastAPI Application
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import settings
from .database import DatabaseManager
from .cache import CacheManager
from .middleware import (
    add_security_headers_middleware,
    add_process_time_middleware,
    add_request_id_middleware
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("🚀 Starting Sutra HRMS Backend...")
    
    # Connect to MongoDB
    await DatabaseManager.connect()
    
    # Create indexes
    await DatabaseManager.create_indexes()
    
    # Connect to Redis
    await CacheManager.connect()
    
    # Seed admin user
    from .services.auth_service import seed_admin_user
    await seed_admin_user()
    
    print("✅ Sutra HRMS Backend is ready!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Sutra HRMS Backend...")
    await DatabaseManager.close()
    await CacheManager.close()
    print("✅ Shutdown complete")


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="Sutra HRMS API",
    description="""
    🕉️ **Sutra HRMS Lite** - A modern, lightweight Human Resource Management System
    
    **Features:**
    - Employee Management (CRUD operations)
    - Attendance Tracking
    - Dashboard Analytics
    - JWT + Google OAuth Authentication
    - Redis-powered caching
    - Rate limiting for security
    
    **Authentication:**
    - Use `/api/v1/auth/login` to get JWT token
    - Click "Authorize" button and enter: `Bearer <your-token>`
    
    ---
    
    *Built with FastAPI, MongoDB, and Redis*
    
    **Jai Shree Ram!** 🚩
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "JWT and Google OAuth authentication endpoints"
        },
        {
            "name": "Employees",
            "description": "Employee management operations (CRUD)"
        },
        {
            "name": "Attendance",
            "description": "Attendance tracking and reporting"
        },
        {
            "name": "Dashboard",
            "description": "Analytics and summary statistics"
        }
    ],
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

# Add custom middleware (order matters - last added runs first)
add_request_id_middleware(app)
add_process_time_middleware(app)
add_security_headers_middleware(app)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Sutra HRMS API",
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sutra HRMS API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Import and include routers (will be added after creating routers)
# Note: Import here to avoid circular imports
def include_routers():
    """Include all API routers"""
    try:
        from .routers import auth, employees, attendance, dashboard
        
        app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
        app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
        app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
        app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
        
        print("✅ API routers included")
    except ImportError as e:
        print(f"⚠️  Some routers not yet created: {e}")


# Include routers
include_routers()


# Custom exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "detail": "Resource not found",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )
