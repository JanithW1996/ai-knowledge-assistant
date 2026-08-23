# Demonstration Guide

## Audience

This demonstration is designed for technical and non-technical viewers, including executives, HR, governance, security and technology teams.

## Opening explanation

The AI Knowledge Assistant helps employees find concise organisational guidance from authorised documents.

This portfolio version uses only synthetic, fictional organisational information.

## Suggested demonstration

1. Open the presentation interface.
2. Point out the synthetic-data notice.
3. Select the Employee demo persona.
4. Ask: `How should I report a security incident?`
5. Show the concise answer, grounded badge and source citation.
6. Ask: `What is the office parking fee?`
7. Show that the assistant safely declines because evidence is unavailable.
8. Explain that different personas receive different authorised documents.
9. Explain that the same core can use Local files, Azure Blob Storage or future SharePoint adapters.

## Key business value

- Employees receive quicker access to organisational guidance.
- Answers are linked to authorised evidence.
- Access rules are checked before documents are retrieved.
- The assistant declines when evidence is insufficient.
- Cloud identity avoids stored passwords and storage keys.
- The modular design supports future platforms without rebuilding the core.

## Important security statement

The current persona selector is for a local portfolio demonstration. It is not production authentication.

Public production deployment is deliberately blocked until a verified organisational identity, such as Microsoft Entra ID, supplies the user's role.

## Current answer mode

The answer provider is deterministic and extractive. It does not currently call an external AI model.

This keeps the demonstration predictable, inexpensive and easy to audit. A future approved model can be added through the existing answer-provider interface.