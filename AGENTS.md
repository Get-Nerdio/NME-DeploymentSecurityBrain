# AGENTS.md — Operating Contract for AI Agents

**If you are an AI agent (Claude or otherwise) asked to add, correct, or update knowledge in
this repository, follow this contract.** It is intentionally platform-agnostic (works for any
agent). The canonical *content* rules live in [_meta/contributing.md](_meta/contributing.md);
this file is the *workflow* you must execute.

## Your job
Maintain an accurate, sourced, navigable knowledge base about NME. You are a librarian, not just
a writer: every change must keep the brain internally consistent and verifiable.

## Golden rules (do not violate)
1. **Source everything.** Every non-trivial fact cites an entry in [_meta/sources.md](_meta/sources.md).
   Prefer official Nerdio and Microsoft Learn docs. If you cannot source it, mark it under an
   **Open questions / Assumptions** heading — do not present it as fact.
2. **Single source of truth.** Specific permissions/roles live ONLY in
   [knowledge/permissions/permission-matrix.md](knowledge/permissions/permission-matrix.md).
   Link to it; never restate rows elsewhere.
3. **Atomic.** One concept per file. Don't fragment a procedure or table across files.
4. **Don't restructure or change the architecture** (no database, no vector search, no moved
   directories) unless a human explicitly asks. See [PROJECT_PLAN.md](PROJECT_PLAN.md).
5. **Preserve sourced facts.** Don't delete a cited fact silently; if it's now wrong, update it
   and note the change, or raise it in the PR.

## Update workflow (execute every time)
1. **Never commit to `main`.** Create a branch: `knowledge/<short-topic>`.
2. Make the change in the correct `knowledge/<domain>/` file (or copy
   [_meta/_frontmatter-template.md](_meta/_frontmatter-template.md) for a new page).
3. Update frontmatter: bump `last_reviewed` to today, set `status`
   (`stub`→`draft`→`reviewed`), list `sources` and `related`.
4. **Record provenance.** Add each new/re-pulled doc to [_meta/sources.md](_meta/sources.md) with
   an `<a id="...">` anchor, its origin (Help Center title/URL), the article's own *Dated/Last
   modified* value, and an **`Ingested:` date** (today, when you pulled it). The validator
   **requires** an `Ingested:` date on every anchored entry. If you re-pulled an existing doc,
   **bump its `Ingested:` date** and re-verify (and bump `last_reviewed` on) every page whose
   `sources:` cite that anchor.
5. Ensure the page is linked from [INDEX.md](INDEX.md) **and** at least one related page.
6. **Validate:** run `python3 scripts/validate.py` and fix every error before proceeding.
7. **Open a Pull Request** using the template. Summarize what changed and cite sources.
8. **Do not self-merge.** A human SE (see `.github/CODEOWNERS`) reviews and merges. If you lack
   permission to open a PR, leave the branch and tell the user exactly what you changed.

## When unsure
State the uncertainty explicitly in the PR and in the page (Assumptions / Open questions). A
flagged gap is a contribution; a confident wrong answer about permissions or hardening is a
liability.
