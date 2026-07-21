import pytest

from app.config import settings


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

def test_database_url_is_loaded():
    """
    Verify DATABASE_URL is loaded successfully.
    """
    assert settings.DATABASE_URL is not None
    assert settings.DATABASE_URL != ""


def test_database_url_type():
    """
    Verify DATABASE_URL is a string.
    """
    assert isinstance(settings.DATABASE_URL, str)


def test_database_url_scheme():
    """
    Verify DATABASE_URL uses PostgreSQL.
    """
    assert settings.DATABASE_URL.startswith("postgresql")


# ==========================================================
# LOGGING CONFIGURATION
# ==========================================================

def test_log_level_is_loaded():
    """
    Verify LOG_LEVEL exists.
    """
    assert settings.LOG_LEVEL is not None


def test_log_level_type():
    """
    Verify LOG_LEVEL is a string.
    """
    assert isinstance(settings.LOG_LEVEL, str)


def test_log_level_allowed_values():
    """
    Verify LOG_LEVEL is one of the supported logging levels.
    """
    assert settings.LOG_LEVEL in {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }


# ==========================================================
# ENVIRONMENT OVERRIDE
# ==========================================================

def test_database_url_can_be_overridden(monkeypatch):
    """
    Verify DATABASE_URL can be overridden during testing.
    """

    test_database_url = (
        "postgresql+psycopg://test_user:test_password@localhost:5432/test_db"
    )

    monkeypatch.setattr(
        settings,
        "DATABASE_URL",
        test_database_url,
    )

    assert settings.DATABASE_URL == test_database_url


def test_log_level_can_be_overridden(monkeypatch):
    """
    Verify LOG_LEVEL can be overridden during testing.
    """

    monkeypatch.setattr(
        settings,
        "LOG_LEVEL",
        "DEBUG",
    )

    assert settings.LOG_LEVEL == "DEBUG"