"""FastAPI application for GCC HTTP server.

Creates and configures the FastAPI app with all endpoints and middleware.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI

from .config import GCCConfig, get_config
from .endpoints import router
from .middleware import setup_middleware
from ..logging.logger import GCCLogger


def create_app(config: GCCConfig | None = None) -> FastAPI:
    """Create and configure FastAPI application.

    Args:
        config: Optional configuration (uses env vars if not provided)

    Returns:
        Configured FastAPI application
    """
    if config is None:
        config = get_config()

    # Initialize logging system
    log_dir = Path(os.environ.get("GCC_LOG_DIR", config.logging.log_dir))
    log_dir.mkdir(parents=True, exist_ok=True)

    # Get logger for app initialization
    logger = GCCLogger.get_logger("gcc.app", log_dir, config.server.log_level)
    logger.info(f"Initializing GCC server (log directory: {log_dir})")

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

    logger.info("GCC server initialized successfully")
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
