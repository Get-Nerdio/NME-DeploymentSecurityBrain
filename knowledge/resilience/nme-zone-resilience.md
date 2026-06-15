---
id: nme-zone-resilience
title: NME Zone Resilience (Within-Region HA)
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#app-zone-resilient, _meta/sources.md#sql-zone-resilient, _meta/sources.md#bcdr-avd]
related: [resilience-overview, nme-backup-restore, nme-database-resilience, hardening-checklist]
---

# NME Zone Resilience (Within-Region HA)

> Two independent procedures that together make NME resilient to a single availability zone or
> data-centre failure within one Azure region. Both are supported on any edition.
> Sources: [_meta/sources.md#app-zone-resilient], [_meta/sources.md#sql-zone-resilient].

## Overview

Zone redundancy is configured independently for the App Service and SQL Database. Both are
recommended for Situation 2 (AZ failure) protection; see [avd-bcdr-guidance.md](avd-bcdr-guidance.md).

Other NME components (Key Vault, Storage, Automation, Log Analytics) **automatically** use ZRS in
supported regions — no additional steps. App Insights requires workspace-based mode and a dedicated
cluster for full zone redundancy. ([_meta/sources.md#bcdr-avd])

## 1 — App Service zone resilience

**Prerequisites:** Complete before enabling zone redundancy on the App Service Plan.

### 1a. Create a ZRS storage account and locks container

1. Azure portal → Resource groups → select NME resource group → +Create → Storage Account.
2. Set **Redundancy** to **Zone-redundant storage (ZRS)**; accept other defaults.
3. Open the new storage account → Data storage → Containers → +Container → Name: **`locks`** →
   Create.

### 1b. Generate a SAS token for the locks container

1. Right-click the `locks` container → Generate SAS.
2. Permissions: **Read, Write, Create**. Expiry: a long date (e.g., 2099 or 2999).
3. Select **Generate SAS token and URL** → copy the **Blob SAS URL**.

### 1c. Add the SAS URL to the App Service

**Option 1 — App Service Environment Variables (simpler):**
1. App Services → open NME App Service → Settings → Environment variables → +Add.
2. Name: `Deployment:LocksContainerSasUrl`. Value: paste the Blob SAS URL.
3. Select Apply → Apply → Confirm (restarts the App Service).

**Option 2 — Key Vault secret:**
1. Key vaults → open `nmw-app-kv-#############` → Objects → Secrets → +Generate/Import.
2. Name: `Deployment--LocksContainerSasUrl` (double dash). Value: paste the Blob SAS URL.
3. Restart the App Service manually after creating the secret.

### 1d. Verify the locks container

After the App Service restarts, confirm that `background.loop` and `web.startup` blob files
were created inside the `locks` container.

### 1e. Create a zone-redundant App Service Plan

1. Azure portal → Resource groups → NME resource group → +Create → App Service Plan.
2. **Pricing Tier**: Premium or Isolated plan. **Zone redundancy**: Enabled.
3. Create.

### 1f. Migrate the App Service to the new plan

1. Open the existing NME App Service → App Service plan blade → Change App Service plan →
   select the new zone-redundant plan → OK.
2. The old plan can be deleted after 1–2 weeks once stability is confirmed.

## 2 — SQL Database zone resilience

The default NME SQL database uses the **S1 DTU tier**, which supports only local redundancy
(LRS — three copies within a single data centre). Zone redundancy requires the **Premium** DTU
tier (or vCore Business Critical / General Purpose). ([_meta/sources.md#sql-zone-resilient])

> **Note:** Basic and Standard DTU tiers do not support zone redundancy.

### Steps

1. Azure portal → SQL databases → NME database (default name: `nmw-app-db`).
2. Settings → Compute + storage → Service tier: **Premium (Highest availability and
   performance)**.
3. Under *"Would you like to make this database zone redundant?"* → select **Yes**.
4. Apply. After a few minutes the database is on Premium P1 with zone redundancy.

> Zone redundancy on Premium/Business Critical is available at no extra cost because existing
> replicas are redistributed across zones rather than creating new ones.

## Interaction with Database Resilience

Zone resilience (this page) and
[Database Resilience](nme-database-resilience.md) (cross-region SQL failover groups) are
compatible and can be combined. Zone resilience protects within a region; Database Resilience
protects against a full regional outage. Configure zone resilience first.
