"""Answer-generation capability required by the core."""

from typing import Protocol

from src.core.models import GenerationRequest


class AnswerProvider(Protocol):
    """Interface implemented by answer-generation adapters."""

    name: str

    def generate(self, request: GenerationRequest) -> str:
        """Generate an answer from governed input."""
        ...