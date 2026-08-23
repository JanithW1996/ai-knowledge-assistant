"""Parse trusted Microsoft Entra identity information."""

import base64
import json
from dataclasses import dataclass
from typing import Any


SUPPORTED_ROLES = {
    "employee",
    "manager",
    "senior_executive",
    "hr_adviser",
    "it_support_officer",
    "finance_officer",
}

USER_ID_CLAIM_TYPES = {
    "sub",
    "http://schemas.microsoft.com/identity/"
    "claims/objectidentifier",
    "http://schemas.xmlsoap.org/ws/2005/05/"
    "identity/claims/nameidentifier",
}

DISPLAY_NAME_CLAIM_TYPES = {
    "name",
    "preferred_username",
    "http://schemas.xmlsoap.org/ws/2005/05/"
    "identity/claims/name",
}


class IdentityError(ValueError):
    """Raised when a trusted identity cannot be established."""


@dataclass(frozen=True)
class VerifiedIdentity:
    """Trusted identity and assigned application role."""

    user_id: str
    display_name: str
    role: str


def decode_client_principal(
    encoded_principal: str,
) -> dict[str, Any]:
    """Decode the App Service client-principal header."""
    try:
        padding = "=" * (
            -len(encoded_principal) % 4
        )
        decoded_bytes = base64.b64decode(
            encoded_principal + padding,
            validate=True,
        )
        principal = json.loads(
            decoded_bytes.decode("utf-8")
        )
    except (
        ValueError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as error:
        raise IdentityError(
            "Invalid Microsoft Entra identity header."
        ) from error

    if not isinstance(principal, dict):
        raise IdentityError(
            "Invalid Microsoft Entra identity payload."
        )

    return principal


def get_claim_values(
    principal: dict[str, Any],
    claim_types: set[str],
) -> list[str]:
    """Return values for selected claim types."""
    claims = principal.get("claims", [])

    if not isinstance(claims, list):
        raise IdentityError(
            "Invalid Microsoft Entra claims payload."
        )

    values = []

    for claim in claims:
        if not isinstance(claim, dict):
            continue

        claim_type = claim.get("typ")
        claim_value = claim.get("val")

        if (
            claim_type in claim_types
            and isinstance(claim_value, str)
            and claim_value.strip()
        ):
            values.append(
                claim_value.strip()
            )

    return values


def get_role_claim_types(
    principal: dict[str, Any],
) -> set[str]:
    """Return recognized role-claim type names."""
    role_claim_types = {
        "role",
        "roles",
        "http://schemas.microsoft.com/ws/"
        "2008/06/identity/claims/role",
    }

    configured_role_type = principal.get(
        "role_typ"
    )

    if isinstance(configured_role_type, str):
        role_claim_types.add(
            configured_role_type
        )

    return role_claim_types


def parse_entra_identity(
    encoded_principal: str | None,
) -> VerifiedIdentity:
    """Return one verified identity with one trusted role."""
    if not encoded_principal:
        raise IdentityError(
            "Microsoft Entra identity is required."
        )

    principal = decode_client_principal(
        encoded_principal
    )

    authentication_type = str(
        principal.get("auth_typ", "")
    ).strip().lower()

    if authentication_type not in {
        "aad",
        "microsoft",
    }:
        raise IdentityError(
            "Microsoft Entra authentication is required."
        )

    user_ids = get_claim_values(
        principal,
        USER_ID_CLAIM_TYPES,
    )

    if not user_ids:
        raise IdentityError(
            "Microsoft Entra user identifier is missing."
        )

    display_names = get_claim_values(
        principal,
        DISPLAY_NAME_CLAIM_TYPES,
    )

    role_values = get_claim_values(
        principal,
        get_role_claim_types(principal),
    )

    recognized_roles = {
        value.strip().lower()
        for value in role_values
        if value.strip().lower()
        in SUPPORTED_ROLES
    }

    if len(recognized_roles) != 1:
        raise IdentityError(
            "Exactly one supported application role "
            "must be assigned."
        )

    role = next(iter(recognized_roles))

    return VerifiedIdentity(
        user_id=user_ids[0],
        display_name=(
            display_names[0]
            if display_names
            else "Authenticated user"
        ),
        role=role,
    )