---
id: nme-database-resilience
title: NME Database Resilience (Cross-Region SQL Failover)
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#ha-talking-points, _meta/sources.md#nme-ha-dr-webapp]
related: [resilience-overview, nme-zone-resilience, nme-regional-resilience, secrets-keyvault]
---

# NME Database Resilience (Cross-Region SQL Failover)

> **Premium edition only.** Replicates the NME SQL database to a secondary Azure region using an
> Azure SQL auto-failover group, so a regional SQL outage does not take the NME control plane
> offline. Must be configured before [Regional Resilience](nme-regional-resilience.md).
> Sources: [_meta/sources.md#ha-talking-points] (internal), [_meta/sources.md#nme-ha-dr-webapp].

## What it does

NME automates creation of the secondary database in a chosen Azure region, surfaces the new
failover-group connection string, and initiates replication between the source and replica
databases. RPO is typically seconds (asynchronous replication).

## Configuration: two parts

### Part A — Create the failover group in NME

1. NME → Settings → Environment → Nerdio tab → scroll down → expand **Nerdio Manager
   Resilience**.
2. Verify the read-back fields: Status = **"No Replication"**; current SQL server, database name,
   Key Vault, and primary region are shown.
3. Select **Create failover group**.
4. In the dialog: choose the **Resource Group**, select a **Location** (must be a different Azure
   region from the primary), choose **Failover Policy** (see below), click OK.
5. Monitor progress in the **Tasks** tab. When complete, Status flips to **"Active Replication"**
   with a warning icon — this is expected until Part B is finished.

After Part A, the **Current connection string: host** field changes from the original SQL server
hostname to the failover-group endpoint (a GUID-based `.database.windows.net` hostname). Part B
updates the Key Vault so the App Service actually uses this endpoint.

### Part B — Update the Key Vault connection string

The App Service still resolves to the original SQL server until this step. A failover without
completing Part B leaves NME unable to reach its database.

Requires: Key Vault Secrets Officer permissions (read + create) on `nmw-app-kv-<id>`.

1. Azure portal → Key Vaults → `nmw-app-kv-<id>` → Objects → Secrets →
   **`ConnectionStrings--DefaultConnection`** (double dash is deliberate — App Configuration
   encodes colons as double dashes in secret names).
2. Open the current version; copy the **Unhidden Secret value** into Notepad.
3. In NME → Settings → Environment → Nerdio → Nerdio Manager Resilience → Configuration →
   copy the **Endpoint** value (the failover-group GUID hostname).
4. In Notepad: replace **only** the `Server=tcp:<hostname>` portion with the new endpoint
   hostname. Leave port (`,1433`), `Initial Catalog`, `User ID`, `Password`, `Authentication`,
   `Encrypt`, `TrustServerCertificate`, and `Connection Timeout` byte-for-byte identical.
5. In the Key Vault secret → select **+ New Version** → paste the edited connection string →
   Create.
6. **Disable** (do not delete) the previous secret version — this is the rollback path.
7. Azure portal → App Services → NME App Service → **Stop** → wait for Stopped state →
   **Start** → wait 2–3 minutes for the App Service and WebJobs to come back up.
8. Validate in NME: Settings → Environment → Nerdio → Nerdio Manager Resilience → Status
   should read **"Active Replication + Failover"** with a green check.

> **Critical gotcha:** Editing anything other than the `Server=tcp:` hostname in the connection
> string is the #1 cause of "App Service won't start after cutover." Touch only that one field.

### Part B maintenance window

Restarting the App Service causes **2–3 minutes of NME console downtime**. WebJobs (auto-scale,
scheduled actions) also pause. Schedule this outside business hours or in a maintenance window.

## Failover policy

Chosen in the Create Failover Group dialog; can be changed afterwards in Azure portal on the
failover group resource (Configuration → Read/Write failover policy).

| Policy | Behaviour | When to use |
|---|---|---|
| **Customer Managed** (NME default) | Manual failover — a human triggers it from the Azure portal on the failover group resource | Compliance/change-control requirements; concern about false-positive auto-failovers |
| **Microsoft Managed (Automatic)** | Azure SQL auto-fails over after the primary is unavailable for the configured grace period (min 1 hour, default 1 hour) | RTO < 1 hour; lean ops teams |

> **Note:** The NME dialog only exposes Customer Managed at creation time. To switch to
> Automatic, change the policy directly in the Azure portal on the failover group resource after
> Part A is complete.

Automatic failover trade-off: replication is asynchronous, so data committed after the last
replication cycle may be lost. In-flight NME tasks at the moment of failover may need to be
retried.

## Nerdio Manager Resilience panel — other fields

| Field | Meaning |
|---|---|
| Database log retention period | Defaults to Indefinite; cap only if a data-retention policy requires it |
| Nerdio Manager Regional Resilience | Shows Disabled until [Regional Resilience](nme-regional-resilience.md) is configured |

## Open questions

- The canonical public KB article "Configure Nerdio Manager Database Resilience" (under Setup
  and Settings › Integrations) has not been ingested. The walkthrough above is sourced from the
  internal TAM talking-points document. Ingest that KB article to replace or augment this page.
