"""Build authorised, relevant context for an AI model."""

from src.access_control import (
    get_authorised_documents,
    read_authorised_document,
)
from src.chunking import chunk_text
from src.retrieval import tokenise


def retrieve_passages(
    question: str,
    role: str,
    limit: int = 3,
) -> list[dict]:
    """Return the strongest authorised passages."""
    question_terms = tokenise(question)
    passages = []

    for document in get_authorised_documents(role):
        content = read_authorised_document(document.id, role)

        for number, text in enumerate(chunk_text(content), start=1):
            matched_terms = question_terms & tokenise(text)
            score = len(matched_terms)

            if score == 0:
                continue

            passages.append(
                {
                    "citation": f"{document.id}#passage-{number}",
                    "document_id": document.id,
                    "title": document.title,
                    "classification": document.classification,
                    "score": score,
                    "matched_terms": sorted(matched_terms),
                    "text": text,
                }
            )

    return sorted(
        passages,
        key=lambda passage: (
            -passage["score"],
            passage["citation"],
        ),
    )[:limit]

def build_context(
    question: str,
    role: str,
    limit: int = 3,
    max_characters: int = 2000,
) -> str:
    """Format relevant passages within a controlled size limit."""
    passages = retrieve_passages(question, role, limit)
    blocks = []

    for passage in passages:
        block = (
            f"[Source: {passage['citation']} | "
            f"Title: {passage['title']}]\n"
            f"{passage['text']}"
        )

        candidate = "\n\n".join([*blocks, block])

        if len(candidate) <= max_characters:
            blocks.append(block)

    return "\n\n".join(blocks)