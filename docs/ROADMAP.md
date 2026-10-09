# Roadmap

## Phases

1. **Specification** *(done: spec v0.7, decisions 1-69, chain pinouts in CHAIN.md, input module interface in INPUT-MODULE.md)*. Supply rating for 16 cards settled by decision 96 (system decisions 96-99 settle the 2026-10-06 system validation)
2. **Simulation and breadboard**: filter simulated in ngspice *(done, `simulation/filter/`)*; channel fader law and ducking *(done, `simulation/level/`)*; SSI2144 breadboard *(parts ordered; plan, schematic, layout and BOM in `simulation/filter/`)*. compressor side chain and sidechain/ducker simulated in ngspice *(done, `simulation/compressor/`, `simulation/sidechain/`)*. Later: VCA and compressor detector on the breadboard, sidechain LPF
3. **Input module** (`hardware/input-module-6p3`): schematic *(done, ERC clean)*, then PCB
4. **Channel card** (`hardware/channel-card`): schematic *(done)*, mechanical parts *(chosen 2026-10-09, decisions 110-122; pots RoHS-cleared by Alpha's declaration, decision 124; meter LEDs drawn)*, then PCB
   - Input: header, AD8273 receiver, trim with soft clip, 100 Hz low-cut, DG413 switching *(done, ERC clean apart from sheet links)*
   - Filter: 2x SSI2144, LM13700 Q VCA (resonance compensation), cutoff summer and CV, drive and compensation jumpers, DG413 bypass *(done, ERC clean apart from sheet links; output scale and Q limit provisional until the breadboard)*
   - Level: SSI2162 VCA, 3-segment fader law, DG413 mute and DUCK *(done, ERC clean apart from sheet links)*
   - Routing: pre-fader buffers, AUX sends with pre/post jumpers, bus assign, PFL and SC send, PFL_ACT driver *(done; outputs wait for the Meter and Chain sheets)*
   - Meter: 8-segment peak meter (full-wave superdiode peak detector, LM339 comparators) *(done)*
   - Chain and power: ribbon connectors, ±15 V regulation, +5 V logic supply, test pads for the rails and PGND *(done; schematic complete, ERC 0 errors 0 warnings)*
5. **Master/compressor card** (`hardware/master`): schematic sheet by sheet *(schematic complete: ten sheets, ERC 0/0; decisions 97, 98, 103, 104 drawn; pre-layout parts session 2026-10-09, decisions 125-128)*, then PCB (after `/system mechanical` on the master section)
6. **Power board** (`hardware/power`, decisions 81, 100): 24 V brick input, protection, non-isolated TPS54560 buck and inverter to ±20 V; *(schematic complete, ERC 0 errors 0 warnings)*, then PCB
7. **Prototype build and measurement** against the targets in SPEC.md section 5

## Backlog (after the prototype)

- Channel HPF
- Digital output per channel for recording: ADAT or similar
- More input modules (the interface exists from the prototype, `INPUT-MODULE.md`): 3.5 mm, D-SUB bundle, XLR
- More CV control options
- Pre-fader direct output per channel for multitrack recording (input header pins 8 and 9 already reserved; jacks on the input module)
- Momentary buttons with flip-flop logic and LEDs instead of latching switches, enabling CV/MIDI control and mute groups over the spare chain lines. Must keep button states through a power cycle (for example after a power cut during a gig), so the states need non-volatile storage (FRAM or microcontroller EEPROM) restored at power-up
- Insert points on the channel strips
- Microphone channel strip: mic preamp input (XLR) for vocals or acoustic sources
- Expansion to 32 channels: power injector board every 16 cards (the 8-pin power ribbon carries only about 16 cards' current), mixing amps sized for 32 inputs (about 3 dB more bus noise), two frames of 16 strips linked by a longer ribbon. Channel cards and pinouts stay unchanged
- (Done for the channel meter in the prototype, decision 119; the master meter may follow) 3D-printed LED bar diffuser for the meters: an opaque printed bezel with square windows (for example 4 x 4 mm at 5 mm pitch) and a translucent diffuser over 0805 SMD LEDs, replacing the round 3 mm meter LEDs (decision 86). Same look as the printed button caps; walls between the windows stop light bleeding between segments
- Mains power (decision 101): an external linear supply box (mains and toroid in their own earthed box, ±20 V on a locking connector; the power board shrinks to protection and fusing) or an internal mains supply (Class I, safety earth to the chassis, ground lift between signal ground and chassis). Either must keep the supply output floating (invariant 8)
- Mixer variant with external channel strips, for bands or groups of performers who each connect and control their own instrument submix
- Longer-life channel fader (decision 48): TT Electronics PS60-10MC2BR10K (PSxx Issue B, 11/2020): same 75 × 9 × 6.5 mm body, M2 holes 71 mm apart and 15 mm metal lever as the PTA6043, rated 100,000 cycles instead of 15,000; check its pin pattern against the PTA footprint. A factory order at Mouser (3,600 minimum, about 1.25 € each, 2026-10-09); the 20 and 25 mm lever versions (MC4, MC5) would allow a taller panel gap (decision 107) if the pots change too

## Cost-cut candidates

Decisions that can fall back to a cheaper option if the budget needs it:

- Main balanced outputs: THAT1646 line drivers → NE5532 buffer + inverter (decision 83; the THAT1646 is now the DRV135UA, decision 125, about €3.40 each)

### Cost review 2026-10-09

The user asked for a large cost cut (2026-10-09), then set the frame: the prototype is 4 channels, maybe only 2 (first trial-and-error versions of the channel design); the cost of a full 16-channel console must stay in view in case it becomes a commercial product; the ladder filter stays, being the feature that sets this mixer apart. Prices below are rough, before VAT and shipping, from the four schematic BOMs (20-50 pieces; LCSC and Mouser checks on 2026-10-09 for the DG413DY, DRV135UA, PTA6043 and the jacks, the rest estimated, so ±25 %). Through-hole parts are hand-soldered by the user (decision 133).

**Figures from `tools/costs.py` (decision 136), 2026-10-09:** the schematic BOMs priced from `docs/lcsc-check.csv` and `docs/costs/prices.csv`, with the overheads in `docs/costs/overheads.csv`. About a third of the part prices and every overhead figure are estimates (marked in those files), so treat the totals as ±25 %. Rerun `python3 tools/costs.py estimate --channels N` for current figures.

| Build | Total |
|---|---|
| Prototype, 2 channels | ~€960 |
| Prototype, 4 channels | ~€1,115 |
| Full console, 16 channels, ordered like the prototype | ~€2,110 |

The 4-channel prototype in detail:

| Item | EUR |
|---|---|
| Channel card parts (4 boards, about €65 each) | 261 |
| Input module parts (4) | 7 |
| Master parts (JLCPCB assembles at least 2 boards per design, so a second set of SMD parts) | 182 |
| Power board parts (2 assembled) | 30 |
| JLCPCB fees (82 extended or consigned types, 3 assembled designs, placements) | 343 |
| PCBs | 75 |
| FR4 panels | 55 |
| Frame, hardware, ribbons, 24 V brick | 110 |
| Knobs and fader caps | 22 |
| Consigned parts handling | 30 |
| **Total** | **1,115** |

These replace the first hand estimate of the same day (prototype about €1,450, console about €2,600), which guessed about 130 extended part types (the BOMs have 82 once JLCPCB's fee-free "preferred" parts are counted, decision 137) and a higher channel card cost (about €75; the BOMs give about €65). Includes decisions 130 and 131 (TFPT tempco pair, RELEASE C100K). At prototype size the JLCPCB fees are about a third of the cost; at 16 channels the channel cards are about half. The full-size power board still needs its 4 A design (or power lever 1).

**As a product:** at production volume the set-up and extended-part fees spread over many units and the per-channel parts become the cost, together with labour: through-hole assembly (hand-soldered here, decision 133, not in a product) and calibration (three trimmers per channel: CUTOFF OFFSET ×2 and V/OCT, plus the TRIM and drive/Q jumpers). Per-channel levers therefore count sixteen times per console, and anything that removes a trimming step saves labour on every channel.

Levers [proposed] (board details in each `STATUS.md`, "Cost-cut levers"):

*For the prototype (fixed costs):*

1. **JLCPCB fees:** one order for all boards (shared part types pay their fee once), and fewer extended types: JLCPCB basic or preferred (fee-free) parts wherever one fits (decision 137; candidates in each board's `STATUS.md`, all types with a fee from `python3 tools/costs.py extended`). Value selection is each board's job (decision 134: E24 by default, justified exceptions listed in the board's `STATUS.md`, "Component values"; now 25 types on the channel card, 23 on the master, 4 on the power board). Up to about €100-150 per order.
2. **The second master and power board:** JLCPCB's two-board minimum buys a spare; place only one fully and leave the spare for repair, or hand-place the spare's SMD parts later. Check JLCPCB's current minimum and partial-assembly options when ordering.
3. **Start with 2 channels:** about €150 less, at the cost of not testing 3- and 4-card chain effects (bus noise, chain current).

*For the full console and a product (per channel, ×16):*

4. **Op-amp receivers instead of the AD8273** (channel and AUX returns): about €4.50 per channel (€80 at 16) and one part fewer to consign; costs CMRR and needs the input stage checked again.
5. **Fewer DG413s** (4 per channel, about €1.90 each) by using VCA control for mute and DUCK: about €2-4 per channel.
6. **Cheaper trimmers** than the Bourns 3296W: about €4 per channel; and for a product, fewer trimmers (each is a calibration step).
7. Done: Rean NYS216 jacks instead of the Neutrik NMJ6HCD2 (decision 132), about €1.15 per jack. For a product, recheck the 1,000-cycle rating against the inputs' expected use (the Neutrik is rated over 10,000).

Rejected by the user (2026-10-09): **the filter as a fitting option** (about €25 per channel). The SSI2144 ladder filter is one of the essential features that make this mixer stand out; it stays on every channel.

## Power-cut candidates

From `/system power conversion` (2026-10-08). About three-quarters of the supply current is op amp quiescent current; the NE5532s in the core audio path stay. Supply currents per amplifier, typical / maximum (TI datasheets): NE5532 3 / 8 mA, TL072 1.4 / 2.5 mA, TL062 0.2 / 0.25 mA, OPA1678 2 / 2.5 mA.

1. **Done on the channel card (decision 123):** Channel U107 (cutoff CV summer, one unit unused): NE5532 → TL072. Saves 3.2 / 11 mA per rail per card; DC accuracy improves (FET input bias into 100-300 kΩ)
2. **Done (decisions 123, 126):** channel U401, U404 and master U409, U410, U802, U804 TL072 → TL062; the superdiodes (channel U205, master U207, U307, U706) and the master's log-detector U407 stay TL072. Master saves about 9.6 mA per rail typical
3. Later cost choice: NE5532 → OPA1678 in low-noise-gain audio stages (channel U3, U106; master U205, U305, U404, U405). Saves 2 / 11 mA per package with equal or better audio; costs more (price not checked)

The channel share is done: decision 123 cut the card from 121 / 103 to 113 / 95 mA typical (the budget in `ARCHITECTURE.md` includes it). The master's share is done too: decision 126 moved four packages (about 9.6 mA per rail typical; master 340 / 269 → 331 / 260 mA with decision 125); `ARCHITECTURE.md` still shows the old master figures until `/system` reruns the budget. NE5532 → TL072 in audio stages was rejected (measurably more noise and distortion).

## KiCad workflow

- One KiCad project per module; hierarchical sheets inside a module for sub-blocks (input stage, filter, VCA, AUX sends)
- Custom symbols and footprints live in `hardware/libs/`
- Sheets are generated by scripts in `hardware/channel-card/scripts/` and drawn with real wires inside each circuit block (labels only between blocks); every rebuild is checked pin by pin against a separate reference netlist. See the scripts README
- Edit schematics and PCBs through the KiCad MCP server (kicad-mcp-pro, profile `schematic_authoring`); pause for the user's review before each commit
- The server's circuit builder connects nets by labels and cannot handle multi-unit symbols (dual op amps, DG413): build with temporary references per unit, then rename them in the file, and verify with ERC plus a netlist check against the intended nets
- Shared project symbols: `hardware/libs/syntsamix.kicad_sym` (AD8273, SSI2144, SSI2162), registered in each project's `sym-lib-table`
- Give every placed symbol the BOM fields in `docs/PART-NUMBERING.md`
- Run ERC after schematic changes and DRC after layout changes
- Keep a BOM export per module
- Keep simulation netlists and results in `simulation/`

## Design cautions

- Ladder filters need low-level signals; do the gain structure before layout
- L/R filter tracking needs a per-chip offset trim and a temperature-compensating resistor close to each SSI2144; plan layout accordingly
- 8 filter cores means significant board area per channel card
- Verify every part's pinout, footprint and limits against its datasheet
