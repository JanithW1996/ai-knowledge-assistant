"""Enforce provider-neutral role-based document access."""

from src.core.models import DocumentMetadata
from src.dependencies import create_document_repository
from src.ports.document_repository import DocumentRepository


ROLE_HIERARCHY = {
    "employee": {
        "employee",
    },
    "manager": {
        "employee",
        "manager",
    },
    "senior_executive": {
        "employee",
        "manager",
        "senior_executive",
    },
    "hr_adviser": {
        "employee",
        "hr_adviser",
    },
    "it_support_officer": {
        "employee",
        "it_support_officer",
    },
    "finance_officer": {
        "employee",
        "finance_officer",
    },
}


def get_effective_roles(role: str) -> set[str]:
    """Return roles inherited through the organisation hierarchy."""
    normalised_role = role.strip().lower()

    return ROLE_HIERARCHY.get(
        normalised_role,
        {normalised_role},
    )


def is_document_authorised(
    document: DocumentMetadata,
    role: str,
) -> bool:
    """Check whether any effective role may access a document."""
    effective_roles = get_effective_roles(role)

    return bool(
        effective_roles
        & set(document.allowed_roles)
    )


def get_authorised_documents(
    role: str,
    repository: DocumentRepository | None = None,
) -> list[DocumentMetadata]:
    """Return only documents available to the supplied role."""
    selected_repository = (
        repository
        or create_document_repository()
    )

    return [
        document
        for document
        in selected_repository.list_documents()
        if is_document_authorised(document, role)
    ]


def get_unauthorised_documents(
    role: str,
    repository: DocumentRepository | None = None,
) -> list[DocumentMetadata]:
    """Return denied metadata for internal detection only."""
    selected_repository = (
        repository
        or create_document_repository()
    )

    return [
        document
        for document
        in selected_repository.list_documents()
        if not is_document_authorised(document, role)
    ]


def read_authorised_document(
    document_id: str,
    role: str,
    repository: DocumentRepository | None = None,
) -> str:
    """Read a document only when the role is authorised."""
    selected_repository = (
        repository
        or create_document_repository()
    )

    document = next(
        (
            item
            for item
            in selected_repository.list_documents()
            if item.id == document_id
        ),
        None,
    )

    if document is None:
        raise KeyError(
            f"Unknown document ID: {document_id}"
        )

    if not is_document_authorised(document, role):
        raise PermissionError(
            "The user is unauthorized to access this data."
        )

    return selected_repository.read_document(
        document_id
    )