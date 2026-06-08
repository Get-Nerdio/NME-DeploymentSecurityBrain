# Glossary

Canonical definitions of terms used across the brain. Link to these rather than redefining.

## Product & editions
- **NME** — Nerdio Manager for Enterprise. An Azure Marketplace application that extends and
  manages Azure Virtual Desktop, Windows 365, and Intune within a customer's own subscription.
- **Core / Premium edition** — NME's two commercial editions. Some features (e.g. Split Identity)
  are Premium-only. Edition is selected in the Marketplace Plan.
- **Secondary module** — an optional NME feature area that introduces its own app registration,
  resources, and/or permissions: **User Cost Attribution** (`nmw-ccl-app`), **Intune Insights**
  (`nmw-ii-app`), **REST API** (`nmw-rest-api-client`), **UEM / Intune**, **Windows 365 (Cloud PC)**,
  **Copilot**. See [[permission-matrix]].

## Entra ID app registrations (the "five apps")
- **`nerdio-nmw-app`** — the primary NME application identity (App Registration + Enterprise
  Application / service principal). Holds the core Graph, AVD, and ARM permissions.
- **`NerdioManagerForWVD-Subscribe`** — billing/licensing app, created during subscription activation.
- **`nerdio-nmw-app-automation`** — legacy Run-As app for the Automation Account; **deprecated since
  v5.1** in favor of the Automation Account's Managed Identity. Has no API permissions.
- **`nmw-rest-api-client`** — the REST API client app; holds the custom `RestClient` role.
- **`nmw-ccl-app`** — the User Cost Attribution app (also a separate App Service). See [[ucap-overview]].
- **`nmw-ii-app`** — the Intune Insights app. See [[intune-insights-overview]].
- **`nmw-rti-app-*` / `nmw-rti-sql*`** — Real-Time Insights **managed identities** (not app
  registrations). See [[rti-overview]].

## Module backends
- **Eido** — third-party endpoint-analytics engine behind **Intune Insights** (`eidocentral.eido.cloud`).

## Permission concepts
- **Application permission (Graph)** — app-only permission, used **without** a signed-in user.
  Always requires Global Administrator admin consent.
- **Delegated permission (Graph)** — used **on behalf of** a signed-in user, bounded by that
  user's own rights.
- **Admin consent** — tenant-wide approval of an app's permissions by a Global Administrator.
- **Install-time permission** — elevated rights (Global Administrator, subscription Owner) needed
  only during installation/consent, reducible afterward. See [[install-time-permissions]].
- **Runtime permission** — what NME uses on an ongoing basis post-install (largely via Managed
  Identity / its service principal). See [[runtime-permissions-core]].

## Identity / install models
- **Managed Identity** — Azure-managed service identity NME uses post-install for secure access
  (e.g. Key Vault, Automation Account) without stored credentials.
- **Split Identity** — Premium advanced-install model where user identities live in a separate
  Entra tenant from where VMs/session hosts are deployed. See [[deployment-models]].
- **DPS storage account** — dedicated storage account holding the database encryption keys (v5.5+).

## AVD
- **AVD Classic / WVD Classic** — the legacy (pre-ARM) Azure Virtual Desktop object model;
  requires the `TenantCreator` and WVD `user_impersonation` permissions when enabled.
- **MAU (Monthly Active User)** — NME's billing unit: a unique user who connected to an AVD
  desktop in the past month or held a Windows 365 Enterprise Cloud PC assignment in the past month.
