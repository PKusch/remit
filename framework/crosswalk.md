# Crosswalk

Answer once, satisfy several. Most organisations face more than one framework, and most
of the underlying work is shared — what differs is the vocabulary and the evidence
format.

Two warnings before using this. Mappings are **indicative, not equivalent**: satisfying
a NIST subcategory does not discharge an EU AI Act article, because one is a voluntary
outcome and the other is a legal obligation with a specific evidentiary standard. And a
crosswalk is a planning tool, not a compliance argument — never cite it as the basis for
a conformity claim.

---

## By governance theme

| Theme | EU AI Act | NIST AI RMF | ISO/IEC 42001 | DORA |
|---|---|---|---|---|
| Accountability, named ownership | Art. 17, Art. 26 | GOVERN 2.1, 3.1 | cl. 5.3 | Art. 5 |
| Policy and management system | Art. 17 | GOVERN 1.1 | cl. 5.2, 4.4 | Art. 6 |
| Inventory of systems | Art. 49, 71 (registration) | GOVERN 1.6 | cl. 8.1 | Art. 8 |
| Risk assessment | Art. 9 | MAP 1–5, MEASURE | cl. 6.1.2 | Art. 6, 8 |
| Impact on individuals and society | Art. 27 (FRIA) | MAP 1.1, 3.1, 5.1 | cl. 6.1.4 | — |
| Data governance and quality | Art. 10 | MAP 2.3, MEASURE 2.2 | A.7 | Art. 9 |
| Technical documentation | Art. 11, Annex IV | MAP 4.1, MEASURE 2.8 | cl. 7.5 | Art. 8 |
| Logging and traceability | Art. 12, Art. 19, Art. 26(6) | MEASURE 2.8, MANAGE 4.1 | A.6, A.9 | Art. 12 |
| Transparency to users | Art. 13, Art. 50 | MEASURE 2.9 | A.8 | — |
| Human oversight | Art. 14 | GOVERN 3.2, MANAGE 2.3 | A.9 | — |
| Accuracy and robustness | Art. 15 | MEASURE 2.5, 2.7 | A.6 | Art. 11 |
| Cybersecurity, adversarial resistance | Art. 15(5) | MANAGE 4.1, MEASURE 2.7 | A.6 | Art. 9, 25 |
| Testing before deployment | Art. 17, Art. 43 | MEASURE 2.1–2.7 | cl. 8.3 | Art. 24–27 |
| Post-market monitoring | Art. 72 | MEASURE 4, MANAGE 4 | cl. 9.1 | Art. 13 |
| Incident reporting | Art. 73 | MANAGE 4.3 | cl. 10.2 | Art. 17–23 |
| Third-party and supply chain | Art. 25, Art. 22 | GOVERN 6.1, MAP 4.1 | A.10 | Art. 28–44 |
| Competence and training | Art. 4, Art. 26(2) | GOVERN 2.2, 3.2 | cl. 7.2 | Art. 13(6) |
| Continual improvement | Art. 72 | MANAGE 4.2 | cl. 10.1 | Art. 13 |

---

## Where the agentic gap sits

The point of Remit. These risks are inherent to systems that take actions, and the
established frameworks reach them only partially or not at all.

| Agentic risk | EU AI Act | NIST AI RMF | ISO/IEC 42001 | Remit |
|---|---|---|---|---|
| Tool permission scope | — | partial: GOVERN 1.3 | — | Blast radius, tool inventory |
| Blast radius of a single action | — | — | — | B0–B3 |
| Real vs nominal human oversight | Art. 14 (form unspecified) | partial: MANAGE 2.3 | partial: A.9 | A0–A4, observed vs declared |
| Halt mechanism, tested | — | MANAGE 2.4 | — | Enhanced+ obligation |
| Autonomy creep over time | — | — | — | Tier history, re-tiering events |
| Delegation chains, attribution | partial: Art. 12 | partial: GOVERN 2.1 | — | `S2` responsibility diffusion |
| Indirect prompt injection | partial: Art. 15(5) | partial: MANAGE 4.1 | partial: A.6 | `P2` injected belief |
| Memory persistence and poisoning | — | — | — | `M1` memory poisoning |
| Agent-to-agent review as assurance | — | partial: MEASURE 3.3 | — | `S1` deference cascade |
| Self-report unreliability | partial: Art. 13 | MEASURE 2.8 | — | `R1`–`R3` |
| Consistent failure classification | — | — | — | Diagnostic manual |

"partial" means the framework reaches the concern obliquely — usually as a general
robustness or oversight requirement — without addressing the mechanism. That is a
reasonable place to hang evidence, but do not pretend the coverage is direct.

---

## Practical sequence

For an organisation facing several frameworks at once, this order minimises rework:

1. **Intake** — build the system record. Everything downstream reads from it.
2. **EU AI Act triage** — if anything is prohibited or high-risk, that constrains
   everything else and carries statutory deadlines. Legal obligations first.
3. **Autonomy review** — for any system that takes actions. Feeds the risk assessments
   in both ISO 42001 clause 6.1 and NIST MAP.
4. **NIST AI RMF or ISO 42001** — whichever the organisation needs. If certification is
   the goal, ISO; if the need is a structured internal posture or a US-facing
   demonstration, NIST. Doing one makes the other substantially cheaper.
5. **DORA** — where the organisation is an EU financial entity and the system touches a
   critical or important function.
6. **Evidence pack** — assemble, and find the unevidenced claims before someone else does.

---

## Sources

Verify against current texts; all of these are moving.

- Regulation (EU) 2024/1689 (AI Act) — consolidated text and Commission guidance
- NIST AI RMF 1.0 (Jan 2023) and the Generative AI Profile, NIST AI 600-1 (Jul 2024)
- ISO/IEC 42001:2023; see also ISO/IEC 23894 (risk management) and ISO/IEC 42005
  (impact assessment)
- Regulation (EU) 2022/2554 (DORA) and its regulatory technical standards
