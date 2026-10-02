#!/usr/bin/env python3
"""Every number the README quotes from a harness must match what that harness prints.

The previous version of this check grepped for two magic strings — "16/16" and "4%" —
and passed. Meanwhile the line directly beneath the first one said `spurious findings: 2`
while the zoo printed `3`. A repository whose entire pitch is catching its own overclaims
was overclaiming, behind a gate that only looked at the numbers it already trusted.

That was found by an outside reader in about ninety seconds. This runs the harnesses and
compares every extracted figure, so the class of error is closed rather than the instance.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd: list[str]) -> str:
    return subprocess.run([sys.executable, *cmd], cwd=ROOT, capture_output=True,
                          text=True, timeout=600).stdout


def main() -> int:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    zoo = run(["evidence/zoo/run.py", "--no-colour"])
    adv = run(["evidence/adversary/run.py", "--no-colour"])

    # (label, harness output, regex, what to look for in the README from the match).
    # Each figure MUST be found in the harness output: a regex that no longer matches
    # means the harness changed its wording and this figure is no longer being gated.
    # Skipping it silently is the exact overclaim-behind-a-trusted-gate this script
    # exists to prevent, so a missing match is a failure, not a quietly dropped check.
    specs = [
        ("zoo recall", zoo, r"recall on detectable classes\s*:\s*(\d+/\d+)",
         lambda m: m.group(1)),
        ("zoo spurious findings", zoo, r"spurious findings\s*:\s*(\d+)",
         lambda m: f"spurious findings            : {m.group(1)}"),
        ("zoo deferred", zoo, r"deferred to human\s*:\s*(\d+)",
         lambda m: f"deferred to human            : {m.group(1)}"),
        ("adversary evaded", adv, r"(\d+)/(\d+) tactics did the damage",
         lambda m: f"{m.group(1)}/{m.group(2)} tactics"),
    ]

    bad = 0
    for label, src, pattern, needle_of in specs:
        m = re.search(pattern, src)
        if m is None:
            print(f"  ✗ {label:<26} the harness no longer prints this figure (output changed)")
            bad += 1
            continue
        needle = needle_of(m)
        ok = needle in readme
        print(f"  {'✓' if ok else '✗'} {label:<26} code says {needle!r}")
        if not ok:
            print(f"      README does not contain: {needle!r}")
            bad += 1

    print(f"\n{'✗' if bad else '✓'} {len(specs)} figure(s) checked · {bad} stale or missing")
    if bad:
        print("Update the README to what the code prints. Do not update the code to the README.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
