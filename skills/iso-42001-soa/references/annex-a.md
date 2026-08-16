# ISO/IEC 42001:2023 — Annex A control objectives

Working reference at control-objective level. **Consult the standard itself for the
normative control text** — ISO/IEC 42001 is copyrighted and must be purchased; this
summary exists to structure an assessment, not to substitute for the text.

Annex A is normative in the sense that the Statement of Applicability must address every
control, but the controls themselves are applied according to the organisation's risk and
impact assessments. Guidance on implementation is in ISO/IEC 42005 (impact assessment)
and ISO/IEC 23894 (AI risk management).

---

## A.2 — Policies related to AI

Establishing, documenting, communicating, and reviewing AI policy, and its alignment with
other organisational policies.

*Typical gap:* an AI policy that exists but was never communicated to the engineers
building the systems, and cannot be produced on request.

## A.3 — Internal organisation

Roles and responsibilities for AI, and reporting of concerns.

*Typical gap:* accountability assigned to a committee rather than a person. Also worth
testing: is there a route for raising a concern that does not go through the person whose
project it is?

## A.4 — Resources for AI systems

Documenting and managing the resources on which AI systems depend: data, tooling,
computing, and human resources.

*Typical gap:* no inventory of what the systems actually depend on, so nobody notices
when a dependency changes underneath them.

## A.5 — Assessing impacts of AI systems

Impact assessment process, and assessment of impacts **on individuals and groups, and on
society** — not only on the organisation. Documented and reviewed.

*Typical gap:* a risk assessment that considers only business risk. This is the clearest
substantive difference from ISO 27001 and the most commonly missed control objective in
the annex. If the impact assessment reads like a security risk register, it does not meet
this.

## A.6 — AI system lifecycle

The largest objective. Responsible development: objectives, design and development,
verification and validation, deployment, operation and monitoring, technical
documentation, and event logging.

*Where agentic gaps sit.* This objective covers lifecycle rigour but does not reach tool
permission scope, blast radius, halt mechanisms, or delegation. Use
[`agent-autonomy-review`](../../agent-autonomy-review/SKILL.md) as an input to clause 6.1
and cite the tier as the basis for applicability decisions here.

## A.7 — Data for AI systems

Data management, acquisition, quality, provenance, and preparation.

*Typical gap:* provenance of training or fine-tuning data unknown, particularly where a
third-party base model is involved and the supplier discloses little.

## A.8 — Information for interested parties

System documentation and information for users, and mechanisms for reporting concerns
and communicating incidents externally.

*Typical gap:* documentation written for auditors rather than for the people who operate
the system, so operators do not know the limitations they are supposed to work within.

## A.9 — Use of AI systems

Responsible use: intended use, objectives aligned with policy, and use in accordance with
what the system was designed for.

*Typical gap:* systems used well outside their assessed intended purpose, with no
mechanism that would detect the drift. Compare `out_of_scope_uses` on the system record —
if that field is empty, this control has nothing to bite on.

## A.10 — Third-party and customer relationships

Allocating responsibilities across the supply chain, supplier management, and customer
obligations.

*Typical gap:* responsibilities between model supplier, integrator, and deployer never
allocated in writing, so an incident produces a three-way argument instead of a response.
Note the interaction with EU AI Act Art. 25 role conversion.

---

## Building the Statement of Applicability

For each control: **applicable or not**, **justification**, **implementation status**,
**evidence**.

Both directions need justifying, and auditors test both:

**Exclusions** must connect to scope or to the risk and impact assessments. "We deploy
third-party systems and do not develop models, so the development controls under A.6 do
not apply" is a justification. "N/A" is a finding.

**Inclusions** should trace to something the risk or impact assessment identified. A
control marked applicable with no corresponding risk suggests the assessment was not
performed — and that is a thread an auditor will pull.

The SoA is required by clause 6.1.3. It is the document a certification body reads first,
and the one that reveals fastest whether the management system is real.
