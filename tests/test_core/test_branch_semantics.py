from __future__ import annotations

import subprocess
from pathlib import Path

from gcc.core import commands
from gcc.core.storage import session_root


def _git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo_root),
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_existing_branch_checkout_does_not_reset_pointer(tmp_path: Path) -> None:
    root = tmp_path
    session_id = "branch-isolation"

    commands.init(root, "goal", [], session_id)
    commands.branch(root, "alpha", "alpha purpose", session_id)
    commands.commit(root, "alpha", "alpha-1", None, None, None, None, session_id)

    repo_root = session_root(root, session_id)
    alpha_after_first_commit = _git(repo_root, "rev-parse", "alpha")

    commands.branch(root, "beta", "beta purpose", session_id)
    commands.commit(root, "beta", "beta-1", None, None, None, None, session_id)

    # alpha pointer should stay unchanged while working on beta.
    assert _git(repo_root, "rev-parse", "alpha") == alpha_after_first_commit

    beta_after_first_commit = _git(repo_root, "rev-parse", "beta")
    commands.commit(root, "alpha", "alpha-2", None, None, None, None, session_id)

    # beta pointer should stay unchanged while switching back to alpha.
    assert _git(repo_root, "rev-parse", "beta") == beta_after_first_commit
    assert _git(repo_root, "rev-parse", "alpha") != alpha_after_first_commit
