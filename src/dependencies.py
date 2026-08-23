"""Select provider adapters used by the application."""

import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from src.adapters.azure.blob_document_repository import (
    AzureBlobDocumentRepository,
)
from src.adapters.local.extractive_answer_provider import (
    LocalExtractiveAnswerProvider,
)
from src.adapters.local.file_repository import LocalFileRepository
from src.ports.answer_provider import AnswerProvider
from src.ports.document_repository import DocumentRepository


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SYNTHETIC_DATA_DIRECTORY = PROJECT_ROOT / "data" / "synthetic"

load_dotenv(PROJECT_ROOT / ".env")


def create_document_repository() -> DocumentRepository:
    """Create the configured document repository."""
    repository_type = os.getenv(
        "DOCUMENT_REPOSITORY",
        "local",
    ).strip().lower()

    if repository_type == "local":
        return LocalFileRepository(SYNTHETIC_DATA_DIRECTORY)

    if repository_type == "azure":
        account_url = os.getenv(
            "AZURE_STORAGE_ACCOUNT_URL",
            "",
        ).strip()
        container_name = os.getenv(
            "AZURE_STORAGE_CONTAINER",
            "knowledge-documents",
        ).strip()
        managed_identity_client_id = os.getenv(
            "AZURE_MANAGED_IDENTITY_CLIENT_ID",
            "",
        ).strip()

        credential = DefaultAzureCredential(
            managed_identity_client_id=(
                managed_identity_client_id or None
            )
        )

        return AzureBlobDocumentRepository(
            account_url=account_url,
            container_name=container_name,
            credential=credential,
        )

    raise ValueError(
        f"Unsupported DOCUMENT_REPOSITORY: {repository_type}"
    )


def create_answer_provider() -> AnswerProvider:
    """Create the configured answer-generation provider."""
    return LocalExtractiveAnswerProvider()