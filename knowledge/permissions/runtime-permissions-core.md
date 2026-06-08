---
id: runtime-permissions-core
title: Runtime Permissions — Core NME
domain: permissions
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#azure-permissions, _meta/sources.md#reference-architecture, _meta/sources.md#update-app, _meta/sources.md#release-notes]
related: [permission-matrix, install-time-permissions, identity-and-rbac]
---

# Runtime Permissions — Core NME

> What core NME uses on an ongoing basis after install. Specific permission rows live in
> [permission-matrix.md](permission-matrix.md); per-module runtime permissions are under
> [knowledge/modules/](../modules/).

## The model: managed identity + delegated, not standing admin
- After install and admin consent, **no standing user permissions in Azure are required** to
  manage the AVD environment through NME. Most actions execute **on behalf of the signed-in user**
  (delegated), bounded by that user's own Azure rights. ([_meta/sources.md#azure-permissions], [_meta/sources.md#security-faq])
- NME runs as an **Azure App Service with a Managed Identity**; the Managed Identity is how NME
  reaches Key Vault and applies updates — no stored credentials. ([_meta/sources.md#security-faq])
- **Each identity (user or service principal) receives its own token; tokens are not shared**,
  keeping activity isolated and auditable. ([_meta/sources.md#security-faq])

## Ongoing app-level (application) permissions
A subset of the matrix is **application** type — used without a signed-in user, for background
work: licensing collection, group/user resolution, and (when enabled) Intune/Windows 365
background tasks. The always-on core application permissions are limited (e.g.
`GroupMember.Read.All`, `Organization.Read.All`); the broad Intune/Windows 365 application
permissions are present **only when those features are enabled**. See
[permission-matrix.md](permission-matrix.md) §1.

## Azure RBAC held at runtime
The `nerdio-nmw-app` service principal retains **Reader + Backup Reader** at subscription scope
and **Contributor** on the resource groups it manages, so it can orchestrate AVD resources via
API. Runbooks/scripted actions execute via the Automation Account **in the context of this
service principal.** ([_meta/sources.md#reference-architecture])

## Update operations (least privilege per method)
Applying NME updates does **not** require Global Admin/Owner. Required rights depend on the update
method ([_meta/sources.md#update-app]):

| Method | Required right |
|---|---|
| Deploy button (Automation job) | Contributor **or** Automation Operator on the Automation Account |
| Azure Cloud Shell (v2.10+) | Contributor on the NME App Service |
| Standalone PowerShell | Contributor on the NME deployment resource group |
| Manual .zip push / manual Cloud Shell | Contributor on the NME App Service |

## Reducible permissions
- `Group.Read.All` and `User.Read.All` **application-level** permissions can be removed (v4.0+),
  with trade-offs: REST API can't assign users to host pools without `User.Read.All` (app), and
  Installed-App rulesets must be re-saved after removing `Group.Read.All` (app).
  ([_meta/sources.md#azure-permissions])

## Open questions
- NME 8.0 is Public Preview (GA is v7.7.4); the runtime model is unchanged in the 8.0 release
  notes (8.0 also adds optional user-assigned managed identities for host pools — an AVD resource
  concern, not core NME runtime). Re-verify at 8.0 GA.
