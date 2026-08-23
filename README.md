# AI Knowledge Assistant

An Azure-ready governed knowledge assistant that retrieves concise answers from authorized organizational documents.

## Project goal

Demonstrate how an enterprise knowledge assistant can combine:

- role-based document access;
- organizational hierarchy;
- departmental restrictions;
- document sensitivity levels;
- authorized retrieval before answer generation;
- grounded answers with citations;
- safe access denial and evidence-unavailable responses;
- secure Azure document storage;
- managed identity and passwordless Azure access;
- Azure Key Vault, infrastructure-as-code and cost governance;
- replaceable local, Azure, Microsoft 365 and AI-provider adapters.

Microsoft Entra authentication is the planned production identity source. The current local persona selector demonstrates authorization behavior only.

## Data policy

This project uses synthetic, fictional organizational data only.

Do not add real customer, employee, salary, payroll, banking, tax, operational, confidential, personal or production information.

## Project structure

- `src/` — Python application and interface code
- `tests/` — automated security and behavior tests
- `data/synthetic/` — invented organizational documents
- `docs/` — architecture, governance and demonstration guidance
- `infra/` — Azure Bicep infrastructure definitions
- `scripts/` — setup and deployment helpers

## Synthetic knowledge base

The demonstration contains seven fictional documents:

- public company overview;
- internal workplace guide;
- restricted HR leave procedure;
- restricted management workforce-planning procedure;
- restricted IT privileged-access recovery procedure;
- restricted financial planning summary;
- highly confidential payroll control review.

The same synthetic dataset is stored locally and in the governed Azure Blob Storage container.

## Supported demonstration roles

- `employee`
- `manager`
- `senior_executive`
- `hr_adviser`
- `it_support_officer`
- `finance_officer`

## Access model

| Document category | Employee | Manager | Senior executive | Specialist |
|---|---:|---:|---:|---:|
| Public and internal guidance | Yes | Yes | Yes | Yes |
| Management planning | No | Yes | Yes | No |
| Restricted HR procedure | No | No | Yes | HR only |
| Restricted IT procedure | No | No | Yes | IT only |
| Restricted finance summary | No | No | Yes | Finance only |
| Highly confidential payroll review | No | No | No | Finance only |

Senior executives inherit appropriate employee and manager access but do not inherit finance-only payroll access.

See `docs/access-control.md` for the complete policy.

## Answer outcomes

The application produces three controlled outcomes:

1. **Grounded answer** — authorized evidence exists, so the response includes a citation.
2. **Access denied** — relevant information exists, but the role is unauthorized. No restricted content or citation is returned.
3. **Evidence unavailable** — no relevant authorized information exists, so the assistant safely declines.

## Local command-line demo

Activate the virtual environment, then run:

```powershell
python -m src.app "How should I report a security incident?" --role employee
```

Example hierarchy demonstration:

```powershell
python -m src.app "What financial planning information may senior executives review?" --role senior_executive
```

Example confidentiality exception:

```powershell
python -m src.app "What payroll amount, reconciliation status and exception count must finance review?" --role senior_executive
```

The current answer provider is deterministic and extractive. It does not call an external AI model.

## Presentation interface

Keep `DOCUMENT_REPOSITORY=local` in the ignored `.env` file, then run:

```powershell
python -m uvicorn src.api:app --host 127.0.0.1 --port 8000
```

Open:

- `http://127.0.0.1:8000` for the non-technical presentation interface;
- `http://127.0.0.1:8000/docs` for the developer API documentation;
- `http://127.0.0.1:8000/health` for the health endpoint.

The interface demonstrates:

- general grounded answers;
- safe uncertainty;
- departmental restrictions;
- role hierarchy;
- executive financial access;
- finance-only payroll access;
- citations without restricted-data leakage.

## Testing

Validate the synthetic dataset:

```powershell
python src/validate_data.py
```

Run the complete automated test suite:

```powershell
python -m pytest
```

Current verified result:

```text
Dataset validation passed: 7 synthetic documents.
83 tests passed.
```

## Azure foundation

The deployed Azure development foundation includes:

- governed resource group;
- required governance tags;
- Azure Storage account;
- private blob container;
- user-assigned managed identity;
- role-based storage access;
- Azure Key Vault;
- recovery protections;
- Bicep infrastructure definitions;
- AUD $10 monthly budget and alerts.

The Azure Blob container contains the same seven synthetic documents used by the local application.

No storage keys, passwords, connection strings or personal email addresses belong in GitHub.

## Portability

The core application depends on provider-neutral interfaces.

Current adapters include:

- local filesystem document repository;
- Azure Blob Storage document repository;
- local deterministic answer provider.

Planned adapters can support:

- Microsoft SharePoint;
- Microsoft 365 and Copilot integrations;
- approved external AI providers;
- other cloud document repositories.

This design allows new platforms to replace adapters without rebuilding authorization, retrieval and answer-generation rules.

## Production security boundary

The local persona selector is not authentication.

Do not expose the application as a production service until:

- Microsoft Entra authenticates the user;
- trusted groups are mapped to application roles;
- users cannot select their own roles;
- network controls are reviewed;
- logging and monitoring are enabled;
- security and privacy reviews are completed.

Application startup is deliberately blocked in production mode until verified organizational identity is configured.

## Documentation

- `docs/access-control.md` — hierarchy, classifications and permission matrix
- `docs/demo-guide.md` — recruiter-friendly demonstration walkthrough
- `docs/final-architecture.md` — completed architecture
- `docs/api-and-azure-adapter.md` — API and Azure repository integration
- `docs/azure-governance.md` — Azure governance controls
- `docs/azure-secure-services.md` — storage, identity and Key Vault design
- `docs/portability-architecture.md` — ports-and-adapters design
- `docs/integration-targets.md` — future deployment targets

## Project milestones

- **Day 1:** repository, environment, governance and testing foundation
- **Day 2:** synthetic data, classifications and role-based access
- **Day 3:** authorized retrieval and source references
- **Day 4:** passage chunking and controlled context
- **Day 5:** grounded answers, citations and safe abstention
- **Day 6:** portable ports-and-adapters architecture
- **Day 7:** Azure governance, Bicep, tags and budget controls
- **Day 8:** secure Azure Storage, Key Vault, identity and RBAC
- **Day 9:** Azure Blob adapter and governed FastAPI endpoints
- **Day 10:** presentation interface, runtime safeguards, CI and container definition
- **Enhancement:** explicit unauthorized responses, expanded restricted scenarios, organizational hierarchy, finance sensitivity levels, seven synthetic documents and 83 passing tests