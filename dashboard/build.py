#!/usr/bin/env python3
"""Build the control room from your system records.

    python dashboard/build.py
    python dashboard/build.py --records path/to/records --out /tmp/estate.html

Reads every record in the given directories, embeds them in the template, and writes one
self-contained HTML file. No server, no dependencies at view time.

The dashboard assumes its input conforms — run scripts/validate_record.py first, which is
the gate. Building from records that do not validate produces a page that is confidently
wrong, which is worse than no page.
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

ROOT = Path(__file__).resolve().parent.parent


def norm(o):
    """PyYAML hands back date objects; JSON cannot carry them."""
    if isinstance(o, dict):
        return {k: norm(v) for k, v in o.items()}
    if isinstance(o, list):
        return [norm(v) for v in o]
    if isinstance(o, (dt.date, dt.datetime)):
        return o.isoformat()[:10]
    return o


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", type=Path, nargs="*",
                    default=[ROOT / "examples", ROOT / "tests" / "fixtures"])
    ap.add_argument("--out", type=Path, default=ROOT / "dashboard" / "index.html")
    args = ap.parse_args()

    recs, seen = [], set()
    for d in args.records:
        for f in sorted(d.rglob("*.yaml")) if d.is_dir() else [d]:
            try:
                data = yaml.safe_load(f.read_text(encoding="utf-8"))
            except Exception as exc:                       # noqa: BLE001
                print(f"  skipped {f.name}: {exc}")
                continue
            if isinstance(data, dict) and data.get("id") and data["id"] not in seen:
                seen.add(data["id"])
                recs.append(norm(data))

    if not recs:
        sys.exit("No records found. Point --records at a directory of *.record.yaml files.")

    tpl = (ROOT / "dashboard" / "template.html").read_text(encoding="utf-8")
    args.out.write_text(
        tpl.replace("__RECORDS__", json.dumps(recs, separators=(",", ":"))),
        encoding="utf-8")

    print(f"✓ {len(recs)} record(s) → {args.out}")
    for r in recs:
        g = r.get("agentic") or {}
        tier = f"{g.get('autonomy_tier','—')}/{g.get('observed_tier','—')}"
        print(f"    {r['id']:<24} {tier:<8} {g.get('blast_radius','—')}  "
              f"{g.get('oversight_level','—')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
