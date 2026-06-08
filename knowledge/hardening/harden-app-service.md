---
id: harden-app-service
title: Hardening — App Service
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#harden-app-service, _meta/sources.md#harden-nme]
related: [hardening-checklist, network-isolation, identity-and-rbac, nme-components]
---

# Hardening — App Service

> The App Service (`nmw-app-xxxxxxxxx`) is the entry point to NME. By default it is protected by
> **Entra ID authentication (incl. MFA + Conditional Access)** but is reachable from any internet
> location. Harden it via access restrictions or a private endpoint, and disable unused FTP.
> Source: [_meta/sources.md#harden-app-service].

## Default posture
- Protected with **Entra ID auth, including MFA and Conditional Access** (enforce MFA for console
  users — see [identity-and-rbac.md](identity-and-rbac.md)).
- **Publicly reachable** from any internet location until restricted.
- **FTP is enabled by default** and can be fully disabled.

## Option A — Access restrictions (IP allowlist)
Restrict inbound so only authorized networks connect. ([_meta/sources.md#harden-app-service])
1. Azure portal → **App Services** → the NME App Service (`nmw-app-xxxxxxxxx`).
2. **Settings → Networking → Inbound traffic → Access restriction → +Add.**
3. Name/Description; **Action = Allow**; specify the source IP block. (Azure auto-adds a **Deny
   All** rule for everything else.) **Add rule.**
4. After all rules: **Networking → Public Network Access Restrictions → Site access and rules →
   Advanced tool site → Use main site rules.**
Only allowed IP ranges can connect after a few minutes.

## Option B — Private endpoint (no public ingress)
Route traffic through your VNet/private IP space instead of the public internet. ([_meta/sources.md#harden-app-service])
1. App Service → **Settings → Networking → Inbound traffic → Add** (private endpoint).
2. Name; **Subscription**; **VNet + Subnet** for the endpoint.
3. Optionally **Integrate with private DNS zone** — often disabled when customers use custom DNS
   pointing at internal AD; if not integrated, ensure DNS resolves the private endpoint (see Azure
   Private Endpoint DNS configuration). **OK.**
After a few minutes, connections to the public IP are rejected; only resolution to the private
endpoint IP succeeds.

## Disable FTP
App Service → **Settings → Configuration → General settings → FTP state → Disabled → Save.**
([_meta/sources.md#harden-app-service])

## VNet integration (outbound)
Gives the App Service line-of-sight to other hardened NME resources (Storage, Key Vault, SQL)
reachable only via private endpoints. ([_meta/sources.md#harden-app-service])
- **Requires a plan tier that supports VNet integration** (Standard/Premium/PremiumV2/PremiumV3;
  some Basic SKUs) — the default **B3** may need upgrading. See "Upgrade the Azure App Service."
- Needs a VNet with **outbound HTTPS (TCP/443)** to the Nerdio licensing server
  `https://nwp-web-app.azurewebsites.net/`.
- Subnet must be **delegated to App Services**, **not shared**, and **/28 or larger**.
- Steps: App Service → **Networking → Outbound traffic → Virtual network integration → Add** →
  pick Subscription/VNet/Subnet → **Connect**. Then allow the addresses in "VNet integration
  firewall requirements."

## Related
Component-level network restriction is part of the broader model in
[network-isolation.md](network-isolation.md); the scripted alternative is the **Enable Private
Endpoints** runbook described there.
