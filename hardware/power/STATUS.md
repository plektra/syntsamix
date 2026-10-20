# Power board status

Updated 2026-10-20 (power board PCB session 2026-10-19/20: PCB placed, routed and reviewed by the user; panel-mount brick jack, decision 182; small module without chain 2, decision 185; PCB form, decision 186). 2026-10-19 (/system: this board's PCB goes first). 2026-10-17 (/system: chain feeds are multi-drop power sections, decision 175).

Reference lists: `CHECKLISTS.md` (checks before layout, before ordering and on delivery, cost-cut levers, component values; decision 151). How the PCB is built: `CLAUDE.md`.

## Where it stands

- Schematic complete: four sheets, every netlist check 0 problems, ERC 0/0. The small power module (decision 185): master and chain 1 headers, up to 8 channel cards. Brick input through the panel-mount Kycon KPJX-PM-4S on the rear strip, wired to J101 (JST VH 4-pin, decision 182). Every part chosen, every value E24.
- PCB done and reviewed by the user (2026-10-20): 2 layers 1 oz, 177 × 35 mm referenced to the panel, two M3 bracket holes to the top strip (decision 186). DRC clean (0 errors, 0 warnings, 0 unconnected, schematic parity). Built by `scripts/build_pcb.sh` (placement, hand-designed power stage, Freerouting for the small signals); a hand edit in KiCad is lost on the next build, so changes go into the scripts.
- Cost (`tools/costs.py estimate`, 2026-10-20, with the channel card's decisions 183-184): €792 / €1,027 / €1,588 for 4 / 8 / 16 channels (decision 182 about €2 more per unit, decision 185 about €2 less); the 16-channel figure still prices this small module.

## Waiting for the user's confirmation

(none)

## Next

1. Before ordering (one JLCPCB order for all boards, `docs/ROADMAP.md`): the checks in `CHECKLISTS.md`, "Before ordering": footprint prints, the bracket design and the top strip's holes (/system), the RoHS audit, LCSC stock.
2. Report the converters' real efficiency (from `scripts/design.py` or the TPS54560 datasheet) for `tools/heat_budget.py`, replacing its 88 % estimate (decision 167).
3. Full-size supply, the larger module with chain 2 (about 4 A per rail), after the prototype cards are measured (decision 96): the −20 V inverter needs a controller with external MOSFETs, the input an 8-10 A fuse and lower-resistance reverse-polarity MOSFETs, the headers 2.5-3 A fuses, the bay probably a fan (decision 167).

## RoHS

- Strict (decision 116, invariant 9): every part needs a `RoHS: <source>` in `docs/parts.csv` before ordering; lead-free finish and assembly; standard passives get their source when the BOM is fixed; the audit of this board's parts runs before the first PCB order.

## For /system

- Mounting (decision 186): two brackets to the bay's top strip only, no fixing to the rear strip (`MECHANICAL.md`, Power bay: "fixed at its rear edge to the bay's rear strip"). Brackets not designed yet; proposal: 3D-printed PETG or ASA (not PLA: 57 °C design air, decision 167), L-shaped with a vertical slot for the height tolerance, some width along the board or two screws each, on the board's back face; M3 screw and nut through H1/H2; M3 button-head screws (ISO 7380) through the top strip into a nut or heat-set insert. The top strip's holes go into the panel drawing.
- Rear strip (decision 182): the brick jack is the panel-mount Kycon KPJX-PM-4S (flange 25.2 × 14.2 mm, two M2.5 screws 19.0 mm apart, about Ø13 hole for the body), beside the rocker, both upright; exhaust slots where they leave room (decision 167).
- Power LED hole (decision 168): above J103, about 300 mm behind the front rail's inner face along the board, at its top edge; its position across the strip follows where the board sits across the bay (set with the brackets).
- Two module sizes (decision 185): `docs/CHAIN.md` ("the power board has three power headers", Current per rail) and the `docs/ARCHITECTURE.md` diagram describe the full system: word them for the small module (master, chain 1) and the full-size module (adds chain 2). `tools/costs.py` prices the small module for every build.
- Master heatsinks next to the bay (the user, 2026-10-20): the master's Wakefield 637-10ABPE heatsinks (25.4 mm below the master card, at least 190 mm behind the front rail, decisions 174, 176) share the height range of the power board, whose parts side faces the master with parts up to about 17 mm tall (mated J101 lead, ribbon sockets). Not checked yet: set the power board's position across the bay with the brackets (for example near the right cheek, parts ending about 20 mm from it) and a keep-out for the master heatsinks at the master section's right edge; also keep the power board's hottest parts away from them (shared air, decision 167).
