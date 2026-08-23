"""Validate the synthetic knowledge dataset."""

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "synthetic"
MANIFEST_PATH = DATA_DIR / "manifest.json"

VALID_CLASSIFICATIONS = {
    "public",
    "internal",
    "restricted",
    "highly_confidential",
}

VALID_ROLES = {
    "employee",
    "manager",
    "senior_executive",
    "hr_adviser",
    "it_support_officer",
    "finance_officer",
}


def validate_dataset() -> int:
    """Validate the manifest and return the document count."""
    manifest = json.loads(
        MANIFEST_PATH.read_text(encoding="utf-8")
    )

    if manifest.get("synthetic") is not True:
        raise ValueError(
            "The dataset must be marked as synthetic."
        )

    document_ids = set()

    for document in manifest.get("documents", []):
        document_id = document["id"]

        if document_id in document_ids:
            raise ValueError(
                f"Duplicate document ID: {document_id}"
            )

        document_ids.add(document_id)

        classification = document["classification"]

        if classification not in VALID_CLASSIFICATIONS:
            raise ValueError(
                f"Invalid classification: {document_id}"
            )

        allowed_roles = set(
            document.get("allowed_roles", [])
        )

        if not allowed_roles:
            raise ValueError(
                f"No allowed roles: {document_id}"
            )

        invalid_roles = allowed_roles - VALID_ROLES

        if invalid_roles:
            raise ValueError(
                f"Invalid roles for {document_id}: "
                f"{sorted(invalid_roles)}"
            )

        document_path = (
            DATA_DIR / document["path"]
        ).resolve()

        if not document_path.is_relative_to(
            DATA_DIR.resolve()
        ):
            raise ValueError(
                f"Unsafe document path: {document_id}"
            )

        if not document_path.is_file():
            raise FileNotFoundError(
                f"Missing document: {document_path}"
            )

    return len(document_ids)


if __name__ == "__main__":
    count = validate_dataset()
    print(
        "Dataset validation passed: "
        f"{count} synthetic documents."
    )