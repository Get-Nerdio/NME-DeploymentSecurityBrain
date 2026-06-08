---
id: identity-and-rbac
title: Hardening — Identity & RBAC
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#azure-permissions, _meta/sources.md#harden-app-service, _meta/sources.md#release-notes]
related: [hardening-checklist, runtime-permissions-core, install-time-permissions, permission-matrix]
---

# Hardening — Identity & RBAC

> Least-privilege guidance for identities and roles. Authoritative permission rows live in
> [permission-matrix.md](../permissions/permission-matrix.md). Source:
> [_meta/sources.md#security-faq], [_meta/sources.md#azure-permissions].

## Reduce elevated install roles
Global Administrator and subscription Owner are needed **only for install/consent**. After
deployment ([_meta/sources.md#security-faq]):
- Reduce the installer's subscription role to **Contributor or User Access Administrator**.
- GA/Owner are **not required** for ongoing management — use NME built-in RBAC + Azure RBAC.
- (Split Identity) remove the temporary **guest deployment admin** and its GA/Owner.

See [install-time-permissions.md](../permissions/install-time-permissions.md) and
[post-install-validation.md](../installation/post-install-validation.md).

## Least-privilege application design
NME requests **application-level permissions only when strictly necessary**; everything else is
**delegated** and bounded by the signed-in user's own rights. ([_meta/sources.md#security-faq])

Optional/negotiable delegated permissions you can omit if the feature isn't used
([_meta/sources.md#security-faq]):
- `Application.ReadWrite.All` — app-registration lifecycle (RBAC Roles feature).
- `AppRoleAssignment.ReadWrite.All` — automated role assignment.
- Trade-off: REST automated user assignment won't function, and Installed-App rulesets may need
  manual re-save.

Reducible **application** permissions (v4.0+): `Group.Read.All` and `User.Read.All` — see
trade-offs in [runtime-permissions-core.md](../permissions/runtime-permissions-core.md).

## Scope of the app's standing Azure rights
The `nerdio-nmw-app` service principal holds **Reader + Backup Reader at subscription scope** and
**Contributor only on the resource groups NME manages** — not Contributor across the whole
subscription. ([_meta/sources.md#azure-permissions]) Full matrix:
[permission-matrix.md](../permissions/permission-matrix.md).

## Console access: enforce MFA
**Nerdio's recommendation is to enforce MFA for every user with access to the NME console.**
The NME App Service is the entry point and is protected by **Entra ID authentication, including
MFA and Conditional Access, by default** — NME hands authentication to Entra and applies whatever
CA/MFA policies the tenant enforces. ([_meta/sources.md#harden-app-service]) Implement via an
Entra **Conditional Access policy requiring MFA** targeting the users/groups entitled to NME (and
the NME enterprise app). This is the single highest-value identity control for console access.

## Separation of duties
The **pre-created Entra app** advanced install separates the Entra admin (registers the app,
grants consent) from the subscription Owner (deploys infrastructure) — useful where one person
should not hold both. See [deployment-models.md](../installation/deployment-models.md).

## NME 8.0 notes
- **Migrate RBAC:** 8.0 adds two migration-specific RBAC definitions — **Read Only** and **Full
  Access** — to be combined with existing AVD Workspace / Windows 365 permissions for granular
  control over who can run migrations. ([_meta/sources.md#release-notes])
- New app registrations use **certificate-based auth** by default (no client secret). See
  [secrets-keyvault.md](secrets-keyvault.md). ([_meta/sources.md#release-notes])

## Open questions
- Map each NME built-in role (WVD/AVD Admin, Desktop Admin, Help Desk, Reviewer, End-User) to its
  capabilities (the app-role IDs are in [_meta/sources.md#create-entra-app]).
