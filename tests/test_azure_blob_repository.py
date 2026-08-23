"""Offline tests for the Azure Blob document adapter."""

import json

import pytest

from src.adapters.azure.blob_document_repository import (
    AzureBlobDocumentRepository,
)


class FakeDownload:
    """Pretend Azure blob download."""

    def __init__(self, content: str) -> None:
        self.content = content

    def readall(self) -> bytes:
        return self.content.encode("utf-8")


class FakeContainerClient:
    """In-memory replacement for Azure Blob Storage."""

    def __init__(self, blobs: dict[str, str]) -> None:
        self.blobs = blobs

    def download_blob(self, blob_name: str) -> FakeDownload:
        return FakeDownload(self.blobs[blob_name])


def create_repository(document_path: str = "internal/guide.md"):
    """Create an Azure repository backed by fake blobs."""
    manifest = {
        "documents": [
            {
                "id": "INT-001",
                "title": "Fictional Guide",
                "path": document_path,
                "classification": "internal",
                "allowed_roles": ["employee"],
            }
        ]
    }

    container = FakeContainerClient(
        {
            "manifest.json": json.dumps(manifest),
            "internal/guide.md": "Synthetic guidance.",
        }
    )

    return AzureBlobDocumentRepository(
        account_url="https://example.blob.core.windows.net",
        container_name="knowledge-documents",
        credential=object(),
        container_client=container,
    )


def test_lists_document_metadata() -> None:
    repository = create_repository()

    documents = repository.list_documents()

    assert documents[0].id == "INT-001"
    assert documents[0].allowed_roles == ("employee",)


def test_reads_document_by_governed_id() -> None:
    repository = create_repository()

    assert repository.read_document(
        "INT-001"
    ) == "Synthetic guidance."


def test_rejects_unknown_document_id() -> None:
    repository = create_repository()

    with pytest.raises(KeyError):
        repository.read_document("UNKNOWN")


def test_rejects_unsafe_blob_path() -> None:
    repository = create_repository("../secret.md")

    with pytest.raises(ValueError):
        repository.read_document("INT-001")