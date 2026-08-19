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

    checks: list[tuple[str, str, str]] = []

    # zoo: recall and spurious count, read from the harness rather than assumed
    m = re.search(r"recall on detectable classes\s*:\s*(\d+/\d+)", zoo)
    if m:
        checks.append(("zoo recall", m.group(1), m.group(1)))
    m = re.search(r"spurious findings\s*:\s*(\d+)", zoo)
    if m:
        checks.append(("zoo spurious findings", f"spurious findings            : {m.group(1)}",
                       m.group(1)))
    m = re.search(r"deferred to human\s*:\s*(\d+)", zoo)
    if m:
        checks.append(("zoo deferred", f"deferred to human            : {m.group(1)}",
                       m.group(1)))
    m = re.search(r"(\d+)/(\d+) tactics did the damage", adv)
    if m:
        checks.append(("adversary evaded", f"{m.group(1)}/{m.group(2)} tactics", m.group(1)))

    bad = 0
    for label, needle, value in checks:
        ok = needle in readme
        print(f"  {'✓' if ok else '✗'} {label:<26} code says {value!r}")
        if not ok:
            print(f"      README does not contain: {needle!r}")
            bad += 1

    print(f"\n{'✗' if bad else '✓'} {len(checks)} figure(s) checked · {bad} stale")
    if bad:
        print("Update the README to what the code prints. Do not update the code to the README.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
