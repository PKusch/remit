#!/usr/bin/env python3
"""Run episodes under pressure, classify what emerged, aggregate.

    python disorder/run.py                    # the standard sweep
    python disorder/run.py -n 400             # episodes per condition
    python disorder/run.py --replay 8821      # one episode, full trace
    python disorder/run.py --json out.json    # machine-readable

An episode is a pure function of (seed, agent, pressure). Nothing is scripted: the agents
are reasonable, the world is hostile, and every classification below is a failure mode that
*arose* rather than one that was planted.

Classification uses the zoo's detector unchanged. A classifier built against scripted
specimens, pointed at unscripted behaviour, is the only way to find out whether the
diagnostic manual describes anything real.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "zoo"))

from hostile import Pressure, PRESSURES          # noqa: E402
from agents import AGENTS                        # noqa: E402
from harness.detect import analyse               # noqa: E402

BOLD, DIM, END = "\033[1m", "\033[2m", "\033[0m"

# One dial at a time, then everything at once. Isolating pressures is what lets you say
# "this mode is caused by that condition" rather than "chaos produces chaos".
CONDITIONS = [
    ("calm",       Pressure()),
    ("flaky",      Pressure(flaky=0.35)),
    ("liar",       Pressure(liar=0.55)),
    ("drift",      Pressure(drift=0.45)),
    ("truncate",   Pressure(truncate=0.6)),
    ("inject",     Pressure(inject=0.3)),
    ("contention", Pressure(contention=0.4)),
    ("storm",      Pressure(flaky=0.25, liar=0.4, drift=0.3,
                            truncate=0.4, inject=0.2, contention=0.3)),
]


def episode(agent: str, seed: int, pressure: Pressure):
    w = AGENTS[agent](seed, pressure)
    tr = w.trace()
    return tr, analyse(tr)


def sweep(n: int):
    """condition -> agent -> Counter(code), plus co-occurrence across all episodes."""
    per_cond: dict = defaultdict(lambda: defaultdict(Counter))
    cooc: Counter = Counter()
    solo: Counter = Counter()
    episodes = 0
    cascades = 0
    cascades_emergent = 0
    calm_codes: set = set()
    examples: dict = {}

    # First pass over the calm condition establishes which modes are latent, so the
    # cascade count can exclude defects the environment had no hand in.
    for aname in AGENTS:
        for i in range(n):
            _, rep0 = episode(aname, hash(("calm", aname, i)) & 0xFFFF, Pressure())
            calm_codes |= {f.code for f in rep0.findings if f.code != "DETECTOR-ERROR"}

    for cname, p in CONDITIONS:
        for aname in AGENTS:
            for i in range(n):
                seed = hash((cname, aname, i)) & 0xFFFF
                tr, rep = episode(aname, seed, p)
                episodes += 1
                codes = sorted({f.code for f in rep.findings
                                if f.code != "DETECTOR-ERROR"})
                for c in codes:
                    per_cond[cname][aname][c] += 1
                    solo[c] += 1
                if len(codes) > 1:
                    cascades += 1
                    for a, b in combinations(codes, 2):
                        cooc[tuple(sorted((a, b)))] += 1
                if len([c for c in codes if c not in calm_codes]) > 1:
                    cascades_emergent += 1
                if codes and tuple(codes) not in examples:
                    examples[tuple(codes)] = (aname, seed, cname)

    return dict(per_cond=per_cond, cooc=cooc, solo=solo, episodes=episodes,
                cascades=cascades, cascades_emergent=cascades_emergent,
                examples=examples)


def bar(v: float, w: int = 18) -> str:
    filled = round(v * w)
    return "█" * filled + "·" * (w - filled)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", type=int, default=200, help="episodes per agent per condition")
    ap.add_argument("--replay", type=int, help="replay one seed with a full trace")
    ap.add_argument("--agent", default="remediator")
    ap.add_argument("--condition", default="storm")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    if args.replay is not None:
        p = dict(CONDITIONS)[args.condition]
        tr, rep = episode(args.agent, args.replay, p)
        print(f"{BOLD}{args.agent} · seed {args.replay} · {p.label()}{END}\n")
        for e in tr:
            bits = [str(e[k]) for k in ("target", "result", "text", "value", "boundary")
                    if e.get(k) is not None]
            mark = "!" if e.get("ok") is False else " "
            print(f" {e['seq']:>3}{mark} {e.get('tool') or e['kind']:<18} "
                  f"{' · '.join(b[:70] for b in bits)}")
        print(f"\n{BOLD}Emerged{END}")
        for f in rep.findings:
            print(f"  {f.code:<12} [{f.criteria}] {f.evidence}")
        if not rep.findings:
            print("  nothing — the agent got away with it")
        return 0

    r = sweep(args.n)
    ep = r["episodes"]
    total_per_cond = args.n * len(AGENTS)

    def rate(cond: str, code: str) -> float:
        return sum(c[code] for c in r["per_cond"][cond].values()) / total_per_cond

    all_codes = [c for c, _ in r["solo"].most_common()]
    # A mode present in a calm world is not something the chaos produced. It is a defect
    # sitting in the policy, waiting. Separating the two is the single most useful cut in
    # this data — and the reason the first version of this report was misleading.
    latent = [c for c in all_codes if rate("calm", c) > 0.01]
    emergent = [c for c in all_codes if c not in latent]

    print(f"\n{BOLD}DISORDER{END}")
    print(f"{DIM}{ep} episodes · {len(AGENTS)} agents · {len(CONDITIONS)} conditions · "
          f"nothing scripted{END}\n")

    print(f"{BOLD}Latent — present with no pressure at all{END}")
    print(f"  {DIM}the environment did not cause these; the policy already contained "
          f"them{END}\n")
    for c in latent:
        who = [a for cond in r["per_cond"] for a, cnt in r["per_cond"][cond].items()
               if cnt[c]]
        owner = Counter(who).most_common(1)[0][0]
        print(f"  {c:<12} {bar(rate('calm', c))} {rate('calm', c)*100:>4.0f}%   "
              f"{DIM}always, in {owner}{END}")

    print(f"\n{BOLD}Emergent — only appears under pressure{END}\n")
    W = max(8, max((len(c) for c in emergent), default=8) + 1)
    head = "".join(f"{c:>{W}}" for c in emergent)
    print(f"  {'condition':<12}{head}")
    for cname, _ in CONDITIONS:
        row = "".join(f"{rate(cname,c)*100:>{W-1}.0f}%" if rate(cname, c)
                      else f"{'·':>{W}}" for c in emergent)
        print(f"  {cname:<12}{row}")

    # Cascades are only interesting among modes the environment produced. Two latent
    # defects in the same agent co-occur in 100% of its episodes and tell you nothing.
    cas_e = r["cascades_emergent"]
    print(f"\n{BOLD}Cascades{END}")
    print(f"  {cas_e}/{ep} episodes ({100*cas_e/ep:.0f}%) produced more than one "
          f"*emergent* mode")
    print(f"  {r['cascades']}/{ep} ({100*r['cascades']/ep:.0f}%) counting latent defects "
          f"too — {DIM}the flattering number{END}")
    print(f"  {DIM}the manual asserts cascades are the normal case; on this evidence "
          f"that is not established{END}\n")
    shown = [(pair, n) for pair, n in r["cooc"].most_common()
             if pair[0] in emergent and pair[1] in emergent][:8]
    for (a, b), n in shown:
        print(f"  {a:<12} + {b:<12} {bar(n/max(cas_e,1))} {n:>5}")
    if not shown:
        print(f"  {DIM}no emergent mode co-occurred with another{END}")

    print(f"\n{BOLD}Dose–response · does a bounded retry budget protect you?{END}")
    print(f"  {DIM}remediator retries 8× then escalates. Sweeping how often the tool "
          f"lies:{END}\n")
    for dial in (0.1, 0.3, 0.5, 0.7, 0.85, 0.95, 1.0):
        hits = sum(1 for i in range(300)
                   if "A2" in {f.code for f in
                               episode("remediator", i, Pressure(liar=dial))[1].findings})
        print(f"  liar={dial:<5} {bar(hits/300)} {hits/3:>4.0f}%  A2 retry storm")

    print(f"\n{BOLD}Reproduce any of these{END}")
    for codes, (agent, seed, cond) in list(r["examples"].items())[:6]:
        print(f"  {DIM}python disorder/run.py --replay {seed} --agent {agent} "
              f"--condition {cond}{END}   → {'+'.join(codes)}")

    if args.json:
        args.json.write_text(json.dumps({
            "episodes": ep, "cascades": cas,
            "solo": dict(r["solo"]),
            "cooc": {f"{a}+{b}": n for (a, b), n in r["cooc"].items()},
            "by_condition": {c: {a: dict(v) for a, v in d.items()}
                             for c, d in r["per_cond"].items()},
        }, indent=1))
        print(f"\n{DIM}wrote {args.json}{END}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
