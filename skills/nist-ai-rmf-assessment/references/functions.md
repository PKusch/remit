# NIST AI RMF 1.0 — functions and categories

Reference for assessment. AI RMF 1.0 (January 2023): four functions, 19 categories,
72 subcategories. This is a working summary at category level with the assessment
questions that tend to surface real gaps — consult the NIST AI RMF Playbook for the full
subcategory text before finalising an assessment.

---

## GOVERN — culture, structures, accountability

Cross-cutting. Assess first; weakness here usually explains findings everywhere else.

| Cat | Concern | Ask |
|---|---|---|
| 1 | Policies, processes, procedures | Can someone produce the AI policy? When was it last reviewed? Are risk tolerances stated *before* systems are built? |
| 2 | Accountability structures | Does accountability resolve to a named person? Do they have authority to stop a deployment? |
| 3 | Workforce diversity, equity, inclusion, accessibility | Who is in the room when risks are identified? Are affected communities represented anywhere? |
| 4 | Culture of risk awareness | Is raising a concern rewarded or costly? What happened the last time someone did? |
| 5 | Engagement with affected communities | Is there any mechanism for affected people to be heard, and has it ever changed anything? |
| 6 | Third-party AI risk | How are acquired models, APIs, and datasets assessed? What happens when a supplier changes a model under you? |

`GOVERN 1.3` — risk-tiered processes — is where the Remit governance grid attaches.

## MAP — context and risk identification

| Cat | Concern | Ask |
|---|---|---|
| 1 | Context established | Intended purpose, setting, and norms documented? Are the assumptions written down anywhere? |
| 2 | Categorisation | Task, method, and system boundaries clear? What is *not* in the system? |
| 3 | Capabilities, targets, costs | What is the benefit, to whom, measured how? What is the cost of being wrong? |
| 4 | Risks and benefits mapped | Including for third-party components |
| 5 | Impacts characterised | **Impacts on people who are not users** — the most commonly empty category in real assessments |

Probe foreseeable misuse explicitly. Teams document intended use thoroughly and misuse
barely at all.

## MEASURE — analysis and tracking

| Cat | Concern | Ask |
|---|---|---|
| 1 | Methods and metrics identified | Are the trustworthiness characteristics actually measured, or asserted? |
| 2 | Systems evaluated for trustworthy characteristics | Includes validity, safety, security, privacy, fairness, explainability |
| 3 | Mechanisms for tracking risks | Who watches, how often, what threshold triggers action? |
| 4 | Feedback on measurement efficacy | Are the metrics still the right ones? Who checks? |

The recurring finding: measurement stops at deployment. Ask what is measured **in
production**, at what cadence, and what happens when it moves.

`MEASURE 2.7` (security and resilience) is where prompt injection testing belongs for
agentic systems. `MEASURE 2.8` (transparency and accountability of the system's
behaviour) is where trace-based evidence belongs — see `R1` in the diagnostic manual on
why self-report will not do.

## MANAGE — acting on what you found

| Cat | Concern | Ask |
|---|---|---|
| 1 | Risks prioritised and acted on | Is there a decision record, and did anything change as a result? |
| 2 | Strategies to maximise benefit, minimise harm | Includes `2.3` supersede/disengage and `2.4` deactivate |
| 3 | Third-party risks managed | |
| 4 | Monitoring, feedback, communication | Includes incident response and recovery |

**`MANAGE 2.3` and `2.4` are the agentic crux.** For any system that takes actions, this
is where the halt mechanism lives. "We could turn it off" is not evidence. Ask when it
was last tested, how long it takes to take effect, and who is authorised to trigger it at
3am.

---

## The seven trustworthiness characteristics

Assess coverage, and say which matter most for this system rather than treating all
seven as equally weighted:

1. **Valid and reliable** — does it work, demonstrably, on the population it will meet?
2. **Safe** — does it avoid endangering life, health, property, environment?
3. **Secure and resilient** — does it withstand adversarial conditions and degrade
   gracefully?
4. **Accountable and transparent** — can decisions be traced to a responsible party?
5. **Explainable and interpretable** — can the mechanism and the output be understood by
   those who need to?
6. **Privacy-enhanced** — does it protect anonymity, confidentiality, and control?
7. **Fair, with harmful bias managed** — across systemic, computational, and
   human-cognitive bias.

---

## Generative AI Profile (NIST AI 600-1, July 2024)

For generative and foundation-model systems, consult the profile. It identifies risks
including confabulation, dangerous or violent recommendations, data privacy, harmful bias
and homogenisation, human-AI configuration, information integrity, information security,
intellectual property, obscene content, value chain and component integration, and CBRN
information.

Two of these map directly onto diagnostic-manual entries and are worth assessing together:
**confabulation** with `P1`, and **human-AI configuration** with `P4` and `S1`.

---

## Assessment discipline

Insist on evidence. The framework is outcome-based and non-prescriptive, which makes it
easy to write an assessment where everything is "partial" and nothing is actionable.

A subcategory is **met** when you can point at an artefact. "We do that informally" is
**not met**. Recording that honestly is the most useful thing the assessment does — and
it is what makes the second assessment, a year later, show real movement.
