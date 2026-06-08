---
id: step-by-step
title: NME Installation — Step by Step
domain: installation
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#install-guide, _meta/sources.md#implementation-guide, _meta/sources.md#release-notes]
related: [prerequisites, deployment-models, install-time-permissions, post-install-validation]
---

# NME Installation — Step by Step

> The standard (Azure Marketplace + Cloud Shell) procedure. Confirm
> [prerequisites.md](prerequisites.md) first. For advanced paths see
> [deployment-models.md](deployment-models.md). Source: [_meta/sources.md#install-guide],
> [_meta/sources.md#implementation-guide].

High-level phases: **(A)** install from Marketplace → **(B)** initialize via PowerShell →
**(C)** configure settings → **(D)** grant admin consent.

## Phase A — Install from Azure Marketplace
1. In Azure Marketplace, search **"Nerdio Manager for Enterprise."**
2. **Create > NME Plan.**
3. **Basics:** choose Subscription, Resource Group (new, or an empty existing one), and Region
   (where NME resources live — this does **not** determine AVD host location).
4. **Resource Names:** set a Name prefix.
5. **Private Endpoints:** optionally **Enable Private Endpoints** (then pick the VNet, the subnet
   for private endpoints, and the subnet for App Service). **Leave "Restrict App Service public
   access" UNSELECTED** — enabling it makes NME unreachable post-deploy and needs manual network
   config. See [network-isolation.md](../hardening/network-isolation.md).
6. **Tags:** optional.
7. **Review + Create → Create.** Deployment takes ~10 minutes.
8. **Go to resource group** → select the **App Service**.

## Phase B — Initialize NME (standard / Cloud Shell)
1. Open the NME URL from the App Service (Browse, or the domain link on Overview).
2. Copy the command shown.
3. Launch **Azure Cloud Shell**, signed in as GA (or PRA+CAA) **and** subscription Owner.
4. If prompted, choose **PowerShell** (not Bash) and create a storage account for shell history.
5. Paste the command, press Enter (~10 min).
6. Success message: **"Deployment completed successfully"** (or `NMW-After-Publish <RG> <App Service>`).
7. Open the URL in the confirmation message (or refresh the tab).

> Advanced paths (pre-created Entra app / Split Identity) instead use *Show advanced*, enter the
> existing App ID / Secret / Service Principal ID (or Identity Tenant ID), **Download script (Az)**,
> and run it on a **local machine** (not Cloud Shell). See [deployment-models.md](deployment-models.md).

## Phase C — Configure NME settings
1. **Register Nerdio Manager** — enter registration info, Register.
2. **Feature set** — choose Azure Virtual Desktop, Windows 365 (Cloud PCs), and/or Intune. AVD
   prompts for **Network** (subnet), **Directory** (AD / Entra DS / native Entra ID account able
   to create computer objects), and **File Storage**.
3. **File storage** — provide the FSLogix storage / UNC path (or skip and add later). Options
   include FSLogix version, Cloud Cache (up to 4 paths), and Entra ID Kerberos config.
4. Optionally configure Windows 365 & Intune scopes.

## Phase D — Complete install (admin consent)
1. Select **Done**, then the tenant link provided.
2. Sign in as a **Global Administrator**; review and accept consent.
3. Back in NME, select **"I have granted admin consent."** → OK.
4. If errors, repeat consent (can take several minutes / multiple retries).

Then verify the install — see [post-install-validation.md](post-install-validation.md) — and
activate the subscription past trial (creates `NerdioManagerForWVD-Subscribe`; billed by MAU).
See [_meta/sources.md#activate-subscription].

## NME 8.0 notes
- New installs use **certificate-based auth** for app registrations by default (no client secret).
  ([_meta/sources.md#release-notes]) See [secrets-keyvault.md](../hardening/secrets-keyvault.md).
- 8.0 introduces an optional **new three-tier menu** (off by default) and an **All Features**
  page; this guide describes the classic navigation. ([_meta/sources.md#release-notes])

## Open questions
- NME 8.0 is Public Preview (GA is v7.7.4); wizard steps carry from the current install guide.
  Re-verify at 8.0 GA.
