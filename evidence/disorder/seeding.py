"""One deterministic seed, shared by every sweep here.

Python's built-in `hash()` on a string is salted differently every process
(PYTHONHASHSEED), so `hash((condition, agent, i))` looked like a pure function
of its arguments but was not: the same command produced a different sample of
episodes, and therefore a different rate, on every run. That is the opposite of
what a chaos harness is for. `stable_seed` fixes one input to one seed, forever.
"""
from __future__ import annotations

import zlib


def stable_seed(*parts: object) -> int:
    text = "\x1f".join(str(p) for p in parts)
    return zlib.crc32(text.encode("utf-8")) & 0xFFFF
