---
id: harden-storage-account
title: Hardening — Azure Storage Account
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#harden-storage, _meta/sources.md#harden-nme]
related: [hardening-checklist, network-isolation, harden-app-service, nme-components]
---

# Hardening — Azure Storage Account

> Storage accounts hold FSLogix profiles, boot diagnostics, scripted actions, and MSIX App Attach
> packages (used by both AVD and NME). Restrict them to your VNet. Source:
> [_meta/sources.md#harden-storage].

## Requirements
- The App Service must have **VNet integration**, which requires upgrading the plan from the
  default **B3 (Basic)** to **Standard or Premium** (increased cost). See
  [harden-app-service.md](harden-app-service.md) and "Upgrade the Azure App Service."
- A VNet to connect the App Service and Storage Account, with **outbound HTTPS (TCP/443)** to the
  Nerdio licensing server `https://nwp-web-app.azurewebsites.net/`.
- **Without VNet integration, NME cannot connect to a network-restricted storage account.**

> **Warning:** misconfiguring this can cut session hosts off from FSLogix profiles, user data, and
> MSIX apps. Plan the subnet linkage before applying.

## Step 1 — Enable VNet integration on the App Service
Portal → App Service (`nmw-app-xxxxxxxxx`) → **Settings → Networking → VNet Integration →
configure → Add VNet** → select VNet → **OK**. The integration subnet must be **delegated to App
Services**, **not shared**, and **/28 or larger**. ([_meta/sources.md#harden-storage])

## Step 2 — Restrict the storage account
1. Portal → **Storage accounts** → select the account to harden.
2. **Security + networking → Networking → Firewalls and virtual networks.**
3. **Allow access from = Selected networks**; **+ Add existing virtual network**; choose the
   VNet(s) and **subnets**.
   - **If the account holds user profiles, link every subnet containing AVD session hosts** so
     FSLogix can mount profiles. **Enable.**
   - A "service endpoints enabling" message indicating up to ~15 minutes is normal.
4. **Save.**

## Step 3 — Verify in NME
Refresh the NME console and check storage locations, or retry an action that previously failed due
to restrictions (e.g. linking an MSIX App Attach location or enabling storage auto-scaling).
([_meta/sources.md#harden-storage])

## Related
[network-isolation.md](network-isolation.md) for the overall model and the Enable Private
Endpoints runbook (note its Hybrid Worker caveat when the scripted-actions storage account is made
private).
