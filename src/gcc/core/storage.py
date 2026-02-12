"""Storage operations for GCC memory system.

This module handles file system operations for storing GCC data,
including sessions, branches, commits, logs, and metadata.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .exceptions import StorageError


# Constants
COMMIT_SEPARATOR = "=== Commit ==="
DEFAULT_SESSION = "default"


def normalize_session_id(session_id: Optional[str]) -> str:
    """Normalize and validate session ID.

    Args:
        session_id: Session identifier from user input

    Returns:
        Normalized session ID (or "default" if empty)

    Raises:
        StorageError: If session_id contains invalid characters
    """
    if not session_id:
        return DEFAULT_SESSION
    if not re.match(r"^[A-Za-z0-9_-]+$", session_id):
        raise StorageError(
            "session_id must be alphanumeric with optional '-' or '_' only",
            field="session_id",
            value=session_id,
        )
    return session_id


def _now_iso() -> str:
    """Get current UTC timestamp in ISO format.

    Returns:
        ISO 8601 formatted timestamp
    """
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


# Path helper functions

def gcc_root(root: Path) -> Path:
    """Get GCC root directory path.

    Args:
        root: Project root directory

    Returns:
        Path to .GCC directory
    """
    return root / ".GCC"


def session_root(root: Path, session_id: str) -> Path:
    """Get session directory path.

    Args:
        root: Project root directory
        session_id: Session identifier

    Returns:
        Path to session directory
    """
    return gcc_root(root) / "sessions" / session_id


def branches_root(root: Path, session_id: str) -> Path:
    """Get branches directory path for a session.

    Args:
        root: Project root directory
        session_id: Session identifier

    Returns:
        Path to branches directory
    """
    return session_root(root, session_id) / "branches"


def branch_root(root: Path, session_id: str, branch: str) -> Path:
    """Get specific branch directory path.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name

    Returns:
        Path to branch directory
    """
    return branches_root(root, session_id) / branch


def main_path(root: Path, session_id: str) -> Path:
    """Get path to main.md file.

    Args:
        root: Project root directory
        session_id: Session identifier

    Returns:
        Path to main.md file
    """
    return session_root(root, session_id) / "main.md"


def commit_path(root: Path, session_id: str, branch: str) -> Path:
    """Get path to commit.md file for a branch.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name

    Returns:
        Path to commit.md file
    """
    return branch_root(root, session_id, branch) / "commit.md"


def log_path(root: Path, session_id: str, branch: str) -> Path:
    """Get path to log.md file for a branch.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name

    Returns:
        Path to log.md file
    """
    return branch_root(root, session_id, branch) / "log.md"


def metadata_path(root: Path, session_id: str, branch: str) -> Path:
    """Get path to metadata.yaml file for a branch.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name

    Returns:
        Path to metadata.yaml file
    """
    return branch_root(root, session_id, branch) / "metadata.yaml"


# File I/O helper functions

def _write_text(path: Path, content: str) -> None:
    """Atomically write text to a file.

    Uses temp file + rename pattern to ensure atomic writes.

    Args:
        path: Target file path
        content: Content to write

    Raises:
        StorageError: If write operation fails
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(content, encoding="utf-8")
        tmp.replace(path)
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to write file: {e}", path=str(path), io_error=str(e))


def _append_text(path: Path, content: str) -> None:
    """Append text to a file.

    Args:
        path: Target file path
        content: Content to append

    Raises:
        StorageError: If append operation fails
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(content)
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to append to file: {e}", path=str(path), io_error=str(e))


# Directory structure management

def ensure_gcc(root: Path, goal: Optional[str], todo: Optional[List[str]], session_id: str) -> None:
    """Ensure GCC directory structure exists.

    Creates necessary directories and initializes main.md if needed.

    Args:
        root: Project root directory
        goal: Session goal description
        todo: List of todo items
        session_id: Session identifier

    Raises:
        StorageError: If directory creation fails
    """
    try:
        gcc_root(root).mkdir(parents=True, exist_ok=True)
        session_root(root, session_id).mkdir(parents=True, exist_ok=True)
        branches_root(root, session_id).mkdir(parents=True, exist_ok=True)
        if not main_path(root, session_id).exists():
            lines = ["# GCC Roadmap", "", "## Goal", goal or "(unset)", "", "## Todo"]
            if todo:
                lines.extend([f"- {item}" for item in todo])
            else:
                lines.append("- (none)")
            _write_text(main_path(root, session_id), "\n".join(lines) + "\n")
    except OSError as e:
        raise StorageError(f"Failed to create GCC directories: {e}", io_error=str(e))


def ensure_branch(root: Path, session_id: str, branch: str, purpose: str) -> None:
    """Ensure branch directory structure exists.

    Creates branch directory and initializes files if needed.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name
        purpose: Branch purpose description

    Raises:
        StorageError: If directory creation fails
    """
    try:
        b_root = branch_root(root, session_id, branch)
        b_root.mkdir(parents=True, exist_ok=True)
        if not commit_path(root, session_id, branch).exists():
            header = [f"# Branch: {branch}", f"# Purpose: {purpose}", ""]
            _write_text(commit_path(root, session_id, branch), "\n".join(header) + "\n")
        log_path(root, session_id, branch).touch(exist_ok=True)
        if not metadata_path(root, session_id, branch).exists():
            _write_text(
                metadata_path(root, session_id, branch),
                yaml.safe_dump({"file_structure": {}, "env_config": {}}),
            )
    except OSError as e:
        raise StorageError(f"Failed to create branch directories: {e}", branch=branch, io_error=str(e))


def list_branches(root: Path, session_id: str) -> List[str]:
    """List all branches for a session.

    Args:
        root: Project root directory
        session_id: Session identifier

    Returns:
        Sorted list of branch names
    """
    if not branches_root(root, session_id).exists():
        return []
    return sorted([p.name for p in branches_root(root, session_id).iterdir() if p.is_dir()])


# Main file operations

def read_main(root: Path, session_id: str) -> str:
    """Read main.md content.

    Args:
        root: Project root directory
        session_id: Session identifier

    Returns:
        Content of main.md, or empty string if not exists

    Raises:
        StorageError: If read operation fails
    """
    if not main_path(root, session_id).exists():
        return ""
    try:
        return main_path(root, session_id).read_text(encoding="utf-8")
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to read main.md: {e}", path=str(main_path(root, session_id)), io_error=str(e))


def update_main(root: Path, session_id: str, update_text: str) -> None:
    """Update main.md with new content.

    Args:
        root: Project root directory
        session_id: Session identifier
        update_text: Text to append

    Raises:
        StorageError: If write operation fails
    """
    content = read_main(root, session_id)
    if content:
        content = content.rstrip() + "\n\n" + update_text.strip() + "\n"
    else:
        content = update_text.strip() + "\n"
    _write_text(main_path(root, session_id), content)


# Log operations

def append_log(root: Path, session_id: str, branch: str, entries: List[str]) -> None:
    """Append log entries to branch log.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name
        entries: List of log entry strings

    Raises:
        StorageError: If append operation fails
    """
    if not entries:
        return
    timestamp = _now_iso()
    block = [f"[{timestamp}]"] + [f"- {item}" for item in entries] + [""]
    _append_text(log_path(root, session_id, branch), "\n".join(block))


def read_log_tail(root: Path, session_id: str, branch: str, tail: int) -> List[str]:
    """Read last N lines from branch log.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name
        tail: Number of lines to read

    Returns:
        List of log lines

    Raises:
        StorageError: If read operation fails
    """
    if not log_path(root, session_id, branch).exists():
        return []
    try:
        lines = log_path(root, session_id, branch).read_text(encoding="utf-8").splitlines()
        if tail <= 0:
            return []
        return lines[-tail:]
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to read log.md: {e}", path=str(log_path(root, session_id, branch)), io_error=str(e))


# Commit operations

def _parse_commits(text: str) -> List[Dict[str, str]]:
    """Parse commit entries from commit.md text.

    Args:
        text: Content of commit.md

    Returns:
        List of commit entry dictionaries
    """
    commits: List[Dict[str, str]] = []
    if COMMIT_SEPARATOR not in text:
        return commits
    parts = text.split(COMMIT_SEPARATOR)
    for part in parts[1:]:
        entry = {}
        lines = [line.rstrip() for line in part.strip().splitlines()]
        current_key = None
        buffer: List[str] = []
        for line in lines:
            if line.startswith("Commit ID:"):
                entry["commit_id"] = line.split(":", 1)[1].strip()
            elif line.startswith("Timestamp:"):
                entry["timestamp"] = line.split(":", 1)[1].strip()
            elif line.endswith(":"):
                if current_key and buffer:
                    entry[current_key] = "\n".join(buffer).strip()
                current_key = line[:-1]
                buffer = []
            else:
                buffer.append(line)
        if current_key and buffer:
            entry[current_key] = "\n".join(buffer).strip()
        commits.append(entry)
    return commits


def get_branch_purpose(root: Path, session_id: str, branch: str) -> str:
    """Extract branch purpose from commit.md header.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name

    Returns:
        Branch purpose string, or empty if not found

    Raises:
        StorageError: If read operation fails
    """
    if not commit_path(root, session_id, branch).exists():
        return ""
    try:
        text = commit_path(root, session_id, branch).read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("# Purpose:"):
                return line.split(":", 1)[1].strip()
        return ""
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to read commit.md: {e}", path=str(commit_path(root, session_id, branch)), io_error=str(e))


def get_commit_entry(root: Path, session_id: str, branch: str, commit_id: str) -> Optional[str]:
    """Get specific commit entry by ID.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name
        commit_id: Commit ID to find

    Returns:
        Commit entry text, or None if not found

    Raises:
        StorageError: If read operation fails
    """
    if not commit_path(root, session_id, branch).exists():
        return None
    try:
        text = commit_path(root, session_id, branch).read_text(encoding="utf-8")
        if COMMIT_SEPARATOR not in text:
            return None
        parts = text.split(COMMIT_SEPARATOR)
        for part in parts[1:]:
            if f"Commit ID: {commit_id}" in part:
                return COMMIT_SEPARATOR + part
        return None
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to read commit.md: {e}", path=str(commit_path(root, session_id, branch)), io_error=str(e))


def append_commit(
    root: Path,
    session_id: str,
    branch: str,
    purpose: str,
    contribution: str,
) -> str:
    """Append a new commit entry to branch.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name
        purpose: Branch purpose
        contribution: Commit contribution text

    Returns:
        New commit ID

    Raises:
        StorageError: If read/write operations fail
    """
    commit_id = uuid.uuid4().hex[:8]
    try:
        existing = commit_path(root, session_id, branch).read_text(encoding="utf-8")
    except (IOError, OSError) as e:
        raise StorageError(f"Failed to read commit.md: {e}", path=str(commit_path(root, session_id, branch)), io_error=str(e))

    commits = _parse_commits(existing)
    if commits:
        prev_summary = commits[-1].get("Previous Progress Summary", "")
        last_contrib = commits[-1].get("This Commit's Contribution", "")
        combined = "\n".join([line for line in [prev_summary, last_contrib] if line]).strip()
    else:
        combined = ""
    prev_block = combined if combined else "(none)"

    entry_lines = [
        COMMIT_SEPARATOR,
        f"Commit ID: {commit_id}",
        f"Timestamp: {_now_iso()}",
        "Branch Purpose:",
        purpose,
        "Previous Progress Summary:",
        prev_block,
        "This Commit's Contribution:",
        contribution,
        "",
    ]
    _append_text(commit_path(root, session_id, branch), "\n".join(entry_lines))
    return commit_id


# Metadata operations

def read_metadata(root: Path, session_id: str, branch: str) -> Dict[str, Any]:
    """Read branch metadata.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name

    Returns:
        Metadata dictionary

    Raises:
        StorageError: If read/parse operations fail
    """
    if not metadata_path(root, session_id, branch).exists():
        return {}
    try:
        data = yaml.safe_load(metadata_path(root, session_id, branch).read_text(encoding="utf-8"))
        return data or {}
    except (yaml.YAMLError, IOError, OSError) as e:
        raise StorageError(f"Failed to read metadata.yaml: {e}", path=str(metadata_path(root, session_id, branch)), io_error=str(e))


def update_metadata(root: Path, session_id: str, branch: str, updates: Dict[str, Any]) -> None:
    """Update branch metadata.

    Args:
        root: Project root directory
        session_id: Session identifier
        branch: Branch name
        updates: Dictionary of metadata updates

    Raises:
        StorageError: If read/write/parse operations fail
    """
    data = read_metadata(root, session_id, branch)
    for key, value in updates.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value
    _write_text(metadata_path(root, session_id, branch), yaml.safe_dump(data, sort_keys=False))


# Locking

def with_lock(root: Path, session_id: str, func, *args, **kwargs):
    """Execute function with session lock held.

    Args:
        root: Project root directory
        session_id: Session identifier
        func: Function to execute
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func

    Returns:
        Return value of func

    Raises:
        LockError: If lock acquisition fails
        StorageError: If file operations fail
    """
    from .lock import file_lock

    lock_path = session_root(root, session_id) / ".lock"
    with file_lock(lock_path):
        return func(*args, **kwargs)
