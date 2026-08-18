#!/usr/bin/env python3
"""Run the zoo: release every specimen, point the detector at it, score the result.

    python zoo/run.py               # score the detector against ground truth
    python zoo/run.py --save        # also write traces to zoo/traces/
    python zoo/run.py --show A2     # print one specimen's trace and findings

Ground truth is declared by construction — each specimen is *built* to exhibit its mode —
so this is a genuine test rather than a self-graded one. What it measures is whether the
diagnostic manual's criteria are operational enough to be implemented, and whether an
implementation of them recovers the label.

Three classes (G1, P1, R1) are deliberately unreachable from a trace. They are reported
separately rather than counted as misses, because "this needs a human" is the correct
answer for them and a detector that pretended otherwise would be the more dangerous tool.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import specimens                                     # noqa: E402
from harness.detect import analyse, NEEDS_HUMAN      # noqa: E402

BOLD, DIM, OK, BAD, WARN, END = "\033[1m", "\033[2m", "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", action="store_true", help="write traces to zoo/traces/")
    ap.add_argument("--show", metavar="CODE", help="print one specimen's trace in full")
    ap.add_argument("--no-colour", action="store_true")
    args = ap.parse_args()

    if args.no_colour:
        globals().update(BOLD="", DIM="", OK="", BAD="", WARN="", END="")

    cases = [fn() for fn in specimens.ALL]

    if args.show:
        case = next((c for c in cases if c.code == args.show), None)
        if not case:
            print(f"no specimen with code {args.show}")
            return 1
        print(f"{BOLD}{case.code} · {case.name}{END}\n")
        print(case.world.to_jsonl())
        print(f"\n{BOLD}Findings{END}")
        for f in analyse([e.prune() for e in case.world.events]).findings:
            print(f"  {f.code:<12} [{f.criteria}] {f.evidence}")
        print(f"\n{DIM}{case.note}{END}")
        return 0

    caught = missed = spurious = 0
    human_only: list = []
    rows = []

    for case in cases:
        trace = [e.prune() for e in case.world.events]
        if args.save:
            case.world.save(Path(__file__).parent / "traces" / f"{case.name}.jsonl")

        rep = analyse(trace)
        found = set(rep.codes)

        if not case.detectable:
            human_only.append(case)
            continue

        hit = case.code in found
        caught += hit
        missed += not hit
        # Contributing codes the specimen genuinely has are not spurious.
        legit = {case.code, *case.contributing}
        extra = sorted(found - legit)
        spurious += len(extra)
        rows.append((case, hit, rep, extra))

    print(f"\n{BOLD}THE BROKEN AGENT ZOO{END}")
    print(f"{DIM}{len(cases)} specimens · {len(rows)} machine-detectable · "
          f"{len(human_only)} require human judgement{END}\n")

    for case, hit, rep, extra in rows:
        mark = f"{OK}✓{END}" if hit else f"{BAD}✗{END}"
        print(f"{mark} {BOLD}{case.code:<12}{END} {case.name}")
        for f in rep.findings:
            is_truth = f.code == case.code
            tag = f"{OK}●{END}" if is_truth else (
                f"{DIM}○{END}" if f.code in case.contributing else f"{WARN}▲{END}")
            print(f"     {tag} {f.code:<12} {DIM}[{f.criteria}]{END} {f.evidence}")
        if not rep.findings:
            print(f"     {BAD}nothing detected{END}")
        if extra:
            print(f"     {WARN}unexpected: {', '.join(extra)}{END}")
        print()

    print(f"{BOLD}Requires human judgement — correctly not attempted{END}")
    for case in human_only:
        print(f"  {DIM}—{END} {case.code:<12} {case.name}")
        print(f"       {DIM}{NEEDS_HUMAN.get(case.code, case.note)}{END}")

    total = caught + missed
    pct = 100 * caught / total if total else 0
    print(f"\n{BOLD}SCORE{END}")
    print(f"  recall on detectable classes : {caught}/{total}  ({pct:.0f}%)")
    print(f"  spurious findings            : {spurious}")
    print(f"  deferred to human            : {len(human_only)}")
    print(f"\n{DIM}● ground truth   ○ genuine contributing   ▲ unexpected{END}")

    if missed:
        print(f"\n{BAD}{missed} specimen(s) not detected — either the detector is wrong "
              f"or the criteria are not operational. Both are findings.{END}")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
