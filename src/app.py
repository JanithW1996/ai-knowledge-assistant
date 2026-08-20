"""AI Knowledge Assistant command-line application."""

import argparse

from dotenv import load_dotenv

from src.retrieval import search_documents


VALID_ROLES = [
    "employee",
    "manager",
    "hr_adviser",
    "it_support_officer",
]


def main(
    question: str | None = None,
    role: str = "employee",
) -> None:
    """Search authorised documents for a user's question."""
    load_dotenv()

    print("AI Knowledge Assistant")
    print("Data policy: synthetic, fictional organisational data only.")

    if not question:
        print("Enter a question to search the knowledge base.")
        return

    results = search_documents(question, role)

    if not results:
        print("No authorised matching documents found.")
        return

    print("\nRelevant authorised sources:")

    for result in results:
        matched = ", ".join(result["matched_terms"])
        print(
            f"- {result['id']}: {result['title']} "
            f"(score={result['score']}; matched={matched})"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument(
        "--role",
        choices=VALID_ROLES,
        default="employee",
    )
    arguments = parser.parse_args()

    main(arguments.question, arguments.role)