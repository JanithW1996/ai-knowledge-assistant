"""Tests for provider-independent document chunking."""

from src.chunking import chunk_text


def test_chunk_text_supports_windows_line_endings() -> None:
    """Azure blobs may preserve Windows CRLF characters."""
    text = "First paragraph.\r\n\r\nSecond paragraph."

    assert chunk_text(text) == [
        "First paragraph.",
        "Second paragraph.",
    ]


def test_chunk_text_removes_empty_passages() -> None:
    """Extra blank space must not create empty passages."""
    text = "First.\n\n\n\nSecond."

    assert chunk_text(text) == ["First.", "Second."]