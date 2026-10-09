# Roadmap

## Phases

1. **Specification** *(done: spec v0.7, decisions 1-69, chain pinouts in CHAIN.md, input module interface in INPUT-MODULE.md)*. Supply rating for 16 cards settled by decision 96 (system decisions 96-99 settle the 2026-10-06 system validation)
2. **Simulation and breadboard**: filter simulated in ngspice *(done, `simulation/filter/`)*; channel fader law and ducking *(done, `simulation/level/`)*; SSI2144 breadboard *(parts ordered; plan, schematic, layout and BOM in `simulation/filter/`)*. compressor side chain and sidechain/ducker simulated in ngspice *(done, `simulation/compressor/`, `simulation/sidechain/`)*. Later: VCA and compressor detector on the breadboard, sidechain LPF
3. **Input module** (`hardware/input-module-6p3`): schematic *(done, ERC clean)*, then PCB
4. **Channel card** (`hardware/channel-card`): schematic *(done)*, mechanical parts *(chosen 2026-10-09, decisions 110-122; pots wait for RoHS declarations; meter LED swap to draw)*, then PCB
   - Input: header, AD8273 receiver, trim with soft clip, 100 Hz low-cut, DG413 switching *(done, ERC clean apart from sheet links)*
   - Filter: 2x SSI2144, LM13700 Q VCA (resonance compensation), cutoff summer and CV, drive and compensation jumpers, DG413 bypass *(done, ERC clean apart from sheet links; output scale and Q limit provisional until the breadboard)*
   - Level: SSI2162 VCA, 3-segment fader law, DG413 mute and DUCK *(done, ERC clean apart from sheet links)*
   - Routing: pre-fader buffers, AUX sends with pre/post jumpers, bus assign, PFL and SC send, PFL_ACT driver *(done; outputs wait for the Meter and Chain sheets)*
   - Meter: 8-segment peak meter (full-wave superdiode peak detector, LM339 comparators) *(done)*
   - Chain and power: ribbon connectors, ±15 V regulation, +5 V logic supply, test pads for the rails and PGND *(done; schematic complete, ERC 0 errors 0 warnings)*
5. **Master/compressor card** (`hardware/master`): schematic sheet by sheet *(schematic complete: ten sheets, ERC 0/0; decisions 97, 98, 103, 104 drawn)*, then PCB
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

- Main balanced outputs: THAT1646 line drivers → NE5532 buffer + inverter (decision 83)

## Power-cut candidates

From `/system power conversion` (2026-10-08). About three-quarters of the supply current is op amp quiescent current; the NE5532s in the core audio path stay. Supply currents per amplifier, typical / maximum (TI datasheets): NE5532 3 / 8 mA, TL072 1.4 / 2.5 mA, TL062 0.2 / 0.25 mA, OPA1678 2 / 2.5 mA.

1. **[proposed]** Channel U107 (cutoff CV summer, one unit unused): NE5532 → TL072. Saves 3.2 / 11 mA per rail per card; DC accuracy improves (FET input bias into 100-300 kΩ)
2. **[proposed]** TL072 → TL062 in DC control and meter stages with light loads, after a check per position (TL062: ±10 V minimum swing into 10 kΩ, input range 4 V inside the rails, about 10 mA output; not for peak detectors, comparators or the SC_ENV driver). Candidates: channel U205, U401, U404 (U204 is an OPA2171 since decision 102); master fader-law superdiodes (U207, U307, U706; U206, U306, U705 are OPA2171s since decision 103), compressor U407, U409, U410, meter U802, U804. Saves 2.4 / 4.5 mA per package
3. Later cost choice: NE5532 → OPA1678 in low-noise-gain audio stages (channel U3, U106; master U205, U305, U404, U405). Saves 2 / 11 mA per package with equal or better audio; costs more (price not checked)

Options 1 and 2 save about 68 mA per rail on the prototype (about 2.7 W of 30 W typical) and 193 mA at full size (about 7.7 W of 84 W), and cut the channel card's worst-case LM317 dissipation from 1.22 W to about 1.10 W (recomputed after decision 102 took U204 off the list). NE5532 → TL072 in audio stages was rejected (measurably more noise and distortion).

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
