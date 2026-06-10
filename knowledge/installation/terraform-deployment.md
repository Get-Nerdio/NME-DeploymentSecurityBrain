---
id: terraform-deployment
title: NME Terraform Deployment (alternate install path)
domain: installation
applies_to: "NME 8.0 (Terraform — Private Preview)"
last_reviewed: 2026-06-10
status: draft
sources: [_meta/sources.md#terraform-repo, _meta/sources.md#terraform-transcript, _meta/sources.md#api-permissions-xlsx]
related: [deployment-models, prerequisites, permission-matrix, install-time-permissions, nme-components, network-isolation]
---

# NME Terraform Deployment (alternate install path)

> **Status: Private Preview / MVP.** An Infrastructure-as-Code alternative to the standard Azure
> Marketplace install — it **coexists with**, and does not replace, the Marketplace path. Treat
> the two as separate procedures: don't mix Terraform steps with Marketplace/Cloud Shell steps.
> The *fundamental requirements for a working NME install are the same*; only the deployment
> mechanism differs. Sources: [_meta/sources.md#terraform-repo] (the repo README is currently the
> only documentation), [_meta/sources.md#terraform-transcript]. **This page tracks a fast-moving
> preview — hence `draft`.**

## When to use Terraform vs. Marketplace
| | Marketplace (standard) | Terraform (IaC, preview) |
|---|---|---|
| Audience | Anyone with the right privileges; no Azure infra skills needed | Orgs with a mature DevOps / Infrastructure-as-Code practice |
| Experience | Click-through; fast and simple | Requires Terraform experience; hiccups stall without it |
| Why | Fastest path to a managed NME | Repeatability, consistency, corporate IaC policy, low-cost UAT instances for testing NME updates |
| Path docs | [deployment-models.md](deployment-models.md), [step-by-step.md](step-by-step.md) | this page |

The Marketplace path and its advanced variants (custom app name, Split Identity, pre-created Entra
app) are all in [deployment-models.md](deployment-models.md). Terraform is a **distinct** path.

## What it deploys (the core platform)
The `modules/service` Terraform module provisions the same core NME footprint as a standard
install ([nme-components.md](../architecture/nme-components.md)):
- **Web tier:** Windows App Service Plan + Web App, with a package-deployment step.
- **Database:** Azure SQL Server + database, Entra ID admin config, SQL user bootstrap for the NME
  service principal (and firewall rules for Azure services + deployer IP when PEs are off).
- **Identity:** the NME **Entra ID application + service principal** — same model as the standard
  app (see parity note below), with app roles (Reviewer, HelpDesk, DesktopAdmin, WvdAdmin,
  RestClient; optional user assignments) and its RBAC role assignments.
- **Secrets/keys:** Key Vault; a data-protection key; secrets for the SQL connection string,
  Entra client secret, data-protection blob path, locks-container SAS URL.
- **Storage:** data-protection storage account with private containers.
- **Automation:** **two** Automation Accounts (updates + scripted actions) and the imported
  `nmwUpdateRunAs` runbook.
- **Monitoring:** two Log Analytics workspaces (session-host monitoring + App Insights/logs), a
  Data Collection Endpoint + Rule, and Application Insights.
- **Networking (optional):** dedicated VNet + subnets, private DNS zones, VNet peering, and
  private endpoints (see below).
- **Protection (optional):** management locks on Key Vault, SQL DB, and the data-protection
  storage account (`protect_resources = true`).

It deploys the **latest GA build** and **health-checks the app until it returns HTTP 200** before
finishing — avoiding the "refresh through a few 500s" first-load behavior of the Marketplace
PowerShell step.

### Permission parity with the standard install
The NME application Terraform creates is the **same permission model** as the standard
`nerdio-nmw-app`: identical Microsoft Graph permissions and app roles, ARM `user_impersonation`,
and the same Azure RBAC — **Reader + Backup Reader** at subscription scope and **Contributor** on
the NME resource group. So the *runtime* permission footprint is unchanged; see
[permission-matrix.md](../permissions/permission-matrix.md) §1. It uses both a client secret
(~10-year) **and** a self-signed Key Vault certificate for scripted actions.

## What it does NOT deploy (important)
The preview **cannot deploy secondary modules** — **User Cost Attribution, Real-Time Insights,
Intune Insights, and (private) WinGet repositories** are out of scope (planned for a future
version). ([_meta/sources.md#terraform-transcript])

> **State-drift warning:** if you enable those modules from the NME console *after* a Terraform
> deploy, they create Azure resources Terraform doesn't know about — producing **drift in the
> Terraform state** that must then be reconciled manually. Decide module strategy before going
> IaC. See the module pages under [knowledge/modules/](../modules/).

## Prerequisites
**Tooling on the Terraform runner:**
- Terraform `>= 1.6.0`; **PowerShell 7+** (`pwsh` on PATH — used by `local-exec` steps).
- PowerShell modules: `Az.Accounts`, `Az.Websites`, `SqlServer`.
- Providers: `azurerm >= 3.110.0`, `azuread >= 2.47.0`, plus `random`, `null`, `http`, `local`,
  `time`.
- **Resource providers must already be registered** in the subscription (root sets
  `resource_provider_registrations = "none"`).
- **No preflight script** — `terraform plan` is a rough equivalent (it confirms API access and
  that it can create the service principal), but it is not the NME pre-flight.

**Authentication** (non-interactive; set even when run outside CI): `ARM_TENANT_ID`,
`ARM_SUBSCRIPTION_ID`, `ARM_CLIENT_ID`, and either `ARM_CLIENT_SECRET` or `ARM_OIDC_TOKEN`.

## Deployer permissions (the pipeline service principal)
Distinct from the Marketplace path's *human* installer (Global Admin + subscription Owner — see
[install-time-permissions.md](../permissions/install-time-permissions.md)). The Terraform runner's
service principal needs:
- **Azure:** subscription **Owner** — *or* **Contributor + User Access Administrator** with
  delegated role assignments restricted to **Contributor, Reader, Backup Reader**.
- **Microsoft Graph (admin-consented):** `Application.ReadWrite.All` (Application),
  `AppRoleAssignment.ReadWrite.All` (Application), `Directory.Read.All` (Application), and
  `User.Read` (Delegated).

Terraform **creates** the NME service principal by default. Pre-creating it is **not** a toggle —
because this is a plain-text template (not yet a provider), you would edit the template to point
at an existing SP. ([_meta/sources.md#terraform-transcript])

## Private endpoints (optional — and one of several PE methods)
`configure_private_endpoints = true` puts every NME service behind a Private Endpoint and disables
public access (SQL/Key Vault/Storage public network access = disabled; KV default action `Deny`).
It creates a dedicated VNet (2 subnets), private DNS zones, and **bidirectional peering to a
pre-existing deployment VNet** — which is required because Terraform must reach those now-private
resources during apply (SQL bootstrap, KV writes, blob upload). So **run Terraform from a runner
on the peered deployment network.** Required vars when enabled: `deployment_vnet_name`,
`deployment_resource_group_name`, `network_config`; `private_web_app` optionally makes the portal
private too. Existing VNets/subnets can be imported.

> This is **another** way private endpoints get enabled in NME — alongside the install-time Secure
> Deployment option and the in-product Enable Private Endpoints runbook. Don't assume any one
> mechanism applies; see [network-isolation.md](../hardening/network-isolation.md).

> **Known issue:** clean PE deploys can hit **403 `ForbiddenByConnection`** on first KV writes (PE
> creation vs. DNS propagation race). Mitigate with `private_endpoint_post_resolve_delay = 60`+ or
> simply re-run `terraform apply` (resources are idempotent).

## Operational notes
- Several steps use `null_resource` with `timestamp()` triggers, so package download/deploy/
  health-check run on **every** apply (idempotent).
- The template handles the NME package download itself (no manual SAS-URL request needed).
- `terraform destroy` removes the resource group **and the NME service principal**.

## Open questions
- **No official Help Center KB exists yet** — the repo README is the only documentation; a KB
  article is planned. Revisit/cite it when published.
- No public ETA for: secondary-module support, a Terraform **Registry** module, or REST-API
  integration (manage host pools/images via Terraform) — all stated as product vision only.
- Confirm the `nmwUpdateRunAs` runbook's relationship to the deprecated Run-As model vs. the
  managed-identity update path used elsewhere ([runtime-permissions-core.md](../permissions/runtime-permissions-core.md)).
- Re-verify against the repo as the preview evolves (this page is `draft`).
