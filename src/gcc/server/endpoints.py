"""API endpoints for GCC FastAPI server.

Provides all HTTP endpoints for GCC memory operations.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from ..core import commands


# Request/Response Models
DEFAULT_DATA_ROOT = "/data"

class StrictRequestModel(BaseModel):
    """Base request model that rejects unknown fields."""

    model_config = ConfigDict(extra="forbid")


class InitRequest(StrictRequestModel):
    """Request model for session initialization."""
    goal: Optional[str] = Field(None, description="Session goal", max_length=10000)
    todo: Optional[List[str]] = Field(None, description="Todo items")
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class BranchRequest(StrictRequestModel):
    """Request model for branch creation."""
    branch: str = Field(..., description="Branch name", max_length=100)
    purpose: str = Field(..., description="Branch purpose", max_length=10000)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class LogRequest(StrictRequestModel):
    """Request model for log appending."""
    branch: str = Field(..., description="Branch name", max_length=100)
    entries: List[str] = Field(..., description="Log entries to append")
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class CommitRequest(StrictRequestModel):
    """Request model for commit creation."""
    branch: str = Field(..., description="Branch name", max_length=100)
    contribution: str = Field(..., description="Commit contribution", min_length=1, max_length=10000)
    purpose: Optional[str] = Field(None, description="Branch purpose", max_length=10000)
    log_entries: Optional[List[str]] = Field(None, description="Log entries")
    metadata_updates: Optional[Dict[str, Any]] = Field(None, description="Metadata updates")
    update_main: Optional[str] = Field(None, description="Text to append to main.md", max_length=10000)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class MergeRequest(StrictRequestModel):
    """Request model for branch merging."""
    source_branch: str = Field(..., description="Source branch name", max_length=100)
    target_branch: Optional[str] = Field(None, description="Target branch name", max_length=100)
    summary: Optional[str] = Field(None, description="Merge summary", max_length=10000)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class ContextRequest(StrictRequestModel):
    """Request model for context retrieval."""
    branch: Optional[str] = Field(None, description="Branch name", max_length=100)
    commit_id: Optional[str] = Field(None, description="Commit ID", max_length=100)
    log_tail: Optional[int] = Field(None, description="Number of log lines", ge=1, le=10000)
    metadata_segment: Optional[str] = Field(None, description="Metadata key", max_length=100)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class HistoryRequest(StrictRequestModel):
    """Request model for history retrieval."""
    limit: int = Field(20, description="Maximum commits to return", ge=1, le=1000)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class DiffRequest(StrictRequestModel):
    """Request model for diff retrieval."""
    from_ref: str = Field(..., description="Source ref", max_length=1000)
    to_ref: Optional[str] = Field(None, description="Target ref", max_length=1000)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class ShowRequest(StrictRequestModel):
    """Request model for file content retrieval."""
    ref: str = Field(..., description="Git ref", max_length=1000)
    path: Optional[str] = Field(None, description="File path", max_length=1000)
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


class ResetRequest(StrictRequestModel):
    """Request model for repository reset."""
    ref: str = Field(..., description="Git ref to reset to", max_length=1000)
    mode: str = Field("soft", description="Reset mode (soft/hard)")
    confirm: bool = Field(False, description="Confirm hard reset")
    session_id: Optional[str] = Field(None, description="Session identifier", max_length=100)


# Path resolution helper

def _resolve_path(session_id: Optional[str]) -> Path:
    """Resolve and validate project root path.

    Args:
        session_id: Session identifier (unused here, kept for call compatibility)

    Returns:
        Data root path used by storage layer

    Raises:
        ValidationError: If resolved path is unsafe

    Note:
        - Container mode data root defaults to /data
        - Session-specific layout is handled by storage layer
    """
    from ..core.validators import Validators

    base = os.environ.get("GCC_DATA_ROOT", DEFAULT_DATA_ROOT)
    base_path = Path(base).resolve()
    Validators.validate_path_safe(str(base_path), base_path)
    return base_path


# API Router

router = APIRouter()


@router.post("/init", tags=["sessions"])
def init(req: InitRequest) -> Dict[str, Any]:
    """Initialize a new GCC session.

    Creates directory structure, initializes git repository,
    and sets up main.md with goal and todo.

    - **root**: Project root directory path
    - **goal**: Optional session goal description
    - **todo**: Optional list of todo items
    - **session_id**: Optional session identifier

    Returns initialization status and paths.
    """
    return commands.init(
        _resolve_path(req.session_id),
        req.goal,
        req.todo,
        req.session_id,
    )


@router.post("/branch", tags=["branches"])
def create_branch(req: BranchRequest) -> Dict[str, Any]:
    """Create a new memory branch.

    Creates a git branch with tracking files for
    isolated exploration and memory storage.

    - **root**: Project root directory path
    - **branch**: Branch name
    - **purpose**: Branch purpose description
    - **session_id**: Optional session identifier

    Returns branch creation status.
    """
    return commands.branch(
        _resolve_path(req.session_id),
        req.branch,
        req.purpose,
        req.session_id,
    )


@router.post("/log", tags=["logs"])
def append_log(req: LogRequest) -> Dict[str, Any]:
    """Append log entries to a branch.

    Adds timestamped log entries and creates a git commit.

    - **root**: Project root directory path
    - **branch**: Branch name
    - **entries**: List of log entry strings
    - **session_id**: Optional session identifier

    Returns log operation status.
    """
    return commands.log(
        _resolve_path(req.session_id),
        req.branch,
        req.entries,
        req.session_id,
    )


@router.post("/commit", tags=["commits"])
def commit(req: CommitRequest) -> Dict[str, Any]:
    """Create a memory checkpoint.

    Records contribution with optional updates to logs,
    metadata, and main.md.

    - **root**: Project root directory path
    - **branch**: Branch name
    - **contribution**: Contribution description
    - **purpose**: Optional branch purpose (for new branches)
    - **log_entries**: Optional log entries to append
    - **metadata_updates**: Optional metadata updates
    - **update_main**: Optional text for main.md
    - **session_id**: Optional session identifier

    Returns commit creation status with commit ID.
    """
    return commands.commit(
        _resolve_path(req.session_id),
        req.branch,
        req.contribution,
        req.purpose,
        req.log_entries,
        req.metadata_updates,
        req.update_main,
        req.session_id,
    )


@router.post("/merge", tags=["branches"])
def merge(req: MergeRequest) -> Dict[str, Any]:
    """Merge a source branch into target branch.

    Combines commits, logs, and metadata from both branches.

    - **root**: Project root directory path
    - **source_branch**: Source branch name
    - **target_branch**: Optional target branch (default: main)
    - **summary**: Optional merge summary
    - **session_id**: Optional session identifier

    Returns merge operation status.
    """
    return commands.merge(
        _resolve_path(req.session_id),
        req.source_branch,
        req.target_branch,
        req.summary,
        req.session_id,
    )


@router.post("/context", tags=["context"])
def context(req: ContextRequest) -> Dict[str, Any]:
    """Retrieve structured context information.

    Returns main.md, branches list, and optional branch-specific info.

    - **root**: Project root directory path
    - **branch**: Optional branch name for detailed info
    - **commit_id**: Optional commit ID to retrieve
    - **log_tail**: Optional number of log lines
    - **metadata_segment**: Optional metadata key
    - **session_id**: Optional session identifier

    Returns context dictionary with requested information.
    """
    return commands.context(
        _resolve_path(req.session_id),
        req.branch,
        req.commit_id,
        req.log_tail,
        req.metadata_segment,
        req.session_id,
    )


@router.post("/history", tags=["history"])
def history(req: HistoryRequest) -> Dict[str, Any]:
    """Get git commit history.

    Returns list of git commits with metadata.

    - **root**: Project root directory path
    - **limit**: Maximum number of commits (default: 20)
    - **session_id**: Optional session identifier

    Returns list of commits.
    """
    return commands.history(
        _resolve_path(req.session_id),
        req.limit,
        req.session_id,
    )


@router.post("/diff", tags=["history"])
def diff(req: DiffRequest) -> Dict[str, Any]:
    """Get git diff between two refs.

    Returns unified diff output.

    - **root**: Project root directory path
    - **from_ref**: Source ref
    - **to_ref**: Optional target ref
    - **session_id**: Optional session identifier

    Returns diff output string.
    """
    return commands.diff(
        _resolve_path(req.session_id),
        req.from_ref,
        req.to_ref,
        req.session_id,
    )


@router.post("/show", tags=["history"])
def show(req: ShowRequest) -> Dict[str, Any]:
    """Show file content at a git ref.

    Returns file content from git history.

    - **root**: Project root directory path
    - **ref**: Git ref (commit, branch, etc.)
    - **path**: Optional file path
    - **session_id**: Optional session identifier

    Returns file content string.
    """
    return commands.show(
        _resolve_path(req.session_id),
        req.ref,
        req.path,
        req.session_id,
    )


@router.post("/reset", tags=["history"])
def reset(req: ResetRequest) -> Dict[str, Any]:
    """Reset repository to a git ref.

    Resets git HEAD to specified ref.

    - **root**: Project root directory path
    - **ref**: Git ref to reset to
    - **mode**: Reset mode (soft/hard)
    - **confirm**: Must be true for hard reset
    - **session_id**: Optional session identifier

    Returns reset operation status.
    """
    return commands.reset(
        _resolve_path(req.session_id),
        req.ref,
        req.mode,
        req.confirm,
        req.session_id,
    )
