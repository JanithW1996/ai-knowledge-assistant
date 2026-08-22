# Secure Azure Services

## Purpose

Day 8 adds a secure Azure data foundation for the AI Knowledge Assistant. Only synthetic, fictional organisational documents may be uploaded.

## Resources

- User-assigned managed identity for passwordless application authentication
- Standard LRS Storage account for low-cost document storage
- Private blob container named `knowledge-documents`
- Standard Key Vault for future secrets and configuration
- Azure RBAC role assignment allowing the application identity to read blobs

## Storage controls

- Anonymous blob access disabled
- Shared-key authentication disabled
- Microsoft Entra OAuth is the default authentication method
- HTTPS-only traffic
- Minimum TLS version 1.2
- Microsoft-managed encryption
- Seven-day blob and container deletion recovery

The public endpoint remains enabled for development access, but every data request still requires an authorised Microsoft Entra identity. A future production deployment can add private networking.

## Key Vault controls

- Azure RBAC authorization
- Soft delete enabled
- Purge protection enabled
- Seven-day recovery period
- No demonstration secrets are stored

## Access model

- The application managed identity has read-only blob access.
- The project owner has Blob Data Contributor access for uploading synthetic documents.
- Personal account identifiers are not stored in project files.
- Key Vault access will be granted only when the application genuinely needs a secret.

## Cost controls

- The subscription spending limit remains enabled.
- A monthly AUD 10 budget has actual-cost alerts.
- Storage and Key Vault use low-cost standard tiers.
- No external AI model or paid search service was deployed on Day 8.

## Verification

The Bicep template was validated and previewed before deployment. Azure security settings were checked after deployment, and the validated synthetic knowledge documents were uploaded successfully.