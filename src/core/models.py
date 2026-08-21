"""Provider-neutral application models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentMetadata:
    """Metadata required for governed document access."""

    id: str
    title: str
    path: str
    classification: str
    allowed_roles: tuple[str, ...]

@dataclass(frozen=True)
class GenerationRequest:
    """Provider-neutral input for an answer generator."""

    messages: tuple[dict[str, str], ...]
    extractive_fallback: str