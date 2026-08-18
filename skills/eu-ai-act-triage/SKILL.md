---
name: eu-ai-act-triage
description: Classify an AI system under the EU AI Act — prohibited, high-risk, transparency-only, or minimal — establish whether the organisation is provider or deployer, and produce the resulting obligation set with dates. Use this whenever the EU AI Act, AI Act, Regulation 2024/1689, Annex III, high-risk AI, GPAI, or AI conformity assessment comes up; whenever someone asks "is this high-risk?", "does the AI Act apply to us?", "what do we have to do for this AI system?", or "are we a provider or a deployer?"; and whenever an AI system touches employment, recruitment, credit or creditworthiness, insurance pricing, education, essential public or private services, biometrics, emotion recognition, critical infrastructure, law enforcement, migration, or the administration of justice, since those are the Annex III areas where high-risk classification is most often missed. Also use it when an organisation is fine-tuning, rebranding, or materially modifying a third-party AI system, because that can silently convert a deployer into a provider with far heavier obligations.
---

# EU AI Act triage

Produces a defensible classification and the obligations that follow. It does not
produce legal advice, and the output should say so — see **Limits** at the end, which is
not boilerplate you can drop.

Work from a system record where one exists (see
[`ai-system-intake`](../ai-system-intake/SKILL.md)). If none exists, gather the same
facts first; classification without the facts is guesswork with a citation attached.

## The order matters

Run these in sequence. Each step can terminate the analysis, and running them out of
order produces confident wrong answers.

### 1. Territorial scope (Art. 2)

Does the Act reach this system at all? It applies to providers placing systems on the EU
market or putting them into service in the EU **regardless of where the provider is
established**, to deployers established or located in the EU, and to providers and
deployers in third countries where the **output is used in the EU**.

That last limb catches organisations that assume they are out of scope because they are
not in Europe. Ask where the output lands, not where the company is.

Note the carve-outs: national security and military purposes, purely personal
non-professional use, and systems released under free and open-source licences except
where they are prohibited, high-risk, or subject to Art. 50 transparency duties.

### 2. Is it an AI system at all (Art. 3(1))

Machine-based, designed to operate with varying levels of autonomy, may exhibit
adaptiveness, and infers from input how to generate outputs. Deterministic rules-based
software is generally outside this. Do not stretch the definition to include a
spreadsheet, and do not let someone shrink it to exclude a model because they call it
"just statistics."

### 3. Prohibited practices (Art. 5)

Applicable since **2 February 2025**. Check before anything else, because nothing
downstream matters if the practice is banned. Read
[`references/prohibitions.md`](references/prohibitions.md).

If a system plausibly falls here, stop and escalate to legal immediately. Do not
continue to a high-risk assessment as though the question were one of degree.

### 4. Role in the supply chain (Arts. 2, 3, 22–27)

Provider, deployer, importer, distributor, or product manufacturer. Obligations attach to
roles, and the heavy ones sit with providers.

Most organisations are deployers. But **Art. 25** converts a deployer into a provider
where they put their name or trademark on a high-risk system, make a substantial
modification to it, or modify its intended purpose such that it becomes high-risk. Ask
directly about fine-tuning, rebranding, and repurposing — this is among the most common
and most expensive misclassifications in practice.

### 5. High-risk classification (Art. 6, Annexes I and III)

Two routes in:

- **Annex I** — the system is a safety component of a product, or is itself a product,
  covered by listed EU harmonisation legislation requiring third-party conformity
  assessment (machinery, medical devices, toys, lifts, vehicles and so on).
- **Annex III** — the system falls in one of the eight listed areas. Read
  [`references/annex-iii.md`](references/annex-iii.md) and check against the actual
  sub-points, not your memory of the categories.

**Then apply the Art. 6(3) filter.** An Annex III system is *not* high-risk if it does not
pose a significant risk of harm to health, safety, or fundamental rights, because it:
performs a narrow procedural task; improves the result of a previously completed human
activity; detects decision-making patterns or deviations without replacing or influencing
the human assessment; or performs a preparatory task.

Two things to hold onto here. First, the derogation never applies where the system
performs **profiling of natural persons** — that is a hard stop. Second, a provider
relying on the derogation must **document that assessment before placing on the market**
and register the system. The derogation is a documented position, not a silent one, and
treating it as a way to avoid paperwork misunderstands it.

Be sceptical of derogation claims where `decision_consequence` on the system record is
`determines-outcome`, or where the human reviewer cannot realistically dissent. See the
`agent-autonomy-review` skill's treatment of nominal-versus-real oversight; the same
scepticism applies here.

### 6. Transparency obligations (Art. 50)

These apply **independently of risk tier** and are routinely missed on systems that are
otherwise minimal-risk:

- Systems interacting directly with people must make clear a person is dealing with AI,
  unless obvious from context.
- Synthetic audio, image, video, or text must be marked machine-readably as artificially
  generated or manipulated.
- Deep fakes must be disclosed as such.
- Emotion recognition and biometric categorisation systems must inform exposed persons.
- Text published to inform the public on matters of public interest must be disclosed as
  AI-generated where not subject to human editorial review.

Applicable from **2 August 2026 — these were deliberately excluded from the Omnibus
deferral.** Generative systems already on the market before that date have until
**2 December 2026** for the Art. 50(2) machine-readable marking requirement.

This is now the nearest live AI Act deadline for most organisations, and it applies
regardless of risk tier. A system that is otherwise minimal-risk can still owe
transparency duties, which is why this step runs independently of the high-risk analysis
rather than after it.

### 7. GPAI (Chapter V)

If the organisation develops or substantially modifies a general-purpose AI model,
separate obligations attach: technical documentation, information for downstream
providers, a copyright policy, and a public summary of training content. Models presenting
**systemic risk** carry more — evaluation, adversarial testing, incident tracking,
cybersecurity. Applicable since **2 August 2025**.

Deployers of somebody else's GPAI do not inherit these. Providers building on one may.

### 8. A negative finding is not an all-clear

If the organisation is an **EU financial entity** — bank, payment or e-money institution,
investment firm, insurer, pension provider, crypto-asset service provider, trading venue —
run [`dora-ict-assessment`](../dora-ict-assessment/SKILL.md) before concluding. DORA has
applied since January 2025 with no transition remaining, and it reaches operational
resilience, four-hour incident reporting, and third-party concentration risk that the AI
Act does not touch at all.

This is the most expensive miss available in financial services: the AI Act analysis
comes back negative, everyone relaxes, and the regime that actually binds was never
assessed. Where the system takes actions, also run
[`agent-autonomy-review`](../agent-autonomy-review/SKILL.md) — a system outside Annex III
can still be an A3/B3 agent needing constrained oversight.

Say plainly in the output which regimes you assessed and which you did not. A triage that
is silent about DORA reads as a clearance it never gave.

## Dates

> **The Digital Omnibus on AI entered into force on 27 July 2026 and deferred the
> high-risk deadlines.** Much published guidance — and many internal compliance
> calendars — still carries the original 2 August 2026 date for Annex III. Check which
> vintage you are reading before relying on it.

Cite these when stating obligations, since half of the practical question is *by when*:

| Date | What applies |
|---|---|
| 1 Aug 2024 | Entry into force |
| 2 Feb 2025 | Prohibitions (Art. 5) and AI literacy (Art. 4) |
| 2 Aug 2025 | GPAI obligations, governance bodies, penalties |
| 2 Aug 2026 | General application · **Art. 50 transparency — NOT deferred** · AI Office enforcement powers · governance bodies operational |
| 2 Dec 2026 | New prohibitions: non-consensual intimate imagery and CSAM generation · Art. 50(2) machine-readable marking for generative systems already on the market before 2 Aug 2026 |
| 2 Aug 2027 | Member State AI regulatory sandboxes (deferred from 2 Aug 2026) |
| **2 Dec 2027** | **Annex III high-risk — deferred from 2 Aug 2026** |
| **2 Aug 2028** | **Annex I high-risk — deferred from 2 Aug 2027** |
| 2 Aug 2030 | High-risk systems already in use by public authorities |

**What the Omnibus did *not* touch**, and where most of the live risk therefore sits:
the Art. 5 prohibitions and Art. 4 AI literacy (in force since Feb 2025), the GPAI
obligations (since Aug 2025), and Art. 50 transparency (2 Aug 2026). A common error
right now is to tell a client "nothing applies until December 2027" — the transparency
duties are live and the prohibitions have been for over a year.

The Omnibus also refined the "safety component" definition to prevent overclassification,
moved machinery products to a lower-risk classification, and reinstated a strict-necessity
threshold for processing special-category data in bias detection under Art. 10(5).

*Verified 17 August 2026 against post-Omnibus sources. Re-check before relying on it —
this area has moved twice in a year.*

## Obligations

Once classified, produce the obligation set from
[`references/obligations.md`](references/obligations.md), split by role. Do not hand
someone a generic list of articles: give them the obligations that attach to *their* role
for *their* classification, with the article reference and the date.

## Output

```markdown
# EU AI Act triage — [system], [date]

## Classification
**[Prohibited / High-risk / Transparency obligations only / Minimal risk]**
Route: [Annex III 5(b) / Annex I / n/a]
Role: **[Provider / Deployer / ...]** — [note Art. 25 if relevant]
Confidence: [high/medium/low]

## Reasoning
[Each step, with the article, and the facts relied on. Show the Art. 6(3) analysis
explicitly where an Annex III area was engaged — including why the derogation was or
was not available.]

## Obligations
| Obligation | Article | Applies from | Status | Gap |
|---|---|---|---|---|

## Facts this turns on
[The two or three findings that would change the classification if wrong. Whoever
reviews this should check these first.]

## Escalate to legal
[Yes/no, and why. Always yes for prohibited-practice candidates, Art. 25 role
conversion, and any Art. 6(3) derogation being relied on.]
```

Append to `assessments` on the system record with `framework: eu-ai-act`.

## Limits

State these in the output, not just here:

This is a structured triage to organise facts and surface the right questions. It is
**not legal advice** and does not substitute for qualified counsel. Classification under
the Act turns on specifics — intended purpose, deployment context, the substance of human
oversight — that reasonable people contest, and much of the detail sits in delegated
acts, harmonised standards, and Commission guidance that continue to develop.

Where confidence is medium or low, say what would raise it. Where the answer depends on
guidance not yet issued, say that too rather than manufacturing certainty. A triage that
honestly flags three open questions is more useful, and far safer, than one that answers
them by assumption.

---

<!-- staleness gate: scripts/check_staleness.py -->
**verified: 2026-08-17** — against sources current at that date. This file restates external law or standards, which move. Re-check before relying on it; re-verify before updating this date.
