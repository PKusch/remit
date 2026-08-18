# Annex III — high-risk areas

The eight areas. A system in one of these is high-risk **unless** the Art. 6(3)
derogation applies (see SKILL.md). Check against the sub-points, not the headline —
most missed classifications come from someone matching on the category name and
stopping.

Annex III is amendable by the Commission under Art. 7. Verify against the current
consolidated text before relying on this.

---

## 1. Biometrics

Where permitted under applicable law:

- **(a)** Remote biometric identification systems. Excludes systems used solely to
  confirm a person is who they claim to be (one-to-one verification, e.g. unlocking a
  phone).
- **(b)** Biometric categorisation according to sensitive or protected attributes, or
  attributes inferred from them.
- **(c)** Emotion recognition systems.

Note the overlap with Art. 5 prohibitions — emotion recognition in workplaces and
education is *prohibited*, not high-risk, outside narrow medical and safety exceptions.
Check prohibitions first.

## 2. Critical infrastructure

Safety components in the management and operation of critical digital infrastructure,
road traffic, or the supply of water, gas, heating, and electricity.

The qualifier is **safety component**. A model forecasting energy demand for commercial
purposes is not automatically in scope; one whose failure endangers supply is.

## 3. Education and vocational training

- **(a)** Determining access, admission, or assignment to institutions at all levels.
- **(b)** Evaluating learning outcomes, including where those outcomes steer the
  learning process.
- **(c)** Assessing the appropriate level of education a person will receive or access.
- **(d)** Monitoring and detecting prohibited behaviour during tests.

Proctoring software sits squarely in (d) and is regularly overlooked.

## 4. Employment, workers management, and access to self-employment

- **(a)** Recruitment or selection — in particular targeted job advertisements, analysing
  and filtering applications, and evaluating candidates.
- **(b)** Decisions affecting terms of work, promotion, or termination; allocating tasks
  based on individual behaviour or personal traits; and monitoring and evaluating
  performance and behaviour.

This is the broadest area in practice. CV screening, interview scoring, shift allocation
by behavioural profile, and productivity monitoring all land here. The 4(a) reference to
**targeted job advertising** catches systems teams rarely think of as HR tools at all.

## 5. Access to essential private and public services and benefits

- **(a)** Public authorities evaluating eligibility for essential public assistance
  benefits and services, including healthcare, and granting, reducing, revoking, or
  reclaiming them.
- **(b)** Evaluating **creditworthiness** or establishing credit score — excluding
  systems used to detect financial fraud.
- **(c)** Risk assessment and pricing in **life and health insurance**.
- **(d)** Evaluating and classifying emergency calls, and dispatch prioritisation of
  emergency services including police, fire, medical, and emergency triage.

For financial services this is the one that matters. Note the boundaries carefully: the
fraud-detection carve-out in (b) is narrow and does not cover a fraud model that in
substance drives credit decisions; and (c) covers life and health insurance
specifically — other lines are not listed here.

## 6. Law enforcement

Where permitted under applicable law:

- **(a)** Assessing the risk of a natural person becoming a victim of criminal offences.
- **(b)** Polygraphs and similar tools.
- **(c)** Evaluating the reliability of evidence in the course of investigation or
  prosecution.
- **(d)** Assessing the risk of offending or re-offending, other than on the basis of
  profiling alone — profiling-only predictive policing is *prohibited* under Art. 5(1)(d),
  not high-risk.
- **(e)** Profiling in the course of detection, investigation, or prosecution.

## 7. Migration, asylum, and border control management

Where permitted under applicable law:

- **(a)** Polygraphs and similar tools.
- **(b)** Assessing risks — including security, irregular migration, and health risks —
  posed by a person intending to enter or entering a Member State.
- **(c)** Assisting the examination of applications for asylum, visa, or residence permits
  and associated complaints regarding eligibility.
- **(d)** Detecting, recognising, or identifying natural persons, **excluding** the
  verification of travel documents.

## 8. Administration of justice and democratic processes

- **(a)** Assisting a judicial authority in researching and interpreting facts and law
  and applying the law, or used similarly in alternative dispute resolution.
- **(b)** Influencing the outcome of an election or referendum, or the voting behaviour
  of persons. Excludes outputs to which people are not directly exposed, such as tools
  used purely for administrative or logistical organisation of campaigns.

---

## Applying this well

**Match on function, not on department.** A model built by a marketing team that targets
job adverts is Annex III 4(a). Where a system sits on the org chart is irrelevant.

**Check the exclusions.** Several sub-points carry carve-outs — one-to-one biometric
verification, fraud detection, travel document verification, campaign logistics. These
are narrow and specific; do not widen them by analogy.

**Where a system spans several sub-points, cite all of them.** The obligations are the
same, but the record should show the full basis, and an assessment that names only one
route looks thin under review.

**Where you conclude a system is *not* in Annex III, write down why.** A negative
classification with no reasoning is the finding an auditor opens with.

---

<!-- staleness gate: scripts/check_staleness.py -->
**verified: 2026-08-18** — against sources current at that date. This file restates external law or standards, which move. Re-check before relying on it; re-verify before updating this date.
