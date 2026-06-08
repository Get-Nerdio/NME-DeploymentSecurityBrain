---
id: secrets-keyvault
title: Hardening — Secrets & Key Vault
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#reference-architecture, _meta/sources.md#release-notes]
related: [hardening-checklist, identity-and-rbac, nme-components]
---

# Hardening — Secrets & Key Vault

> How NME handles secrets, tokens, certificates, and encryption. Source:
> [_meta/sources.md#security-faq].

## Key Vault
Tokens and secrets are stored in **Azure Key Vault**, which ([_meta/sources.md#security-faq]):
- Encrypts data **at rest and in transit**; the encryption keys themselves are stored/managed
  within the Key Vault service.
- Is accessed **only via Managed Identity under RBAC** — secrets are never exposed in logs, code,
  or environment variables.

## Managed Identity, not stored credentials
NME runs as an App Service with a **Managed Identity** for secure Key Vault access. The Automation
Account also uses a **Managed Identity** (legacy Run-As is deprecated since v5.1). This avoids
standing credentials/certificates that would otherwise need rotation/protection. See
[identity-and-rbac.md](identity-and-rbac.md) and [nme-components.md](../architecture/nme-components.md).

## App registration auth — certificate-based by default (NME 8.0)
**New installs use certificate-based authentication for the app registrations by default,
replacing client secrets.** ([_meta/sources.md#release-notes]) This removes a shared secret from
the deployment and is the more secure default. (This supersedes the older client-secret model;
the pre-created-Entra-app flow that handed over an "Application client secret" reflects the
secret-based path used before 8.0.)

## Token isolation
**Each identity (user or service principal) receives its own token; tokens are not shared**,
keeping activity isolated and auditable. NME does not proxy authentication or RDP traffic.
([_meta/sources.md#security-faq])

## Database encryption
Application data is in **Azure SQL**; the DB **encryption keys are held in a dedicated DPS storage
account** (v5.5+). See [nme-components.md](../architecture/nme-components.md).
([_meta/sources.md#reference-architecture])

## Data shared externally
Only license-tracking metadata leaves the tenant: **tenant ID, subscription ID, NME app
registration ID** — no user, VM, or session data. ([_meta/sources.md#security-faq])

## Open questions
- **Secret/certificate rotation cadence** and **explicit SQL hardening** (private endpoint already
  covered; AAD-only auth, TDE specifics) are not detailed in the ingested sources — capture from
  Nerdio's current security guidance. (Note: 8.0's cert-based default reduces the secret-rotation
  concern for new installs; document the certificate lifecycle/rotation once detailed.)
