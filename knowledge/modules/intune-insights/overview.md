---
id: intune-insights-overview
title: Module — Intune Insights
domain: modules
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#insights-intune, _meta/sources.md#api-permissions-xlsx]
related: [permission-matrix, nme-components, network-isolation, runtime-permissions-core]
---

# Module — Intune Insights

> Endpoint analytics over Intune-managed devices (device/patch/app/OS/certificate health). App
> registration: **`nmw-ii-app`** (v7.0+). Backed by a third-party analytics engine ("**Eido**").
> Source: [_meta/sources.md#insights-intune]. *This page covers deployment/security footprint, not
> the dashboards.*

## Prerequisites
- **Intune enabled** in the environment; Intune Insights enabled and thresholds configured.
- Outbound **443 to `https://graph.microsoft.com`** (and the endpoints below).
- App Service / Azure SQL sized by device count (e.g. ≤20k → B3 + S1; up to ~120k → P2V3 + S4).

## What it deploys
App Service (**.NET 8, Windows**, B3+), App Service Plan, Key Vault, Application Insights, Log
Analytics workspace, and an Azure SQL Server/DB. The App Service and SQL Server use
**system-assigned managed identities**. An existing App Service may be reused if it is a .NET 8
Windows web app with SCM Basic Auth enabled, system-assigned identity, and Website
Contributor/Contributor on the NME service principal.

## Permissions
- **App permissions used** (canonical: [permission-matrix.md](../../permissions/permission-matrix.md) §6):
  `nmw-ii-app` holds **read-only Application** Graph permissions — `Device.Read.All`,
  `DeviceManagementApps.Read.All`, `DeviceManagementConfiguration.Read.All`,
  `DeviceManagementManagedDevices.Read.All`, `DeviceManagementServiceConfig.Read.All`,
  `Group.Read.All`, `User.Read.All` (all GA-consented).
- **Enable-time (the admin):** `Microsoft.Authorization/roleAssignments/write` (Owner / RBAC
  Administrator / User Access Administrator) and `AppRoleAssignment.ReadWrite.All` (Global Admin /
  Privileged Role Admin) to assign the managed identity its Graph permissions.

> **Source caveat:** the Intune Insights article's "Minimum Permissions" block appears
> copy-pasted from Real-Time Insights (it references `nmw-rti-sql*` / `nmw-rti-app-*` and
> Storage/Monitoring/Log Analytics roles). The authoritative `nmw-ii-app` permissions are the
> Graph application permissions above, per the API-permissions workbook. Treat the doc's
> managed-identity role list as likely belonging to RTI, not Intune Insights — flagged below.

## Outbound endpoints (Eido backend)
All **443 outbound**: `eidocentral.eido.cloud` (patch inventory), `graph.microsoft.com` (Intune
data), `*.repexpstorage.blob.core.windows.net` (Intune Report API blobs), `apigtwb2c.us.dell.com`
(Dell warranty), `profiler.monitor.azure.com` and `<region>.in.applicationinsights.azure.com`
(App Insights telemetry — held per deployment, no "call home"). Account for these when filtering
egress — see [network-isolation.md](../../hardening/network-isolation.md).

## Hardening
Its Key Vault / SQL / App Service can be placed behind **private endpoints** (via install-time
Secure Deployment, the Enable Private Endpoints runbook, or manual configuration) — see
[network-isolation.md](../../hardening/network-isolation.md) for the methods.

## Open questions
- Confirm whether the doc's managed-identity role grants (Storage Blob/Table Data Contributor,
  Monitoring Reader, Log Analytics Reader) actually apply to an Intune Insights managed identity
  or are an erroneous copy of RTI. Verify against NME 8.0.
