# Inter-rater study — 2026-08-18 (extended 2026-08-19)

The raw materials behind the κ = 0.83 figure in
[`framework/diagnostic-manual.md`](../../framework/diagnostic-manual.md), kept so the
result can be checked rather than taken on trust.

```bash
python tests/interrater.py tests/interrater-2026-08-18
```

| File | What it is |
|---|---|
| `packet.json` | The 8 traces as the raters saw them. Ground-truth fields stripped. |
| `rater_opus_A..D.json` | Four independent classifications, collected blind. |
| `rater_haiku_F` · `rater_sonnet_G` · `rater_fable_E` | Three more raters on different models, added to test the shared-priors objection. |
| `truth.json` | Ground truth, withheld from every rater until scoring. |

**Method.** Each rater received the diagnostic manual and the packet, with no information
about who wrote either, and was asked for a primary code per trace plus the lettered
criteria they found met. Raters never saw each other's answers. The scorer was written
before any ratings were read — writing it afterwards would have made it worth much less.

**The shared-priors test.** The original panel was four instances of one model, and the
obvious objection was that they might agree because they are one model. Extending to seven
raters across four model families answered it: within-model agreement 85.4%, cross-model
87.5%. Agreement did not drop when the rater changed.

That is weaker than it first appears — the same-model group happened to hold the panel's
most contested call, which flatters the cross-model number, and eight traces is not enough
to put a tight interval on a two-point gap. The claim that survives is that agreement is
not an artefact of one model's habits.

**Honest limits.** Eight traces is a small packet, one contested trace moves κ by several
points, and every rater is a model rather than a person. Human raters remain the stronger
test and the same instrument runs on them unmodified.

**What it produced.** Two criteria defects, both fixed in the manual rather than argued
away: `A1`/`G2` are not separable from a trace, and `P3` criterion B asked for evidence a
trace cannot contain. A third observation — that a context boundary can make `R3`
criterion C unsatisfiable — is now addressed in that entry.
