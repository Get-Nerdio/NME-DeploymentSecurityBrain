---
id: harden-key-vault
title: Hardening — Key Vault
domain: hardening
applies_to: "NME 8.0"
last_reviewed: 2026-06-08
status: reviewed
sources: [_meta/sources.md#harden-keyvault, _meta/sources.md#harden-nme]
related: [hardening-checklist, network-isolation, secrets-keyvault, harden-app-service, harden-sql]
---

# Hardening — Key Vault

> The Key Vault (`nmw-app-kv-xxxxxxx`) stores keys, secrets, and certificates — including the
> **SQL connection string**, so SQL connectivity depends on it. Publicly reachable by default;
> restrict via firewall + private endpoint. Source: [_meta/sources.md#harden-keyvault].

## Prerequisites
- App Service plan tier that supports **VNet integration** (default **B3** may need upgrading —
  see [harden-app-service.md](harden-app-service.md)).
- A VNet with **outbound HTTPS (TCP/443)** to the Nerdio licensing server
  `https://nwp-web-app.azurewebsites.net/`.

## Step 1 — Enable VNet integration on the App Service
App Service (`nmw-app-xxxxxxxxx`) → **Settings → Networking → Outbound traffic → Virtual network
integration → Add** → Subscription / VNet / **Subnet** → **Connect**. Subnet must be delegated to
App Services, not shared, **/28 or larger**. Then allow the addresses in "VNet integration
firewall requirements." ([_meta/sources.md#harden-keyvault])

## Step 2 — Restrict the Key Vault firewall
Key vaults → `nmw-app-kv-xxxxxxx` → **Settings → Networking → Firewalls and virtual networks**:
- **Allow access from = Allow public access from specific virtual networks and IP addresses.**
- **+ Add a virtual network** → select the VNet and **subnet** → **Enable** → **Save**.
- A "service endpoints enabling, up to ~15 min" message is normal.

## Step 3 — Create a Key Vault private endpoint
Key Vault → **Networking → Private endpoint connections → Create**:
- **Basics:** Subscription, Resource group, Name, NIC name, Region (the VNet's region).
- **Resource:** Resource type `Microsoft.KeyVault/vaults`; select the vault; target sub-resource
  auto-fills **`vault`**.
- **Virtual Network:** the VNet + subnet for the endpoint. Optionally set NSGs/UDRs (network
  policy) and an ASG.
- **DNS:** optionally **Integrate with private DNS zone** — often disabled when custom DNS points
  at internal AD; if not integrated, ensure DNS resolves the endpoint (Azure Private Endpoint DNS
  values). **Review + create → Create.**

## Step 4 — Disable public access
After the endpoint is created and DNS resolves: **Networking → Firewalls and virtual networks →
Disable public access**, and **clear "Allow trusted Microsoft services to bypass this firewall"**
→ **Apply**. Traffic now flows only through the private endpoint. ([_meta/sources.md#harden-keyvault])

## Related
The **Enable Private Endpoints** runbook automates this (and SQL, Automation, App Service) — see
[network-isolation.md](network-isolation.md). General Key Vault/secrets posture:
[secrets-keyvault.md](secrets-keyvault.md).
