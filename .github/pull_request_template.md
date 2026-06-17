<!-- Knowledge change PR. See AGENTS.md (agents) and _meta/contributing.md (humans). -->

## What changed
<!-- One or two sentences. Which pages/domains? -->

## Sources
<!-- Link the authoritative source(s) for new/changed facts. Confirm they're in _meta/sources.md. -->

## Provenance & confidence
<!-- See the Confidence policy in _meta/sources.md: authoritative > corroborated > reported. -->
- [ ] Every new source in `_meta/sources.md` declares a **`Confidence:`** tier (or is an official doc/artifact → authoritative)
- [ ] Any fact from a **verbal/SME** contribution either cites a corroborating document (`corroborated`) or is tagged **`reported`** and listed below
- [ ] Version-specific sources (deployment artifacts) declare an **`Applies_to:`** release line, and artifact-derived facts are **scoped to that release** on the page (with a re-verify note for newer versions)

### ⚠️ Verbal / uncorroborated contributions (flag for reviewer)
<!-- List any facts that came from a person without a supporting document. Name the SME, the claim,
     and whether a corroborating doc was requested. Leave "None" if not applicable. The reviewer
     should scrutinize these before merge. -->
None.

## Definition of done
- [ ] One concept per file; no procedure/table fragmented across files
- [ ] Specific permissions/roles live only in `permission-matrix.md` (linked, not restated)
- [ ] Frontmatter complete; `last_reviewed` bumped; `status` accurate; `applies_to` set
- [ ] Every non-trivial fact is cited; sources recorded in `_meta/sources.md`
- [ ] **New/re-pulled sources record an `Ingested:` date** (and re-ingests bump it + re-verify pages that cite them)
- [ ] Page linked from `INDEX.md` and at least one related page
- [ ] `python3 scripts/validate.py` passes
- [ ] Uncertainty/assumptions flagged explicitly (not stated as fact)

## Notes for reviewer
<!-- Anything unverified, any open questions, anything you want a second opinion on. -->
