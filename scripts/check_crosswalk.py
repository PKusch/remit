#!/usr/bin/env python3
"""Every citation in the crosswalk table must point at something that exists.

The crosswalk claims a NIST subcategory, an EU AI Act article, an ISO Annex A
control or a DORA article does a particular job. Nothing ever checked that the
citation was real, or that the reference material backing it actually exists.
Links get checked (check_links.py); citations of law and standards did not.

What this checks, per column of the "By governance theme" table:
  EU AI Act   — the base article number appears in one of the three
                eu-ai-act-triage reference files.
  NIST AI RMF — the top-level category (GOVERN 2.1 -> GOVERN 2) appears in
                functions.md.
  ISO/IEC     — an Annex A control (A.6) appears in annex-a.md's control
                table. A clause number (cl. 6.1.2) is outside Annex A scope
                and is not checked — annex-a.md deliberately covers only the
                controls, not the management-system clauses.
  DORA        — reported, not checked. There is no DORA reference file in
                this repo, so every DORA citation in the crosswalk currently
                rests on nothing checkable here. That is stated, not hidden.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CROSSWALK = ROOT / "framework" / "crosswalk.md"

EU_AI_ACT_REFS = [
    ROOT / "skills/eu-ai-act-triage/references/obligations.md",
    ROOT / "skills/eu-ai-act-triage/references/annex-iii.md",
    ROOT / "skills/eu-ai-act-triage/references/prohibitions.md",
]
NIST_REF = ROOT / "skills/nist-ai-rmf-assessment/references/functions.md"
ISO_REF = ROOT / "skills/iso-42001-soa/references/annex-a.md"


def base_article(cite: str) -> str:
    """'Art. 26(6)' -> '26', 'Art. 17–23' -> '17' (the first number in a range)."""
    m = re.search(r"\d+", cite)
    return m.group(0) if m else cite


def load_table_rows() -> list[list[str]]:
    text = CROSSWALK.read_text(encoding="utf-8")
    section = text.split("## By governance theme", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-", " "}:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and cells[0] not in ("Theme",):
            rows.append(cells)
    return rows


def main() -> int:
    rows = load_table_rows()
    eu_text = "\n".join(p.read_text(encoding="utf-8") for p in EU_AI_ACT_REFS)
    nist_text = NIST_REF.read_text(encoding="utf-8")
    # Categories are numbered under a "## GOVERN ..." heading, not repeated as
    # "GOVERN 2" inline, so check each function's own section for its number.
    nist_sections = {
        fn: sec
        for fn, sec in re.findall(
            r"## (GOVERN|MAP|MEASURE|MANAGE)[^\n]*\n(.*?)(?=\n## |\Z)", nist_text, re.S
        )
    }
    iso_text = ISO_REF.read_text(encoding="utf-8")

    problems = 0
    dora_citations: set[str] = set()

    for theme, eu, nist, iso, dora in rows:
        for cite in re.findall(r"Art\.\s*\d+", eu):
            art = base_article(cite)
            if not re.search(rf"Art(?:icle|s?\.)\s*(?:\d+,\s*)*{art}\b", eu_text):
                print(f"  ✗ EU AI Act: '{cite}' (theme: {theme}) not found in any eu-ai-act-triage reference")
                problems += 1
        for fn, num in re.findall(r"(GOVERN|MAP|MEASURE|MANAGE)\s*(\d+)", nist):
            section = nist_sections.get(fn, "")
            if not re.search(rf"^\|\s*{num}\s*\|", section, re.M):
                print(f"  ✗ NIST: '{fn} {num}' (theme: {theme}) — category {num} not found under '{fn}' in functions.md")
                problems += 1
        for cite in re.findall(r"A\.\d+\b", iso):
            if not re.search(rf"\|\s*{re.escape(cite)}\s*\|", iso_text):
                print(f"  ✗ ISO: '{cite}' (theme: {theme}) not found in annex-a.md's control table")
                problems += 1
        for cite in re.findall(r"Art\.\s*\d+(?:[–-]\d+)?", dora):
            dora_citations.add(cite)

    print(f"\n{'✗' if problems else '✓'} {problems} unverifiable citation(s) against EU AI Act, NIST and ISO reference material")
    if dora_citations:
        print(
            f"  ⓘ {len(dora_citations)} DORA article(s) cited ({', '.join(sorted(dora_citations))}) — "
            "not checked, because this repo carries no DORA reference file to check them against. "
            "That gap is real; it is not this script pretending otherwise."
        )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
