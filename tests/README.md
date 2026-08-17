# Tests

Two kinds of check live here, because the repo makes two kinds of claim.

## 1. Mechanical — does a record conform?

```bash
pip install pyyaml jsonschema
python scripts/validate_record.py examples/ tests/fixtures/
```

Validates every record against `framework/system-record.schema.json` with format
checking enabled, and reports governance warnings the schema cannot express. Exits
non-zero on schema failure, so it works as a pre-commit hook or CI step. Add `--strict`
to fail on warnings too.

This is not decoration. On its first run it found that the worked example did not
validate against its own schema — eighteen errors, because YAML parses unquoted dates
into `date` objects while the schema declares strings. Nobody spots that by reading.

## 2. Judgement — do the skills reach the right conclusion?

The skills produce reasoning, so there is no assertion to run. What there can be is a
scenario with a **known correct answer**, written down in advance, so anyone can run the
skills and check.

`fixtures/sentinel-scenario.md` is built for this. It is deliberately adversarial: the
system *sounds* high-risk (autonomous, production payments infrastructure, financial
firm) but is not caught by Annex III, while the regime that genuinely binds it is one an
AI-Act-shaped assessment will walk straight past. It tests for over-classification in one
direction and under-scoping in the other.

Each fixture states what a good assessment must get right and which failure modes it is
watching for. Run the skills against the scenario text and compare.

### Known result

Running the chain against Sentinel on 2026-08-17 surfaced a genuine gap: the correct DORA
conclusion was not reachable from the repo as it then stood — `eu-ai-act-triage` did not
mention DORA and no DORA skill existed, while the README and crosswalk both advertised
coverage. `skills/dora-ict-assessment/` and the routing step in `eu-ai-act-triage`
(§8, "a negative finding is not an all-clear") exist because of that run.

## Adding a fixture

The valuable ones are cases where the obvious answer is wrong. Give the stakeholder
description in the words someone would actually use, the facts needed to score it, what a
good assessment must get right, and the failure modes you are testing for. A fixture
where the answer is easy tests nothing.
