---
id: rti-overview
title: Module — Real-Time Insights
domain: modules
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#insights-rti]
related: [permission-matrix, nme-components, network-isolation, runtime-permissions-core]
---

# Module — Real-Time Insights (RTI)

> Live monitoring (configurable 1–15 min polling) of resource usage and health for managed AVD
> hosts, Windows 365 devices, and sessions, with configurable alert thresholds. Uses **managed
> identities** `nmw-rti-app-*` and `nmw-rti-sql*` (v7.0+). Source: [_meta/sources.md#insights-rti].
> *This page covers the deployment/security footprint, not the dashboards.*

## What it deploys
Enabling RTI provisions an **App Service Plan**, an **Azure SQL database**, a **Storage Account**
(`stnrt*`), **Application Insights** (`nmw-rti-app-insights-*`), and a **Log Analytics workspace**
(`nmw-rti-law-*`), sized automatically from the estimated endpoint count and polling interval.
Resource names are customizable at enable time.

## Permissions (canonical: [permission-matrix.md](../../permissions/permission-matrix.md) §7)
**Enable-time — the admin enabling RTI needs:**
- `Microsoft.Authorization/roleAssignments/write` (Owner / RBAC Administrator / User Access
  Administrator) — to create the role assignments below.
- `AppRoleAssignment.ReadWrite.All` (Global Admin / Privileged Role Admin) — to grant the
  `nmw-rti-sql*` managed identity the Graph `Directory.Read.All` permission.

**Granted to the managed identities after provisioning:**
| Identity | Role | Scope |
|---|---|---|
| `nmw-rti-app-*` | Storage Blob Data Contributor + Storage Table Data Contributor | Storage Account `stnrt*` |
| `nmw-rti-app-*` | Monitoring Reader | Application Insights `nmw-rti-app-insights-*` |
| `nmw-rti-app-*` | Log Analytics Reader | Log Analytics Workspace `nmw-rti-law-*` |
| `nmw-rti-sql*` | Graph `Directory.Read.All` | Tenant |

## Security notes
- Uses **managed identities** (no stored credentials). The only tenant-wide grant is the SQL
  managed identity's `Directory.Read.All`.
- Data is collected into the customer's own RTI resources (Storage / LAW / App Insights).
- More frequent polling increases database/storage cost.
- Hardening: the RTI Key Vault / SQL / App Service / Storage can be placed behind **private
  endpoints** (via install-time Secure Deployment, the Enable Private Endpoints runbook, or manual
  configuration) — see [network-isolation.md](../../hardening/network-isolation.md) for the methods.

## Open questions
- Confirm RTI identity/role grants are unchanged in NME 8.0.
