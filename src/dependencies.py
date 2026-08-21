"""Select provider adapters used by the application."""

from pathlib import Path

from src.adapters.local.file_repository import LocalFileRepository
from src.ports.document_repository import DocumentRepository
from src.adapters.local.extractive_answer_provider import (
    LocalExtractiveAnswerProvider,
)
from src.ports.answer_provider import AnswerProvider


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYNTHETIC_DATA_DIRECTORY = PROJECT_ROOT / "data" / "synthetic"


def create_document_repository() -> DocumentRepository:
    """Create the configured document repository."""
    return LocalFileRepository(SYNTHETIC_DATA_DIRECTORY)

def create_answer_provider() -> AnswerProvider:
    """Create the configured answer-generation provider."""
    return LocalExtractiveAnswerProvider()