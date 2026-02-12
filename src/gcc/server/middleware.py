"""Middleware for GCC FastAPI server.

Provides exception handling, request tracking, rate limiting,
audit logging, and other cross-cutting concerns.
"""
from __future__ import annotations

import time
import uuid
from collections import defaultdict
from typing import Callable

from fastapi import Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from ..core.exceptions import (
    GCCError,
    ValidationError,
    RepositoryError,
    StorageError,
    BranchNotFoundError,
    SessionNotFoundError,
    LockError,
    RateLimitError,
)
from ..logging.audit import log_operation


class ExceptionHandlingMiddleware:
    """Custom exception handler for GCC exceptions.

    Converts GCC exception types into appropriate HTTP responses
    and logs all errors for audit purposes.
    """

    @staticmethod
    async def handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle exceptions and return appropriate HTTP responses.

        Args:
            request: The incoming request
            exc: The raised exception

        Returns:
            JSONResponse with appropriate status code and error details
        """
        # Determine error type and response
        error_type = "unknown_error"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        detail = "An internal error occurred. Please try again later."

        if isinstance(exc, ValidationError):
            error_type = "validation_error"
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            detail = str(exc)
        elif isinstance(exc, BranchNotFoundError):
            error_type = "branch_not_found"
            status_code = status.HTTP_404_NOT_FOUND
            detail = str(exc)
        elif isinstance(exc, SessionNotFoundError):
            error_type = "session_not_found"
            status_code = status.HTTP_404_NOT_FOUND
            detail = str(exc)
        elif isinstance(exc, LockError):
            error_type = "lock_error"
            status_code = status.HTTP_423_LOCKED
            detail = str(exc)
        elif isinstance(exc, RateLimitError):
            error_type = "rate_limit_exceeded"
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
            detail = str(exc)
        elif isinstance(exc, (RepositoryError, StorageError)):
            error_type = "storage_error"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            detail = "Storage operation failed. Please try again."
        elif isinstance(exc, GCCError):
            error_type = "gcc_error"
            status_code = status.HTTP_400_BAD_REQUEST
            detail = str(exc)

        # Log error for audit
        log_operation(
            action=f"error_{error_type}",
            params={
                "method": request.method,
                "url": str(request.url),
                "error_type": error_type,
            },
            result="error",
            error=str(exc),
        )

        return JSONResponse(
            status_code=status_code,
            content={"error": error_type, "detail": detail},
        )


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Add request ID and timing information to requests.

    Generates unique request IDs and measures processing time.
    Also logs all requests for audit trail.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and add tracking headers.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response with tracking headers
        """
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Record start time
        start_time = time.time()

        # Extract endpoint info
        endpoint = getattr(request.state, "route", None)
        endpoint_name = endpoint.path if endpoint else "unknown"

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

        # Log successful request for audit
        log_operation(
            action=f"api_{request.method.lower()}",
            params={
                "method": request.method,
                "url": str(request.url),
                "endpoint": endpoint_name,
                "status_code": response.status_code,
                "process_time": f"{process_time:.3f}",
            },
            result="success" if response.status_code < 400 else "error",
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware.

    Tracks requests per client IP and enforces rate limits.
    """

    def __init__(self, app, requests_per_minute: int = 60):
        """Initialize rate limiter.

        Args:
            app: The ASGI application
            requests_per_minute: Maximum requests per minute per client
        """
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limit and process request.

        Args:
            request: The incoming request
            call_next: The next middleware or route handler

        Returns:
            Response or rate limit error

        Raises:
            HTTPException: If rate limit exceeded
        """
        # Identify client
        client_ip = self._get_client_ip(request)

        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < 60
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
                headers={"Retry-After": "60"},
            )

        # Record request
        self.requests[client_ip].append(now)

        return await call_next(request)

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        """Get client IP address, considering proxies.

        Args:
            request: The incoming request

        Returns:
            Client IP address string
        """
        # Check for forwarded header (proxy/load balancer)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        # Check for real IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # Fall back to direct connection IP
        if request.client:
            return request.client.host

        return "unknown"


def setup_middleware(app, config):
    """Configure all middleware for the FastAPI app.

    Args:
        app: The FastAPI application instance
        config: Server configuration
    """
    # Exception handler
    app.add_exception_handler(Exception, ExceptionHandlingMiddleware.handler)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request tracking
    app.add_middleware(RequestTrackingMiddleware)

    # Rate limiting (if enabled)
    if config.security.enable_rate_limiting:
        app.add_middleware(
            RateLimitMiddleware,
            requests_per_minute=config.security.rate_limit_requests,
        )
