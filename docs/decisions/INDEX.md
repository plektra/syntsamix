# Decision index

The decision log, split by area. Read this index, then the area file for the work at hand. Every decision keeps its global number (referenced elsewhere as "decision N" or "item N"); numbers are never reused.

| File | Area |
|---|---|
| [system.md](system.md) | System scope, signal levels, buses, cross-board functions, chain and grounding |
| [channel-card.md](channel-card.md) | Channel card |
| [input-module.md](input-module.md) | Input module |
| [master-card.md](master-card.md) | Master/compressor card |
| [power.md](power.md) | Power board |
| [mechanical.md](mechanical.md) | Frame, panels, strip layout, front-panel parts |
| [process.md](process.md) | Tools, part numbering, licensing, test points, assembly, availability notes |

## Rules

- **Confirmed** decisions were agreed by the user; ask before changing one. Text marked **[proposed]** inside a decision still needs confirmation.
- New decision: next free number, appended to its area file, plus one row here. A decision that refines another says so ("refines item N").
- Interface documents are contracts between boards: `docs/CHAIN.md` (ribbons), `docs/INPUT-MODULE.md` (input header). Change them only through a confirmed decision.

## All decisions

| # | Decision | Status | File |
|---|---|---|---|
| 1 | Purpose: live mixer for synths and instruments | confirmed | [system](system.md) |
| 2 | Modular by design | confirmed | [system](system.md) |
| 3 | Prototype: 4 stereo channels | confirmed | [system](system.md) |
| 4 | Channel feature set | confirmed | [channel-card](channel-card.md) |
| 5 | Compressor with routable sidechain | confirmed | [master-card](master-card.md) |
| 6 | Sidechain filter is an LPF | confirmed | [master-card](master-card.md) |
| 7 | 24 dB/oct ladder LPF with resonance | confirmed | [channel-card](channel-card.md) |
| 8 | Channel HPF dropped from the prototype | confirmed | [channel-card](channel-card.md) |
| 9 | Filter part SSI2144, AS3320 fallback | confirmed | [channel-card](channel-card.md) |
| 10 | KiCad with its MCP server | confirmed | [process](process.md) |
| 11 | Specification before implementation | confirmed | [process](process.md) |
| 12 | Filter gain structure: hot drive plus bypass | confirmed | [channel-card](channel-card.md) |
| 13 | Dedicated compressor bus | confirmed | [system](system.md) |
| 14 | Stereo AUX, mono-capable | confirmed | [system](system.md) |
| 15 | Headphone output on the master | confirmed | [master-card](master-card.md) |
| 16 | L/R filter tracking: offset trim and tempco resistor | confirmed | [channel-card](channel-card.md) |
| 17 | Fixed maximum Q current | confirmed | [channel-card](channel-card.md) |
| 18 | Resonance bass-loss compensation | confirmed | [channel-card](channel-card.md) |
| 19 | Fader controls a VCA | confirmed | [channel-card](channel-card.md) |
| 20 | Per-channel cutoff CV input | confirmed | [channel-card](channel-card.md) |
| 21 | Mono via L/MONO jack normalling | confirmed | [input-module](input-module.md) |
| 22 | No balance/pan control | confirmed | [channel-card](channel-card.md) |
| 23 | AUX sends post-fader, jumper for pre | confirmed | [channel-card](channel-card.md) |
| 24 | Mono AUX handling on the master card | confirmed | [master-card](master-card.md) |
| 25 | Inputs take hot Eurorack levels | confirmed | [system](system.md) |
| 26 | One wide input trim, no pad | confirmed | [channel-card](channel-card.md) |
| 27 | All jacks 6.3 mm | confirmed | [system](system.md) |
| 28 | PFL and cue bus in the prototype | confirmed | [system](system.md) |
| 29 | Stereo master meter on the master bus | confirmed | [master-card](master-card.md) |
| 30 | Channel cards independent, added one at a time | confirmed | [system](system.md) |
| 31 | VCA: SSI2162, THD+N target 0.05 % | confirmed | [channel-card](channel-card.md) |
| 32 | Tight budget | confirmed | [system](system.md) |
| 33 | Input receiver: AD8273 at G = 1/2 | confirmed | [channel-card](channel-card.md) |
| 34 | Chainable bus from the start | confirmed | [system](system.md) |
| 35 | Linear fader with shaped law | confirmed | [channel-card](channel-card.md) |
| 36 | Fader range +10 dB to off | confirmed | [channel-card](channel-card.md) |
| 37 | Fader scale and markings | confirmed | [channel-card](channel-card.md) |
| 38 | Chain per card, ribbons, no backplane | confirmed | [system](system.md) |
| 39 | Maximum 16 channel cards | confirmed | [system](system.md) |
| 40 | Chain power: unregulated ±20 V, local ±15 V | confirmed | [system](system.md) |
| 41 | Separate 34-pin audio and 8-pin power ribbons | confirmed | [system](system.md) |
| 42 | Chain pinouts and grounding (CHAIN.md) | confirmed | [system](system.md) |
| 43 | 8-segment channel meter | confirmed | [channel-card](channel-card.md) |
| 44 | Compressor performance controls | confirmed | [master-card](master-card.md) |
| 45 | Sidechain source selection INT/BUS/EXT | confirmed | [master-card](master-card.md) |
| 46 | Signal levels, performance targets, coupling | confirmed | [system](system.md) |
| 47 | Tooling | confirmed | [process](process.md) |
| 48 | Fader part: Bourns PTA6043 | confirmed | [channel-card](channel-card.md) |
| 49 | Master meter: 12 segments per side | confirmed | [master-card](master-card.md) |
| 50 | Filter simulation outcome: drive jumper, half compensation | confirmed | [channel-card](channel-card.md) |
| 51 | AUX send and return levels | confirmed | [master-card](master-card.md) |
| 52 | Cutoff range 20 Hz to 20 kHz | confirmed | [channel-card](channel-card.md) |
| 53 | Cutoff CV: 1 V/oct, protected | confirmed | [channel-card](channel-card.md) |
| 54 | Latching channel buttons | confirmed | [channel-card](channel-card.md) |
| 55 | Channel strip panel layout | confirmed | [mechanical](mechanical.md) |
| 56 | Headphone output design | confirmed | [master-card](master-card.md) |
| 57 | Compressor detector: feed-forward log peak | confirmed | [master-card](master-card.md) |
| 58 | Output protection relays | confirmed | [master-card](master-card.md) |
| 59 | Mechanical format: desktop, rail frame | confirmed | [mechanical](mechanical.md) |
| 60 | Prototype power: DC brick, DC-DC, local regulation | confirmed | [power](power.md) |
| 61 | Grounding and chassis | confirmed | [system](system.md) |
| 62 | Separate passive input module | confirmed | [input-module](input-module.md) |
| 63 | Part numbering SX-<category>-<nnn> | confirmed | [process](process.md) |
| 64 | Soft clipping on channels and master | confirmed | [system](system.md) |
| 65 | Switchable fixed low-cut | confirmed | [channel-card](channel-card.md) |
| 66 | Sidechain ducking through channel VCAs | confirmed | [system](system.md) |
| 67 | Cutoff CV jack on the channel card | confirmed | [input-module](input-module.md) |
| 68 | 10-pin input header | confirmed | [input-module](input-module.md) |
| 69 | Stereo buttons switch through DG413 | confirmed | [system](system.md) |
| 70 | Licensing: non-commercial source-available | confirmed | [process](process.md) |
| 71 | Resonance compensation via LM13700 Q VCA | confirmed | [channel-card](channel-card.md) |
| 72 | Level sheet: SSI2162 implementation | confirmed | [channel-card](channel-card.md) |
| 73 | Low-cut at 100 Hz | confirmed | [channel-card](channel-card.md) |
| 74 | Routing sheet: buffers and bus resistors | confirmed | [channel-card](channel-card.md) |
| 75 | Buttons: GPBS850N with printed caps | confirmed | [mechanical](mechanical.md) |
| 76 | Channel meter sheet | confirmed | [channel-card](channel-card.md) |
| 77 | Test points: bare SMD pads | confirmed | [process](process.md) |
| 78 | Channel chain and power sheet | confirmed | [channel-card](channel-card.md) |
| 79 | Assembly at JLCPCB, LCSC basic parts | confirmed | [process](process.md) |
| 80 | Power injected in groups of 8 cards | confirmed | [system](system.md) |
| 81 | Separate power board | confirmed | [power](power.md) |
| 82 | Log detector: AS3046D | confirmed | [master-card](master-card.md) |
| 83 | Main outputs: THAT1646 | confirmed | [master-card](master-card.md) |
| 84 | Headphone driver: TPA6120A2 | confirmed | [master-card](master-card.md) |
| 85 | Relays: Omron G6K-2F-Y | confirmed | [master-card](master-card.md) |
| 86 | Meters use 3 mm round LEDs | confirmed | [mechanical](mechanical.md) |
| 87 | Master card power sheet | confirmed | [master-card](master-card.md) |
| 88 | AUX return implementation | confirmed | [master-card](master-card.md) |
| 89 | Compressor implementation | confirmed, parts proposed | [master-card](master-card.md) |
| 90 | Sidechain and ducking sheet | confirmed, parts proposed | [master-card](master-card.md) |
| 91 | AUX sends implementation | confirmed, parts proposed | [master-card](master-card.md) |
| 92 | Master out implementation | confirmed, parts proposed | [master-card](master-card.md) |
| 93 | Master meter implementation | confirmed, parts proposed | [master-card](master-card.md) |
| 94 | Headphones implementation | confirmed, parts proposed | [master-card](master-card.md) |
| 95 | Master card power recheck | confirmed | [master-card](master-card.md) |
| 96 | Power sizing rule: own parts worst case, shared parts typical × 1.5 plus use loads | confirmed | [system](system.md) |
| 97 | SC_ENV negative, −1 V = 10 dB, summed into the control summer's virtual earth | confirmed | [system](system.md) |
| 98 | PFL_ACT drivers and button pull-downs return to PGND | confirmed | [system](system.md) |
| 99 | Input-module cable: 1:1 KK 254 crimp cable | confirmed | [input-module](input-module.md) |
| 100 | Power board: 24 V Class II brick, non-isolated TPS54560 buck and inverter at 400 kHz, protection and output fusing | confirmed, values proposed | [power](power.md) |

## Proposed but not confirmed

(none as separate decisions; see the **[proposed]** parts of the decisions marked above)

## Open items

- [x] SSI2144 supply, headroom and noise (datasheet Rev 3.0, January 2018; facts in SPEC.md section 3)
- [x] Part availability, checked 2026-10-03 (details in the availability notes in `process.md`)
- [x] Simulate one filter channel to set the gain structure (behavioural model; `simulation/filter/README.md`)
- [ ] Breadboard one SSI2144 channel to verify the real chip's distortion, noise and output scale, and pick the drive jumper setting by ear (plan: `simulation/filter/BREADBOARD.md`)
- [x] Fader part (item 48)
- [x] Pin assignment of the 34-pin audio and 8-pin power connectors (`CHAIN.md`)
- [x] Chain voltage headroom: raised to about ±20 V nominal (item 40)
- [x] Supply rating for 16 cards (decision 96)
- [x] Master meter scale and segment count (item 49)

## Backlog

The backlog is kept in `docs/ROADMAP.md`. Items moved there by decision: channel HPF. (Cue/PFL was in the backlog but is now in the prototype.)
