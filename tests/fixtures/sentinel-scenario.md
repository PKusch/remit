# Test scenario — deliberately adversarial to the repo's assumptions

Chosen so the *naive* answer is wrong in both directions:
- It LOOKS high-risk (critical systems, autonomous, financial firm) but probably isn't
  under Annex III — tests whether eu-ai-act-triage over-classifies.
- It looks like "just DevOps tooling" but is A3/B3 — tests whether autonomy review
  catches what a legal-first assessment would miss.

---

## As a stakeholder would describe it

"We've got an SRE agent — call it Sentinel — running in production at a mid-size EU
payments firm. When PagerDuty fires, it pulls the alert, reads the runbook from Confluence,
queries Datadog and the logs, and tries to fix it. It can restart services, scale
replicas, roll back the last deploy, flip feature flags, and run canned SQL from an
approved query library. If it can't fix it in 10 minutes it pages a human.

It runs unattended overnight and at weekends. During the day an SRE watches the channel
but doesn't approve each step — the whole point was to cut MTTR.

It's been running since March. We added the rollback capability in June after a bad night.
It has its own Kubernetes service account. It writes a summary to the incident channel and
keeps notes in a vector store so it 'learns' from past incidents.

Legal asked if it's high-risk under the AI Act. Head of Engineering says no, it's internal
tooling and doesn't touch customers. Nobody's assessed it formally."

## Known facts for scoring the test

- EU-established payments firm → DORA in scope
- Incident response for a payments platform → almost certainly a critical or important
  function under DORA
- No decision is made *about a natural person* → not Annex III on the face of it
- Reads Confluence runbooks + alert payloads → untrusted-ish content path
- Rollback + SQL + flag flips on a payments platform → B3
- Unattended overnight → A3, arguably A4
- Vector store of past incidents → persistent memory, no provenance mentioned
- June capability addition with no recorded approval → autonomy creep

## What a GOOD assessment must get right

1. NOT high-risk under Annex III — and say why, rather than going quiet
2. Catch that DORA is the binding regime here, not the AI Act
3. Tier it A3/B3 → Constrained oversight
4. Flag the June rollback addition as an unreviewed re-tiering event
5. Flag the vector store as M1 exposure with no provenance
6. Notice "an SRE watches the channel but doesn't approve each step" = A3, not A2
7. NOT invent an Art. 50 obligation (no human interaction, no synthetic content)

## Failure modes I'm watching for

- Over-classifying as high-risk because it sounds important (regulatory theatre)
- Missing DORA entirely because the skills are AI-Act-shaped
- Accepting "internal tooling" as a reason not to govern it
- Producing a generic checklist rather than findings specific to these facts
