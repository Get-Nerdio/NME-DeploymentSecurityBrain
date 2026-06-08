---
id: harden-sql
title: Hardening — Azure SQL Database
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#harden-sql, _meta/sources.md#harden-nme]
related: [hardening-checklist, network-isolation, secrets-keyvault, nme-components]
---

# Hardening — Azure SQL Database

> NME communicates between the **App Service** and **Azure SQL Database** (`nmw-app-sql-*`).
> Source: [_meta/sources.md#harden-sql].

## Default posture (already secure in transit & at rest)
- Communication is encrypted with **TLS**.
- Data at rest is encrypted with **Transparent Data Encryption (TDE)**.
You harden *network reachability* on top of these defaults, via one of two methods.

## Method A — Restrict to App Service outbound IPs
Allow only the NME App Service's IPs to reach the SQL Server. ([_meta/sources.md#harden-sql])
1. Discover the IPs:
   ```powershell
   Login-AzAccount
   (Get-AzWebApp -ResourceGroup <group_name> -Name <app_name>).OutboundIpAddresses
   ```
2. Portal → **SQL servers** → `nmw-app-sql-*` → **Security → Networking → Public access**.
3. Select **Selected networks**; add a rule per App Service IP; **clear "Allow Azure services and
   resources to access this server."** **Save.**

> **Caveat:** App Service runs on shared infrastructure — these outbound IPs are shared with other
> App Services in the same cluster **and can change over time**. Nerdio recommends the VNet/subnet
> allowlist (Method B) to avoid recurring firewall maintenance.

## Method B — Route App Service traffic through a VNet (preferred)
Restrict SQL to traffic from a VNet via an Azure SQL **service endpoint**. ([_meta/sources.md#harden-sql])
- **Prerequisite:** VNet integration on the App Service, which requires a **Standard plan or
  higher** (default B3 may need upgrading). See
  [harden-app-service.md](harden-app-service.md) and "Upgrade the Azure App Service."
1. Portal → **SQL servers** → `nmw-app-sql-*` → **Security → Networking → Public access**.
2. **Selected networks**; add the desired **Virtual networks** and **Firewall rules**; **clear
   "Allow Azure services and resources to access this server."** **Save.**
Only traffic from your VNet's service endpoint can reach the database.

## Related
- Entra ID SQL authentication is a separate enhancement ("Configure Entra ID SQL Authentication" —
  not yet ingested; tracked below).
- The SQL connection string is stored in Key Vault — see
  [secrets-keyvault.md](secrets-keyvault.md).
- For the all-in-one scripted approach, see the Enable Private Endpoints runbook in
  [network-isolation.md](network-isolation.md).

## Open questions
- Capture **Entra ID SQL Authentication** steps (referenced Nerdio article not yet in `ingest/`).
