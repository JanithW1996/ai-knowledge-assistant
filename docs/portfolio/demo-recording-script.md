# AI Knowledge Assistant — 4-Minute Demonstration Script

## Before recording

- Use the local demonstration interface so you can switch personas quickly.
- Close email, chat and Azure tabs containing account identifiers.
- Zoom the browser to approximately 90% so the question, answer and citation are visible together.
- Keep the architecture diagram and GitHub test result ready in separate tabs.

## 0:00–0:25 — Opening

“Many organisations want the benefits of AI, but they cannot allow every user or every AI service to see every document. I built this AI Knowledge Assistant to demonstrate a safer approach: check access first, retrieve only approved information, and show the evidence behind every answer.”

## 0:25–0:55 — What the system does

“The interface is designed for non-technical staff. A user asks a normal workplace question. The system identifies their trusted role, searches only documents that role may access, and returns a short answer with a source citation. If the information is restricted, it denies access. If reliable evidence does not exist, it safely declines instead of inventing an answer.”

## 0:55–1:25 — Architecture

Show the architecture diagram.

“In the Azure version, Microsoft Entra ID authenticates the user and supplies an application role. The FastAPI application checks that role before retrieval. Documents are held in private Azure Blob Storage, and the application uses managed identity rather than a stored password or storage key. The design uses replaceable adapters, so SharePoint, Microsoft 365 or an approved AI provider could be added later without rebuilding the access-control core.”

## 1:25–2:45 — Demonstrate four outcomes

### Grounded answer

Select **Employee** and ask: `How should I report a security incident?`

“The employee receives an answer from an authorised internal guide. The green badge and citation show that the response is grounded in approved evidence.”

### Departmental restriction

Still as **Employee**, ask: `What details must HR check in a leave request?`

“The employee is denied because the matching procedure is restricted to HR.”

Change to **HR adviser** and ask the same question again.

“The HR adviser can now receive the relevant answer. The access decision changes because the trusted role changed, not because an AI model guessed the permission.”

### Executive exception

Select **Senior executive** and ask: `What payroll amount, reconciliation status and exception count must finance review?`

“Even a senior executive is denied access to highly confidential payroll controls. This demonstrates least privilege and an explicit exception to organisational hierarchy.”

Change to **Finance officer** and repeat the question.

“The finance specialist receives the grounded answer because this role is explicitly authorised.”

### Safe uncertainty

Select **Employee** and ask: `What is the office parking fee?`

“There is no approved evidence for this question, so the assistant declines rather than producing an unsupported response.”

## 2:45–3:25 — Engineering evidence

Show the GitHub Actions result or test output.

“The project includes 102 automated tests covering access control, unauthorised requests, API behaviour, repository adapters, Entra identity parsing and runtime safeguards. Infrastructure is defined with Bicep, and GitHub Actions validates the dataset and test suite on every change.”

## 3:25–4:00 — Close

“This is a portfolio demonstration using only fictional data and deterministic extractive answers, not an external language model. The main achievement is the governed foundation: verified identity, access before retrieval, evidence-based answers, safe denial and a portable Azure architecture. It shows how useful AI services can be introduced without treating security and governance as an afterthought.”

## Recording note

When showing the local persona selector, state that it is only a demonstration control. The deployed Azure version obtains roles from Microsoft Entra ID. Do not show subscription IDs, tenant IDs, personal email addresses or Azure portal account details.
