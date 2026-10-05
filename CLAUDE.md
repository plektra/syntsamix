# CLAUDE.md

Project context for Claude Code. Read this first, then `docs/SPEC.md`, `docs/DECISIONS.md`, `docs/CHAIN.md`, `docs/INPUT-MODULE.md`, `docs/PART-NUMBERING.md` and `docs/ROADMAP.md`.

## Project

A modular, analog pro audio mixer for connecting synthesizers and instruments in electronic music live performances. Designed in KiCad. The specification is complete (v0.7); we are now in the **schematic phase**.

## Prototype scope (confirmed by the user)

- 4 stereo channels
- Per channel: balanced inputs, level fader, mute, switchable 150 Hz low-cut, soft-clipping input stage, 24 dB/oct ladder LPF with resonance and bypass, 2 AUX sends and returns (stereo by default, mono-capable), main/compressor bus assign
- Sidechain ducking: per-channel DUCK button applies the master's sidechain envelope to the channel VCA
- Compressor on a dedicated compressor bus, with selectable/routable sidechain input; the sidechain has an LPF (main intent is bass pumping)
- PFL per channel (post-filter, pre-fader, pre-mute); headphones switch to the cue bus automatically while any PFL is active
- 8-segment LED level meter per channel (post-filter, pre-fader)
- Master: headphone output, stereo LED meter on the master bus
- Modular by design: channel strips can be added one at a time; no channel card depends on another
- Inputs accept hot Eurorack levels (up to ±12 V peak) as well as line levels
- Channel HPF is dropped from the prototype to simplify the build (keep room to add it later); a fixed switchable 150 Hz low-cut is included instead
- Input jacks sit on a separate passive input module (10-pin header, `docs/INPUT-MODULE.md`); the cutoff CV jack is on the channel card's top panel
- Stereo button functions switch through DG413 analog switches; buttons only carry logic and LED current

## Filter decision

24 dB/oct (4-pole) ladder LPF, resonance on the LPF only. Not required to be Moog-style.
- Baseline: Sound Semiconductor SSI2144 (SSM2044 reissue). Datasheet Rev 3.0 facts are recorded in `docs/SPEC.md` section 3
- Fallback: AS3320 / V3320 (CEM3320 clone)
- Gain structure: "hot" drive at the datasheet nominal level by default, a prototype jumper for medium drive, per-channel bypass, half resonance compensation through the datasheet's LM13700 Q VCA (jumper: none/half/full). Simulation in `simulation/filter/`
- Sold by synth-DIY resellers (Electrokit, Thonk), not by Mouser or DigiKey.

## How to work on this project

1. **Separate confirmed from assumed.** `docs/DECISIONS.md` lists what the user confirmed and what was only proposed. Never treat a proposal as settled. Ask before changing a confirmed decision.
2. **Spec first.** Settle the open items in `docs/DECISIONS.md` before drawing schematics.
3. **Simulate before layout.** Prove the filter gain structure (headroom and noise) in ngspice or on a breadboard before committing the channel card design.
4. **Use the KiCad MCP server** for schematic and PCB edits. Pause for the user's review before each commit. Run ERC after schematic changes and DRC after layout changes.
5. **Keep modules independent.** Each module is its own KiCad project or hierarchical sheet with a documented chain interface (audio and power ribbon pinouts).
6. **Number every part.** Give each placed symbol the BOM fields in `docs/PART-NUMBERING.md` and register new part types in `docs/parts.csv`.
7. **Keep licensing tidy.** New code files get the two-line SPDX header (`PolyForm-Noncommercial-1.0.0`); other new paths must be covered by `REUSE.toml`. Run `reuse lint` before committing.
8. **Check part facts.** Do not invent pinouts, footprints or electrical limits. Look them up in datasheets, and say so when you cannot verify something.

## Repo layout

```
CLAUDE.md
LICENSE.md, REUSE.toml, LICENSES/  licensing (decision 70)
docs/            SPEC.md, DECISIONS.md, CHAIN.md, INPUT-MODULE.md, PART-NUMBERING.md, parts.csv, ROADMAP.md
hardware/
  channel-card/  KiCad project (stereo channel)
  input-module-6p3/  KiCad project (6.3 mm input module)
  libs/          shared symbols (syntsamix.kicad_sym) and footprints
  master/        KiCad project (compressor, master, outputs), not created yet
  power/         power input section, not created yet
simulation/      ngspice model, filter results, breadboard plan, BOM and order files
```

## Current status and next steps

Status: spec v0.7 complete (decisions 1-72). Filter simulated; breadboard parts ordered. Input module schematic done. Channel card schematic in progress: Input, Filter and Level sheets done (ERC clean apart from sheet links that wait for the Routing and Chain sheets). Filter output scale and Q current limit are provisional until the breadboard.

Next:
1. Remaining channel card sheets: Routing, Meter, Chain and power (see `docs/ROADMAP.md`)
2. Breadboard the SSI2144 when parts arrive (including the LM13700 Q VCA test); update filter values from the measurements
4. Master/compressor card, then the power input section
