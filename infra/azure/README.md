# Azure Infrastructure

This folder contains Azure-specific infrastructure code. The reusable application core remains provider-neutral.

## Current deployment

The current Bicep template creates only:

- development resource group `rg-aika-dev-aue-001`
- six non-sensitive governance tags

No paid storage, search, compute, or AI service is currently deployed.

## Safe deployment workflow

### 1. Compile locally

`az bicep build --file "infra\azure\main.bicep" --stdout | Out-Null`

### 2. Validate with Azure

`az deployment sub validate --location australiaeast --template-file "infra\azure\main.bicep"`

### 3. Preview changes

`az deployment sub what-if --location australiaeast --template-file "infra\azure\main.bicep"`

Review every creation, modification, and deletion before continuing.

### 4. Deploy reviewed changes

`az deployment sub create --name "aika-dev-foundation" --location australiaeast --template-file "infra\azure\main.bicep"`

## Cost controls

- Azure free-account spending limit remains enabled.
- Monthly subscription budget is AUD $10.
- Actual-cost alerts are configured at 25%, 50%, 75%, 90%, and 100%.
- Budgets send warnings but do not automatically stop resources.
- Cost information can be delayed.
- Unused development resources must be deleted.

## Security rules

- Use synthetic data only.
- Never place secrets or personal data in Bicep files, parameters, tags, outputs, or Git.
- Preview infrastructure changes before deployment.
- Keep Azure-specific code inside `infra/azure` and `src/adapters/azure`.
- Prefer managed identities over stored credentials.