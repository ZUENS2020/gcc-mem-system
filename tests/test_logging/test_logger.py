"""Test logging infrastructure."""
from pathlib import Path
import pytest
import logging

from gcc.logging.logger import GCCLogger, get_logger


def test_get_logger_basic():
    """Test basic logger creation."""
    logger = get_logger("test_logger")
    assert logger is not None
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO


def test_logger_caching():
    """Test logger instances are cached."""
    logger1 = GCCLogger.get_logger("cached")
    logger2 = GCCLogger.get_logger("cached")
    assert logger1 is logger2


def test_get_logger_convenience():
    """Test convenience function."""
    logger = get_logger("convenience")
    assert logger is not None
    # Should have handlers
    assert len(logger.handlers) > 0


def test_logger_has_handlers(tmp_path: Path):
    """Test logger has appropriate handlers."""
    logger = GCCLogger.get_logger("handler_test", log_dir=tmp_path)
    
    # Should have at least console handler
    assert len(logger.handlers) >= 1
    
    # Should have file handler if log_dir provided
    assert len(logger.handlers) >= 2
    
    # File handler should be RotatingFileHandler
    from logging.handlers import RotatingFileHandler
    assert any(isinstance(h, RotatingFileHandler) for h in logger.handlers)
