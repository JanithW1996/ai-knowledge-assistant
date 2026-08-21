"""Tests for the local document-repository adapter."""

from src.dependencies import create_document_repository


def test_local_repository_loads_document_metadata() -> None:
    """The local adapter should return all synthetic documents."""
    repository = create_document_repository()
    documents = repository.list_documents()

    assert {document.id for document in documents} == {
        "PUB-001",
        "INT-001",
        "HR-001",
    }


def test_local_repository_reads_document_content() -> None:
    """The local adapter should read content by document ID."""
    repository = create_document_repository()
    content = repository.read_document("INT-001")

    assert "Fictional Workplace Guide" in content