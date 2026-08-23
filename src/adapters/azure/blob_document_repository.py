"""Azure Blob Storage implementation of the document repository."""

import json
from pathlib import PurePosixPath
from typing import Any

from azure.storage.blob import BlobServiceClient

from src.core.models import DocumentMetadata


class AzureBlobDocumentRepository:
    """Read governed documents from a private Azure blob container."""

    def __init__(
        self,
        account_url: str,
        container_name: str,
        credential: Any,
        container_client: Any | None = None,
    ) -> None:
        if not account_url:
            raise ValueError("Azure Storage account URL is required.")

        if not container_name:
            raise ValueError("Azure Storage container name is required.")

        self.container_client = container_client

        if self.container_client is None:
            blob_service = BlobServiceClient(
                account_url=account_url,
                credential=credential,
            )
            self.container_client = blob_service.get_container_client(
                container_name
            )

    def list_documents(self) -> list[DocumentMetadata]:
        """Load governed metadata from the uploaded manifest."""
        manifest = json.loads(self._download_text("manifest.json"))

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
        """Download a document using its governed document ID."""
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

        self._validate_blob_path(document.path)
        return self._download_text(document.path)

    def _download_text(self, blob_name: str) -> str:
        """Download one UTF-8 text blob."""
        content = self.container_client.download_blob(
            blob_name
        ).readall()
        return content.decode("utf-8")

    @staticmethod
    def _validate_blob_path(blob_name: str) -> None:
        """Reject paths that could escape the governed container structure."""
        path = PurePosixPath(blob_name)

        if path.is_absolute() or ".." in path.parts or "\\" in blob_name:
            raise ValueError(f"Unsafe blob path: {blob_name}")