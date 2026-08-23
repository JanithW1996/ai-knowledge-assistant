"""Tests for deployment safety safeguards."""

import pytest

from src.runtime_security import (
    get_environment,
    get_identity_mode,
    validate_runtime_security,
)


def test_allows_development_demo_mode(
    monkeypatch,
) -> None:
    """The local demonstration must remain usable."""
    monkeypatch.setenv(
        "APP_ENVIRONMENT",
        "development",
    )
    monkeypatch.setenv(
        "IDENTITY_MODE",
        "demo",
    )

    validate_runtime_security()

    assert get_environment() == "development"
    assert get_identity_mode() == "demo"


def test_allows_production_entra_mode(
    monkeypatch,
) -> None:
    """Production may run with verified Entra identity."""
    monkeypatch.setenv(
        "APP_ENVIRONMENT",
        "production",
    )
    monkeypatch.setenv(
        "IDENTITY_MODE",
        "entra",
    )

    validate_runtime_security()

    assert get_environment() == "production"
    assert get_identity_mode() == "entra"


def test_rejects_unknown_environment(
    monkeypatch,
) -> None:
    """Unknown environments must not silently continue."""
    monkeypatch.setenv(
        "APP_ENVIRONMENT",
        "prod",
    )
    monkeypatch.setenv(
        "IDENTITY_MODE",
        "demo",
    )

    with pytest.raises(
        RuntimeError,
        match="Unsupported APP_ENVIRONMENT",
    ):
        validate_runtime_security()


def test_rejects_unknown_identity_mode(
    monkeypatch,
) -> None:
    """Unknown identity modes must be rejected."""
    monkeypatch.setenv(
        "APP_ENVIRONMENT",
        "development",
    )
    monkeypatch.setenv(
        "IDENTITY_MODE",
        "unverified",
    )

    with pytest.raises(
        RuntimeError,
        match="Unsupported IDENTITY_MODE",
    ):
        validate_runtime_security()


def test_blocks_demo_identity_in_production(
    monkeypatch,
) -> None:
    """Caller-selected roles must not run in production."""
    monkeypatch.setenv(
        "APP_ENVIRONMENT",
        "production",
    )
    monkeypatch.setenv(
        "IDENTITY_MODE",
        "demo",
    )

    with pytest.raises(
        RuntimeError,
        match=(
            "Production startup requires verified "
            "Microsoft Entra identity mode"
        ),
    ):
        validate_runtime_security()


def test_defaults_to_safe_development_demo(
    monkeypatch,
) -> None:
    """Missing settings should preserve safe local defaults."""
    monkeypatch.delenv(
        "APP_ENVIRONMENT",
        raising=False,
    )
    monkeypatch.delenv(
        "IDENTITY_MODE",
        raising=False,
    )

    validate_runtime_security()

    assert get_environment() == "development"
    assert get_identity_mode() == "demo"