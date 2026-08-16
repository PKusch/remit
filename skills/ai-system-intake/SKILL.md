---
name: ai-system-intake
description: Create or update the governance record for an AI system or agent — the shared artefact every other Remit assessment reads from. Use this whenever someone describes an AI system, model, agent, copilot, chatbot, or automation and there is any governance, risk, compliance, audit, or regulatory dimension to the conversation; whenever a new AI use case is proposed, onboarded, inventoried, or registered; whenever someone asks "do we need to assess this?", "is this in scope for the AI Act?", or "what AI do we have?"; and always as the first step before any EU AI Act, NIST AI RMF, ISO 42001, DORA, or autonomy assessment, because those skills need a system record to work from. Use it even when the user has not asked for an inventory — if they are describing an AI system that will touch real users or real decisions, the record is what makes everything downstream possible.
---

# AI system intake

The record you produce here is the spine of every other assessment. Framework skills
read it; incident triage annotates it; the evidence pack assembles from it. When each
assessment keeps its own private notion of what the system is, they drift, contradict
each other, and an auditor finds the contradiction before you do.

Your job is to produce a record that is **accurate about what is actually deployed**,
not one that describes the design intention. That distinction is most of the value.

## What to produce

A YAML or JSON file conforming to [`framework/system-record.schema.json`](../../framework/system-record.schema.json).
Default to YAML for human editing unless the user is wiring this into tooling.

Name it `<system-id>.record.yaml`. Ask where it should live if there is an existing
inventory; otherwise propose `records/`.

## How to run the intake

Work conversationally. This is an interview, not a form — the useful answers usually
arrive as follow-ups to something the person said in passing.

### 1. Establish what it actually does

Get the intended use in language a non-specialist could check. If the answer is
abstract ("improves customer experience"), keep asking until you have something falsifiable
("ranks incoming support tickets by predicted urgency, and auto-closes ones scored below
0.2").

Then ask the question that drives most downstream classification: **what happens to a
person as a result of this system?** Map to `purpose.decision_consequence`:

- `none` — no person is affected
- `informational` — a person sees output but nothing follows from it automatically
- `influences-human-decision` — a human decides, with this as an input
- `determines-outcome` — the system's output effectively is the decision

People consistently understate this. "It just makes a recommendation" often turns out to
mean the recommendation is followed 98% of the time with no independent review, which is
`determines-outcome` in substance. Probe with: *how often is the output overridden, and
by whom, and what would that person have to do to override it?* A human who cannot
realistically dissent is not an oversight control — record what happens, not what the
process document says.

### 2. Fill `out_of_scope_uses` properly

This field earns its place. Most misuse findings are cases where nobody wrote down what
the system was *not* for, so a reasonable person extended it somewhere unreasonable.
Ask directly: what would be a wrong use of this? What would make you uncomfortable if
you found out someone was doing it?

### 3. Determine whether it is agentic

The test is not whether it is fashionable to call it an agent. Ask: **does it take
actions with effects outside its own output?** If it calls tools, writes to systems,
sends messages, or triggers workflows, populate the `agentic` block and hand off to
[`agent-autonomy-review`](../agent-autonomy-review/SKILL.md) for tiering.

Enumerate tools exhaustively, including ones "rarely used" — blast radius follows from
what is held, not from what is typical. For each tool, ask for a justification. A tool
nobody can justify is the finding.

### 4. Establish the supply chain role

Under the EU AI Act, obligations attach to roles, and most organisations are deployers
rather than providers. But note Art. 25: putting your name on a system, or substantially
modifying it, can convert you into a provider with the far heavier obligation set. If the
organisation is fine-tuning, rebranding, or materially changing intended purpose, flag
this explicitly — it is one of the most common and most expensive misclassifications.

### 5. Name a single accountable person

Not a team, not a function. If nobody can be named, that is the first finding, and it is
usually the one that predicts every other gap.

## Handling uncertainty

Record `unknown` rather than guessing. A record with honest gaps is auditable; a record
with confident fiction is worse than nothing because it stops anyone looking.

Where an answer materially changes downstream classification and is unavailable, note it
in `notes` and flag it in your summary as a blocking question. Do not stall the whole
intake on one open point — complete everything else and surface what is missing.

## What to tell the user afterwards

Give them, briefly:

1. The record location.
2. The two or three fields most likely to change a downstream conclusion if wrong —
   usually `decision_consequence`, `supply_chain.role`, and the tool inventory.
3. Which assessments this record now unlocks, and which are advisable given what it says.
   If `decision_consequence` is `determines-outcome`, or the system touches employment,
   credit, education, essential services, biometrics, or law enforcement, say plainly
   that EU AI Act triage should happen next.
4. Anything recorded as `unknown` that someone needs to go and find out.

Do not editorialise about compliance posture at this stage. Intake establishes facts;
the framework skills reach conclusions.
