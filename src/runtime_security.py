"""Runtime safeguards for deployment environments."""

import os


VALID_ENVIRONMENTS = {
    "development",
    "test",
    "production",
}

VALID_IDENTITY_MODES = {
    "demo",
    "entra",
}


def get_environment() -> str:
    """Return the configured application environment."""
    return os.getenv(
        "APP_ENVIRONMENT",
        "development",
    ).strip().lower()


def get_identity_mode() -> str:
    """Return the configured identity mode."""
    return os.getenv(
        "IDENTITY_MODE",
        "demo",
    ).strip().lower()


def validate_runtime_security() -> None:
    """Reject unsafe environment and identity combinations."""
    environment = get_environment()
    identity_mode = get_identity_mode()

    if environment not in VALID_ENVIRONMENTS:
        raise RuntimeError(
            "Unsupported APP_ENVIRONMENT: "
            f"{environment}"
        )

    if identity_mode not in VALID_IDENTITY_MODES:
        raise RuntimeError(
            "Unsupported IDENTITY_MODE: "
            f"{identity_mode}"
        )

    if (
        environment == "production"
        and identity_mode != "entra"
    ):
        raise RuntimeError(
            "Production startup requires verified "
            "Microsoft Entra identity mode."
        )