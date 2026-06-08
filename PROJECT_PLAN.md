# Project Plan — NME Deployment & Security Brain

**Status:** Active · **Created:** 2026-06-08 · **Owner:** nwagner@getnerdio.com

## 1. Purpose

A maintainable, AI-readable knowledge base ("brain") about **Nerdio Manager for Enterprise (NME)**:
how to deploy and install it, how to secure/harden the installation, what permissions are
required to install it, and what permissions NME and its secondary modules use on an ongoing
basis.

Initial scope is **installation + hardening + permissions**. The architecture is designed so the
brain can expand into a **general NME technical knowledge base** without restructuring.

## 2. Architecture Decision (and why)

**Decision: a structured, git-versioned Markdown knowledge base with an AI-readable router
(`INDEX.md`). No database. No semantic/vector search.**

Rationale:
- The corpus is small enough that a frontier model navigates it by reading the router and
  fetching/grepping the right files. Vector search adds chunking, embedding pipelines, ops
  overhead, and staleness — and *shreds* the structure (permission matrices, step-by-step
  procedures) that models reason over best when kept whole.
- **Git is the database**: version history, diffs, blame, branches, PR review for knowledge.
- This is the "LLM Wiki" pattern — current best practice for a corpus of this size and shape.

### When to revisit (explicit triggers)
Add a retrieval/semantic-search layer **on top of the same Markdown files** (no restructure)
only when **all** hold:
1. Corpus grows past index-navigable size (realistically thousands of docs).
2. Consumers submit fuzzy natural-language queries through an interface that cannot browse the
   file tree itself.
3. Measured answer-quality degradation.

A database is reconsidered only for large-scale concurrent multi-author editing or usage
analytics — neither is in scope.

### Consumption / packaging (deferred — does not affect file structure)
All consumers read the *same* Markdown:
- **Claude Code / coding agents** — repo + `INDEX.md`, or packaged as a Claude Skill.
- **Chat product / many users** — exposed via an MCP server.
- **Human browsing** — static site (MkDocs/Docusaurus) over the same files.

`INDEX.md` (not `CLAUDE.md`) is the router by design, to keep the brain platform-agnostic.

## 3. Core Principles

1. **Router-first navigation** — `INDEX.md` maps every file and how they relate; agents select
   precisely instead of loading everything.
2. **Atomicity** — one concept per file.
3. **Single source of truth** — e.g. the permission matrix lives in exactly one file; everything
   else links to it. Prevents contradictory copies (the #1 failure mode of security KBs).
4. **Provenance + freshness** — every fact links to an authoritative source and carries a
   `last_reviewed` date. A stale, uncited permissions answer is worse than none.
5. **Explicit uncertainty** — mark facts vs. assumptions vs. open questions.
6. **Git governance** — knowledge changes go through PRs like code.

## 4. Conventions

### Directory layout
```
knowledge/
  installation/   prerequisites, deployment models, step-by-step, validation
  permissions/    permission-matrix (SSOT), install-time, runtime-core, per-module
  hardening/      checklist (index), identity/rbac, network, secrets/keyvault
  architecture/   nme-components (the moving parts)
  modules/        <secondary-module>/...  (expansion slot)
_meta/
  sources.md      provenance ledger → official Nerdio / Microsoft Learn docs
  glossary.md     canonical term definitions
  contributing.md how to add/update a fact (governance rules)
  _frontmatter-template.md   copy-paste schema for new pages
```

### Required YAML frontmatter (every knowledge page)
```yaml
---
id: kebab-case-id          # unique; matches filename
title: Human Readable Title
domain: installation|permissions|hardening|architecture|modules
applies_to: "NME 6.x"      # version scoping — critical for security accuracy
last_reviewed: YYYY-MM-DD
status: stub|draft|reviewed
sources: [_meta/sources.md#anchor]
related: [other-id, another-id]
---
```

### Authoring rules
- New page MUST be linked from `INDEX.md` and from at least one related page.
- Cite sources for every non-trivial fact; record the URL in `_meta/sources.md`.
- Keep procedural steps and tables intact — do not fragment a table across pages.
- Use relative Markdown links for cross-references.

## 5. Roadmap

- [x] **Phase 0 — Scaffold**: structure, router, governance (`AGENTS.md`, CODEOWNERS, PR template,
      `scripts/validate.py` + CI), stubs.
- [x] **Phase 1 — Permissions**: `permission-matrix.md` (SSOT, all 6 app registrations + Azure
      RBAC), install-time, runtime-core — seeded from the API-permissions workbook + Azure
      Permissions doc. *(status: draft — pending NME 8.0 release-note verification.)*
- [x] **Phase 2 — Installation**: prerequisites, deployment models, step-by-step, validation.
- [x] **Phase 3 — Hardening**: checklist, identity/RBAC (incl. MFA), network isolation (+ the
      Enable Private Endpoints runbook documented from the actual script: params, resources, VNet/
      DNS/peering, architecture), secrets/Key Vault, component pages (App Service, SQL, Key Vault,
      Storage Account), and Entra ID SQL authentication. *Remaining: CIS images/Intune policies
      (source article not yet ingested).*
- [~] **Phase 4 — Modules**: done — User Cost Attribution, Intune Insights, Real-Time Insights
      (deployment/security footprint + permissions; RTI managed identities added to the matrix).
      *Remaining: REST API, UEM/Intune, Windows 365, Copilot pages if needed.*
- [ ] **Phase 5 — Packaging**: ship as a Claude Skill; evaluate MCP exposure.
- [ ] **Phase 6 — Governance cadence**: define review interval; verify all `draft` → `reviewed`
      against NME 8.0; resolve open questions on each page.

**Baseline version:** NME 8.0. Sources ingested were dated late-2025/early-2026 (version notes
through ~v7.4); 8.0-specific deltas are tracked as open questions per page.

## 5a. Ingestion staging area
Raw source documents live in [ingest/](ingest/) ("capture first, process later"). They are the
provenance for Phase 1–3 content and are catalogued in [_meta/sources.md](_meta/sources.md). Leave
them in place; processed knowledge belongs in `knowledge/`.

## 6. Open Questions
- Which NME version(s) is the brain authoritative for at launch? (sets `applies_to` baseline)
- Full list of secondary modules in scope for Phase 4.
- Are there internal (non-public) deployment/hardening sources to incorporate alongside docs?
