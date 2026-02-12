"""Git operations for GCC memory system.

Provides wrapper functions for git commands used throughout the system.
Improves error handling, logging, and validation over direct git calls.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Iterable, List, Optional

from .exceptions import RepositoryError


def _get_git_config():
    """Get git configuration from global config.

    Returns:
        GitConfig instance with default name and email
    """
    try:
        from ..server.config import get_config
        config = get_config()
        return config.git
    except Exception:
        # Fallback if config not initialized
        class GitConfig:
            default_name = "gcc"
            default_email = "gcc@localhost"
            default_branch = "main"
        return GitConfig()


def _log_path(repo_root: Path) -> Path:
    """Get path to git operation log file.

    Args:
        repo_root: Git repository root directory

    Returns:
        Path to git.log file
    """
    return repo_root / "git.log"


def _append_git_log(repo_root: Path, args: List[str], result: subprocess.CompletedProcess) -> None:
    """Append git operation to log file.

    Args:
        repo_root: Git repository root directory
        args: Git command arguments
        result: Completed process result

    Note:
        Failures in logging are silently ignored to avoid disrupting
        the main operation flow.
    """
    try:
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        lines = [
            f"[{timestamp}] git {' '.join(args)}",
            f"exit={result.returncode}",
        ]
        if result.stdout:
            lines.append("stdout:")
            lines.append(result.stdout.rstrip())
        if result.stderr:
            lines.append("stderr:")
            lines.append(result.stderr.rstrip())
        lines.append("")

        _log_path(repo_root).parent.mkdir(parents=True, exist_ok=True)

        # Add retry mechanism for robustness
        for attempt in range(3):
            try:
                with _log_path(repo_root).open("a", encoding="utf-8") as handle:
                    handle.write("\n".join(lines) + "\n")
                break
            except (IOError, OSError) as e:
                if attempt == 2:
                    # Last attempt failed, log to stderr
                    import sys
                    print(f"Failed to write git log: {e}", file=sys.stderr)
                import time
                time.sleep(0.1 * (attempt + 1))
    except Exception as e:
        # Log but don't raise - logging failure shouldn't break operations
        import sys
        print(f"Error in _append_git_log: {e}", file=sys.stderr)


def _run_git(args: List[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run git command and raise on error.

    Args:
        args: Git command arguments (without 'git' prefix)
        cwd: Working directory for command

    Returns:
        Completed process result

    Raises:
        RepositoryError: If git command fails
    """
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            check=True,
            capture_output=True,
            text=True,
        )
        _append_git_log(cwd, args, result)
        return result
    except subprocess.CalledProcessError as exc:
        _append_git_log(cwd, args, exc)
        raise RepositoryError(
            f"Git command failed: git {' '.join(args)}",
            repo_path=str(cwd),
            git_error=exc.stderr or exc.stdout or str(exc),
        ) from exc
    except FileNotFoundError as e:
        raise RepositoryError(
            f"Git not found: {e}",
            repo_path=str(cwd),
        ) from e
    except Exception as e:
        raise RepositoryError(
            f"Unexpected error running git: {e}",
            repo_path=str(cwd),
        ) from e


def _try_git(args: List[str], cwd: Path) -> Optional[str]:
    """Run git command and return None on error.

    Args:
        args: Git command arguments (without 'git' prefix)
        cwd: Working directory for command

    Returns:
        Command stdout if successful, None otherwise
    """
    try:
        result = _run_git(args, cwd)
        return result.stdout.strip()
    except RepositoryError:
        return None


def ensure_repo(repo_root: Path) -> None:
    """Ensure git repository exists and is configured.

    Initializes repository if needed, configures user identity,
    and ensures at least one commit exists.

    Args:
        repo_root: Path where repository should exist

    Raises:
        RepositoryError: If initialization fails
    """
    try:
        repo_root.mkdir(parents=True, exist_ok=True)
        if not (repo_root / ".git").exists():
            git_config = _get_git_config()
            _run_git(["init", "-b", git_config.default_branch], repo_root)
        _ensure_identity(repo_root)
        _ensure_initial_commit(repo_root)
    except OSError as e:
        raise RepositoryError(
            f"Failed to create repository directory: {e}",
            repo_path=str(repo_root),
        ) from e


def _ensure_identity(repo_root: Path) -> None:
    """Ensure git user identity is configured.

    Args:
        repo_root: Git repository path

    Raises:
        RepositoryError: If configuration fails
    """
    git_config = _get_git_config()
    name = _try_git(["config", "--get", "user.name"], repo_root)
    email = _try_git(["config", "--get", "user.email"], repo_root)

    if not name:
        _run_git(["config", "user.name", git_config.default_name], repo_root)
    if not email:
        _run_git(["config", "user.email", git_config.default_email], repo_root)


def _ensure_initial_commit(repo_root: Path) -> None:
    """Ensure repository has at least one commit.

    Args:
        repo_root: Git repository path

    Raises:
        RepositoryError: If commit creation fails
    """
    head = _try_git(["rev-parse", "--verify", "HEAD"], repo_root)
    if head:
        return
    _run_git(["add", "-A"], repo_root)
    _run_git(["commit", "--allow-empty", "-m", "GCC init"], repo_root)


def current_branch(repo_root: Path) -> str:
    """Get current branch name.

    Args:
        repo_root: Git repository path

    Returns:
        Current branch name

    Raises:
        RepositoryError: If git command fails
    """
    try:
        name = _run_git(["rev-parse", "--abbrev-ref", "HEAD"], repo_root).stdout.strip()
        return name or _get_git_config().default_branch
    except RepositoryError:
        return _get_git_config().default_branch


def checkout_branch(repo_root: Path, branch: str) -> None:
    """Checkout or create a branch.

    Args:
        repo_root: Git repository path
        branch: Branch name to checkout

    Raises:
        RepositoryError: If checkout fails
    """
    # Basic validation (full validation done in validators module)
    if not branch:
        raise RepositoryError("Branch name cannot be empty")
    _run_git(["checkout", "-B", branch], repo_root)


def add_and_commit(repo_root: Path, paths: Iterable[Path], message: str) -> None:
    """Add files and create commit.

    Args:
        repo_root: Git repository path
        paths: Paths to add (relative to repo_root)
        message: Commit message

    Raises:
        RepositoryError: If add or commit fails
    """
    try:
        rel_paths = []
        for p in paths:
            try:
                rel_paths.append(str(p.relative_to(repo_root)))
            except ValueError as e:
                raise RepositoryError(
                    f"Path {p} is not under repository root {repo_root}",
                    repo_path=str(repo_root),
                ) from e

        if not rel_paths:
            return

        _run_git(["add", *rel_paths], repo_root)
        if _try_git(["diff", "--cached", "--quiet"], repo_root) is None:
            _run_git(["commit", "-m", message], repo_root)
    except RepositoryError:
        raise
    except Exception as e:
        raise RepositoryError(
            f"Unexpected error in add_and_commit: {e}",
            repo_path=str(repo_root),
        ) from e


def merge_branch(repo_root: Path, source: str, message: str) -> None:
    """Merge a branch into current branch.

    Args:
        repo_root: Git repository path
        source: Source branch name
        message: Merge commit message

    Raises:
        RepositoryError: If merge fails
    """
    _run_git(["merge", "--no-ff", source, "-m", message], repo_root)


def git_log(repo_root: Path, limit: int = 20) -> List[dict]:
    """Get commit history.

    Args:
        repo_root: Git repository path
        limit: Maximum number of commits to return

    Returns:
        List of commit dictionaries with hash, timestamp, subject

    Raises:
        RepositoryError: If log command fails
    """
    try:
        # Validate limit bounds
        limit = max(1, min(limit, 10000))
        result = _run_git(
            ["log", f"-n{limit}", "--pretty=format:%H|%ct|%s"],
            repo_root,
        )
        entries = []
        for line in result.stdout.splitlines():
            parts = line.split("|", 2)
            if len(parts) != 3:
                continue
            try:
                entries.append({
                    "hash": parts[0],
                    "timestamp": int(parts[1]),
                    "subject": parts[2]
                })
            except ValueError:
                # Skip entries with invalid timestamp
                continue
        return entries
    except RepositoryError:
        raise
    except Exception as e:
        raise RepositoryError(
            f"Failed to parse git log: {e}",
            repo_path=str(repo_root),
        ) from e


def git_diff(repo_root: Path, from_ref: str, to_ref: Optional[str]) -> str:
    """Get diff between two refs.

    Args:
        repo_root: Git repository path
        from_ref: Source ref
        to_ref: Target ref (None for working tree diff)

    Returns:
        Diff output

    Raises:
        RepositoryError: If diff command fails
    """
    if to_ref:
        args = ["diff", f"{from_ref}..{to_ref}"]
    else:
        args = ["diff", from_ref]
    return _run_git(args, repo_root).stdout


def git_show(repo_root: Path, ref: str, path: Optional[str]) -> str:
    """Show file content at ref.

    Args:
        repo_root: Git repository path
        ref: Git ref (commit, branch, tag, etc.)
        path: Optional path to specific file

    Returns:
        File content

    Raises:
        RepositoryError: If show command fails
    """
    if path:
        return _run_git(["show", f"{ref}:{path}"], repo_root).stdout
    return _run_git(["show", ref], repo_root).stdout


def git_reset(repo_root: Path, ref: str, mode: str) -> None:
    """Reset repository to ref.

    Args:
        repo_root: Git repository path
        ref: Git ref to reset to
        mode: Reset mode ('soft' or 'hard')

    Raises:
        RepositoryError: If reset command fails
        ValueError: If mode is invalid
    """
    if mode not in {"soft", "hard"}:
        raise ValueError(f"reset mode must be 'soft' or 'hard', got: {mode}")
    _run_git(["reset", f"--{mode}", ref], repo_root)
