---
id: ucap-overview
title: Module — User Cost Attribution
domain: modules
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#ucap-overview, _meta/sources.md#insights-costs, _meta/sources.md#api-permissions-xlsx]
related: [permission-matrix, nme-components, network-isolation, deployment-models]
---

# Module — User Cost Attribution (CCL)

> Per-user cost reporting: allocates total AVD deployment cost (compute, storage, network, PaaS,
> SaaS) to individual users by usage duration, for show-back / charge-back. App registration /
> service principal: **`nmw-ccl-app`**. Surfaced under **Insights → Costs & Efficiency → User Cost
> Attribution** (Public Preview). Source: [_meta/sources.md#ucap-overview]. *This page covers the
> deployment/security footprint, not the full reporting feature set.*

## Eligibility & prerequisites
- **Premium edition only.**
- Subscription must support **Azure Cost Management**.
- **Not supported with the Split Identity install model** (see
  [deployment-models.md](../../installation/deployment-models.md)).
- To enable, the admin needs tenant role **Global Administrator / Cloud Application Administrator /
  Application Administrator** *and* subscription **Owner / User Access Administrator**.

## What it deploys
A separate **App Service** (`nmw-ccl-app`, default plan P0v3), a **Storage Account**, and a **Log
Analytics workspace**. See [nme-components.md](../../architecture/nme-components.md).

## Permissions used (canonical: [permission-matrix.md](../../permissions/permission-matrix.md) §5)
The `nmw-ccl-app` service principal is granted:
- **API:** Azure Service Management `user_impersonation` (Del); Log Analytics API `Data.Read` (Del).
- **Azure RBAC:** Cost Management Reader, Desktop Virtualization Reader, Monitoring Reader (all at
  **subscription** scope, all in-scope subscriptions); Reader on the Cost Attribution **Log
  Analytics workspace**; Storage Blob Data Contributor on the Cost Attribution **storage account**.

## Security / data
- **All data stays within your Azure tenant/subscription(s).**
- Cost source is moving to **Log Analytics heartbeat data** (v6.1+) as Microsoft deprecates the
  Azure consumption details API.
- Hardening: the CCL Key Vault / App Service / Storage are covered by the **Enable Private
  Endpoints** runbook — see [network-isolation.md](../../hardening/network-isolation.md).

## Open questions
- Confirm the CCL app-registration vs. App Service naming/relationship for NME 8.0 (the workbook
  lists `nmw-ccl-app` as an app registration; the architecture also describes an `nmw-ccl-app` App
  Service).
