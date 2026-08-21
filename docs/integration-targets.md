# Integration Targets

## Reusable core

The following behaviour must remain platform-neutral:

- document metadata
- role-based authorisation
- retrieval workflow
- chunking and context limits
- grounding and abstention
- citations and security tests

## Local development

Current adapters:

- local Markdown and JSON document repository
- local extractive answer provider

Purpose:

- free development
- predictable testing
- offline demonstrations

## Azure

Planned adapters:

- Azure Blob Storage document repository
- Azure AI Search retrieval provider
- Azure-hosted AI answer provider
- Microsoft Entra identity provider
- Azure monitoring and audit destination

Azure-specific infrastructure will remain under `infra/azure`.

## SharePoint

Planned use:

- SharePoint document libraries as knowledge sources
- Microsoft Graph for authorised document retrieval
- SharePoint permissions mapped to the application's access model

SharePoint-specific code will remain under `src/adapters/microsoft365`.

## Microsoft 365 Copilot

Planned use:

- conversational interface for users
- API plugin calling the governed backend
- optional Copilot connector for indexed external content

Copilot configuration will remain separate from the reusable application core.

## Other clouds

A future provider must implement the same ports for documents, search, answers, identity, and auditing.

Provider changes must not remove access filtering, grounding, citations, context limits, or security tests.