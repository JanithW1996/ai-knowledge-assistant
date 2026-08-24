# Public Repository Security Review

## Overall result

**Suitable for a public portfolio after the high-priority actions below are completed.**

The reviewed repository contains synthetic documents only. No committed passwords, client secrets, storage keys, SAS tokens, connection strings, private keys, personal email addresses or local `.env` file were found in the current files or the searched Git history. The Azure role-definition GUID present in Bicep is a public Microsoft identifier, not a secret.

## Controls already demonstrated well

- `.env` and environment variants are excluded from Git.
- The dataset is explicitly marked and validated as synthetic.
- Microsoft Entra roles are checked before document retrieval.
- Unauthorised responses contain no document citation or restricted content.
- Azure Blob Storage disallows public blob access and shared-key access.
- The application uses managed identity instead of embedded cloud credentials.
- Production startup requires Entra identity mode.
- GitHub Actions validates the dataset and automated tests.
- The deterministic answer mode avoids unsupported model claims.

## Complete before actively promoting the repository

### 1. Replace the outdated public README

The existing README describes earlier project stages and understates the final Entra-protected deployment. Replace it with the recruiter-focused README in this portfolio package. Keep the statement that the current answer provider is deterministic and extractive.

### 2. Add a security policy

Add `SECURITY.md` explaining how vulnerabilities should be reported. Enable GitHub private vulnerability reporting so reporters do not publish security details in an issue.

### 3. Add a licence

Choose and add a licence before inviting reuse. An MIT licence is common for portfolio software, but only select it if you are comfortable allowing broad reuse with attribution.

### 4. Verify the App Service authentication boundary

The application trusts the App Service identity header in Entra mode. Confirm that Azure App Service Authentication requires sign-in and returns HTTP 401 for unauthenticated requests. Do not expose the Python service through another route that bypasses this platform control. For a broader production deployment, validate signed tokens and their issuer, audience and expiry in the application as defence in depth.

### 5. Remove identifying screenshots and logs

Before posting links, inspect repository issues, pull requests, releases and documentation for subscription IDs, tenant IDs, email addresses, portal screenshots and deployment logs. Azure subscription IDs are not passwords, but there is no benefit in publishing them.

## Recommended next security improvements

| Priority | Improvement | Why it matters |
|---|---|---|
| High | Pin GitHub Actions to immutable commit SHAs | Reduces workflow supply-chain risk. |
| High | Lock Python dependencies and add Dependabot or `pip-audit` | Makes builds reproducible and identifies vulnerable packages. |
| High | Manage App Service Authentication in infrastructure as code | Reduces configuration drift between portal and Bicep. |
| Medium | Add CodeQL or Bandit scanning | Adds automated static security analysis. |
| Medium | Add security response headers such as CSP and HSTS | Hardens the browser-facing interface. |
| Medium | Add request limits, rate limiting and security-focused audit events | Helps protect and investigate a shared deployment. |
| Medium | Restrict Storage and Key Vault networking or use private endpoints | Reduces public network exposure beyond identity controls. |
| Medium | Align CI and App Service Python versions | Reduces deployment-only incompatibilities. |
| Low | Add retention and privacy guidance for future telemetry | Prevents accidental collection of sensitive user questions. |

## Important portfolio wording

Use these claims:

- “Entra-protected Azure App Service demonstration”
- “Role-based access is enforced before retrieval”
- “Private Blob Storage is accessed using managed identity”
- “Deterministic extractive answer provider with citations”
- “Designed for future approved AI and SharePoint adapters”

Avoid these claims:

- “Production-ready enterprise AI”
- “The system currently uses a generative AI model”
- “Key Vault stores all application secrets” unless that is implemented and verified
- “Zero risk” or “fully secure”

## Final public-release checklist

- [ ] Recruiter-focused README is live.
- [ ] `SECURITY.md` and a licence are added.
- [ ] App Service unauthenticated requests return 401.
- [ ] No identifying screenshots or logs remain public.
- [ ] Repository secret scanning and private vulnerability reporting are enabled.
- [ ] The latest GitHub Actions run is green.
- [ ] The public demonstration contains fictional data only.
