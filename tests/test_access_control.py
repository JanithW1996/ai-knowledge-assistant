"""Tests for document access control."""

import pytest

from src.access_control import (
    get_authorised_documents,
    read_authorised_document,
)


def test_employee_sees_public_and_internal_documents() -> None:
    """Employees should see two non-restricted documents."""
    documents = get_authorised_documents("employee")
    document_ids = {document["id"] for document in documents}

    assert document_ids == {"PUB-001", "INT-001"}


def test_hr_adviser_can_read_hr_document() -> None:
    """The HR role should be allowed to read HR guidance."""
    content = read_authorised_document("HR-001", "hr_adviser")

    assert "Fictional HR Leave Processing Guide" in content


def test_employee_cannot_read_hr_document() -> None:
    """An employee must be denied access to restricted HR guidance."""
    with pytest.raises(PermissionError):
        read_authorised_document("HR-001", "employee")