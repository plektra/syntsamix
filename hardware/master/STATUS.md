# Master card status

Updated 2026-10-13 (/board master: headphone jack, decisions 169; 0805 LEDs, 170; off-board parts in the estimate, 171; NYS216 samples; heatsinks on hold. /system the same day: decision 163 wording in ARCHITECTURE, CHAIN and MECHANICAL; ventilation, decision 167). 2026-10-12: rear ribbons, decision 163. 2026-10-11: /system mechanical, decision 162.

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128, 131, 138, 144, 146-150, 153, 163, 169, 170). Net counts: bus 29, AUX returns 73, compressor 83, sidechain 55, AUX sends 41, master out 63, headphones 28, meter 83, power 20.
- Values E24 and parts fee-free wherever one fits (decisions 144, 146-149, 153; exceptions and drawn swaps in `CHECKLISTS.md`); DG413, SSI2162, DRV135UA and AS3046D hand-soldered on the prototype (150).
- Rear jacks and SW901 are off the card (163): ribbons J603 (outputs) and J903 (inputs, ground lift) to two row boards, not drawn yet. Headphone jack J751 is a KK 3-pin header for the panel NYS230 and a ready-made lead (169). All master LEDs are 0805 basic parts; the GR LEDs are yellow (170).
- Power budget: typical 327 / 256 mA, worst case 701 / 576 mA (`ARCHITECTURE.md`); heatsinks open (Next 2).
- Cost (`tools/costs.py estimate`, 2026-10-13, every off-board part counted, decision 171): €831 / €1,110 / €1,693 for 4 / 8 / 16 channels before VAT and shipping. The master's off-board parts (rear jacks, SW901, row-board headers, ribbon sockets, NYS230 and its lead) are in `docs/costs/offboard.csv` until the row-board projects exist; the two row boards are priced as two PCB designs.
- PCB: not started.

## Waiting for the user's confirmation

- Decision 147 was made under the user's delegation of minor changes ("ask me only about major changes"): review the compressor pairs, the GR LED shift (at most 0.2 dB) and the SC LPF sweep (3-6 % lower).

## Open: needs the user or another session

- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **Ground-lift switch SW901 (SX-SW-002):** part to choose (€2 estimate in the cost); it sits on the rear input row board between J903 conductors 25 and 26 (decisions 162, 163), so a PCB-mount toggle with a threaded bushing fits.
- **Bipolar 10 µF ×16 (SX-C-023, consigned) → two ROQANG 10 µF (SX-C-024) back to back:** done on the channel card by decision 161. Do the same swap here (refines 127): first check with the DRV135 datasheet whether the sense-pin capacitors C707-C710 may drop to 5 µF (TI recommends 10 µF non-polarised); if not, two 22 µF there (a new extended type). The €30 consignment handling and about €7 of parts go with it.
- **Fee types shared with the channel** (220p C0G, TL062, LM339): only go away if both boards change; noted in `hardware/channel-card/STATUS.md`. Checked and dropped: OPA2171 → LM358 (onsemi LM358/D Rev. 27) and ceramic LM337 output capacitors (onsemi LM337/D Rev. 11 p. 7, can oscillate).
- **Samples to order** (next Tayda order, with the channel's CUTOFF pot): about 3 Rean NYS216 (Tayda lists Rean as the maker, $0.70; Mouser 568-NYS216 stays the RoHS source) and one NYS230 (Mouser, or Tayda if listed). On the NYS216: height above the board (at most about 17 mm, decision 162) and to the bushing centre, bushing length past the housing, pin roles with a meter (decision 132). On the NYS230: depth behind the panel (about 30 mm assumed) and pin roles; on the 217797-1031 lead the pin order of the free ends.

## Next

0. **SX-IC-010 is NRND:** the TI LM317KCSE3 (TO-220) in `docs/parts.csv` is marked NRND in TI's orderable table (SLVS044Z p.30, found 2026-10-13). Choose a replacement, for example onsemi LM317TG (TO-220, no lifecycle mark in LM317/D Rev 18; RthJA 65 °C/W, RthJC 5 °C/W), with its RoHS source. The TI LM337KCSE3 is still Active (SLVS047L p.12).
1. **Rear row boards** (decisions 162, 163), after measuring an NYS216 sample: two new KiCad projects (6 jacks in a row at about 23 mm, the 26-pin header SX-CONN-017, SW901 on the input board between conductors 25 and 26, insulated from the row board's ground; the return normalling R-to-L wired jack to jack). If the NYS216 is taller than about 17 mm: on-edge 2-jack boards with the AUX returns reusing `input-module-6p3`, and decision 163's pinout is revisited. Add both projects to `BOARDS` in `tools/costs.py` and move their parts out of `docs/costs/offboard.csv`.
2. **Heatsinks, on hold (user, 2026-10-13): none fits.** U901-U903 TO-220 on the underside, one heatsink each, behind the card's middle, up to 25 mm deep, ≥ 3 mm from each other, the frame and the cover (162). Worst case (`scripts/power_budget.py`): LM317 3.44 W, LM337 2.82 W, L7805 0.73 W. At 40 °C air that needs ≤ 11.5 °C/W; at decision 167's 57 °C inside air about 6.5 °C/W for decision 95's 100 °C junction (the script still assumes 40 °C; change it). Checked and failed: Wakefield 637-10ABPE (25.4 mm, 12.67 °C/W, distributors); Aavid 577202B00000G (24.4 °C/W); Aavid 7021B-MTG (stands about 37 mm, Aavid sheet); Same Sky HSE-BX-02 series (rev 1.05, 2026-01-27, p. 4: stands upright, length = height; 25.4 mm about 14.3 °C/W, 38.1 mm about 13.2, 50.8 mm about 11.0 at 3.44 W). Even the rear edge has only about 40 mm under the card. Options: (a) review the worst-case loads in `power_budget.py` (701/576 mA against 327/256 mA typical) on this board; (b) /system: raw rails about ±18 V instead of ±20 V (about 2.1 / 1.7 W; every board's regulator headroom and the power board converters to check); (c) /system: LM317/LM337 on the chassis (rear angle or bottom cover) with insulating pads and short leads; relaxing decision 95 is the user's call. HS901/HS902 are placeholders, nothing in `parts.csv`. Leave room on the rear piece for exhaust slots (about 3 cm², `docs/MECHANICAL.md`, Ventilation).
3. Card at most 138 × 318 mm under a 4-strip (139.8 mm) top panel; chain headers on the left edge at the channel distance; the NYS230 passes through a cutout in the card at least about 90 mm behind the front edge.
4. PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`); the AS3046D declaration before ordering.

## For /system

- Input-module cable (decision 99, `docs/INPUT-MODULE.md` Cable): the user agrees (2026-10-13) to replace the hand-crimped cable (22-01-3107 housings, 20 crimps 08-50-0114 per cable) with the ready-made Molex 217796-1101 (SX-CONN-022; KK 254 10-pin both ends, 150 mm, 22 AWG UL 11028 discrete wires, mates the AE-6410 headers; Mouser 538-217796-1101, $5.63, $4.65 at 25+, RoHS compliant, Active, 2026-10-13); crimping about 80 terminals for the prototype is too slow. Headers and pinout stay. To settle: 1:1 wiring on the Molex sales drawing; 22 AWG instead of 26-28; hot/cold pairs twisted by hand; 150 mm against the provisional 100 mm (decision 160). Already counted in the estimate (171); under cost watch (`docs/ROADMAP.md`, Cost-cut candidates item 8): about €3.20 more per cable than crimped parts.
- Heatsinks (Next 2), if options (b) or (c) are taken.
