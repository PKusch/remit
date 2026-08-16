# Obligations by role and classification

Hand people the obligations that attach to *their* role for *their* classification, with
the article and the date. A generic list of articles is not an output anyone can act on.

---

## High-risk — provider obligations

The heavy set. Chapter III, Section 2 states the requirements for the system; Section 3
states the provider's duties.

| # | Obligation | Article | What it means in practice |
|---|---|---|---|
| 1 | Risk management system | Art. 9 | Continuous, iterative across the lifecycle — not a one-off assessment. Must consider reasonably foreseeable misuse. |
| 2 | Data and data governance | Art. 10 | Training, validation, and test sets relevant, sufficiently representative, and to the extent possible free of errors and complete. Art. 10(5) permits processing special-category data for bias detection under conditions. |
| 3 | Technical documentation | Art. 11, Annex IV | Drawn up **before** placing on the market and kept up to date. Annex IV sets the contents. |
| 4 | Record-keeping / logging | Art. 12 | Automatic recording of events over the lifetime, enabling traceability. |
| 5 | Transparency and information to deployers | Art. 13 | Instructions for use with characteristics, capabilities, limitations, and required oversight measures. |
| 6 | Human oversight | Art. 14 | Designed so that oversight is *effective* — including the ability to interpret output, override, and stop. Design-time obligation, not a process bolted on later. |
| 7 | Accuracy, robustness, cybersecurity | Art. 15 | Declared accuracy metrics; resilience to errors and adversarial manipulation, including data poisoning and adversarial examples. |
| 8 | Quality management system | Art. 17 | Documented, covering the full lifecycle including post-market. |
| 9 | Documentation retention | Art. 18 | Generally 10 years after placing on the market. |
| 10 | Automatically generated logs | Art. 19 | Retained where under the provider's control, generally at least 6 months. |
| 11 | Corrective actions and duty to inform | Art. 20 | Withdraw, disable, or recall where non-conforming; inform distributors and authorities. |
| 12 | Cooperation with authorities | Art. 21 | On request, provide all information and documentation. |
| 13 | Authorised representative | Art. 22 | Required for providers established outside the EU. |
| 14 | Conformity assessment | Art. 43 | Route depends on the Annex. Most Annex III systems allow internal control (Annex VI); biometrics may require a notified body. |
| 15 | EU declaration of conformity, CE marking | Arts. 47, 48 | |
| 16 | Registration in the EU database | Arts. 49, 71 | Before placing on the market. Also required where a provider relies on the Art. 6(3) derogation. |
| 17 | Serious incident reporting | Art. 73 | See timings below. |
| 18 | Post-market monitoring | Art. 72 | A documented plan, proportionate to risk. |

## High-risk — deployer obligations

Lighter, and frequently underestimated because "we just use it."

| # | Obligation | Article |
|---|---|---|
| 1 | Use in accordance with instructions for use | Art. 26(1) |
| 2 | Assign human oversight to people with competence, training, authority, and support | Art. 26(2) |
| 3 | Ensure input data is relevant and sufficiently representative for the intended purpose, so far as the deployer controls it | Art. 26(4) |
| 4 | Monitor operation; suspend use and inform the provider where risk arises | Art. 26(5) |
| 5 | Keep automatically generated logs, generally at least 6 months | Art. 26(6) |
| 6 | Inform workers' representatives and affected workers before putting into service in the workplace | Art. 26(7) |
| 7 | Public authorities: register in the EU database | Art. 26(8) |
| 8 | Where used for decisions about natural persons, inform them that they are subject to the system | Art. 26(11) |
| 9 | Cooperate with authorities | Art. 26(12) |
| 10 | **Fundamental rights impact assessment (FRIA)** — before first use | Art. 27 |
| 11 | Explanation of individual decision-making, on request from an affected person | Art. 86 |

**Art. 27 FRIA scope.** Required for deployers that are bodies governed by public law, or
private entities providing public services, and for deployers of Annex III 5(b)
creditworthiness and 5(c) life and health insurance pricing systems. That last limb puts
FRIA squarely on ordinary financial services firms, and it is the deployer obligation most
often missed.

**Art. 25 conversion.** A deployer becomes a provider — inheriting the entire table above
— where it puts its name or trademark on the system, substantially modifies it, or
modifies the intended purpose such that it becomes high-risk.

---

## Transparency obligations (Art. 50)

Independent of risk tier. Applicable **2 August 2026**.

| Who | Obligation |
|---|---|
| Providers of systems interacting with people | Inform the person they are interacting with AI, unless obvious in context |
| Providers of generative systems | Mark synthetic audio/image/video/text in a machine-readable format as artificially generated or manipulated |
| Deployers of emotion recognition or biometric categorisation | Inform exposed persons, and process personal data accordingly |
| Deployers producing deep fakes | Disclose that the content is artificially generated or manipulated |
| Deployers publishing AI-generated text to inform the public on matters of public interest | Disclose, unless human editorial review with editorial responsibility applies |

---

## GPAI (Chapter V) — applicable since 2 August 2025

**All GPAI model providers (Art. 53):** technical documentation for the model;
information and documentation for downstream providers; a policy to comply with EU
copyright law including a TDM opt-out reservation; and a sufficiently detailed public
summary of training content.

Providers of GPAI released under free and open-source licences are exempt from parts of
this, unless the model presents systemic risk.

**Systemic-risk models (Art. 55):** additionally, model evaluation including adversarial
testing; assessment and mitigation of systemic risks; tracking, documenting, and
reporting serious incidents to the AI Office; and adequate cybersecurity for the model
and its physical infrastructure.

---

## Serious incident reporting (Art. 73)

Providers of high-risk systems report serious incidents to the market surveillance
authority of the Member State where the incident occurred.

| Trigger | Deadline |
|---|---|
| General | Immediately after establishing the causal link, and no later than **15 days** after becoming aware |
| Widespread infringement, or serious and irreversible disruption of critical infrastructure | **2 days** |
| Death of a person | **10 days** |

An initial incomplete report is permitted where necessary to meet the deadline, followed
by a complete one. Report first, complete second.

---

## Penalties (Art. 99)

| Breach | Maximum |
|---|---|
| Prohibited practices (Art. 5) | €35m or 7% of total worldwide annual turnover |
| Most other obligations, including high-risk requirements | €15m or 3% |
| Supplying incorrect, incomplete, or misleading information to authorities | €7.5m or 1% |

Whichever is higher, except for SMEs and start-ups where the lower of the two applies.

---

**Verify before relying.** Article numbering, dates, and the details above should be
checked against the current consolidated text of Regulation (EU) 2024/1689 and current
Commission guidance. Implementation timelines have been under active political
discussion.
