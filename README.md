# AI Knowledge Assistant

An Azure-ready governed AI assistant that helps users find information from authorised organisational documents.

## Project goal

Build a secure knowledge assistant demonstrating:

- Microsoft Entra ID authentication
- role-based access control
- secure Azure document storage
- Azure Key Vault secret management
- authorised retrieval before AI generation
- monitoring and cost governance

## Data policy

This project uses synthetic, fictional organisational data only.

Do not add real customer, employee, operational, confidential, personal, or production data.

## Project structure

- `src/` — Python application code
- `tests/` — automated tests
- `data/synthetic/` — fictional project documents
- `docs/` — architecture and governance notes
- `infra/` — Azure infrastructure definitions
- `scripts/` — setup and deployment helpers

## Local document search

Activate the virtual environment, then run:

```powershell
python -m src.app "How should I report a security incident?" --role employee

## Current status

- Day 1 complete: local project foundation, governance, testing, and GitHub setup.
- Day 2 complete: synthetic knowledge documents, classification metadata, dataset validation, and role-based document access.
- Day 3 complete: authorised keyword retrieval, relevance ranking, command-line search, and source references.