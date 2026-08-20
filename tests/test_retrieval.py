"""Tests for authorised document retrieval."""

from src.retrieval import search_documents, tokenise


def test_tokenise_removes_common_words() -> None:
    """Common words should not influence relevance."""
    terms = tokenise("How do I report a security incident?")

    assert terms == {"report", "security", "incident"}


def test_employee_finds_internal_security_guidance() -> None:
    """Security questions should find the workplace guide."""
    results = search_documents(
        "How should I report a security incident?",
        "employee",
    )

    assert results[0]["id"] == "INT-001"


def test_employee_cannot_discover_restricted_hr_document() -> None:
    """Restricted metadata must not appear in employee results."""
    results = search_documents(
        "How is a leave request processed?",
        "employee",
    )
    result_ids = {result["id"] for result in results}

    assert "HR-001" not in result_ids


def test_hr_adviser_finds_restricted_hr_document() -> None:
    """An authorised HR role should find HR guidance."""
    results = search_documents(
        "How is a leave request processed?",
        "hr_adviser",
    )

    assert results[0]["id"] == "HR-001"