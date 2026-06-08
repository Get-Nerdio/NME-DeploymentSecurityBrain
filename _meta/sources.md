# Sources — Provenance Ledger

Every non-trivial fact in this brain cites a source recorded here. Add an entry, give it an
anchor, and reference it from a page's `sources:` frontmatter (e.g. `_meta/sources.md#security-faq`).

All sources below are official Nerdio documentation (Nerdio Help Center,
`https://nmehelp.getnerdio.com`) or the Nerdio API-permissions workbook, captured into
[../ingest/](../ingest/) for Phase 1 ingestion. Dates are the source's own "last modified" where
shown. Public unless marked otherwise.

## Nerdio — permissions (authoritative)
<a id="api-permissions-xlsx"></a>
- **Nerdio Manager for Enterprise – API Permissions (workbook)** — `ingest/Nerdio Manager for Enterprise - API Permissions.xlsx`.
  Last modified **2025-12-15**. One worksheet per Entra app registration (`nerdio-nmw-app`,
  `NerdioManagerForWVD-Subscribe`, `nerdio-nmw-app-automation`, `nmw-rest-api-client`,
  `nmw-ccl-app`, `nmw-ii-app`). The canonical, per-permission source for the permission matrix.
  Covers version-introduction notes through v7.3+. Verified: 2026-06-08.
<a id="azure-permissions"></a>
- **Azure Permissions and Nerdio Manager** — `ingest/Azure Permissions and Nerdio Manager – Nerdio Manager for Enterprise.pdf`.
  ARM RBAC roles for the primary app (Reader, Backup Reader), install-time vs ongoing permissions,
  configuration-action permissions. Verified: 2026-06-08.
<a id="security-faq"></a>
- **Security and Permissions FAQs** — `ingest/Security and Permissions FAQs – Nerdio Manager for Enterprise.pdf`.
  Hardening guidance: private-endpoint models, Key Vault/Managed Identity, token isolation,
  least-privilege design, data shared with licensing. Verified: 2026-06-08.

## Nerdio — installation
<a id="install-guide"></a>
- **Nerdio Manager Installation Guide** — `ingest/Nerdio Manager Installation Guide – Nerdio Manager for Enterprise.pdf`.
  Marketplace deploy, Cloud Shell initialization, configuration wizard, admin consent. Verified: 2026-06-08.
<a id="install-prep"></a>
- **Nerdio Manager Installation Preparation Steps** — `ingest/Nerdio Manager Installation Preparation Steps – Nerdio Manager for Enterprise.pdf`.
  Prerequisites, App Service Plan quota, pre-flight script, networking prereqs. Verified: 2026-06-08.
<a id="adv-install"></a>
- **Advanced Installation Methods** — `ingest/Advanced Installation Methods – Nerdio Manager for Enterprise.pdf`.
  Custom app name, split identity, pre-created Entra app. Verified: 2026-06-08.
<a id="create-entra-app"></a>
- **Advanced installation: Create Entra ID application** — `ingest/Advanced installation: Create Entra ID application – Nerdio Manager for Enterprise.pdf`.
  Pre-created Entra app registration details (app roles, redirect URIs, permissions). Verified: 2026-06-08.
<a id="split-identity"></a>
- **Advanced Installation: Split Identity** — `ingest/Advanced Installation: Split Identity – Nerdio Manager for Enterprise.pdf`.
  Premium split-identity model, prerequisites, limitations, verification. Verified: 2026-06-08.
<a id="activate-subscription"></a>
- **Activate your subscription** — `ingest/Activate your subscription – Nerdio Manager for Enterprise.pdf`.
  SaaS billing offer, `NerdioManagerForWVD-Subscribe` app, MAU billing. Verified: 2026-06-08.

## Nerdio — architecture & maintenance
<a id="reference-architecture"></a>
- **Nerdio Manager for Enterprise reference architecture** — `ingest/Nerdio Manager for Enterprise reference architecture – Nerdio Manager for Enterprise.pdf`.
  Components deployed, resource-group topology, networking/peering, data flow. Verified: 2026-06-08.
<a id="implementation-guide"></a>
- **Nerdio Manager for Enterprise Implementation Guide** — `ingest/Nerdio Manager for Enterprise Implementation Guide-2.pdf`.
  Install wizard detail, private-endpoint tab, optional resources (Copilot, Cost Attribution). Verified: 2026-06-08.
<a id="update-app"></a>
- **Update the Nerdio Manager application** — `ingest/Update the Nerdio Manager application – Nerdio Manager for Enterprise.pdf`.
  Five update methods + least-privilege rights per method, hardened-environment restore. Verified: 2026-06-08.
<a id="release-notes"></a>
- **Release Notes** — `ingest/Release Notes – Nerdio Manager for Enterprise.pdf`. Per-version
  changelog. **v8.0 = Public Preview, release date 2026-06-02; latest GA = v7.7.4 (2026-05-21).**
  Source of the NME 8.0 deltas applied to this brain. Verified: 2026-06-08.

## Microsoft Learn
<a id="graph-permissions"></a>
- **Microsoft Graph permissions reference** — https://learn.microsoft.com/graph/permissions-reference —
  authoritative definitions of the Graph permissions named in the matrix. Verified: 2026-06-08. Public.
<a id="azure-rbac"></a>
- **Azure built-in roles** — https://learn.microsoft.com/azure/role-based-access-control/built-in-roles —
  definitions of Reader, Contributor, Backup Reader, Cost Management Reader, etc. Verified: 2026-06-08. Public.

## Notes
- **Version baseline:** this brain targets **NME 8.0**, which is currently **Public Preview**
  (released 2026-06-02). The latest **GA is v7.7.4**. Most install/permission/hardening
  fundamentals are carried from the current Nerdio docs (workbook dated 2025-12-15; doc PDFs
  early 2026, version notes through ~v7.4) with **NME 8.0 deltas applied from the release notes**
  ([#release-notes]). Notable 8.0 deltas reflected across pages: certificate-based auth for new
  installs (replacing client secrets), AVD Classic end-of-support (8.0 is the last supporting
  version; MS retires AVD Classic 2026-09-30), user-assigned managed identity for host pools,
  Copilot private-endpoint support, and Egress Path status on linked networks.
