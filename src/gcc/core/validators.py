"""Input validation for GCC system.

Provides validation functions for all user inputs to prevent
security issues like injection attacks and path traversal.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

from .exceptions import ValidationError


def _get_security_config():
    """Get security configuration.

    Returns:
        SecurityConfig instance
    """
    try:
        from ..server.config import get_config
        config = get_config()
        return config.security
    except Exception:
        # Fallback defaults if config not initialized
        class SecurityConfig:
            max_branch_name_length = 100
            max_session_id_length = 100
            max_limit = 1000
            min_limit = 1
            max_string_length = 10000
            allow_path_traversal = False
        return SecurityConfig()


# Regex patterns for validation
BRANCH_NAME_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]*$')
SESSION_ID_PATTERN = re.compile(r'^[A-Za-z0-9_-]+$')
GIT_REF_PATTERN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_./~-]*$')
SAFE_STRING_PATTERN = re.compile(r'^[A-Za-z0-9\s\-_.,!?@#$%&*()+=:\'"\\/]*$')


class Validators:
    """Input validation utilities.

    All validation methods raise ValidationError on failure.
    """

    @staticmethod
    def validate_branch_name(name: str) -> str:
        """Validate git branch name.

        Args:
            name: Branch name to validate

        Returns:
            Validated branch name

        Raises:
            ValidationError: If name is invalid
        """
        config = _get_security_config()

        if not name:
            raise ValidationError(
                "branch name cannot be empty",
                field="branch",
            )

        if len(name) > config.max_branch_name_length:
            raise ValidationError(
                f"branch name too long (max {config.max_branch_name_length} characters)",
                field="branch",
                value=name[:50] + "..." if len(name) > 50 else name,
            )

        if not BRANCH_NAME_PATTERN.match(name):
            raise ValidationError(
                "branch name must start with alphanumeric character and contain only alphanumeric, underscore, or hyphen",
                field="branch",
                value=name,
            )

        # Prevent git-specific special names
        if name in ("HEAD", "ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD"):
            raise ValidationError(
                f"branch name '{name}' is reserved by git",
                field="branch",
                value=name,
            )

        return name

    @staticmethod
    def validate_session_id(session_id: Optional[str]) -> str:
        """Validate and normalize session ID.

        Args:
            session_id: Session identifier (may be empty)

        Returns:
            Normalized session ID ("default" if empty)

        Raises:
            ValidationError: If session_id is invalid
        """
        config = _get_security_config()

        if not session_id:
            return "default"

        if len(session_id) > config.max_session_id_length:
            raise ValidationError(
                f"session_id too long (max {config.max_session_id_length} characters)",
                field="session_id",
                value=session_id[:50] + "..." if len(session_id) > 50 else session_id,
            )

        if not SESSION_ID_PATTERN.match(session_id):
            raise ValidationError(
                "session_id must contain only alphanumeric characters, hyphens, and underscores",
                field="session_id",
                value=session_id,
            )

        return session_id

    @staticmethod
    def validate_git_ref(ref: str) -> str:
        """Validate git reference (commit hash, branch, tag, etc.).

        Args:
            ref: Git reference string

        Returns:
            Validated git ref

        Raises:
            ValidationError: If ref is invalid
        """
        if not ref:
            raise ValidationError(
                "git ref cannot be empty",
                field="ref",
            )

        if len(ref) > 1000:  # Git ref max reasonable length
            raise ValidationError(
                "git ref too long (max 1000 characters)",
                field="ref",
                value=ref[:100] + "...",
            )

        if not GIT_REF_PATTERN.match(ref):
            raise ValidationError(
                "git ref contains invalid characters",
                field="ref",
                value=ref[:100] + "..." if len(ref) > 100 else ref,
            )

        # Prevent potential command injection
        if any(char in ref for char in [';', '|', '&', '$', '`', '\n', '\r']):
            raise ValidationError(
                "git ref contains potentially dangerous characters",
                field="ref",
                value=ref[:100] + "..." if len(ref) > 100 else ref,
            )

        return ref

    @staticmethod
    def validate_limit(limit: int) -> int:
        """Validate limit parameter for pagination.

        Args:
            limit: Limit value

        Returns:
            Validated limit value

        Raises:
            ValidationError: If limit is out of range
        """
        config = _get_security_config()

        if not isinstance(limit, int):
            raise ValidationError(
                "limit must be an integer",
                field="limit",
            )

        if limit < config.min_limit:
            raise ValidationError(
                f"limit must be at least {config.min_limit}",
                field="limit",
                value=str(limit),
            )

        if limit > config.max_limit:
            raise ValidationError(
                f"limit must be at most {config.max_limit}",
                field="limit",
                value=str(limit),
            )

        return limit

    @staticmethod
    def validate_string_length(value: str, field_name: str = "value") -> str:
        """Validate string length against maximum.

        Args:
            value: String to validate
            field_name: Name of the field for error messages

        Returns:
            Validated string

        Raises:
            ValidationError: If string is too long
        """
        config = _get_security_config()

        if len(value) > config.max_string_length:
            raise ValidationError(
                f"{field_name} too long (max {config.max_string_length} characters)",
                field=field_name,
                value=value[:100] + "..." if len(value) > 100 else value,
            )

        return value

    @staticmethod
    def validate_path_safe(root: str, base_path: Optional[Path] = None) -> Path:
        """Validate path is safe and within allowed boundaries.

        Args:
            root: Path string to validate
            base_path: Allowed base directory (default from GCC_DATA_ROOT)

        Returns:
            Resolved, validated Path

        Raises:
            ValidationError: If path is unsafe
        """
        config = _get_security_config()

        # Determine allowed base path
        if base_path is None:
            env_base = os.environ.get("GCC_DATA_ROOT", "/data")
            base_path = Path(env_base).resolve()

        # Expand and resolve the path
        try:
            path = Path(root).expanduser().resolve()
        except (OSError, ValueError) as e:
            raise ValidationError(
                f"invalid path: {e}",
                field="root",
                value=root,
            )

        # Check if path is within allowed boundaries
        # Skip check in test mode or if traversal is explicitly allowed
        if not config.allow_path_traversal:
            # Also skip if GCC_DATA_ROOT is not set (direct mode)
            if os.environ.get("GCC_DATA_ROOT"):
                try:
                    path.relative_to(base_path)
                except ValueError:
                    raise ValidationError(
                        f"path is outside allowed directory",
                        field="root",
                        value=str(path),
                    )

        return path

    @staticmethod
    def validate_purpose(purpose: str) -> str:
        """Validate branch purpose string.

        Args:
            purpose: Purpose description

        Returns:
            Validated purpose string

        Raises:
            ValidationError: If purpose is invalid
        """
        if not purpose:
            raise ValidationError(
                "purpose cannot be empty",
                field="purpose",
            )

        return Validators.validate_string_length(purpose, "purpose")

    @staticmethod
    def validate_contribution(contribution: str) -> str:
        """Validate commit contribution string.

        Args:
            contribution: Contribution text

        Returns:
            Validated contribution string

        Raises:
            ValidationError: If contribution is invalid
        """
        if not contribution:
            raise ValidationError(
                "contribution cannot be empty",
                field="contribution",
            )

        return Validators.validate_string_length(contribution, "contribution")

    @staticmethod
    def validate_reset_mode(mode: str) -> str:
        """Validate git reset mode.

        Args:
            mode: Reset mode string

        Returns:
            Validated mode

        Raises:
            ValidationError: If mode is invalid
        """
        if mode not in ("soft", "hard", "mixed"):
            raise ValidationError(
                "reset mode must be 'soft', 'hard', or 'mixed'",
                field="mode",
                value=mode,
            )

        return mode

    @staticmethod
    def sanitize_log_entry(entry: str) -> str:
        """Sanitize log entry to prevent injection.

        Args:
            entry: Log entry string

        Returns:
            Sanitized entry
        """
        # Remove potential control characters
        # Keep newlines and tabs but remove other control chars
        sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', entry)

        # Limit length
        config = _get_security_config()
        if len(sanitized) > config.max_string_length:
            sanitized = sanitized[:config.max_string_length]

        return sanitized
