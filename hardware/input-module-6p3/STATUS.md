# Input module status

Updated 2026-10-18 (/cost input-module-6p3: IDC ribbon input cable, decision 180). 2026-10-17 (/system: ready-made input cable, decision 179). 2026-10-13 (/system: exhaust slots in the rear strip, decision 167). 2026-10-11 (/system mechanical: decision 160).

- Schematic done, ERC clean, with the 1×10 KK 254 header J3 (decisions 68, 105) and the Rean NYS216 jacks J1, J2 (decision 132, kept by the user 2026-10-18).
- Cable to the channel card: a self-made IDC ribbon on shrouded box headers replaces the ready-made Molex lead (decision 180, direction confirmed). Header size (2x6 proposed), the pin mapping, keying against the 8-pin power socket and unlatched headers are **[proposed]** and wait for a `/system` session; until then the drawn KK header stands.
- Cost (2026-10-18): €6.69 per board in parts as drawn (Molex lead and KK header repriced from Mouser); estimate €828 / €1,105 / €1,741 at 4 / 8 / 16 channels, before the ribbon saving of decision 180 (about €17 / €34 / €69) is counted.
- PCB: not started. Layout per decision 160 (`docs/MECHANICAL.md`, Rear and input module); checks in `CHECKLISTS.md`.

## Next

1. `/system input-cable` (before the channel card layout): settle decision 180's details, update `docs/INPUT-MODULE.md`, register the box header, IDC socket and ribbon in `docs/parts.csv` (with RoHS sources) and `docs/costs/prices.csv`, and replace the KK footprints on this board and the channel card.
2. Then redraw J3 here through the KiCad MCP server and run ERC.
3. PCB after the channel card PCB (`docs/CONTINUE-FROM-HERE.md`).

## For /system

- Decision 180's open details (above): 2x6 against 2x7, 105's pinout on 12 pins (spare pins as grounds), keying so a 2x4 power socket cannot seat in the 2x6 shroud (Adam Tech drawing not read), latches, RoHS for the Adam Tech and 3M parts. Prices found: `docs/reviews/2026-10-18-cost-input-module-6p3.md`.
- At layout: report the module's height and whether the rear bottom angle clears the lower jack and slots (decision 167).
