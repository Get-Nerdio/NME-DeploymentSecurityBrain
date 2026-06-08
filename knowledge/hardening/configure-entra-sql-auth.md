---
id: configure-entra-sql-auth
title: Hardening — Entra ID SQL Authentication
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#configure-entra-sql-auth]
related: [harden-sql, secrets-keyvault, identity-and-rbac, nme-components]
---

# Hardening — Entra ID SQL Authentication

> By default NME's managed SQL Server uses **local (SQL) authentication only**, with credentials
> in the connection string stored in Key Vault under `ConnectionStrings--DefaultConnection`. If
> policy requires **Entra ID authentication**, convert SQL to mixed mode and have NME authenticate
> as its **own service principal** (`nerdio-nmw-app`). Source:
> [_meta/sources.md#configure-entra-sql-auth].

## Prerequisites & least privilege
- The account used to connect to SQL needs **at minimum Contributor** (advanced/restricted-perm
  installs) — do not exceed what the procedure requires (PoLP).
- Network-restricted App Services need connectivity to Microsoft auth URLs (VNet integration
  firewall requirements).
- From the NME **Enterprise Application** in Entra ID, record the **Application Name** (added as
  `db_owner`) and **Application ID** (used in the connection string).

## Procedure
1. **Assign an Entra ID admin on the SQL Server:** Azure portal → NME SQL Server → **Settings →
   Microsoft Entra ID** → set a user as Entra ID admin.
2. **Connect via SSMS** to the SQL Server using that Entra ID admin (Authentication: *Microsoft
   Entra ID – Universal with MFA*). You may be prompted to add your client IP to the SQL firewall.
3. **Target the right DB:** confirm SSMS has **`nmw-app-db`** selected (running against `master`
   causes a `Cannot alter the role 'db_owner'` error).
4. **Add NME as `db_owner`:** run `CREATE USER [nerdio-nmw-app] ... ALTER ROLE db_owner ADD MEMBER
   ...` (use your **Enterprise App name**, keep the square brackets — not the App Service name).
   Then run the validation `SELECT` to confirm the app appears as `db_owner`.
5. **Update the Key Vault connection string:**
   - Key Vault `nmw-app-kv-*` → **Objects → Secrets**.
   - Copy `AzureAD-ClientSecret` (current secret) — or generate a new Entra secret.
   - **Back up** the current `ConnectionStrings--DefaultConnection` value.
   - Build the new string: `Authentication=Active Directory Service Principal`; `Server` = NME SQL
     Server; `Database`/`Initial Catalog` = NME DB; **`User ID` = the Enterprise App ID** (not the
     Object ID); **`Password` = the `AzureAD-ClientSecret` value**.
   - Save it as a **New Version** of `ConnectionStrings--DefaultConnection` (existing secret can't
     be replaced directly).
6. **Restart the App Service** (Stop → Start). NME returns an immediate error if the string is
   invalid or permissions are wrong.
7. **Restrict to Entra-only:** once NME loads correctly, SQL Server → **Settings → Microsoft Entra
   ID → limit authentication to Entra ID only.**

> **Rollback:** restore the original connection string and restart the App Service.

## Notes
- A separate dedicated app for SQL auth is possible but out of scope (contact Nerdio Support).
- 8.0 new installs already use **certificate-based app auth** by default; this procedure documents
  the service-principal-secret path for SQL. See [secrets-keyvault.md](secrets-keyvault.md).

## Related
Network-restricting SQL: [harden-sql.md](harden-sql.md).
