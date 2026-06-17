# Sources — Provenance Ledger

Every non-trivial fact in this brain cites a source recorded here. Add an entry, give it an
anchor, and reference it from a page's `sources:` frontmatter (e.g. `_meta/sources.md#security-faq`).

## Provenance & freshness policy
- **Origin:** unless marked otherwise, every source is an official **Nerdio Help Center** article
  at `https://nmehelp.getnerdio.com` (Zendesk KB), or the Nerdio API-permissions workbook.
- **Snapshots:** docs are pulled into [../ingest/](../ingest/), which is **gitignored** — so *this
  ledger is the authoritative record of what was ingested*. The binaries are not in git.
- **Two distinct dates per entry:**
  - **Dated / Last modified** = the article's *own* last-modified date shown in the KB (the content's age).
  - **Ingested** = when *we* pulled the snapshot. Because the KB is live and changes under us, this
    is what tells you how current our copy is.
- **Ingested ≠ page freshness.** A page's `last_reviewed` is when that page was checked; it does
  not move when a source is re-pulled. **When you re-ingest a doc, bump its `Ingested` date here
  and re-verify every page whose `sources:` reference it.**
- Public unless marked otherwise.

### Confidence tiers (every entry has one)
Each source declares a **`Confidence:`** tier so readers and reviewers know how much weight a fact
carries. When omitted, an entry defaults to **`authoritative`** (the ledger's origin policy is
"official doc unless marked otherwise"). **Any non-document source — verbal/SME, a meeting, a
Slack thread — MUST set its tier explicitly**, and the validator enforces this.

| Tier | Meaning | Use for |
|---|---|---|
| **`authoritative`** | First-party documentation or shipped artifact. | Official Nerdio/Microsoft docs, the API-permissions workbook, **deployment artifacts** (ARM templates, install scripts), product source/repos. |
| **`corroborated`** | A verbal/SME claim that is **backed by ≥1 authoritative source**. | An SE's correction that we then confirmed against a doc, artifact, or code. Cite **both** the SME entry and the corroborating source on the page. |
| **`reported`** | A verbal/SME claim with **no supporting document yet**. Lowest confidence. | A new SE contribution we could not (yet) corroborate. **Flag in the PR**, and flag inline on the page (Assumptions / "reported, unverified"). Aim to upgrade to `corroborated` later. |

**Contributor rule:** when someone gives you a fact, **ask for a corroborating document**. If they
provide one, record the fact as `corroborated` (citing both). If they cannot, record it as
`reported`, attribute it to the named SME, and **flag the verbal contribution in the PR for
reviewer scrutiny**. Never silently promote a `reported` fact to `authoritative`.

> All entries below were ingested **2026-06-08** (current as of that date per the KB). Exact
> article URLs (KB slugs) are a TODO; the article title + Help Center base identifies each.
> Entries without an explicit `Confidence:` line are **`authoritative`** (official docs/artifacts).

## Nerdio — permissions (authoritative)
<a id="api-permissions-xlsx"></a>
- **Nerdio Manager for Enterprise – API Permissions (workbook)** — `ingest/Nerdio Manager for Enterprise - API Permissions.xlsx`.
  Last modified **2025-12-15**. One worksheet per Entra app registration (`nerdio-nmw-app`,
  `NerdioManagerForWVD-Subscribe`, `nerdio-nmw-app-automation`, `nmw-rest-api-client`,
  `nmw-ccl-app`, `nmw-ii-app`). The canonical, per-permission source for the permission matrix.
  Covers version-introduction notes through v7.3+. Ingested: 2026-06-08.
<a id="azure-permissions"></a>
- **Azure Permissions and Nerdio Manager** — `ingest/Azure Permissions and Nerdio Manager – Nerdio Manager for Enterprise.pdf`.
  ARM RBAC roles for the primary app (Reader, Backup Reader), install-time vs ongoing permissions,
  configuration-action permissions. Ingested: 2026-06-08.
<a id="security-faq"></a>
- **Security and Permissions FAQs** — `ingest/Security and Permissions FAQs – Nerdio Manager for Enterprise.pdf`.
  Hardening guidance: private-endpoint models, Key Vault/Managed Identity, token isolation,
  least-privilege design, data shared with licensing. Ingested: 2026-06-08.

## Nerdio — installation
<a id="install-guide"></a>
- **Nerdio Manager Installation Guide** — `ingest/Nerdio Manager Installation Guide – Nerdio Manager for Enterprise.pdf`.
  Marketplace deploy, Cloud Shell initialization, configuration wizard, admin consent. Ingested: 2026-06-08.
<a id="install-prep"></a>
- **Nerdio Manager Installation Preparation Steps** — `ingest/Nerdio Manager Installation Preparation Steps – Nerdio Manager for Enterprise.pdf`.
  Prerequisites, App Service Plan quota, pre-flight script, networking prereqs. Ingested: 2026-06-08.
<a id="adv-install"></a>
- **Advanced Installation Methods** — `ingest/Advanced Installation Methods – Nerdio Manager for Enterprise.pdf`.
  Custom app name, split identity, pre-created Entra app. Ingested: 2026-06-08.
<a id="create-entra-app"></a>
- **Advanced installation: Create Entra ID application** — `ingest/Advanced installation: Create Entra ID application – Nerdio Manager for Enterprise.pdf`.
  Pre-created Entra app registration details (app roles, redirect URIs, permissions). Ingested: 2026-06-08.
<a id="split-identity"></a>
- **Advanced Installation: Split Identity** — `ingest/Advanced Installation: Split Identity – Nerdio Manager for Enterprise.pdf`.
  Premium split-identity model, prerequisites, limitations, verification. Ingested: 2026-06-08.
<a id="activate-subscription"></a>
- **Activate your subscription** — `ingest/Activate your subscription – Nerdio Manager for Enterprise.pdf`.
  SaaS billing offer, `NerdioManagerForWVD-Subscribe` app, MAU billing. Ingested: 2026-06-08.

## Nerdio — architecture & maintenance
<a id="reference-architecture"></a>
- **Nerdio Manager for Enterprise reference architecture** — `ingest/Nerdio Manager for Enterprise reference architecture – Nerdio Manager for Enterprise.pdf`.
  Components deployed, resource-group topology, networking/peering, data flow. Ingested: 2026-06-08.
<a id="implementation-guide"></a>
- **Nerdio Manager for Enterprise Implementation Guide** — `ingest/Nerdio Manager for Enterprise Implementation Guide-2.pdf`.
  Install wizard detail, private-endpoint tab, optional resources (Copilot, Cost Attribution). Ingested: 2026-06-08.
<a id="update-app"></a>
- **Update the Nerdio Manager application** — `ingest/Update the Nerdio Manager application – Nerdio Manager for Enterprise.pdf`.
  Five update methods + least-privilege rights per method, hardened-environment restore. Ingested: 2026-06-08.
<a id="release-notes"></a>
- **Release Notes** — `ingest/Release Notes – Nerdio Manager for Enterprise.pdf`. Per-version
  changelog. **v8.0 = Public Preview, release date 2026-06-02; latest GA = v7.7.4 (2026-05-21).**
  Source of the NME 8.0 deltas applied to this brain. Ingested: 2026-06-08.

## Nerdio — privacy & licensing telemetry
<a id="customer-data-privacy"></a>
- **Does Nerdio Manager Store Customer Information?** — `ingest/Does Nerdio Manager Store Customer Information? – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-03-22. Authoritative statement: NME does not collect customer data; Nerdio staff
  have no access unless granted. Documents the full list of licensing/usage telemetry sent to
  Nerdio's licensing system (Azure SQL, North Central US, encrypted at rest/in transit): registration
  info, user/host/CPU counts, host pool names/IDs, cost metrics, feature enablement flags. v5.1+
  adds feature usage reporting (no PII); opt-out via support. Veracode Verified Standard.
  Ingested: 2026-06-15.

## Nerdio — component hardening (Setup & Settings › Nerdio Components and Customization)
All dated 2026-05-05.
<a id="harden-nme"></a>
- **Harden Nerdio Manager** — `ingest/Harden Nerdio Manager – Nerdio Manager for Enterprise.pdf`.
  Overview of the four hardening areas + the **Enable Private Endpoints** Azure runbook (params,
  Hybrid Worker caveat). Ingested: 2026-06-08.
<a id="harden-app-service"></a>
- **Harden App Service** — `ingest/Harden App Service – Nerdio Manager for Enterprise.pdf`.
  Default Entra ID auth (MFA + CA), access restrictions, App Service private endpoint, disable
  FTP, VNet integration. Ingested: 2026-06-08.
<a id="harden-sql"></a>
- **Harden SQL** — `ingest/Harden SQL – Nerdio Manager for Enterprise.pdf`.
  TLS + TDE defaults; restrict SQL to App Service outbound IPs; route via VNet service endpoint.
  Ingested: 2026-06-08.
<a id="harden-storage"></a>
- **Harden Azure Storage Account** — `ingest/Harden Azure Storage Account – Nerdio Manager for Enterprise.pdf`.
  VNet integration + storage firewall; FSLogix subnet caveat. Ingested: 2026-06-08.
<a id="harden-keyvault"></a>
- **Harden key vault** — `ingest/Harden key vault – Nerdio Manager for Enterprise.pdf`.
  VNet integration → KV firewall (selected networks) → KV private endpoint → disable public access.
  Ingested: 2026-06-08.
<a id="configure-entra-sql-auth"></a>
- **Configure Entra ID SQL Authentication** — `ingest/Configure Entra ID SQL Authentication – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-29. Convert managed SQL to mixed mode, add NME service principal as `db_owner`,
  update the Key Vault connection string, restrict to Entra-only auth. Ingested: 2026-06-08.

## Nerdio — networking / firewall
<a id="vnet-firewall"></a>
- **VNet integration firewall requirements** — `ingest/VNet integration firewall requirements – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-29. Outbound addresses + service tags the **NME App Service** needs when
  VNet-integrated (licensing, ARM/AVD mgmt, Graph/Entra auth, SQL, Key Vault, App Insights, Log
  Analytics, GitHub). Ingested: 2026-06-08.
<a id="session-host-outbound"></a>
- **Required outbound internet access from AVD session host VMs** — `ingest/Required outbound internet access from AVD session host VMs – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Required/optional session-host egress + service tags, FSLogix SMB 445,
  deprecated agent URLs, DSC-extension retirement (2028-03-31) → service tags, scripted-action
  download hosts, WinRM/DVD-ROM notes. Ingested: 2026-06-08.

## Nerdio — modules
<a id="ucap-overview"></a>
- **User cost attribution overview** — `ingest/User cost attribution overview – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-03-22. Premium-only; prerequisites; CCL service-principal permissions; not supported
  with Split Identity; heartbeat (LAW) data migration. Ingested: 2026-06-08.
<a id="insights-costs"></a>
- **Insights: Costs and efficiency** — `ingest/Insights: Costs and efficiency – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Surfaces User Cost Attribution (Public Preview) + Operational Efficiency.
  Ingested: 2026-06-08.
<a id="insights-rti"></a>
- **Insights: Real-Time** — `ingest/Insights: Real-Time – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Enable-time permissions, `nmw-rti-app-*` / `nmw-rti-sql*` managed-identity
  grants, resources created, polling/thresholds. Ingested: 2026-06-08.
<a id="insights-intune"></a>
- **Insights: Intune** — `ingest/Insights: Intune – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Prerequisites, DB/App sizing, **outbound port requirements (Eido backend)**,
  enable flow + resources. NOTE: its "Minimum Permissions" block appears copy-pasted from RTI
  (references `nmw-rti-*`); authoritative `nmw-ii-app` permissions are in the workbook
  ([#api-permissions-xlsx]). Ingested: 2026-06-08.

## Nerdio — code (GitHub)
<a id="enable-pe-script"></a>
- **Enable Private Endpoints (Azure runbook)** — `Get-Nerdio/NMW`,
  `scripted-actions/azure-runbooks/Enable Private Endpoints.ps1`
  (https://github.com/Get-Nerdio/NMW/blob/main/scripted-actions/azure-runbooks/Enable%20Private%20Endpoints.ps1).
  Authoritative source for the private-endpoint runbook's parameters and the resulting private
  network architecture. Ingested: 2026-06-08. Public. *(Code on `main` may be ahead of the Help
  Center article's documented UI. This is **one** way private endpoints are enabled — not the only
  one; e.g. the install-time Secure Deployment option also provisions them — see [#implementation-guide].)*
<a id="nme-network-test"></a>
- **NmeNetworkTest.ps1** — `Get-Nerdio/NME-SE`, `NmeNetworkTest.ps1`
  (https://github.com/Get-Nerdio/NME-SE/blob/main/NmeNetworkTest.ps1). Diagnostic that tests **NME
  App Service** outbound + dependency connectivity (licensing, Graph/Entra auth, ARM, monitoring
  APIs, and auto-detected Key Vault / SQL / DPS storage over local DNS). Run from the App Service
  Kudu/SCM debug console. Ingested: 2026-06-08. Public.
<a id="test-outbound-avd"></a>
- **Test Outbound Connections from AVD Host (Azure runbook)** — `Get-Nerdio/NMW`,
  `scripted-actions/azure-runbooks/Test Outbound Connections from AVD Host.ps1`
  (https://github.com/Get-Nerdio/NMW/blob/main/scripted-actions/azure-runbooks/Test%20Outbound%20Connections%20from%20AVD%20Host.ps1).
  NME runbook that tests **AVD session-host** egress to required AVD endpoints + the scripted-actions
  storage account, via `Invoke-AzVMRunCommand` (bypasses storage so it works during outages).
  Ingested: 2026-06-08. Public.

## Nerdio — Terraform deployment (Private Preview)
<a id="terraform-repo"></a>
- **NME Terraform repository** — `Get-Nerdio/NME-Terraform` (snapshot in `ingest/NME-Terraform-main/`).
  `README.md` is the authoritative (and currently only) documentation; `modules/service/*.tf`
  inspected for the Entra app, RBAC, automation, and networking specifics. Covers the IaC
  alternate install path. Ingested: 2026-06-10. Public.
<a id="terraform-transcript"></a>
- **"Nerdio under the hood — Terraform" deep-dive (Roan)** — `ingest/roan terraform deep dive.txt`.
  Internal meeting transcript (2026-06-10): positioning vs Marketplace, Private Preview/MVP status,
  what it does/doesn't deploy (no secondary modules → state drift), SP creation, vision/no-ETA.
  Ingested: 2026-06-10. **Internal / non-public.**

## Nerdio — resilience & BCDR
All sourced from the Nerdio Help Center unless marked otherwise.
<a id="bcdr-avd"></a>
- **Business continuity and disaster recovery (BCDR) guidance for AVD environments with Nerdio Manager** —
  `ingest/bcdr-avd-nme.pdf`. Dated 2026-03-22. Architecture guidance for three outage scenarios
  (local corruption, AZ failure, full region outage); AVD component DR responsibility table; key
  framing that NME is not in the critical path for user sessions. Ingested: 2026-06-15.
<a id="nme-ha-dr-webapp"></a>
- **Configure the Nerdio Manager web app for high availability (HA) or disaster recovery (DR) scenarios** —
  `ingest/nme-ha-dr-webapp.pdf`. Dated 2026-05-05. Covers all four NME protection layers; the
  `configure_resilience.ps1` script; limitations table; Known Issues (AFD propagation, AADSTS50011).
  Important caveat: "As of NME v6.5, HA is supported for the web app layer only … the SQL database
  layer is classed as a DR invocation action due to the active/passive nature of SQL failover
  groups." Ingested: 2026-06-15.
<a id="host-pool-dr-kb"></a>
- **Host Pool Disaster Recovery** — `ingest/Host Pool Disaster Recovery – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Active-active pooled host pool DR; FSLogix Cloud Cache requirements;
  configuration walkthrough (Properties → Disaster Recovery); auto-scale integration. Ingested: 2026-06-15.
<a id="nme-backup-restore-kb"></a>
- **Back up and restore NME configuration** — `ingest/Back up and restore NME configuration – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Updated strategy (Feb 2025+): three components (KV, SQL, App Service), backup
  frequencies, custom backup scripts (`app-service-backup.ps1`, `key-vault-backup.ps1`), restore
  procedures, hardened-env SQL firewall note. Ingested: 2026-06-15.
<a id="sql-zone-resilient"></a>
- **Configure SQL database for zone resilient mode** — `ingest/Configure SQL database for zone resilient mode – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-03-22. Upgrade SQL to Premium DTU tier, enable zone redundancy; note that Basic/Standard
  DTU tiers do not support zone redundancy. Ingested: 2026-06-15.
<a id="app-zone-resilient"></a>
- **Configure the application for zone resilient mode** — `ingest/Configure the application for zone resilient mode – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Create ZRS storage + locks container, generate SAS token, add env var or KV
  secret, create zone-redundant App Service Plan (Premium/Isolated), migrate App Service. Ingested: 2026-06-15.
<a id="db-resilience-kb"></a>
- **Configure Nerdio Manager Database Resilience** — `ingest/Configure Nerdio Manager Database Resilience – Nerdio Manager for Enterprise.pdf`.
  Dated 2026-05-05. Premium-only; two-part procedure: (A) create failover group in NME UI, (B) edit
  `ConnectionStrings--DefaultConnection` in Key Vault with the failover-group endpoint and restart the
  App Service. Default failover policy = **Automatic** (auto-failover + auto-failback); can be changed
  to Manual via Azure portal. Distinguishes Failover (full sync, no data loss) vs Forced Failover
  (immediate switch, potential data loss). Ingested: 2026-06-15.
<a id="ha-talking-points"></a>
- **Nerdio HA/DR TAM Talking Points v3.11** — `ingest/HA_TalkingPoints_v3_11.pdf`. Dated May 2026.
  Internal TAM guide: all four protection layers with step-by-step walkthroughs, key framing
  ("NME not in critical path"), failover policy comparison, known issues, Host Pool DR architecture,
  `configure_resilience.ps1` script deep-dive. **Internal / non-public — Nerdio Confidential,
  TAM Internal Use.** Ingested: 2026-06-15.

## Microsoft Learn
<a id="graph-permissions"></a>
- **Microsoft Graph permissions reference** — https://learn.microsoft.com/graph/permissions-reference —
  authoritative definitions of the Graph permissions named in the matrix. Ingested: 2026-06-08. Public.
<a id="azure-rbac"></a>
- **Azure built-in roles** — https://learn.microsoft.com/azure/role-based-access-control/built-in-roles —
  definitions of Reader, Contributor, Backup Reader, Cost Management Reader, etc. Ingested: 2026-06-08. Public.

## Nerdio — deployment artifacts (ARM template & install scripts)
Primary-source deployment artifacts pulled directly from an NME 8.0.1 Marketplace deployment.
These are authoritative for *what is actually deployed* (resource SKUs, security settings, the
identity/cert/secret setup) and override prose docs where they conflict.

<a id="arm-template-80"></a>
- **NME 8.0.1 ARM deployment template** — `ingest/template-8.0/template.json` + `parameters.json`
  (Bicep-generated). The Marketplace/`Microsoft.Resources/deployments` template that provisions all
  core NME resources. Authoritative for initial resource **SKUs/sizes**, security properties (TLS,
  public-network-access, Entra-only SQL auth, resource locks), the **two automation accounts**, the
  Data Protection key/storage wiring, and the optional private-endpoint topology. Package version
  **8.0.1**. Ingested: 2026-06-17. (Semi-public: delivered to every customer at deploy time.)
<a id="cloudshell-deploy-script"></a>
- **NME 8.0.1 post-deployment init script** — `ingest/cloudshell-deploy.ps1` (the Cloud Shell
  command body), identical in body to `ingest/deploy-custom-app-name/install-az.ps1` and
  `ingest/deploy-precreated-app/install-az.ps1` (verified byte-identical apart from the header
  parameter block + CRLF). Runs after the ARM deploy: creates/updates the Entra app + app roles +
  API permissions, the 10-yr client secret, the scripted-actions certificate, configures SQL
  (Entra admin + SP DB roles), assigns Azure RBAC, sets app settings, and MSDeploy-publishes the
  app package. Authoritative for the **identity/secret/cert provisioning** and **install
  sequence**. Ingested: 2026-06-17. **Internal** (contains tenant-specific values in the header).

## Nerdio — internal SME (verbal / no document)
Entries in this section have no ingested file. **Dated** = date the information was shared;
**Ingested** = same date (date recorded here). These are lower-confidence than official docs —
flag for replacement if a Help Center article or workbook entry is ever published that covers
the same ground.

<a id="nw-se-automation-aa-2026-06-15"></a>
- **Nick Wagner, Nerdio SE — verbal clarification (2026-06-15).** Two-automation-account
  architecture: the **Update AA** uses a system-assigned Managed Identity (replaced the
  `nerdio-nmw-app-automation` Run-As app at v5.1) and handles NME binary deployments to the
  App Service. The **Scripted Actions AA** has no Managed Identity; it holds the
  `nerdio-nmw-app` enterprise app's Key Vault certificate as an Automation Certificate and
  uses it to authenticate as the `nerdio-nmw-app` service principal. The certificate must not
  be exported as it is NME's own application identity. Corrects prior conflation of both
  accounts into one. No document exists; sourced from direct product knowledge.
  **Corroborated 2026-06-17** by the 8.0.1 ARM template ([#arm-template-80]) and deploy script
  ([#cloudshell-deploy-script]), which independently show the two accounts and the full cert flow
  (`nmw-scripted-action-cert` → asset `ScriptedActionRunAsCert` → app KeyCredential). Those
  artifacts are now the primary citation for these facts on the pages; this entry records the
  origin/first report.
  Dated: 2026-06-15. Ingested: 2026-06-15. **Confidence: corroborated** (verbal SME, since
  confirmed by [#arm-template-80] + [#cloudshell-deploy-script]; was `reported` when first added).
  **Internal.**

## Notes
- **Version baseline:** this brain targets **NME 8.0**, which is currently **Public Preview**
  (released 2026-06-02). The latest **GA is v7.7.4**. Most install/permission/hardening
  fundamentals are carried from the current Nerdio docs (workbook dated 2025-12-15; doc PDFs
  early 2026, version notes through ~v7.4) with **NME 8.0 deltas applied from the release notes**
  ([#release-notes]). Notable 8.0 deltas reflected across pages: certificate-based auth for new
  installs (replacing client secrets), AVD Classic end-of-support (8.0 is the last supporting
  version; MS retires AVD Classic 2026-09-30), user-assigned managed identity for host pools,
  Copilot private-endpoint support, and Egress Path status on linked networks.
