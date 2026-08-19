# Governance

## Data rules

- Use synthetic, fictional organisational data only.
- Do not use real customer, employee, personal, confidential, or production data.
- Store approved fictional documents only in `data/synthetic`.
- Minimise the information sent to the AI model.
- Define retention and deletion rules before cloud deployment.

## Security rules

- Use individual accounts and multifactor authentication.
- Apply least-privilege Azure RBAC.
- Prefer managed identity instead of passwords or access keys.
- Store unavoidable secrets in Azure Key Vault.
- Never place secrets in code, Git, prompts, or logs.

## AI controls

- Check document access before AI processing.
- Test for prompt injection and unsafe retrieval.
- Show source references with answers.
- Require human review for important decisions.
- Do not treat AI output as guaranteed fact.

## Monitoring and cost

- Record access and security events without logging document content.
- Use resource tags, budgets, and cost alerts.
- Remove unused development resources.

## Initial risks

| Risk | Initial control |
|---|---|
| Secret uploaded to GitHub | Ignore `.env` |
| Real data used accidentally | Synthetic-only policy |
| Excessive Azure permissions | Least-privilege RBAC |
| Unauthorised AI context | Access check before retrieval |
| Unexpected charges | Azure budget alerts |