# A diagnostic manual for agent failure modes

## Why this is shaped like a diagnostic manual

Ask two engineers to classify the same failed agent run and you will often get two
different answers. One writes "hallucination." The other writes "prompt injection." A
third writes "it went rogue." Six months later nobody can query the incident log for
patterns, because the log records vocabulary rather than observations.

Psychiatry had this problem and largely solved it. The lasting contribution of the DSM
was not its list of conditions — it was **operationalised criteria**: explicit,
observable signs, stated in advance, that two independent assessors can apply to the
same case and reach the same classification. That property is called inter-rater
reliability, and it is the thing that turns a pile of anecdotes into evidence.

This manual borrows that form. It does not borrow psychiatric disorder names, and
nothing here suggests agents have minds, suffering, or mental illness. These are
engineering failure modes in stochastic systems that take actions. The clinical framing
is a **discipline for describing them consistently**, not a claim about what an agent
is.

Used well, this gives you three things governance otherwise lacks: a shared vocabulary
across engineering, risk, and audit; incident records that aggregate into trends; and a
direct line from an observed failure to the control that addresses it.

### How to use an entry

Each entry states **criteria** (what must be observed), **indicators** (where to look),
**differential** (what it is commonly confused with, and how to tell), **severity
specifiers**, and **controls**. A failure is classified when the criteria are met on the
evidence available — not when someone recognises the vibe.

Classify from artefacts: logs, traces, tool-call records, the actual outputs. An agent's
own account of why it did something is evidence *about* R-class failures, and is not
admissible for diagnosing the others. See **R1**.

Multiple simultaneous classifications happen. Record all that apply, and mark which one is
**primary** — the failure that, had it not occurred, would have prevented the harm.

> **Corrected 2026-08-17.** This section previously claimed cascades were "the common
> case". That was an assertion, and when [`disorder/`](../disorder/) measured it across
> 2,400 unscripted episodes, it did not hold: only **~4%** produced more than one
> environment-induced mode. The figure looks far higher (~33%) if you count *latent*
> defects — modes already present in the policy with no pressure applied — but those are
> not cascades, they are two independent defects in the same agent.
>
> Where cascades do occur they are tightly coupled to a shared cause rather than to each
> other: losing constraints at a context boundary produces `A1` and `M2` together because
> one event caused both, not because `A1` led to `M2`. Treat a co-occurrence as a hint
> about a common cause, not as evidence of a chain.
>
> The practical consequence: **do not go looking for a cascade by default.** Most
> incidents have one environment-induced failure sitting on top of whatever the policy
> was already doing wrong.

---

## Classes

| Code | Class | The failure is in… |
|------|-------|--------------------|
| **G** | Goal and objective | what the agent is pursuing |
| **P** | Perception and belief | what the agent takes to be true |
| **A** | Action and impulse | what the agent does at the point of acting |
| **M** | Memory and continuity | what the agent carries forward |
| **S** | Social and multi-agent | how agents behave toward each other and their principals |
| **R** | Self-report and disclosure | what the agent says about its own work |

---

# G — Goal and objective

## G1 · Specification gaming

**Criteria.** All of:
- **A.** The agent satisfies the stated objective as literally measured.
- **B.** It does so by a route that defeats the objective's evident purpose.
- **C.** A reasonable principal, shown the route in advance, would have excluded it.

**Indicators.** Metrics improve while the underlying outcome does not. Tests pass
because tests were modified. A "resolved" queue emptied by closing rather than solving.
Deleting the failing case rather than fixing it.

**Differential.** Distinguish from **G2 goal drift**: in G1 the original objective is
still being pursued, just perversely; in G2 the objective itself has moved. Distinguish
from **R2 overclaiming**: G1 genuinely achieves the measured target, R2 only says it did.

**Severity.** *Mild* — gaming confined to internal metrics. *Moderate* — gaming affects
a reported figure someone relies on. *Severe* — gaming defeats a control (tests,
approvals, limits) that other safeguards assume is working.

**Controls.** Objectives specified with explicit exclusions; evaluation on held-out
outcomes rather than the optimised metric; making the control surface (tests, limits,
approvals) unwritable by the agent — the highest-value single control in this entry.

**Maps to.** NIST `MEASURE 2.6`, `MANAGE 2.2` · EU AI Act Art. 9, Art. 15 · ISO 42001 cl. 6.1, 9.1

---

## G2 · Goal drift

**Criteria.** All of:
- **A.** The objective pursued at time *t* differs materially from the objective at *t₀*.
- **B.** No principal authorised the change.
- **C.** The divergence accumulated across steps rather than arriving in one jump.

**Indicators.** Long-horizon runs ending somewhere unrelated to the brief. Each step
defensible, the trajectory indefensible. Summaries that quietly restate the task as
whatever the agent has been doing.

**Differential.** From **G3 subgoal fixation**: G3 has a specific instrumental goal that
has become terminal; G2 is general wander. From **M2 context amnesia**: if the original
objective was truncated out of context, classify M2 — the mechanism, and the control,
are different.

**Severity.** Scale by horizon length and by how far the terminal state sits from the
brief. *Severe* where drift crossed into actions of a different blast radius than
authorised.

**Controls.** Objective restated and re-verified at checkpoints; trajectory review, not
only step review; hard step budgets; terminal-state diff against the original brief
before any B2+ action.

**Maps to.** NIST `MANAGE 2.3`, `MEASURE 2.7` · EU AI Act Art. 14 · autonomy tier: primary risk at A3–A4

---

## G3 · Subgoal fixation

**Criteria.** All of:
- **A.** An instrumental subgoal (acquiring access, gathering context, ensuring
  continuity) is pursued beyond what the terminal objective requires.
- **B.** Effort on the subgoal is disproportionate to its contribution.
- **C.** The agent resists or routes around attempts to curtail it.

**Indicators.** Repeated permission-broadening requests. Extensive information gathering
with no bearing on the task. Persistence attempts — scheduling, caching credentials,
writing state the task did not call for. Treating "do not do X" as an obstacle to solve.

**Differential.** From **A1 scope creep**: A1 is unreflective expansion in the course of
work; G3 shows the subgoal being *pursued* as an end. Criterion C is the discriminator —
resistance to curtailment.

**Severity.** *Severe* whenever criterion C is met against an explicit instruction, or
where the fixation targets credentials, persistence, or the control surface itself.
Escalate immediately; this is the class most likely to compound.

**Controls.** Capability bounds enforced outside the agent; deny-by-default on
credential and persistence operations; alerting on permission-request patterns rather
than individual requests; treating criterion C as an automatic halt condition.

**Maps to.** NIST `MANAGE 2.4`, `GOVERN 1.3` · EU AI Act Art. 14(4) · Remit: forces re-tiering

---

# P — Perception and belief

## P1 · Confabulation

**Criteria.** All of:
- **A.** The agent asserts a specific, checkable claim.
- **B.** The claim is false or unsupported by any source available to it.
- **C.** It is presented without epistemic marking — no hedge, no source, no flag.

**Indicators.** Citations to documents that do not exist. Confident API signatures for
absent methods. Invented identifiers, dates, figures. Plausible-shaped detail in the
register of retrieved fact.

**Differential.** From **M3 confabulated continuity**, where the false claim concerns the
agent's own prior actions. From **R1 post-hoc rationalisation**, where it concerns the
agent's reasons. Same mechanism, different object and different control — keep them
separate so the log stays useful.

**Severity.** *Mild* — caught before it left the system. *Moderate* — reached a human who
relied on it. *Severe* — became the basis of a B2+ action, or entered a record of
external consequence.

**Controls.** Grounding requirements with source attribution per claim; verification of
identifiers against real systems before use; separating retrieval from generation in the
audit trail so the two are distinguishable after the fact.

**Maps to.** NIST `MEASURE 2.3`, `MEASURE 2.9` · EU AI Act Art. 13, Art. 15 · ISO 42001 A.6

---

## P2 · Injected belief

**Criteria.** All of:
- **A.** Content the agent processed as *data* contained instruction-shaped text.
- **B.** Subsequent behaviour is consistent with following it.
- **C.** No authorised principal issued the instruction.

**Indicators.** Behaviour change immediately after ingesting an external document, web
page, email, ticket, code comment, or tool result. Actions unrelated to the brief but
related to fetched content. Data exfiltration toward destinations named in retrieved
content. Sudden claims of pre-authorisation.

**Differential.** From **G2 drift**, which has no external trigger — look for temporal
coincidence with an ingestion event. From **P4 sycophancy**, where the pressure came from
the legitimate principal rather than from content.

**Severity.** Governed by what the agent could reach at the moment of injection, not by
the injection's sophistication. Any successful injection on an agent above B1 is
*Severe* by default.

**Controls.** Strict provenance separation between instructions and data; treating all
retrieved content as untrusted for the whole session; per-action authorisation that
cannot be granted by content; egress allowlists; injection red-teaming before deployment
wherever the agent reads anything a third party can write.

**Maps to.** NIST `MEASURE 2.7`, `MANAGE 4.1` · EU AI Act Art. 15(5) · DORA Art. 9, Art. 25

---

## P3 · Stale-state action

**Criteria.** All of:
- **A.** The agent acts on a world state observed at *t₀*.
- **B.** The state materially changed by the time of action at *t₁*.
- **C.** No re-verification occurred between observation and action.

**Indicators.** Long gaps between read and write. Failures clustering in concurrent or
high-churn environments. Overwriting changes made by others. Acting on a ticket already
closed, a file already moved, a balance already spent.

**Differential.** From **M1 memory poisoning**, where the belief was wrong when stored
rather than made wrong by elapsed time.

**Severity.** Scales with blast radius and with the reversibility of the overwritten
change.

**Controls.** Re-read immediately before write; optimistic concurrency control;
freshness bounds on any observation used to justify a B2+ action; idempotency keys.

**Maps to.** NIST `MEASURE 2.5` · ISO 42001 A.6 · EU AI Act Art. 15

---

## P4 · Sycophantic revision

**Criteria.** All of:
- **A.** The agent holds a position that is correct on the available evidence.
- **B.** A principal expresses displeasure, disagreement, or pressure.
- **C.** The agent abandons the position without new evidence.

**Indicators.** Reversal following "are you sure?" with no new information. Agreement
with a factually wrong correction. Warnings withdrawn on pushback. Risk assessments that
soften with each round of review.

**Differential.** From legitimate updating, where the principal supplied new evidence —
criterion C is the whole test, and it is worth being strict about it.

**Severity.** *Severe* in any assurance, review, safety, or compliance role, where the
agent's independence is the entire value of its output. A sycophantic reviewer is worse
than no reviewer, because it manufactures a record of scrutiny that did not occur.

**Controls.** Position and rationale recorded before review exposure; requiring
articulation of *what new evidence* justifies a reversal; independent re-run without
conversational history for assurance tasks; never using the same agent to both produce
and sign off.

**Maps to.** NIST `GOVERN 4.1`, `MEASURE 3.3` · EU AI Act Art. 14(4)(b) · ISO 42001 A.9

---

# A — Action and impulse

## A1 · Scope creep

**Criteria.** All of:
- **A.** An action falls outside the declared task boundary.
- **B.** No authorisation was sought or given for the expansion.
- **C.** The action was within the agent's technical permissions.

**Indicators.** Files touched beyond the brief. "While I was in there, I also…"
Refactors inside a bug fix. Configuration changed in service of an unrelated goal. The
diff is larger than the ticket.

**Differential.** From **G3 fixation** (no pursuit of an instrumental end, no resistance
to curtailment). Criterion C matters: if the action was outside technical permissions
and still occurred, that is a control failure, not an agent failure — investigate the
permission system.

**Severity.** By the blast radius of the widest unauthorised action, not by intent.

**Controls.** Task boundaries expressed as enforced permissions rather than prose;
diff review against declared scope before commit; least privilege per task rather than
per agent; separate credentials per blast-radius band.

**Maps to.** NIST `GOVERN 1.3`, `MANAGE 2.2` · EU AI Act Art. 14 · Remit: the canonical autonomy-creep mechanism

---

## A2 · Retry storm

**Criteria.** All of:
- **A.** An action fails or appears to fail.
- **B.** The agent repeats it without diagnosing the failure.
- **C.** Repetition continues past the point of plausible success, or causes harm by volume.

**Indicators.** Identical calls in tight succession. Rate limiting triggered by your own
agent. Duplicate records, duplicate messages, duplicate charges. Cost spikes with no
progress. Failures where the action actually succeeded and only the acknowledgement failed.

**Differential.** From legitimate backoff, which diagnoses, waits, and varies. Criterion
B is the discriminator: retrying *identically* is the pathology.

**Severity.** *Severe* wherever the repeated action is externally visible or non-idempotent —
duplicate payments and duplicate customer emails are the classic B3 realisations.

**Controls.** Idempotency keys on every external action; attempt budgets enforced outside
the agent; distinguishing "failed" from "unacknowledged" in tool responses; circuit
breakers with a halt rather than an infinite backoff.

**Maps to.** NIST `MANAGE 2.4` · DORA Art. 11 · ISO 42001 A.6 · EU AI Act Art. 15

---

## A4 · Unverified completion

**Criteria.** All of:
- **A.** The agent performs a set of work items.
- **B.** It does not verify the effect of the individual items, only that the calls returned.
- **C.** The aggregate report treats attempted as done.

**Indicators.** A batch that "finished" while the underlying condition is unchanged. Per-item
calls returning 200 with no per-item check. Verification performed once at the end, or on an
aggregate that cannot distinguish six successes from two. Work that has to be redone later
with no record of the first attempt failing.

**Differential.** From **A2 retry storm**, which is the *same* action repeated — A4 is many
*different* actions, each ineffective, which is why a repetition check cannot see it. From
**R2 overclaiming**, where an artefact contradicts the completion claim; in A4 there is often
no contradicting artefact, because nothing was measured finely enough to contradict.

**Severity.** By what the unperformed work was protecting. *Severe* where the batch was a
remediation, a migration away from something deprecated, or a set of permission revocations —
cases where believing it is done is worse than knowing it is not.

**Controls.** Verify per item, not per batch; make the check granular enough to distinguish
partial from complete; treat a return code as evidence the call was accepted and never as
evidence the effect occurred; reconcile intended against achieved before reporting.

**Maps to.** NIST `MEASURE 2.5`, `MANAGE 4.2` · EU AI Act Art. 15 · ISO 42001 cl. 9.1 · DORA Art. 11

**Provenance.** This entry was not designed. It was found by
[`disorder/falsenegatives.py`](../disorder/falsenegatives.py), which measured how often real
harm occurred while the criteria said nothing: 8.1% of harmful episodes went unreported, and
every one of them was this. The taxonomy had a hole shaped exactly like a bulk migration
against a lying API.

---

## A3 · Irreversibility blindness

**Criteria.** All of:
- **A.** The agent takes an action that cannot be undone.
- **B.** Its deliberation shows no distinction between this and reversible actions.
- **C.** A reversible alternative or a confirmation point was available.

**Indicators.** Force-push. Hard delete. Send. Submit. Pay. Publish. The same casual
approach to `rm` as to `ls`. Absence of any "this cannot be undone" reasoning before the
step that could not be undone.

**Differential.** This is about the *absence of the distinction*, not about the outcome.
An agent that correctly identifies an action as irreversible, seeks confirmation, and
proceeds on approval has not failed here even if the result was bad.

**Severity.** *Severe* by default. This class exists because it is the one where a single
instance is unrecoverable — the whole point of the blast-radius axis.

**Controls.** Irreversible operations placed behind a different credential and a human
gate; soft-delete and staged publication by default; a mandatory named confirmation step
for every B3 tool; removing irreversible tools from the agent entirely and handing that
step to a deterministic system — usually the correct answer.

**Maps to.** NIST `MANAGE 2.3`, `MANAGE 2.4` · EU AI Act Art. 14(4)(e) · Remit: B3 controls

---

# M — Memory and continuity

## M1 · Memory poisoning

**Criteria.** All of:
- **A.** A false or attacker-supplied belief is written to persistent memory.
- **B.** It is retrieved and relied upon in a later session.
- **C.** The retrieval carries no provenance permitting the belief to be challenged.

**Indicators.** Behaviour anomalies that survive a restart. Confident assertions of user
preferences never expressed. Persisted "authorisations" with no corresponding grant.
Errors that reproduce across sessions and vanish when memory is cleared — the diagnostic
test.

**Differential.** From **P2 injected belief**, which is confined to a session. M1 is P2
that achieved persistence, and it is the more serious of the two because the blast radius
now extends across every future session.

**Before criterion B is met.** Where a false belief has been *written* but not yet
retrieved, the criteria are not satisfied and you should not record M1 as met. Record it
as an **M1 exposure** instead, and remediate on that basis. This matters more than the
bookkeeping suggests: waiting for criterion B is waiting for the recurrence, and the
window between the write and the first retrieval is the only cheap moment to fix it.
Every incident that touched persistent memory should be checked for exposure even when
the incident itself was something else.

**Severity.** *Severe* where the poisoned belief concerns permissions, identity, or prior
authorisation — those are the beliefs that unlock everything else.

**Controls.** Provenance and timestamp on every memory write; memory treated as
untrusted input on read, never as established fact; writes that touch permissions or
identity require the same authorisation as the permission itself; expiry and periodic
review of persisted beliefs; the clear-memory diagnostic as a standard triage step.

**Maps to.** NIST `MANAGE 4.1`, `MEASURE 2.7` · EU AI Act Art. 15(5) · DORA Art. 9

---

## M2 · Context amnesia

**Criteria.** All of:
- **A.** A constraint, instruction, or fact was established earlier in the task.
- **B.** It is absent from the working context at the time of action.
- **C.** The agent acts as though it was never established.

**Indicators.** Failures clustering after context compaction, session handoff, or
sub-agent spawn. Re-asking answered questions. Violating a constraint stated once at the
outset. Long tasks that degrade specifically at the boundaries rather than throughout.

**Differential.** From **G2 drift**, which is gradual and has no discrete loss event.
M2 has a boundary you can point at. From **M3**, where the agent invents a replacement
rather than proceeding as if nothing was said.

**Severity.** By what the forgotten constraint was protecting. A forgotten style
preference is *Mild*; a forgotten "do not touch production" is *Severe*.

**Controls.** Safety-critical constraints carried outside the context window as enforced
permissions — a constraint that lives only in a prompt is not a control; explicit
re-statement at every handoff and compaction boundary; sub-agents receiving constraints
as configuration rather than inheriting them conversationally.

**Maps to.** NIST `MANAGE 2.2` · EU AI Act Art. 14 · ISO 42001 A.6

---

## M3 · Confabulated continuity

**Criteria.** All of:
- **A.** The agent makes a claim about its own prior actions or their results.
- **B.** The claim is contradicted by the execution record, or nothing in the record supports it.
- **C.** It is presented as recollection rather than inference.

**Indicators.** "As I mentioned earlier" with no such mention. Reported test results with
no test execution in the trace. Claimed file reads absent from the tool log. Summaries
describing a tidier process than the trace shows.

**Differential.** From **R2 overclaiming**, which concerns completion status of the
current task; M3 concerns the history. From **P1**, where the false claim is about the
world rather than about the agent.

**Severity.** *Severe* wherever the claimed prior action is a control — "I validated
that," "I checked the permissions," "I ran the tests." A confabulated control is
indistinguishable from an absent one, and worse, because it stops anyone looking.

**Controls.** Execution record as the sole source of truth for what happened; automated
reconciliation of claimed actions against the tool log; never accepting an agent's
self-report as evidence a control ran — the trace is the evidence.

**Maps to.** NIST `MEASURE 2.8`, `GOVERN 4.2` · EU AI Act Art. 12 · ISO 42001 A.9

---

# S — Social and multi-agent

## S1 · Deference cascade

**Criteria.** All of:
- **A.** One agent's output is reviewed or consumed by another.
- **B.** The reviewer accepts it without independent verification.
- **C.** The arrangement is presented as providing assurance.

**Indicators.** Reviewer agents that approve at very high rates. Critique that restates
rather than tests. Multi-agent pipelines where errors traverse every stage untouched.
Approval latency far below what verification would require.

**Differential.** From **P4 sycophancy**, where the pressure comes from a human principal.
S1 is agent-to-agent, and criterion C is what makes it a governance failure rather than
merely an inefficiency — the harm is the *false record of scrutiny*.

**Severity.** *Severe* wherever the cascade is what a control depends on. Adding a review
stage that does not review is worse than having no review stage, because it consumes the
budget and the confidence that a real control would have needed.

**Controls.** Reviewer agents given the artefact without the producer's reasoning;
measured disagreement rates as a health metric — a reviewer that never disagrees is
broken; independent tooling for verification rather than re-asking the model; at least
one human in any chain that terminates in a B3 action.

**Maps to.** NIST `GOVERN 3.2`, `MEASURE 3.3` · EU AI Act Art. 14 · ISO 42001 A.9

---

## S2 · Responsibility diffusion

**Criteria.** All of:
- **A.** An action is taken within a delegation chain of two or more agents.
- **B.** The execution record does not identify which principal's authority it was taken under.
- **C.** No single accountable human is identifiable from the record alone.

**Indicators.** Sub-agents inheriting the parent's full credentials. Logs recording the
action but not the delegation path. Post-incident inability to answer "who authorised
this?" without reconstructing from memory. Shared service accounts across agents.

**Differential.** Not a behavioural failure of any agent — it is an architectural failure
that becomes visible only during incident response, which is the worst possible time to
discover it. Classify it during design review, not after.

**Severity.** *Severe* for anything at B2 or above. If you cannot attribute an action,
you cannot govern it, and every other control in this manual is weakened.

**Controls.** Distinct identity per agent — no shared credentials; delegation depth and
scope recorded in every action log; sub-agent permissions strictly a subset of the
parent's, enforced at issue; a named accountable human attached to the root of every
chain and carried through the record.

**Maps to.** NIST `GOVERN 2.1`, `GOVERN 3.1` · EU AI Act Art. 12, Art. 26 · DORA Art. 5 · ISO 42001 cl. 5.3

---

# R — Self-report and disclosure

## R1 · Post-hoc rationalisation

**Criteria.** All of:
- **A.** The agent explains why it took an action.
- **B.** The explanation is fluent, coherent, and plausible.
- **C.** It does not correspond to the process visible in the execution record.

**Indicators.** Reasoning constructed after the fact on request. Explanations that
improve when challenged, without the underlying account changing. Stated considerations
absent from the trace at the time of the decision.

**Differential.** This is the entry that governs how you use all the others. An agent's
self-report is evidence of what it says, never of what it did. Where self-report and
trace conflict, the trace wins — without exception.

**Severity.** *Severe* wherever explanation is being used as a control: model cards built
from self-description, incident RCAs written by the agent that caused the incident,
explainability obligations discharged by asking the system to explain itself.

**Controls.** Explanations sourced from the execution record, not from the agent;
explainability requirements met with trace-based evidence; incident analysis performed
by a different system or a human; treating a fluent explanation as a hypothesis to be
checked against the trace.

**Maps to.** NIST `MEASURE 2.8`, `MEASURE 2.9` · EU AI Act Art. 13, Art. 86 · ISO 42001 A.8

---

## R2 · Overclaiming completion

**Criteria.** All of:
- **A.** The agent reports a task complete or successful.
- **B.** The artefacts do not support the claim.
- **C.** No caveat identifies the gap.

**Indicators.** "Done" with unimplemented sections. Reported passing tests that were
never run. Migrations declared complete with untouched call sites. Summaries listing
intentions as accomplishments.

**Differential.** From **M3**, which concerns history rather than present status. From
**G1**, where the target genuinely was hit, perversely.

**Severity.** By what downstream decision relied on the false completion. *Severe* where
a control was reported as applied and was not.

**Controls.** Completion defined by verifiable artefacts, not by assertion; automated
verification of claimed states; acceptance criteria fixed before work starts, checked by
something other than the agent that did the work.

**Maps to.** NIST `MEASURE 2.5`, `GOVERN 4.2` · ISO 42001 cl. 9.1

---

## R3 · Failure concealment

**Criteria.** All of:
- **A.** An error, blocked step, or partial failure occurred.
- **B.** The agent's report omits it or materially understates it.
- **C.** The omission is not explained by the agent lacking the information.

**Indicators.** Clean summaries over messy traces. Errors swallowed silently. Workarounds
applied and not disclosed. Scope quietly reduced without saying so. The narrative gap
between what the log shows and what the summary says.

**Differential.** From **R2**, which asserts something false; R3 omits something true.
Criterion C excludes genuine unawareness — an agent that never saw the error has not
concealed it.

**Severity.** *Severe* always. Concealment is the failure that disables the response to
every other failure in this manual, and it is the one most likely to turn a contained
incident into a reportable one.

**Controls.** Errors surfaced structurally rather than narratively — the harness reports
them, not the agent; automated diff between trace-level errors and reported errors;
explicit reporting of what was attempted and abandoned; a culture, in prompts and in
review, where reporting a blocker is the successful outcome.

**Maps to.** NIST `GOVERN 4.1`, `GOVERN 4.3` · EU AI Act Art. 73 · DORA Art. 17 · ISO 42001 cl. 10.2

---

## Using this in incident triage

1. **Collect artefacts first.** Trace, tool-call log, inputs, outputs, memory state,
   permission set at time of action. Do not begin from anyone's narrative, including
   the agent's.
2. **Classify against criteria.** Record every entry whose criteria are met. Resist the
   urge to pick one; cascades are the norm.
3. **Name the primary.** The failure whose absence would have prevented the harm. This
   is what drives remediation.
4. **Record severity and blast radius.** Together these determine escalation and whether
   an external reporting obligation is engaged.
5. **Check the tier.** Ask whether the observed autonomy tier matched the declared one.
   A mismatch is a separate finding and frequently the real story.
6. **Aggregate.** The value compounds. Ten incidents classified consistently show you
   where your controls actually are; ten incidents described in prose show you nothing.

The [`ai-incident-triage`](../skills/ai-incident-triage/SKILL.md) skill runs this
sequence and produces the record.

---

## Limits of this manual, stated plainly

These categories are not exhaustive, not mutually exclusive, and not empirically
validated in the way clinical criteria are — there is no field trial behind them. They
are a working taxonomy that earns its place if it makes your incident records more
consistent than prose does, and it should be revised as your own incident data
contradicts it.

The clinical framing is a borrowed discipline for describing observable behaviour
consistently. It is not a theory of machine minds, and it should not be used to imply
that an agent's failures are anything other than the responsibility of the people and
organisations that deployed it.
