"""Exception hierarchy for GCC system.

This module defines all custom exceptions used throughout the GCC system,
providing clear error categorization for proper error handling.
"""
from __future__ import annotations


class GCCError(Exception):
    """Base exception for all GCC-related errors.

    All custom exceptions in the GCC system inherit from this class,
    allowing catch-all error handling when needed.
    """

    def __init__(self, message: str, details: dict | None = None) -> None:
        """Initialize a GCC error.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return the error message."""
        return self.message

    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses.

        Returns:
            Dictionary with error type and message
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(GCCError):
    """Input validation failed.

    Raised when user input does not meet validation requirements,
    such as invalid format, length constraints, or disallowed characters.
    """

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value: str | None = None,
    ) -> None:
        """Initialize a validation error.

        Args:
            message: Description of what failed validation
            field: Name of the field that failed validation
            value: The invalid value (may be omitted for security)
        """
        details = {}
        if field:
            details["field"] = field
        if value is not None:
            details["value"] = value
        super().__init__(message, details)


class RepositoryError(GCCError):
    """Git repository operation failed.

    Raised when git commands fail or repository state is invalid.
    """

    def __init__(
        self,
        message: str,
        repo_path: str | None = None,
        git_error: str | None = None,
    ) -> None:
        """Initialize a repository error.

        Args:
            message: Description of the repository error
            repo_path: Path to the repository
            git_error: Raw error output from git command
        """
        details = {}
        if repo_path:
            details["repo_path"] = repo_path
        if git_error:
            details["git_error"] = git_error
        super().__init__(message, details)


class StorageError(GCCError):
    """File system or storage operation failed.

    Raised when file I/O, path operations, or data storage fails.
    """

    def __init__(
        self,
        message: str,
        path: str | None = None,
        io_error: str | None = None,
    ) -> None:
        """Initialize a storage error.

        Args:
            message: Description of the storage error
            path: Path related to the error
            io_error: Underlying I/O error message
        """
        details = {}
        if path:
            details["path"] = path
        if io_error:
            details["io_error"] = io_error
        super().__init__(message, details)


class BranchNotFoundError(RepositoryError):
    """Requested git branch does not exist.

    Raised when attempting to access a branch that hasn't been created.
    """

    def __init__(self, branch: str, available: list[str] | None = None) -> None:
        """Initialize a branch not found error.

        Args:
            branch: Name of the branch that was not found
            available: List of available branch names
        """
        details = {"branch": branch}
        if available:
            details["available_branches"] = available
        super().__init__(f"Branch not found: {branch}", details=details)


class SessionNotFoundError(GCCError):
    """Requested session does not exist.

    Raised when attempting to access a session that hasn't been initialized.
    """

    def __init__(self, session_id: str) -> None:
        """Initialize a session not found error.

        Args:
            session_id: The session ID that was not found
        """
        super().__init__(f"Session not found: {session_id}", details={"session_id": session_id})


class LockError(GCCError):
    """File locking operation failed.

    Raised when unable to acquire or release a file lock.
    """

    def __init__(self, message: str, lock_path: str | None = None) -> None:
        """Initialize a lock error.

        Args:
            message: Description of the locking error
            lock_path: Path to the lock file
        """
        details = {}
        if lock_path:
            details["lock_path"] = lock_path
        super().__init__(message, details)


class ConflictError(GCCError):
    """Operation conflict with concurrent changes.

    Raised when an operation cannot complete due to conflicting state.
    """

    def __init__(self, message: str, conflict_type: str | None = None) -> None:
        """Initialize a conflict error.

        Args:
            message: Description of the conflict
            conflict_type: Type of conflict (merge, lock, etc.)
        """
        details = {}
        if conflict_type:
            details["conflict_type"] = conflict_type
        super().__init__(message, details)


class RateLimitError(GCCError):
    """Rate limit exceeded.

    Raised when a client exceeds configured request rate limits.
    """

    def __init__(self, limit: int, window: int = 60) -> None:
        """Initialize a rate limit error.

        Args:
            limit: Maximum number of requests allowed
            window: Time window in seconds
        """
        super().__init__(
            f"Rate limit exceeded: {limit} requests per {window} seconds",
            details={"limit": limit, "window": window},
        )
