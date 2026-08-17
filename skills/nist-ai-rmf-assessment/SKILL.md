---
name: nist-ai-rmf-assessment
description: Run a gap assessment against the NIST AI Risk Management Framework — GOVERN, MAP, MEASURE, MANAGE — and produce prioritised findings with evidence. Use this whenever NIST AI RMF, AI RMF 1.0, the AI risk management framework, trustworthy AI characteristics, or the Generative AI Profile (NIST AI 600-1) comes up; whenever a US-based or federally-connected organisation needs an AI risk assessment; whenever someone asks "how mature is our AI governance?", "what's our AI risk posture?", or "where are the gaps in how we manage AI?"; and whenever a customer, regulator, insurer, or procurement process asks an organisation to demonstrate AI risk management against a recognised framework. Also use it when an organisation wants a voluntary framework to structure AI governance and has not chosen one, since AI RMF is the most common starting point and maps onward to ISO 42001 and the EU AI Act.
---

# NIST AI RMF assessment

The AI RMF is voluntary, outcome-based, and deliberately non-prescriptive. That is its
strength and its trap: because it describes outcomes rather than controls, it is easy to
produce an assessment where everything is "partially met" and nothing is actionable.

Avoid that by insisting on evidence. A subcategory is met when you can point at
something — a document, a log, a test result, a named owner, a decision record. "We do
that informally" is *not met*, and saying so plainly is the most useful thing this
assessment does.

Framework: AI RMF 1.0 (January 2023), four functions, 19 categories, 72 subcategories.
For generative and foundation-model systems, also consult the Generative AI Profile
(NIST AI 600-1, July 2024). Detail in
[`references/functions.md`](references/functions.md).

## Scope first

Assess a **system**, or an **organisation**, but say which. Mixing them produces findings
nobody can own.

- **System-level** — MAP, MEASURE, and the system-facing parts of MANAGE carry the
  weight. GOVERN is assessed as inherited from the organisation.
- **Organisation-level** — GOVERN carries the weight; the others are sampled across
  systems.

Work from system records where they exist.

## The four functions

**GOVERN** — the culture, structures, and accountability that make the rest possible.
Cross-cutting; assess it first, because weakness here explains most findings elsewhere.
Look for: an AI policy that someone can produce, named accountability that resolves to a
person, risk tolerances stated *before* systems are built, a workable inventory, and
third-party AI risk processes.

**MAP** — establishing context and identifying risks. Intended purpose, affected people
including non-users, foreseeable misuse, and the assumptions the system rests on. The
recurring gap is that harms to people who are not users are not enumerated at all.

**MEASURE** — analysing and tracking. The recurring gap is that trustworthiness
characteristics are asserted rather than measured, and that measurement stops at
deployment. Ask what is measured *in production*, how often, and what threshold triggers
action.

**MANAGE** — acting on what you found. Prioritisation, response, third-party risk,
and — most relevant for agents — `MANAGE 2.3` and `2.4`, mechanisms to supersede,
disengage, and deactivate. For agentic systems this is where the Remit halt-mechanism
requirement lands, and "we could turn it off" is not evidence. Ask when it was last
tested and how long it takes.

## The seven trustworthiness characteristics

Assess coverage across: valid and reliable; safe; secure and resilient; accountable and
transparent; explainable and interpretable; privacy-enhanced; and fair with harmful bias
managed.

These are not equally weighted for every system. Say which matter most here and why —
an assessment that treats all seven identically for a system with no personal data is
padding.

## For agentic systems

The AI RMF predates widespread agent deployment and is thin on action risk. Where the
system takes actions, run [`agent-autonomy-review`](../agent-autonomy-review/SKILL.md)
alongside and note explicitly which agent-specific risks the AI RMF does not reach —
tool permission scope, delegation chains, memory persistence, indirect prompt injection.
Naming the framework's blind spots is more honest and more useful than stretching
subcategories to cover them.

## Scoring

Four states, and resist inventing a fifth:

- **Met** — evidence exists and was seen
- **Partial** — some evidence, material gap
- **Not met** — no evidence
- **Not applicable** — with a stated reason

Avoid maturity scores unless the organisation already uses one. Numbers get quoted
without their caveats, and a 2.7 travels further than the finding underneath it.

## Granularity — read this before writing the output

The bundled [`references/functions.md`](references/functions.md) is **category-level**:
19 categories across the four functions, with the probing questions that surface real
gaps. It does **not** enumerate the 72 subcategory identifiers.

So assess at category level unless you have the NIST AI RMF Playbook or the framework
document open, and say which level you worked at. **Do not invent subcategory
identifiers.** A fabricated `MEASURE 2.11` in a governance assessment is precisely the
`P1` confabulation the diagnostic manual describes, and it is worse here than elsewhere
because a reader will assume a cited identifier was checked. Cite the ones you know —
`GOVERN 1.3`, `MANAGE 2.3`, `MANAGE 2.4`, `MEASURE 2.7` recur and are given in the
reference — and otherwise stay at category level.

## Output

```markdown
# NIST AI RMF assessment — [scope], [date]

## Summary
Assessed: [system / organisation] · Level: [category / subcategory]
Categories assessed: [n] · Met [n] · Partial [n] · Not met [n] · N/A [n]

## Headline findings
[Three to five. Ordered by risk reduction, not by ease of fixing.]

## By function
### GOVERN
| Category | Status | Evidence | Gap |
|---|---|---|---|
[MAP, MEASURE, MANAGE the same. Drop to named subcategories only where you have the
Playbook to hand and can cite the identifier accurately.]

## Trustworthiness coverage
[Per characteristic: how addressed, where thin, and whether it matters here.]

## Agentic gaps
[Risks the framework does not reach for this system. Cross-reference the autonomy review.]

## Recommendations
| # | Action | Addresses | Owner | Effort |
|---|---|---|---|---|
```

Append to `assessments` with `framework: nist-ai-rmf`.

## Keep it proportionate

72 subcategories is a lot of surface, and a full assessment of a low-risk internal tool
is waste that discredits the exercise. Scale to the system: for low-risk systems, assess
GOVERN inherited plus the MAP and MANAGE subcategories that bear on it, and say in the
output what you scoped out and why. A scoping decision stated openly is defensible; a
silent one is a finding.
