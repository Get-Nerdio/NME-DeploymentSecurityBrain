# Contributing to the Brain

How to add or update knowledge. These rules keep the brain accurate, navigable, and trustworthy.
They apply to both human SEs and AI agents. (Agents also follow the workflow contract in
[../AGENTS.md](../AGENTS.md), which points back here for the rules.)

## Update workflow (humans)
1. Branch off `main`: `git switch -c knowledge/<short-topic>`. Never commit knowledge to `main`.
2. Edit the right `knowledge/<domain>/` file, or copy
   [_frontmatter-template.md](_frontmatter-template.md) to start a new page.
3. Follow the rules below (sourcing, single source of truth, freshness).
4. Validate locally: `python3 scripts/validate.py` — fix every error.
5. Push and open a Pull Request using the template. CI runs the validator automatically.
6. A reviewer (see `.github/CODEOWNERS`) approves and merges. Don't merge your own knowledge
   changes to permissions/hardening without a second set of eyes.

To **propose a correction** without writing the fix, open an issue (or a PR that just adds an
`> **Open question:**` note to the relevant page) — flagging a problem is a valid contribution.

## Adding a page
1. Copy [_frontmatter-template.md](_frontmatter-template.md). Set a unique `id` matching the filename.
2. Place it in the correct `knowledge/<domain>/` directory (one concept per file — atomic).
3. Fill all frontmatter. `applies_to` must state the NME version(s) the facts hold for.
4. Link the new page from [../INDEX.md](../INDEX.md) **and** from at least one related page.

## Sourcing & accuracy (non-negotiable for security/permissions content)
- Cite a source for every non-trivial fact. Record the URL in [sources.md](sources.md) and
  reference its anchor in the page's `sources:` frontmatter.
- Prefer official Nerdio and Microsoft Learn documentation.
- Mark uncertainty explicitly: separate **facts** from **assumptions** and **open questions**.
- A stale, uncited permissions/hardening answer is worse than none.

## Single source of truth
- Specific permissions/roles live **only** in
  [../knowledge/permissions/permission-matrix.md](../knowledge/permissions/permission-matrix.md).
  Other pages link to it; they do not restate rows.
- Do not fragment a procedure or table across multiple files.

## Freshness
- Update `last_reviewed` whenever you verify or change a page.
- Set `status`: `stub` (placeholder) → `draft` (content, unverified) → `reviewed` (verified against source).

## Change workflow
- Knowledge changes go through Git like code (branch + PR + review). Git is the version store.
