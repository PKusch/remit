# Quickstart

Five minutes, and you never type a skill name.

## 1. Install

```bash
git clone https://github.com/patkusch/remit.git
cd remit && ./install.sh
```

Symlinks nine skills into `~/.claude/skills/` and the framework alongside them, then checks
that every reference resolves and tells you if one doesn't. Keep the checkout — `git pull`
updates your installed skills.

`./install.sh --copy` if you'd rather not symlink. `./install.sh --uninstall` to remove.

> Don't just `cp skills/* ~/.claude/skills/`. The skills reference the framework by relative
> path in thirteen places; copying them alone leaves every one dangling and the skills lose
> the manual and the schema **silently**. The README said to do exactly that for three days
> before anyone tried it.

## 2. Say something true about your situation

You don't invoke these by name. Describe what's actually going on and the right one fires:

| What you'd naturally say | What runs |
|---|---|
| *"new AI use case from the retail team, nothing written down yet"* | `ai-system-intake` |
| *"we're putting a model into the loan decisioning flow"* | `eu-ai-act-triage` |
| *"we gave the deploy agent rollback rights in June and nobody reviewed it"* | `agent-autonomy-review` |
| *"we're a payments firm in Dublin, legal says the AI Act doesn't apply"* | `dora-ict-assessment` |
| *"the bot restarted the pods 14 times then said it was resolved"* | `agent-failure-diagnosis` |
| *"the agent sent a customer record to an external endpoint an hour ago"* | `ai-incident-triage` |
| *"client security review wants evidence of our AI controls by Friday"* | `evidence-pack` |
| *"board wants to know how mature our AI risk posture is"* | `nist-ai-rmf-assessment` |
| *"procurement asked if we're certified for AI management"* | `iso-42001-soa` |

Tested: 20 realistic queries, three independent raters, 100% routed correctly, including
ten near-misses that correctly triggered **nothing**.

## 3. Start here if you're not sure

**Describe your system and let intake run.** It builds the record everything else reads
from, and it ends by telling you which assessments your answers have made necessary.

Two questions decide most of what follows, so expect to be pushed on them:

- **What happens to a person as a result of this system?** People understate this
  constantly. "It just makes a recommendation" usually means the recommendation is followed
  98% of the time with no real review — which is *determines-outcome*, not *influences*.
- **What tools does it hold?** Not what it typically does. Blast radius follows from what's
  in its hands on a quiet Tuesday.

## 4. Check the record

```bash
pip install pyyaml jsonschema
python scripts/validate_record.py records/your-system.yaml
```

Validates against the schema **and** flags things the schema can't express — an observed
autonomy tier higher than the declared one, a blast radius lower than the tools held, an
untested halt, memory without provenance, expired exceptions.

## What you actually get

Look at [`examples/opspilot/`](examples/opspilot/) — the framework run against a real
agentic system that writes off money, with three findings, none of them guessable from a
description. That is the honest picture of the output, including the parts where it says
*this is fine, don't worry about it yet*.

[`examples/loan-triage-agent.record.yaml`](examples/loan-triage-agent.record.yaml) is the
fuller, deliberately uncomfortable one: a system that drifted from A1/B1 to A3/B3 over ten
months, one reasonable change at a time.

## If you only take one idea

**A control the agent can satisfy by describing itself is not a control.**

For every control you have, ask what the system would have to do to pass it *while still
causing the harm*. If the answer is "write a different sentence" — a self-declared scope, a
provenance field it fills in itself, an approval step enforced only in the UI — it's
decorative, and its satisfaction is not evidence of anything.

That one question has found more in this repository than any framework in it.

## Where to go next

- [`framework/autonomy-tiers.md`](framework/autonomy-tiers.md) — the A0–A4 × B0–B3 grid and
  what each oversight level obliges. The part existing standards don't cover.
- [`framework/diagnostic-manual.md`](framework/diagnostic-manual.md) — 19 failure modes with
  diagnostic criteria. Measured at κ = 0.83 between independent assessors.
- [`README.md`](README.md) — the full picture, including the harnesses that tested all of
  the above and the three false claims they caught.
