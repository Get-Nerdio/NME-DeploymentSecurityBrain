---
id: host-pool-dr
title: Host Pool Disaster Recovery
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#host-pool-dr-kb, _meta/sources.md#ha-talking-points]
related: [resilience-overview, avd-bcdr-guidance]
---

# Host Pool Disaster Recovery

> **Premium edition only. Independent of NME control-plane HA.**
> Active-active DR at the host pool level: new VMs are distributed 50/50 between a primary and
> secondary Azure region, FSLogix profiles are replicated in real-time via Cloud Cache, and
> failover is automatic if one region goes offline. No manual runbook execution required.
> Sources: [_meta/sources.md#host-pool-dr-kb], [_meta/sources.md#ha-talking-points] (internal).

## What it does (vs NME HA)

| Dimension | NME control-plane HA | Host Pool DR |
|---|---|---|
| Protects | NME web app + database | Session host VMs users connect to |
| Pattern | Active/passive (AFD + SQL failover groups) | Active/active (VMs in both regions simultaneously) |
| Failover trigger | Health probe failure / manual | Automatic — AVD routes to surviving region |
| Profile replication | n/a | FSLogix Cloud Cache (synchronous, both regions on every write) |

Both tracks are needed for full resilience; neither replaces the other.
([_meta/sources.md#ha-talking-points])

## Requirements

| Requirement | Detail |
|---|---|
| Edition | Nerdio Manager **Premium** |
| Host pool type | **Pooled** only — personal (single-user) host pools are not supported |
| Network | Both regions must have line-of-sight to Active Directory domain controllers (VNet peering + DC VMs in secondary region, or Entra ID Join) |
| Azure Compute Gallery | Desktop image must be stored in ACG and **already replicated to both regions** before DR can be enabled — confirm this in pre-work |
| FSLogix profile | The profile assigned to the host pool must have **Cloud Cache enabled**. Create a new profile or modify the existing one, then select it on the FSLogix properties page |
| Existing hosts | Must be **deleted and recreated** after enabling DR so they are provisioned with the dual-region Cloud Cache configuration |

## Configuration

Host Pool DR is configured per host pool (not globally).

### Part 1 — Enable DR on the host pool

1. Locate the host pool.
2. Action menu → **Properties → Disaster Recovery**.
3. Toggle **Enable Disaster Recovery** on.
4. **Secondary VM Prefix:** prefix for session hosts created in the secondary region. Max 10
   characters; system appends `-xxxx` for uniqueness. Do not add a trailing hyphen.
5. **Secondary Network:** network in the secondary region that 50% of new VMs connect to. The
   selected network determines the Azure region of those VMs.
6. **Secondary Resource Group:** resource group in the secondary region for the secondary VMs.
7. **Desktop Image (Template):** must be in Azure Compute Gallery, replicated to both regions.
8. **Secondary FSLogix Storage:** FSLogix storage location in the secondary region.
9. **Secondary FSLogix Office Container:** office container location in the secondary region (if
   applicable).
10. Select **Save** or **Save & close**.

### Part 2 — Review auto-scale configuration

After enabling DR, the host pool's auto-scale configuration must reference the same image and
account for both regions.

1. Same host pool → action menu → **Auto-scale → Configure**.
2. Confirm **Desktop Image (Template)** matches the DR configuration.
3. In **Host Pool Sizing**, set the **Base host pool capacity** to account for VMs in both
   regions.
4. Select **Save & close**.

## How it works at runtime

- All new VMs created by NME auto-scale are distributed: half configured with the primary region
  FSLogix storage as primary (and secondary as backup), half with the opposite.
- FSLogix Cloud Cache writes profile data to both regions **synchronously** on every write —
  this adds latency compared to a single-region profile setup. Test with latency-sensitive
  workloads before committing.
- If a region goes offline, AVD automatically routes users to the surviving region — no
  administrator action required.

## Operational notes

- **Image replication is a prerequisite, not an afterthought.** Confirm ACG replication is in
  place before starting configuration. This is a common blocker discovered too late.
- **Existing hosts must be rebuilt.** Plan a maintenance window — this is disruptive to users.
  Size the conversation accordingly.
- **BgInfo extension:** NME does not install the BgInfo Azure extension during automation. It
  may be installed via a scripted action or unintentionally through the Azure PowerShell module
  (see the Azure PowerShell module issues report for details). ([_meta/sources.md#host-pool-dr-kb])

## Open questions

- Confirm whether the Entra ID Join path (no AD line-of-sight requirement) is fully supported
  for Host Pool DR in NME 8.0, or still future roadmap.
