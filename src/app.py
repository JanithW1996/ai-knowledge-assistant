"""AI Knowledge Assistant entry point."""

from dotenv import load_dotenv


def main() -> None:
    """Start the local development application."""
    load_dotenv()

    print("AI Knowledge Assistant is ready.")
    print("Data policy: synthetic, fictional organisational data only.")


if __name__ == "__main__":
    main()