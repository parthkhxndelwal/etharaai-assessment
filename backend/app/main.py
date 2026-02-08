"""Main FastAPI application"""

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
    print("Starting Sutra Backend...")
    await DatabaseManager.connect()
    await DatabaseManager.create_indexes()
    await CacheManager.connect()

    from .services.auth_service import seed_admin_user
    await seed_admin_user()
    print("Sutra Backend is ready!")

    yield

    await DatabaseManager.close()
    await CacheManager.close()


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Sutra API",
    description="""
    A modern, lightweight Human Resource Management System.
    
    **Features:**
    - Employee Management (CRUD operations)
    - Attendance Tracking
    - Dashboard Analytics
    - JWT Authentication
    - Redis-powered caching
    - Rate limiting
    
    **Authentication:**
    - Use `/api/v1/auth/login` to get a JWT token
    - Click "Authorize" and enter: `Bearer <your-token>`
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "JWT authentication endpoints"
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

# Rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600
)

# Custom middleware
add_request_id_middleware(app)
add_process_time_middleware(app)
add_security_headers_middleware(app)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Sutra API",
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sutra API",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


# Import and include routers
# (imported here to avoid circular imports)
def include_routers():
    from .routers import auth, employees, attendance, dashboard

    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(employees.router, prefix="/api/v1/employees", tags=["Employees"])
    app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
    app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])


include_routers()


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
