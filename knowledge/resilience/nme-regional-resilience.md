---
id: nme-regional-resilience
title: NME Regional Resilience (Multi-Region Web App HA)
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#nme-ha-dr-webapp, _meta/sources.md#ha-talking-points]
related: [resilience-overview, nme-database-resilience, nme-zone-resilience, hardening-checklist, secrets-keyvault]
---

# NME Regional Resilience (Multi-Region Web App HA)

> **Premium edition only. Requires [Database Resilience](nme-database-resilience.md) first.**
> Extends NME HA beyond database replication to protect the full control-plane deployment: a
> PowerShell script provisions a secondary App Service in a different Azure region, an Azure App
> Configuration store with regional replica, a distributed lease blob, and Azure Front Door to
> route traffic to whichever instance is healthy.
> Sources: [_meta/sources.md#nme-ha-dr-webapp], [_meta/sources.md#ha-talking-points] (internal).

## Architecture produced

```
Users → Azure Front Door (*.azurefd.net)
            ├─ Origin Priority 1 → Primary App Service (e.g. East US)
            └─ Origin Priority 2 → Secondary App Service (e.g. North Central US)

Both App Services read shared config from Azure App Configuration (Standard SKU)
   └─ Regional replica in each secondary location
Both App Services access the same Key Vault
Distributed lease blob (locks container) prevents competing auto-scale
```

Active/passive: AFD sends all traffic to Priority 1 unless its health probe fails (3 of 4
samples over 100 s intervals). Practical RTO primary-to-secondary: ~5 minutes. This is **not**
load balancing — the secondary is idle until needed.

> **SQL HA/DR note:** Even with Regional Resilience configured, the SQL database layer uses
> active/passive auto-failover groups. Brief NME outages should be expected during SQL failover.
> ([_meta/sources.md#nme-ha-dr-webapp])

## Requirements

- Nerdio Manager **Premium Edition**
- `Microsoft.Cdn` content provider registered for the subscription
- **Database Resilience must be configured first** (both Part A and B complete, status "Active
  Replication + Failover")
- DPS (Data Protection Keys) storage account (prefix `dps`) must exist and be **GRS** (not LRS);
  if LRS, convert before proceeding. If it doesn't exist (pre-v5.5 installs), run the
  `migrate-dataprotection.ps1` script first (Settings → Environment → Nerdio → Data Protection
  Keys migration → Download script → run from Cloud Shell)
- All NME web app resources must be in the **same subscription** and **single resource group**
- Pre-run: screenshot or export the primary App Service environment variables (Configuration →
  Environment variables) — the script replaces them; this is the rollback safety net

## The configure_resilience.ps1 script

Download from: NME → Settings → Environment → Nerdio → Nerdio Manager Regional Resilience →
**Download script**. The script is pre-populated with the environment's values.

Run as: `./configure_resilience.ps1` (not just `configure_resilience.ps1`).

Requires Azure CLI ≥ 2.24.0 and 8 PowerShell modules (`Az.Accounts`, `Az.Resources`,
`Az.Websites`, `Az.KeyVault`, `Az.Storage`, `Az.AppConfiguration`, `Az.Cdn`,
`Microsoft.Graph.Applications`). In restricted environments without PSGallery access, pre-install
these manually.

### What the script does (step sequence)

| Step | Action |
|---|---|
| 1 | Dependency checks (Azure CLI, 8 PS modules) |
| 2 | Authentication (Azure CLI + Graph; managed identity in Cloud Shell, interactive locally) |
| 3 | Environment inventory — reads primary App Service, plan, Entra App Registration |
| 4 | Creates Azure App Configuration store (Standard SKU) + regional replica(s); grants **App Configuration Data Reader** to primary managed identity |
| 5 | Prerequisite validation — gates on `DataProtection:Storage:Type = AzureBlobStorage`; exits if not met |
| 6 | Migrates all shared app settings to App Configuration, **skipping** 4 per-instance keys: `ApplicationInsights:ConnectionString`, `ApplicationInsights:InstrumentationKey`, `Deployment:WebAppName`, `AppConfiguration:Endpoint` |
| 7 | Locks container — creates `locks` container in DPS storage; generates 50-year SAS token; stores as `Deployment--LocksContainerSasUrl` in Key Vault |
| 8 | **Stops primary App Service** — maintenance window begins (~5–15 min) |
| 9 | Clones primary App Service to secondary region(s); copies managed identity; grants App Configuration Data Reader + KV `wrapKey`/`unwrapKey`/`get`/`list`/`set`/`delete` |
| 10 | Creates Azure Front Door Standard profile; origin group (100 s health probe on `/public/health/ping`, session affinity **on**); primary at Priority 1, each secondary at Priority 2+ |
| 11 | Writes `Deployment:MultiInstance:ProxyHostname` and `Deployment:MultiInstance:FrontDoorProfileId` into App Configuration |
| 12 | Adds AFD hostname to Entra App Registration redirect URIs (note: does **not** add secondary `.azurewebsites.net` URIs — see Known Issues) |
| 13 | Replaces all shared App Service env vars with a single `AppConfiguration:Endpoint` pointer; per-instance settings remain local |
| 14 | (Optional, `SafdAccessOnly = True`) AFD-only firewall lockdown — adds `AzureFrontDoor.Backend` service tag rule; sets default action to Deny on all App Services |
| 15 | Disables App Configuration local auth (managed identity + RBAC only) |
| 16 | **Restarts all App Services and WebJobs** — maintenance window ends |
| 17 | Final validation — HEAD request to AFD hostname; prints AFD hostname as the new NME URL |

After the script completes, validate in NME: Settings → Environment → Nerdio → Nerdio Manager
Regional Resilience → target state: **"Enabled (2 of 2 Web Apps active)"**.

**Users should bookmark the AFD hostname only.** The direct App Service URL does not survive a
regional failover.

## Updating NME after Regional Resilience is configured

> **Warning: the standard NME portal Deploy button breaks HA.** It deploys to the primary only;
> the secondary runs the old version. Mismatched versions are explicitly unsupported and can cause
> unpredictable behaviour.

**Required method: Cloud Shell (Method 2) or Zip Deploy (Method 4) only.**

Procedure:
1. NME → Updates page → review the available version and both listed App Service instances.
2. **Stop ALL App Service instances** before running any update command.
3. Run the update command for the primary; wait for it to complete.
4. Run the update command for the secondary; wait for it to complete.
5. Do not start either instance until both are updated.
6. Validate via the AFD hostname; confirm Regional Resilience still shows "Enabled (2 of 2 Web
   Apps active)".

## Limitations and gaps

| Component | HA status | Action required |
|---|---|---|
| User Cost Attribution (UCA) web app | Not supported | Flag to customer; document in design sign-off |
| Private Endpoints | Requires AFD Premium (no upgrade from Standard — full AFD rebuild) | Confirm before running script |
| Auto-scale (CSSA storage dependency) | Halts if CSSA region unavailable | Communicate manual scaling fallback; document in operator runbook |
| NME console (DPS storage dependency) | Inaccessible if DPS region unavailable (GRS replica activates only on declared regional outage) | Ensure DPS is GRS; communicate impact window |
| Standby web app start (DR mode) | Manual start required from Azure portal | Include in failover runbook; factor into RTO |
| WebJobs after restart | May need manual start if 3 retries fail | Check WebJobs post-script; App Service → WebJobs → start manually |
| GRS region pairing | Azure-assigned; cannot be changed | Validate GRS pair at design time; align secondary region accordingly |
| App Insights | Per-instance, not shared | Optionally point both instances at a shared workspace in a neutral region post-script |
| NME updates | Portal Deploy button off-limits post-HA | Runbook: Cloud Shell or Zip Deploy only |

## Known issues

**AFD "Page not found" immediately after script completion:** DNS and CDN propagation takes
5–15 minutes. This is not a configuration error. Wait and retry.

**AADSTS50011 on secondary App Service direct access:** The script adds the AFD hostname to
Entra redirect URIs but does not add the secondary App Service's `.azurewebsites.net` URLs.
Direct access to the secondary (for testing/troubleshooting) fails with AADSTS50011.
Workaround: manually add `https://<secondary-app-name>.azurewebsites.net/signin-oidc` and
`https://<secondary-app-name>.azurewebsites.net/` to the Entra App Registration redirect URIs
(Entra ID → App registrations → `nerdio-nmw-app` → Authentication). Especially important if
AFD-only firewall lockdown is enabled.
