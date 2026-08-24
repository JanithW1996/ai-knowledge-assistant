# LinkedIn Post

I recently completed a project that helped me explore an important question: how can an organisation use AI without giving every user access to every document?

I built a governed AI Knowledge Assistant using Python, FastAPI and Microsoft Azure.

The system:

- signs users in through Microsoft Entra ID;
- checks their role before retrieving documents;
- answers only from information they are authorised to access;
- includes a source citation with supported answers;
- clearly denies restricted requests; and
- declines when approved evidence is unavailable.

I also added an important hierarchy exception: senior executives can access restricted financial planning information, but highly confidential payroll controls remain available only to finance personnel.

The Azure solution uses private Blob Storage, managed identity, Key Vault, App Service and Bicep infrastructure. Its modular design can support future SharePoint, Microsoft 365 or approved AI integrations without rebuilding the governance core.

To make the project reliable, I created 102 automated tests and a GitHub Actions workflow. All organisational data in the demonstration is fictional.

My biggest learning was that responsible AI is not only about the model. Identity, permissions, evidence, safe refusal and auditability need to be part of the design from the beginning.

Project: https://github.com/JanithW1996/ai-knowledge-assistant

#ResponsibleAI #MicrosoftAzure #Python #FastAPI #MicrosoftEntra
