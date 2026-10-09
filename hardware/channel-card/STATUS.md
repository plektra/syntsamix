# Channel card status

Updated 2026-10-09 (schematic session: pot MPNs on the symbols and RV183 reference fixed; R184 10 k → 12 k for the RESONANCE pot rating, decision 129; tempco leg = Vishay TFPT 820 Ω + 180 Ω, decision 130. Earlier the same day: mechanical parts 110-117, /system 118-122 and 124, meter LEDs and power levers 123, RoHS audit).

## Where it stands

- Schematic complete: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0 errors 0 warnings; every sheet matches its reference netlist.
- 2026-10-08: decisions 97, 98 and 102 drawn (SC_ENV into VSUM through R217; PGND returns for Q301 and the button pull-downs; U204 = OPA2171). The Level control is simulated in `simulation/level/`.
- 2026-10-09, mechanical parts (decisions 110-117): every top-side part now fits the 9 mm limit under the panel. Regulators D²PAK on copper (110); electrolytics SMD at most 5.4 mm (111); trimmers and jumper headers on the underside (112); low-cut caps C0G 1206 (113); pot shaft standard T18 (114); trim stage scaled to a 100 k pot and the pots chosen (115); RoHS strict for every part (116, project-wide); button LEDs and chain headers chosen (117). Sheets rebuilt, netlists match, ERC 0/0.
- 2026-10-09, /system mechanical: 3.5 mm CV jack by the new jack-size rule (118), meter as 0805 LEDs under a printed bezel at 6.0 mm pitch (119), one centred panel screw per end with a printed key (120), underside rules, keep-out and bottom cover (121), RoHS invariant 9 with standard passives at BOM time (122).
- 2026-10-09, schematic: meter LEDs D411-D418 drawn as 0805 (KT-0805G, KT-0805Y, NCD0805R1; decision 119); power levers (decision 123): U107 NE5532 → TL072, meter U401/U404 TL072 → TL062CDR (SX-IC-024). Card load now 113 / 95 mA typical, 229 / 194 mA worst case, sizing 174 / 142 mA. Netlists match, ERC 0/0. RoHS audit of `parts.csv` done (report `docs/reviews/2026-10-09-rohs-audit.md`).
- 2026-10-09, schematic (pots): Alpha MPNs on RV1, RV181, RV301/RV302 (Thonk `-0057` codes); RV183 is SX-POT-012 (Tayda RD901F-40-15K-C10K) in the reference too; R184 10 k → 12 k (SX-R-008) so RV183 stays within Alpha's 0.02 W rating for non-B tapers (decision 129; RD901F spec facts in `parts.csv`). Netlists match, ERC 0/0.
- 2026-10-09, schematic (tempco): R108/R158 Vishay TFPT0603L8200FV (820 Ω, +4110 ppm/K) with new R122/R172 180 Ω in series to AGND replace the end-of-life ERA-V33J102V: 1 k, about +3370 ppm/K (decision 130). Trim pot value text shortened to "50k OFFSET" for room. Netlists match (filter 80 nets), ERC 0/0, sheet looked at.
- PCB: not started; waits for the breadboard, the SSI2144/SSI2162 RoHS declaration and the cable mock-up.

## Provisional until the breadboard

`simulation/filter/BREADBOARD.md` tests 1-10 set R111/R161 (filter output scale) and R120/R170 (Q current limit; with R184 = 12 k the maximum is about 254 µA, 36.5 k would restore about 280 µA, decision 129). Then edit `filter_wired.py` / `filter_build.py`, run `scripts/rebuild_all.sh`, and update `docs/decisions/channel-card.md`.

## Waiting for the user's confirmation

(none)

## Waiting on others

- **Alpha `-0057` suffix (left open by the user 2026-10-09):** the variant code on Thonk's three Alpha order codes is not defined in the RD901F spec; RV183 (Tayda) has none. Check the shaft and knurl of the Tayda RESONANCE pot against the Thonk pots on delivery.
- **RD902F dual specification:** not read yet (the Mouser RD901F PDF is blocked to scripts; the Tayda copy covers the RD901F single); confirm the dual's power rating when it is found.

- **RoHS declaration for the SSI2144 (SX-IC-001) and SSI2162 (SX-IC-002) (decision 122):** no RoHS statement from Sound Semiconductor, Electrokit or the datasheets; requested by the user by email (2026-10-09). Without it they block the PCB order.
- **Knobs:** after the pots (T18 push-on, up to about 19 mm across; for example Thonk Davies 1900H clone, Tall Satin Synthpointer, Mini MXR); need a RoHS source.

## Parts

Chosen (fields on the symbols, sources and RoHS in `docs/parts.csv`): regulators onsemi LM317D2TR4G / LM337D2TR4G; ROQANG SMD electrolytics; Panasonic EEE-1VA100NP bipolar (land pattern checked: size D, KiCad `C_Elec_6.3x5.4`); Murata C0G low-cut caps; Bourns 3296W trimmers; Bourns PTA6043 fader; chain headers Würth 61203421621 (2×17) and 61200821621 (2×4); button LEDs JLCPCB basic 0805 (MUTE red NCD0805R1, PFL yellow KT-0805Y, SC SEND/DUCK/COMP BUS green KT-0805G, LOW-CUT/BYPASS white KT-0805W); CV jack Thonkiconn PJ398SM (decision 118). Printed in-house: button caps, the meter bezel (decision 119) and the 1 mm M6 washer for the CV jack (SX-MECH-004). Supply budget: `scripts/power_budget.py` (rerun after changing parts that draw current).

## Check before layout

- **Mechanical contract (decisions 106-109, `docs/MECHANICAL.md`):** strip pitch 35 mm, PCB at most 33.0 mm wide and 318 mm deep; PCB 10.0 mm below the panel, top-side parts at most 9.0 mm (all parts now comply); chain headers J501/J503 (IN) on the left edge, J502/J504 (OUT) on the right edge, underside, long axis front to back, one distance from the front in the rear half: record that distance in `MECHANICAL.md` (tell /system); orientation and crimping wait for the cable mock-up.
- **Meter (decision 119):** D411-D418 are drawn as `LED_SMD:LED_0805_2012Metric` (KT-0805G D411-D415, KT-0805Y D416-D417, NCD0805R1 D418; 2026-10-09). At layout: LEDs on a 6.0 mm pitch in one column, CLIP level with the fader's top travel end, two 1.5 mm non-plated holes for the bezel pegs, nothing taller than the bezel footprint allows under it; record the column position in `MECHANICAL.md`. Tune the 1k5 resistors per colour after a test print.
- **Regulator copper (decision 110):** about 20 × 20 mm of top copper per D²PAK tab, via-stitched to a bottom pour; U501 tab = +15V, U502 tab = −20V_RAW: keep apart and off AGND. The 89 / 82 °C worst case assumes 40 °C/W and 40 °C ambient; check against onsemi LM337 Figure 19 once placed.
- **Chain header holes:** KiCad's `IDC-Header_2x17/2x04_P2.54mm_Vertical` drill 1.0 mm; Würth recommends 1.1 ± 0.15 mm for the 0.64 mm square pins: use 1.1 mm drills.
- **Trimmers and jumpers on the underside (decision 112):** RV101, RV151, RV182 (3296W, screw facing down; RV101/RV151 next to their SSI2144s) and JP101/JP151, JP102/JP152, J301/J302 on the bottom side, L/R pairs side by side with matching bottom-silkscreen labels, leads soldered on the top side, outside the keep-out of decision 121 (10 mm from each long edge over the header length plus 15 mm front and back; provisional until the mock-up), at most 10.5 mm below the PCB; nothing tall around them.
- **Tempco leg (decision 130):** R108/R158 (TFPT, 0603) against the top of its SSI2144, short traces, away from the regulators and other warm parts; R122/R172 (180 Ω) may sit a little further away.
- **CV jack J181 (Thonkiconn):** 3 mm hole in the PCB under the barrel (Thonk note; the footprint has none), centred 6.48 mm from the S pad toward T; no traces or pour in it. Centred on the strip above CUTOFF (decision 106).
- **Fader:** KiCad `Potentiometer_Bourns_PTA6043_Single_Slide` matches the Bourns PTA drawing (Rev. 08/25). The M2 holes are tapped in the top of the frame, 71 mm apart, for panel screws from above: no PCB feature; choose the M2 screw length (1.6 mm panel + 3.5 mm spacer + the frame's thread depth, not stated by Bourns) so it cannot reach the track. Screwed to the panel before soldering. Keep the footprint compatible with the product-version TT PS60-10MC2BR10K if that costs nothing.
- **Pot footprints:** the stock KiCad RD901F/RD902F footprints (slots 9.6 mm centre to centre, 7.5 mm from the pins) match Alpha's drawing SLH-211-414 (its 11.4 mm spans the slot ends).

## Check on first delivery or assembly

- **GPBS850N buttons:** Mouser's listing says "DPDT Non-Latching ON-(ON)", the maker datasheet Rev 1 (2012) and decision 75 say latching; check that the delivered switches latch.

- **T18 panel pots:** bushing thread M7×0.75 × 5 mm (Alpha's RD902F drawing; confirmed by Thonk support 2026-10-09 for the Thonk pots): check the nut fit; legs bent back parallel to the shaft and bracket tabs in the footprint slots. Tayda sells 9 mm and 16 mm horizontal Alpha pots under similar names (the C10K dual is an RV16A01F-20): check any further Tayda pot against its own drawing.
- **CV jack Thonkiconn:** the nut (thickness not on Thonk's drawing, typically about 2 mm) grips the 2.9 mm of thread left above the printed washer and the panel. Pinout settled (1 sleeve, 2 switch, 3 tip; pads S/TN/T).
- **LED brightness:** even out the button LEDs (12 k from +15 V, about 1 mA) per colour after a test with the printed caps; the same for the meter once its bezel is printed.

## Next

1. Breadboard the SSI2144 when parts arrive (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`). Test 10 (fader law) wants one OPA2171 (SOIC-8, adapter) and one TL072; with two TL072s, skip the 0 % row (`simulation/filter/BREADBOARD.md`).
2. RoHS gaps: SSI2144/SSI2162 declaration (requested, waiting); copy the orderable MPNs the audit checked (NE5532DR, TL072CDR, LM339DR, AD8273ARZ, DG413DY-T1-E3, DG412DY-T1-E3, LM13700MX/NOPB) into the MPN column at BOM time. At the next LCSC check run, add SX-R-089 (TFPT, Mouser-only: hand-solder or consign) and SX-R-090 to `docs/lcsc-check.csv` / `tools/lcsc_check.py`.
3. Cable mock-up (decision 109).
4. Tidy (any schematic session, no wiring change): the reference netlist scripts still give the button LEDs the 3 mm THT footprint and SX-D-002 (`filter_build.py` D183, `level_build.py` button LEDs); the drawings use 0805 with the decision 117 part numbers.
5. PCB layout.

## For /system

- `docs/ARCHITECTURE.md`, Open system items, RoHS gaps: "End of Life THAT1646S08-U (master) and ERA-V33J102V (channel)" is out of date. The THAT1646 is replaced by the DRV135UA (decision 125); the channel card no longer uses the ERA-V33J102V (decision 130); it remains on the master's R421.
