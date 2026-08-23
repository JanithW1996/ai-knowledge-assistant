"""Tests for deployment safety safeguards."""

import pytest

from src.runtime_security import validate_runtime_security


def test_allows_development_demo_mode(monkeypatch) -> None:
    """The local portfolio demonstration must remain usable."""
    monkeypatch.setenv("APP_ENVIRONMENT", "development")
    monkeypatch.setenv("IDENTITY_MODE", "demo")

    validate_runtime_security()


def test_rejects_unknown_environment(monkeypatch) -> None:
    """Mistyped environment names must not silently continue."""
    monkeypatch.setenv("APP_ENVIRONMENT", "prod")
    monkeypatch.setenv("IDENTITY_MODE", "demo")

    with pytest.raises(RuntimeError):
        validate_runtime_security()


def test_rejects_unimplemented_identity_mode(monkeypatch) -> None:
    """A security mode cannot be claimed before implementation."""
    monkeypatch.setenv("APP_ENVIRONMENT", "development")
    monkeypatch.setenv("IDENTITY_MODE", "unverified")

    with pytest.raises(RuntimeError):
        validate_runtime_security()


def test_blocks_demo_identity_in_production(monkeypatch) -> None:
    """Caller-selected roles must never run as production identity."""
    monkeypatch.setenv("APP_ENVIRONMENT", "production")
    monkeypatch.setenv("IDENTITY_MODE", "demo")

    with pytest.raises(
        RuntimeError,
        match="Production startup is blocked",
    ):
        validate_runtime_security()