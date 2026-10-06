# Channel card

KiCad project `channel-card.kicad_pro`: one stereo channel. Decisions: `docs/decisions/channel-card.md` (and `system.md` for the chain and cross-board functions). Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

- Sheets: Input, Filter, Level, Routing, Meter, Chain and power. Generators and the full rebuild how-to: `scripts/README.md`; rebuild and check everything with `scripts/rebuild_all.sh`.
- The shared sheet tools live in `scripts/` here; the master card symlinks to them, so a change here affects both projects. Rerun both projects' checks after editing one.
- Filter facts (SSI2144 Rev 3.0) are in `docs/SPEC.md` section 3; the simulation behind the gain structure is in `simulation/filter/`.
- Layout cautions: keep each SSI2144's offset trim and tempco resistor close to the chip; 8 filter cores need significant board area.

## Filter

24 dB/oct (4-pole) ladder LPF, resonance on the LPF only. Not required to be Moog-style.
- Baseline: Sound Semiconductor SSI2144 (SSM2044 reissue). Datasheet Rev 3.0 facts are recorded in `docs/SPEC.md` section 3
- Fallback: AS3320 / V3320 (CEM3320 clone)
- Gain structure: "hot" drive at the datasheet nominal level by default, a prototype jumper for medium drive, per-channel bypass, half resonance compensation through the datasheet's LM13700 Q VCA (jumper: none/half/full). Simulation in `simulation/filter/`
- Sold by synth-DIY resellers (Electrokit, Thonk), not by Mouser or DigiKey.
