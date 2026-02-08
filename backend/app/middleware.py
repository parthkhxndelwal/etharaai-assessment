"""Custom middleware for security headers, request tracking, and timing"""

import time
import uuid
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Add HSTS only in production (when not localhost)
        if not request.url.hostname in ["localhost", "127.0.0.1"]:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy - relaxed for Swagger/ReDoc docs pages
        if request.url.path in ("/docs", "/redoc", "/openapi.json"):
            response.headers["Content-Security-Policy"] = (
                "default-src 'self'; "
                "img-src 'self' https://fastapi.tiangolo.com data:; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "worker-src 'self' blob:"
            )
        else:
            response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Add X-Process-Time header showing request processing time"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request"""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


def add_security_headers_middleware(app: FastAPI):
    """Add security headers middleware to app"""
    app.add_middleware(SecurityHeadersMiddleware)


def add_process_time_middleware(app: FastAPI):
    """Add process time middleware to app"""
    app.add_middleware(ProcessTimeMiddleware)


def add_request_id_middleware(app: FastAPI):
    """Add request ID middleware to app"""
    app.add_middleware(RequestIDMiddleware)
