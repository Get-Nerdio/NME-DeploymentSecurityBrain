---
id: firewall-requirements
title: Hardening — Outbound Firewall Requirements
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#vnet-firewall, _meta/sources.md#session-host-outbound, _meta/sources.md#nme-network-test, _meta/sources.md#test-outbound-avd]
related: [network-isolation, harden-app-service, harden-storage-account, prerequisites, intune-insights-overview]
---

# Hardening — Outbound Firewall Requirements

> The outbound endpoints required in a network-restricted/secure environment. **Two distinct
> egress surfaces:** (1) the **NME App Service** (once VNet-integrated) and (2) the **AVD session
> host VMs**. Prefer **Azure service tags** over literal addresses where available. Sources:
> [_meta/sources.md#vnet-firewall], [_meta/sources.md#session-host-outbound].

## 1. NME App Service egress (after VNet integration)
When VNet integration is applied to the NME app, its subnet typically has outbound access
restricted; allow the following for NME to function. ([_meta/sources.md#vnet-firewall])

| Address | Port | Purpose | Service tag |
|---|---|---|---|
| `*.azurewebsites.net` | 443 | Update NME via the Automation account | AzureAppService |
| `nwp-web-app.azurewebsites.net` | 443 | **Nerdio licensing servers** | Internet |
| `nmwextensions.blob.core.windows.net` | 443 | Retrieve extension-install scripts (hosted storage) | Storage |
| (Azure SQL) | 1433, 11000–11999 | Azure SQL Services | AzureSQL |
| `*.applicationinsights.azure.com` | 443 | Application Insights | ActionGroup / ApplicationInsightsAvailability / AzureMonitor |
| `login.microsoftonline.com`, `graph.microsoft.com` | 443 | Authentication | AzureIdentity |
| `login.windows.net` | 443 | Entra ID (AAD) SQL authentication | — |
| `*.azurewebsites.net` **or** explicit Web App URL and/or custom web app address | 443 | Back-end access management | AzureAppService |
| `management.azure.com` | 443 | AVD management | AzureAppConfiguration |
| `api.github.com` | 443 | Scripted Actions repository | — |
| `[KeyVaultName].vault.azure.net` or `*.vault.azure.net` | 443 | Key Vault access | — |
| `*.githubusercontent.com` | 443 | GitHub content access | — |
| `api.loganalytics.io` | 443 | Log Analytics API | — |
| `api.applicationinsights.io` | 443 | Application Insights API | — |

Notes ([_meta/sources.md#vnet-firewall]):
- **Azure Files** connectivity is required for Auto-scaling and FSLogix profile management — see
  [harden-storage-account.md](harden-storage-account.md).
- With **private endpoints**, source addresses can change — see
  [harden-app-service.md](harden-app-service.md). **Service tags are not applied/required for
  private endpoints.**
- The **Intune Insights** module adds its own outbound endpoints (Eido backend) — see
  [intune-insights/overview.md](../modules/intune-insights/overview.md).

## 2. AVD session host egress
For NME to create/manage session hosts where VMs are internet-restricted (UDR/NSG/proxy/GPO),
allow the following. ([_meta/sources.md#session-host-outbound]) For Azure US Gov, see Nerdio's
"Required URL List."

### Required
| Address | Port | Purpose | Service tag |
|---|---|---|---|
| `login.microsoftonline.com` | 443 | Auth to Microsoft Online Services | — |
| `nmwextensions.blob.core.windows.net` | 443 | Nerdio DSC extension (see notes) | Storage |
| `*.wvd.microsoft.com` | 443 | AVD service traffic | WindowsVirtualDesktop |
| `*.prod.warm.ingest.monitor.core.windows.net` | 443 | Agent traffic (**current** — see deprecated) | AzureCloud |
| `catalogartifact.azureedge.net` | 443 | Azure Marketplace | AzureFrontDoor.Frontend |
| `gcs.prod.monitoring.core.windows.net` | 443 | Agent traffic | AzureCloud |
| `kms.core.windows.net`, `azkms.core.windows.net` | 1688 | Windows activation | Internet |
| `mrsglobalsteus2prod.blob.core.windows.net` | 443 | Agent & SXS stack updates | AzureCloud |
| `wvdportalstorageblob.blob.core.windows.net` | 443 | Azure portal support | AzureCloud |
| `169.254.169.254` | 80 | Azure Instance Metadata Service | — |
| `168.63.129.16` | 80 | Session host health monitoring | — |
| `oneocsp.microsoft.com`, `www.microsoft.com` | 80 | Certificates | — |
| NME `cssa…blob.core.windows.net` storage account (unique per install) | 443 | Install AVD agent, FSLogix agent, other tools | — |

### FSLogix
| Address | Port | Purpose |
|---|---|---|
| `[FQDN of storage]` | 445 | SMB access to FSLogix file shares |

### No longer supported (remove if present)
Microsoft retired the old Agent-traffic URLs (`production.diagnostics.monitoring.core.windows.net`,
`*xt.blob/table/queue.core.windows.net`, `*eh.servicebus.windows.net`). Ensure
`*.prod.warm.ingest.monitor.core.windows.net` is allowed or hosts show **Needs Assistance**.
([_meta/sources.md#session-host-outbound])

### DSC extension → service tags
The Azure **DSC Extension** has no dedicated service tag and **retires 2028-03-31** (successor:
**Azure Machine Configuration**). To keep DSC working, Microsoft recommends the tags
**AzureAutomation**, **GuestAndHybridManagement**, plus **Storage** and **KeyVault** (if DSC pulls
configs/scripts/secrets from those). ([_meta/sources.md#session-host-outbound])

### Optional (feature-dependent)
Windows Update (`*.prod.do.dsp.mp.microsoft.com`), Microsoft 365 sign-in (`login.windows.net`),
telemetry (`*.events.data.microsoft.com`), connectivity test (`www.msftconnecttest.com`), OneDrive
(`*.sfx.ms`), cert revocation (`*.digicert.com`), Azure DNS (`*.azure-dns.com/.net`), NVIDIA GPU
drivers (`raw.githubusercontent.com`, `download.microsoft.com`). Scripted-action app installers
pull from `github.com`, `teams.microsoft.com`, `microsoft.com`, `support.zoom.us`,
`s3.amazonaws.com` — these can be self-hosted for heavily restricted environments.

> **Host build prerequisites** ([_meta/sources.md#session-host-outbound]): the generalized image
> must have the **DVD-ROM enabled** (Azure mounts an ISO at create; otherwise the VM hangs at
> OOBE); **WinRM must not be disabled** and **unsigned PowerShell** must be allowed on session
> hosts (exclude the session-host OU / use a naming-prefix exclusion if a GPO restricts these,
> since NME's DSC extensions use PowerShell + WinRM).

## Testing connectivity (troubleshooting)
Two Nerdio tools verify the two egress surfaces above — use them when connectivity is suspect.

- **NME App Service connectivity** → **`NmeNetworkTest.ps1`** ([_meta/sources.md#nme-network-test]).
  **Recommend this first when troubleshooting App Service connectivity.** Run it from the App
  Service **Kudu/SCM debug console** (Azure portal → the NME App Service → Development Tools →
  Advanced Tools → Debug Console → PowerShell). It tests the §1 endpoints plus the auto-detected
  Key Vault / SQL / DPS storage over local DNS, capturing DNS resolution and TLS certificate
  details to `NmeNetworkTestOutput.txt`. Optional params: `AdditionalTestUris` (for non-standard
  app names), `TlsVersion` (default `Tls12`).
- **AVD session-host connectivity** → the **"Test Outbound Connections from AVD Host"** Azure
  runbook scripted action ([_meta/sources.md#test-outbound-avd]). Run it from NME against a target
  host pool / VM; it tests the required AVD endpoints (§2) and the scripted-actions storage
  account. It executes via `Invoke-AzVMRunCommand`, so it **works even when the scripted-actions
  storage is unreachable** — useful precisely when egress is broken. Params: `KeyVaultName`,
  `AzureResourceGroupName`, `AzureVMName`, `TestRequiredAvdUrls` (default `$true`).

## Related
Overall network model and the private-endpoint enablement methods:
[network-isolation.md](network-isolation.md). Prerequisites:
[prerequisites.md](../installation/prerequisites.md).
