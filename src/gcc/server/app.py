"""FastAPI application for GCC HTTP server.

Creates and configures the FastAPI app with all endpoints and middleware.
"""
from __future__ import annotations

from fastapi import FastAPI

from .config import GCCConfig, get_config
from .endpoints import router
from .middleware import setup_middleware


def create_app(config: GCCConfig | None = None) -> FastAPI:
    """Create and configure FastAPI application.

    Args:
        config: Optional configuration (uses env vars if not provided)

    Returns:
        Configured FastAPI application
    """
    if config is None:
        config = get_config()

    # Create FastAPI app
    app = FastAPI(
        title="GCC Context Controller",
        description="Git-Context-Controller (GCC) memory system HTTP API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Setup middleware
    setup_middleware(app, config)

    # Include endpoints
    app.include_router(router)

    # Health check endpoint
    @app.get("/health", tags=["health"])
    def health_check():
        """Health check endpoint.

        Returns:
            Status indicator
        """
        return {"status": "ok", "version": "1.0.0"}

    return app


# Create default app instance
app = create_app()


def main() -> None:
    """Entry point for running the server.

    Can be invoked via:
    - gcc-server command
    - python -m gcc.server.app
    - uvicorn gcc.server.app:app
    """
    import uvicorn

    config = get_config()
    uvicorn.run(
        app,
        host=config.server.host,
        port=config.server.port,
        workers=config.server.workers,
        log_level=config.server.log_level,
        reload=config.server.reload,
    )
