---
id: nme-components
title: NME Components & Architecture
domain: architecture
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#reference-architecture, _meta/sources.md#implementation-guide, _meta/sources.md#api-permissions-xlsx, _meta/sources.md#release-notes, _meta/sources.md#nw-se-automation-aa-2026-06-15]
related: [deployment-models, network-isolation, permission-matrix, runtime-permissions-core]
---

# NME Components & Architecture

> The moving parts of an NME deployment and how they interact. Foundational context other pages
> reference. Source: [_meta/sources.md#reference-architecture], [_meta/sources.md#implementation-guide].

## What NME is
NME is a **self-contained, API-driven Azure application** (an App Service / Web App) that runs
inside the customer's own subscription and orchestrates AVD, Windows 365, and Intune via APIs. It
sits **outside the AVD control and data planes** — it does not proxy authentication or RDP
traffic. ([_meta/sources.md#reference-architecture], [_meta/sources.md#security-faq])

## Core resources deployed (in the NME resource group)
| Resource | Role |
|---|---|
| **App Service + App Service Plan** | Hosts the NME web app / console (name prefix `nmw-app`). The solution core. |
| **Azure SQL Server + Database** | Application database. Dedicated PaaS instance, default tier **S1**, collation `Latin1_General_CP1_CI_AS`. Sharing the instance or putting the DB in an existing instance is **not supported**. |
| **Key Vault** | Secrets/tokens; encryption keys managed within Key Vault; accessed only via Managed Identity. |
| **Storage Account(s)** | Transient scripts; temporary VHDs; VM boot diagnostics; **DPS storage account for DB encryption keys** (v5.5+). |
| **Update Automation Account** | Deploys NME application updates — downloads and applies latest binaries to the App Service when an admin triggers an update. Uses a **system-assigned Managed Identity**. Formerly used the `nerdio-nmw-app-automation` Run-As app (deprecated v5.1). |
| **Scripted Actions Automation Account** | Executes NME scripted actions and user-defined runbooks against managed Azure resources. **No Managed Identity.** Authenticates as the `nerdio-nmw-app` service principal using an **Automation Certificate** — the same self-signed certificate stored in Key Vault and associated with the `nerdio-nmw-app` enterprise app. The certificate grants it full NME application identity; it must not be exported or shared. |
| **Application Insights** | Logs exceptions and API utilization. |
| **Log Analytics workspace(s)** | Host-pool/performance monitoring; tunable retention/sample rate for cost. |

**Scaling guidance:** for 200+ session hosts, scale SQL to 100 DTUs and the App Service Plan to at
least S3/P2V2. ([_meta/sources.md#reference-architecture])

## Optional / module resources
- **`nmw-ccl-app`** — a separate **App Service** for User Cost Attribution (plus a storage account
  and Log Analytics workspace; default plan P0v3). Distinct from the main `nmw-app`.
- **Intune Insights / Realtime Insights** — additional B3 App Service instances when enabled.
- **Copilot (optional AI)** — deploys its own set (App Service, Event Grid/Hub, Service Bus, AI
  Search, a separate SQL Server, AI/translation/Form-Recognizer services, Azure OpenAI, Bot
  Service, Functions, App Configuration, App Insights, Storage). ([_meta/sources.md#implementation-guide])
- **Private WinGet / Shell App repository** — a Shell App repo creates only an Azure Storage account.

## Identities
The five Entra app registrations and the Update Automation Account Managed Identity are documented in the
[glossary](../../_meta/glossary.md) and, with their permissions, in
[permission-matrix.md](../permissions/permission-matrix.md):
`nerdio-nmw-app` (primary; also the identity used by the Scripted Actions AA via certificate),
`NerdioManagerForWVD-Subscribe` (billing), `nerdio-nmw-app-automation` (legacy Run-As for Update AA, deprecated v5.1),
`nmw-rest-api-client` (REST), `nmw-ccl-app` (Cost Attribution), `nmw-ii-app` (Intune Insights).

## Resource-group topology
- A **dedicated NME resource group** holds the core components above.
- **Separate resource groups per AVD component**: one (or more) per **host pool** (recommended
  ≤100 session hosts each), one for **storage** (FSLogix profiles — Azure Files / NetApp), and RGs
  for **other management resources** such as Entra Domain Services. ([_meta/sources.md#reference-architecture])

## Data flow
- Application data → **Azure SQL**; secrets → **Key Vault**; encryption keys → **DPS storage
  account**; scripts/VHDs/boot-diagnostics transit **storage accounts**.
- NME ↔ **Azure Resource Manager** (VM/resource lifecycle), **AVD/WVD APIs**, **Microsoft Graph**,
  and (when enabled) **Intune/UEM** and **Windows 365**.
- The **Scripted Actions Automation Account** runs runbooks against managed resources as the `nerdio-nmw-app` SP (via Key Vault certificate). The **Update Automation Account** manages NME application deployments via its Managed Identity.
- **Multi-subscription/tenant:** orchestrated via API; **direct connectivity required to domain
  and file-share services**; **VNet peering** is the recommended best practice. ([_meta/sources.md#reference-architecture])

## NME 8.0 notes
- **User-Assigned Managed Identities for host pools:** admins can attach a UAMI directly in a host
  pool's Virtual Machine Settings. ([_meta/sources.md#release-notes])
- **Copilot supports private endpoints** in 8.0. See [network-isolation.md](../hardening/network-isolation.md).
- New app registrations use **certificate-based auth** by default. See
  [secrets-keyvault.md](../hardening/secrets-keyvault.md).

## Open questions
- Exact number/naming of storage accounts ("one or more" in source).
- NME 8.0 is Public Preview (GA is v7.7.4); re-verify the resource list at GA.
