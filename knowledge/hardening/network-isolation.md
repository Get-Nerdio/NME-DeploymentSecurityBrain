---
id: network-isolation
title: Hardening — Network Isolation
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#security-faq, _meta/sources.md#implementation-guide, _meta/sources.md#release-notes, _meta/sources.md#harden-nme, _meta/sources.md#enable-pe-script]
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
Actions → Azure runbooks**. It builds a dedicated private network and routes NME's PaaS traffic
through private endpoints — no public internet. The script is authoritative for current behavior
([_meta/sources.md#enable-pe-script]); the Help Center article shows a simpler UI subset
([_meta/sources.md#harden-nme]).

**What it private-endpoints** (GroupId in parens): primary **SQL Server** (`sqlserver`), NME
**Key Vault** (`vault`), the NME and the **Scripted Actions Automation Accounts**
(`DSCAndHybridWorker`), and the **App Service** (`sites`). Conditionally, for components that
exist: **Cost Attribution (CCL)**, **Intune Insights**, and **Real-Time Insights** (their Key
Vault / SQL / App Service / Storage), the **DPS storage account**, the scripted-actions storage
(if made private), and an **Azure Monitor Private Link Scope** (optional).

**Key parameters** (script defaults):
| Parameter | Default | Behavior |
|---|---|---|
| `PrivateLinkVnetName` | `nmw-private-vnet` | VNet created (or reused) for the private network. |
| `VnetAddressRange` | `10.250.250.0/23` | New VNet address space. |
| `PrivateEndpointSubnetName` / `...Range` | `nmw-privateendpoints-subnet` / `10.250.250.0/24` | Subnet hosting the private endpoints (service endpoints enabled). |
| `AppServiceSubnetName` / `...Range` | `nmw-app-subnet` / `10.250.251.0/28` | Subnet delegated to `Microsoft.Web/serverFarms` for App Service VNet integration. |
| `PeerVnetIds` | _(empty)_ | Comma-separated VNet IDs, or `All` to peer all linked networks. Peering is bidirectional, same subscription only. |
| `MakeAppServicePrivate` | `false` | `true` ⇒ App Service public access disabled — reachable only from the script's VNet or peered VNets. |
| `MakeSaStoragePrivate` | `false` | `true` ⇒ restrict the scripted-actions storage to the private network (**AVD hosts need it — peer the AVD VNets**). |
| `SkipDNS` / `ExistingDNSZonesRG` | `false` / _(empty)_ | Skip private-DNS-zone creation, or use pre-existing zones in a given RG. |

**Firewall changes:** Key Vault → `PublicNetworkAccess = Disabled`, default action `Deny`, bypass
`None`, VNet rule for the PE subnet. SQL → `PublicNetworkAccess = Disabled` with a VNet rule
(relies on the private endpoint + deny-public rather than IP firewall rules). Both applied to
component KVs/SQL servers too.

**Private DNS zones** created and linked to the VNet (and to peer VNets where needed):
`privatelink.vaultcore.azure.net`, `privatelink.database.windows.net`,
`privatelink.blob.core.windows.net`, `privatelink.azure-automation.net`,
`privatelink.azurewebsites.net` (plus Azure Monitor zones if enabled). Gov cloud uses `.us`
equivalents.

**App Service:** VNet-integrated into the app subnet (`vnetRouteAllEnabled = false`, so not all
outbound is forced through the VNet); stays public unless `MakeAppServicePrivate = true` (the CCL
component app is set private when present).

> **Prerequisites:** the target resource group / VNet must be **linked in NME → Settings → Azure
> Environment**; using `ExistingDNSZonesRG` in another subscription requires that subscription
> linked (NME may need a temporary **Private DNS Zone Contributor** assignment). App Service Plan
> tier must support VNet integration; the VNet needs outbound **HTTPS 443** to Nerdio licensing.
> **Re-entrancy:** if the App Service restarts within ~10 min of completion, the script detects
> the prior run and exits to avoid re-applying. ([_meta/sources.md#enable-pe-script])

> **Hybrid Worker caveat:** if the **scripted-actions** storage is made private, runbook scripted
> actions stop working unless you use the **Hybrid Worker** option, with the Hybrid Worker VM on a
> VNet (peered or the PE VNet) that can reach that storage. ([_meta/sources.md#harden-nme])

> **Sensitive values:** clear-text runbook variables appear in Azure Automation logs — use
> **Global Secure Variables** for secrets. ([_meta/sources.md#harden-nme])

### Resulting private architecture
```
Private Link VNet  (nmw-private-vnet, 10.250.250.0/23)
├─ PE subnet (10.250.250.0/24)  ── private endpoints:
│     SQL · Key Vault · Automation (NME + scripted-actions) · App Service
│     · [CCL/Intune Insights/RTI] · [DPS + scripted-actions storage]
│     service endpoints: Microsoft.KeyVault, .Sql, .Web (+ .Storage)
└─ App subnet (10.250.251.0/28, delegated Microsoft.Web/serverFarms)
      └─ NME App Service (VNet integration)
Private DNS zones (vault / database / blob / automation / azurewebsites)
      └─ linked to the VNet  ── optional bidirectional peering ──▶ AVD / peer VNets
KV & SQL: public network access = Disabled (private endpoint only)
```

### Manual per-component hardening
Instead of (or alongside) the script, harden each component manually:
[harden-app-service.md](harden-app-service.md) · [harden-sql.md](harden-sql.md) ·
[harden-key-vault.md](harden-key-vault.md) · [harden-storage-account.md](harden-storage-account.md).

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
