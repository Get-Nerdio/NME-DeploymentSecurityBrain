# NME Deployment & Security Brain

An AI-readable knowledge base about **Nerdio Manager for Enterprise (NME)**: how to deploy and
install it, how to secure/harden the installation, and what permissions are required to install
it and used by NME and its secondary modules on an ongoing basis.

It is a structured, git-versioned Markdown knowledge base with an AI-readable router. No
database, no semantic search — by design (see [PROJECT_PLAN.md](PROJECT_PLAN.md)).

## Start here
- **[INDEX.md](INDEX.md)** — the router. Read it first to navigate the knowledge.
- **[PROJECT_PLAN.md](PROJECT_PLAN.md)** — scope, architecture decision, conventions, roadmap.
- **[_meta/contributing.md](_meta/contributing.md)** — how to add/update knowledge.

## Layout
```
INDEX.md            Router (read first)
PROJECT_PLAN.md     Architecture & roadmap
knowledge/          The knowledge, by domain (installation / permissions / hardening / architecture / modules)
_meta/              Sources ledger, glossary, contributing rules, frontmatter template
```

Scope today is installation + hardening + permissions; the architecture is built to expand into
a general NME technical brain without restructuring.
