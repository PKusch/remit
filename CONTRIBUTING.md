# Contributing

The most useful contribution is a failure mode the diagnostic manual misses, or a
case where its criteria gave the wrong answer on real evidence. Open an issue with
what you saw and, where you can share it, the artefacts.

If you are changing files, run the same checks CI runs before you push. All of them
are plain Python scripts with two small dependencies:

```bash
pip install pyyaml jsonschema
python scripts/check_links.py        # every relative link in the markdown resolves
python scripts/check_staleness.py    # legal content has been re-verified recently
python scripts/check_crosswalk.py    # every citation in the crosswalk points at something real
python scripts/validate_record.py examples/ tests/fixtures/
```

## Legal and standards content

Anything that depends on a law or a standard carries a line like
`verified: 2026-09-15` and `check_staleness.py` fails once it is more than 90 days
old. When it fails, go back to the regulation, confirm the file is still right, fix
what has changed, and only then update the date. Bumping the date without checking
defeats the point of the check.

The files it watches are listed at the top of `scripts/check_staleness.py`. A new
file that leans on external law should be added to that list.

## The crosswalk

`framework/crosswalk.md` maps governance themes to the EU AI Act, NIST AI RMF,
ISO/IEC 42001 and DORA. `check_crosswalk.py` reads its "By governance theme"
table and fails if a cited article or control does not appear in the matching
reference file under `skills/`. So a new citation needs its reference entry first,
in the same change.

## Adding a skill

A skill is a folder under `skills/` holding a `SKILL.md`, plus a `references/`
folder if it needs one. The description in the front matter is what decides when
the skill is used, so write it as the situations a person would actually be in, not
as a summary of the contents. `./install.sh` picks up every folder in `skills/`, so
there is no list to update. Link to the framework files with relative paths and
`check_links.py` will tell you if any of them are wrong.

## Style

Write for the person who has to make a decision with it. Say what a thing does and
why it matters, keep to one idea per sentence, and put a plain meaning next to any
number.
