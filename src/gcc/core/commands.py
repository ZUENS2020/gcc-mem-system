"""High-level commands for GCC memory system.

This module provides the main API functions that combine storage,
git operations, and business logic for memory management.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from . import storage
from .exceptions import GCCError, BranchNotFoundError, ValidationError
from .git_ops import (
    add_and_commit,
    checkout_branch,
    ensure_repo,
    git_diff,
    git_log,
    git_reset,
    git_show,
    merge_branch,
)


def init(
    root: Path,
    goal: Optional[str],
    todo: Optional[List[str]],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Initialize a GCC memory session.

    Creates the directory structure, initializes git repository,
    and sets up main.md with goal and todo.

    Args:
        root: Project root directory
        goal: Session goal description
        todo: List of todo items
        session_id: Session identifier

    Returns:
        Dictionary with initialization results

    Raises:
        GCCError: If initialization fails
    """
    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, goal, todo, session)
        ensure_repo(storage.session_root(root, session))
        return {
            "gcc_root": str(storage.gcc_root(root)),
            "session": session,
            "main": str(storage.main_path(root, session)),
        }

    return storage.with_lock(root, session, _run)


def branch(
    root: Path,
    branch_name: str,
    purpose: str,
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Create a new memory branch.

    Creates a branch with git tracking and initializes
    commit.md, log.md, and metadata.yaml.

    Args:
        root: Project root directory
        branch_name: Name for the branch
        purpose: Purpose description for the branch
        session_id: Session identifier

    Returns:
        Dictionary with branch creation results

    Raises:
        ValidationError: If branch_name or purpose are empty
        GCCError: If branch creation fails
    """
    if not branch_name:
        raise ValidationError("branch name is required", field="branch")
    if not purpose:
        raise ValidationError("branch purpose is required", field="purpose")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)
        checkout_branch(repo_root, branch_name)
        storage.ensure_branch(root, session, branch_name, purpose)
        add_and_commit(
            repo_root,
            [
                storage.commit_path(root, session, branch_name),
                storage.log_path(root, session, branch_name),
                storage.metadata_path(root, session, branch_name),
            ],
            f"GCC branch {branch_name}",
        )
        return {"branch": branch_name, "purpose": purpose, "session": session}

    return storage.with_lock(root, session, _run)


def log(
    root: Path,
    branch_name: str,
    entries: List[str],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Append log entries to a branch.

    Adds timestamped log entries and creates a git commit.

    Args:
        root: Project root directory
        branch_name: Branch name
        entries: List of log entry strings
        session_id: Session identifier

    Returns:
        Dictionary with log operation results

    Raises:
        ValidationError: If branch_name is empty
        BranchNotFoundError: If branch doesn't exist
        GCCError: If operation fails
    """
    if not branch_name:
        raise ValidationError("branch name is required", field="branch")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)

        branches = storage.list_branches(root, session)
        if branch_name not in branches:
            raise BranchNotFoundError(branch_name, available=branches)

        checkout_branch(repo_root, branch_name)
        storage.append_log(root, session, branch_name, entries)
        add_and_commit(
            repo_root,
            [storage.log_path(root, session, branch_name)],
            f"GCC log {branch_name}",
        )
        return {"branch": branch_name, "entries": len(entries), "session": session}

    return storage.with_lock(root, session, _run)


def commit(
    root: Path,
    branch_name: str,
    contribution: str,
    purpose: Optional[str],
    log_entries: Optional[List[str]],
    metadata_updates: Optional[Dict[str, Any]],
    update_main_text: Optional[str],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Create a memory checkpoint commit.

    Records contribution with optional log entries, metadata updates,
    and main.md update.

    Args:
        root: Project root directory
        branch_name: Branch name
        contribution: Contribution description
        purpose: Branch purpose (required if creating new branch)
        log_entries: Optional log entries to append
        metadata_updates: Optional metadata updates
        update_main_text: Optional text to append to main.md
        session_id: Session identifier

    Returns:
        Dictionary with commit results

    Raises:
        ValidationError: If required fields are empty
        BranchNotFoundError: If branch doesn't exist and purpose not provided
        GCCError: If operation fails
    """
    if not branch_name:
        raise ValidationError("branch name is required", field="branch")
    if not contribution:
        raise ValidationError("contribution is required", field="contribution")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)

        branches = storage.list_branches(root, session)
        if branch_name not in branches:
            if not purpose:
                raise BranchNotFoundError(
                    branch_name,
                    available=branches,
                )
            storage.ensure_branch(root, session, branch_name, purpose)

        checkout_branch(repo_root, branch_name)
        branch_purpose = storage.get_branch_purpose(root, session, branch_name) or (purpose or "")

        if log_entries:
            storage.append_log(root, session, branch_name, log_entries)
        if metadata_updates:
            storage.update_metadata(root, session, branch_name, metadata_updates)

        commit_id = storage.append_commit(root, session, branch_name, branch_purpose, contribution)

        if update_main_text:
            storage.update_main(root, session, update_main_text)

        add_and_commit(
            repo_root,
            [
                storage.commit_path(root, session, branch_name),
                storage.log_path(root, session, branch_name),
                storage.metadata_path(root, session, branch_name),
                storage.main_path(root, session),
            ],
            f"GCC commit {branch_name}: {contribution[:60]}",
        )

        return {"branch": branch_name, "commit_id": commit_id, "session": session}

    return storage.with_lock(root, session, _run)


def merge(
    root: Path,
    source_branch: str,
    target_branch: Optional[str],
    summary: Optional[str],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Merge a source branch into target branch.

    Combines commits, logs, and metadata from source into target.

    Args:
        root: Project root directory
        source_branch: Source branch name
        target_branch: Target branch name (default: "main")
        summary: Merge summary description
        session_id: Session identifier

    Returns:
        Dictionary with merge results

    Raises:
        ValidationError: If source_branch is empty
        BranchNotFoundError: If source branch doesn't exist
        GCCError: If merge fails
    """
    if not source_branch:
        raise ValidationError("source_branch is required", field="source_branch")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)

        branches = storage.list_branches(root, session)
        if source_branch not in branches:
            raise BranchNotFoundError(source_branch, available=branches)

        target = target_branch or "main"
        if target not in branches:
            storage.ensure_branch(root, session, target, f"Main branch (merged from {source_branch})")

        checkout_branch(repo_root, target)

        # Merge commit history
        source_commit = storage.commit_path(root, session, source_branch).read_text(encoding="utf-8")
        storage._append_text(storage.commit_path(root, session, target), "\n" + source_commit)

        # Merge log history
        source_log = storage.log_path(root, session, source_branch).read_text(encoding="utf-8")
        log_block = f"\n== Merge from {source_branch} ==\n" + source_log + "\n"
        storage._append_text(storage.log_path(root, session, target), log_block)

        # Merge metadata
        source_meta = storage.read_metadata(root, session, source_branch)
        if source_meta:
            target_meta = storage.read_metadata(root, session, target)
            merged_from = target_meta.get("merged_from", {})
            merged_from[source_branch] = source_meta
            target_meta["merged_from"] = merged_from
            storage.update_metadata(root, session, target, target_meta)

        # Create git merge
        merge_note = summary or f"Merged branch {source_branch} into {target}"
        merge_branch(repo_root, source_branch, merge_note)
        storage.update_main(root, session, merge_note)

        add_and_commit(
            repo_root,
            [
                storage.commit_path(root, session, target),
                storage.log_path(root, session, target),
                storage.metadata_path(root, session, target),
                storage.main_path(root, session),
            ],
            f"GCC merge {source_branch} -> {target}",
        )

        return {"source_branch": source_branch, "target_branch": target, "session": session}

    return storage.with_lock(root, session, _run)


def context(
    root: Path,
    branch_name: Optional[str],
    commit_id: Optional[str],
    log_tail: Optional[int],
    metadata_segment: Optional[str],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Retrieve structured context information.

    Returns main.md, branches list, and optional branch-specific info.

    Args:
        root: Project root directory
        branch_name: Optional branch name for detailed info
        commit_id: Optional commit ID to retrieve
        log_tail: Optional number of log lines to return
        metadata_segment: Optional metadata key to retrieve
        session_id: Session identifier

    Returns:
        Dictionary with context information

    Raises:
        BranchNotFoundError: If branch_name specified but not found
        GCCError: If operation fails
    """
    session = storage.normalize_session_id(session_id)
    storage.ensure_gcc(root, None, None, session)

    result: Dict[str, Any] = {
        "main": storage.read_main(root, session),
        "branches": storage.list_branches(root, session),
        "session": session,
    }

    if branch_name:
        branches = storage.list_branches(root, session)
        if branch_name not in branches:
            raise BranchNotFoundError(branch_name, available=branches)

        commit_text = storage.commit_path(root, session, branch_name).read_text(encoding="utf-8")
        commits = storage._parse_commits(commit_text)
        last_commit = commits[-1] if commits else {}
        result["branch"] = {
            "name": branch_name,
            "purpose": storage.get_branch_purpose(root, session, branch_name),
            "latest_commit": last_commit.get("commit_id"),
            "latest_summary": last_commit.get("This Commit's Contribution"),
            "recent_commits": [c.get("commit_id") for c in commits[-10:]],
        }

    if commit_id and branch_name:
        result["commit_entry"] = storage.get_commit_entry(root, session, branch_name, commit_id)

    if log_tail and branch_name:
        result["log_tail"] = storage.read_log_tail(root, session, branch_name, log_tail)

    if metadata_segment and branch_name:
        metadata = storage.read_metadata(root, session, branch_name)
        result["metadata"] = metadata.get(metadata_segment)

    return result


def history(
    root: Path,
    limit: int,
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Get git commit history.

    Args:
        root: Project root directory
        limit: Maximum number of commits to return
        session_id: Session identifier

    Returns:
        Dictionary with commit history

    Raises:
        GCCError: If operation fails
    """
    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)
        return {"session": session, "commits": git_log(repo_root, limit)}

    return storage.with_lock(root, session, _run)


def diff(
    root: Path,
    from_ref: str,
    to_ref: Optional[str],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Get git diff between two refs.

    Args:
        root: Project root directory
        from_ref: Source ref
        to_ref: Target ref (optional)
        session_id: Session identifier

    Returns:
        Dictionary with diff output

    Raises:
        ValidationError: If from_ref is empty
        GCCError: If operation fails
    """
    if not from_ref:
        raise ValidationError("from_ref is required", field="from_ref")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)
        return {"session": session, "diff": git_diff(repo_root, from_ref, to_ref)}

    return storage.with_lock(root, session, _run)


def show(
    root: Path,
    ref: str,
    path: Optional[str],
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Show file content at a git ref.

    Args:
        root: Project root directory
        ref: Git ref (commit, branch, etc.)
        path: Optional file path
        session_id: Session identifier

    Returns:
        Dictionary with file content

    Raises:
        ValidationError: If ref is empty
        GCCError: If operation fails
    """
    if not ref:
        raise ValidationError("ref is required", field="ref")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)
        return {"session": session, "content": git_show(repo_root, ref, path)}

    return storage.with_lock(root, session, _run)


def reset(
    root: Path,
    ref: str,
    mode: str,
    confirm: bool,
    session_id: Optional[str],
) -> Dict[str, Any]:
    """Reset repository to a ref.

    Args:
        root: Project root directory
        ref: Git ref to reset to
        mode: Reset mode ('soft' or 'hard')
        confirm: Must be True for hard reset
        session_id: Session identifier

    Returns:
        Dictionary with reset results

    Raises:
        ValidationError: If ref is empty or hard reset without confirm
        GCCError: If operation fails
    """
    if not ref:
        raise ValidationError("ref is required", field="ref")
    if mode == "hard" and not confirm:
        raise ValidationError("hard reset requires confirm=true", field="confirm")

    session = storage.normalize_session_id(session_id)

    def _run() -> Dict[str, Any]:
        storage.ensure_gcc(root, None, None, session)
        repo_root = storage.session_root(root, session)
        ensure_repo(repo_root)
        git_reset(repo_root, ref, mode)
        return {"session": session, "ref": ref, "mode": mode}

    return storage.with_lock(root, session, _run)
