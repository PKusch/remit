# Remit

**An agentic skills framework for AI governance.**

Established AI governance frameworks were written for systems that *produce outputs*.
An agent *takes actions*. Remit is a set of installable agent skills that do real
governance work — classification, assessment, diagnosis, evidence — plus a framework
layer for the part existing standards leave thin: **what an agent is allowed to do
without asking anyone.**

The name is the thesis. An agent's remit is the scope of authority it has been granted,
and governance is the business of defining that scope, evidencing it, and enforcing it.

---

## Why this exists

Three gaps, and Remit is built around them.

**Governance frameworks stop at the model.** NIST AI RMF asks whether a system is valid,
reliable, and fair. ISO/IEC 42001 asks whether you manage its lifecycle responsibly. The
EU AI Act asks what it is used for. None of them ask what tools it holds, how large a
single action's blast radius is, or whether the human in the loop could realistically
say no. Remit adds an [autonomy and blast-radius model](framework/autonomy-tiers.md)
that answers those, and feeds the answers back into the statutory frameworks as evidence.

**Agent failures are described, not classified.** Two engineers look at the same failed
run and one writes "hallucination," the other "prompt injection," a third "it went
rogue." Six months later the incident log holds vocabulary instead of observations and no
pattern is visible. Remit includes a [diagnostic manual](framework/diagnostic-manual.md)
that borrows the DSM's *form* — numbered criteria, differential diagnosis, severity
specifiers — because its real contribution was inter-rater reliability, which is exactly
what agent incident classification lacks. It does not borrow psychiatric disorder names,
and nothing in it suggests agents have minds.

**Governance work is done by people, at the speed of documents.** These are agent skills.
They run where the work is, read from a shared system record, and produce artefacts that
survive an audit.

---

## What's in it

### Framework

| File | What it gives you |
|---|---|
| [`autonomy-tiers.md`](framework/autonomy-tiers.md) | A0–A4 autonomy × B0–B3 blast radius, the governance grid, and what each oversight level obliges |
| [`diagnostic-manual.md`](framework/diagnostic-manual.md) | 18 agent failure modes across six classes, with diagnostic criteria and controls |
| [`system-record.schema.json`](framework/system-record.schema.json) | The shared artefact every skill reads from and writes to |
| [`crosswalk.md`](framework/crosswalk.md) | EU AI Act ↔ NIST AI RMF ↔ ISO 42001 ↔ DORA, and where the agentic gap sits |

### Skills

| Skill | What it does |
|---|---|
| [`ai-system-intake`](skills/ai-system-intake/) | Builds the system record. Run this first — everything else reads from it |
| [`agent-autonomy-review`](skills/agent-autonomy-review/) | Tiers autonomy and blast radius, derives the oversight obligation, finds autonomy creep |
| [`agent-failure-diagnosis`](skills/agent-failure-diagnosis/) | Classifies why an agent misbehaved, from artefacts rather than narrative |
| [`eu-ai-act-triage`](skills/eu-ai-act-triage/) | Prohibited / high-risk / transparency / minimal, provider vs deployer, obligations with dates |
| [`nist-ai-rmf-assessment`](skills/nist-ai-rmf-assessment/) | GOVERN / MAP / MEASURE / MANAGE gap assessment with evidence |
| [`iso-42001-soa`](skills/iso-42001-soa/) | Clause conformity and the Statement of Applicability |
| [`ai-incident-triage`](skills/ai-incident-triage/) | Incident classification, harm assessment, and the reporting-clock call |
| [`evidence-pack`](skills/evidence-pack/) | Assembles audit-ready evidence and finds the claims that aren't evidenced |

---

## Install

Copy the skills you want into your skills directory:

```bash
git clone https://github.com/patkusch/remit.git
cp -r remit/skills/* ~/.claude/skills/
```

Or install one:

```bash
cp -r remit/skills/agent-autonomy-review ~/.claude/skills/
```

The skills reference `framework/` by relative path, so keep the repository structure
intact — clone it somewhere permanent and symlink, or copy `framework/` alongside.

---

## Using it

The skills are designed to be invoked by describing your situation, not by naming them.
"We're putting a model into the loan decisioning flow" should reach intake and EU AI Act
triage on its own.

A typical sequence:

```
1. Intake            → system record
2. Autonomy review   → tier, blast radius, oversight level      (if it takes actions)
3. EU AI Act triage  → classification and statutory obligations (legal duties first)
4. NIST or ISO       → framework assessment                     (whichever you need)
5. Evidence pack     → before the audit, not during
```

And when something goes wrong:

```
Incident triage → reporting clock first, then classification
       └── agent-failure-diagnosis → primary failure, severity, controls
```

---

## The two ideas worth stealing even if you don't use the skills

**Score the tier you actually run at.** If an approver has 400 approvals queued and
clicks through them in eleven seconds, you are running A3 with an A2 label. That gap is
the finding, and auditors treat a mislabelled tier far more harshly than an honestly
declared high one.

**Diagnose from artefacts, never from narrative.** An agent's account of why it did
something is evidence about `R1 post-hoc rationalisation` and is inadmissible for
everything else. Where self-report and trace conflict, the trace wins.

---

## Limits, stated plainly

**This is not legal advice.** The EU AI Act, ISO 42001, and DORA material here is a
structured triage to organise facts and surface the right questions. Classification turns
on specifics that reasonable people contest, and much of the detail sits in delegated
acts, harmonised standards, and guidance that continue to develop. Verify article
numbers, dates, and control text against current sources before relying on any of it, and
route real decisions to qualified counsel.

**The diagnostic manual is a working taxonomy, not a validated instrument.** Its
categories are not exhaustive, not mutually exclusive, and carry no field trial. They
earn their place if your incident records become more consistent than prose, and they
should be revised as your own data contradicts them.

**The clinical framing is a borrowed discipline for describing behaviour consistently.**
It is not a theory of machine minds, and it should never be used to imply that an agent's
failures are anything other than the responsibility of the people and organisations that
deployed it.

---

## Contributing

The most useful contributions are failure modes the diagnostic manual misses, and cases
where its criteria produced the wrong classification on real evidence. Open an issue with
the observation and, where you can share it, the artefacts.

## Licence

MIT — see [LICENSE](LICENSE).
