---
name: dora-ict-assessment
description: Assess an AI system or agent against DORA — the EU Digital Operational Resilience Act — covering the critical-or-important-function determination, ICT risk management, incident classification and reporting clocks, resilience testing, and ICT third-party risk. Use this whenever DORA, digital operational resilience, ICT risk, or Regulation 2022/2554 comes up, and whenever an AI system is deployed by an EU financial entity of any kind — bank, payment or e-money institution, investment firm, insurer, reinsurer, pension provider, crypto-asset service provider, credit rating agency, or trading venue. Trigger on "does DORA apply to this?", "is this a critical or important function?", "do we have to report this incident?", "what's in the register of information?", and on any AI system touching trading, payments, settlement, underwriting, claims, credit decisioning, customer onboarding, or the ICT that supports them. Use it alongside eu-ai-act-triage rather than instead of it: for many financial-sector AI systems the AI Act turns out not to bite while DORA does, and missing that is the most expensive error available in this sector.
---

# DORA assessment

Regulation (EU) 2022/2554. **Applicable since 17 January 2025** — no transition period
remaining, unlike the AI Act.

The reason this skill exists: for a great many AI systems in financial services, the EU
AI Act analysis comes back negative and everyone relaxes. DORA is frequently the regime
that actually binds, it is already live, and it reaches things the AI Act does not —
notably operational resilience, incident reporting on a four-hour clock, and third-party
concentration risk.

Run this **alongside** [`eu-ai-act-triage`](../eu-ai-act-triage/SKILL.md), not after it.
A negative AI Act finding is not an all-clear.

## 1. Is the entity in scope

DORA applies to some 20 categories of financial entity under Art. 2 — credit
institutions, payment and e-money institutions, investment firms, crypto-asset service
providers, insurers and reinsurers, pension institutions, credit rating agencies, trading
venues, central counterparties, and more — plus ICT third-party service providers serving
them.

If the organisation is not a financial entity, stop: DORA does not apply directly. But
ask whether they are an **ICT third-party provider to one**, in which case DORA reaches
them contractually through their financial-sector customers, and increasingly through
the CTPP oversight regime if they are designated critical.

Note the proportionality regime: certain smaller entities may use the simplified ICT risk
management framework under Art. 16. Establish which applies before assessing against the
full set.

## 2. Critical or important function — the pivot

Everything downstream scales off this determination, so make it explicitly and record the
reasoning.

A function is critical or important where a disruption would **materially impair** the
financial performance of the entity, or the soundness or continuity of its services and
activities, or where discontinuation would materially impair continued compliance with
the conditions of its authorisation.

For AI systems the useful framing is: *what breaks, and for whom, if this stops or does
the wrong thing?* An agent that triages internal IT tickets is unlikely to qualify. An
agent that touches payment processing, trade execution, settlement, underwriting,
sanctions screening, or the ICT that keeps those running very likely does — **including
where it is only "internal tooling"**, because DORA governs the ICT supporting the
function, not just customer-facing systems. That misconception is the most common way
firms under-scope an AI system here.

Record the outcome in `supply_chain.critical_or_important_function` on the system record.

## 3. The five pillars

Assess against each. Scale depth to the CIF determination — a non-CIF system does not
warrant the full apparatus, and saying so is part of the job.

**ICT risk management (Arts. 5–16).** A documented framework, governed by the management
body, which under Art. 5(2) bears final responsibility and cannot delegate it away.
Covers identification, protection and prevention, detection, response and recovery,
learning and evolving, and communication. For AI systems the questions that bite are:
is the system in the ICT asset inventory at all; are its dependencies mapped; and does
the detection capability actually cover *model* failure, or only infrastructure failure?
Most monitoring will tell you the agent is up, not that it is wrong.

**ICT incident management and reporting (Arts. 17–23).** Classification against criteria
in the RTS, then reporting on the clocks in section 4 below.

**Digital operational resilience testing (Arts. 24–27).** A testing programme
proportionate to risk, with threat-led penetration testing (TLPT) for entities so
designated. For agents this is where the halt mechanism and the injection-resistance
evidence live — and unlike the AI Act, DORA gives you a positive obligation to test them
rather than merely to have them.

**ICT third-party risk (Arts. 28–44).** The register of information, contractual
requirements, exit strategies, and concentration risk. If the AI system is built on a
third-party model or API, that supplier is an ICT third-party service provider and
belongs in the register. Model suppliers are routinely missed here because procurement
booked them as software licences rather than ICT services supporting a function.

**Information sharing (Arts. 45+).** Voluntary. Note it, do not labour it.

## 4. Incident reporting clocks

Ask this question early in any incident, because the clocks are short and start from
events that precede your investigation.

| Report | Deadline |
|---|---|
| Initial notification | Within **4 hours of classifying** the incident as major, and no later than **24 hours from becoming aware** |
| Intermediate report | Within **72 hours** of the initial notification |
| Final report | Within **1 month**, covering root cause, impact, and remediation |

The four-hour clock runs from **classification**, not detection — which makes the
classification decision itself time-critical, and makes "we were still investigating" a
poor answer. Significant cyber threats may be notified voluntarily.

Where an AI agent caused or contributed to the incident, run
[`ai-incident-triage`](../ai-incident-triage/SKILL.md) in parallel: DORA needs the
operational impact classification, and the Remit diagnosis gives you the mechanism and
the remediation that the final report will need.

## 5. What DORA reaches that the AI Act does not

Say this explicitly in the output, because it is usually the finding that changes
behaviour:

- **Resilience testing as a positive obligation.** The AI Act asks for robustness; DORA
  makes you test and evidence it on a programme.
- **Incident reporting for operational disruption**, regardless of whether any person's
  rights were affected — the AI Act's Art. 73 trigger is much narrower.
- **Third-party concentration risk.** Several agents on one model provider is a DORA
  concern and an AI Act non-issue.
- **Management body accountability** that cannot be delegated (Art. 5(2)).
- **Exit strategies.** What happens when the model provider changes the model under you,
  deprecates it, or fails.

## Output

```markdown
# DORA assessment — [system], [date]

## Scope
Entity type: [Art. 2 category] · Simplified framework (Art. 16): [yes/no]
**Critical or important function: [yes/no]** — [reasoning, explicitly]

## By pillar
| Pillar | Requirement | Status | Evidence | Gap |
|---|---|---|---|---|

## Incident readiness
Classification process: [exists / not established]
Can the 4-hour clock be met? [assessment, not assertion]

## ICT third-party
| Provider | Service | In register? | Supports CIF? | Exit strategy |
|---|---|---|---|---|

## What DORA catches here that the AI Act does not
[The point of running both.]

## Findings
[Ordered by risk reduction.]
```

Append to `assessments` with `framework: dora`.

## Limits

Not legal advice. DORA's detail sits substantially in regulatory technical standards and
implementing standards which continue to be issued and amended, and classification
thresholds in particular are RTS-driven. Verify against current ESA materials and your
own competent authority's guidance, and route real determinations — especially the
critical-or-important-function call and any major-incident classification — to the people
who own them.

*Legal content verified 17 August 2026. Re-check before relying on it.*
