"""Tests for authorised passage retrieval."""

from src.chunking import chunk_text
from src.context_builder import build_context, retrieve_passages


def test_chunk_text_splits_paragraphs() -> None:
    """Blank lines should separate passages."""
    chunks = chunk_text("First paragraph.\n\nSecond paragraph.")

    assert chunks == ["First paragraph.", "Second paragraph."]


def test_security_question_returns_cited_internal_passage() -> None:
    """The strongest passage should come from internal guidance."""
    results = retrieve_passages(
        "How should I report a security incident?",
        "employee",
    )

    assert results[0]["document_id"] == "INT-001"
    assert results[0]["citation"].startswith("INT-001#passage-")
    assert "security" in results[0]["text"].lower()


def test_employee_cannot_retrieve_hr_passages() -> None:
    """Employees must not discover restricted HR passages."""
    results = retrieve_passages(
        "How is a leave request recorded?",
        "employee",
    )

    assert all(
        result["document_id"] != "HR-001"
        for result in results
    )


def test_hr_adviser_retrieves_hr_passage() -> None:
    """The HR role should retrieve relevant restricted content."""
    results = retrieve_passages(
        "How is a leave request recorded?",
        "hr_adviser",
    )

    assert results[0]["document_id"] == "HR-001"
    assert "leave request" in results[0]["text"].lower()

def test_context_contains_citations_without_hr_leakage() -> None:
    """Employee context should cite sources without exposing HR data."""
    context = build_context(
        "How should I report a security incident?",
        "employee",
    )

    assert "[Source: INT-001#passage-" in context
    assert "HR-001" not in context


def test_context_respects_size_limit() -> None:
    """Context must remain within its configured character budget."""
    context = build_context(
        "How should I report a security incident?",
        "employee",
        max_characters=500,
    )

    assert len(context) <= 500