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