from __future__ import annotations

import os
from pathlib import Path

from gcc.mcp import proxy


def _reset_session_env(monkeypatch) -> None:
    monkeypatch.setattr(proxy, "DEFAULT_SESSION_ID", None)
    for key in (
        proxy.SESSION_ID_ENV,
        proxy.SESSION_MODE_ENV,
        proxy.SESSION_LOCK_MODE_ENV,
        proxy.SESSION_NAMESPACE_ENV,
        proxy.SESSION_ID_FILE_ENV,
        "HOSTNAME",
    ):
        monkeypatch.delenv(key, raising=False)


def test_env_session_id_locks_and_overrides_arguments(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv(proxy.SESSION_ID_ENV, "shared-memory")

    payload = proxy._ensure_session_id({"session_id": "custom-memory"})
    assert payload["session_id"] == "shared-memory"


def test_env_lock_mode_allows_custom_session_in_docker(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv("HOSTNAME", "abc123def456")
    monkeypatch.setenv(proxy.SESSION_LOCK_MODE_ENV, "env")

    payload = proxy._ensure_session_id({"session_id": "custom-memory"})
    assert payload["session_id"] == "custom-memory"


def test_strict_lock_mode_keeps_legacy_docker_lock(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv("HOSTNAME", "abc123def456")
    monkeypatch.setenv(proxy.SESSION_LOCK_MODE_ENV, "strict")
    monkeypatch.setenv(proxy.SESSION_MODE_ENV, "shared")

    payload = proxy._ensure_session_id({"session_id": "custom-memory"})
    assert payload["session_id"] == "container-abc123def456"


def test_auto_mode_uses_shared_default_in_docker(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv("HOSTNAME", "abc123def456")
    monkeypatch.setenv(proxy.SESSION_MODE_ENV, "auto")
    monkeypatch.setenv(proxy.SESSION_LOCK_MODE_ENV, "none")

    session_id = proxy._default_session_id()
    assert session_id == "container-abc123def456"


def test_isolated_mode_uses_pid_suffix_in_docker(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv("HOSTNAME", "abc123def456")
    monkeypatch.setenv(proxy.SESSION_MODE_ENV, "isolated")
    monkeypatch.setenv(proxy.SESSION_LOCK_MODE_ENV, "none")

    session_id = proxy._default_session_id()
    assert session_id.startswith("container-abc123def456-p")
    assert session_id.endswith(str(os.getpid()))


def test_shared_mode_uses_workspace_stable_session(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv(proxy.SESSION_MODE_ENV, "shared")
    monkeypatch.setenv(proxy.SESSION_LOCK_MODE_ENV, "none")
    monkeypatch.setattr(proxy, "_running_in_docker", lambda: False)

    session_1 = proxy._default_session_id()
    session_2 = proxy._default_session_id()
    assert session_1.startswith("ws-")
    assert session_1 == session_2


def test_session_id_file_is_used_when_configured(monkeypatch, tmp_path: Path) -> None:
    _reset_session_env(monkeypatch)
    session_file = tmp_path / "session.id"
    session_file.write_text("file-memory-01\n", encoding="utf-8")
    monkeypatch.setenv(proxy.SESSION_ID_FILE_ENV, str(session_file))

    session_id = proxy._default_session_id()
    assert session_id == "file-memory-01"


def test_namespace_prefix_is_applied_to_generated_session(monkeypatch) -> None:
    _reset_session_env(monkeypatch)
    monkeypatch.setenv(proxy.SESSION_NAMESPACE_ENV, "team-a")
    monkeypatch.setenv(proxy.SESSION_MODE_ENV, "isolated")
    monkeypatch.setenv(proxy.SESSION_LOCK_MODE_ENV, "none")
    monkeypatch.setattr(proxy, "_running_in_docker", lambda: False)

    session_id = proxy._default_session_id()
    assert session_id.startswith("team-a-mcp-")
