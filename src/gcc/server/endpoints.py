"""API endpoints for GCC FastAPI server.

Provides all HTTP endpoints for GCC memory operations.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..core import commands
from ..core.storage import normalize_session_id


# Request/Response Models

class InitRequest(BaseModel):
    """Request model for session initialization."""
    root: str = Field(..., description="Project root path")
    goal: Optional[str] = Field(None, description="Session goal")
    todo: Optional[List[str]] = Field(None, description="Todo items")
    session_id: Optional[str] = Field(None, description="Session identifier")


class BranchRequest(BaseModel):
    """Request model for branch creation."""
    root: str = Field(..., description="Project root path")
    branch: str = Field(..., description="Branch name")
    purpose: str = Field(..., description="Branch purpose")
    session_id: Optional[str] = Field(None, description="Session identifier")


class LogRequest(BaseModel):
    """Request model for log appending."""
    root: str = Field(..., description="Project root path")
    branch: str = Field(..., description="Branch name")
    entries: List[str] = Field(..., description="Log entries to append")
    session_id: Optional[str] = Field(None, description="Session identifier")


class CommitRequest(BaseModel):
    """Request model for commit creation."""
    root: str = Field(..., description="Project root path")
    branch: str = Field(..., description="Branch name")
    contribution: str = Field(..., description="Commit contribution")
    purpose: Optional[str] = Field(None, description="Branch purpose")
    log_entries: Optional[List[str]] = Field(None, description="Log entries")
    metadata_updates: Optional[Dict[str, Any]] = Field(None, description="Metadata updates")
    update_main: Optional[str] = Field(None, description="Text to append to main.md")
    session_id: Optional[str] = Field(None, description="Session identifier")


class MergeRequest(BaseModel):
    """Request model for branch merging."""
    root: str = Field(..., description="Project root path")
    source_branch: str = Field(..., description="Source branch name")
    target_branch: Optional[str] = Field(None, description="Target branch name")
    summary: Optional[str] = Field(None, description="Merge summary")
    session_id: Optional[str] = Field(None, description="Session identifier")


class ContextRequest(BaseModel):
    """Request model for context retrieval."""
    root: str = Field(..., description="Project root path")
    branch: Optional[str] = Field(None, description="Branch name")
    commit_id: Optional[str] = Field(None, description="Commit ID")
    log_tail: Optional[int] = Field(None, description="Number of log lines")
    metadata_segment: Optional[str] = Field(None, description="Metadata key")
    session_id: Optional[str] = Field(None, description="Session identifier")


class HistoryRequest(BaseModel):
    """Request model for history retrieval."""
    root: str = Field(..., description="Project root path")
    limit: int = Field(20, description="Maximum commits to return")
    session_id: Optional[str] = Field(None, description="Session identifier")


class DiffRequest(BaseModel):
    """Request model for diff retrieval."""
    root: str = Field(..., description="Project root path")
    from_ref: str = Field(..., description="Source ref")
    to_ref: Optional[str] = Field(None, description="Target ref")
    session_id: Optional[str] = Field(None, description="Session identifier")


class ShowRequest(BaseModel):
    """Request model for file content retrieval."""
    root: str = Field(..., description="Project root path")
    ref: str = Field(..., description="Git ref")
    path: Optional[str] = Field(None, description="File path")
    session_id: Optional[str] = Field(None, description="Session identifier")


class ResetRequest(BaseModel):
    """Request model for repository reset."""
    root: str = Field(..., description="Project root path")
    ref: str = Field(..., description="Git ref to reset to")
    mode: str = Field("soft", description="Reset mode (soft/hard)")
    confirm: bool = Field(False, description="Confirm hard reset")
    session_id: Optional[str] = Field(None, description="Session identifier")


# Path resolution helper

def _resolve_path(root: str, session_id: Optional[str] = None) -> Path:
    """Resolve and validate project root path.

    Args:
        root: Project root path string
        session_id: Optional session identifier

    Returns:
        Resolved Path object

    Note:
        When GCC_DATA_ROOT env var is set, path is resolved under that directory
        with session_id subdirectory for container isolation.
    """
    base = os.environ.get("GCC_DATA_ROOT")
    if base:
        # Container mode: use session_id for isolation
        normalized_session = normalize_session_id(session_id)
        return (Path(base) / normalized_session).resolve()
    return Path(root).expanduser().resolve()


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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
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
        _resolve_path(req.root, req.session_id),
        req.ref,
        req.mode,
        req.confirm,
        req.session_id,
    )
