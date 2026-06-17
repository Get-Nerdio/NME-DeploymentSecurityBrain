---
id: secrets-keyvault
title: Hardening — Secrets & Key Vault
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-17
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#reference-architecture, _meta/sources.md#release-notes, _meta/sources.md#arm-template-77, _meta/sources.md#cloudshell-deploy-script]
related: [hardening-checklist, identity-and-rbac, nme-components]
---

# Hardening — Secrets & Key Vault

> How NME handles secrets, tokens, certificates, and encryption. Source:
> [_meta/sources.md#security-faq].

## Key Vault
Tokens and secrets are stored in **Azure Key Vault**, which ([_meta/sources.md#security-faq]):
- Encrypts data **at rest and in transit**; the encryption keys themselves are stored/managed
  within the Key Vault service.
- Is accessed via the App Service **Managed Identity** and the NME **service principal** — secrets
  are never exposed in logs, code, or environment variables.

**Deploy-time configuration** ([_meta/sources.md#arm-template-77]): **Standard** SKU; **soft-delete
enabled** with **90-day** retention; authorization via **access policies** (RBAC authorization is
**disabled**), not Azure RBAC; and a **`CanNotDelete`** resource lock. Access policies grant the
App Service MI `wrapKey`/`unwrapKey` on keys and `get`/`list`/`set`/`delete` on secrets; the NME
service principal gets `get`/`list` on secrets and `get`/`list`/`create` on certificates.
> Note: this access-policy model differs from the Managed-Identity-under-RBAC phrasing in the
> Security FAQ; the deployed template uses **vault access policies**, not RBAC authorization.

## Managed Identity vs. stored credentials (two patterns)
NME uses **both** patterns, depending on the component ([_meta/sources.md#arm-template-77], [_meta/sources.md#cloudshell-deploy-script]):
- The **App Service** uses a **system-assigned Managed Identity** for Key Vault access (and is the
  SQL Entra admin at deploy time).
- The **Update Automation Account** uses a **system-assigned Managed Identity** (legacy Run-As
  deprecated since v5.1).
- The **Scripted Actions Automation Account** has **no Managed Identity** — it authenticates as the
  `nerdio-nmw-app` service principal using a **stored certificate** (below).

See [identity-and-rbac.md](identity-and-rbac.md) and [nme-components.md](../architecture/nme-components.md).

## What the install provisions for app auth — 7.7 vs 8.0
The ingested deployment artifacts are from the **7.7** release line ([_meta/sources.md#arm-template-77],
[_meta/sources.md#cloudshell-deploy-script]). On **7.7**, the post-install script creates **both** a
client secret **and** a certificate on the `nerdio-nmw-app` app registration:

| Credential (7.7) | Key Vault object | Lifetime | Purpose |
|---|---|---|---|
| **Client secret** | secret `AzureAD--ClientSecret` | **10 years** | App sign-in; **SQL connection string** (`Authentication=Active Directory Service Principal`, `User ID`=appId + this secret), stored as KV secret `ConnectionStrings--DefaultConnection`. |
| **Self-signed certificate** | certificate `nmw-scripted-action-cert` | **120 months (10 yr)**, `ReuseKeyOnRenewal` | Added to the app as a **KeyCredential** (`AsymmetricX509Cert`, usage `Verify`) **and** imported into the Scripted Actions Automation Account as the Automation Certificate asset **`ScriptedActionRunAsCert`** (exportable). This is how scripted actions authenticate as the NME SP. |

> **Version note (resolves an earlier flag).** On **7.7** the app registration is **secret-based**
> for sign-in/SQL, with a separate certificate provisioned for scripted actions. **NME 8.0** changes
> this: new installs use **certificate-based authentication for the app registration by default,
> replacing the client secret** ([_meta/sources.md#release-notes]). So the 7.7 artifact's
> 10-year `AzureAD--ClientSecret` is expected to **go away (or change form) in 8.0**. The
> **scripted-actions certificate** mechanism (KV cert → `ScriptedActionRunAsCert` asset → app
> KeyCredential) is a separate concern and is expected to persist. **Re-verify against an 8.0
> deployment** to confirm exactly how the app-registration credential changes.

During install the script temporarily opens Key Vault (and SQL) public network access from the
installer's IP, then **re-locks** it (disables public access, clears network bypass) on completion
when the resources were hardened. ([_meta/sources.md#cloudshell-deploy-script])

## Token isolation
**Each identity (user or service principal) receives its own token; tokens are not shared**,
keeping activity isolated and auditable. NME does not proxy authentication or RDP traffic.
([_meta/sources.md#security-faq])

## Database encryption & ASP.NET Data Protection
Application data is in **Azure SQL**; the DB **encryption keys are held in a dedicated DPS storage
account** (v5.5+). See [nme-components.md](../architecture/nme-components.md).
([_meta/sources.md#reference-architecture])

The app's **ASP.NET Data Protection keys** are stored as a blob in the DPS storage account
(`dataprotectionkeys` container) and **encrypted (envelope) with an RSA key in Key Vault**
(`DataProtection-<uniqueString>`). The blob is reached via a long-lived SAS URL held in the KV
secret `DataProtection--Storage--Path`; a second `locks` container (SAS in `Deployment--LocksContainerSasUrl`)
provides blob-lease coordination. ([_meta/sources.md#arm-template-77])

## Data shared externally
Only license-tracking metadata leaves the tenant: **tenant ID, subscription ID, NME app
registration ID** — no user, VM, or session data. ([_meta/sources.md#security-faq])

## Open questions
- **Confirm the 8.0 app-registration credential.** 8.0 release notes say cert-based auth replaces
  client secrets; the ingested artifacts are 7.7 (secret-based). Pull an **8.0** ARM template +
  install script to document exactly what replaces `AzureAD--ClientSecret` and how SQL auth works
  without it.
- **Secret/certificate rotation cadence.** On 7.7 both the client secret and the scripted-actions
  certificate are issued for **10 years**; there is no documented rotation procedure in the
  ingested sources. The cert is reused across the app KeyCredential and the Automation Certificate
  asset, so rotation must update both. Capture the lifecycle from Nerdio's guidance.
- **Explicit SQL hardening** beyond what the template sets (Entra-only auth + TLS 1.2 are on by
  default; TDE specifics) — capture from Nerdio's current security guidance.
