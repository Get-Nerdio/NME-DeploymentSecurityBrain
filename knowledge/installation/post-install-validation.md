---
id: post-install-validation
title: Post-Install Validation
domain: installation
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#install-guide, _meta/sources.md#split-identity, _meta/sources.md#create-entra-app, _meta/sources.md#release-notes]
related: [step-by-step, hardening-checklist, install-time-permissions]
---

# Post-Install Validation

> How to verify a healthy NME install, then hand off to hardening
> ([hardening-checklist.md](../hardening/hardening-checklist.md)).

## Standard install
- Cloud Shell reports **"Deployment completed successfully"** (or `NMW-After-Publish <RG> <App
  Service>`). ([_meta/sources.md#install-guide])
- The NME URL loads and the registration/configuration wizard is reachable.
- Admin consent completes without error — confirmed via **"I have granted admin consent."**
  ([_meta/sources.md#install-guide])

## Split Identity — verify permissions & consent
([_meta/sources.md#split-identity])
- **Deployment tenant → App Registrations → `nerdio-nmw-app` → API Permissions:** all show a
  **green check**; if not, **Grant admin consent**.
- **Deployment tenant → Enterprise Applications → `nerdio-nmw-app` → Permissions:** each shows a
  value under **"Granted by"**.
- **Identity tenant → Enterprise Applications → `nerdio-nmw-app` → Permissions:** same — all show
  a "Granted by" value.
- **Cleanup (security):** remove GA/Owner from the install accounts; remove the guest deployment
  admin from NME (RBAC Roles > Assignments); delete the guest account from the identity tenant.
  See [install-time-permissions.md](../permissions/install-time-permissions.md).

## Pre-created Entra app — finalize
Confirm each **app role** exists under App Roles; ensure the Enterprise App **"Visible to user? =
Yes."** The Entra admin hands the subscription Owner three values: **Application ID**, the
**credential** (a **certificate** by default in NME 8.0 — formerly an application client secret),
and **Service Principal ID** (Object ID from Enterprise Applications).
([_meta/sources.md#create-entra-app], [_meta/sources.md#release-notes]) See
[secrets-keyvault.md](../hardening/secrets-keyvault.md).

## Open questions
- Define a positive functional smoke test (e.g. create a test host pool) beyond the
  deployment-success signals above.
- NME 8.0 is Public Preview (GA is v7.7.4); re-verify validation steps at GA.
