"""Tests for the governed HTTP API."""

import base64
import json

from fastapi.testclient import TestClient

import src.api as api_module


client = TestClient(api_module.app)


def encode_entra_principal(
    role: str,
) -> str:
    """Create a synthetic trusted App Service header."""
    principal = {
        "auth_typ": "aad",
        "name_typ": (
            "http://schemas.xmlsoap.org/"
            "ws/2005/05/identity/claims/name"
        ),
        "role_typ": "roles",
        "claims": [
            {
                "typ": (
                    "http://schemas.microsoft.com/"
                    "identity/claims/objectidentifier"
                ),
                "val": "synthetic-user-id",
            },
            {
                "typ": (
                    "http://schemas.xmlsoap.org/"
                    "ws/2005/05/identity/claims/name"
                ),
                "val": "Synthetic User",
            },
            {
                "typ": "roles",
                "val": role,
            },
        ],
    }

    encoded = base64.b64encode(
        json.dumps(principal).encode("utf-8")
    )

    return encoded.decode("ascii")


def test_health_endpoint() -> None:
    """Health checks must not access documents."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "data_policy": "synthetic-fictional-only",
    }


def test_demo_session_allows_role_selection(
    monkeypatch,
) -> None:
    """Local mode should expose the persona selector."""
    monkeypatch.setattr(
        api_module,
        "get_identity_mode",
        lambda: "demo",
    )

    response = client.get("/v1/session")

    assert response.status_code == 200
    assert response.json() == {
        "identity_mode": "demo",
        "role": None,
        "display_name": "Demo user",
        "allow_demo_role_selection": True,
    }


def test_entra_session_returns_trusted_role(
    monkeypatch,
) -> None:
    """Entra mode should return the assigned app role."""
    monkeypatch.setattr(
        api_module,
        "get_identity_mode",
        lambda: "entra",
    )

    response = client.get(
        "/v1/session",
        headers={
            "X-MS-CLIENT-PRINCIPAL": (
                encode_entra_principal(
                    "senior_executive"
                )
            )
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "identity_mode": "entra",
        "role": "senior_executive",
        "display_name": "Synthetic User",
        "allow_demo_role_selection": False,
    }


def test_entra_session_rejects_missing_identity(
    monkeypatch,
) -> None:
    """Entra mode must fail closed without a header."""
    monkeypatch.setattr(
        api_module,
        "get_identity_mode",
        lambda: "entra",
    )

    response = client.get("/v1/session")

    assert response.status_code == 401


def test_demo_answer_uses_selected_role(
    monkeypatch,
) -> None:
    """Local demonstrations may use a selected persona."""

    def fake_answer_question(
        question: str,
        role: str,
    ) -> dict:
        assert question == "How do I report an incident?"
        assert role == "employee"

        return {
            "answer": (
                "Report it to the fictional IT team."
            ),
            "citations": [
                "INT-001#passage-5"
            ],
            "grounded": True,
            "mode": "test-provider",
        }

    monkeypatch.setattr(
        api_module,
        "get_identity_mode",
        lambda: "demo",
    )
    monkeypatch.setattr(
        api_module,
        "answer_question",
        fake_answer_question,
    )

    response = client.post(
        "/v1/answers",
        json={
            "question": "How do I report an incident?",
            "role": "employee",
        },
    )

    assert response.status_code == 200
    assert response.json()["grounded"] is True
    assert response.json()["citations"] == [
        "INT-001#passage-5"
    ]


def test_entra_answer_ignores_selected_role(
    monkeypatch,
) -> None:
    """Production must use the trusted Entra role."""

    def fake_answer_question(
        question: str,
        role: str,
    ) -> dict:
        assert question == "Show the payroll review."
        assert role == "finance_officer"

        return {
            "answer": "Synthetic payroll guidance.",
            "citations": [
                "FIN-002#passage-5"
            ],
            "grounded": True,
            "mode": "test-provider",
        }

    monkeypatch.setattr(
        api_module,
        "get_identity_mode",
        lambda: "entra",
    )
    monkeypatch.setattr(
        api_module,
        "answer_question",
        fake_answer_question,
    )

    response = client.post(
        "/v1/answers",
        headers={
            "X-MS-CLIENT-PRINCIPAL": (
                encode_entra_principal(
                    "finance_officer"
                )
            )
        },
        json={
            "question": "Show the payroll review.",
            "role": "employee",
        },
    )

    assert response.status_code == 200
    assert response.json()["citations"] == [
        "FIN-002#passage-5"
    ]


def test_entra_answer_rejects_missing_identity(
    monkeypatch,
) -> None:
    """Production answers require a verified identity."""
    monkeypatch.setattr(
        api_module,
        "get_identity_mode",
        lambda: "entra",
    )

    response = client.post(
        "/v1/answers",
        json={
            "question": "Show me documents.",
            "role": "employee",
        },
    )

    assert response.status_code == 401


def test_answer_endpoint_rejects_unknown_role() -> None:
    """Callers cannot submit unsupported demo roles."""
    response = client.post(
        "/v1/answers",
        json={
            "question": "Show me documents.",
            "role": "administrator",
        },
    )

    assert response.status_code == 422


def test_answer_endpoint_rejects_empty_question() -> None:
    """Invalid questions are rejected before retrieval."""
    response = client.post(
        "/v1/answers",
        json={
            "question": "",
            "role": "employee",
        },
    )

    assert response.status_code == 422


def test_home_serves_presentation_interface() -> None:
    """Business users receive the presentation interface."""
    response = client.get("/")

    assert response.status_code == 200
    assert "Ask with confidence" in response.text
    assert "Synthetic demonstration data" in response.text


def test_interface_stylesheet_is_available() -> None:
    """Presentation styling must deploy with the API."""
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert response.headers[
        "content-type"
    ].startswith("text/css")
    assert "--navy" in response.text


def test_interface_script_calls_governed_api() -> None:
    """The interface must use governed API endpoints."""
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert 'fetch("/v1/answers"' in response.text
    assert "textContent" in response.text


def test_api_returns_unauthorized_without_citation() -> None:
    """Restricted matches must be denied safely."""
    response = client.post(
        "/v1/answers",
        json={
            "question": (
                "How should a privileged account recovery "
                "request be verified?"
            ),
            "role": "employee",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": (
            "The user is unauthorized to access this data."
        ),
        "citations": [],
        "grounded": False,
        "mode": "unauthorized",
    }


def test_interface_offers_restricted_questions() -> None:
    """The interface should offer governed scenarios."""
    response = client.get("/")

    assert response.status_code == 200
    assert "Try a question:" in response.text
    assert "Restricted demonstrations" not in response.text
    assert "🔒 HR leave processing" in response.text
    assert "🔒 Management staffing" in response.text
    assert "🔒 IT access recovery" in response.text
    assert "🔒 Executive financial summary" in response.text
    assert "🔒 Confidential payroll review" in response.text


def test_interface_supports_access_denied_badge() -> None:
    """The interface should distinguish denied access."""
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "Access denied" in response.text
    assert "access-denied" in response.text