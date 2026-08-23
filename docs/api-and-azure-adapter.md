# API and Azure Blob Adapter

## Purpose

Day 9 connects the portable Python application to Azure Blob Storage and exposes the existing governed answer flow through an HTTP API.

Only synthetic, fictional organisational data is permitted.

## Portable document flow

Local files and Azure Blob both connect through the same `DocumentRepository` interface:

Local files or Azure Blob → DocumentRepository → Retrieval → Grounding → Answer

The `DOCUMENT_REPOSITORY` environment setting selects the adapter. Core retrieval, access control and answer code does not change.

## Authentication

During local development, `DefaultAzureCredential` can use the signed-in Azure CLI user.

When hosted in Azure, the same code can use the user-assigned managed identity. No storage key or application password is required.

## API endpoints

- `GET /health` checks whether the API process is running.
- `POST /v1/answers` accepts a question and demonstration role.
- Responses include the answer, citations, grounding status and provider mode.
- Invalid questions and unsupported roles are rejected automatically.

## Security boundary

The API currently accepts a demonstration role supplied by the caller. It must remain local and must not be exposed publicly until Microsoft Entra authentication maps a verified user identity to trusted application roles.

No CORS access has been enabled.

## Portability fix

Azure Blob preserved Windows `CRLF` line endings, causing the first Azure result to be treated as one large passage.

The shared chunker now normalises Windows, Unix and older line endings. Local, Azure, SharePoint and future adapters therefore inherit the fix.

## Testing

- Azure adapter tests use an in-memory fake container and consume no Azure services.
- API tests do not start a public server.
- Live Azure Blob access was verified using synthetic documents.
- A known Starlette warning remains while its stable testing dependency transitions from `httpx`.