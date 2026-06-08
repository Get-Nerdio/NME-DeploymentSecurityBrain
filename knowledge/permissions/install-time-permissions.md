---
id: install-time-permissions
title: Install-Time Permissions
domain: permissions
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#azure-permissions, _meta/sources.md#security-faq, _meta/sources.md#install-guide, _meta/sources.md#release-notes]
related: [permission-matrix, prerequisites, runtime-permissions-core, identity-and-rbac]
---

# Install-Time Permissions

> Elevated rights needed only during installation/configuration and **reducible afterward**.
> Specific app permission rows live in [permission-matrix.md](permission-matrix.md); this page
> covers what the **human installer** needs and why it's temporary.

## What the installer needs
The Entra ID user performing the install requires **both**:

1. **Global Administrator** in Entra ID — *or* the combination **Privileged Role Administrator +
   Cloud Application Administrator**. ([_meta/sources.md#azure-permissions], [_meta/sources.md#install-guide])
2. **Owner** on the Azure subscription where NME is installed. ([_meta/sources.md#azure-permissions])

## Why each is needed — and why it's temporary
- **Global Administrator** is used **once, at the end of install**, to grant tenant-level
  **admin consent** to the NME enterprise app's required permissions (all **Application**-type
  Graph permissions in the matrix require this). After consent, NME runs under its own **Managed
  Identity** and needs no further Global Admin access. ([_meta/sources.md#security-faq])
- **Subscription Owner** is required to create/configure the Azure resources (App Service, Azure
  SQL, Key Vault, Storage Account) and to register the SaaS billing object. ([_meta/sources.md#security-faq])

## Reducing permissions after install
- After deployment, the installer's subscription role **can be reduced to Contributor or User
  Access Administrator**, aligning with least privilege. ([_meta/sources.md#security-faq])
- **Global Administrator and subscription Owner are no longer required** for ongoing management;
  day-to-day access is governed by NME's built-in RBAC roles and Azure RBAC. See
  [runtime-permissions-core.md](runtime-permissions-core.md).
- In the **Split Identity** model, post-install cleanup explicitly removes GA/Owner from the
  install accounts and deletes the temporary guest deployment admin. See
  [post-install-validation.md](../installation/post-install-validation.md).

## Admin consent
All **Application** (app-only) Graph permissions, plus `TenantCreator` (AVD Classic) and the
`RestClient` role, require **Global Administrator admin consent**. In the separation-of-duties
advanced install, the Entra ID admin (not the subscription owner) creates the app registration
and grants consent. ([_meta/sources.md#security-faq], [_meta/sources.md#create-entra-app])

## App authentication (NME 8.0)
**New installs use certificate-based authentication for the app registrations by default**,
replacing client secrets — a more secure default with no shared secret to store or rotate.
([_meta/sources.md#release-notes]) See [secrets-keyvault.md](../hardening/secrets-keyvault.md).

## Configuration-action permissions (signed-in user)
Certain post-install "linking"/creation actions require the **signed-in user** (not the app) to
hold specific Azure roles on the targeted resource — e.g. link a resource group / network /
additional subscription, switch the AVD object model, create Azure Files or NetApp shares, create
AVD ARM host pools, associate session-host VMs. ([_meta/sources.md#azure-permissions])

## Open questions
- **Per-action role/scope table:** the source PDF's role column did not render. Capture the exact
  required role + scope per configuration action from the live Azure Permissions doc / RBAC
  articles (also tracked in [permission-matrix.md](permission-matrix.md)).
- NME 8.0 is Public Preview (GA is v7.7.4); installer-role requirements are unchanged in the 8.0
  release notes. Re-verify at 8.0 GA.
