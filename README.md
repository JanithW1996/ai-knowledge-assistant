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

## Local grounded answer demo

Activate the virtual environment, then run:

```powershell
python -m src.app "How should I report a security incident?" --role employee
```

The current mode is a deterministic local extractive answer, not an external AI model.

Supported fictional roles:

- `employee`
- `manager`
- `hr_adviser`
- `it_support_officer`

The application filters documents by role before calculating relevance.

## Local API demo

Keep `DOCUMENT_REPOSITORY=local` in the ignored `.env` file, then run:

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` to test the local API.

The role in the current API request is for local demonstration only. Do not expose the API publicly until verified Microsoft Entra identities are mapped to trusted roles.

## Presentation interface

Start the local application:

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` for the non-technical presentation interface.

Open `http://127.0.0.1:8000/docs` for the developer API documentation.

The interface supports grounded answers, source citations, safe refusal and demonstration personas.

## Deployment status

The secure Azure data foundation is deployed and contains synthetic documents only.

The API and presentation interface remain local because the current persona selector is not production authentication. Application startup is deliberately blocked in production mode until verified organisational identity is implemented.

See:

- `docs/demo-guide.md` for the presentation walkthrough.
- `docs/final-architecture.md` for the completed system design.
- `docs/api-and-azure-adapter.md` for Azure and API integration details.

## Current status

- Day 1 complete: local project foundation, governance, testing, and GitHub setup.
- Day 2 complete: synthetic knowledge documents, classification metadata, dataset validation, and role-based document access.
- Day 3 complete: authorised keyword retrieval, relevance ranking, command-line search, and source references.
- Day 4 complete: document chunking, authorised passage retrieval, controlled context limits, and precise citations
- Day 5 complete: grounded answer service, safe abstention, prompt boundaries, citations, and local extractive mode.
- Day 6 complete: provider-neutral models, repository and answer ports, local adapters, dependency injection, and future integration boundaries.
- Day 7 complete: Azure CLI and Bicep setup, subscription governance, naming and tags, AUD $10 budget alerts, reviewed infrastructure deployment, and an empty governed resource group.
- Day 8 complete: secure Azure Storage, private document container, managed identity, Key Vault, RBAC, recovery controls, and synthetic document upload.
- Day 9 complete: Azure Blob adapter, passwordless configuration, portable line-ending fix, governed FastAPI endpoints, and 34 passing tests.
- Day 10 complete: presentation interface, production safety lock, automated GitHub testing, container definition, final architecture, and demonstration guide.