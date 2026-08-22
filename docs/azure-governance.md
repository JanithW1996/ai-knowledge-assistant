# Azure Governance

## Environment

This project uses a development environment containing synthetic data only.

Primary region: `australiaeast`

The region will be rechecked for service availability before deploying search or AI resources.

## Naming pattern

`<resource-type>-<application>-<environment>-<region>-<instance>`

Project abbreviations:

- application: `aika`
- environment: `dev`
- region: `aue`
- first instance: `001`

Initial resource group:

`rg-aika-dev-aue-001`

Some Azure services have different naming restrictions. For example, storage-account names cannot contain hyphens and must be globally unique.

## Required tags

| Tag | Value | Purpose |
|---|---|---|
| `application` | `ai-knowledge-assistant` | Identifies the workload |
| `environment` | `development` | Prevents confusion with production |
| `data-classification` | `synthetic-only` | Records the data boundary |
| `managed-by` | `bicep` | Shows how resources are controlled |
| `purpose` | `portfolio-learning` | Explains why resources exist |
| `cost-control` | `monthly-budget-alerts` | Records the cost-control expectation |

## Rules

- Never place secrets or personal information in names or tags.
- Use infrastructure as code instead of manual resource creation.
- Preview changes before deployment.
- Use low-cost development tiers.
- Delete unused development resources.
- Do not deploy real organisational data.