"""Tests for the local document-repository adapter."""

from src.dependencies import create_document_repository


def test_local_repository_loads_document_metadata() -> None:
    """The local adapter should return all synthetic documents."""
    repository = create_document_repository()
    documents = repository.list_documents()

    assert {
        document.id
        for document in documents
    } == {
        "PUB-001",
        "INT-001",
        "HR-001",
        "MGR-001",
        "IT-001",
        "FIN-001",
        "FIN-002",
    }


def test_local_repository_preserves_classifications() -> None:
    """The adapter should preserve document sensitivity."""
    repository = create_document_repository()
    documents = repository.list_documents()

    classifications = {
        document.id: document.classification
        for document in documents
    }

    assert classifications["FIN-001"] == "restricted"
    assert (
        classifications["FIN-002"]
        == "highly_confidential"
    )


def test_local_repository_reads_document_content() -> None:
    """The local adapter should read content by document ID."""
    repository = create_document_repository()
    content = repository.read_document("INT-001")

    assert "Fictional Workplace Guide" in content


def test_local_repository_reads_payroll_guidance() -> None:
    """The adapter should read synthetic payroll guidance."""
    repository = create_document_repository()
    content = repository.read_document("FIN-002")

    assert "Fictional Payroll Control Review" in content
    assert "Synthetic:** Yes" in content