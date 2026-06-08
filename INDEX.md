# NME Deployment & Security Brain — Router

> **Read this first.** This is the map of the knowledge base. Use it to locate the precise
> file(s) that answer a question, then open those files. Do not scan blindly. Every fact in
> this brain is sourced and dated — prefer cited content over inference, and check
> `last_reviewed` against `applies_to` for the NME version in question.

**Scope:** Nerdio Manager for Enterprise (NME) — installation, hardening, and permissions.
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
- [deployment-models.md](knowledge/installation/deployment-models.md) — supported topologies/options.
- [step-by-step.md](knowledge/installation/step-by-step.md) — the install procedure.
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
