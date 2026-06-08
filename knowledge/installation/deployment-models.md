---
id: deployment-models
title: NME Deployment Models
domain: installation
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#install-guide, _meta/sources.md#adv-install, _meta/sources.md#create-entra-app, _meta/sources.md#split-identity, _meta/sources.md#reference-architecture, _meta/sources.md#release-notes]
related: [prerequisites, step-by-step, nme-components, install-time-permissions]
---

# NME Deployment Models

> Supported installation methods and when to use each. Advanced methods should be used only in
> special circumstances and with Nerdio Support guidance (nme.support@getnerdio.com).

## Standard (Azure Marketplace) deploy
The default, most common path. Deploy from Azure Marketplace, then initialize via **Azure Cloud
Shell** (PowerShell). Creates the default Entra app `nerdio-nmw-app`. Installed and billed through
Azure Marketplace. ([_meta/sources.md#install-guide]) Full steps:
[step-by-step.md](step-by-step.md).

## Advanced methods

### 1. Custom Entra ID application name
Change the default app name `nerdio-nmw-app` to a custom value. **Use when installing multiple NME
instances into the same Entra tenant.** Done via *Show advanced* → enter name → **Download script
(Az)** → run in **local PowerShell** (`deploy-az.ps1`; **cannot use Cloud Shell**). ([_meta/sources.md#adv-install])

### 2. Split Identity *(Premium only)*
Supports **user identities in a separate Entra tenant** from where VMs/session hosts are
provisioned. ([_meta/sources.md#adv-install], [_meta/sources.md#split-identity])
- Billable resources (NME components, VMs, networking, storage) → a subscription in the
  **deployment tenant**.
- Users, groups, and AVD resources (Workspaces, Host Pools, App Groups) → a subscription in the
  **identity tenant**; deployment-tenant resources register to them.
- **Prereqs:** GA-or-equivalent + subscription Owner cloud-native account in **both** tenants
  (recommend `*.onmicrosoft.com`); deployment user invited as a **guest** (GA + Owner, temporary,
  revoked after install) into the identity tenant; identity tenant needs a **funded Azure
  subscription** (an AVD requirement).
- **Enabled during PowerShell deployment** — **cannot use Cloud Shell or Automated methods**.
- **Limitations:** same cloud type only (global↔global / gov↔gov); Entra-ID-joined resources not
  supported (domain or Entra DS only); AVD Monitor Insights, Start-on-Connect, User Cost
  Attribution, and Intune/UEM are not supported or are variable. ([_meta/sources.md#split-identity])

### 3. Pre-created Entra ID application
Use when security policy requires the Entra app to be created **separately**, or the Marketplace
deployer lacks rights to register apps. Splits work across three roles: Marketplace deployment
(subscription Owner), Entra app registration + consent (GA or PRA+CAA), Azure resource
configuration (subscription Owner). ([_meta/sources.md#adv-install], [_meta/sources.md#create-entra-app])
- **Important:** in this mode the **automation-account app is NOT created** — NME updates must be
  applied via Cloud Shell or PowerShell scripts (no Deploy button). ([_meta/sources.md#adv-install])
- Completion uses **local PowerShell** (`deploy-az.ps1`; **cannot use Cloud Shell**).
- Entra app technical details (app roles, redirect URIs, exact permission set) are captured in the
  source doc — see [_meta/sources.md#create-entra-app] when documenting this path in depth.

## Deployment scenarios (independent of method)
NME supports **single-subscription**, **multi-subscription**, and **multi-tenant** deployments
(multi-tenant is "advanced" and requires a support engagement). Best practice across subscriptions
is **VNet peering**; AVD session hosts need line-of-sight to domain services and direct
connectivity to file storage. See [nme-components.md](../architecture/nme-components.md) and
[network-isolation.md](../hardening/network-isolation.md). ([_meta/sources.md#reference-architecture])

## Government cloud
For Azure Government, the Entra app uses the Azure Government management API
(`$azureEnv = "AzureUSGovernment"`). ([_meta/sources.md#create-entra-app])

## NME 8.0 notes
- **Certificate-based auth by default** for new installs (replaces client secrets) — affects the
  pre-created Entra app flow (cert instead of a client secret). See
  [secrets-keyvault.md](../hardening/secrets-keyvault.md). ([_meta/sources.md#release-notes])
- **AVD Classic end-of-support:** 8.0 is the last version supporting AVD Classic tenants/host
  pools; Microsoft retires AVD Classic 2026-09-30. New deployments should use AVD (ARM); existing
  AVD Classic users should migrate via NME's automated process. ([_meta/sources.md#release-notes])
- **Intune-only deployment** (no AVD) is supported — an 8.0 fix removed the requirement to enable
  AVD for standalone Windows 365 / physical-endpoint environments. ([_meta/sources.md#release-notes])

## Open questions
- NME 8.0 is Public Preview (GA is v7.7.4); re-verify advanced-install constraints at GA.
