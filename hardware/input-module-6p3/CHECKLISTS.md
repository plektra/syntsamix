# Input module: checklists and reference

Read for layout, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

## Check before layout

- **Placement (decision 160, `docs/MECHANICAL.md`, Rear panel and input module):** the PCB stands on edge under the rear rail, J1 (L/MONO) above J2 (R) about 19 mm between centres, module about 40 mm tall, centred on the 35 mm strip, fixed only by the jack nuts on its rear strip; the cable header faces forward.
- **Rear strip:** the 34.8 mm FR4 panel with the two 11.4 mm cut-outs and legends is drawn with this board. It carries the exhaust slots of decision 167 (`docs/MECHANICAL.md`, Ventilation): four routed 2 × 30 mm slots in the jack zone, two beside each jack nut, with the legends and the top screw on the 20 mm in front of the rail.
- Measure the NYS216 nut (taken as about 15 mm across). Check that the rear bottom angle (decision 160, 20 × 20 mm) clears the lower slots and the lower jack's body; if not, propose to /system an angle under the jack zone or a shorter leg. Report the module's final height to /system: it sets the rear inside height (about 60 mm).
- **Jack pin roles (decision 132):** the footprint `syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal` (rows 16.50 mm apart, cut-out 11.4 mm) has inferred pin roles; check them with a meter on the first delivered jack before ordering this PCB.
- **Cable header J3 (decision 181):** Adam Tech BHR-12-VUA 2x6 (SX-CONN-024) on KiCad `Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical`, the same footprint as the channel card's J1 (checked 2026-10-19 against drawing BHR-XX-VUA: drill 1.0 mm against 1.02 mm, fab body 8.90 × 22.90 mm against 22.86 × 8.80 mm, key slot on the odd-pin side and centred; the fab slot is drawn 4.1 mm against 4.50 mm, drawing only). Place it facing forward (the cable leaves towards the channel card), pin 1 marked on the silkscreen.

## Check on delivery

- Press one test input cable (Würth 12-way SX-WIRE-006 into two FCS-12-SG, SX-CONN-025; the FCS drawing names no cable pitch or gauge) and check it 1:1 with a meter.
- Dry-fit a 2x4 power socket in the BHR-12-VUA shroud once: it should sit centred on pins 3-10 (decision 181, misplug rule).

## Cost-cut levers

- Done: Rean NYS216 jacks instead of the Neutrik NMJ6HCD2 (decision 132), about €3.50 per module in parts instead of about €6; through-hole parts hand-soldered by the user (decision 133).
- Done (decisions 180, 181): a self-made IDC flat cable on 2x6 box headers instead of the Molex 217796-1101 lead, about €1.85 per channel against €5.98, saving about €16 at 4 channels and €66 at 16 (`docs/reviews/2026-10-18-cost-input-module-6p3.md`). Estimate 2026-10-18 with the cable parts counted (headers still SX-CONN-002 until redrawn): €813 / €1,075 / €1,689 at 4 / 8 / 16 channels; with both headers on SX-CONN-024 (2026-10-19): €811 / €1,072 / €1,684.
- Rejected by the user (2026-10-18): cheaper LCSC 6.3 mm jacks (about €5 / €8 / €12 saved at 4 / 8 / 16 channels, no cycle rating, mostly no threaded bushing); latched headers (+€1 per header; none, decision 181).
- Not now (the user, 2026-10-18): one board for two channels' jacks (decision 160), a DB25 bundle input module (possible later under `docs/INPUT-MODULE.md`).

## Component values (decision 134)

This board has no resistors or capacitors; the rule in `CLAUDE.md` applies if any are added.

## RoHS

- **RoHS strict (decision 116; invariant 9, decision 122):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly. The audit of this board's registered parts runs before the first PCB order (`docs/CONTINUE-FROM-HERE.md`); the IDC parts of decision 181 have theirs (Adam Tech drawings, Würth datasheet).
