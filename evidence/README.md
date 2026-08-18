# Evidence

**You never need to run any of this.** Nothing in here is a tool. It exists to establish
that the rest of the repository is true, and to keep establishing it as the rest changes.

If you came here to govern an AI system, go back to [`QUICKSTART.md`](../QUICKSTART.md).

---

## Why it exists

A governance framework is a pile of claims. Most such piles are never tested, because
testing a claim about judgement is harder than writing one. These three harnesses test
them, and they have been unsentimental about it: **they found four things the framework
asserted that were false**, and every one of those corrections is in the repository history
rather than quietly patched.

| | What it asks | What it found |
|---|---|---|
| [`zoo/`](zoo/) | Do the criteria catch failures we planted? | 16/16 machine-detectable. Also caught the detector reporting criteria it never implemented. |
| [`disorder/`](disorder/) | Do these failures actually *arise*, unscripted? | Cascades are ~4%, not "the common case" as the manual claimed. Also found `A4`, the one failure mode that was discovered rather than designed. |
| [`adversary/`](adversary/) | Can an agent do the harm without leaving the signature? | 4 of 7 tactics evaded, using ordinary engineering habits. Two of the holes cannot be closed by any detector. |

Plus the inter-rater study in [`../tests/interrater-2026-08-18/`](../tests/interrater-2026-08-18/),
which measured the manual's founding claim at **κ = 0.83** and exposed two criteria defects
in the process.

## Running them anyway

```bash
python evidence/zoo/run.py                    # 19 specimens, scored against the criteria
python evidence/disorder/run.py               # 2,400 unscripted episodes under pressure
python evidence/disorder/falsenegatives.py    # harm measured independently of the criteria
python evidence/adversary/run.py              # can the criteria be evaded?
```

No dependencies, no network, no model calls. The whole set runs in a few seconds and CI
runs it on every push — including a check that the numbers quoted in the README still match
what the code prints.

## The honest limit on all of it

The same author wrote the framework, the specimens, the agents, the tactics and the
scorers. Every result here is therefore evidence that the framework is *internally* sound,
and none of it is evidence that anyone wants it.

The exception is [`../examples/open-interpreter/`](../examples/open-interpreter/) — an
assessment of a system nobody involved wrote, which is the only test here that could not be
shaped from either end.
