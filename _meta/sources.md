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

> All entries below were ingested **2026-06-08** (current as of that date per the KB). Exact
> article URLs (KB slugs) are a TODO; the article title + Help Center base identifies each.

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
  Center article's documented UI.)*

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

## Microsoft Learn
<a id="graph-permissions"></a>
- **Microsoft Graph permissions reference** — https://learn.microsoft.com/graph/permissions-reference —
  authoritative definitions of the Graph permissions named in the matrix. Ingested: 2026-06-08. Public.
<a id="azure-rbac"></a>
- **Azure built-in roles** — https://learn.microsoft.com/azure/role-based-access-control/built-in-roles —
  definitions of Reader, Contributor, Backup Reader, Cost Management Reader, etc. Ingested: 2026-06-08. Public.

## Notes
- **Version baseline:** this brain targets **NME 8.0**, which is currently **Public Preview**
  (released 2026-06-02). The latest **GA is v7.7.4**. Most install/permission/hardening
  fundamentals are carried from the current Nerdio docs (workbook dated 2025-12-15; doc PDFs
  early 2026, version notes through ~v7.4) with **NME 8.0 deltas applied from the release notes**
  ([#release-notes]). Notable 8.0 deltas reflected across pages: certificate-based auth for new
  installs (replacing client secrets), AVD Classic end-of-support (8.0 is the last supporting
  version; MS retires AVD Classic 2026-09-30), user-assigned managed identity for host pools,
  Copilot private-endpoint support, and Egress Path status on linked networks.
