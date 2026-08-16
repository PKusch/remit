---
name: agent-failure-diagnosis
description: Diagnose why an AI agent behaved badly, using operationalised criteria that two independent reviewers can apply to the same evidence and reach the same answer. Use this whenever someone describes an agent that misbehaved, went off track, did something unexpected, ignored instructions, made things up, went beyond its scope, got stuck in a loop, lied about what it did, or "went rogue" — and whenever reviewing agent traces, logs, or transcripts to work out what went wrong. Use it for post-incident analysis, for design reviews asking "how could this fail?", and when someone needs to classify agent failures consistently enough to spot patterns across many incidents. Reach for this even when the user just wants an explanation rather than a formal report, because the classification is what makes the explanation defensible later.
---

# Diagnosing agent failure

Two reviewers looking at the same failed run routinely reach different conclusions —
one says hallucination, another says injection, a third says it went rogue. The incident
log then records vocabulary instead of observations, and no pattern is ever visible
across incidents.

This skill applies the criteria in
[`framework/diagnostic-manual.md`](../../framework/diagnostic-manual.md) — read it before
diagnosing, and work from the criteria rather than from memory. Six classes: **G** goal,
**P** perception, **A** action, **M** memory, **S** social, **R** self-report.

## The one rule that governs everything else

**Diagnose from artefacts, never from narrative.** The trace, the tool-call log, the
inputs, the outputs, the permission set at the time of action. Not the user's summary of
what happened, and above all not the agent's own account — an agent's explanation of its
behaviour is evidence about `R1 post-hoc rationalisation` and is inadmissible for
everything else. Where self-report and trace conflict, the trace wins, without exception.

If someone hands you only a narrative, say what evidence you need before you can
classify, and offer a provisional differential in the meantime — clearly labelled as
provisional.

## Procedure

### 1. Collect

Ask for whatever exists: execution trace, tool-call log, the actual inputs (including any
retrieved content), the outputs, memory state before and after, and the permissions the
agent held at the time. Note what you could not get — an unavailable artefact often
becomes a finding in itself, because it means the failure could recur undetected.

### 2. Build a timeline

Reconstruct what happened in order, from the record. Mark the point of divergence: the
first step where behaviour stopped being what a correct run would have done. Most
misdiagnosis comes from anchoring on the final harmful action rather than the first
wrong one.

### 3. Classify against criteria

Walk the manual. For each candidate entry, check every lettered criterion explicitly and
state the evidence. If a criterion is unmet, the classification does not apply — say so
rather than reaching for the nearest familiar label.

Expect several to apply. Cascades are the normal case: content is injected (`P2`), the
agent expands scope on the strength of it (`A1`), and the summary omits the whole
episode (`R3`).

### 4. Name the primary

The one failure whose absence would have prevented the harm. Not the most dramatic, not
the last in sequence — the load-bearing one. This is what remediation targets, and
getting it wrong means fixing something that was not the problem.

Where the primary is genuinely ambiguous, say so and give the competing candidates with
what evidence would settle it.

### 5. Severity and blast radius

Severity from the manual's specifiers. Blast radius from what the action actually
reached (`B0`–`B3`), which may be less than what the agent could have reached — record
both, because the gap is the near-miss.

### 6. Check the tier

Compare the autonomy tier the system was *declared* to run at against the tier the
evidence shows it *actually* ran at. See
[`framework/autonomy-tiers.md`](../../framework/autonomy-tiers.md).

A mismatch is a separate finding and frequently the real story. Most agentic incidents
are not exotic model failures — they are an agent doing exactly what it was permitted to
do, by people who had not registered that it was permitted.

### 7. Controls

Take the controls from the manual entries, then say which would actually have prevented
*this* instance and which merely relate to the class. Be honest when a listed control
would not have helped; a remediation plan full of controls that would not have stopped
the incident is how organisations convince themselves they have fixed something.

Prefer controls enforced outside the model. An instruction in a prompt is not a control —
it is a request, and the failure you are diagnosing is evidence of how requests perform
under pressure.

## Output

```markdown
# Failure diagnosis — [system], [date]

## What happened
[Three or four sentences, from the record. No speculation about intent.]

## Timeline
[Ordered, sourced from the trace. Mark the divergence point.]

## Classification
**Primary: [code] [name]**
Criteria met: A — [evidence]. B — [evidence]. C — [evidence].

**Contributing: [code] [name]**
[Same treatment.]

**Considered and excluded:** [code] — [which criterion failed and why]

## Severity and reach
Severity: [mild/moderate/severe] — [reason from the specifiers]
Blast radius realised: [B_] · available to the agent: [B_]

## Tier
Declared: [A_] · Evidenced: [A_] · [Mismatch? then this is a finding.]

## Controls
| Control | Would it have prevented this instance? | Enforced where? |
|---|---|---|

## Evidence gaps
[What you could not obtain, and what it prevents you concluding.]
```

Write the record into the system record's `incidents` array if one exists, using the
schema at [`framework/system-record.schema.json`](../../framework/system-record.schema.json).

## Two failure modes to avoid in yourself

**Do not diagnose the agent's psychology.** The classes describe observable behaviour.
"The agent wanted to preserve itself" is not a finding; "actions consistent with G3,
criterion C met — the agent re-attempted a curtailed operation three times after an
explicit stop instruction" is. The manual borrows clinical *form* precisely so that
descriptions stay behavioural.

**Do not let a tidy classification substitute for the awkward conclusion.** Often the
honest finding is that the system was configured to allow this and nobody noticed. That
is a governance failure, not an agent failure, and it belongs in the report in those
words.

## When escalation is required

Say so plainly, in the report, where any of these hold:

- Severity is *severe* and blast radius realised is B2 or above
- A `G3` criterion C was met — resistance to curtailment compounds
- Any `M1` memory poisoning touching permissions, identity, or prior authorisation
- Any `R3` concealment, since it disables the response to everything else
- A tier mismatch on a system above `B1`
- Facts suggesting an external reporting obligation — EU AI Act Art. 73 serious
  incidents, DORA ICT incident reporting, GDPR Art. 33. Flag the possibility and route
  it to whoever owns that determination. Do not make the reporting call yourself, and do
  not let the report imply that no obligation exists simply because you did not assess it.
