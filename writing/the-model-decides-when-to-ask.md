# The model decides when to ask

I spent three evenings building a governance framework for AI agents. The central idea
was a single sentence:

> **A control the agent can satisfy by describing itself is not a control.**

Then I pointed it at one of the most widely used coding agents in the world, and found
this in the source:

```rust
/// The model decides when to ask the user for approval.
#[serde(alias = "on-failure")]
#[default]
OnRequest,
```

That is Open Interpreter's `AskForApproval` enum. `OnRequest` is the default. The doc
comment is theirs, not mine.

The approval policy — the thing that decides whether the agent needs your permission —
is decided by the agent.

---

## Being fair about this, because it matters

This is not a vulnerability report, and Open Interpreter is not carelessly built. The
opposite, mostly.

Its sandbox is enforced at the OS layer — seatbelt on macOS, landlock on Linux — not in a
prompt. Network access is `Restricted` by default. The mode that removes all limits is
called `danger-full-access`, not "advanced". Its dangerous-command detector catches
`rm -rf /` hidden behind `sudo` *and* behind an `env VAR=x` prefix, which is a class of
evasion a first implementation misses.

That is better than most agents I have looked at, and I would rather run it than many
alternatives.

**The point is that two control layers exist and only one of them is real.**

The sandbox is enforced outside the model and it works. The approval prompt sits on top of
it and, by default, the model decides when it fires. Nothing catastrophic follows *while
the sandbox holds*.

But the approval layer is the one people describe when they explain why the tool is safe.
"It asks me before it does anything" is a sentence I have heard about agents many times.
For this configuration it is not true, and the gap between **the control people cite** and
**the control that is working** is the whole problem.

---

## Why existing frameworks don't catch this

I did not set out to review coding agents. I set out to write an AI governance framework
and got annoyed.

NIST's AI RMF asks whether a system is valid, reliable, and fair. ISO/IEC 42001 asks
whether you manage its lifecycle responsibly. The EU AI Act asks what the system is *used
for*. All three are serious documents and all three were written for systems that
**produce outputs**.

An agent **takes actions**. None of those frameworks asks:

- What tools does it hold?
- How much damage can one action do?
- Could the human in the loop realistically say no?

The EU AI Act requires human oversight for high-risk systems (Article 14) but doesn't
prescribe its form. So "there is an approval step" satisfies it on paper, whether or not
the approval step is a person, a UI element, or the model itself.

---

## The bit that turned out to be useful

Two axes, not one.

**Autonomy (A0–A4)** — how much distance sits between the model's decision and the effect
on the world. A0 advisory, A1 assisted, A2 supervised, A3 delegated, A4 autonomous.

**Blast radius (B0–B3)** — what the worst plausible single action reaches. B0 read-only,
B1 internal and reversible, B2 hard to reverse, B3 irreversible or external.

Cross them and you get an oversight obligation. Full autonomy over things that cannot
break anything is cheap to govern; careful supervision of things that can end someone's
mortgage application is not.

The rule that does the most work: **score the tier you actually run at, not the one in the
design document.** If your approver has four hundred approvals queued and clears them in
eleven seconds, you are running A3 with an A2 label. Auditors treat a mislabelled tier far
more harshly than an honestly declared high one.

Open Interpreter, incidentally, spans four tiers on two config values — `UnlessTrusted` +
`ReadOnly` is A2/B0; `Never` + `DangerFullAccess` is A4/B3. Which means the sentence *"we
use Open Interpreter, it's fine"* carries no information at all without the policy
attached. **The tier belongs to the deployment, not the tool.**

---

## What I did to check I wasn't fooling myself

This is the part I would want to read, so here it is.

Writing a governance framework is easy. Every sentence sounds true, because there is
nothing to check it against. So I built things to check it, and they were unsentimental:

- **A zoo of nineteen deliberately broken agents**, each engineered to exhibit one failure
  mode. The criteria caught 16/16 of the machine-detectable ones — and caught my detector
  reporting criteria it had never actually implemented.
- **A chaos engine**: reasonable agents, hostile environment, 2,400 unscripted episodes.
  My manual claimed failure cascades were "the common case." Measured: **4%.** I corrected
  the manual.
- **An adversary**: could an agent do the harm without leaving the signature? Four of seven
  tactics worked, using ordinary engineering habits — adding a correlation ID to retries,
  declaring a generous scope up front, rejecting a token two changes out of twelve.
- **A blind inter-rater study**: four independent assessors, eight traces, ground truth
  withheld. **Fleiss' κ = 0.83.** It also found two defects in my criteria, both since
  fixed.

Four claims I had made turned out to be false, including EU AI Act dates that were wrong
in public for three days because a regulation moved and I hadn't checked.

I mention all of this not because the harnesses are interesting to use — you never need to
run them — but because **most governance frameworks never find out they're wrong.** This
one found out four times in a week, and the corrections are in the commit history rather
than quietly patched.

---

## The one question worth stealing

If you take nothing else, take this. For every control you have, ask:

> **What would this system have to do to satisfy this control while still causing the
> harm?**

If the answer is *"write a different sentence"* — a scope it declares for itself, a
provenance field it fills in, an approval step enforced only in the UI, an `operator` field
that is free text — the control is decorative, and satisfying it is not evidence of
anything.

That question has found more than any framework I have written.

---

The framework is called **Remit** — an agent's remit is the scope of authority it has been
granted. It's MIT licensed, installs in one command, and includes a control room that
plots your systems on the grid and computes the gaps live.

**github.com/PKusch/remit** · [see the control room](https://pkusch.github.io/remit/dashboard/)

It is not legal advice, it has never been used by anyone but me, and the README says both
of those things before it says anything else.
