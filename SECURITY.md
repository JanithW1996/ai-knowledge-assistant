# Security Policy

## Project scope

This repository is a portfolio demonstration using synthetic and fictional organisational data only.

Do not submit real employee, customer, financial, cultural, operational, personal or confidential information to this application.

## Reporting a vulnerability

Please do not disclose suspected security vulnerabilities through a public GitHub issue.

Use GitHub's private vulnerability reporting feature:

1. Open the repository's **Security** tab.
2. Select **Advisories**.
3. Select **Report a vulnerability**.

Include:

- a clear description of the issue;
- the affected component;
- steps needed to reproduce it;
- its possible security impact; and
- any suggested mitigation.

## Supported version

Only the latest version on the `main` branch is currently supported.

## Security design

The project demonstrates:

- Microsoft Entra ID authentication;
- role-based access before document retrieval;
- private Azure Blob Storage;
- managed identity instead of embedded cloud credentials;
- controlled denial without restricted-content leakage;
- safe refusal when authorised evidence is unavailable; and
- production runtime safeguards.

## Important limitation

The application relies on the Microsoft Azure App Service authentication boundary when running in Entra mode.

The local persona selector exists only for portfolio demonstrations and must never be treated as production authentication.

## Secrets and sensitive information

Never commit:

- `.env` files;
- passwords or client secrets;
- access tokens;
- storage keys or SAS tokens;
- connection strings;
- private keys;
- personal email addresses; or
- Azure portal screenshots containing account identifiers.

If sensitive information is committed accidentally, revoke or rotate it immediately before removing it from Git history.
