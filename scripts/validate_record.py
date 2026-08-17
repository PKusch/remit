#!/usr/bin/env python3
"""Validate Remit system records against the schema.

    python scripts/validate_record.py examples/*.yaml
    python scripts/validate_record.py records/           # walks a directory

Exits non-zero if any record fails, so it works as a pre-commit hook or CI step.

Two things this handles that a bare jsonschema call does not, both of which produced
false results the first time this repo was tested:

1. **YAML dates.** `last_reviewed: 2026-07-14` unquoted parses to a Python `date`
   object, not a string, and the schema declares these as `type: string`. Every date
   in a hand-written record fails for a reason that has nothing to do with governance.
   Dates are normalised to ISO strings before validation.

2. **Format checking is off by default.** `"format": "date"` is an annotation in JSON
   Schema unless a format checker is supplied, so `last_reviewed: "sometime in July"`
   validates happily. A format checker is enabled here, because a date field that
   accepts prose is not a date field.

Beyond schema conformance it reports *governance* warnings — internally consistent
records that are nonetheless telling you something. Those never fail the run; they are
observations for a human, not errors.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Missing dependency: pip install pyyaml")
try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:
    sys.exit("Missing dependency: pip install jsonschema")


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "framework" / "system-record.schema.json"

# Derived from framework/autonomy-tiers.md. Kept here so the grid is enforceable
# rather than merely documented — a record claiming 'minimal' oversight on an A3/B3
# agent is the single most common way autonomy creep hides in plain sight.
GRID = {
    "A0": {"B0": "minimal",  "B1": "minimal",  "B2": "standard",    "B3": "standard"},
    "A1": {"B0": "minimal",  "B1": "standard", "B2": "standard",    "B3": "enhanced"},
    "A2": {"B0": "minimal",  "B1": "standard", "B2": "enhanced",    "B3": "enhanced"},
    "A3": {"B0": "standard", "B1": "enhanced", "B2": "enhanced",    "B3": "constrained"},
    "A4": {"B0": "standard", "B1": "enhanced", "B2": "constrained", "B3": "prohibited"},
}
RADIUS_ORDER = ["B0", "B1", "B2", "B3"]

# A halt tested a year ago is evidence about last year. Six months is a defensible
# default; organisations with a shorter DR cycle should tighten it.
HALT_TEST_MAX_AGE_DAYS = 180


def normalise(obj):
    """Convert date/datetime objects PyYAML produced back into ISO strings."""
    if isinstance(obj, dict):
        return {k: normalise(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalise(v) for v in obj]
    if isinstance(obj, dt.datetime):
        return obj.date().isoformat()
    if isinstance(obj, dt.date):
        return obj.isoformat()
    return obj


def load(path: Path):
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    return normalise(data)


def days_since(value) -> int | None:
    """Age in days, or None if the value is a sentinel rather than a date.

    Fields that accept "unknown"/"never" reach here, so never assume a parseable date —
    a checker that crashes on a legitimately-recorded gap is worse than the gap.
    """
    if not isinstance(value, str):
        return None
    try:
        return (dt.date.today() - dt.date.fromisoformat(value)).days
    except ValueError:
        return None


def governance_warnings(rec: dict) -> list[str]:
    """Things that pass the schema but a reviewer should see."""
    out: list[str] = []
    ag = rec.get("agentic")
    if not ag:
        return out

    declared, observed = ag.get("autonomy_tier"), ag.get("observed_tier")
    radius = ag.get("blast_radius")

    if observed and declared and observed > declared:
        out.append(
            f"observed tier {observed} exceeds declared tier {declared} — "
            "the system is running with more autonomy than it is governed for"
        )

    # Blast radius must be at least the highest-radius tool actually held.
    tools = ag.get("tools") or []
    if tools and radius:
        worst = max((t.get("blast_radius", "B0") for t in tools), key=RADIUS_ORDER.index)
        if RADIUS_ORDER.index(worst) > RADIUS_ORDER.index(radius):
            names = [t["name"] for t in tools if t.get("blast_radius") == worst]
            out.append(
                f"blast_radius is {radius} but tool(s) {', '.join(names)} are {worst} — "
                "radius follows from the tools held, not from typical behaviour"
            )

    # Oversight level must match the grid for the tier actually observed.
    effective = observed or declared
    if effective and radius:
        expected = GRID[effective][radius]
        actual = ag.get("oversight_level")
        if actual and actual != expected:
            out.append(
                f"oversight_level is '{actual}' but the grid gives '{expected}' "
                f"for {effective}/{radius}"
            )
        if expected == "prohibited":
            out.append(f"{effective}/{radius} is prohibited by default — cut blast radius")

    # Enhanced and above require a halt mechanism that has actually been tested.
    if effective and radius and GRID[effective][radius] in ("enhanced", "constrained"):
        halt = ag.get("halt_mechanism") or {}
        exists = halt.get("exists")
        tested = halt.get("last_tested")
        if exists == "unknown":
            out.append("oversight level requires a halt mechanism; whether one exists is unknown")
        elif not exists:
            out.append("oversight level requires a halt mechanism; none recorded")
        elif tested in (None, "never", "unknown"):
            out.append("halt mechanism recorded but not evidenced as tested — an untested halt is not a halt")
        else:
            age = days_since(tested)
            if age is not None and age > HALT_TEST_MAX_AGE_DAYS:
                out.append(
                    f"halt mechanism last tested {age} days ago "
                    f"(> {HALT_TEST_MAX_AGE_DAYS}) — treat as untested until re-exercised"
                )

    if ag.get("reads_untrusted_content") and radius in ("B2", "B3"):
        out.append(
            f"reads untrusted content at {radius} — injection testing is load-bearing here (see P2)"
        )

    mem = ag.get("memory") or {}
    if mem.get("persistent") and not mem.get("provenance_recorded"):
        out.append("persistent memory without provenance — M1 exposure")

    for t in tools:
        if not t.get("justification"):
            out.append(f"tool '{t.get('name')}' has no justification recorded")

    for exc in rec.get("exceptions") or []:
        if exc.get("expires") and exc["expires"] < dt.date.today().isoformat():
            out.append(f"exception expired {exc['expires']}: {exc.get('description', '')[:60]}")

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate Remit system records.")
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--strict", action="store_true",
                    help="treat governance warnings as failures")
    args = ap.parse_args()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    files: list[Path] = []
    for p in args.paths:
        if p.is_dir():
            files += sorted(
                f for f in p.rglob("*")
                if f.suffix in (".yaml", ".yml", ".json") and f.is_file()
            )
        else:
            files.append(p)

    if not files:
        print("No records found.")
        return 1

    failed = warned = 0
    for path in files:
        rel = path.relative_to(REPO_ROOT) if REPO_ROOT in path.parents else path
        try:
            rec = load(path)
        except Exception as exc:  # noqa: BLE001 — surface any parse error to the user
            print(f"✗ {rel}\n    could not parse: {exc}")
            failed += 1
            continue

        errors = sorted(validator.iter_errors(rec), key=lambda e: list(e.path))
        warnings = governance_warnings(rec) if isinstance(rec, dict) else []

        if errors:
            failed += 1
            print(f"✗ {rel} — {len(errors)} schema error(s)")
            for e in errors:
                loc = "/".join(str(p) for p in e.path) or "(root)"
                print(f"    {loc}: {e.message}")
        else:
            print(f"✓ {rel}")

        if warnings:
            warned += 1
            for w in warnings:
                print(f"    ! {w}")

    print(f"\n{len(files)} record(s) · {failed} failed · {warned} with warnings")
    if failed:
        return 1
    return 1 if (args.strict and warned) else 0


if __name__ == "__main__":
    sys.exit(main())
