# Generation Safety

## Current mode

The application currently uses local extractive answers.

It returns the strongest authorised passage without using an external AI model. This provides a free and predictable baseline for testing the complete governed-answer flow.

## Grounding controls

- authorise documents before retrieval
- use only retrieved passages as context
- limit context size
- require source citations
- abstain when context is unavailable
- label the dataset as fictional
- keep document content separate from trusted instructions

## Primary risks

### Hallucination

An AI model may invent information not supported by the documents.

**Control:** Require answers to use supplied context and abstain when evidence is insufficient.

### Prompt injection

A document may contain instructions intended to override application rules.

**Control:** Treat document content as untrusted data and keep it outside the system message.

### Data leakage

A model may receive information the user is not permitted to access.

**Control:** Apply role-based filtering before reading, searching, or sending document content.

## Future AI provider

An Azure-hosted model can later replace the local extractive mode. The retrieval, access control, context limits, citations, abstention rules, and tests must remain provider-independent.