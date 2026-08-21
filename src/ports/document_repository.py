"""Document-storage capability required by the core."""

from typing import Protocol

from src.core.models import DocumentMetadata


class DocumentRepository(Protocol):
    """Interface implemented by document-storage adapters."""

    def list_documents(self) -> list[DocumentMetadata]:
        """Return available document metadata."""
        ...

    def read_document(self, document_id: str) -> str:
        """Return document content using its unique ID."""
        ...