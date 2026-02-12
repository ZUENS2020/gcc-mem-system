"""Audit logging for GCC system.

Records all operations for security, compliance, and debugging purposes.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class AuditLogger:
    """Audit logger for tracking all operations.

    Records operations with timestamps, parameters, and results
    for security auditing and compliance.
    """

    def __init__(self, log_dir: Path):
        """Initialize audit logger.

        Args:
            log_dir: Directory for audit logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / "audit.log"

    def log(
        self,
        action: str,
        session_id: Optional[str],
        user: Optional[str],
        params: Dict[str, Any],
        result: str = "success",
        error: Optional[str] = None,
    ) -> None:
        """Record an audit event.

        Args:
            action: Operation performed (e.g., "gcc_init", "gcc_commit")
            session_id: Session identifier
            user: User identifier (optional)
            params: Operation parameters (sanitized)
            result: Operation result (success/error)
            error: Error message if operation failed
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "session_id": session_id,
            "user": user,
            "params": self._sanitize(params),
            "result": result,
            "error": error,
        }

        try:
            with self.log_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            # Fallback to stderr if audit log fails
            import sys
            print(f"Failed to write audit log: {e}", file=sys.stderr)

    def _sanitize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize sensitive information from parameters.

        Args:
            params: Original parameters

        Returns:
            Sanitized parameters with sensitive values redacted
        """
        if not params:
            return {}

        sensitive_keys = {
            "password", "token", "secret", "key", "api_key",
            "private_key", "credential", "auth"
        }

        sanitized = {}
        for key, value in params.items():
            key_lower = key.lower()
            if any(s in key_lower for s in sensitive_keys):
                # Check if value is a string/bytes type
                if isinstance(value, (str, bytes)):
                    sanitized[key] = "***REDACTED***"
                elif isinstance(value, dict):
                    # Recursively sanitize dict values
                    sanitized[key] = self._sanitize(value)
                else:
                    sanitized[key] = type(value).__name__
            else:
                # Truncate long values
                if isinstance(value, str) and len(value) > 1000:
                    sanitized[key] = value[:1000] + "... (truncated)"
                elif isinstance(value, dict):
                    sanitized[key] = self._sanitize(value)
                else:
                    sanitized[key] = value

        return sanitized


# Global audit logger instance
_global_audit_logger: Optional[AuditLogger] = None


def get_audit_logger() -> Optional[AuditLogger]:
    """Get the global audit logger.

    Returns:
        AuditLogger instance if enabled, None otherwise
    """
    global _global_audit_logger

    # Check if audit logging is enabled
    if os.environ.get("GCC_ENABLE_AUDIT_LOG", "true").lower() != "true":
        return None

    if _global_audit_logger is not None:
        return _global_audit_logger

    # Get log directory from environment or use default
    log_dir = os.environ.get("GCC_LOG_DIR", "/var/log/gcc")
    _global_audit_logger = AuditLogger(Path(log_dir))

    return _global_audit_logger


def log_operation(
    action: str,
    session_id: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    result: str = "success",
    error: Optional[str] = None,
) -> None:
    """Convenience function to log an operation.

    Args:
        action: Operation performed
        session_id: Session identifier
        params: Operation parameters
        result: Operation result
        error: Error message if failed
    """
    audit_logger = get_audit_logger()
    if audit_logger:
        audit_logger.log(
            action=action,
            session_id=session_id,
            user=None,  # Could be extracted from request headers in future
            params=params or {},
            result=result,
            error=error,
        )
