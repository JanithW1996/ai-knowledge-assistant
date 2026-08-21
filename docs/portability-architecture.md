# Portability Architecture

## Objective

Deploy the same governed knowledge-assistant core through multiple hosting and integration platforms without rebuilding its security and retrieval logic.

## Layers

### Core

Provider-neutral business and security behaviour:

- document metadata
- role-based authorisation
- chunking
- retrieval workflow
- context limits
- grounding
- citations
- abstention

The core must not import Azure, AWS, Google Cloud, SharePoint, or Copilot SDKs.

### Ports

Python interfaces describing capabilities required by the core:

- document repository
- search provider
- answer provider
- identity provider
- audit-event destination

Ports describe what the application needs, not which vendor supplies it.

### Adapters

Provider-specific implementations of ports:

- local files for development
- Azure Storage and Azure AI Search
- SharePoint and Microsoft Graph
- possible future AWS or Google Cloud services

### Interfaces

Ways users or platforms call the application:

- command line
- web API
- Microsoft 365 Copilot plugin
- web or mobile user interface

### Infrastructure

Deployment definitions remain platform-specific:

- `infra/azure`
- possible future `infra/aws`
- possible future `infra/gcp`

## Dependency rule

```text
Interfaces → Core → Ports ← Adapters