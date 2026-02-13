from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from gcc.core.git_ops import ensure_repo
from gcc.core.storage import _now_iso
from gcc.logging.audit import AuditLogger


def test_storage_timestamp_is_utc_z_format() -> None:
    timestamp = _now_iso()
    assert timestamp.endswith("Z")
    datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


def test_git_log_timestamp_is_utc_z_format(tmp_path: Path) -> None:
    repo_root = tmp_path / "repo"
    ensure_repo(repo_root)

    git_log_path = repo_root / "git.log"
    assert git_log_path.exists()

    first_line = git_log_path.read_text(encoding="utf-8").splitlines()[0]
    assert first_line.startswith("[")
    timestamp = first_line.split("]", 1)[0].lstrip("[")
    datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")


def test_audit_timestamp_is_timezone_aware_utc(tmp_path: Path) -> None:
    audit_logger = AuditLogger(tmp_path)
    audit_logger.log(
        action="test",
        session_id="session",
        user="user",
        params={},
    )

    entry = json.loads((tmp_path / "audit.log").read_text(encoding="utf-8").splitlines()[0])
    timestamp = entry["timestamp"]
    assert timestamp.endswith("Z")

    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    assert parsed.tzinfo is not None
    assert parsed.utcoffset() == timedelta(0)
    assert parsed.tzinfo == timezone.utc
