# Master card status

Updated 2026-10-13 (/system: decision 163 wording taken into ARCHITECTURE, CHAIN and MECHANICAL; ventilation, decision 167: heatsinks to recheck at 57 °C air). 2026-10-12 (/board master schematic: rear ribbons drawn, decision 163; rest of the decision 162 rework under Next). 2026-10-11: /system mechanical, decision 162. 2026-10-10: R232/R332 30k drawn (153).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128, 131, 138, 144, 146-150, 153). Net counts: AUX returns 73, compressor 83, sidechain 55, AUX sends 37, master out 63, meter 83.
- Values E24 and parts fee-free wherever one fits (decisions 144, 146-149, 153; exceptions and drawn swaps in `CHECKLISTS.md`); DG413, SSI2162, DRV135UA and AS3046D hand-soldered on the prototype (150).
- Power budget: typical 327 / 256 mA, worst case 701 / 576 mA (`ARCHITECTURE.md`); heatsinks ≤ 11.5 °C/W at 40 °C air, about 6.5 °C/W needed at 57 °C air (decision 167, see Next).
- Cost (`tools/costs.py estimate`, 2026-10-11 after the power board decisions 156-159, the GPBS850L price, the JLCPCB fee model fix and Thonk volume breaks): €778 / €1,040 / €1,600 for 4 / 8 / 16 channels before VAT and shipping; 28 fee types system-wide, billed per design as 38 at $3.07. Series of 8-channel mixers: `tools/costs.py sets`. Economic PCBA assumed (conditions in `hardware/CLAUDE.md`, Parts).
- `simulation/sidechain` reflects the 30k loads (1.667 kΩ); results unchanged.
- 2026-10-10, button MPN corrected: SX-SW-001 is CW GPBS850L (latching, Electrokit 41012905); GPBS850N, recorded until now, is the momentary twin. MPN, footprint `SW_Latching_8.5x8.5mm_CW_GPBS850L` (same geometry per datasheet Rev 2), parts.csv and prices.csv changed; erratum on decision 75; no wiring change, ERC 0/0. Estimate €769 / €1,037 / €1,609 for 4 / 8 / 16 channels.
- 2026-10-12, rear ribbons (decision 163): the eleven rear jacks and SW901 left the schematic; J603 (AUX sends sheet) carries main outs and both sends to the output row board, J903 (Power sheet) brings the AUX returns, SC EXT and the ground-lift switch from the input row board (26-pin Würth 61202621621, SX-CONN-017; cable sockets SX-CONN-018). 26 new root sheet pins (Power sheet box enlarged); net counts AUX sends 41, power 20, the rest unchanged; netlist checks 0 problems, ERC 0/0, cross-sheet nets traced on the full netlist. `tools/costs.py` reads the master schematic, so the jacks and SW901 (about €9 per master) are out of the estimate until the row board projects exist.
- PCB: not started.

## Waiting for the user's confirmation

- Decision 147 was made under the user's delegation of minor changes ("ask me only about major changes"): review the compressor pairs, the GR LED shift (at most 0.2 dB) and the SC LPF sweep (3-6 % lower).

## Open: needs the user or another session

- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **Ground-lift switch SW901 (SX-SW-002):** part to choose; it sits on the rear input row board between J903 conductors 25 and 26 (decisions 162, 163), so a PCB-mount toggle with a threaded bushing fits.
- **Bipolar 10 µF ×16 (SX-C-023, consigned) → two ROQANG 10 µF (SX-C-024) back to back:** done on the channel card by decision 161 (2026-10-11, confirmed by the user; the X5R option is dropped). Do the same swap here (refines 127): first check with the DRV135 datasheet whether the sense-pin capacitors C707-C710 may drop to 5 µF (TI recommends 10 µF non-polarised); if not, two 22 µF there (a new extended type). The €30 consignment handling and about €7 of parts go with it.
- **Fee types shared with the channel** (220p C0G, TL062, LM339): only go away if both boards change; noted in `hardware/channel-card/STATUS.md`. Checked and dropped: OPA2171 → LM358 (onsemi LM358/D Rev. 27) and ceramic LM337 output capacitors (onsemi LM337/D Rev. 11 p. 7, can oscillate).

## Next

0. **SX-IC-010 is NRND:** the TI LM317KCSE3 (TO-220) in `docs/parts.csv` is marked NRND in TI's orderable table (SLVS044Z p.30, found 2026-10-13). Choose a replacement, for example onsemi LM317TG (TO-220, no lifecycle mark in LM317/D Rev 18; RthJA 65 °C/W, RthJC 5 °C/W), with its RoHS source. The TI LM337KCSE3 is still Active (SLVS047L p.12).

1. **Schematic rework for decision 162** (`/board master schematic`; `docs/MECHANICAL.md`, Master section): the master card hangs 10 mm under its panel, so no jack on it reaches a panel.
   - Done on the master card (decision 163): ribbons J603 and J903, 26-pin, pinouts in `docs/decisions/master-card-sheets.md`.
   - Still to do: the two row boards as new KiCad projects (6 jacks in a row at about 23 mm, the 26-pin header SX-CONN-017, SW901 on the input board between conductors 25 and 26, insulated from the row board's ground; the return normalling R-to-L wired jack to jack). NYS216 must be at most about 17 mm tall above its board: **measure a sample first** (not measured yet, 2026-10-12); if taller, on-edge 2-jack boards with the AUX returns reusing `input-module-6p3`, and decision 163's pinout is revisited. Add both projects to `BOARDS` in `tools/costs.py`.
   - Headphones J751: a panel-mounted 6.3 mm stereo jack (part to choose, RoHS source) on the top panel, wired to a header on the card; the jack passes through a cutout in the card, at least about 90 mm behind the front edge.
   - Meter and gain-reduction LEDs to 0805 (KT-0805G, KT-0805Y, NCD0805R1 as on the channel, decision 119) under printed bezels: 2 × 12 at 6.0 mm pitch plus 5 GR LEDs; SX-D-004/005/006 retire.
   - U901-U903 TO-220 on the underside with one heatsink each, behind the card's middle, up to 25 mm deep, ≥ 3 mm from each other, the frame and the cover.
   - Card at most 138 × 318 mm under a 4-strip (139.8 mm) top panel; chain headers on the left edge at the channel distance.
   - Heatsinks at 57 °C air (decision 167: inside air 22 K above a 35 °C stage): `scripts/power_budget.py` assumes 40 °C; at 57 °C the worst-case 3.44 W gives TJ about 117 °C on 11.5 °C/W (typical 85 °C). Decision 95's 100 °C target stands: change the script to 57 °C and choose a heatsink of about 6.5 °C/W (6 °C/W junction to sink) that fits the 25 mm underside zone, with the ≥ 3 mm clearances; if none fits, bring it to the user (relaxing 95 is the user's call). Leave room on the rear piece for exhaust slots (about 3 cm², `docs/MECHANICAL.md`, Ventilation).
2. PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`); the AS3046D declaration before ordering.

## For /system

(none; the decision 163 wording is in `ARCHITECTURE.md` invariant 2, `CHAIN.md` Grounding and the `MECHANICAL.md` Rear jacks row, /system 2026-10-13)
