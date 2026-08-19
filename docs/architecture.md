# Architecture

## Planned system

```text
User
  |
  v
Microsoft Entra ID
  |
  v
Python application
  |
  v
Authorisation check
  |
  v
Azure Blob Storage
  |
  v
Approved document content
  |
  v
AI model
  |
  v
Answer with source references