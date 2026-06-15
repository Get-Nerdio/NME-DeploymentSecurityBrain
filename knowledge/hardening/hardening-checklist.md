---
id: hardening-checklist
title: NME Hardening Checklist
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#implementation-guide, _meta/sources.md#harden-nme, _meta/sources.md#harden-app-service, _meta/sources.md#harden-sql, _meta/sources.md#harden-storage, _meta/sources.md#harden-keyvault, _meta/sources.md#configure-entra-sql-auth, _meta/sources.md#vnet-firewall, _meta/sources.md#session-host-outbound, _meta/sources.md#customer-data-privacy]
related: [identity-and-rbac, network-isolation, secrets-keyvault, harden-app-service, harden-sql, harden-key-vault, harden-storage-account, configure-entra-sql-auth, firewall-requirements, install-time-permissions, customer-data-privacy]
---

# NME Hardening Checklist

> Actionable index for hardening an NME install. Each item links to detail. Source:
> [_meta/sources.md#security-faq].

## Network
- [ ] **Deploy with Private Endpoints** (Secure Deployment — recommended) so NME and its
      dependencies (SQL, Storage, Key Vault, App Service) are not publicly reachable.
      → [network-isolation.md](network-isolation.md)
- [ ] If deployed without PEs, run the **Enable Private Endpoints** runbook post-deployment (v7.4+
      supports hardened deployment of all core modules **without a hybrid worker VM** for scripts
      <500 KB). → [network-isolation.md](network-isolation.md)
- [ ] Leave **"Restrict App Service public access" unselected at install**; restrict later via the
      supported hardening path. → [network-isolation.md](network-isolation.md)
- [ ] **Harden the App Service:** access restrictions or private endpoint; disable FTP.
      → [harden-app-service.md](harden-app-service.md)
- [ ] **Harden SQL:** restrict to VNet (preferred) or App Service outbound IPs; clear "Allow Azure
      services." → [harden-sql.md](harden-sql.md)
- [ ] **Harden Key Vault:** firewall to VNet, private endpoint, disable public access + trusted
      Microsoft services bypass. → [harden-key-vault.md](harden-key-vault.md)
- [ ] **Harden Storage:** VNet integration + storage firewall; link all session-host subnets for
      FSLogix. → [harden-storage-account.md](harden-storage-account.md)
- [ ] Allow the required outbound endpoints/service tags for the App Service (VNet-integrated) and
      AVD session hosts; remove deprecated agent URLs. → [firewall-requirements.md](firewall-requirements.md)

## Identity & least privilege
- [ ] **Enforce MFA (Conditional Access) for all users with NME console access** — Nerdio's
      recommendation. → [identity-and-rbac.md](identity-and-rbac.md)
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
- [ ] Understand what NME reports to Nerdio's licensing system and confirm no customer data
      leaves the tenant. → [customer-data-privacy.md](customer-data-privacy.md)
- [ ] Confirm secrets/tokens are in **Key Vault**, accessed only via **Managed Identity**.
      → [secrets-keyvault.md](secrets-keyvault.md)
- [ ] Confirm SQL encryption: **TDE** at rest and **TLS** in transit (both on by default).
      → [harden-sql.md](harden-sql.md)
- [ ] Prefer **certificate-based app auth** (NME 8.0 default for new installs).
      → [secrets-keyvault.md](secrets-keyvault.md)
- [ ] Use **Global Secure Variables** for any sensitive runbook inputs (clear-text variables show
      in Automation logs). → [network-isolation.md](network-isolation.md)
- [ ] (If policy requires) switch SQL to **Entra ID authentication** via NME's service principal.
      → [configure-entra-sql-auth.md](configure-entra-sql-auth.md)

## Review & operate
- [ ] Review the Marketplace deployment via **Review + Create** / downloaded ARM template /
      Deployment History.
- [ ] Apply updates using the **least-privilege method** appropriate to the environment (hardened
      environments restore via manual .zip push). → [runtime-permissions-core.md](../permissions/runtime-permissions-core.md)

## Open questions
- Add **CIS hardened images / CIS Intune policies** guidance (Nerdio article referenced but not
  yet ingested).
