---
id: nme-backup-restore
title: NME Backup & Restore
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#nme-backup-restore-kb]
related: [resilience-overview, nme-zone-resilience, nme-database-resilience, secrets-keyvault]
---

# NME Backup & Restore

> Backup and restore procedures for all three NME PaaS components: App Service, SQL Database,
> and Key Vault. Updated strategy applies from **February 2025** onwards.
> Source: [_meta/sources.md#nme-backup-restore-kb].

## Components and backup frequency

| Component | Contents | Change frequency | Backup method |
|---|---|---|---|
| **Azure Key Vault** | Service principal secrets, AD domain joiner passwords | Fairly static | Script (`key-vault-backup.ps1`) or "Backup NMW App" scripted action |
| **Azure SQL Database** | Auto-scale config, schedules, logs, history | Changes with auto-scale edits | Daily automatic (Azure default); configurable |
| **Azure App Service** | NME application binaries only (no customer data) | Changes at upgrade | Hourly automatic (Azure default); configurable |

## App Service backup

Azure enables **hourly automatic backups** by default. To view them: Azure portal → App Services
→ NME App Service → Settings → Backups.

**Custom backups** (recommended — sets daily schedule + 15-day retention + linked SQL DB):

1. Run the `app-service-backup.ps1` script from your local computer (download from the Nerdio
   backup scripts package).
2. Provide: Azure Subscription ID, App Service resource group name, App Service name, storage
   account resource group, storage account name.
3. After the script runs, backups are automatic daily with 15-day retention.

To adjust retention: Azure portal → App Service → Settings → Backups → Configure custom
backups. Ensure the SQL connection string is present (retrieve from Key Vault secret
`ConnectionStrings—DefaultConnection` if missing).

> **Hardened environment note:** App Service backups run in the App Service cluster and do **not**
> use configured private endpoints or VNet integration. If SQL is hardened, all App Service cluster
> IP addresses must be allowed on the SQL firewall for the backup to connect.

## SQL Database backup

Azure enables **daily automatic backups** by default.

To modify retention: Azure portal → SQL servers → NME SQL server → Data management →
Backups → Retention policies.

**Databases > 4 GB** cannot be backed up via the App Service backup — use SQL Server-provided
backups instead.

## Key Vault backup

No native Azure backup process exists for Key Vaults. Two options:

**Option A — "Backup NMW App" scripted action** (recommended for recurring backup):
Schedule this from NME to back up certificates, keys, and secrets on a recurring basis.

**Option B — `key-vault-backup.ps1` script** (one-time):
1. Run the script locally; provide Azure Subscription name and Key Vault name.
2. Authenticate as a non-guest account with Access policies and Owner permissions on the KV.
3. Script produces `keyvault-backup.zip` (encrypted; can only be decrypted in the **original KV
   region**).

> **Warning:** The PowerShell script creates a one-time backup only. For recurring backup,
> schedule the "Backup NMW App" scripted action.

## Key Vault restore

1. Place `key-vault-restore.ps1` in the same directory as `keyvault-backup.zip`.
2. Run the script.

Notes:
- Restores only keys/secrets/certificates that **do not already exist**. Deleted-but-not-purged
  items return a conflict error.
- Does not overwrite existing values.
- KV restore is **in-region only** — cannot restore to a different Azure region.
- To revert a single secret to an older value: Key Vault → Secrets → target secret → Older
  Versions → select version → Set Active.

## App Service restore

Restore from: Azure portal → App Service → Settings → Backups (portal option), or from the
`nmwbackup` blob container in the backup storage account (PowerShell).

## Open questions

- Confirm whether `app-service-backup.ps1` is available directly from the NME UI or requires
  a separate download link from the Nerdio KB.
