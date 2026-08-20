"""Split documents into small retrievable passages."""


def chunk_text(text: str) -> list[str]:
    """Split text at blank lines and remove empty passages."""
    return [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]