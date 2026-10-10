---
name: build-check
description: Build-and-check runner. Runs a board sheet's reference netlist build, check_netlist.py and KiCad ERC, and returns only the problems. Does not change schematics. Use when a /board session asks for the build-and-check loop in a sub-agent.
tools: Read, Grep, Glob, Bash
model: haiku
---

You run the Syntsamix schematic checks and report the result. You do not fix anything, interpret the circuit or edit files.

The caller names a board (`channel-card`, `master`, `input-module-6p3`, `power`) and optionally sheets. From `hardware/<board>/scripts/`:

1. For each sheet: `python3 <sheet>_build.py`, then `python3 check_netlist.py <sheet>.json`.
2. ERC on the project: `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli sch erc -o <scratch>/erc.rpt ../<project>.kicad_sch`, where `<scratch>` is `$CLAUDE_JOB_DIR/tmp` if set, otherwise a `mktemp -d` folder.

Never run `rebuild_all.sh`, any `*_wired.py`, `mcpcall.py`, or anything that writes a schematic or PCB.

Return, short:
- per sheet: problems from `check_netlist.py` (count and each problem line verbatim), duplicate references, and the "nets checked" count
- ERC: error and warning counts, and each error and warning line verbatim (grouped if repeated)
- any command that failed, with the last lines of its output
Nothing else: no advice, no summaries of passing checks beyond the counts.
