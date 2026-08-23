"""Tests for document access control."""

import pytest

from src.access_control import (
    get_authorised_documents,
    get_effective_roles,
    read_authorised_document,
)


def get_document_ids(role: str) -> set[str]:
    """Return document IDs visible to a demonstration role."""
    documents = get_authorised_documents(role)

    return {
        document.id
        for document in documents
    }


def test_employee_sees_public_and_internal_documents() -> None:
    """Employees should see only general documents."""
    assert get_document_ids("employee") == {
        "PUB-001",
        "INT-001",
    }


def test_manager_inherits_employee_access() -> None:
    """Managers should receive general and management access."""
    assert get_effective_roles("manager") == {
        "employee",
        "manager",
    }

    assert get_document_ids("manager") == {
        "PUB-001",
        "INT-001",
        "MGR-001",
    }


def test_senior_executive_inherits_management_access() -> None:
    """Senior executives should inherit lower-level access."""
    assert get_effective_roles(
        "senior_executive"
    ) == {
        "employee",
        "manager",
        "senior_executive",
    }


def test_senior_executive_sees_broad_restricted_data() -> None:
    """Executives should see approved strategic information."""
    assert get_document_ids(
        "senior_executive"
    ) == {
        "PUB-001",
        "INT-001",
        "HR-001",
        "MGR-001",
        "IT-001",
        "FIN-001",
    }


def test_senior_executive_cannot_read_payroll() -> None:
    """Executive authority must not override payroll privacy."""
    with pytest.raises(
        PermissionError,
        match=(
            "The user is unauthorized "
            "to access this data."
        ),
    ):
        read_authorised_document(
            "FIN-002",
            "senior_executive",
        )


def test_finance_officer_sees_both_finance_documents() -> None:
    """Finance officers should see finance and general data."""
    assert get_document_ids(
        "finance_officer"
    ) == {
        "PUB-001",
        "INT-001",
        "FIN-001",
        "FIN-002",
    }


def test_finance_officer_can_read_payroll() -> None:
    """Finance officers may read payroll control guidance."""
    content = read_authorised_document(
        "FIN-002",
        "finance_officer",
    )

    assert "Fictional Payroll Control Review" in content


def test_hr_adviser_can_read_hr_document() -> None:
    """HR advisers should be allowed to read HR guidance."""
    content = read_authorised_document(
        "HR-001",
        "hr_adviser",
    )

    assert "Fictional HR Leave Processing Guide" in content


@pytest.mark.parametrize(
    ("role", "expected_ids"),
    [
        (
            "hr_adviser",
            {
                "PUB-001",
                "INT-001",
                "HR-001",
            },
        ),
        (
            "it_support_officer",
            {
                "PUB-001",
                "INT-001",
                "IT-001",
            },
        ),
        (
            "finance_officer",
            {
                "PUB-001",
                "INT-001",
                "FIN-001",
                "FIN-002",
            },
        ),
    ],
)
def test_specialists_see_only_their_approved_areas(
    role: str,
    expected_ids: set[str],
) -> None:
    """Specialists must not see another department's data."""
    assert get_document_ids(role) == expected_ids


@pytest.mark.parametrize(
    "role",
    [
        "employee",
        "manager",
        "senior_executive",
        "hr_adviser",
        "it_support_officer",
    ],
)
def test_non_finance_roles_cannot_read_payroll(
    role: str,
) -> None:
    """Highly confidential payroll remains finance-only."""
    with pytest.raises(
        PermissionError,
        match=(
            "The user is unauthorized "
            "to access this data."
        ),
    ):
        read_authorised_document(
            "FIN-002",
            role,
        )