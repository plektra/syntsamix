# Decision index

The decision log, split by area. Read this index, then the area file for the work at hand. Every decision keeps its global number (referenced elsewhere as "decision N" or "item N"); numbers are never reused.

| File | Area |
|---|---|
| [system.md](system.md) | System scope, signal levels, buses, cross-board functions, chain and grounding |
| [channel-card.md](channel-card.md) | Channel card |
| [channel-card-parts.md](channel-card-parts.md) | Channel card: part and mechanical choices (110-115, 117) |
| [input-module.md](input-module.md) | Input module |
| [master-card.md](master-card.md) | Master/compressor card: scope and part choices (125: DRV135, 150: hand-soldered ICs) |
| [master-card-sheets.md](master-card-sheets.md) | Master/compressor card: sheet implementations (87-95, 103, 104, 126-128, 131, 138, 144, 146-149) |
| [power.md](power.md) | Power board |
| [mechanical.md](mechanical.md) | Frame, panels, strip layout, front-panel parts |
| [process.md](process.md) | Tools, part numbering, licensing, test points, assembly, availability notes |

## Rules

- **Confirmed** decisions were agreed by the user; ask before changing one. Text marked **[proposed]** inside a decision still needs confirmation.
- New decision: next free number, appended to its area file, plus one row here. A decision that refines another says so ("refines item N").
- Interface documents are contracts between boards: `docs/CHAIN.md` (ribbons), `docs/INPUT-MODULE.md` (input header), `docs/MECHANICAL.md` (strip envelope, panels, frame). Change them only through a confirmed decision.

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
| 27 | All jacks 6.3 mm (size rule replaced by 118) | confirmed, refined | [system](system.md) |
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
| 43 | 8-segment channel meter (meter form: 119) | confirmed, refined | [channel-card](channel-card.md) |
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
| 55 | Channel strip panel layout (meter form: 119) | confirmed, refined | [mechanical](mechanical.md) |
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
| 76 | Channel meter sheet (LEDs 0805 under a printed bezel: 119) | confirmed, refined | [channel-card](channel-card.md) |
| 77 | Test points: bare SMD pads | confirmed | [process](process.md) |
| 78 | Channel chain and power sheet | confirmed | [channel-card](channel-card.md) |
| 79 | Assembly at JLCPCB, LCSC basic parts | confirmed | [process](process.md) |
| 80 | Power injected in groups of 8 cards | confirmed | [system](system.md) |
| 81 | Separate power board | confirmed | [power](power.md) |
| 82 | Log detector: AS3046D | confirmed | [master-card](master-card.md) |
| 83 | Main outputs: THAT1646 (part replaced by 125) | confirmed, refined | [master-card](master-card.md) |
| 84 | Headphone driver: TPA6120A2 | confirmed | [master-card](master-card.md) |
| 85 | Relays: Omron G6K-2F-Y | confirmed | [master-card](master-card.md) |
| 86 | Meters use 3 mm round LEDs (channel meter refined by 119) | confirmed, refined | [mechanical](mechanical.md) |
| 87 | Master card power sheet | confirmed | [master-card-sheets](master-card-sheets.md) |
| 88 | AUX return implementation | confirmed | [master-card-sheets](master-card-sheets.md) |
| 89 | Compressor implementation | confirmed | [master-card-sheets](master-card-sheets.md) |
| 90 | Sidechain and ducking sheet | confirmed | [master-card-sheets](master-card-sheets.md) |
| 91 | AUX sends implementation | confirmed | [master-card-sheets](master-card-sheets.md) |
| 92 | Master out implementation | confirmed | [master-card-sheets](master-card-sheets.md) |
| 93 | Master meter implementation | confirmed | [master-card-sheets](master-card-sheets.md) |
| 94 | Headphones implementation | confirmed | [master-card-sheets](master-card-sheets.md) |
| 95 | Master card power recheck | confirmed | [master-card-sheets](master-card-sheets.md) |
| 96 | Power sizing rule: own parts worst case, shared parts typical × 1.5 plus use loads | confirmed | [system](system.md) |
| 97 | SC_ENV negative, −1 V = 10 dB, summed into the control summer's virtual earth | confirmed | [system](system.md) |
| 98 | PFL_ACT drivers and button pull-downs return to PGND | confirmed | [system](system.md) |
| 99 | Input-module cable: 1:1 KK 254 crimp cable | confirmed | [input-module](input-module.md) |
| 100 | Power board: 24 V Class II brick, non-isolated TPS54560 buck and inverter at 400 kHz, protection and output fusing, start-up ramp | confirmed | [power](power.md) |
| 101 | Floating supply: the power ribbons' source floats from mains earth (invariant 8); mains supply to the backlog | confirmed | [system](system.md) |
| 102 | Channel fader buffer and control summer on an OPA2171 (input range includes V−) | confirmed | [channel-card](channel-card.md) |
| 103 | Master fader-law buffers and summers (U206, U306, U705) on an OPA2171 | confirmed | [master-card-sheets](master-card-sheets.md) |
| 104 | SC_ENV drive: negative DEPTH, follower fed back after 100 Ω, BAT54 clamp | confirmed | [master-card-sheets](master-card-sheets.md) |
| 105 | Input header pinout confirmed as drawn | confirmed | [input-module](input-module.md) |
| 106 | Strip envelope (35 mm pitch, card ≤ 33 mm, control area ≤ 320 mm), CV jack above CUTOFF, `MECHANICAL.md` contract | confirmed | [mechanical](mechanical.md) |
| 107 | Panel stack: PCB 10 mm below the panel, pots hold the panel, fader screwed to the panel before soldering, top-side parts ≤ 9 mm (underside: 112, 121) | confirmed, refined | [mechanical](mechanical.md) |
| 108 | Card fixing: panel on both 2020 rails, two M3 screws per end into T-nuts (now one per end, 120); PCB between the rails, ≤ 318 mm | confirmed, refined | [mechanical](mechanical.md) |
| 109 | Chain headers: master at the right end, IN on the left edge, OUT on the right edge (underside), U-loop jumpers, mock-up before the first PCB (underside rules: 121) | confirmed, refined | [mechanical](mechanical.md) |
| 110 | Channel regulators U501/U502 in D²PAK (onsemi LM317D2TR4G, LM337D2TR4G), tab on about 20 × 20 mm copper both sides | confirmed | [channel-card-parts](channel-card-parts.md) |
| 111 | Channel electrolytics to SMD at most 5.4 mm tall: ROQANG 47 µF and 10 µF 35 V (LCSC), Panasonic EEE-1VA100NP bipolar | confirmed | [channel-card-parts](channel-card-parts.md) |
| 112 | Trimmers RV101, RV151, RV182 (3296W, screws down) and jumper headers JP101, JP102, JP151, JP152, J301, J302 on the underside, set through a detachable bottom cover | confirmed (cover: 121) | [channel-card-parts](channel-card-parts.md) |
| 113 | Low-cut capacitors C9-C12: C0G 47 nF 5 % 1206 (Murata, LCSC C21812) instead of film | confirmed | [channel-card-parts](channel-card-parts.md) |
| 114 | Panel pots: Alpha 9 mm with 6 mm T18 knurled shaft, 15 mm, push-on knobs | confirmed | [channel-card-parts](channel-card-parts.md) |
| 115 | Trim stage scaled to a 100 k audio dual pot (same gain law); channel pots TRIM, CUTOFF, RESONANCE, AUX chosen (Thonk, Tayda) | confirmed; all four pots RoHS-cleared by Alpha's declaration (124) | [channel-card-parts](channel-card-parts.md) |
| 116 | RoHS (2011/65/EU + 2015/863) strict for every component and board; compliance source recorded in `parts.csv`; lead-free finish, assembly and hand soldering (invariant 9, passives, audit: 122) | confirmed, refined | [process](process.md) |
| 117 | Button LED colours (JLCPCB basic 0805: MUTE red, PFL yellow, SC SEND/DUCK/COMP BUS green, LOW-CUT/BYPASS white); chain headers Würth 61203421621 and 61200821621 | confirmed | [channel-card-parts](channel-card-parts.md) |
| 118 | Jack size by function: 6.3 mm default for audio to other gear, 3.5 mm for Eurorack-level CV/gate and where 6.3 mm does not fit; cutoff CV jack = 3.5 mm Thonkiconn | confirmed | [system](system.md) |
| 119 | Channel meter: 0805 LEDs under a printed bezel flush in one panel slot, 6.0 mm pitch, column top level with the fader top, scales independent | confirmed | [mechanical](mechanical.md) |
| 120 | Panel fixing: one centred M3 button-head screw per end plus a printed locating key in the rail slot; second screw returns if the prototype twists | confirmed | [mechanical](mechanical.md) |
| 121 | Underside: chain headers at the edges, hand-set parts (trimmers, jumpers) ≤ 10.5 mm elsewhere, 10 mm edge keep-out (provisional until the mock-up), detachable bottom cover with feet on cheeks or rails | confirmed | [mechanical](mechanical.md) |
| 122 | RoHS invariant 9; standard passives get their RoHS source at BOM time; parts.csv audit before the first PCB order | confirmed | [system](system.md) |
| 123 | Channel op amp power levers: U107 NE5532 → TL072, meter U401/U404 TL072 → TL062 | confirmed | [channel-card](channel-card.md) |
| 124 | A maker's general RoHS declaration covers its standard parts: Taiwan Alpha's RoHS II declaration clears every standard Alpha pot (channel CUTOFF, TRIM, AUX, RESONANCE; master Alpha pots once chosen); declarations kept in git-ignored `docs/rohs/` | confirmed | [process](process.md) |
| 125 | Main output driver DRV135UA replaces the end-of-life THAT1646 (same SO-8 pinout) | confirmed (delegated) | [master-card](master-card.md) |
| 126 | Master op amp power levers: U409, U410, U802, U804 TL072 → TL062 | confirmed (delegated) | [master-card-sheets](master-card-sheets.md) |
| 127 | Master electrolytics to SMD (item 111 parts); TO-220 regulators still too tall | confirmed (delegated) | [master-card-sheets](master-card-sheets.md) |
| 128 | Relay drop-out watches both raw rails (U707C on −20V_RAW) | confirmed (delegated) | [master-card-sheets](master-card-sheets.md) |
| 129 | RESONANCE pot RV183 within Alpha's 0.02 W non-B rating: R184 10 k → 12 k (about 17 mW), maximum Q current about 254 µA, provisional with R120/R170 | confirmed | [channel-card](channel-card.md) |
| 130 | Tempco leg R108/R158: end-of-life ERA-V33J102V replaced by Vishay TFPT0603L8200FV 820 Ω plus 180 Ω in series (1 k, about +3370 ppm/K); new R122/R172 | confirmed | [channel-card](channel-card.md) |
| 131 | RELEASE pot RV402 within Alpha's 0.02 W non-B rating: C10K → C100K (RD901F-40-15K-C100K) with R425 620 Ω → 6.2 kΩ, same release law, about 2 mW | confirmed | [master-card-sheets](master-card-sheets.md) |
| 132 | 6.3 mm jacks: Rean NYS216 replaces the Neutrik NMJ6HCD2 on every board (cost); new footprint, pin roles to check on the first part | confirmed (delegated) | [system](system.md) |
| 133 | Through-hole parts hand-soldered by the user; JLCPCB places SMD only (master's expensive ICs hand-soldered on the prototype: 150) | confirmed, refined | [process](process.md) |
| 134 | Component values from E24 (capacitors preferably E12/E6); each board owns its value selection and lists justified exceptions in its STATUS.md | confirmed | [process](process.md) |
| 135 | Cost principle: a live performance device, not studio equipment (what may be relaxed for cost, what must stay; the filter stays) | confirmed | [system](system.md) |
| 136 | Cost control: `/cost` and the cost-controller sub-agent, `tools/costs.py` estimate, private ledger of realized costs | confirmed | [process](process.md) |
| 137 | Prefer JLCPCB fee-free parts: basic, then preferred, then extended, then consigned; exceptions with reasons in the board STATUS.md | confirmed | [process](process.md) |
| 138 | SC LPF pot RV501: standard Alpha dual B100K (Thonk) instead of the unsourced C100K dual; same circuit, middle of the sweep 85 Hz | confirmed | [master-card-sheets](master-card-sheets.md) |
| 139 | Channel PFL/SC switch U303 a DG413 (SC send on the NC section, driven from the button's released throw); DG412 no longer used | confirmed (delegated) | [channel-card](channel-card.md) |
| 140 | Channel card values on E24 with fee-free parts: E24 pairs for the V/oct feedback and the fader law, meter ladder and filter scaling re-fitted; R217 30k1 kept (chain line) | confirmed (delegated) | [channel-card](channel-card.md) |
| 141 | Filter temperature compensation to the backlog: R108/R158 plain 820 Ω with the 180 Ω (FREQ leg still 1 k); TFPT no longer used | confirmed (delegated) | [channel-card](channel-card.md) |
| 142 | MUTE and DUCK switched by the buttons' spare pole into the control summer (10 ms ramp kept); channel U206 DG413 removed | confirmed (delegated) | [channel-card](channel-card.md) |
| 143 | Channel input receiver: TL072 difference amplifier G = ½ with 10k 0.1 % resistors instead of the AD8273 (CMRR ≥ 51.5 dB) | confirmed (delegated) | [channel-card](channel-card.md) |
| 144 | Master fader laws (AUX returns, master level) on the channel's E24 values and pairs; 30k1 kept | confirmed | [master-card-sheets](master-card-sheets.md) |
| 145 | Full-size brick: Mean Well GSM220B24-R7B (221 W, Class II, same R7B plug) instead of the GSM160B24-R7B; prototype keeps the GSM120B24-R7B | confirmed | [power](power.md) |
| 146 | Master meter ladder (16k … 120, about 0.45 mA) and R732 22k + 560R on fee-free E24 values; thresholds within 0.14 dB | confirmed | [master-card-sheets](master-card-sheets.md) |
| 147 | Compressor (R420 510k + 51k, R426 120k + 20k, GR ladder 470k/4k3) and SC LPF C503 2 × 47n C0G (Q 0.707) on fee-free parts; master TL072 symbols ST TL072CDT | confirmed (delegated) | [master-card-sheets](master-card-sheets.md) |
| 148 | AUX return receivers: TL072 difference amplifier G = ½ with 10k 0.1 % resistors instead of the AD8273 (as 143); AD8273 no longer used | confirmed | [master-card-sheets](master-card-sheets.md) |
| 149 | Compressor R421 a plain 1k on the prototype (end-of-life tempco part dropped); detector temperature compensation to the backlog | confirmed | [master-card-sheets](master-card-sheets.md) |
| 150 | Master DG413, SSI2162, DRV135UA and AS3046D hand-soldered on the prototype (Assembly field, refines 133); potential single point of failure kept in the backlog | confirmed | [master-card](master-card.md) |

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

The backlog is kept in `docs/ROADMAP.md`. Items moved there by decision: channel HPF; mains supply, an external linear box or an internal supply (decision 101). (Cue/PFL was in the backlog but is now in the prototype.)
