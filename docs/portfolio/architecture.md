# Governed AI Knowledge Assistant - architecture

```mermaid
flowchart LR
    U[Staff user] --> E[Microsoft Entra ID]
    E --> A[Azure App Service<br/>Python + FastAPI]
    A --> I[Trusted identity and assigned role]
    I --> C{Authorised for relevant document?}

    C -->|Yes| R[Passage retrieval and ranking]
    C -->|No| D[Access denied<br/>No content or citation returned]

    R --> B[(Private Azure Blob Storage)]
    R --> G[Grounded answer service]
    G --> Q{Reliable evidence available?}
    Q -->|Yes| O[Answer with source citation]
    Q -->|No| N[Evidence unavailable]

    M[User-assigned managed identity] -. passwordless read access .-> B
    K[Azure Key Vault] -. secure configuration boundary .-> A
    P[Ports and adapters] -. replaceable document and answer providers .-> A
    F[Future SharePoint / Microsoft 365 / approved AI provider] -. future adapter .-> P
```

## Reading the diagram

1. Microsoft Entra ID establishes the user identity and assigned application role.
2. The API uses that trusted role instead of accepting a user-selected production role.
3. Access control runs before document retrieval.
4. Only authorised passages can reach the answer service.
5. The service returns a cited answer, an access-denied response or an evidence-unavailable response.
6. Managed identity provides passwordless access to the private Azure document container.
7. Provider-neutral interfaces allow future integrations without replacing the core security rules.
