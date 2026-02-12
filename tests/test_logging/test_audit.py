"""Test audit logging."""
from pathlib import Path
import json
import pytest

from gcc.logging.audit import AuditLogger, log_operation, get_audit_logger


def test_audit_logger_init(tmp_path: Path):
    """Test audit logger initialization."""
    audit = AuditLogger(tmp_path)
    assert audit.log_dir == tmp_path
    assert audit.log_path == tmp_path / "audit.log"


def test_audit_log_operation(tmp_path: Path):
    """Test logging an operation."""
    audit = AuditLogger(tmp_path)
    
    audit.log(
        action="test_action",
        session_id="test_session",
        user="test_user",
        params={"key": "value"},
        result="success",
    )
    
    # Check file was created
    assert audit.log_path.exists()
    
    # Check content
    with audit.log_path.open("r", encoding="utf-8") as f:
        content = f.read()
        entries = [json.loads(line) for line in content.strip().split("\n") if line]
    
    assert len(entries) == 1
    assert entries[0]["action"] == "test_action"
    assert entries[0]["result"] == "success"


def test_audit_sanitize_sensitive_data(tmp_path: Path):
    """Test sensitive data sanitization."""
    audit = AuditLogger(tmp_path)
    
    audit.log(
        action="login",
        session_id="test",
        user="test",
        params={
            "username": "testuser",
            "password": "secret123",
            "api_key": "key-value",
        },
        result="success",
    )
    
    with audit.log_path.open("r", encoding="utf-8") as f:
        content = f.read()
        entry = json.loads(content.strip())
    
    # Sensitive fields should be redacted
    assert entry["params"]["username"] == "testuser"
    assert entry["params"]["password"] == "***REDACTED***"
    assert entry["params"]["api_key"] == "***REDACTED***"


def test_log_operation_convenience():
    """Test convenience function."""
    # Should not raise even if audit log is disabled
    log_operation(
        action="test",
        session_id="test",
        params={},
    )
