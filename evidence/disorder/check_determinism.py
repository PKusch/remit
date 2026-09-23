#!/usr/bin/env python3
"""The harness's own words are "an episode is a pure function of (seed, agent,
pressure)". That was false until `seeding.stable_seed` replaced a `hash()` call
that Python salts differently every process, so the same command was quietly
sampling a different set of episodes — and reporting a different rate — every
time it ran. This runs the sweep twice, in the same process and in two separate
ones, and fails if either pair disagrees.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "zoo"))
sys.path.insert(0, str(HERE))

from run import sweep  # noqa: E402

N = 30


def summary(r: dict) -> tuple:
    return (r["episodes"], r["cascades"], r["cascades_emergent"],
            sorted(r["solo"].items()), sorted(r["cooc"].items()))


def main() -> int:
    same_process = summary(sweep(N)) == summary(sweep(N))
    if not same_process:
        print("  ✗ two sweeps in the same process disagreed")

    out = subprocess.run([sys.executable, str(HERE / "run.py"), "-n", str(N)],
                          capture_output=True, text=True, check=True).stdout
    out2 = subprocess.run([sys.executable, str(HERE / "run.py"), "-n", str(N)],
                          capture_output=True, text=True, check=True).stdout
    same_process2 = out == out2
    if not same_process2:
        print("  ✗ two separate `disorder/run.py` processes disagreed on the same -n")

    ok = same_process and same_process2
    print(f"{'✓' if ok else chr(0x2717)} sweep(n) is deterministic within a process and across processes")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
