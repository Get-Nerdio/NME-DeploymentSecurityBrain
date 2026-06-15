---
id: avd-bcdr-guidance
title: AVD BCDR — Three-Scenario Guidance
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#bcdr-avd, _meta/sources.md#ha-talking-points]
related: [resilience-overview, host-pool-dr, nme-backup-restore, nme-zone-resilience, nme-database-resilience, nme-regional-resilience]
---

# AVD BCDR — Three-Scenario Guidance

> Architecture-level guidance for protecting the full AVD environment across three outage types.
> NME HA protects only the management plane; full BCDR requires decisions across every AVD layer.
> Sources: [_meta/sources.md#bcdr-avd], [_meta/sources.md#ha-talking-points] (internal).

## Key framing

**NME is not in the critical path of a user's desktop connection.** Users can still sign in and
use their AVD desktops when NME is down. NME's BCDR value is preventing auto-scale failures and
enabling rapid reprovisioning — not keeping the session-host connection alive.

The real BCDR risk surfaces at: session host availability, FSLogix profile access, and Active
Directory reachability. ([_meta/sources.md#ha-talking-points])

## AVD environment components and DR responsibility

| Component | DR owner | Notes |
|---|---|---|
| AVD Service (connection broker, metadata) | Microsoft | Globally distributed PaaS; fails over automatically; no customer action |
| Nerdio Manager | Customer | Not in user connection path; needs HA/backup for auto-scale and admin functions |
| Active Directory | Customer | Critical — no DC = no user sign-in to domain-joined session hosts |
| Desktop images | Customer | Not user-facing at runtime; critical for reprovisioning new hosts |
| Session host VMs | Customer | Primary delivery vehicle for desktops and apps |
| FSLogix profile storage | Customer | Must be available whenever a user connects; must be replicated |

---

## Situation 1: Local data / resource corruption (no regional or AZ outage)

The Azure region is healthy; something specific broke — corrupted profile, bad image, failed VM.

| Component | Response |
|---|---|
| NME | Enable automated backups; restore from backup if misconfiguration detected |
| Session hosts | Enable NME auto-heal; or delete failed hosts and let NME reprovision |
| FSLogix profiles | Restore corrupted VHD(X) from Azure Backup (Azure Files), ANF snapshots, or Volume Shadow Copies |
| Desktop images | Use NME's built-in image versioning to roll back to a pre-corruption version |
| Active Directory | Maintain multiple DC VMs; restore AD system state from backup if needed |

---

## Situation 2: Single AZ / data-centre failure (within one Azure region)

Most AVD components auto-recover if zone redundancy was configured **before** the outage. This
is an architectural decision — it cannot be fixed reactively during an incident.

| Component | Response if zone redundancy in place | Guidance |
|---|---|---|
| NME App Service | Auto-recovers | Configure zone-redundant App Service plan — [nme-zone-resilience.md](nme-zone-resilience.md) |
| Azure SQL Database | Auto-recovers | Upgrade to Premium tier + enable zone redundancy — [nme-zone-resilience.md](nme-zone-resilience.md) |
| Session hosts | VMs in failed AZ go offline | Enable NME Availability Zones feature so VMs are distributed across AZs at deploy time |
| FSLogix profiles | May be impacted | Use Azure Files **Premium ZRS** in a region that supports AZs for Premium Files; no action needed at outage time if in place |
| Key Vault, Storage, Automation, LAW | Auto-recover | Automatically use ZRS in supported regions |
| App Insights | Partial | Must be workspace-based with dedicated cluster for full zone redundancy |
| Active Directory | Auto-recovers if AZ-deployed | Migrate DC VMs into availability zones if not already |

> **Important:** Not all Azure regions support AZs for all products. Verify AZ support for
> Premium Files storage in the target region before committing to this architecture.

---

## Situation 3: Full Azure region outage

The highest-complexity scenario and the one most customers mean when they say "DR." A full
region failure is rare but requires a pre-built secondary environment. This cannot be improvised
during an outage. ([_meta/sources.md#ha-talking-points])

### Active/passive secondary deployment

| Component | Recommendation |
|---|---|
| NME | Deploy NME Database Resilience + Regional Resilience for the management plane — [nme-database-resilience.md](nme-database-resilience.md), [nme-regional-resilience.md](nme-regional-resilience.md) |
| Session hosts | Pre-stage VMs in secondary region (powered off; faster RTO) or provision on-demand (slower RTO, lower cost). Configure all host pools + auto-scale settings identically; keep auto-scale **OFF** until failover |
| Desktop images | After every primary image update, clone to secondary region. Stale secondary images are a common gap discovered too late |
| FSLogix profiles | Azure Files Premium does **not** support GRS. Use **Azure NetApp Files with cross-region replication**; configure secondary NME instance to point at the ANF volume in the secondary region |
| Active Directory | Deploy DC VMs in secondary region VNet with VNet peering back to primary; required for user sign-in |
| AVD Service | Microsoft-managed; fails over automatically; no customer action |

### Active-active alternative for session hosts

If the customer wants users to survive a region outage without a manual failover runbook, point
them to **Host Pool DR** ([host-pool-dr.md](host-pool-dr.md)), which distributes VMs across two
regions automatically and handles session-host failover without administrator intervention.
([_meta/sources.md#ha-talking-points])

## BCDR is an architecture, not a configuration task

- **NME HA alone is not full BCDR.** Completing NME Regional Resilience protects the management
  layer; it does not protect users' ability to connect if session hosts, AD, or FSLogix storage
  in the primary region become unavailable.
- **A single script does not complete AVD BCDR.** Unlike Regional Resilience (one script), full
  AVD BCDR requires architectural decisions, multi-region infrastructure, networking, and ongoing
  operational processes.
- **Testing is part of BCDR.** An untested DR plan is not a DR plan. Schedule a failover test in
  a maintenance window, validate every component, and document the runbook.

## Effort and timelines (rough)

| Scope | Typical effort |
|---|---|
| Zone resilience for NME (Situation 2) | A day or less |
| NME Database + Regional Resilience | Days (technical work + testing) |
| Full active/passive regional DR (Situation 3) — secondary NME, session hosts, ANF, networking | Multiple weeks; dedicated project |
