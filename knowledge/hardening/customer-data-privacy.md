---
id: customer-data-privacy
title: Customer Data & Nerdio Licensing Telemetry
domain: hardening
applies_to: "NME 5.1+"
last_reviewed: 2026-06-15
status: reviewed
sources: [_meta/sources.md#customer-data-privacy]
related: [hardening-checklist, firewall-requirements, secrets-keyvault]
---

# Customer Data & Nerdio Licensing Telemetry

> What NME collects from your environment (nothing), what it reports to Nerdio's licensing system,
> and how to opt out. Source: [_meta/sources.md#customer-data-privacy].

## Core position

Nerdio Manager does not collect customer data. It is an Azure application deployed inside the
customer's own Azure subscription, operating via a service principal that makes Graph and Azure API
calls only to execute tasks the customer initiates. Nerdio staff have no access to a customer's
installation unless the customer explicitly grants it.

NME does report **usage/licensing telemetry** to Nerdio's licensing system on a periodic basis.
This telemetry contains no PII from the customer's end-user population — it is operational and
licensing metadata about the NME deployment itself (counts, versions, feature flags).

## What IS reported to Nerdio

Data is transmitted via HTTPS (encrypted in transit) and stored in an Azure SQL database in
Azure's **North Central US** region, encrypted at rest. ([_meta/sources.md#customer-data-privacy])

**Registration / installation metadata**
- License registration info provided at install: first name, last name, company, phone, email,
  Azure tenant & subscription ID, tenant name and domain
- Date/time of first installation; initial version installed
- Current NME version; email of last user to update the install

**Usage / licensing counts**
- Number of named users and concurrent users
- Number of CPU cores consumed by AVD session hosts
- Number of AVD Workspaces, ARM Host Pools, ARM session hosts
- Number of AVD tenants, tenant host pools, tenant session hosts
- Email address and datetime stamp of the last person to sign in to NME
- Whether Sepago is enabled

**Host pool detail**
- AVD Workspace names and IDs
- Host pool names, IDs, CPU core counts
- Desktop user count per host pool
- Monthly active user count (current month and past 30 days) per host pool
- Session count per host pool
- VM size, disk size, average/max host count last hour, average/max running VMs last hour,
  compute cost, storage cost per host pool

**Feature flags**
- Enablement status of all features within NME

> **Note (v5.1+):** Starting with NME v5.1, feature usage is additionally reported to the
> licensing system. This data contains no PII and is used to improve the product. Opt-out is
> available by contacting Nerdio support.

## What is NOT reported

No content from your Azure environment is sent to Nerdio: no user profile data, no session
recordings, no VM disk or file share contents, no Entra ID user/group objects, and no
customer-managed secrets.

## Opt-out

Contact Nerdio support to opt out of the v5.1+ feature usage reporting.

## Veracode verification

Nerdio Manager is **Veracode Verified Standard**.

## Related

The firewall rule that carries this telemetry — `nwp-web-app.azurewebsites.net:443` — is
documented in [firewall-requirements.md](firewall-requirements.md) (labeled "Nerdio licensing
servers"). All telemetry data stays within NME's own Azure resources in the customer's tenant;
only the licensing payload above leaves the tenant.
