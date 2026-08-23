"""Tests for trusted Microsoft Entra identities."""

import base64
import json

import pytest

from src.entra_identity import (
    IdentityError,
    parse_entra_identity,
)


def encode_principal(
    *,
    roles: list[str],
    authentication_type: str = "aad",
) -> str:
    """Create a synthetic App Service identity header."""
    claims = [
        {
            "typ": (
                "http://schemas.microsoft.com/"
                "identity/claims/objectidentifier"
            ),
            "val": "synthetic-user-id",
        },
        {
            "typ": (
                "http://schemas.xmlsoap.org/"
                "ws/2005/05/identity/claims/name"
            ),
            "val": "Synthetic User",
        },
    ]

    claims.extend(
        {
            "typ": "roles",
            "val": role,
        }
        for role in roles
    )

    principal = {
        "auth_typ": authentication_type,
        "name_typ": (
            "http://schemas.xmlsoap.org/"
            "ws/2005/05/identity/claims/name"
        ),
        "role_typ": "roles",
        "claims": claims,
    }

    encoded = base64.b64encode(
        json.dumps(principal).encode("utf-8")
    )

    return encoded.decode("ascii")


@pytest.mark.parametrize(
    "role",
    [
        "employee",
        "manager",
        "senior_executive",
        "hr_adviser",
        "it_support_officer",
        "finance_officer",
    ],
)
def test_accepts_each_supported_entra_role(
    role: str,
) -> None:
    """Each approved app role should be accepted."""
    identity = parse_entra_identity(
        encode_principal(roles=[role])
    )

    assert identity.user_id == "synthetic-user-id"
    assert identity.display_name == "Synthetic User"
    assert identity.role == role


def test_rejects_missing_identity_header() -> None:
    """Production requests require an identity header."""
    with pytest.raises(
        IdentityError,
        match="identity is required",
    ):
        parse_entra_identity(None)


def test_rejects_invalid_identity_header() -> None:
    """Malformed headers must fail closed."""
    with pytest.raises(
        IdentityError,
        match="Invalid Microsoft Entra",
    ):
        parse_entra_identity(
            "not-valid-base64"
        )


def test_rejects_non_entra_authentication() -> None:
    """Another authentication type must not be trusted."""
    with pytest.raises(
        IdentityError,
        match="Entra authentication is required",
    ):
        parse_entra_identity(
            encode_principal(
                roles=["employee"],
                authentication_type="github",
            )
        )


def test_rejects_missing_role() -> None:
    """Authenticated users still require an app role."""
    with pytest.raises(
        IdentityError,
        match="Exactly one supported",
    ):
        parse_entra_identity(
            encode_principal(roles=[])
        )


def test_rejects_unsupported_role() -> None:
    """Unknown role values must not grant access."""
    with pytest.raises(
        IdentityError,
        match="Exactly one supported",
    ):
        parse_entra_identity(
            encode_principal(
                roles=["global_administrator"]
            )
        )


def test_rejects_multiple_roles() -> None:
    """Ambiguous role assignments must fail closed."""
    with pytest.raises(
        IdentityError,
        match="Exactly one supported",
    ):
        parse_entra_identity(
            encode_principal(
                roles=[
                    "senior_executive",
                    "finance_officer",
                ]
            )
        )