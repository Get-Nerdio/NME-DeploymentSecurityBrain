# NME Deployment & Security Brain — Router

> **Read this first.** This is the map of the knowledge base. Use it to locate the precise
> file(s) that answer a question, then open those files. Do not scan blindly. Every fact in
> this brain is sourced and dated — prefer cited content over inference, and check
> `last_reviewed` against `applies_to` for the NME version in question.

**Scope:** Nerdio Manager for Enterprise (NME) — installation, hardening, permissions, and resilience/BCDR.
**Updating the brain (AI agents):** follow [AGENTS.md](AGENTS.md) — the maintenance contract.
**Updating the brain (humans):** see [_meta/contributing.md](_meta/contributing.md).
**Architecture & roadmap:** see [PROJECT_PLAN.md](PROJECT_PLAN.md).

## How to navigate
1. Identify the domain below (installation / permissions / hardening / architecture / modules).
2. Open the specific page. Permission questions almost always resolve to the **single source of
   truth**: [knowledge/permissions/permission-matrix.md](knowledge/permissions/permission-matrix.md).
3. Follow `related:` frontmatter and inline links for adjacent facts.

## Domains

### Installation — [knowledge/installation/](knowledge/installation/)
How to deploy and install NME.
- [prerequisites.md](knowledge/installation/prerequisites.md) — what must exist before install.
- [deployment-models.md](knowledge/installation/deployment-models.md) — the two installation paths + Marketplace topologies/options.
- [step-by-step.md](knowledge/installation/step-by-step.md) — the Marketplace install procedure.
- [terraform-deployment.md](knowledge/installation/terraform-deployment.md) — **alternate** Infrastructure-as-Code path (Private Preview).
- [post-install-validation.md](knowledge/installation/post-install-validation.md) — verify a good install.

### Permissions — [knowledge/permissions/](knowledge/permissions/)
What permissions are required to install NME and what it uses on an ongoing basis.
- **[permission-matrix.md](knowledge/permissions/permission-matrix.md) — SINGLE SOURCE OF TRUTH (canonical table).**
- [install-time-permissions.md](knowledge/permissions/install-time-permissions.md) — needed only during install.
- [runtime-permissions-core.md](knowledge/permissions/runtime-permissions-core.md) — used by core NME ongoing.

### Hardening — [knowledge/hardening/](knowledge/hardening/)
How to secure/harden an NME installation.
- **[hardening-checklist.md](knowledge/hardening/hardening-checklist.md) — actionable index of this domain.**
- [identity-and-rbac.md](knowledge/hardening/identity-and-rbac.md) — least privilege, roles, accounts, **MFA**.
- [network-isolation.md](knowledge/hardening/network-isolation.md) — network exposure, private endpoints, the Enable Private Endpoints runbook.
- [secrets-keyvault.md](knowledge/hardening/secrets-keyvault.md) — secrets, certs, Key Vault, encryption.
- [harden-app-service.md](knowledge/hardening/harden-app-service.md) — access restrictions, private endpoint, disable FTP, VNet integration.
- [harden-sql.md](knowledge/hardening/harden-sql.md) — TLS/TDE defaults, restrict SQL to VNet or App Service IPs.
- [harden-key-vault.md](knowledge/hardening/harden-key-vault.md) — KV firewall + private endpoint, disable public access.
- [harden-storage-account.md](knowledge/hardening/harden-storage-account.md) — VNet integration + storage firewall (FSLogix-safe).
- [configure-entra-sql-auth.md](knowledge/hardening/configure-entra-sql-auth.md) — switch SQL from local auth to NME's Entra service principal.
- [firewall-requirements.md](knowledge/hardening/firewall-requirements.md) — outbound endpoints/service tags for the App Service and AVD session hosts (secure environments).
- [customer-data-privacy.md](knowledge/hardening/customer-data-privacy.md) — what NME reports to Nerdio's licensing system; no customer data collected.

### Resilience & BCDR — [knowledge/resilience/](knowledge/resilience/)
Two independent tracks: NME control-plane HA and session-host/AVD BCDR.
- **[overview.md](knowledge/resilience/overview.md) — orientation: two tracks, four NME protection layers, three BCDR scenarios. Start here.**
- [nme-backup-restore.md](knowledge/resilience/nme-backup-restore.md) — App Service, SQL, and Key Vault backup/restore procedures.
- [nme-zone-resilience.md](knowledge/resilience/nme-zone-resilience.md) — within-region AZ protection: ZRS locks container + zone-redundant App Service Plan + SQL Premium.
- [nme-database-resilience.md](knowledge/resilience/nme-database-resilience.md) — cross-region SQL auto-failover groups (Premium); two-part config walkthrough and gotchas.
- [nme-regional-resilience.md](knowledge/resilience/nme-regional-resilience.md) — full multi-region NME web-app HA via `configure_resilience.ps1` + Azure Front Door (Premium).
- [host-pool-dr.md](knowledge/resilience/host-pool-dr.md) — active-active session-host DR; FSLogix Cloud Cache; per-host-pool configuration (Premium).
- [avd-bcdr-guidance.md](knowledge/resilience/avd-bcdr-guidance.md) — full AVD BCDR: component DR responsibility table; three outage scenarios.

### Architecture — [knowledge/architecture/](knowledge/architecture/)
- [nme-components.md](knowledge/architecture/nme-components.md) — the moving parts of an NME deployment.

### Modules — [knowledge/modules/](knowledge/modules/)
Secondary modules — deployment/security footprint and permissions (permission rows live in the matrix).
- [user-cost-attribution/overview.md](knowledge/modules/user-cost-attribution/overview.md) — `nmw-ccl-app`; Premium-only; per-user cost reporting.
- [intune-insights/overview.md](knowledge/modules/intune-insights/overview.md) — `nmw-ii-app`; Intune endpoint analytics (Eido backend); outbound endpoints.
- [real-time-insights/overview.md](knowledge/modules/real-time-insights/overview.md) — `nmw-rti-app-*`/`nmw-rti-sql*` managed identities; live monitoring.

## Reference
- [_meta/sources.md](_meta/sources.md) — provenance ledger (authoritative source URLs).
- [_meta/glossary.md](_meta/glossary.md) — canonical term definitions.

---
*Pages marked `status: stub` are placeholders awaiting content — see the roadmap in PROJECT_PLAN.md.*
