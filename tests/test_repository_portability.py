"""Prove access control works with a replaceable repository."""

import pytest

from src.access_control import (
    get_authorised_documents,
    read_authorised_document,
)
from src.core.models import DocumentMetadata


class InMemoryRepository:
    """Small provider used only for portability testing."""

    def __init__(self) -> None:
        self.documents = [
            DocumentMetadata(
                id="TEST-001",
                title="Internal Test Guide",
                path="unused",
                classification="internal",
                allowed_roles=("employee", "manager"),
            ),
            DocumentMetadata(
                id="TEST-002",
                title="Restricted Manager Guide",
                path="unused",
                classification="restricted",
                allowed_roles=("manager",),
            ),
        ]

        self.content = {
            "TEST-001": "Synthetic internal test content.",
            "TEST-002": "Synthetic restricted manager content.",
        }

    def list_documents(self) -> list[DocumentMetadata]:
        """Return in-memory metadata."""
        return self.documents

    def read_document(self, document_id: str) -> str:
        """Return in-memory content."""
        return self.content[document_id]


def test_access_control_accepts_replaceable_repository() -> None:
    """Core access rules should work without local files."""
    repository = InMemoryRepository()

    documents = get_authorised_documents("employee", repository)

    assert [document.id for document in documents] == ["TEST-001"]


def test_replaceable_repository_still_enforces_denial() -> None:
    """Changing storage providers must not bypass security."""
    repository = InMemoryRepository()

    with pytest.raises(PermissionError):
        read_authorised_document("TEST-002", "employee", repository)