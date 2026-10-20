# Master card status

Updated 2026-10-20 (/system mechanical: heatsink keep-out at the right edge and power ribbon route, decision 188). 2026-10-17 (/system: J101 on the cards' header line, decision 175; regulator zone at least about 190 mm behind the front rail, decision 176; ready-made input cable, decision 179; budgets and heatsink line in ARCHITECTURE refreshed. /board master: `CHECKLISTS.md` brought to decisions 174 and 175; AUX return MUTE and DUCK on the buttons, decision 177; decision 147 confirmed). Earlier the same day: decisions 172-175 (onsemi regulators, back-to-back pairs, NE5532 → TL072, Wakefield heatsinks, multi-drop chain cables).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128, 131, 138, 144, 146-150, 153, 163, 169, 170, 172-174, 177). Net counts: bus 29, AUX returns 73, compressor 85, sidechain 55, AUX sends 41, master out 69, headphones 28, meter 83, power 20.
- Values E24 and parts fee-free wherever one fits (decisions 144, 146-149, 153; exceptions and drawn swaps in `CHECKLISTS.md`); DG413 (×8 since 177), SSI2162, DRV135UA and AS3046D hand-soldered on the prototype (150). Nothing is consigned: the 16 bipolar 10 µF are back-to-back ROQANG pairs (172). U901/U902 are onsemi LM317TG/LM337TG (TI LM317KCSE3 was NRND).
- Rear jacks and SW901 are off the card (163): ribbons J603 (outputs) and J903 (inputs, ground lift) to two row boards, not drawn yet. Headphone jack J751 is a KK 3-pin header for the panel NYS230 and a ready-made lead (169). All master LEDs are 0805 basic parts; the GR LEDs are yellow (170).
- Power budget (after decision 173): typical 295 / 224 mA, worst case 591 / 466 mA, sizing 522 / 408 mA (in `ARCHITECTURE.md` since 2026-10-17). Heatsinks HS901/HS902 Wakefield 637-10ABPE (174): at 57 °C inside air the LM317 junction reaches about 111 °C worst case, 105 °C at the sizing load, 84 °C typical, within the 125 °C rating.
- Cost (`tools/costs.py estimate`, 2026-10-17, every off-board part counted, decision 171): €798 / €1,084 / €1,683 for 4 / 8 / 16 channels before VAT and shipping, after decision 177 (€801 / €1,087 / €1,686 before it). The master's off-board parts (rear jacks, SW901, row-board headers, ribbon sockets, NYS230 and its lead) are in `docs/costs/offboard.csv` until the row-board projects exist; the two row boards are priced as two PCB designs.
- PCB: not started.

## Waiting for the user's confirmation

(none)

## Open: needs the user or another session

- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **Ground-lift switch SW901 (SX-SW-002):** part to choose (€2 estimate in the cost); it sits on the rear input row board between J903 conductors 25 and 26 (decisions 162, 163), so a PCB-mount toggle with a threaded bushing (straight PC pins, bushing axis normal to the board) fits. Choose it with the row board, after the NYS216 sample: the board hangs on the jack nuts, so the switch body plus bushing must reach through the 1.6 mm rear piece at the same height as the jacks (2026-10-17: deferred for that reason).
- **Fee types shared with the channel** (220p C0G, TL062, LM339): only go away if both boards change; noted in `hardware/channel-card/STATUS.md`. Checked and dropped: OPA2171 → LM358 (onsemi LM358/D Rev. 27) and ceramic LM337 output capacitors (onsemi LM337/D Rev. 11 p. 7, can oscillate).
- **Samples to order** (next Tayda order, with the channel's CUTOFF pot): about 3 Rean NYS216 (Tayda lists Rean as the maker, $0.70; Mouser 568-NYS216 stays the RoHS source) and one NYS230 (Mouser, or Tayda if listed). On the NYS216: height above the board (at most about 17 mm, decision 162) and to the bushing centre, bushing length past the housing, pin roles with a meter (decision 132). On the NYS230: depth behind the panel (about 30 mm assumed) and pin roles; on the 217797-1031 lead the pin order of the free ends.

## Next

1. **Rear row boards** (decisions 162, 163), after measuring an NYS216 sample: two new KiCad projects (6 jacks in a row at about 23 mm, the 26-pin header SX-CONN-017, SW901 on the input board between conductors 25 and 26, insulated from the row board's ground; the return normalling R-to-L wired jack to jack). If the NYS216 is taller than about 17 mm: on-edge 2-jack boards with the AUX returns reusing `input-module-6p3`, and decision 163's pinout is revisited. Add both projects to `BOARDS` in `tools/costs.py` and move their parts out of `docs/costs/offboard.csv`.
2. **Heatsinks: settled by decision 174** (Wakefield 637-10ABPE, 25.4 mm, 12.67 °C/W; junction limit 125 °C). Zone (decision 176): U901/U902 with HS901/HS902 at least about 190 mm behind the front rail's inner face, where the sloped floor clears 25.4 mm plus 3 mm; footprint for the two 25.4 mm-pitch pins from the Wakefield drawing at layout; L7805 U903 without a heatsink (about 104 °C free-air worst case at 57 °C). Earlier candidates that failed: Aavid 577202B00000G (24.4 °C/W), Aavid 7021B-MTG (about 37 mm), Same Sky HSE-BX-02 (14.3 °C/W at 25.4 mm). Leave room on the rear piece for exhaust slots (about 3 cm², `docs/MECHANICAL.md`, Ventilation).
3. At layout: card at most 138 × 318 mm; heatsinks at least 10 mm inside the right edge and the power ribbon in front of the heatsink zone (decision 188); the NYS230 cutout at least about 90 mm behind the front edge (chain header and regulator checks in `CHECKLISTS.md`).
4. PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`); the AS3046D declaration before ordering.

## For /system

- Settled by /system 2026-10-20 (decision 188, `docs/MECHANICAL.md`, Master section): at layout, HS901/HS902 and the TO-220 tabs at least 10 mm inside the card's right edge (preferably near the middle), about 20 mm of air to the power board's parts; place the power header so the ribbon from the power board's J401 (about 164 mm behind the front rail, at the floor) reaches it in front of the heatsink zone (less than about 185 mm behind the front rail); the chain 1 feed also crosses there, and no chain cable passes under a heatsink.

- (Settled 2026-10-17, the user: "let's keep the heatsink and 20V rails": the board heatsinks of decision 174 and decision 40's ±20 V chain stay; ±18 V raw rails and regulators bolted to a 2020 rail are not pursued.)
