# Access Control

## Purpose

The AI Knowledge Assistant applies authorization before using document content.

The answer generator must never decide whether access is allowed. Access decisions are made by application policy using a trusted role and each document's permitted roles.

## Classifications

| Classification | Meaning |
|---|---|
| Public | Safe for general viewing |
| Internal | Available to authenticated organisational users |
| Restricted | Available only to approved roles or departments |
| Highly confidential | Available only to explicitly named specialist roles |

## Role hierarchy

| Role | Inherited access |
|---|---|
| Employee | Employee access |
| Manager | Employee and manager access |
| Senior executive | Employee, manager and approved executive access |
| HR adviser | Employee and HR specialist access |
| IT support officer | Employee and IT specialist access |
| Finance officer | Employee and finance specialist access |

Higher organizational authority does not automatically override highly confidential specialist controls.

## Permission matrix

| Document category | Employee | Manager | Senior executive | HR adviser | IT support | Finance officer |
|---|---:|---:|---:|---:|---:|---:|
| Public guidance | Yes | Yes | Yes | Yes | Yes | Yes |
| Internal guidance | Yes | Yes | Yes | Yes | Yes | Yes |
| Management planning | No | Yes | Yes | No | No | No |
| Restricted HR procedure | No | No | Yes | Yes | No | No |
| Restricted IT procedure | No | No | Yes | No | Yes | No |
| Restricted finance summary | No | No | Yes | No | No | Yes |
| Highly confidential payroll review | No | No | No | No | No | Yes |

## Executive exception

Senior executives can review aggregated financial planning information required for strategic decisions.

They cannot access the highly confidential payroll control document. This demonstrates that organizational seniority does not automatically grant access to specialist confidential data.

## Enforcement sequence

```text
Verified role
    ↓
Role hierarchy and document permissions
    ↓
Authorized documents only
    ↓
Relevant passage retrieval
    ↓
Grounded answer and citation
```

If relevant information exists but the role is not permitted, the application returns:

```text
The user is unauthorized to access this data.
```

The response contains no restricted content, document title, document ID or citation.

If no relevant information exists, the application returns a separate evidence-unavailable response.

## Demonstration limitation

The local interface uses selectable personas to demonstrate authorization behavior.

In production, the role selector must be replaced by verified Microsoft Entra identities and trusted group-to-role mappings. A user must never be allowed to assign their own production role.

## Data policy

All documents and scenarios in this project are synthetic and fictional. No real employee, salary, payroll, banking, tax, customer or organizational records may be added.