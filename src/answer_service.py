"""Create grounded answers using replaceable providers."""

from src.context_builder import (
    build_context,
    get_unauthorised_relevance_score,
    retrieve_passages,
)
from src.core.models import GenerationRequest
from src.dependencies import create_answer_provider
from src.ports.answer_provider import AnswerProvider
from src.prompt_builder import build_messages


ABSTENTION_MESSAGE = (
    "I do not have enough authorised information to answer that question."
)

UNAUTHORISED_MESSAGE = (
    "The user is unauthorized to access this data."
)


def answer_question(
    question: str,
    role: str,
    provider: AnswerProvider | None = None,
) -> dict:
    """Return a grounded provider answer, denial or safe abstention."""
    passages = retrieve_passages(question, role)

    unauthorised_score = get_unauthorised_relevance_score(
        question,
        role,
    )
    authorised_score = passages[0]["score"] if passages else 0

    if (
        unauthorised_score >= 2
        and unauthorised_score > authorised_score
    ):
        return {
            "answer": UNAUTHORISED_MESSAGE,
            "citations": [],
            "grounded": False,
            "mode": "unauthorized",
        }

    if not passages:
        return {
            "answer": ABSTENTION_MESSAGE,
            "citations": [],
            "grounded": False,
            "mode": "abstention",
        }

    context = build_context(question, role)
    messages = build_messages(question, context)
    strongest_passage = passages[0]
    selected_provider = provider or create_answer_provider()

    request = GenerationRequest(
        messages=tuple(messages),
        extractive_fallback=strongest_passage["text"],
    )

    return {
        "answer": selected_provider.generate(request),
        "citations": [strongest_passage["citation"]],
        "grounded": True,
        "mode": selected_provider.name,
    }