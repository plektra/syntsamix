# Roadmap

## Phases

1. **Specification**: finalize SPEC.md, block diagram, chain pinouts; close the open items in DECISIONS.md *(in progress)*
2. **Simulation**: ngspice or breadboard for the critical blocks: ladder filter gain structure and noise, VCA, compressor detector with sidechain LPF
3. **Channel card**: schematic, then PCB
4. **Master/compressor card**: schematic, then PCB
5. **Power input section** (DC brick input, DC-DC to ±20 V, protection; on the master card or a small card beside it)
6. **Prototype build and measurement** against the targets in SPEC.md section 5

## Backlog (after the prototype)

- Channel HPF
- Digital output per channel for recording: ADAT or similar
- More input modules (the interface exists from the prototype, `INPUT-MODULE.md`): 3.5 mm, D-SUB bundle, XLR
- More CV control options
- Pre-fader direct output per channel for multitrack recording (needs a pin or connector beyond the 8-pin input header)
- Momentary buttons with flip-flop logic and LEDs instead of latching switches, enabling CV/MIDI control and mute groups over the spare chain lines
- Insert points on the channel strips
- Microphone channel strip: mic preamp input (XLR) for vocals or acoustic sources
- Mixer variant with external channel strips, for bands or groups of performers who each connect and control their own instrument submix

## KiCad workflow

- One KiCad project per module; hierarchical sheets inside a module for sub-blocks (input stage, filter, VCA, AUX sends)
- Custom symbols and footprints live in `hardware/libs/`
- Edit schematics and PCBs through the KiCad MCP server; pause for the user's review before each commit
- Run ERC after schematic changes and DRC after layout changes
- Keep a BOM export per module
- Keep simulation netlists and results in `simulation/`

## Design cautions

- Ladder filters need low-level signals; do the gain structure before layout
- L/R filter tracking needs a per-chip offset trim and a temperature-compensating resistor close to each SSI2144; plan layout accordingly
- 8 filter cores means significant board area per channel card
- Verify every part's pinout, footprint and limits against its datasheet
