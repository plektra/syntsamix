# Input module status

Updated 2026-10-17 (/system: ready-made input cable, decision 177). 2026-10-13 (/system: exhaust slots in the rear strip, decision 167). 2026-10-11 (/system mechanical: decision 160).

- Schematic done, ERC clean. Header pinout confirmed as drawn (decision 105); no change needed.
- Cable to the channel card (decision 177, `docs/INPUT-MODULE.md`, Cable): ready-made Molex 217796-1101, 150 mm, male headers stay on both boards; check its 1:1 wiring on the Molex sales drawing or with a meter on delivery. Hand crimping (decision 99) is the fallback.
- PCB: not started. Layout per decision 160 (`docs/MECHANICAL.md`, Rear panel and input module): the PCB stands on edge under the rear rail, J1 (L/MONO) above J2 (R) about 19 mm between centres, module about 40 mm tall, centred on the 35 mm strip, fixed only by the jack nuts on its rear strip; KK header facing forward. The rear strip (34.8 mm FR4 panel with the two 11.4 mm cut-outs and legends) is drawn with this board; it carries the exhaust slots of decision 167 (`docs/MECHANICAL.md`, Ventilation): four routed slots 2 × 30 mm in the jack zone, two beside each jack nut, legends and the top screw on the 20 mm in front of the rail. Measure the NYS216 nut (taken as about 15 mm across). Check that the rear bottom angle (decision 160, 20 × 20 mm) clears the lower slots and the lower jack's body; if not, propose to /system an angle under the jack zone or a shorter leg. Report the module's final height to /system: it sets the rear inside height (about 60 mm).

## Cost (2026-10-09)

- Jacks J1 and J2 are now Rean NYS216 (SX-CONN-015, decision 132) instead of the Neutrik NMJ6HCD2: about €3.50 per module in parts instead of about €6. Footprint `syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal` (rows 16.50 mm apart, panel cut-out 11.4 mm); its pin roles are inferred, so check them with a meter on the first delivered jack before ordering this PCB. ERC 0/0 after the change.
- Hand-soldered by the user, like every through-hole part (decision 133).
- Remaining cost: the ready-made KK 254 cable (about €5, decision 177; hand crimping about €1.50 is the fallback). No further lever proposed.
- Component values (decision 134): this board has no resistors or capacitors; the rule in `CLAUDE.md` applies if any are added.

## RoHS

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; invariant 9 (decision 122); standard passives get their source when the BOM is fixed; the audit of this board's registered parts runs before the first PCB order (`docs/CONTINUE-FROM-HERE.md`).

## For /system

- Cost check before the channel card layout (the user, 2026-10-17; `docs/ROADMAP.md`, Cost-cut candidates item 8): a simple input module with a self-made IDC ribbon (2x6 or 2x7 box headers, not 2x5: decision 41) against the ready-made Molex lead of decision 177, for cost and manual work. Run it through `/cost input-module-6p3`; a header change is a /system decision.

- At layout: report the module's height and whether the rear bottom angle clears the lower jack and slots (decision 167).
