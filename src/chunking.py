"""Split documents into small retrievable passages."""


def chunk_text(text: str) -> list[str]:
    """Split text at blank lines regardless of its source platform."""
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    return [
        paragraph.strip()
        for paragraph in normalized_text.split("\n\n")
        if paragraph.strip()
    ]