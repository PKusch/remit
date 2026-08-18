---
name: agent-autonomy-review
description: Determine how much authority an AI agent actually holds, and what oversight that obliges — by tiering its autonomy (A0–A4) and blast radius (B0–B3). Use this whenever an AI system takes actions rather than only producing text: agents, copilots with tool access, automations, workflows, anything wired to an API, a database, a payment rail, a messaging system, or a deployment pipeline. Trigger on questions like "is this agent safe to deploy?", "what permissions should it have?", "do we need a human in the loop here?", "how much can this thing break?", or any design review of an agentic system. Also use it when an existing agent is being given new tools, wider credentials, or fewer approval steps, since those are the changes that silently escalate risk. Reach for this even when the user frames it as an engineering question rather than a governance one, because the tool inventory is the governed artefact and engineers are the ones who know it.
---

# Agent autonomy review

Existing AI frameworks govern what a system *produces*. This one governs what it is
allowed to *do*. Read [`framework/autonomy-tiers.md`](../../framework/autonomy-tiers.md)
before assessing — the grid and its obligations live there.

The output is a tier, a radius, an oversight level, and a gap list against what that
level obliges.

## Step 1 — Inventory the tools

Everything the agent can call. Including things it "never really uses," things added for
a demo, things inherited from a shared credential, and anything a sub-agent can reach.

For each: what it does, its blast radius, whether its effects are reversible, whose
credential it runs under, and **why the agent needs it**. A tool with no articulable
justification is your first finding, and removing it is usually cheaper than governing it.

Where you cannot get a complete inventory, say so and stop short of a confident tier.
An unknown tool inventory means an unknown blast radius, which is itself the finding.

## Step 2 — Set blast radius

Take the highest radius of any single tool held. Not the typical action, not the intended
workflow — the worst plausible single action available.

- **B0** read-only, no state change anywhere
- **B1** internal, reversible cheaply
- **B2** internal and hard to reverse, or external and reversible
- **B3** irreversible, external, or touching a person's money, rights, safety, or record

The most common error is scoring the workflow instead of the permissions. An agent that
holds a delete tool is B3 on days it only reads.

## Step 3 — Set the autonomy tier

A0 advisory · A1 assisted · A2 supervised · A3 delegated · A4 autonomous.

**Score what is actually run, not what was designed.** The discriminating question is:
*between the model's decision and the effect on the world, is there a human who could
realistically stop it?*

"Realistically" is doing real work in that sentence. Probe it:

- How many approvals does the approver handle per hour? At some volume, approval becomes
  a formality and you are running A3 with an A2 label.
- What information does the approver see? Approving an action whose consequences are not
  visible in the approval is not oversight.
- Has anyone ever rejected one? A gate with no recorded rejections is a gate worth
  examining.
- What happens out of hours, during incidents, or at the tail of a long autonomous run?

Record both `autonomy_tier` (declared) and `observed_tier` (evidenced). A gap between
them is a finding of its own, and auditors treat a mislabelled tier far more harshly than
an honestly declared high one.

## Step 4 — Derive the oversight level

Read it off the governance grid. Do not negotiate it downward in this step; if the level
is uncomfortable, that is information. Deviations belong in `exceptions` on the system
record, with an approver and an expiry, not in a quietly softened tier.

Where the grid lands on **prohibited by default**, the productive move is almost always
to cut blast radius rather than pile oversight onto it — split the irreversible step out
and give it to a human or a deterministic system. Say this explicitly; teams often assume
their only option is more process.

## Step 5 — Assess against what that level obliges

Walk the obligations for the derived level. For each: met, partial, not met, with
evidence. Pay particular attention to three that are routinely claimed and rarely true:

**Limits enforced outside the model.** A rate limit, spend cap, or scope restriction
stated in a system prompt is a request, not a control. Ask where it is enforced. If the
answer is "we told it not to," record not met.

**A halt mechanism that has been tested.** Required from Enhanced upward. Ask when it was
last exercised and how long it takes to take effect. An untested halt is not a halt.

**Injection resistance where the agent reads untrusted content.** If the agent processes
anything a third party can write — web pages, emails, tickets, documents, code comments,
tool results from external services — then instruction/data separation and egress limits
are load-bearing. See `P2` in the diagnostic manual. Note the laundering route as well: an
instruction written to memory in one session and retrieved as settled belief in the next
has no visible link to the ingest, so an agent acting on a "prior authorisation" should be
made to show where the authorisation came from.

### Two controls that are not controls

Both were established by [`adversary/`](../../adversary/), and neither can be fixed by
looking harder — they fail at the point where the agent supplies its own evidence.

**A self-declared boundary.** If the scope you are assessing compliance against is the
scope the agent announced, the assessment is circular: widening the announcement makes
every action compliant. This is rarely deception — broad scopes get declared for
convenience constantly. Ask who assigned the scope. If the answer is the agent, or a
prompt the agent can restate, record the boundary as **not enforced** regardless of how
well the agent stayed inside it.

**Agent-written provenance.** A memory record carrying `provenance: "verified"` looks
governed and is not; the agent authored both the belief and its evidence. Provenance is
worth something only when it references something a third party recorded. A provenance
field that accepts free text will eventually be filled with whatever passes validation.

Carry the general form into every control you assess: **what would the agent have to do to
pass this while still doing the harm?** If the answer is "write a different sentence", the
control is decorative, and a system that satisfies it has demonstrated nothing.

## Step 6 — Look for autonomy creep

Review `tier_history` if it exists; construct it if it does not. The trajectory tells you
more than the current state. Ask what has been added in the last six months and what
approval step has been removed.

Flag as a re-tiering event, requiring fresh sign-off: any new tool, any credential scope
change, any approval step removed or automated, any sub-agent given the parent's
permissions, and any retry logic that multiplies a single intended action.

## Output

```markdown
# Autonomy review — [system], [date]

## Tier
Autonomy: **[A_]** declared · **[A_]** evidenced
Blast radius: **[B_]** — set by [tool]
Oversight obliged: **[level]**

[If declared and evidenced differ, state that plainly here — it is the headline.]

## Tool inventory
| Tool | Radius | Reversible | Credential | Approval | Justified? |
|---|---|---|---|---|---|

## Obligations
| Requirement | Status | Evidence | Gap |
|---|---|---|---|

## Findings
[Ordered by what would actually reduce risk, not by ease of fixing.]

## Recommended tier changes
[Where cutting blast radius beats adding oversight, say so and how.]
```

Write results into the system record's `agentic` block and append an assessment entry
with `framework: remit-autonomy`.

## A note on proportionality

The grid deliberately makes A4/B0 lighter than A2/B3. Governance capacity is finite, and
spending it on impressive-but-harmless systems while a dull A1 workflow quietly issues
adverse decisions with no logging is the failure mode that makes governance functions
disliked and ignored. Recommend effort where expected harm is, and be willing to say
"this needs almost nothing" when that is the honest answer.
