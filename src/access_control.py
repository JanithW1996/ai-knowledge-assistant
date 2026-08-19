"""Enforce role-based document access."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "synthetic"
MANIFEST_PATH = DATA_DIR / "manifest.json"


def load_documents() -> list[dict]:
    """Load document metadata from the manifest."""
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return manifest["documents"]


def get_authorised_documents(role: str) -> list[dict]:
    """Return only documents available to the supplied role."""
    normalised_role = role.strip().lower()

    return [
        document
        for document in load_documents()
        if normalised_role in document["allowed_roles"]
    ]


def read_authorised_document(document_id: str, role: str) -> str:
    """Read a document only when the role is authorised."""
    for document in load_documents():
        if document["id"] != document_id:
            continue

        if role.strip().lower() not in document["allowed_roles"]:
            raise PermissionError(
                f"Role '{role}' cannot access document '{document_id}'."
            )

        document_path = DATA_DIR / document["path"]
        return document_path.read_text(encoding="utf-8")

    raise KeyError(f"Unknown document ID: {document_id}")