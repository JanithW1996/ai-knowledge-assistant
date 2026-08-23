"""Tests for the governed HTTP API."""

from fastapi.testclient import TestClient

import src.api as api_module


client = TestClient(api_module.app)


def test_health_endpoint() -> None:
    """Health checks must not access documents or external services."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "data_policy": "synthetic-fictional-only",
    }


def test_answer_endpoint_returns_stable_contract(
    monkeypatch,
) -> None:
    """Approved clients receive a predictable JSON structure."""

    def fake_answer_question(question: str, role: str) -> dict:
        assert question == "How do I report an incident?"
        assert role == "employee"

        return {
            "answer": "Report it to the fictional IT team.",
            "citations": ["INT-001#passage-5"],
            "grounded": True,
            "mode": "test-provider",
        }

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


def test_answer_endpoint_rejects_unknown_role() -> None:
    """A caller cannot invent an unsupported demonstration role."""
    response = client.post(
        "/v1/answers",
        json={
            "question": "Show me documents.",
            "role": "administrator",
        },
    )

    assert response.status_code == 422


def test_answer_endpoint_rejects_empty_question() -> None:
    """Invalid questions are rejected before retrieval begins."""
    response = client.post(
        "/v1/answers",
        json={
            "question": "",
            "role": "employee",
        },
    )

    assert response.status_code == 422

def test_home_serves_presentation_interface() -> None:
    """Business users receive the non-technical interface."""
    response = client.get("/")

    assert response.status_code == 200
    assert "Ask with confidence" in response.text
    assert "Synthetic demonstration data" in response.text


def test_interface_stylesheet_is_available() -> None:
    """The presentation styling must be deployable with the API."""
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/css")
    assert "--navy" in response.text


def test_interface_script_calls_governed_api() -> None:
    """The browser interface must use the governed answer endpoint."""
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert 'fetch("/v1/answers"' in response.text
    assert "textContent" in response.text


def test_api_returns_unauthorized_without_citation() -> None:
    """The API must deny a strong restricted match safely."""
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
    response = client.get("/")

    assert response.status_code == 200
    assert "Try a question:" in response.text
    assert "Restricted demonstrations" not in response.text
    assert "🔒 HR leave processing" in response.text
    assert "🔒 Management staffing" in response.text
    assert "🔒 IT access recovery" in response.text


def test_interface_supports_access_denied_badge() -> None:
    """The browser script visually distinguishes denied access."""
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "Access denied" in response.text
    assert "access-denied" in response.text