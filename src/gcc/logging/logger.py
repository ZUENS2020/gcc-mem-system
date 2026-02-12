"""Logging infrastructure for GCC system.

Provides centralized logging with file rotation, different log levels,
and proper formatting for both development and production environments.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


# Log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class GCCLogger:
    """Centralized logger with caching and rotation support.

    Provides consistent logging across all modules with automatic
    file rotation and sensible defaults.
    """

    _instances: dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(
        cls,
        name: str,
        log_dir: Optional[Path] = None,
        level: Optional[str] = None,
    ) -> logging.Logger:
        """Get or create a logger with file rotation.

        Args:
            name: Logger name (typically __name__ of module)
            log_dir: Directory for log files (default from config/env)
            level: Log level (debug, info, warning, error, critical)

        Returns:
            Configured logger instance
        """
        if name in cls._instances:
            return cls._instances[name]

        # Create logger
        logger = logging.getLogger(name)

        # Set log level
        log_level = cls._get_log_level(level)
        logger.setLevel(log_level)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        # Create formatter
        formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

        # Console handler (always present)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler with rotation (if log_dir is specified)
        if log_dir is not None:
            log_dir = Path(log_dir)
            log_dir.mkdir(parents=True, exist_ok=True)

            # Rotating file handler: 10MB max, 5 backups
            file_handler = RotatingFileHandler(
                log_dir / "gcc.log",
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # Prevent propagation to root logger
        logger.propagate = False

        # Cache instance
        cls._instances[name] = logger
        return logger

    @staticmethod
    def _get_log_level(level: Optional[str]) -> int:
        """Convert string level to logging constant.

        Args:
            level: String level (debug, info, warning, error, critical)

        Returns:
            Logging level constant
        """
        if not level:
            # Check environment variable
            env_level = os.environ.get("GCC_LOG_LEVEL", "info").lower()
            level = env_level

        level_map = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        return level_map.get(level.lower(), logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a logger.

    Args:
        name: Logger name

    Returns:
        Logger instance with default configuration
    """
    return GCCLogger.get_logger(name)
