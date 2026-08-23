# Final Architecture

## System flow

Presentation interface or approved client  
↓  
Governed API  
↓  
Verified request and role boundary  
↓  
Access-controlled document list  
↓  
Retrieval and passage ranking  
↓  
Grounded context and answer  
↓  
Answer, citation or safe refusal

## Replaceable integrations

### Document sources

- Local files
- Azure Blob Storage
- Future SharePoint adapter

### Answer providers

- Local extractive provider
- Future approved AI model

### User interfaces

- Presentation website
- Future Microsoft Copilot
- Microsoft Teams
- Other approved clients

## Folder guide

- `src/core` contains provider-neutral data models.
- `src/ports` defines capabilities required by the core.
- `src/adapters` connects external document and answer providers.
- `src/static` contains the presentation interface.
- `src/api.py` exposes the governed application through HTTP.
- `src/dependencies.py` selects configured adapters.
- `data/synthetic` contains invented demonstration documents.
- `tests` checks security and application behaviour.
- `infra/azure` describes Azure resources using Bicep.
- `docs` records architecture, governance and operating decisions.
- `.github/workflows` runs automatic validation and tests.
- `Dockerfile` packages the application for a future cloud runtime.

## Azure foundation

The development resource group contains:

- a user-assigned managed identity;
- a Standard LRS Storage account;
- a private synthetic-document container;
- a Standard Key Vault;
- a read-only Storage RBAC assignment for the application identity.

Azure budget alerts and the subscription spending limit provide cost governance.

## Security controls

- Synthetic fictional data only
- Role-based document filtering
- Grounded answers with citations
- Safe refusal when evidence is insufficient
- Anonymous blob access disabled
- Shared storage keys disabled
- HTTPS and TLS 1.2 required
- Encryption at rest
- Soft-delete recovery controls
- Passwordless Azure authentication
- Secrets and local environment files excluded from Git
- Production startup blocked while identity remains in demo mode

## Current boundary

The cloud data foundation is deployed, while the API and presentation interface remain local.

This is intentional. The current persona selector demonstrates authorization behaviour but does not verify a real user identity.

Before public deployment, Microsoft Entra authentication must be connected and tested. After that, the container and API can be deployed without rewriting the core.