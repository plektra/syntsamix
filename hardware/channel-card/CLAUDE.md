# Channel card

KiCad project `channel-card.kicad_pro`: one stereo channel. Decisions: `docs/decisions/channel-card.md` and `channel-card-parts.md` (and `system.md` for the chain and cross-board functions). Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

- Sheets: Input, Filter, Level, Routing, Meter, Chain and power. Generators and the full rebuild how-to: `scripts/README.md`; rebuild and check everything with `scripts/rebuild_all.sh`.
- `rebuild_all.sh` regenerates every sheet with new UUIDs: restore the unchanged sheets and the root (`git checkout -- <files>`), then rerun `check_netlist.py` and ERC, so commits stay focused (as on the master).
- The shared sheet tools live in `scripts/` here; the master card symlinks to them, so a change here affects both projects. Rerun both projects' checks after editing one.
- Filter facts (SSI2144 Rev 3.0) are in `docs/SPEC.md` section 3; the simulation behind the gain structure is in `simulation/filter/`.
- Layout cautions: keep each SSI2144's offset trim and tempco resistor close to the chip; 8 filter cores need significant board area.
- Panel stack: top-side parts at most 9 mm under the panel (decision 107); trimmers and jumper headers go on the underside, adjustable through the bottom cover (decision 112); chain headers on the underside at the edges (decision 109). Chosen parts and open checks: `STATUS.md`.

## Filter

24 dB/oct (4-pole) ladder LPF, resonance on the LPF only. Not required to be Moog-style.
- Baseline: Sound Semiconductor SSI2144 (SSM2044 reissue). Datasheet Rev 3.0 facts are recorded in `docs/SPEC.md` section 3
- Fallback: AS3320 / V3320 (CEM3320 clone)
- Gain structure: "hot" drive at the datasheet nominal level by default, a prototype jumper for medium drive, per-channel bypass, half resonance compensation through the datasheet's LM13700 Q VCA (jumper: none/half/full). Simulation in `simulation/filter/`
- Sold by synth-DIY resellers (Electrokit, Thonk), not by Mouser or DigiKey.

## Component values and parts (decisions 134, 137)

This board owns its value selection. Choose every resistor and capacitor value from the E24 series (capacitors preferably E12 or E6). Keep a value outside E24 only where the circuit needs a ratio or accuracy that E24 values cannot give, singly or as a pair of E24 parts, and list it with its references and reason in `CHECKLISTS.md`, "Component values". Review that list before layout and after any value change. Each value outside the JLCPCB basic library costs a $3 fee per type per order.

Parts (decision 137): for every SMD part JLCPCB places, take a JLCPCB basic part first, then a "preferred" part (no fee), then another LCSC extended part, and a part LCSC does not stock only as a last resort. Another maker's basic part with the same function is fine once its datasheet confirms pinout, package and limits. Record each part that still costs a fee, with its reason, in `CHECKLISTS.md`; `python3 tools/costs.py extended` lists them.
