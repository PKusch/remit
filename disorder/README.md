# Disorder

The zoo is caged. Every specimen is scripted, deterministic, exhibits exactly one
pathology, and the answer was known in advance. It proves the diagnostic criteria are
*implementable*. It proves nothing about whether these failures actually **arise**.

So: don't script anything. Write agents that are genuinely reasonable, put them in a world
that misbehaves, and find out what emerges.

```bash
python disorder/run.py                 # the sweep
python disorder/run.py -n 400          # more episodes per condition
python disorder/run.py --replay 46727 --agent remediator --condition flaky
```

Seeded throughout. An episode is a pure function of `(seed, agent, pressure)`, so anything
interesting is reproducible from an integer. No model calls, no dependencies, no network.

---

## The discipline

**The agents must be reasonable.** If you write an agent that retries forever you have
just rebuilt the zoo with extra steps. Every policy in [`agents.py`](agents.py) is one a
competent engineer would ship and defend in review: bounded retries, verify before
reporting, escalate when stuck, fail open rather than block the queue, record what you
learned.

Where a policy takes a shortcut, it is a shortcut real systems take constantly, and the
comment says so — the remediator writes its closing summary from the last action's *return
code* rather than from its verification; the reviewer approves when its static-analysis
tool is unavailable rather than blocking the pipeline. Neither is negligent. Both are
recognisable.

**The environment does the work.** Six dials, each mundane, each something production does
on an ordinary Tuesday:

| Pressure | What it does |
|---|---|
| `flaky` | tools fail intermittently |
| `liar` | actions return 200 without changing anything |
| `drift` | a third party mutates state mid-episode |
| `truncate` | a context boundary drops earlier constraints |
| `inject` | fetched documents carry instruction-shaped text |
| `contention` | another actor writes the same keys concurrently |

Classification uses the **zoo's detector, unchanged**. A classifier built against scripted
specimens, pointed at unscripted behaviour, is the only honest way to find out whether the
manual describes anything real.

---

## What it found

### 1. Most of what looks emergent is latent

The first version of this report was misleading, and the way it was misleading is the most
useful thing here. Four modes appeared at ~20% under **every** condition — including
`calm`, with all dials at zero.

They were not emergent at all. Each was one agent out of five exhibiting a mode in 100% of
its episodes regardless of environment: the coordinator always delegates without recording
authority (`S2`) and always writes irreversibly without confirmation (`A3`); the reviewer
always rubber-stamps (`S1`); the learner always persists a lesson without provenance
(`M1`).

Those are **defects sitting in the policy, waiting** — visible in a completely benign
world, if anyone had looked. The report now separates them, because conflating the two
inflates every other number on the page.

The governance reading is blunt: a chaos exercise that finds a lot of failures may simply
be finding your architecture.

### 2. The manual's cascade claim does not hold

`framework/diagnostic-manual.md` asserted that cascades are "the common case". Measured
across 2,400 unscripted episodes:

```
  86/2400 episodes  (4%)  produced more than one *emergent* mode
 793/2400 episodes (33%)  counting latent defects too — the flattering number
```

**Four percent.** The manual has been corrected rather than the measurement.

And where cascades do occur, they are not chains. `A1` and `M2` co-occur strongly because
a single truncation event causes both — not because scope creep leads to amnesia. Treat a
co-occurrence as a hint about a **common cause**, not as evidence of a sequence.

### 3. A bounded retry budget protects you, right up until it doesn't

The remediator retries eight times and then escalates. That is a sensible policy. Sweeping
how often the tool lies about success:

```
  liar=0.1   ··················    0%   A2 retry storm
  liar=0.3   █·················    6%
  liar=0.5   ████··············   21%
  liar=0.7   ████████··········   45%
  liar=0.85  █████████████·····   73%
  liar=1.0   ██████████████████  100%
```

The budget genuinely protects the agent while failures are occasional, then gives way
sharply. There is no gentle degradation to notice in staging — which is exactly why this
class of failure arrives in production as a surprise.

### 4. Concealment is the dominant emergent mode

Under `flaky` alone, **~74%** of episodes produce `R3` failure concealment. Not from a
dishonest agent — from a reporting granularity coarser than the failure granularity. The
migrator reports that the batch finished, because the batch did finish; four items inside
it did not.

If you fix one thing after reading this, make errors structural in the harness rather than
narrative in the summary. The agent should not be the component deciding what counts as
worth mentioning.

---

## Shape

```
disorder/
├── hostile.py    the world that fights back, and the six pressures
├── agents.py     five reasonable policies — the discipline lives here
└── run.py        episode runner, latent/emergent split, dose–response, cascades
```

Traces are emitted in the zoo's format, so `zoo/harness/detect.py` reads both.

## What this does not prove

The agents are mine, so the space of reachable failures is bounded by policies I thought
to write. Emergence here means "not scripted", not "not anticipated" — I chose the dials,
and a dial exists because I suspected it would matter.

The stronger version of this experiment uses agents somebody else wrote, or real
production traces. What is defensible right now is narrower and still worth having: given
these policies and these pressures, the failure rates and the cascade rate are
**measurements**, and one of them was sufficient to falsify a claim the manual had been
making with a straight face.
