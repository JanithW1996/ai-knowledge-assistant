"""Runtime safeguards for deployment environments."""

import os


VALID_ENVIRONMENTS = {
    "development",
    "test",
    "production",
}


def validate_runtime_security() -> None:
    """Prevent the demonstration identity mode running in production."""
    environment = os.getenv(
        "APP_ENVIRONMENT",
        "development",
    ).strip().lower()

    identity_mode = os.getenv(
        "IDENTITY_MODE",
        "demo",
    ).strip().lower()

    if environment not in VALID_ENVIRONMENTS:
        raise RuntimeError(
            f"Unsupported APP_ENVIRONMENT: {environment}"
        )

    if identity_mode != "demo":
        raise RuntimeError(
            f"Unsupported IDENTITY_MODE: {identity_mode}"
        )

    if environment == "production":
        raise RuntimeError(
            "Production startup is blocked until verified "
            "organisational identity is implemented."
        )