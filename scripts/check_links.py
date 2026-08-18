#!/usr/bin/env python3
"""Every relative markdown link in the repo must resolve.

Added after moving three directories under evidence/ silently broke a dozen links: a
bulk find-and-replace fixed the link *text* and left the *targets* pointing at paths
that no longer existed. Nothing complained, because nothing was checking.

A repo that gates its own numbers should gate its own links.
"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
bad = 0

for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for target in LINK.findall(md.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        path = (md.parent / target.split("#")[0]).resolve()
        if not path.exists():
            print(f"  ✗ {md.relative_to(ROOT)} → {target}")
            bad += 1

print(f"\n{'✗' if bad else '✓'} {bad} broken link(s)")
sys.exit(1 if bad else 0)
