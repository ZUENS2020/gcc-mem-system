from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from gcc.server.app import app
from gcc.server import endpoints as server_endpoints


client = TestClient(app)


def _set_data_root(monkeypatch, tmp_path: Path) -> Path:
    data_root = tmp_path / "data"
    data_root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("GCC_DATA_ROOT", str(data_root))
    return data_root


def test_uses_default_data_root_when_env_missing(monkeypatch, tmp_path: Path) -> None:
    default_data_root = tmp_path / "default-data-root"
    monkeypatch.setattr(server_endpoints, "DEFAULT_DATA_ROOT", str(default_data_root))
    monkeypatch.delenv("GCC_DATA_ROOT", raising=False)

    res = client.post(
        "/init",
        json={"goal": "Test", "todo": ["a"], "session_id": "session-a"},
    )

    assert res.status_code == 200
    assert default_data_root.exists()


def test_unknown_fields_are_rejected(monkeypatch, tmp_path: Path) -> None:
    _set_data_root(monkeypatch, tmp_path)

    res = client.post(
        "/init",
        json={
            "goal": "Test",
            "todo": ["a"],
            "session_id": "session-a",
            "root": str(tmp_path),
        },
    )

    assert res.status_code == 422
    detail = res.json().get("detail", [])
    assert any(err.get("loc", [])[-1:] == ["root"] for err in detail)


def test_init_branch_commit_context(monkeypatch, tmp_path: Path) -> None:
    _set_data_root(monkeypatch, tmp_path)
    session_id = "session-a"

    res = client.post(
        "/init",
        json={"goal": "Test", "todo": ["a"], "session_id": session_id},
    )
    assert res.status_code == 200

    res = client.post(
        "/branch",
        json={"branch": "main", "purpose": "Main work", "session_id": session_id},
    )
    assert res.status_code == 200

    res = client.post(
        "/commit",
        json={"branch": "main", "contribution": "Did work", "session_id": session_id},
    )
    assert res.status_code == 200
    commit_id = res.json()["commit_id"]

    res = client.post(
        "/context",
        json={
            "branch": "main",
            "commit_id": commit_id,
            "log_tail": 5,
            "session_id": session_id,
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert "branches" in body
    assert body["branch"]["latest_commit"] == commit_id


def test_session_isolation(monkeypatch, tmp_path: Path) -> None:
    _set_data_root(monkeypatch, tmp_path)

    res = client.post(
        "/branch",
        json={"branch": "main", "purpose": "Main", "session_id": "one"},
    )
    assert res.status_code == 200

    res = client.post(
        "/context",
        json={"session_id": "two"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["branches"] == []


def test_history_and_show(monkeypatch, tmp_path: Path) -> None:
    _set_data_root(monkeypatch, tmp_path)
    session_id = "history"

    res = client.post(
        "/init",
        json={"goal": "Test", "todo": [], "session_id": session_id},
    )
    assert res.status_code == 200

    res = client.post(
        "/branch",
        json={"branch": "main", "purpose": "Main", "session_id": session_id},
    )
    assert res.status_code == 200

    res = client.post(
        "/history",
        json={"limit": 5, "session_id": session_id},
    )
    assert res.status_code == 200
    commits = res.json().get("commits", [])
    assert commits

    res = client.post(
        "/show",
        json={"ref": "HEAD", "path": "main.md", "session_id": session_id},
    )
    assert res.status_code == 200
    assert "GCC Roadmap" in res.json().get("content", "")


def test_init_path_layout_not_duplicated(monkeypatch, tmp_path: Path) -> None:
    data_root = _set_data_root(monkeypatch, tmp_path)
    session_id = "path-layout"

    res = client.post("/init", json={"session_id": session_id})
    assert res.status_code == 200

    body = res.json()
    main_path = body.get("main", "")
    expected = str((data_root / ".GCC" / "sessions" / session_id / "main.md")).replace("\\", "/")
    assert main_path.replace("\\", "/") == expected
    assert f"/sessions/{session_id}/.GCC/sessions/{session_id}/" not in main_path.replace("\\", "/")


def test_branch_not_found_maps_to_404(monkeypatch, tmp_path: Path) -> None:
    _set_data_root(monkeypatch, tmp_path)
    session_id = "missing-branch"
    no_raise_client = TestClient(app, raise_server_exceptions=False)

    res = no_raise_client.post("/init", json={"session_id": session_id})
    assert res.status_code == 200

    res = no_raise_client.post(
        "/log",
        json={"branch": "does-not-exist", "entries": ["x"], "session_id": session_id},
    )
    assert res.status_code == 404
    body = res.json()
    assert body.get("error") == "branch_not_found"
    assert "does-not-exist" in body.get("detail", "")
