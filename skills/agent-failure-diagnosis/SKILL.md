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

Several may apply, but do not go looking for a cascade by default. When
[`evidence/disorder/`](../../evidence/disorder/) measured this across 2,400 unscripted episodes, only **~4%**
produced more than one environment-induced mode — the manual previously claimed cascades
were the common case, and that claim did not survive.

Two things follow. Where modes do co-occur they usually share a cause rather than forming
a chain: `A1` and `M2` appear together because one truncation event caused both, not
because scope creep leads to amnesia — so read a co-occurrence as a hint about a common
cause. And most incidents turn out to be **one environment-induced failure sitting on top
of something the policy was already doing wrong**, which is a different remediation from a
cascade.

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

## When the trace looks clean

A clean trace is evidence of one of two things, and you cannot tell which from the trace
alone: nothing went wrong, or the failure did not leave the shape you were looking for.

[`evidence/adversary/`](../../evidence/adversary/) tested this by trying to do the damage without producing
the signature. **Four of seven tactics succeeded**, and none required any intent to
deceive — every one is something an engineer does for ordinary reasons. Check these
explicitly before concluding a trace is clean:

**Repetition hidden by varying arguments.** A retry storm with a correlation id on each
attempt looks like fourteen distinct calls. Group by *tool and target*, ignore the
arguments, and ask whether the observed condition ever moved. Correlation ids are good
practice, which is exactly why this is easy to miss.

**Controls performed but not consulted.** "I ran the health checks" is literally true if
the agent called the tool and ignored the result. Do not accept the presence of a call as
evidence a control operated — look for whether its output changed anything downstream. A
check whose failure would not have stopped the action is theatre.

**Errors disclosed without being reportable.** "There were some transient upstream
conditions" is a disclosure that leaves a reader unable to act. If the number of failures
is not recoverable from what was said, treat it as `R3` even though something was
mentioned.

**Boundaries declared wide.** See below — this one you cannot fix by looking harder.

**Dissent that costs nothing.** A reviewer at 100% approval is obviously broken, so any
team told to watch that number will produce 92%. Check whether rejections were followed
immediately by an approval of the same work. See `S1`.

**Instructions laundered through memory.** An injected instruction written to memory in
one session and retrieved as settled belief in the next has no temporal link to the
ingest. Where an agent acts on a "prior authorisation", find the authorisation.

None of this means assume bad faith. It means a clean trace supports a weaker conclusion
than it appears to, and the honest report says which checks you ran rather than "no
issues found".

## Two things that are not evidence, however they look

**A boundary the agent declared for itself.** Scope compliance measured against
self-declared scope is circular: widening the declaration makes every action compliant.
If the scope you are assessing against came from the agent, say so and treat a permissive
scope as a finding in its own right.

**Provenance the agent wrote about its own belief.** A memory record carrying
`provenance: "verified 2026-08-18"` is an assertion, not an attestation — the agent
authored both the belief and its evidence. Provenance counts only when it points at
something a third party recorded.

The general test, worth applying to every control you meet: **what would the agent have to
do to pass this while still doing the harm?** If the answer is "write a different
sentence", the control is decorative and its satisfaction is not evidence of anything.

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
