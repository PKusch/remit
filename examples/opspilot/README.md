# Worked example — a real system

Everything else in this repository is synthetic: specimens built to exhibit a mode, agents
built to meet a hostile world. This is the one assessment run against a system nobody
designed for the test.

**Target:** [github.com/patkusch/opspilot](https://github.com/patkusch/opspilot) — an
agentic reconciliation copilot for financial-services back office. 494 lines of Python. It
takes a plain-English intent, dispositions a queue of ledger breaks (auto-match, write off,
or escalate), executes the eligible ones, and verifies the outcome arithmetically.

It writes off money. That is what makes it worth assessing.

The assessment was produced by **reading the source**, not from a description — which is
the point. If the skills only work when someone hands you a tidy summary, they do not work.

## Start with what is good, because most of it is

The guardrail design here is better than most production agents:

- **Limits live in code, not prompts.** `DUAL_CONTROL_LIMIT`, `WRITE_OFF_LIMIT`,
  `WRITE_OFF_MIN_AGE`, `BATCH_WRITE_OFF_CAP` are module constants checked in the decision
  path. Ask it to write off £40,000 and you get an escalation — enforced, not requested.
- **There is no model in the decision path at all.** Intent parsing is regex; disposition is
  threshold logic. Most of the failure modes in
  [`framework/diagnostic-manual.md`](../../framework/diagnostic-manual.md) are designed out
  rather than mitigated.
- **It refuses to authorise itself.** `Store.run` rejects an empty operator and rejects the
  literal string `agent`.

A framework that only produces criticism is a framework nobody runs twice.

## Three findings, all at the same seam

Every one is about the boundary between the agent and the humans around it — not the
agent's own logic. That is precisely where this framework claims the gap usually is, which
is either a good sign or a reason to be suspicious of the framework; both readings are fair.

### 1. The dual-control limit is defeated by typing a different name

`POST /api/run` takes `operator` as a free-text string. There is no authentication on any
route. The strongest control in the system — nothing at or above £10,000 is ever automatic,
a human must sign off — rests on the caller honestly describing who they are.

This is the finding [`adversary/`](../../adversary/) had established two hours earlier by a
completely unrelated route: **a control the caller satisfies by describing itself is not a
control.** Seeing it land on real code within the same evening is the strongest evidence in
this repository that the abstraction is worth anything.

### 2. The proof is produced by the thing being proved

`execute_and_verify` mutates `break.status`, then computes four `VerificationCheck` objects
from the same in-memory objects it just mutated. "Cleared breaks actually gone" checks that
the code did what the code just did.

Conservation of value is a genuine arithmetic identity and does hold. But an independent
reader of the ledger would turn all four checks from assertion into evidence. The system's
own tagline — *verified, not asserted* — is exactly right about the ambition and one step
short of achieving it.

### 3. The approval gate is not enforced server-side

`/api/plan` and `/api/run` are separate endpoints, and the README describes a plan-then-
approve flow. But `/api/run` builds a *fresh* plan and executes it in the same call. Nothing
server-side requires that a plan was ever seen, let alone approved.

That is the **A2 declared / A3 evidenced** gap the tier model exists to surface — the
approval step lives in the UI, and the UI is not the control.

## What the tooling caught on its own

```bash
python scripts/validate_record.py examples/opspilot/
```

```
✓ examples/opspilot/opspilot.record.yaml
    ! observed tier A3 exceeds declared tier A2 — the system is running with
      more autonomy than it is governed for
    ! oversight level requires a halt mechanism; none recorded
```

Two of the three findings fell out mechanically from the record, without anyone reasoning
about them.

## Proportionality

As built this is a hackathon demo against a seeded in-memory queue. **None of the above is
urgent**, and saying so is part of the job — a framework that flags everything at the same
severity is one people learn to ignore.

The findings are conditional and the condition is deployment. Pointed at a live
reconciliation ledger inside an EU financial entity, this becomes ICT supporting a critical
or important function: DORA Art. 9 attaches, the missing halt becomes a resilience-testing
gap, and unauthenticated write-off authority becomes the sort of thing that ends up in a
regulatory finding. The record captures that as a conditional, not a scare.

## The honest read on the exercise

What was being tested was not OpsPilot. It was whether these skills produce findings
**specific to a system** or generic checklist noise.

On this evidence: specific. All three findings are things the code actually does, none
could have been guessed from a description, and two arrived from a defect class established
independently hours earlier. One data point is not a pattern — but it is the first one, and
it is not a flattering one, because the system assessed was written by the same person who
wrote the framework and the framework still found things.
