# Control room

```bash
python dashboard/build.py && open dashboard/index.html
```

A single self-contained HTML file. No server, no build step, no dependencies — open it and
your AI estate is on screen.

## What it is for

Not a report. An **instrument**. You open it, and the thing that needs attention is already
obvious without reading anything.

**The grid is the interface, not an illustration of one.** Every system sits in its real
square — autonomy across, reach down — and clicking a square tells you what that position
obliges and filters the list to the systems there. That is the whole model, learnable in
about thirty seconds without opening a document.

**Control gaps are computed in the page**, by the same checks
[`scripts/validate_record.py`](../scripts/validate_record.py) runs: an observed tier above
the declared one, a blast radius below the tools actually held, an untested halt where the
level requires one, memory without provenance, expired exceptions. What you see here is
what CI would tell you. It is not a summary of an assessment someone wrote — it is the
assessment, run now.

## Regenerating it

`build.py` reads every record in `examples/` and `tests/fixtures/`, embeds them, and writes
`index.html`. Point it at your own records directory to see your own estate:

```bash
python dashboard/build.py --records path/to/your/records --out dashboard/index.html
```

Records must validate first — `validate_record.py` is the gate, and the dashboard assumes
conformance rather than re-checking it.

## Reading it

The four numbers across the top are the only things you must look at. `systems governed`
is a count; the other three are all counts of things being wrong, and they are coloured
when they are non-zero.

Severity is encoded in **form as well as number** — the stripe down the left of each system
row carries its oversight level, so the list is scannable without reading a word of it.

The findings inside each row are set in a serif, and that is deliberate: they are written
judgements by an assessor, not UI chrome, and they should not look like the same kind of
object as a count.
