"""Unified configuration management for GCC system.

This module provides centralized configuration with environment variable support,
allowing different modes (MCP, skill, standalone) to customize behavior.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GitConfig:
    """Git operation configuration.

    Attributes:
        default_name: Default git user name
        default_email: Default git user email
        default_branch: Default branch name
    """

    default_name: str = "GCC Agent"
    default_email: str = "gcc@example.com"
    default_branch: str = "main"

    @classmethod
    def from_env(cls) -> GitConfig:
        """Create config from environment variables."""
        return cls(
            default_name=os.getenv("GCC_GIT_NAME", cls.default_name),
            default_email=os.getenv("GCC_GIT_EMAIL", cls.default_email),
            default_branch=os.getenv("GCC_GIT_DEFAULT_BRANCH", cls.default_branch),
        )


@dataclass
class SecurityConfig:
    """Security and validation configuration.

    Attributes:
        max_branch_name_length: Maximum branch name length
        max_session_id_length: Maximum session ID length
        max_limit: Maximum value for limit parameters
        min_limit: Minimum value for limit parameters
        max_string_length: Maximum length for string parameters
        allow_path_traversal: Whether to allow path traversal (should be False)
        enable_rate_limiting: Enable rate limiting middleware
        rate_limit_requests: Requests per minute per client
    """

    max_branch_name_length: int = 100
    max_session_id_length: int = 100
    max_limit: int = 1000
    min_limit: int = 1
    max_string_length: int = 10000
    allow_path_traversal: bool = False
    enable_rate_limiting: bool = True
    rate_limit_requests: int = 60

    @classmethod
    def from_env(cls) -> SecurityConfig:
        """Create config from environment variables."""
        return cls(
            max_branch_name_length=int(os.getenv("GCC_MAX_BRANCH_LENGTH", str(cls.max_branch_name_length))),
            max_session_id_length=int(os.getenv("GCC_MAX_SESSION_LENGTH", str(cls.max_session_id_length))),
            max_limit=int(os.getenv("GCC_MAX_LIMIT", str(cls.max_limit))),
            min_limit=int(os.getenv("GCC_MIN_LIMIT", str(cls.min_limit))),
            max_string_length=int(os.getenv("GCC_MAX_STRING_LENGTH", str(cls.max_string_length))),
            allow_path_traversal=os.getenv("GCC_ALLOW_PATH_TRAVERSAL", "false").lower() == "true",
            enable_rate_limiting=os.getenv("GCC_ENABLE_RATE_LIMIT", "true").lower() == "true",
            rate_limit_requests=int(os.getenv("GCC_RATE_LIMIT_REQUESTS", str(cls.rate_limit_requests))),
        )


@dataclass
class ServerConfig:
    """FastAPI server configuration.

    Attributes:
        host: Server host address
        port: Server port
        workers: Number of worker processes
        log_level: Logging level
        reload: Enable auto-reload for development
        access_log: Enable access logging
    """

    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    log_level: str = "info"
    reload: bool = False
    access_log: bool = True

    @classmethod
    def from_env(cls) -> ServerConfig:
        """Create config from environment variables."""
        return cls(
            host=os.getenv("GCC_HOST", cls.host),
            port=int(os.getenv("GCC_PORT", str(cls.port))),
            workers=int(os.getenv("GCC_WORKERS", str(cls.workers))),
            log_level=os.getenv("GCC_LOG_LEVEL", cls.log_level),
            reload=os.getenv("GCC_RELOAD", "false").lower() == "true",
            access_log=os.getenv("GCC_ACCESS_LOG", "true").lower() == "true",
        )


@dataclass
class LoggingConfig:
    """Logging configuration.

    Attributes:
        log_dir: Directory for log files
        log_max_bytes: Maximum size of each log file before rotation
        log_backup_count: Number of backup log files to keep
        enable_audit_log: Enable audit logging
        enable_git_log: Enable git command logging
        log_format: Log message format
    """

    log_dir: str = "/var/log/gcc"
    log_max_bytes: int = 10 * 1024 * 1024  # 10MB
    log_backup_count: int = 5
    enable_audit_log: bool = True
    enable_git_log: bool = True
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @classmethod
    def from_env(cls) -> LoggingConfig:
        """Create config from environment variables."""
        return cls(
            log_dir=os.getenv("GCC_LOG_DIR", cls.log_dir),
            log_max_bytes=int(os.getenv("GCC_LOG_MAX_BYTES", str(cls.log_max_bytes))),
            log_backup_count=int(os.getenv("GCC_LOG_BACKUP_COUNT", str(cls.log_backup_count))),
            enable_audit_log=os.getenv("GCC_ENABLE_AUDIT_LOG", "true").lower() == "true",
            enable_git_log=os.getenv("GCC_ENABLE_GIT_LOG", "true").lower() == "true",
        )


@dataclass
class GCCConfig:
    """Main configuration container.

    This class aggregates all sub-configurations and provides
    a single entry point for configuration access.
    """

    git: GitConfig = field(default_factory=GitConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    @classmethod
    def from_env(cls) -> GCCConfig:
        """Create complete config from environment variables."""
        return cls(
            git=GitConfig.from_env(),
            security=SecurityConfig.from_env(),
            server=ServerConfig.from_env(),
            logging=LoggingConfig.from_env(),
        )


# Global config instance (can be overridden by application startup)
_global_config: Optional[GCCConfig] = None


def get_config() -> GCCConfig:
    """Get the global configuration instance.

    Returns:
        GCCConfig: The current configuration

    Raises:
        RuntimeError: If config has not been initialized
    """
    global _global_config
    if _global_config is None:
        _global_config = GCCConfig.from_env()
    return _global_config


def set_config(config: GCCConfig) -> None:
    """Set the global configuration instance.

    Args:
        config: The configuration to use globally
    """
    global _global_config
    _global_config = config
