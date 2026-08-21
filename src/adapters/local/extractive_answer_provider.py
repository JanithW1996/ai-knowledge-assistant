"""Local deterministic answer-provider adapter."""

from src.core.models import GenerationRequest


class LocalExtractiveAnswerProvider:
    """Return the strongest passage without external AI."""

    name = "local_extractive"

    def generate(self, request: GenerationRequest) -> str:
        """Return the approved fallback passage as the answer."""
        return (
            f"{request.extractive_fallback}\n\n"
            "This answer uses fictional demonstration data."
        )