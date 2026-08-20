"""Search authorised synthetic documents."""

import re

from src.access_control import (
    get_authorised_documents,
    read_authorised_document,
)


STOP_WORDS = {
    "a", "an", "and", "are", "do", "for", "how",
    "i", "in", "is", "of", "the", "to", "what",
    "should",
}


def tokenise(text: str) -> set[str]:
    """Convert text into meaningful lowercase words."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 2
    }


def search_documents(
    question: str,
    role: str,
    limit: int = 3,
) -> list[dict]:
    """Return the most relevant documents permitted for the role."""
    question_terms = tokenise(question)
    results = []

    for document in get_authorised_documents(role):
        content = read_authorised_document(document["id"], role)
        matched_terms = question_terms & tokenise(content)
        score = len(matched_terms)

        if score > 0:
            results.append(
                {
                    "id": document["id"],
                    "title": document["title"],
                    "classification": document["classification"],
                    "score": score,
                    "matched_terms": sorted(matched_terms),
                }
            )

    return sorted(
        results,
        key=lambda result: (-result["score"], result["id"]),
    )[:limit]