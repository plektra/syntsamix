# Power board status

Updated 2026-10-20 (power board EMI session: DNP switch-node snubber footprints, decision 189, schematic and PCB rebuilt). 2026-10-20 (/system: `CHAIN.md` and `ARCHITECTURE.md` worded for the two module sizes, decision 185). 2026-10-20 (/system mechanical: power bay layout, brackets, LED hole and position across the bay, decision 188). 2026-10-20 (power board EMI session: input pi filter C108/L101, decision 187, schematic and PCB rebuilt). 2026-10-20 (power board PCB session 2026-10-19/20: PCB placed, routed and reviewed by the user; panel-mount brick jack, decision 182; small module without chain 2, decision 185; PCB form, decision 186). 2026-10-19 (/system: this board's PCB goes first). 2026-10-17 (/system: chain feeds are multi-drop power sections, decision 175).

Reference lists: `CHECKLISTS.md` (checks before layout, before ordering and on delivery, cost-cut levers, component values; decision 151). How the PCB is built: `CLAUDE.md`.

## Where it stands

- Schematic complete: four sheets, every netlist check 0 problems, ERC 0/0. The small power module (decision 185): master and chain 1 headers, up to 8 channel cards. Brick input through the panel-mount Kycon KPJX-PM-4S on the rear strip, wired to J101 (JST VH 4-pin, decision 182). Every part chosen, every value E24.
- PCB done and reviewed by the user (2026-10-20): 2 layers 1 oz, 177 × 35 mm referenced to the panel, two M3 bracket holes to the top strip (decision 186). DRC clean (0 errors, 0 warnings, 0 unconnected, schematic parity). Built by `scripts/build_pcb.sh` (placement, hand-designed power stage, Freerouting for the small signals); a hand edit in KiCad is lost on the next build, so changes go into the scripts.
- EMI (decision 187, 2026-10-20): the output side was already covered (one 400 kHz clock, opposite-phase sync, second-stage LC filters, separate PGND, tight input loops over the plane); the input had nothing between the brick lead and the converters. Added a pi filter after Q102: C108 4.7 µF 100 V, L101 2.2 µH SRP7028A, then C103 (net VIN_PRE between Q102 and L101). Hand model: lead ripple about −80 dB against −44 dB today; L101 alone gains nothing because C101 (100 nF) resonates with the lead near 400 kHz. Schematic rebuilt (netlist checks 0, ERC 0/0); PCB rebuilt by `build_pcb.sh` (DRC 0 violations, 0 unconnected, schematic parity); `placement.py` now takes new parts and every pad's net from the schematic. Reviewed by the user, committed (32daa73).
- Switch-node snubbers (decision 189, 2026-10-20): RC footprints across D201 (R208/C215) and D301 (R308/C315), 0805, DNP; values from the bench measurement (`CHECKLISTS.md`, Bench). Schematic rebuilt (netlist checks 0, ERC 0/0; L201 and L301 moved right on their sheets, no net change), PCB rebuilt by `build_pcb.sh` (DRC 0 violations, 0 unconnected, schematic parity); `placement.py` now takes the DNP and BOM flags from the symbols. Cost unchanged. Reviewed by the user (2026-10-20).
- Cost (`tools/costs.py estimate`, 2026-10-20, with decision 187): €793 / €1,028 / €1,590 for 4 / 8 / 16 channels (the input filter about €1-2); before it, with the channel card's decisions 183-184: €792 / €1,027 / €1,588 (decision 182 about €2 more per unit, decision 185 about €2 less); the 16-channel figure still prices this small module.

## Waiting for the user's confirmation

(none)

## Next

1. EMI on the first boards: the bench list in `CHECKLISTS.md`, "Bench, first boards" (input filter ripple, switch-node ringing and snubber values); common-mode noise through the brick and the audio cable shields only if the bench shows a problem.
2. Before ordering (one JLCPCB order for all boards, `docs/ROADMAP.md`): the checks in `CHECKLISTS.md`, "Before ordering": footprint prints, the bracket drawing and the top strip's holes (decision 188), the RoHS audit, LCSC stock.
3. Report the converters' real efficiency (from `scripts/design.py` or the TPS54560 datasheet) for `tools/heat_budget.py`, replacing its 88 % estimate (decision 167).
4. Full-size supply, the larger module with chain 2 (about 4 A per rail), after the prototype cards are measured (decision 96): the −20 V inverter needs a controller with external MOSFETs, the input an 8-10 A fuse and lower-resistance reverse-polarity MOSFETs, the headers 2.5-3 A fuses, the bay probably a fan (decision 167).

## RoHS

- Strict (decision 116, invariant 9): every part needs a `RoHS: <source>` in `docs/parts.csv` before ordering; lead-free finish and assembly; standard passives get their source when the BOM is fixed; the audit of this board's parts runs before the first PCB order.

## For /system

- Settled by /system 2026-10-20 (decision 188, `docs/MECHANICAL.md`, Power bay): mounting, rear strip, LED hole and position across the bay. Board follow-ups:
  - Bracket drawing (printed PETG or ASA, inverted L): vertical leg on the back face holds the board's back face 6 mm from the bay's right edge (vertical slot, M3 from the parts side through H1/H2 into a heat-set insert); horizontal leg about 4 mm thick in the 5 mm gap above the top edge; one M3 button-head screw per bracket through the top strip on its centreline above H1 (about 309 mm behind the front rail) and H2 (about 144 mm), plus an anti-twist peg. Keep parts near H1/H2 clear of the leg.
  - Power LED hole on the top strip's centreline about 290 mm behind the front rail (J103 lead long enough to reach it).
  - Back-face copper at least 5 mm from the cheek: true with the 6 mm spacing; keep through-hole pins and the brackets' screws within it.
  - On the frame: the rocker's tabs with 4.8 mm receptacles against the about 25 mm gap to the board's rear edge.
