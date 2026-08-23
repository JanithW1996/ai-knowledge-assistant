# Demonstration Guide

## Audience

This demonstration is designed for technical and non-technical viewers, including executives, HR, finance, governance, security and technology teams.

## Opening explanation

The AI Knowledge Assistant helps organisational users find concise guidance from authorised documents.

This portfolio version uses only synthetic, fictional organisational information.

The demonstration focuses on three outcomes:

- provide a grounded answer when authorized evidence exists;
- deny access when relevant information exists but the role is unauthorized;
- safely decline when no relevant evidence exists.

## Suggested demonstration

### 1. Grounded general answer

1. Open the presentation interface.
2. Point out the synthetic-data notice.
3. Select the **Employee** persona.
4. Select **Report a security incident**.
5. Click **Ask assistant**.
6. Show the concise answer, grounded badge and source citation.

Explain that the answer comes from an authorized internal document.

### 2. Safe uncertainty

1. Keep the **Employee** persona.
2. Ask: `What is the office parking fee?`
3. Show the evidence-unavailable response.

Explain that the system does not invent an answer when evidence is missing.

### 3. Departmental access control

1. Select the **Employee** persona.
2. Select **HR leave processing**.
3. Show the access-denied response with no citation.
4. Change the persona to **HR adviser**.
5. Ask the same question again.
6. Show the grounded HR answer and authorized citation.

Explain that changing the trusted role changes which documents can be retrieved.

### 4. Organizational hierarchy

1. Select the **Manager** persona.
2. Select **Management staffing**.
3. Show the grounded management answer.
4. Select the **Senior executive** persona.
5. Ask the same question.
6. Show that the senior executive also receives the answer.

Explain that senior executives inherit appropriate employee and management access.

### 5. Restricted financial summary

1. Select the **Senior executive** persona.
2. Select **Executive financial summary**.
3. Show the grounded answer from `FIN-001`.
4. Select the **Employee** persona.
5. Ask the same question.
6. Show the access-denied response.

Explain that aggregated financial planning information is available only to approved finance and executive roles.

### 6. Highly confidential payroll exception

1. Select the **Senior executive** persona.
2. Select **Confidential payroll review**.
3. Show the access-denied response with no citation.
4. Change the persona to **Finance officer**.
5. Ask the same question again.
6. Show the grounded answer from `FIN-002`.

Explain that organizational seniority does not automatically override highly confidential specialist controls.

## Access model summary

| Scenario | Expected outcome |
|---|---|
| Employee asks a general question | Grounded answer |
| Employee asks an HR question | Access denied |
| HR adviser asks an HR question | Grounded HR answer |
| Manager asks a management question | Grounded management answer |
| Senior executive asks for a finance summary | Grounded finance answer |
| Senior executive asks for payroll controls | Access denied |
| Finance officer asks for payroll controls | Grounded payroll answer |
| Any role asks an unsupported question | Evidence unavailable |

## Key business value

- Users receive quicker access to organizational guidance.
- Answers are linked to authorized evidence.
- Role hierarchy supports appropriate inherited access.
- Departmental controls enforce least privilege.
- Highly confidential information can override executive hierarchy.
- Denied responses reveal no restricted content or citations.
- The assistant declines when evidence is insufficient.
- Cloud identity avoids stored passwords and storage keys.
- The modular design supports Azure Blob Storage, SharePoint, Microsoft 365 and future approved AI providers without rebuilding the core.

## Important security statement

The current persona selector is for a local portfolio demonstration. It is not production authentication.

A production deployment must replace the selector with a verified organizational identity, such as Microsoft Entra ID, and trusted group-to-role mappings.

Users must never be allowed to assign their own production roles.

## Current answer mode

The answer provider is deterministic and extractive. It does not currently call an external AI model.

This keeps the demonstration predictable, inexpensive and easy to audit. A future approved model can be added through the existing answer-provider interface.

## Data statement

The local and Azure demonstration repositories contain seven synthetic documents.

No real employee names, salaries, payroll records, bank details, tax information, customer information or confidential organizational data are used.