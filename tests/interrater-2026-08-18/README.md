# Inter-rater study — 2026-08-18

The raw materials behind the κ = 0.83 figure in
[`framework/diagnostic-manual.md`](../../framework/diagnostic-manual.md), kept so the
result can be checked rather than taken on trust.

```bash
python tests/interrater.py tests/interrater-2026-08-18
```

| File | What it is |
|---|---|
| `packet.json` | The 8 traces as the raters saw them. Ground-truth fields stripped. |
| `rater_A..D.json` | Four independent classifications, collected blind. |
| `truth.json` | Ground truth, withheld from every rater until scoring. |

**Method.** Each rater received the diagnostic manual and the packet, with no information
about who wrote either, and was asked for a primary code per trace plus the lettered
criteria they found met. Raters never saw each other's answers. The scorer was written
before any ratings were read — writing it afterwards would have made it worth much less.

**Honest limits.** Eight traces and four raters is a small study, and one contested trace
moves κ by several points. The raters are model instances, not people, so their agreement
may be inflated by shared priors. This is the first evidence the manual has had, not the
last it needs — and the same instrument runs on humans without modification.

**What it produced.** Two criteria defects, both fixed in the manual rather than argued
away: `A1`/`G2` are not separable from a trace, and `P3` criterion B asked for evidence a
trace cannot contain. A third observation — that a context boundary can make `R3`
criterion C unsatisfiable — is now addressed in that entry.
