"""AI Knowledge Assistant command-line application."""

import argparse

from dotenv import load_dotenv

from src.answer_service import answer_question


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

    result = answer_question(question, role)

    print("\nAnswer:\n")
    print(result["answer"])

    if result["citations"]:
        print("\nSources:")
        for citation in result["citations"]:
            print(f"- {citation}")

    print(f"\nMode: {result['mode']}")

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