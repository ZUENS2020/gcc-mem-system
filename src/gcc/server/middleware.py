"""Middleware for GCC FastAPI server.

Provides exception handling, request tracking, rate limiting,
and other cross-cutting concerns.
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


class ExceptionHandlingMiddleware:
    """Custom exception handler for GCC exceptions.

    Converts GCC exception types into appropriate HTTP responses.
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
        if isinstance(exc, ValidationError):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"error": "validation_error", "detail": str(exc)},
            )
        elif isinstance(exc, BranchNotFoundError):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "branch_not_found", "detail": str(exc)},
            )
        elif isinstance(exc, SessionNotFoundError):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "session_not_found", "detail": str(exc)},
            )
        elif isinstance(exc, LockError):
            return JSONResponse(
                status_code=status.HTTP_423_LOCKED,
                content={"error": "lock_error", "detail": str(exc)},
            )
        elif isinstance(exc, RateLimitError):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "rate_limit_exceeded", "detail": str(exc)},
            )
        elif isinstance(exc, (RepositoryError, StorageError)):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "storage_error",
                    "detail": "Storage operation failed. Please try again.",
                },
            )
        elif isinstance(exc, GCCError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "gcc_error", "detail": str(exc)},
            )
        else:
            # Unknown error - don't expose internal details
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "internal_error",
                    "detail": "An internal error occurred. Please try again later.",
                },
            )


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    """Add request ID and timing information to requests.

    Generates unique request IDs and measures processing time.
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

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Add headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"

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
