# CLAUDE.md

Project context for Claude Code. Read this first, then `docs/SPEC.md`, `docs/DECISIONS.md`, `docs/CHAIN.md` and `docs/ROADMAP.md`.

## Project

A modular, analog pro audio mixer for connecting synthesizers and instruments in electronic music live performances. Designed in KiCad. We are currently in the **specification phase**: no schematics or PCBs exist yet.

## Prototype scope (confirmed by the user)

- 4 stereo channels
- Per channel: balanced inputs, level fader, mute, 24 dB/oct ladder LPF with resonance and bypass, 2 AUX sends and returns (stereo by default, mono-capable), main/compressor bus assign
- Compressor on a dedicated compressor bus, with selectable/routable sidechain input; the sidechain has an LPF (main intent is bass pumping)
- PFL per channel (post-filter, pre-fader, pre-mute); headphones switch to the cue bus automatically while any PFL is active
- 8-segment LED level meter per channel (post-filter, pre-fader)
- Master: headphone output, stereo LED meter on the master bus
- Modular by design: channel strips can be added one at a time; no channel card depends on another
- Inputs accept hot Eurorack levels (up to ±12 V peak) as well as line levels
- Channel HPF is dropped from the prototype to simplify the build (keep room to add it later)

## Filter decision

24 dB/oct (4-pole) ladder LPF, resonance on the LPF only. Not required to be Moog-style.
- Baseline: Sound Semiconductor SSI2144 (SSM2044 reissue). Datasheet Rev 3.0 facts are recorded in `docs/SPEC.md` section 3
- Fallback: AS3320 / V3320 (CEM3320 clone)
- Gain structure: "hot" drive at the datasheet nominal level, with a per-channel bypass
- Distributor availability is still unverified.

## How to work on this project

1. **Separate confirmed from assumed.** `docs/DECISIONS.md` lists what the user confirmed and what was only proposed. Never treat a proposal as settled. Ask before changing a confirmed decision.
2. **Spec first.** Settle the open items in `docs/DECISIONS.md` before drawing schematics.
3. **Simulate before layout.** Prove the filter gain structure (headroom and noise) in ngspice or on a breadboard before committing the channel card design.
4. **Use the KiCad MCP server** for schematic and PCB edits. Pause for the user's review before each commit. Run ERC after schematic changes and DRC after layout changes.
5. **Keep modules independent.** Each module is its own KiCad project or hierarchical sheet with a documented chain interface (audio and power ribbon pinouts).
6. **Check part facts.** Do not invent pinouts, footprints or electrical limits. Look them up in datasheets, and say so when you cannot verify something.

## Proposed repo layout (not created yet)

```
CLAUDE.md
docs/            SPEC.md, DECISIONS.md, CHAIN.md, ROADMAP.md
hardware/
  channel-card/  KiCad project (stereo channel)
  master/        KiCad project (compressor, master, outputs)
  power/         KiCad project (supply)
  chain/         ribbon interface definition (pinouts, shared footprints)
  libs/          custom symbols and footprints
simulation/      ngspice netlists and results
```

## Current status and next steps

Status: spec v0.6 drafted. All feature proposals confirmed. Open: filter simulation, supply rating.

Next:
1. Settle the open items in `docs/DECISIONS.md`
2. Write the block diagram and the chain pinouts (34-pin audio, 8-pin power)
3. Simulate or breadboard one SSI2144 filter channel (headroom, noise, tracking)
4. Start the channel card schematic in KiCad
