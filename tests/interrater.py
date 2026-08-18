#!/usr/bin/env python3
"""Measure whether independent assessors, given the criteria, agree.

    python tests/interrater.py <ratings-dir>

The diagnostic manual's entire justification is inter-rater reliability: the claim that
operationalised criteria let two people looking at the same evidence reach the same
classification. That claim was asserted from the first line the manual ever had and never
tested, because testing it needs assessors who did not write it.

This scores a blind panel. Each rater receives the manual and eight traces with ground
truth withheld, and returns a primary classification per trace. From that:

  agreement   — mean pairwise agreement on the primary code, the number a practitioner
                actually cares about ("will my colleague call this what I called it?")
  kappa       — Fleiss' kappa, which corrects for agreement that would occur by chance.
                Reported because raw agreement flatters any scheme with few categories.
  accuracy    — agreement with ground truth, where ground truth exists

Landis & Koch's conventional bands for kappa: <0 poor, 0–.20 slight, .21–.40 fair,
.41–.60 moderate, .61–.80 substantial, .81–1 almost perfect. Clinical instruments are
usually expected to clear .60. That is the bar this should be held to, and the number is
printed whether or not it clears it.

This scorer was written before any ratings were read. If it had been written afterwards
it would be worth much less.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


def fleiss_kappa(table: list[Counter], n_raters: int) -> float:
    """table: one Counter of category->count per item. Standard Fleiss formulation."""
    N = len(table)
    if N == 0 or n_raters < 2:
        return float("nan")
    cats = sorted({c for row in table for c in row})
    # P_i: agreement among rater pairs within item i
    P = []
    for row in table:
        s = sum(row.get(c, 0) ** 2 for c in cats)
        P.append((s - n_raters) / (n_raters * (n_raters - 1)))
    P_bar = sum(P) / N
    # P_e: agreement expected by chance from marginal category frequencies
    p_j = [sum(row.get(c, 0) for row in table) / (N * n_raters) for c in cats]
    P_e = sum(p ** 2 for p in p_j)
    if abs(1 - P_e) < 1e-12:
        return float("nan")
    return (P_bar - P_e) / (1 - P_e)


def band(k: float) -> str:
    if k != k:
        return "undefined"
    for lo, name in [(.81, "almost perfect"), (.61, "substantial"), (.41, "moderate"),
                     (.21, "fair"), (0, "slight")]:
        if k >= lo:
            return name
    return "poor"


def main() -> int:
    d = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    ratings = {}
    for f in sorted(d.glob("rater_*.json")):
        ratings[f.stem] = json.loads(f.read_text())
    if len(ratings) < 2:
        print("need at least 2 rater files (rater_*.json)")
        return 1

    truth_f = d / "truth.json"
    truth = json.loads(truth_f.read_text()) if truth_f.exists() else {}

    items = sorted({k for r in ratings.values() for k in r})
    raters = sorted(ratings)

    print(f"\n\033[1mINTER-RATER RELIABILITY\033[0m")
    print(f"\033[2m{len(raters)} independent raters · {len(items)} traces · ground truth "
          f"withheld from all of them\033[0m\n")

    # per item
    table = []
    agree_pairs = tot_pairs = 0
    print(f"  {'trace':<7}{'primary codes given':<44}{'agree':>7}  truth")
    for it in items:
        got = [str(ratings[r].get(it, {}).get("primary", "?")
                   if isinstance(ratings[r].get(it), dict) else ratings[r].get(it, "?"))
               for r in raters]
        c = Counter(got)
        table.append(c)
        a = sum(1 for x, y in combinations(got, 2) if x == y)
        t = len(got) * (len(got) - 1) // 2
        agree_pairs += a
        tot_pairs += t
        shown = " ".join(f"{k}×{v}" if v > 1 else k for k, v in c.most_common())
        print(f"  {it:<7}{shown:<44}{a}/{t:>5}  {truth.get(it,'—')}")

    raw = agree_pairs / tot_pairs if tot_pairs else 0
    k = fleiss_kappa(table, len(raters))

    print(f"\n\033[1mRESULT\033[0m")
    print(f"  mean pairwise agreement   {raw*100:>5.1f}%")
    print(f"  Fleiss' kappa             {k:>5.2f}   \033[1m{band(k)}\033[0m")
    print(f"  \033[2mconventional bar for a usable instrument: kappa ≥ 0.61\033[0m")

    if truth:
        hits = tot = 0
        for it in items:
            gt = truth.get(it)
            if not gt:
                continue
            for r in raters:
                v = ratings[r].get(it)
                p = v.get("primary") if isinstance(v, dict) else v
                tot += 1
                hits += 1 if p and p in gt else 0
        if tot:
            print(f"  accuracy vs ground truth  {100*hits/tot:>5.1f}%   ({hits}/{tot} "
                  f"rater-judgements)")

    # where the disagreement lives — the actionable part
    contested = [(it, table[i]) for i, it in enumerate(items) if len(table[i]) > 1]
    if contested:
        print(f"\n\033[1mContested traces\033[0m  \033[2mthe entries whose criteria are "
              f"not discriminating\033[0m")
        for it, c in contested:
            print(f"  {it}: {dict(c)}  \033[2mtruth {truth.get(it,'—')}\033[0m")
    else:
        print(f"\n  \033[2mno contested traces — every rater agreed on every item\033[0m")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
