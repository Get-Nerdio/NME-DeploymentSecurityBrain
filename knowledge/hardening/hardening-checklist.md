---
id: hardening-checklist
title: NME Hardening Checklist
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: draft
sources: [_meta/sources.md#security-faq, _meta/sources.md#implementation-guide]
related: [identity-and-rbac, network-isolation, secrets-keyvault, install-time-permissions]
---

# NME Hardening Checklist

> Actionable index for hardening an NME install. Each item links to detail. Source:
> [_meta/sources.md#security-faq].

## Network
- [ ] **Deploy with Private Endpoints** (Secure Deployment — recommended) so NME and its
      dependencies (SQL, Storage, Key Vault, App Service) are not publicly reachable.
      → [network-isolation.md](network-isolation.md)
- [ ] If deployed without PEs, apply the **hardening runbook** post-deployment (v7.4+ supports
      hardened deployment of all core modules **without a hybrid worker VM** for scripts <500 KB).
      → [network-isolation.md](network-isolation.md)
- [ ] Leave **"Restrict App Service public access" unselected at install**; restrict later via the
      supported hardening path. → [network-isolation.md](network-isolation.md)
- [ ] Ensure required Microsoft outbound endpoints remain reachable (service tags / private
      endpoints) for licensing, Azure APIs, logging, and session hosts.

## Identity & least privilege
- [ ] After install, **reduce the installer's subscription role** from Owner to Contributor or
      User Access Administrator; confirm GA/Owner are no longer assigned for ongoing use.
      → [identity-and-rbac.md](identity-and-rbac.md)
- [ ] Govern access via **NME built-in RBAC roles** + Azure RBAC.
      → [identity-and-rbac.md](identity-and-rbac.md)
- [ ] Consider omitting the **optional** delegated permissions (`Application.ReadWrite.All`,
      `AppRoleAssignment.ReadWrite.All`) if RBAC Roles / REST automation isn't needed.
      → [permission-matrix.md](../permissions/permission-matrix.md)
- [ ] (Split Identity) Complete post-install cleanup: remove guest deployment admin and elevated
      roles. → [post-install-validation.md](../installation/post-install-validation.md)

## Secrets & data
- [ ] Confirm secrets/tokens are in **Key Vault**, accessed only via **Managed Identity**.
      → [secrets-keyvault.md](secrets-keyvault.md)
- [ ] Confirm DB encryption at rest (DPS encryption-key storage account) and TLS in transit.
      → [secrets-keyvault.md](secrets-keyvault.md)

## Review & operate
- [ ] Review the Marketplace deployment via **Review + Create** / downloaded ARM template /
      Deployment History.
- [ ] Apply updates using the **least-privilege method** appropriate to the environment (hardened
      environments restore via manual .zip push). → [runtime-permissions-core.md](../permissions/runtime-permissions-core.md)

## Open questions
- Source docs do not detail **MFA/Conditional Access for admin access** or **explicit SQL
  hardening** steps — capture Nerdio's current guidance and add dedicated items.
