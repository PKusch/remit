#!/usr/bin/env python3
"""Legal content decays. Make the decay a build failure rather than a silent liability.

This repo carried pre-Omnibus EU AI Act dates in public for three days after the
regulation moved, and only found out because someone asked it to test itself. Regulatory
summaries have a half-life; the honest response is not to try harder, it is to make
staleness impossible to ignore.

Files carrying legal content declare `verified: YYYY-MM-DD`. Past the threshold, this
fails, and the fix is to re-verify and update the date — not to bump it.
"""
from __future__ import annotations
import argparse, datetime as dt, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Files whose correctness depends on external law or standards.
WATCHED = [
    "skills/eu-ai-act-triage/SKILL.md",
    "skills/eu-ai-act-triage/references/annex-iii.md",
    "skills/eu-ai-act-triage/references/obligations.md",
    "skills/eu-ai-act-triage/references/prohibitions.md",
    "skills/dora-ict-assessment/SKILL.md",
    "skills/dora-ict-assessment/references/articles.md",
    "skills/iso-42001-soa/references/annex-a.md",
    "skills/nist-ai-rmf-assessment/references/functions.md",
    "framework/crosswalk.md",
]
STAMP = re.compile(r"verified[:\s]+(\d{4}-\d{2}-\d{2})", re.I)


def _nonneg_int(v: str) -> int:
    # A negative max-age marks every file stale (age > a negative is always true),
    # which reads like a real result. Refuse it at the argument.
    n = int(v)
    if n < 0:
        raise argparse.ArgumentTypeError(f"cannot be negative, got {n}")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-age-days", type=_nonneg_int, default=90)
    # fromisoformat as the type: a mistyped override is a usage error, not a
    # ValueError traceback from inside main.
    ap.add_argument("--today", type=dt.date.fromisoformat, default=None, help="override for testing, YYYY-MM-DD")
    args = ap.parse_args()
    today = args.today or dt.date.today()

    stale = missing = 0
    for rel in WATCHED:
        p = ROOT / rel
        if not p.exists():
            print(f"  ? {rel} — watched file not found"); missing += 1; continue
        m = STAMP.search(p.read_text(encoding="utf-8"))
        if not m:
            print(f"  ✗ {rel} — no 'verified: YYYY-MM-DD' stamp"); missing += 1; continue
        age = (today - dt.date.fromisoformat(m.group(1))).days
        flag = "✗" if age > args.max_age_days else "✓"
        if age > args.max_age_days:
            stale += 1
        print(f"  {flag} {rel:<52} {age:>4}d")

    print(f"\n{len(WATCHED)} watched · {stale} stale (>{args.max_age_days}d) · {missing} unstamped")
    if stale or missing:
        print("Re-verify against current sources, then update the date. Do not just bump it.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
