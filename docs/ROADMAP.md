# Roadmap

## Phases

1. **Specification** *(done: spec v0.7, decisions 1-69, chain pinouts in CHAIN.md, input module interface in INPUT-MODULE.md)*. Still open: supply rating for 16 cards
2. **Simulation and breadboard**: filter simulated in ngspice *(done, `simulation/filter/`)*; SSI2144 breadboard *(parts ordered; plan, schematic, layout and BOM in `simulation/filter/`)*. Later: VCA and compressor detector with sidechain LPF
3. **Input module** (`hardware/input-module-6p3`): schematic *(done, ERC clean)*, then PCB
4. **Channel card** (`hardware/channel-card`): schematic sheet by sheet *(in progress)*, then PCB
   - Input: header, AD8273 receiver, trim with soft clip, 150 Hz low-cut, DG413 switching *(done, ERC clean apart from sheet links)*
   - Filter: 2x SSI2144, LM13700 Q VCA (resonance compensation), cutoff summer and CV, drive and compensation jumpers, DG413 bypass *(done, ERC clean apart from sheet links; output scale and Q limit provisional until the breadboard)*
   - Level: SSI2162 VCA, 3-segment fader law, DG413 mute and DUCK *(done, ERC clean apart from sheet links)*
   - Routing: AUX sends, bus assign, PFL and SC send taps, chain bus drivers
   - Meter: 8-segment peak meter
   - Chain and power: ribbon connectors, ±15 V regulation, +5 V logic supply
5. **Master/compressor card**: schematic, then PCB
5. **Power input section** (DC brick input, DC-DC to ±20 V, protection; on the master card or a small card beside it)
6. **Prototype build and measurement** against the targets in SPEC.md section 5

## Backlog (after the prototype)

- Channel HPF
- Digital output per channel for recording: ADAT or similar
- More input modules (the interface exists from the prototype, `INPUT-MODULE.md`): 3.5 mm, D-SUB bundle, XLR
- More CV control options
- Pre-fader direct output per channel for multitrack recording (input header pins 8 and 9 already reserved; jacks on the input module)
- Momentary buttons with flip-flop logic and LEDs instead of latching switches, enabling CV/MIDI control and mute groups over the spare chain lines
- Insert points on the channel strips
- Microphone channel strip: mic preamp input (XLR) for vocals or acoustic sources
- Expansion to 32 channels: power injector board every 16 cards (the 8-pin power ribbon carries only about 16 cards' current), mixing amps sized for 32 inputs (about 3 dB more bus noise), two frames of 16 strips linked by a longer ribbon. Channel cards and pinouts stay unchanged
- Mixer variant with external channel strips, for bands or groups of performers who each connect and control their own instrument submix

## KiCad workflow

- One KiCad project per module; hierarchical sheets inside a module for sub-blocks (input stage, filter, VCA, AUX sends)
- Custom symbols and footprints live in `hardware/libs/`
- Large sheets: describe the circuit in a script and send it to `sch_build_circuit` through an MCP stdio client; keep same-axis two-pin parts at least about 25 mm apart, or their label stubs touch and short nets. Then remove the builder's PWR_FLAGs (the Input sheet already flags the rails) and check the exported netlist against the intended nets and for duplicate references across sheets (ERC does not flag them). Reference blocks: Input 1-99, Filter 101-199 (decoupling C191-C206), Level 201-299 (capacitors from C221)
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
