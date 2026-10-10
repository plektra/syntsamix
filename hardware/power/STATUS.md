# Power board status

Updated 2026-10-11 (power schematic session: decisions 156-159).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: four sheets (input and clock, +20 V buck, −20 V inverter, outputs), every netlist check 0 problems, ERC 0 errors 0 warnings (decision 100; start-up ramp on both converters). Every part is chosen and every value is E24 (decisions 156, 158); the power switch is a rear-panel rocker wired to J102 (decision 157); D201 sits on an SMA footprint (decision 159). Cost levers all closed (`CHECKLISTS.md`).
- Cost (2026-10-11, `tools/costs.py estimate`): €764 / €1,045 / €1,641 for 4 / 8 / 16 channels, down about €20 per build with decisions 156-159 (six fee types fewer on this board, cheap rocker); the 240k feedback resistor is the board's only extended resistor.
- Converter values derived in `scripts/design.py`; LC filter simulated (about 47 dB at 400 kHz at the filter, 63 dB at the cards; peaking about 4.4 dB near 4 kHz).
- PCB: not started.

## Waiting for the user's confirmation

(none)

## Next

1. PCB layout (after the channel card PCB, per `docs/CONTINUE-FROM-HERE.md`).
2. Full-size supply (about 4 A per rail) after the prototype cards are measured (decision 96): the −20 V inverter needs a controller with external MOSFETs.

## RoHS

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; invariant 9 (decision 122); standard passives get their source when the BOM is fixed; the audit of this board's registered parts runs before the first PCB order (`docs/CONTINUE-FROM-HERE.md`).

## For /system

- Rear panel (`/system mechanical`, decision 157): the power rocker Legion SS11-BBIWG-R20-R needs a rectangular cutout of 19.2 × 12.9 mm (0.8-1.2 mm panel; 19.4 for 1.3-2.0 mm, 19.8 for 2.1-2.5 mm) on the rear panel near the power board, beside the brick jack. Decision 100 had a board-mounted switch at the rear edge.
