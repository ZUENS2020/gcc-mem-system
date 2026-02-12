"""Security tests for input validation.

Tests that validators properly reject malicious or invalid inputs.
"""
from pathlib import Path
import pytest

from gcc.core.exceptions import ValidationError
from gcc.core.validators import Validators


def test_validate_branch_name_valid():
    """Test valid branch names."""
    assert Validators.validate_branch_name("main") == "main"
    assert Validators.validate_branch_name("feature-123") == "feature-123"
    assert Validators.validate_branch_name("dev_test") == "dev_test"
    assert Validators.validate_branch_name("a") == "a"  # Single char
    assert Validators.validate_branch_name("X" * 100) == "X" * 100  # Max length


def test_validate_branch_name_invalid():
    """Test invalid branch names are rejected."""
    with pytest.raises(ValidationError) as exc:
        Validators.validate_branch_name("")
    assert "empty" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_branch_name("X" * 101)
    assert "too long" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_branch_name("-invalid")
    assert "alphanumeric" in str(exc.value).lower()

    # Git reserved names
    for reserved in ["HEAD", "ORIG_HEAD", "FETCH_HEAD", "MERGE_HEAD"]:
        with pytest.raises(ValidationError) as exc:
            Validators.validate_branch_name(reserved)
        assert "reserved" in str(exc.value).lower()


def test_validate_session_id_valid():
    """Test valid session IDs."""
    assert Validators.validate_session_id(None) == "default"
    assert Validators.validate_session_id("") == "default"
    assert Validators.validate_session_id("session-123") == "session-123"
    assert Validators.validate_session_id("test_session") == "test_session"
    assert Validators.validate_session_id("ABC_123") == "ABC_123"


def test_validate_session_id_invalid():
    """Test invalid session IDs are rejected."""
    with pytest.raises(ValidationError) as exc:
        Validators.validate_session_id("X" * 101)
    assert "too long" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_session_id("session@123")
    assert "alphanumeric" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_session_id("session/123")
    assert "alphanumeric" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_session_id("session.123")
    assert "alphanumeric" in str(exc.value).lower()


def test_validate_git_ref_valid():
    """Test valid git refs."""
    assert Validators.validate_git_ref("HEAD") == "HEAD"
    assert Validators.validate_git_ref("main") == "main"
    assert Validators.validate_git_ref("a1b2c3d") == "a1b2c3d"
    assert Validators.validate_git_ref("v1.0.0") == "v1.0.0"
    assert Validators.validate_git_ref("origin/main") == "origin/main"
    assert Validators.validate_git_ref("HEAD~1") == "HEAD~1"
    assert Validators.validate_git_ref("feature-branch") == "feature-branch"


def test_validate_git_ref_invalid():
    """Test invalid git refs are rejected."""
    with pytest.raises(ValidationError) as exc:
        Validators.validate_git_ref("")
    assert "empty" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_git_ref("X" * 1001)
    assert "too long" in str(exc.value).lower()

    # Command injection attempts
    for dangerous in ["main; rm -rf /", "HEAD | cat /etc/passwd", "ref && malicious"]:
        with pytest.raises(ValidationError) as exc:
            Validators.validate_git_ref(dangerous)
        assert "dangerous" in str(exc.value).lower() or "invalid" in str(exc.value).lower()


def test_validate_limit_valid():
    """Test valid limit values."""
    assert Validators.validate_limit(1) == 1
    assert Validators.validate_limit(20) == 20
    assert Validators.validate_limit(100) == 100
    assert Validators.validate_limit(1000) == 1000


def test_validate_limit_invalid():
    """Test invalid limit values are rejected."""
    with pytest.raises(ValidationError) as exc:
        Validators.validate_limit(0)
    assert "at least" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_limit(-1)
    assert "at least" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_limit(1001)
    assert "at most" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_limit("abc")
    assert "integer" in str(exc.value).lower()


def test_validate_purpose_valid():
    """Test valid purpose strings."""
    purpose = "This is a test purpose"
    assert Validators.validate_purpose(purpose) == purpose

    long_purpose = "X" * 10000
    assert Validators.validate_purpose(long_purpose) == long_purpose


def test_validate_purpose_invalid():
    """Test invalid purpose strings are rejected."""
    with pytest.raises(ValidationError) as exc:
        Validators.validate_purpose("")
    assert "empty" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_purpose("X" * 10001)
    assert "too long" in str(exc.value).lower()


def test_validate_contribution_valid():
    """Test valid contribution strings."""
    contribution = "Added feature X"
    assert Validators.validate_contribution(contribution) == contribution

    long_contribution = "X" * 10000
    assert Validators.validate_contribution(long_contribution) == long_contribution


def test_validate_contribution_invalid():
    """Test invalid contribution strings are rejected."""
    with pytest.raises(ValidationError) as exc:
        Validators.validate_contribution("")
    assert "empty" in str(exc.value).lower()

    with pytest.raises(ValidationError) as exc:
        Validators.validate_contribution("X" * 10001)
    assert "too long" in str(exc.value).lower()


def test_validate_reset_mode_valid():
    """Test valid reset modes."""
    assert Validators.validate_reset_mode("soft") == "soft"
    assert Validators.validate_reset_mode("hard") == "hard"
    assert Validators.validate_reset_mode("mixed") == "mixed"


def test_validate_reset_mode_invalid():
    """Test invalid reset modes are rejected."""
    for invalid in ["", "invalid", "SOFT", "HARD", "delete"]:
        with pytest.raises(ValidationError) as exc:
            Validators.validate_reset_mode(invalid)
        assert "soft" in str(exc.value).lower() or "hard" in str(exc.value).lower()


def test_sanitize_log_entry():
    """Test log entry sanitization."""
    # Normal text
    assert Validators.sanitize_log_entry("Normal log") == "Normal log"

    # Control characters should be removed
    assert Validators.sanitize_log_entry("Text\x00with\x01control") == "Textwithcontrol"

    # Long text should be truncated
    long = "X" * 20000
    sanitized = Validators.sanitize_log_entry(long)
    assert len(sanitized) == 10000
