# Power board status

Updated 2026-10-13 (/system: ventilation, decision 167). 2026-10-11 (/system mechanical: power bay and two module sizes, decision 162; power schematic session: decisions 156-159).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: four sheets (input and clock, +20 V buck, −20 V inverter, outputs), every netlist check 0 problems, ERC 0 errors 0 warnings (decision 100; start-up ramp on both converters). Every part is chosen and every value is E24 (decisions 156, 158); the power switch is a rear-panel rocker wired to J102 (decision 157); D201 sits on an SMA footprint (decision 159). Cost levers all closed (`CHECKLISTS.md`).
- Cost (2026-10-11, `tools/costs.py estimate`): €764 / €1,045 / €1,641 for 4 / 8 / 16 channels, down about €20 per build with decisions 156-159 (six fee types fewer on this board, cheap rocker); the 240k feedback resistor is the board's only extended resistor. Merged with the button price and the JLCPCB fee model fix (fees per design at $3.07) and Thonk volume breaks: €778 / €1,040 / €1,600.
- Converter values derived in `scripts/design.py`; LC filter simulated (about 47 dB at 400 kHz at the filter, 63 dB at the cards; peaking about 4.4 dB near 4 kHz).
- PCB: not started.

## Waiting for the user's confirmation

(none)

## Next

1. PCB layout (after the channel card PCB, per `docs/CONTINUE-FROM-HERE.md`) in the power bay form of decision 162 (`docs/MECHANICAL.md`, Power bay): the board stands on edge in the front-to-back plane, outline up to about 300 × 35 mm following the panel slope (about 6°), hung from the bay's top strip on two brackets and fixed at its rear edge to the bay's rear strip, which carries the brick jack J101 (KPJX-4S, right angle, pointing back) and the rocker (cutout 19.2 × 12.9 mm for 0.8-1.2 mm, 19.4 mm for 1.3-2.0 mm). Insulating mounting, no PGND to the frame. Ventilation (decision 167): the board's loss (about 4 W prototype, 10 W full size at an assumed 88 %, `tools/heat_budget.py`) shares the unit's air; give the bay's rear strip exhaust slots where the jack and rocker leave room (about 2 cm², `docs/MECHANICAL.md` Ventilation), and report the converters' real efficiency from `scripts/design.py` or the TPS54560 datasheet so the 88 % estimate can go. The power LED is not visible on a fin: bring it to the bay's top strip (light pipe or a wired LED; check the schematic). Ribbons: master header and chain 1 to the left (chain 1 into the power OUT header of the channel card next to the master), chain 2 about 0.5 m along the rear floor.
2. **Two power module sizes (decision 162, the user's plan for cheaper small units):** one module for up to 8 channel cards (master + chain 1; the present design, 120 W brick; the chain 2 header and its two fuses could be left off) and a larger one for full size. Same bay, same ribbons. Decide in a power board session whether the small module simply omits the chain 2 parts.
3. Full-size supply, the larger module (about 4 A per rail) after the prototype cards are measured (decision 96): the −20 V inverter needs a controller with external MOSFETs.

## RoHS

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; invariant 9 (decision 122); standard passives get their source when the BOM is fixed; the audit of this board's registered parts runs before the first PCB order (`docs/CONTINUE-FROM-HERE.md`).

## For /system

(none; decision 162 put the rocker and the brick jack on the power bay's rear strip)
