# Syntsamix

A modular, analog stereo mixer for live electronic music: synthesizers, drum machines and Eurorack modular gear on one desk, with a resonant ladder filter on every channel and a compressor built for bass pumping.

> **Status: in design.** The specification is complete and the schematics for all four prototype boards are done. Nothing has been built yet: no PCB is laid out and the filter breadboard is still waiting for parts. Figures below are design targets, not measurements.

## Goals

- **Made for playing live.** Few controls, each with an obvious musical effect; the mixer is part of the performance, not only a utility.
- **Modular.** Identical stereo channel cards, added one at a time from 1 to 16. No card depends on another, and there is no backplane: cards are daisy-chained by ribbon cables, with the master card at one end.
- **Synth-friendly inputs.** Balanced inputs take everything from consumer line level to hot Eurorack signals of ±12 V peak, with no external attenuator.
- **Analog signal path** with pro headroom: +4 dBu nominal, about +20 dBu internal maximum, +24 dBu at the balanced outputs.
- **Cost-effective.** A tight budget: cheaper parts wherever the audible difference is small.
- **Open design** for anyone to build for themselves (non-commercial license, see below).

## Features

### Channel strip (stereo, every element an L/R pair)

- Balanced 6.3 mm TRS inputs (L/MONO and R) on a separate, swappable passive input module; a mono source in L/MONO feeds both sides
- One wide input trim (about -20 to +20 dB) with **soft clipping**, so overloads saturate gently
- Switchable 100 Hz low-cut
- **24 dB/octave ladder low-pass filter** (Sound Semiconductor SSI2144) with cutoff (20 Hz to 20 kHz), resonance and bypass. Driven "hot" for character, with resonance capped below self-oscillation and the bass loss half compensated
- Cutoff CV input at about 1 V/octave for modulation from modular gear
- 60 mm fader driving a VCA (SSI2162) with a console-style law: +10 dB at the top, 0 dB at 75 % of travel, fully off at the bottom; click-free mute
- Two stereo AUX sends (post-fader, jumper for pre-fader)
- Main or compressor bus assign
- **PFL** (pre-fader listen): headphones switch to the cue bus automatically while any PFL is on
- **SC send** to the sidechain bus and **DUCK**, which lets the channel duck with the sidechain trigger
- 8-segment LED level meter
- Lit latching buttons; stereo functions switch electronically, so buttons carry only logic

### Master and compressor

- **Performance compressor** on a dedicated compressor bus: Amount (threshold and makeup together), Release, Mix (parallel compression), click-free on/off and gain-reduction LEDs. Feed-forward log peak detector, about 1 ms attack, 4:1
- **Sidechain** from the compressor bus itself, the channels' sidechain bus or an external jack (audio or Eurorack gates and envelopes), with a 40 to 500 Hz low-pass so the kick drives the pumping. An SC listen button puts it in the headphones
- **Sidechain ducking**: an envelope follower (threshold, depth, decay) ducks any channel with DUCK on, independently of the compressor
- Two stereo AUX returns (level, mute, main or compressor bus; jumper for pro or pedal levels) and two AUX send masters
- Master level through a VCA, soft clipping on the master bus
- Balanced main outputs (THAT1646, +24 dBu) and a headphone amplifier (TPA6120A2, 32 to 600 Ω)
- Stereo 12-segment master meter
- Output protection relays: silent power-up and power-down on the main and headphone outputs

### Construction

- Desktop unit: one PCB and a 35 mm FR4 top panel per channel strip, on an aluminium rail frame cut to length (about 650 to 700 mm wide at 16 strips)
- Powered by an off-the-shelf DC brick through a separate power board (24 V brick, non-isolated converters to ±20 V); every card regulates its own supply
- Separate audio and power ribbons, with audio and power grounds joined at a single star point
- RoHS compliant: every part needs a maker or supplier RoHS statement before it is chosen, and the boards are built lead-free

## Status

| Part | Schematic | PCB |
|---|---|---|
| Channel card | done (6 sheets, ERC clean; mechanical parts chosen) | waits for the filter breadboard, the RoHS declaration for the SSI2144/SSI2162 and the cable mock-up |
| Master card | done (10 sheets, ERC clean) | not started |
| Input module (6.3 mm) | done | not started |
| Power board | done (4 sheets, ERC clean) | not started |

Also done: ngspice simulations of the filter gain structure, the compressor detector, the sidechain/ducking circuits and the fader level control (`simulation/`); the mechanical contract for strips, panels and frame ([`docs/MECHANICAL.md`](docs/MECHANICAL.md)); a RoHS audit of the parts register. Next: the SSI2144 breadboard, a chain cable mock-up, then PCB layout, starting with the channel card. The prototype has 4 channels.

The full roadmap and backlog (more input modules, direct outputs, 32 channels, and more) are in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Repository

| Path | Contents |
|---|---|
| [`docs/SPEC.md`](docs/SPEC.md) | Full specification and performance targets |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | System diagram, cross-board budgets and invariants |
| [`docs/decisions/`](docs/decisions/INDEX.md) | Every design decision, numbered and grouped by area |
| [`docs/CHAIN.md`](docs/CHAIN.md), [`docs/INPUT-MODULE.md`](docs/INPUT-MODULE.md) | Ribbon and input header pinouts |
| [`docs/MECHANICAL.md`](docs/MECHANICAL.md) | Strip envelope, panel stack, frame and card fixing |
| [`docs/parts.csv`](docs/parts.csv) | Parts register (`SX-` part numbers) |
| `hardware/` | KiCad projects: `channel-card`, `master`, `input-module-6p3`, `power`; shared libraries in `libs/` |
| `simulation/` | ngspice models, results and the breadboard plan |

Schematics are generated by Python scripts and checked pin by pin against an independent reference netlist; see `hardware/channel-card/scripts/README.md`. The design is developed with Claude Code; [`docs/WORKING-WITH-CLAUDE.md`](docs/WORKING-WITH-CLAUDE.md) describes the workflow.

## License

Source-available for **non-commercial** use; the author keeps all commercial rights. Hardware and documentation are CC BY-NC-SA 4.0, code is PolyForm Noncommercial 1.0.0. You may build, modify and play the mixer (paid gigs included), but not sell boards, kits or units without permission. Details in [`LICENSE.md`](LICENSE.md).
