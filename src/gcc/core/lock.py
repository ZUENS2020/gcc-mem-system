"""File-based locking mechanism for GCC system.

Provides cross-process locking using POSIX file locking semantics.
"""
from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path

from .exceptions import LockError


@contextmanager
def file_lock(lock_path: Path, timeout_s: float = 10.0, poll_s: float = 0.1):
    """Acquire a file-based lock.

    Uses O_EXCL flag to create an exclusive lock file. This provides
    cross-process locking on POSIX systems and basic locking on Windows.

    Args:
        lock_path: Path to the lock file
        timeout_s: Maximum time to wait for lock (default 10s)
        poll_s: Time between lock attempts (default 0.1s)

    Yields:
        None when lock is acquired

    Raises:
        LockError: If lock cannot be acquired within timeout
        OSError: If lock file creation fails for other reasons
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    fd = None

    # Try to acquire lock
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.write(fd, str(os.getpid()).encode("utf-8"))
            break
        except FileExistsError:
            # Lock file exists, check if it's stale
            if time.time() - start > timeout_s:
                raise LockError(
                    f"Timed out waiting for lock after {timeout_s}s",
                    lock_path=str(lock_path),
                )
            time.sleep(poll_s)

    try:
        yield
    finally:
        # Release lock
        try:
            if fd is not None:
                os.close(fd)
            if lock_path.exists():
                lock_path.unlink()
        except OSError:
            # Best effort cleanup - don't raise if cleanup fails
            pass
