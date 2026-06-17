---
id: permission-matrix
title: NME Permission Reference Matrix
domain: permissions
applies_to: "NME 8.0"
last_reviewed: 2026-06-17
status: reviewed
sources: [_meta/sources.md#api-permissions-xlsx, _meta/sources.md#azure-permissions, _meta/sources.md#graph-permissions, _meta/sources.md#azure-rbac, _meta/sources.md#release-notes, _meta/sources.md#insights-rti, _meta/sources.md#insights-intune, _meta/sources.md#nw-se-automation-aa-2026-06-15, _meta/sources.md#arm-template-80, _meta/sources.md#cloudshell-deploy-script, _meta/sources.md#configure-entra-sql-auth]
related: [install-time-permissions, runtime-permissions-core, identity-and-rbac, nme-components]
---

# NME Permission Reference Matrix

> **SINGLE SOURCE OF TRUTH for every permission NME requests.** Other pages link here rather
> than restating rows. Organized by Entra ID app registration, because NME's least-privilege
> model grants permissions per-app and most are gated behind the feature that needs them.
> Canonical source: the Nerdio API-permissions workbook ([_meta/sources.md#api-permissions-xlsx]),
> last modified 2025-12-15, cross-checked against the Azure Permissions doc.

NME uses **up to five** Entra ID app registrations. A baseline AVD-only install needs only the
core app; the rest are provisioned when their feature is enabled.

> **NME 8.0 notes** ([_meta/sources.md#release-notes]):
> - **New installs use certificate-based authentication** for app registrations by default,
>   replacing client secrets. See [secrets-keyvault.md](../hardening/secrets-keyvault.md).
> - **AVD Classic is end-of-support:** 8.0 is the **last** version supporting AVD Classic
>   (Microsoft retires it 2026-09-30). The AVD-Classic-only permissions in §1f apply only while
>   AVD Classic is in use; plan migration.

**Design principle (per Nerdio):** application-level (app-only) permissions are requested only
where strictly necessary; everything else is **delegated** (bounded by the signed-in user's own
rights). All **application** permissions require Global Administrator admin consent. See
[install-time-permissions.md](install-time-permissions.md).

Legend — **Type**: App = application (no signed-in user) · Del = delegated (on behalf of user).
**Consent**: GA = requires Global Administrator admin consent.

---

## 1. `nerdio-nmw-app` — primary application

### 1a. Azure RBAC (ARM) role assignments
Granted at install; these are how NME orchestrates Azure resources. Source: [_meta/sources.md#azure-permissions], [_meta/sources.md#reference-architecture].

| Role | Scope | Mandatory | Why |
|---|---|---|---|
| **Reader** | Subscription | Yes | Read Azure resources NME manages. |
| **Backup Reader** | Subscription | Yes | Read backup state of managed resources. |
| **Contributor** | Each managed resource group (NME RG + host-pool/storage RGs) | Yes | Create/manage AVD resources NME provisions. Scoped to managed RGs, not whole subscription. |

> The Update Automation Account's Managed Identity is separately granted **Contributor on the NME
> App Service** (to deploy application updates). ([_meta/sources.md#arm-template-80])

### 1a-SQL. SQL database roles (contained-DB, not Azure RBAC)
At install the SP is added to the application database **`FROM EXTERNAL PROVIDER`** with these
contained-database roles (the installer is set as the SQL **Entra admin**; SQL is **Entra-only
auth**). Source: [_meta/sources.md#cloudshell-deploy-script].

| DB role | Why |
|---|---|
| `db_ddladmin` | Apply schema/migrations on app updates. |
| `db_datareader` | Read application data. |
| `db_datawriter` | Write application data. |

> Note: this is the **automated install** grant. The separate **Entra-ID SQL Authentication
> hardening** flow ([_meta/sources.md#configure-entra-sql-auth]) instead adds the SP as `db_owner`
> when converting a managed SQL instance to mixed/Entra auth — don't conflate the two.

### 1b. Core Microsoft Graph + ARM permissions (always required)
Source: [_meta/sources.md#api-permissions-xlsx] sheet `nerdio-nmw-app`.

| Permission | API | Type | Consent | Why (condensed) |
|---|---|---|---|---|
| `user_impersonation` | Azure Service Management | Del | — | Query/manage Azure resources as the signed-in user (role assignments, linking subscriptions/RGs/VNets). |
| `openid` | Graph | Del | — | Sign users in via Entra. |
| `profile` | Graph | Del | — | Basic profile; run delegated tasks/audit as the calling user. |
| `offline_access` | Graph | Del | — | Maintain session/refresh tokens so users aren't re-prompted each call. |
| `User.Read` | Graph | Del | — | Read active user (name/UPN/tenant) for auditing + licensing. |
| `User.ReadBasic.All` | Graph | Del | — | Search/list users for assignment and host-pool entitlement. |
| `GroupMember.Read.All` | Graph | App | GA | Identify users by group membership (licensing de-dup, UAM, auto-shrink); resolve GUID↔UPN. |
| `Organization.Read.All` | Graph | App + Del | GA | Read tenant name/domain (subscription linking, licensing collection). |

### 1c. Directory read — two interchangeable models
v6.2+ replaces the broad `Directory.Read.All` with a least-privilege set. New v6.2+ installs use
the replacement set automatically. Source: [_meta/sources.md#api-permissions-xlsx].

| Permission | API | Type | Consent | Role |
|---|---|---|---|---|
| `Directory.Read.All` | Graph | Del | GA | Legacy single grant (pre-v6.2 default). Validates app/SP permissions only. |
| ↳ replacement set: `User.Read`, `User.ReadBasic.All`, `User.Read.All`, `Group.Read.All`, `Application.Read.All`, `Organization.Read.All` | Graph | Del/App | GA | v6.2+ least-privilege equivalent. One of the two models is required for overall functionality. |

> v7.0+: `Application.Read.All` + `Directory.Read.All` + `AppRoleAssignment.ReadWrite.All`
> (delegated) are required at deploy time to set API permissions on the new Intune Insights app
> service identity. No non-Nerdio identities are modified.

### 1d. RBAC Roles feature (managing who can use NME)
| Permission | API | Type | Consent | Mandatory | Why |
|---|---|---|---|---|---|
| `Application.ReadWrite.All` | Graph | Del | GA | No (RBAC Roles only) | Update NME's own app registration; grant AVD Admins Owner on the NME enterprise app. Delegated by design (cannot modify other apps without a consenting admin). |
| `AppRoleAssignment.ReadWrite.All` | Graph | Del | GA | No (RBAC Roles only) | Assign users/groups to NME roles. Minimum available permission for this; Entra offers nothing lesser. |
| `Application.Read.All` | Graph | Del | GA | UEM only | Enumerate apps for Conditional Access management. |

### 1e. UEM / Intune & Windows 365 (Cloud PC) — feature-gated
All require GA consent. Required only when the corresponding feature is enabled; many have
Read-only vs Manage variants (the `ReadWrite` form supersedes the `Read` form). Source:
[_meta/sources.md#api-permissions-xlsx]. Condensed — see the workbook for full per-version notes.

| Permission | API | Type | Gating feature |
|---|---|---|---|
| `Device.Read.All` | Graph | App | All UEM/Intune features (baseline). |
| `DeviceManagementManagedDevices.Read.All` / `.ReadWrite.All` | Graph | App (+Del) | Intune Managed Devices (Read / Manage). |
| `DeviceManagementServiceConfig.Read.All` / `.ReadWrite.All` | Graph | App | Intune Managed Devices (Autopilot identities/tags). |
| `DeviceManagementApps.Read.All` / `.ReadWrite.All` | Graph | App | Intune Applications & App Policies. |
| `DeviceManagementConfiguration.Read.All` / `.ReadWrite.All` | Graph | App (+Del) | Scripts / Device Policies / Cloud PC / WUfB. |
| `DeviceManagementScripts.Read.All` / `.ReadWrite.All` | Graph | Del / App+Del | Scripts; Delegated form for User Operating Mode (v7.3+). |
| `DeviceManagementManagedDevices.PrivilegedOperations.All` | Graph | App | Privileged Operations (wipe/reset/etc., Manage). |
| `BitlockerKey.Read.All` | Graph | Del | Privileged Operations (read BitLocker recovery keys). |
| `CloudPC.ReadWrite.All` | Graph | App (+Del) | Windows 365 / Cloud PC management. |
| `Group.Read.All` | Graph | App + Del | Groups for host pools, RBAC, app masking (also part of v6.2 replacement set). |
| `Group.ReadWrite.All` | Graph | App (+Del) | Intune Applications & App Policies (temp deployment groups). |
| `GroupMember.ReadWrite.All` | Graph | App | Windows 365 License Optimization / Group Membership (Manage). |
| `Policy.Read.All` | Graph | App | Conditional Access Policies (Read). |
| `Policy.ReadWrite.ConditionalAccess` | Graph | App | Conditional Access Policies (Manage). |
| `Application.Read.All` | Graph | Del | Conditional Access (enumerate apps); Intune Insights enablement (v7.0+). |
| `WindowsUpdates.ReadWrite.All` | Graph | Del + App | Windows Update for Business (WUfB) Reports. |
| `User.Read.All` | Graph | App + Del | Resolve GUID↔UPN; REST user assignment; licensing de-dup. |

### 1f. Optional & AVD-Classic-only
| Permission | API | Type | Consent | When |
|---|---|---|---|---|
| `Mail.Send` | Graph | Del | — | Optional. Notifications feature (user must explicitly link their mailbox). |
| `TenantCreator` | WVD | App | GA | AVD Classic only — create AVD tenants as the app. |
| `user_impersonation` | Windows Virtual Desktop | Del | — | AVD Classic only — query/assign externally-created AVD Classic tenants. |

---

## 2. `NerdioManagerForWVD-Subscribe` — billing / licensing app
Created during subscription activation. Source: [_meta/sources.md#api-permissions-xlsx] + [_meta/sources.md#activate-subscription].

| Permission | API | Type | Consent | Why |
|---|---|---|---|---|
| `openid` | Graph | Del | — | Authenticate the user completing billing setup. |
| `profile` | Graph | Del | — | Register the SaaS subscription on the user's behalf. |
| `User.Read` | Graph | Del | — | Identify who is purchasing, which SaaS object bills, which tenant connects. |

Data shared with Nerdio's licensing service is limited to **tenant ID, subscription ID, and NME
app registration ID** — no user/VM/session data. ([_meta/sources.md#security-faq])

## 3. `nerdio-nmw-app-automation` — legacy Run-As app (Update AA only)
**No API permissions.** Formerly the Run-As app for the **Update Automation Account** (NME
application update deployments), certificate auth only, no client secrets. **Deprecated since
v5.1** — the Update AA now uses its **system-assigned Managed Identity** instead.
([_meta/sources.md#api-permissions-xlsx])

> **Scripted Actions AA auth model (separate, current):** The **Scripted Actions Automation
> Account** has no Managed Identity and did not use `nerdio-nmw-app-automation`. The install
> script creates a self-signed Key Vault certificate (`nmw-scripted-action-cert`), imports it into
> this account as the Automation Certificate asset `ScriptedActionRunAsCert`, and adds it as a
> KeyCredential on the `nerdio-nmw-app` app registration — so the account authenticates directly as
> the `nerdio-nmw-app` service principal. Because this certificate represents NME's own application
> identity, it must not be exported or shared with other automation accounts.
> ([_meta/sources.md#cloudshell-deploy-script], [_meta/sources.md#arm-template-80]; corroborates
> [_meta/sources.md#nw-se-automation-aa-2026-06-15]) See [nme-components.md](../architecture/nme-components.md).

## 4. `nmw-rest-api-client` — REST API client
| Permission | API | Type | Consent | Why |
|---|---|---|---|---|
| `RestClient` | `nerdio-nmw-app` (custom) | App | GA | Custom role issued by the core app so the REST client can invoke commands on its behalf. Required only to operate the REST API. |

## 5. `nmw-ccl-app` — User Cost Attribution
Required only for the User Cost Attribution feature. Source: [_meta/sources.md#api-permissions-xlsx] sheet `nmw-ccl-app`.

**API permissions:**
| Permission | API | Type | Why |
|---|---|---|---|
| `user_impersonation` | Azure Service Management | Del | Query Azure resources as the user. |
| `Data.Read` | Log Analytics API | Del | Read cost/usage data from Log Analytics on the user's behalf. |

**Azure RBAC (service-principal) role assignments:**
| Role | Scope | Why |
|---|---|---|
| **Cost Management Reader** | Subscription | Read cost/usage data (inherits to resources). |
| **Desktop Virtualization Reader** | Subscription | Read host-pool properties & desktop assignments to attribute cost to users. |
| **Monitoring Reader** | Subscription | Read VM heartbeat/usage data (v6.1+ Heartbeat-based model). |
| **Reader** | Cost Attribution Log Analytics Workspace | Read session/connection data. |
| **Storage Blob Data Contributor** | Cost Attribution Storage Account | Write exported cost reports. |

## 6. `nmw-ii-app` — Intune Insights
Required only for the Intune Insights feature (v7.0+). All **Application** type, all require GA
consent, all read-only. Source: [_meta/sources.md#api-permissions-xlsx] sheet `nmw-ii-app`.

| Permission (Graph, Application) | Why |
|---|---|
| `Device.Read.All` | Read managed device configuration. |
| `DeviceManagementApps.Read.All` | Read Intune app policies/deployments. |
| `DeviceManagementConfiguration.Read.All` | Read device config/compliance policies. |
| `DeviceManagementManagedDevices.Read.All` | Read managed device details. |
| `DeviceManagementServiceConfig.Read.All` | Read enrollment/registration details. |
| `Group.Read.All` | Filter devices/users by group. |
| `User.Read.All` | Read user properties and related devices. |

**Enable-time requirements** (the admin enabling Intune Insights) — see
[modules/intune-insights/overview.md](../modules/intune-insights/overview.md):
`Microsoft.Authorization/roleAssignments/write` (Owner / RBAC Administrator / User Access
Administrator) **and** `AppRoleAssignment.ReadWrite.All` (Global Admin / Privileged Role Admin) to
grant the app's managed identity the Graph permissions above. ([_meta/sources.md#insights-intune])

## 7. Real-Time Insights — `nmw-rti-app-*` / `nmw-rti-sql*` (managed identities)
Real-Time Insights uses **system-assigned managed identities**, not app registrations. Required
only for the RTI feature (v7.0+). Source: [_meta/sources.md#insights-rti]. Full module page:
[modules/real-time-insights/overview.md](../modules/real-time-insights/overview.md).

**Enable-time (the admin enabling RTI):**
| Permission | Why |
|---|---|
| `Microsoft.Authorization/roleAssignments/write` (Owner / RBAC Administrator / User Access Administrator) | Create the role assignments below. |
| `AppRoleAssignment.ReadWrite.All` (Global Admin / Privileged Role Admin) | Grant the `nmw-rti-sql*` managed identity the Graph `Directory.Read.All` permission. |

**Granted to the RTI managed identities after provisioning:**
| Identity | Role | Scope |
|---|---|---|
| `nmw-rti-app-*` | Storage Blob Data Contributor + Storage Table Data Contributor | RTI Storage Account `stnrt*` |
| `nmw-rti-app-*` | Monitoring Reader | RTI Application Insights `nmw-rti-app-insights-*` |
| `nmw-rti-app-*` | Log Analytics Reader | RTI Log Analytics Workspace `nmw-rti-law-*` |
| `nmw-rti-sql*` | Graph `Directory.Read.All` | Tenant |

---

## Open questions
- **NME 8.0 = Public Preview** (GA is v7.7.4). Rows are verified against the permissions workbook
  (2025-12-15) with 8.0 release-note deltas applied; re-verify when 8.0 reaches GA.
- **Configuration-action RBAC:** the Azure Permissions doc lists per-action signed-in-user role
  requirements (link RG/network/subscription, create host pools, etc.) but the role/scope column
  did not render. Capture from the live doc / RBAC articles — tracked in
  [install-time-permissions.md](install-time-permissions.md).
