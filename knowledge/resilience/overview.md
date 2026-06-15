---
id: resilience-overview
title: Resilience & BCDR — Orientation
domain: resilience
applies_to: "NME 8.0"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#bcdr-avd, _meta/sources.md#nme-ha-dr-webapp, _meta/sources.md#ha-talking-points]
related: [nme-backup-restore, nme-zone-resilience, nme-database-resilience, nme-regional-resilience, host-pool-dr, avd-bcdr-guidance]
---

# Resilience & BCDR — Orientation

> Two independent protection tracks: NME control-plane HA and session-host BCDR. Read this page
> first to understand which track (or combination) a question belongs to.
> Sources: [_meta/sources.md#bcdr-avd], [_meta/sources.md#nme-ha-dr-webapp].

## The two independent tracks

| Track | What it protects | NME feature |
|---|---|---|
| **NME control-plane HA** | The web app and database that *run* Nerdio Manager | Backup/restore, zone resilience, Database Resilience, Regional Resilience |
| **Session-host / AVD BCDR** | The VMs users actually connect to for desktops and apps | Host Pool Disaster Recovery; broader AVD BCDR architecture |

These are entirely separate concerns. **NME is not in the critical path of a user's desktop
connection.** Users can still sign in and use their desktops when NME is down; only NME-driven
auto-scale and scripted actions fail. ([_meta/sources.md#bcdr-avd])

Both tracks are needed for comprehensive resilience. Neither replaces the other.

## NME control-plane protection layers

The layers below are additive. Each gives incrementally broader protection.
Layers 3 and 4 require **Nerdio Manager Premium edition**.

| Layer | Protection scope | Premium? | Page |
|---|---|---|---|
| **1. Backup & restore** | Recovery from data corruption / misconfiguration | No | [nme-backup-restore.md](nme-backup-restore.md) |
| **2. Zone resilience** | Single AZ / data-centre failure within one region | No | [nme-zone-resilience.md](nme-zone-resilience.md) |
| **3. Database Resilience** | Azure SQL cross-region replication + failover | Yes | [nme-database-resilience.md](nme-database-resilience.md) |
| **4. Regional Resilience** | Full multi-region web-app HA (requires layer 3) | Yes | [nme-regional-resilience.md](nme-regional-resilience.md) |

> **HA vs DR distinction (from the KB):** As of NME v6.5, HA is supported for the web-app layer
> only. The SQL database layer uses auto-failover groups, which are DR in nature (active/passive)
> — brief outages should be expected and planned for during SQL failover.
> ([_meta/sources.md#nme-ha-dr-webapp])

## Session-host protection

| Feature | Pattern | Page |
|---|---|---|
| **Host Pool DR** | Active-active: VMs split 50/50 across two regions; FSLogix Cloud Cache replication; automatic failover | [host-pool-dr.md](host-pool-dr.md) |
| **Full AVD BCDR** | Architecture-level guidance across three outage scenarios (local corruption, AZ failure, full region outage) | [avd-bcdr-guidance.md](avd-bcdr-guidance.md) |

## Quick scope guide

| Customer says… | Likely answer |
|---|---|
| "NME is down, what do we do?" | Restore from backup or invoke DR; session hosts are unaffected |
| "Users can't connect to their desktops" | Session-host or AD issue, not NME HA |
| "We need RTO < 1 hour for NME" | Database Resilience (Microsoft Managed auto-failover) + Regional Resilience |
| "We need users to survive a full region outage" | Full AVD BCDR: secondary region, Host Pool DR or active/passive session hosts, ANF cross-region replication |
| "HA is done — are we fully protected?" | Only the management plane is. Session hosts, FSLogix profiles, and AD still need protection |
