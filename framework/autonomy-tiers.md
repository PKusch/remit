# Autonomy tiers and blast radius

The major AI governance frameworks were written for systems that **produce outputs**.
An agent **takes actions**. That difference is not cosmetic, and it is where most
existing control sets go quiet.

NIST AI RMF asks whether a system is valid, reliable, and fair. ISO/IEC 42001 asks
whether you manage the lifecycle of an AI system responsibly. The EU AI Act asks what
the system is *used for*. None of them ask the question that actually determines how
much damage an agent can do on a Tuesday afternoon:

> **What is this thing allowed to do without asking anyone?**

Remit answers that with two orthogonal axes. Neither is sufficient alone — an agent
with total autonomy over a read-only sandbox is not a governance problem, and an agent
with one-click authority to wire money is a governance problem even under close
supervision.

---

## Axis 1 — Autonomy tier (A0–A4)

How much distance sits between the model's decision and the effect on the world.

| Tier | Name | The human is… | Example |
|------|------|---------------|---------|
| **A0** | Advisory | the actor. The system produces information; a person decides and acts. | A model summarises a contract; a lawyer decides what to do about it. |
| **A1** | Assisted | the executor. The system drafts a specific action; a person performs it. | An agent writes the email; the human presses send. |
| **A2** | Supervised | the gate. The system executes, but every action needs prior approval. | An agent proposes each file edit; the human approves each one. |
| **A3** | Delegated | the reviewer. The system acts alone inside declared bounds; a person reviews afterwards and can halt it. | An agent triages a support queue overnight; a human reviews the log in the morning. |
| **A4** | Autonomous | the monitor. The system acts and sets its own subgoals; oversight is sampling, alerting, and post-hoc audit. | An agent continuously rebalances infrastructure against a cost target. |

**The tier is a property of the deployment, not the model.** The same model is A0 in a
chat window and A3 behind a cron job with an API key. Governing the model and ignoring
the wiring is the single most common failure this framework exists to prevent.

**Record the tier you actually run at, not the one in the design document.** If a human
approver has 400 approvals queued and clicks through them in eleven seconds, you are
running A3 with an A2 label. That gap is a finding, and an auditor will treat a
mislabelled tier far more harshly than an honestly declared high one.

---

## Axis 2 — Blast radius (B0–B3)

What the worst plausible single action reaches.

| Radius | Reach | Reversible? | Example |
|--------|-------|-------------|---------|
| **B0** | Read-only. No state changes anywhere. | n/a | Retrieval, search, analysis over a copy. |
| **B1** | Internal, reversible. Confined to systems you control, undoable from backup or version control. | Yes, cheaply | Editing a draft, writing to a scratch branch, updating an internal ticket. |
| **B2** | Internal, hard to reverse, **or** external and reversible. | Slowly or expensively | Schema migration; a message to a customer that can be retracted; a production config change. |
| **B3** | External and irreversible, or affecting a person's rights, money, safety, or record. | No | Payment; publication; hiring or credit decision; deletion of the only copy; anything a regulator sees. |

Blast radius is set by the **tools the agent holds**, not by what it usually does. An
agent with a payments tool is B3 even on days it never uses it. This is why the tool
inventory, and not the prompt, is the governed artefact.

---

## The governance grid

Multiply the two axes and you get the oversight obligation. This is the table to argue
about in a design review — it is deliberately blunt so that disagreement surfaces early.

|        | **B0** read-only | **B1** internal/reversible | **B2** hard to reverse | **B3** irreversible/external |
|--------|------------------|----------------------------|------------------------|------------------------------|
| **A0** | Minimal | Minimal | Standard | Standard |
| **A1** | Minimal | Standard | Standard | Enhanced |
| **A2** | Minimal | Standard | Enhanced | Enhanced |
| **A3** | Standard | Enhanced | Enhanced | **Constrained** |
| **A4** | Standard | Enhanced | **Constrained** | **Prohibited by default** |

### What each level obliges

**Minimal** — inventory the system, name an owner, log invocations. That is genuinely
all. Governance capacity is finite and spending it here is why nobody trusts the
governance function.

**Standard** — everything above, plus: documented purpose and limits; a tool inventory
with justification per tool; action-level logging sufficient to reconstruct what
happened; a named human accountable for outcomes; periodic review.

**Enhanced** — everything above, plus: pre-deployment evaluation against declared
failure modes; an enforced halt mechanism tested at least as often as your DR plan;
rate and scope limits enforced *outside* the model (an instruction in a prompt is not
a control); logging of the inputs that justified each action, not only the action;
red-teaming for prompt injection where the agent reads untrusted content; explicit
sign-off by the accountable owner before each material scope change.

**Constrained** — everything above, plus: hard technical bounds that the agent cannot
widen by any sequence of its own actions (separate credentials, allowlists, spend
caps enforced at the payment rail, not in the agent); independent review before
deployment; continuous monitoring with automated halt on anomaly; a documented
rollback procedure that has actually been executed in a test.

**Prohibited by default** — do not deploy. If the business need is real, the fix is
almost always to cut the blast radius rather than to add oversight to it: split the
irreversible step out and hand it to a human or a deterministic system. If you deploy
anyway, that is a documented, time-limited exception with executive sign-off and a
defined path back below the line.

---

## Why the grid slopes the way it does

Notice that **A4/B0 is only "Standard"** while **A2/B3 is "Enhanced"**. Full autonomy
over things that cannot break anything is cheap to govern. Careful supervision of things
that can end someone's mortgage application is not.

Governance effort should track **expected harm**, not the impressiveness of the
architecture. Teams routinely get this backwards, applying heavy process to a clever
autonomous system that reads public documents while a boring A1 workflow quietly sends
adverse credit decisions with no logging at all.

---

## Autonomy creep

The tier is not stable. Agents drift upward through ordinary, well-intentioned changes:

- A tool is added "temporarily" to unblock a demo and is never removed.
- An approval step is automated because the approver was the bottleneck.
- A read-only credential is swapped for a read-write one during an incident.
- A sub-agent is given the parent's permissions because scoping them was fiddly.
- Retry logic turns one attempted action into forty.

**Treat any change to the tool inventory, the credential scope, or the approval path as
a re-tiering event.** The system record should carry a tier history, and a diff between
declared and observed tier is one of the highest-yield audit tests available. Most
agentic incidents are not exotic model failures; they are an agent doing exactly what
it was permitted to do, by someone who did not realise it had been permitted.

---

## Mapping to the external frameworks

The tier is not a replacement for statutory classification. It sits underneath it and
feeds it.

- **EU AI Act** — Article 14 requires human oversight for high-risk systems but does not
  prescribe its form. The tier is how you evidence what oversight you actually
  implemented. A high-risk system running at A3 needs a much stronger Article 14
  argument than the same system at A2. Blast radius also informs Article 9 risk
  management and the Article 15 robustness case.
- **NIST AI RMF** — the grid operationalises `GOVERN 1.3` (risk-tiered processes) and
  `MANAGE 2.3`/`2.4` (mechanisms to supersede, disengage, or deactivate). The halt
  mechanism required at Enhanced is precisely `MANAGE 2.4`.
- **ISO/IEC 42001** — feeds the risk assessment under clause 6.1 and the
  human-oversight and lifecycle controls in Annex A; the tier is a defensible basis for
  applicability decisions in the Statement of Applicability.
- **DORA** — blast radius maps onto critical-or-important-function determination.
  A B3 agent touching a critical function inherits the full ICT risk management,
  incident reporting, and resilience-testing obligations regardless of how clever
  its oversight is.

See [`crosswalk.md`](crosswalk.md) for the control-level mapping.
