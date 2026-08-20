"""Create grounded answers from authorised context."""

from src.context_builder import build_context, retrieve_passages
from src.prompt_builder import build_messages


ABSTENTION_MESSAGE = (
    "I do not have enough authorised information to answer that question."
)


def answer_question(question: str, role: str) -> dict:
    """Return an extractive grounded answer or safely abstain."""
    passages = retrieve_passages(question, role)

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

    return {
        "answer": (
            f"{strongest_passage['text']}\n\n"
            "This answer uses fictional demonstration data."
        ),
        "citations": [strongest_passage["citation"]],
        "grounded": True,
        "mode": "local_extractive",
        "messages": messages,
    }