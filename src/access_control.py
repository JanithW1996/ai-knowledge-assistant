"""Enforce provider-neutral role-based document access."""

from src.core.models import DocumentMetadata
from src.dependencies import create_document_repository
from src.ports.document_repository import DocumentRepository


def get_authorised_documents(
    role: str,
    repository: DocumentRepository | None = None,
) -> list[DocumentMetadata]:
    """Return only documents available to the supplied role."""
    selected_repository = repository or create_document_repository()
    normalised_role = role.strip().lower()

    return [
        document
        for document in selected_repository.list_documents()
        if normalised_role in document.allowed_roles
    ]


def read_authorised_document(
    document_id: str,
    role: str,
    repository: DocumentRepository | None = None,
) -> str:
    """Read a document only when the role is authorised."""
    selected_repository = repository or create_document_repository()

    document = next(
        (
            item
            for item in selected_repository.list_documents()
            if item.id == document_id
        ),
        None,
    )

    if document is None:
        raise KeyError(f"Unknown document ID: {document_id}")

    if role.strip().lower() not in document.allowed_roles:
        raise PermissionError(
            f"Role '{role}' cannot access document '{document_id}'."
        )

    return selected_repository.read_document(document_id)