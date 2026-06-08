#!/usr/bin/env python3
"""Validate the NME brain's structural rules. Zero dependencies (stdlib only).

Checks every knowledge page for:
  - required YAML frontmatter keys + valid enums
  - id matching the filename
  - the page being linked from INDEX.md
  - referenced source anchors existing in _meta/sources.md

Exit code 0 = clean, 1 = errors. Run: python3 scripts/validate.py
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "knowledge"
INDEX = ROOT / "INDEX.md"
SOURCES = ROOT / "_meta" / "sources.md"

REQUIRED_KEYS = {"id", "title", "domain", "applies_to", "last_reviewed", "status"}
VALID_DOMAINS = {"installation", "permissions", "hardening", "architecture", "modules"}
VALID_STATUS = {"stub", "draft", "reviewed"}

# Pages that are navigational, not knowledge pages, and so are exempt from frontmatter rules.
EXEMPT = {"README.md"}

# Structural filenames that may carry an id different from the filename stem (e.g. one per
# module subdirectory). `id` must still be globally unique.
STRUCTURAL_NAMES = {"overview.md"}


def parse_frontmatter(text: str) -> dict | None:
    """Return a flat dict of the leading YAML frontmatter block, or None if absent."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    data: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("-"):
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()
    return data


def main() -> int:
    errors: list[str] = []
    index_text = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    sources_text = SOURCES.read_text(encoding="utf-8") if SOURCES.exists() else ""
    source_anchors = set(re.findall(r'<a id="([^"]+)">', sources_text))

    pages = sorted(KNOWLEDGE.rglob("*.md"))
    if not pages:
        errors.append("No knowledge pages found under knowledge/.")

    seen_ids: dict[str, str] = {}
    for page in pages:
        rel = page.relative_to(ROOT).as_posix()
        if page.name in EXEMPT:
            continue
        text = page.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter block.")
            continue

        missing = REQUIRED_KEYS - fm.keys()
        if missing:
            errors.append(f"{rel}: missing frontmatter keys: {', '.join(sorted(missing))}")

        page_id = fm.get("id")
        if page_id:
            if page_id in seen_ids:
                errors.append(f"{rel}: duplicate id '{page_id}' (also in {seen_ids[page_id]}).")
            seen_ids[page_id] = rel
            if page.name not in STRUCTURAL_NAMES and page_id != page.stem:
                errors.append(f"{rel}: id '{page_id}' does not match filename '{page.stem}'.")

        if fm.get("domain") and fm["domain"] not in VALID_DOMAINS:
            errors.append(f"{rel}: invalid domain '{fm['domain']}'.")

        if fm.get("status") and fm["status"] not in VALID_STATUS:
            errors.append(f"{rel}: invalid status '{fm['status']}'.")

        if rel not in index_text:
            errors.append(f"{rel}: not linked from INDEX.md.")

        # Validate any referenced source anchors (e.g. _meta/sources.md#graph-permissions).
        for anchor in re.findall(r"_meta/sources\.md#([A-Za-z0-9_-]+)", text):
            if anchor not in source_anchors:
                errors.append(f"{rel}: references unknown source anchor '#{anchor}'.")

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"OK: {len(pages)} knowledge page(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
