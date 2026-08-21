"""Local-file implementation of the document repository."""

import json
from pathlib import Path

from src.core.models import DocumentMetadata


class LocalFileRepository:
    """Read governed documents from the local synthetic dataset."""

    def __init__(self, data_directory: Path) -> None:
        self.data_directory = data_directory.resolve()
        self.manifest_path = self.data_directory / "manifest.json"

    def list_documents(self) -> list[DocumentMetadata]:
        """Load document metadata from the JSON manifest."""
        manifest = json.loads(
            self.manifest_path.read_text(encoding="utf-8")
        )

        return [
            DocumentMetadata(
                id=document["id"],
                title=document["title"],
                path=document["path"],
                classification=document["classification"],
                allowed_roles=tuple(document["allowed_roles"]),
            )
            for document in manifest["documents"]
        ]

    def read_document(self, document_id: str) -> str:
        """Read a document while enforcing safe local paths."""
        document = next(
            (
                item
                for item in self.list_documents()
                if item.id == document_id
            ),
            None,
        )

        if document is None:
            raise KeyError(f"Unknown document ID: {document_id}")

        document_path = (
            self.data_directory / document.path
        ).resolve()

        if not document_path.is_relative_to(self.data_directory):
            raise ValueError(f"Unsafe document path: {document_id}")

        return document_path.read_text(encoding="utf-8")