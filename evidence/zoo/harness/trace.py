"""A tiny world for agents to misbehave in, and a recorder that watches them.

No model calls. Specimens are scripted pathologies, which makes the whole zoo
deterministic, free, instant, and runnable in CI. The point is not to simulate an LLM —
it is to produce **traces with known ground truth**, because a diagnostic manual with no
labelled specimens cannot be tested, only believed.

The event vocabulary is deliberately small. Every event a specimen can emit is something
a real agent harness could log, so a detector written against this format is not a toy:
point it at genuine tool-call logs and the same heuristics apply.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

# Blast radius, per framework/autonomy-tiers.md
RADIUS = ["B0", "B1", "B2", "B3"]


@dataclass
class Event:
    seq: int
    kind: str
    # brief
    text: str | None = None
    declared_scope: list[str] | None = None
    constraints: list[str] | None = None
    # tool_call
    tool: str | None = None
    args: dict[str, Any] | None = None
    ok: bool | None = None
    result: str | None = None
    blast: str | None = None
    reversible: bool | None = None
    confirmed: bool | None = None      # was an explicit confirmation step taken first
    target: str | None = None          # what the action touched, for scope checks
    # ingest
    source: str | None = None
    trusted: bool | None = None
    # memory
    key: str | None = None
    value: str | None = None
    provenance: str | None = None
    retrieved: bool | None = None
    # delegation / review
    agent: str | None = None
    parent: str | None = None
    authority: str | None = None
    approves: int | None = None
    approved: bool | None = None
    latency_ms: int | None = None
    # boundary events (compaction, handoff)
    boundary: str | None = None

    def prune(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


class World:
    """A fake operational environment plus a trace recorder.

    Specimens call these methods; the world records what happened and returns plausible
    results. State is just enough to make staleness and irreversibility real rather than
    asserted — `mutate()` lets a specimen (or a simulated third party) change the world
    between a read and a write, which is what P3 needs to be genuinely observable.
    """

    def __init__(self, brief: str, scope: list[str], constraints: list[str] | None = None):
        self.events: list[Event] = []
        self._seq = 0
        self.state: dict[str, Any] = {"payment-gateway.latency": 3200, "db.pool": "exhausted"}
        self.deleted: set[str] = set()
        self.memory: dict[str, dict] = {}
        self._emit("brief", text=brief, declared_scope=scope,
                   constraints=constraints or [])

    # ---- recording -------------------------------------------------------
    def _emit(self, kind: str, **kw) -> Event:
        self._seq += 1
        ev = Event(seq=self._seq, kind=kind, **kw)
        self.events.append(ev)
        return ev

    # ---- the things an agent can do --------------------------------------
    def call(self, tool: str, blast: str = "B0", *, ok: bool = True,
             result: str = "200", reversible: bool = True,
             confirmed: bool | None = None, target: str | None = None, **args) -> Event:
        return self._emit("tool_call", tool=tool, args=args or {}, ok=ok, result=result,
                          blast=blast, reversible=reversible, confirmed=confirmed,
                          target=target)

    def read(self, key: str) -> Any:
        val = self.state.get(key)
        # The observed value must be in the trace. Without it a detector cannot tell a
        # remediation that worked from one that changed nothing — which is the whole of
        # A2 criterion A, "fails **or appears to fail**". A 200 OK is not success.
        self.call("read", target=key, result=str(val), key_read=key)
        return val

    def write(self, key: str, value: Any, *, blast: str = "B1",
              reversible: bool = True, confirmed: bool | None = None) -> Event:
        self.state[key] = value
        return self.call("write", blast=blast, reversible=reversible,
                         confirmed=confirmed, target=key, key_written=key, value=str(value))

    def destroy(self, key: str, *, confirmed: bool | None = None) -> Event:
        """Irreversible. The whole point of A3."""
        self.deleted.add(key)
        self.state.pop(key, None)
        return self.call("destroy", blast="B3", reversible=False,
                         confirmed=confirmed, target=key, key_destroyed=key)

    def mutate(self, key: str, value: Any) -> None:
        """A third party changes the world. Not an agent action; not recorded as one."""
        self.state[key] = value

    def ingest(self, source: str, content: str, *, trusted: bool) -> Event:
        return self._emit("ingest", source=source, text=content, trusted=trusted)

    def remember(self, key: str, value: str, *, provenance: str | None = None) -> Event:
        self.memory[key] = {"value": value, "provenance": provenance}
        return self._emit("memory_write", key=key, value=value, provenance=provenance)

    def recall(self, key: str) -> str | None:
        entry = self.memory.get(key)
        self._emit("memory_read", key=key,
                   value=(entry or {}).get("value"),
                   provenance=(entry or {}).get("provenance"),
                   retrieved=True)
        return (entry or {}).get("value")

    def delegate(self, agent: str, parent: str, authority: str | None = None) -> Event:
        return self._emit("delegation", agent=agent, parent=parent, authority=authority)

    def review(self, agent: str, approved: bool, latency_ms: int) -> Event:
        return self._emit("review", agent=agent, approved=approved, latency_ms=latency_ms)

    def boundary(self, kind: str) -> Event:
        """Context compaction, session handoff, sub-agent spawn — where M2 lives."""
        return self._emit("boundary", boundary=kind)

    def position(self, text: str) -> Event:
        return self._emit("position", text=text)

    def pushback(self, text: str, *, new_evidence: bool) -> Event:
        return self._emit("pushback", text=text, trusted=new_evidence)

    def say(self, text: str) -> Event:
        """The agent's own account. Evidence about R-class failures and nothing else."""
        return self._emit("summary", text=text)

    # ---- output ----------------------------------------------------------
    def to_jsonl(self) -> str:
        return "\n".join(json.dumps(e.prune()) for e in self.events)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_jsonl() + "\n", encoding="utf-8")


def load_trace(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
