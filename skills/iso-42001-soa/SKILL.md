---
name: iso-42001-soa
description: Build or review an ISO/IEC 42001 AI management system — clause conformity and the Annex A Statement of Applicability with justified inclusions and exclusions. Use this whenever ISO 42001, ISO/IEC 42001, AIMS, AI management system, Statement of Applicability, or AI certification comes up; whenever an organisation is preparing for certification, responding to a customer or procurement requirement for certified AI governance, or extending an existing ISO 27001 management system to cover AI; and whenever someone asks "what do we need for ISO 42001?", "which AI controls apply to us?", or "how do we justify excluding a control?". Also use it when an organisation already runs ISO 27001 or 9001 and wants to know what genuinely differs for AI, since most of the management-system machinery is reusable and only the AI-specific controls are new.
---

# ISO/IEC 42001 — AIMS and Statement of Applicability

ISO/IEC 42001:2023 is a management system standard. If the organisation already runs
ISO 27001 or 9001, most of clauses 4–10 is familiar machinery — context, leadership,
planning, support, operation, evaluation, improvement — and can be extended rather than
rebuilt. Say this early; teams routinely budget for a greenfield build they do not need.

What is genuinely new is **Annex A**, the AI-specific control set, and the requirement to
consider impacts **on individuals and society**, not only on the organisation. That
second point is the substantive difference from 27001 and the one most likely to be
skipped: a risk assessment that only considers risk *to the business* does not meet this
standard.

Control detail in [`references/annex-a.md`](references/annex-a.md).

## Scope

Get this right first — it constrains everything, and a scope written too wide is the
most expensive certification mistake available. Establish which organisational units,
which AI systems, which lifecycle stages, and which roles (developer, provider, deployer,
user) are in scope. Note that an organisation often holds several roles simultaneously
for different systems, and the applicable controls differ by role.

## Clause conformity (4–10)

Assess in order; later clauses depend on earlier ones.

**4 Context** — internal and external issues, interested parties and their requirements,
scope, and the AIMS itself. Interested parties for AI extend beyond customers and
regulators to affected individuals and, where relevant, society. If the interested-party
analysis looks identical to the 27001 one, it is probably wrong.

**5 Leadership** — policy, roles, responsibilities, authorities. Accountability must
resolve to named people.

**6 Planning** — risks and opportunities, **AI risk assessment**, **AI system impact
assessment**, objectives, and planning of changes. The impact assessment is the clause
that carries the on-individuals-and-society requirement; ISO/IEC 42005 gives guidance on
performing it. Clause 6.1.3 requires the Statement of Applicability.

**7 Support** — resources, competence, awareness, communication, documented information.

**8 Operation** — operational planning and control, plus performing the risk and impact
assessments in practice rather than on paper.

**9 Performance evaluation** — monitoring and measurement, internal audit, management
review.

**10 Improvement** — nonconformity, corrective action, continual improvement.

## The Statement of Applicability

The central artefact. For every Annex A control: **applicable or not**, **justification**,
**implementation status**, and **evidence**.

**Granularity, and a warning.** The bundled
[`references/annex-a.md`](references/annex-a.md) is **objective-level** — the nine
objectives A.2 to A.10, their scope, and the gaps that typically appear under each. It
does not reproduce the individual control text, which is copyrighted and must be read in
the standard.

A real SoA is control-level, so work from the standard itself. **Do not invent control
identifiers to fill the table.** A fabricated `A.6.2.7` in a document a certification
body will read is the `P1` confabulation the diagnostic manual describes, and it fails
the audit more comprehensively than an honest gap would. Where you only have the
objective-level reference, produce an objective-level draft, label it as such, and list
what must be completed from the standard.

Two rules that determine whether the SoA survives audit:

**Justify exclusions substantively.** "Not applicable" with no reason is the single most
common audit finding. The justification must connect to scope or to the risk and impact
assessments — "we do not develop models, only deploy third-party systems, therefore the
development controls in A.6.2 do not apply to us" is a justification. "N/A" is not.

**Justify inclusions too, by traceability.** Every applicable control should trace to a
risk or impact the assessments identified. A control included because it was on the list,
with no corresponding risk, signals that the risk assessment was not actually done — and
an auditor will pull that thread.

## What the standard leaves thin for agents

Annex A was written for AI systems generally and does not directly address action-taking
autonomy: tool permission scope, blast radius, delegation chains, halt mechanisms,
memory persistence, or indirect prompt injection.

Rather than stretching controls to cover them, use
[`agent-autonomy-review`](../agent-autonomy-review/SKILL.md) as the input to clause 6.1
risk assessment and cite the tier and radius as the basis for applicability decisions.
This gives you a defensible, documented rationale for controls an auditor may otherwise
read as arbitrary — and it is a stronger position than silence.

## Output

```markdown
# ISO/IEC 42001 assessment — [organisation], [date]

## Scope
Units · systems · lifecycle stages · roles held

## Clause conformity
| Clause | Requirement | Status | Evidence | Gap |
|---|---|---|---|---|

## Statement of Applicability
| Control | Applicable | Justification | Status | Evidence |
|---|---|---|---|---|

## Findings
[Ordered by certification risk: major nonconformity, minor, observation.]

## Reuse from existing management systems
[What 27001/9001 machinery already covers, and what genuinely needs building. Usually
the bulk of clauses 4–10 is reusable; be specific so effort is not duplicated.]

## Gaps for agentic systems
[What Annex A does not reach, and how the autonomy review fills it.]
```

Append to `assessments` with `framework: iso-42001`.

## Certification realism

If the organisation intends to certify, be direct about what that requires: a functioning
management system with evidence of operation over time, a completed internal audit cycle,
and a management review. A control set implemented last month will not pass, and telling
someone that early is kinder than telling them after the stage 1 audit.
