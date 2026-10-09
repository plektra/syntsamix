# CLAUDE.md

Project context for Claude Code. Read this first, then:

1. `docs/CONTINUE-FROM-HERE.md`: project-level handoff (which board is where, what is next)
2. `docs/decisions/INDEX.md`: every decision with its status and area file
3. `docs/ARCHITECTURE.md`: system diagram, cross-board budgets, chain lines, invariants (the constitution; changed only in `/system` sessions)
4. For the work at hand: the board's `CLAUDE.md` and `STATUS.md` (`hardware/<board>/`), its decision file in `docs/decisions/`, and `hardware/CLAUDE.md` for the shared schematic workflow

Read the rest only when the task needs it: `docs/SPEC.md` (full specification), `docs/CHAIN.md`, `docs/INPUT-MODULE.md` and `docs/MECHANICAL.md` (interfaces between boards), `docs/PART-NUMBERING.md`, `docs/ROADMAP.md` (phases, backlog), `simulation/CLAUDE.md`.

For the user: `docs/WORKING-WITH-CLAUDE.md` describes the roles and the session loop: `/board <board> [phase]` for board work, `/system [topic]` for architecture, `/handoff` to wrap up, `/validate <scope>` for an independent check (the `architect` and `validator` sub-agents live in `.claude/agents/`). Work one board and phase per session (for example "power board schematic"), and update that board's `STATUS.md` before ending. Use sub-agents only for bounded jobs with a short result (datasheet fact checks, build-and-check loops, simulation runs, stock checks); design choices stay in the main conversation with the user.

## Project

A modular, analog pro audio mixer for connecting synthesizers and instruments in electronic music live performances. Designed in KiCad. The specification is complete (v0.7); all schematics are drawn; PCB layout is next.

## Prototype scope (confirmed by the user)

- 4 stereo channels
- Per channel: balanced inputs, level fader, mute, switchable 100 Hz low-cut, soft-clipping input stage, 24 dB/oct ladder LPF with resonance and bypass, 2 AUX sends and returns (stereo by default, mono-capable), main/compressor bus assign
- Sidechain ducking: per-channel DUCK button applies the master's sidechain envelope to the channel VCA
- Compressor on a dedicated compressor bus, with selectable/routable sidechain input; the sidechain has an LPF (main intent is bass pumping)
- PFL per channel (post-filter, pre-fader, pre-mute); headphones switch to the cue bus automatically while any PFL is active
- 8-segment LED level meter per channel (post-filter, pre-fader)
- Master: headphone output, stereo LED meter on the master bus
- Modular by design: channel strips can be added one at a time; no channel card depends on another
- Inputs accept hot Eurorack levels (up to ±12 V peak) as well as line levels
- Channel HPF is dropped from the prototype to simplify the build (keep room to add it later); a fixed switchable 100 Hz low-cut is included instead
- Input jacks sit on a separate passive input module (10-pin header, `docs/INPUT-MODULE.md`); the cutoff CV jack is on the channel card's top panel
- Stereo button functions switch through DG413 analog switches; buttons only carry logic and LED current

## How to work on this project

1. **Separate confirmed from assumed.** `docs/decisions/` records what the user confirmed; text marked **[proposed]** is only proposed. Never treat a proposal as settled. Ask before changing a confirmed decision.
2. **Spec first.** Settle the open items in `docs/decisions/INDEX.md` before drawing schematics. New decisions take the next free number, go into their area file, and get a row in the index.
3. **Simulate before layout.** Prove the filter gain structure (headroom and noise) in ngspice or on a breadboard before committing the channel card design.
4. **Use the KiCad MCP server** for schematic and PCB edits. Pause for the user's review before each commit. Run ERC after schematic changes and DRC after layout changes.
5. **Keep modules independent.** Each module is its own KiCad project or hierarchical sheet with a documented chain interface (audio and power ribbon pinouts).
6. **Number every part.** Give each placed symbol the BOM fields in `docs/PART-NUMBERING.md` and register new part types in `docs/parts.csv`.
7. **Keep licensing tidy.** New code files get the two-line SPDX header (`PolyForm-Noncommercial-1.0.0`); other new paths must be covered by `REUSE.toml`. Run `reuse lint` before committing.
8. **Check part facts.** Do not invent pinouts, footprints or electrical limits. Look them up in datasheets, and say so when you cannot verify something. Every part must be RoHS compliant, with its source recorded in `docs/parts.csv` (invariant 9, decisions 116 and 122).

## Repo layout

```
README.md        landing page (project, features, status)
CLAUDE.md
.claude/commands/  /board, /system, /handoff, /validate
.claude/agents/    architect (contract reviewer), validator (independent design checks)
LICENSE.md, REUSE.toml, LICENSES/  licensing (decision 70)
docs/            CONTINUE-FROM-HERE.md, ARCHITECTURE.md, WORKING-WITH-CLAUDE.md, SPEC.md, CHAIN.md, INPUT-MODULE.md, MECHANICAL.md, PART-NUMBERING.md, parts.csv, ROADMAP.md
  decisions/     decision log by area, INDEX.md (DECISIONS.md is a pointer to it)
  reviews/       validator reports
hardware/        CLAUDE.md: shared schematic workflow; each board has CLAUDE.md and STATUS.md
  channel-card/  KiCad project (stereo channel)
  input-module-6p3/  KiCad project (6.3 mm input module)
  libs/          shared symbols (syntsamix.kicad_sym) and footprints
  master/        KiCad project (compressor, master, outputs)
  power/         KiCad project (24 V brick input, non-isolated converters to ±20 V; decisions 81, 100)
simulation/      ngspice model, filter results, breadboard plan, BOM and order files
```

## Current status

Spec v0.7 complete (decisions 1-123; RoHS is invariant 9). Schematics done for the input module, channel card, master card and power board (ERC 0/0); no PCB yet. Per-board detail is in each `STATUS.md`; the order of work is in `docs/CONTINUE-FROM-HERE.md`.
