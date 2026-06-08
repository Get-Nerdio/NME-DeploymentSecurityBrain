---
id: network-isolation
title: Hardening — Network Isolation
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#implementation-guide, _meta/sources.md#release-notes]
related: [hardening-checklist, nme-components, secrets-keyvault]
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
