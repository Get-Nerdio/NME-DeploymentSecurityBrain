---
id: network-isolation
title: Hardening — Network Isolation
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#implementation-guide, _meta/sources.md#release-notes, _meta/sources.md#harden-nme]
related: [hardening-checklist, nme-components, secrets-keyvault, harden-app-service, harden-sql, harden-storage-account]
---

# Hardening — Network Isolation

> Network exposure and how to lock it down. Source: [_meta/sources.md#security-faq],
> [_meta/sources.md#implementation-guide].

## Default exposure
By default NME and its dependencies (SQL Database, Storage Account, Key Vault, App Service) are
reachable via their **public endpoints**. ([_meta/sources.md#implementation-guide])

## Private endpoints — three hardening models
([_meta/sources.md#security-faq])
1. **Secure Deployment (recommended)** — enable **Private Endpoints at install**; NME provisions
   all required resources with PEs. Most streamlined and fully supported.
2. **Post-deployment scripted hardening** — run NME's **hardening runbook** to apply PEs after a
   non-PE deployment.
3. **Fully manual hardening** — for environments with specific DNS/security requirements (e.g. not
   using Azure DNS); manually configure PEs, DNS, and routes beyond the script's scope.

When Private Endpoints are enabled, the app and **all** dependencies are **no longer reachable via
public endpoints** — access is via private IPs on the customer VNet. Install-wizard inputs: VNet,
subnet for private endpoints, subnet for App Service (VNet integration). ([_meta/sources.md#implementation-guide])

> **v7.4+:** all core NME modules (UCA, Intune Insights, Private WinGet, Azure
> Runbooks/Automation, Azure AI Analytics) support hardened deployment with private endpoints
> **without a hybrid worker VM**, for scripts under 500 KB. ([_meta/sources.md#security-faq])

### The "Enable Private Endpoints" Azure runbook
The scripted hardening (model 2) is the **Enable Private Endpoints** runbook under **Scripted
Actions → Azure runbooks**. It adds private/service endpoints so the App Service reaches **SQL and
Key Vault over a private network** (no public-internet traffic). Optional parameters
([_meta/sources.md#harden-nme]):
- **PeerVnetId** — Resource ID of an existing VNet to peer to the new private-endpoint VNet.
  Nerdio **recommends against peering to production networks** in hardened scenarios unless storage
  access is restricted or the app service is made private.
- **StorageAccountResource** — a single storage account (an Azure Files location) to include in the
  private-endpoint subnet; access becomes restricted to NME and peered VNets.
- **MakeAppServicePrivate** — `true` limits app access to hosts on the script's VNet or peered VNets.

Requirements: an App Service Plan tier supporting **VNet integration**, and a VNet with **outbound
HTTPS (TCP/443)** to Nerdio licensing servers.

> **Hybrid Worker caveat:** if the storage account holding **scripted actions** is made private,
> Azure runbook scripted actions stop working — use the **Hybrid Worker** option, with the Hybrid
> Worker VM on a VNet (peered or the private-endpoint VNet) that can reach that storage account.
> ([_meta/sources.md#harden-nme])

> **Sensitive values:** runbook variables in clear text appear in Azure Automation logs — use
> **Global Secure Variables** for secrets. ([_meta/sources.md#harden-nme])

### Manual per-component hardening
Instead of (or alongside) the script, harden each component manually:
[harden-app-service.md](harden-app-service.md) · [harden-sql.md](harden-sql.md) ·
[harden-storage-account.md](harden-storage-account.md).

## Install-time pitfall
**Leave "Restrict App Service public access" UNSELECTED during install** — enabling it makes NME
unreachable after deployment and requires additional manual network configuration. Restrict access
later via a supported hardening path. ([_meta/sources.md#implementation-guide])

## Temporary public access during install
Install requires temporary public access to **Key Vault** (to write secrets) and other services
used by the initial ARM template; components convert to private endpoints afterward where
configured. ([_meta/sources.md#security-faq])

## Session-host networking
- **Enable private subnet** disables default outbound access (note: default outbound access is
  removed for new deployments as of 2025-09-30) — outbound to required Microsoft endpoints must be
  granted explicitly. ([_meta/sources.md#implementation-guide])
- Optionally attach an existing **NSG**; otherwise NME creates one with the network.

## Outbound / firewall
NME components need outbound to licensing, Azure APIs, and logging; session hosts need outbound for
broker comms, updates, and Microsoft Store/WinGet. If filtering via firewall/private DNS, keep
Microsoft services reachable via **private endpoints or Azure service tags**. ([_meta/sources.md#security-faq])

## Cross-subscription / tenant
Best practice is **VNet peering**; ExpressRoute/VPN supported (ExpressRoute Authorizations for
multi-subscription). AVD session hosts need line-of-sight to domain services and direct
file-storage connectivity. See [nme-components.md](../architecture/nme-components.md).

## NME 8.0 notes
- **Egress Path status:** the Linked Networks settings page now shows the identified internet
  routing method per network, making it easy to spot networks still relying on **legacy default
  outbound access** (removed for new deployments as of 2025-09-30). ([_meta/sources.md#release-notes])
- **Copilot now supports private endpoints**, extending hardened deployment to the optional AI
  module. ([_meta/sources.md#release-notes])

## Open questions
- Enumerate the exact required outbound endpoints/service tags (referenced by external doc title
  in sources, not enumerated here).
- NME 8.0 is Public Preview (GA is v7.7.4); re-verify at GA.
