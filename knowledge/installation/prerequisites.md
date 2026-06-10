---
id: prerequisites
title: NME Installation Prerequisites
domain: installation
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#install-prep, _meta/sources.md#install-guide, _meta/sources.md#implementation-guide, _meta/sources.md#release-notes]
related: [deployment-models, step-by-step, install-time-permissions, nme-components]
---

# NME Installation Prerequisites

> What must exist before installing NME (the **Marketplace** path). Permission specifics are in
> [install-time-permissions.md](../permissions/install-time-permissions.md). The **Terraform** path
> has its own tooling/permission prerequisites — see
> [terraform-deployment.md](terraform-deployment.md). The underlying Azure/Entra requirements for a
> working install are shared across both paths.

## Accounts & roles
The installer needs **Global Administrator** (or **Privileged Role Administrator + Cloud
Application Administrator**) in Entra ID **and** **Owner** on the target Azure subscription.
Details and post-install reduction: [install-time-permissions.md](../permissions/install-time-permissions.md).
([_meta/sources.md#install-prep], [_meta/sources.md#install-guide])

## Azure subscription
- Must support deploying **Azure SQL, App Service, Key Vault, Application Insights, and an
  Automation Account** in the selected region. ([_meta/sources.md#install-guide])
- The **Microsoft.DesktopVirtualization** resource provider must be **registered**. ([_meta/sources.md#install-guide])
- Install targets a **new resource group**, or an existing one **only if it is empty**. ([_meta/sources.md#install-guide])

## App Service Plan quota (verify before install)
Check App Service Plan quota for the target subscription **and region** — both the overall plan-VM
limit and the specific SKUs ([_meta/sources.md#install-prep]):

| SKU | Instances | For |
|---|---|---|
| B3 | up to 3 | Main NME app; Intune Insights (optional); Realtime Insights (optional) |
| P0v3 | 1 | Cost Attribution (optional) |

If quota is insufficient, raise a Microsoft support ticket for that subscription/region and notify Nerdio.

## Pre-flight checks
- Run the NME pre-flight PowerShell script (`https://github.com/Get-Nerdio/NME-SE/tree/main/preflight`)
  in the target subscription. It verifies permissions/quota and the ability to create the required
  resources (Log Analytics, Storage, SQL Server + DB, App Service Plan, Automation Account, Key
  Vault) that Azure Policy might block, and reports resource-provider/role state. ([_meta/sources.md#install-prep])
- Run the included **Kusto/Graph query** to surface Azure Policies with a **Deny** effect that
  could block install; exclude/adjust before installing. ([_meta/sources.md#install-prep])

## Networking & AVD-side prerequisites
- A **VNet + subnet** for AVD session-host VMs (selected during config). ([_meta/sources.md#install-guide])
- For AD / Entra DS: subnet DNS must point to a domain-aware DNS server or Azure DNS zone; for
  Windows ADDS, **ADDS must be synced with Entra ID**. ([_meta/sources.md#implementation-guide])
- For Active Directory: an account that can join/unjoin VMs and create/disable computer objects in
  at least one OU. ([_meta/sources.md#install-guide])
- **SMB storage for FSLogix profiles** (file server, Azure Files, Azure NetApp Files, or any UNC
  path, FQDN form) — best practice same region as host pools. Can be deferred and created later by
  NME. ([_meta/sources.md#install-guide])
- Outbound internet from session hosts must match Nerdio's required-endpoints list; the NME App
  Service must reach its required external endpoints (relevant with VNet integration/firewalls).
  Exact endpoints/service tags: [firewall-requirements.md](../hardening/firewall-requirements.md).
  ([_meta/sources.md#install-prep])

## Resources NME will deploy
See [nme-components.md](../architecture/nme-components.md) for the full list (App Service + plan,
Azure SQL, Key Vault, Storage, Automation Account, Application Insights, Log Analytics; plus a DPS
encryption-key storage account on v5.5+).

## Open questions
- NME 8.0 is Public Preview (GA is v7.7.4); quota/SKU figures carry from the current prep doc and
  are unchanged in the 8.0 release notes. Re-verify at 8.0 GA.
