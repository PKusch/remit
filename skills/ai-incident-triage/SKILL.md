---
name: ai-incident-triage
description: Triage an AI or agent incident — classify what failed, establish severity and reach, determine whether external reporting obligations are engaged, and produce the incident record. Use this whenever an AI system or agent caused a problem, produced a harmful or wrong output that reached someone, took an action it should not have, leaked data, or failed in production; whenever someone says "the agent did something bad", "we had an AI incident", "this model gave a customer the wrong answer", or asks whether an AI failure needs reporting to a regulator. Use it for near misses too, since those carry the same lessons at a fraction of the cost. Reach for this before writing any incident summary or RCA involving an AI system, because the classification and the reporting-clock assessment need to happen early — reporting deadlines under the EU AI Act and DORA run from awareness, not from the end of your investigation.
---

# AI incident triage

Two jobs, and the second is time-critical: **classify what happened**, and **establish
whether a reporting clock is running**. Do them in that order but do not let the first
delay the second — EU AI Act Art. 73 and DORA deadlines run from the point of awareness,
not from the point where your investigation concludes.

## Immediately: is a clock running?

Before the detailed analysis, make a preliminary call and say so explicitly. Get this
question to whoever owns the determination within the first hour.

Signals that an external obligation may be engaged:

- Death, serious harm to health, or serious damage to property
- Serious and irreversible disruption of critical infrastructure
- Breach of fundamental rights obligations
- Personal data breach (GDPR Art. 33 — 72 hours)
- ICT-related incident affecting a critical or important function (DORA)
- Any incident in a system classified high-risk under the EU AI Act

**You are not the person who makes the reporting decision.** Your job is to surface the
possibility fast, with the facts, and route it. Never let a report imply that no
obligation exists merely because you did not assess it — say what you assessed and what
you did not.

Timings, for the escalation note: EU AI Act Art. 73 — 15 days generally, 2 days for
widespread infringement or serious critical-infrastructure disruption, 10 days for death.
An initial incomplete report is permitted to meet the deadline.

## Then: classify

Run [`agent-failure-diagnosis`](../agent-failure-diagnosis/SKILL.md) for the mechanism,
working from [`framework/diagnostic-manual.md`](../../framework/diagnostic-manual.md).

The essentials, if you are doing it inline:

1. **Collect artefacts first** — trace, tool logs, inputs including retrieved content,
   outputs, memory state, permissions held. Not narrative. An agent's own account of
   what happened is evidence about `R1` and nothing else.
2. **Classify against criteria**, recording every entry whose criteria are met.
3. **Name the primary** — the failure whose absence would have prevented the harm.
4. **Severity** from the manual's specifiers; **blast radius realised** (`B0`–`B3`), and
   separately the radius that was *available*. The gap between them is the near-miss, and
   it is often the more important number.
5. **Check the tier** — declared versus evidenced. A mismatch is a separate finding and
   is frequently the actual story.

## Harm assessment

Distinct from severity, and the part most incident records skip.

- **Who was affected**, including people who were not users
- **How many**, and whether the number is known or estimated
- **Whether affected people know** — and whether they need to be told
- **Whether the harm is reversible**, and what reversal would take
- **Whether it is ongoing** — the first question, and the one that determines whether you
  are triaging or still responding

If the incident is ongoing, containment precedes analysis. Say so and stop.

## Remediation

Distinguish three horizons, and be honest about which you have actually done:

**Contain** — stop the bleeding. Usually a halt, a permission revocation, or a rollback.
**Correct** — fix this instance, including any bad state that was written.
**Prevent** — the control that stops the class recurring.

Take candidate controls from the diagnostic manual entry, then say which would actually
have prevented *this* instance. Be willing to say a listed control would not have helped.
A remediation plan full of controls that would not have stopped the incident is how
organisations persuade themselves they have fixed something.

Prefer controls enforced outside the model. If the proposed fix is "we updated the
prompt," record that as a mitigation, not a control, and say why.

## Output

```markdown
# Incident — [system], [date]

## Status
[Ongoing / contained / resolved] · Detected [when] · Contained [when]

## Reporting assessment — PRELIMINARY
Possible obligations: [EU AI Act Art. 73 / DORA Art. 19 / GDPR Art. 33 / none identified]
Clock starts: [awareness date/time]
Routed to: [who owns the determination] at [when]

## What happened
[From the record. No speculation about intent.]

## Classification
Primary: **[code] [name]** — criteria A/B/C with evidence
Contributing: [codes]
Severity: [mild/moderate/severe]
Blast radius realised: [B_] · available: [B_]
Tier declared: [A_] · evidenced: [A_]

## Harm
Affected: [who, how many, known or estimated]
Reversible: [yes/no — what reversal requires]
Notification needed: [yes/no/undetermined]

## Remediation
| Horizon | Action | Owner | Status |
|---|---|---|---|
| Contain | | | |
| Correct | | | |
| Prevent | | | |

## Evidence gaps
[What you could not obtain and what it prevents concluding.]
```

Append to `incidents` on the system record using
[`framework/system-record.schema.json`](../../framework/system-record.schema.json).

## Why consistency matters more than eloquence here

A well-written incident report that classifies by vibe is worth less than a terse one
that classifies by criteria. The value compounds only if records aggregate: ten incidents
classified consistently show you where your controls actually are, while ten described in
prose show you nothing. Resist the pull toward narrative.

## Near misses

Triage them the same way. An agent that *could* have sent the wrong payment and did not,
because a rate limit happened to fire, is the cheapest possible lesson about a real B3
exposure. Record the available blast radius, not the realised one, and treat it with the
severity that reach deserves.
