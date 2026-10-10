# Channel card: checklists and reference

Read for layout, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

## Check before layout

- **Mechanical contract (decisions 106-109, `docs/MECHANICAL.md`):** strip pitch 35 mm, PCB at most 33.0 mm wide and 318 mm deep; PCB 10.0 mm below the panel, top-side parts at most 9.0 mm (all parts now comply); chain headers J501/J503 (IN) on the left edge, J502/J504 (OUT) on the right edge, underside, long axis front to back, one distance from the front in the rear half: record that distance in `MECHANICAL.md` (tell /system); orientation and crimping wait for the cable mock-up.
- **Meter (decision 119):** D411-D418 are drawn as `LED_SMD:LED_0805_2012Metric` (KT-0805G D411-D415, KT-0805Y D416-D417, NCD0805R1 D418; 2026-10-09). At layout: LEDs on a 6.0 mm pitch in one column, CLIP level with the fader's top travel end, two 1.5 mm non-plated holes for the bezel pegs, nothing taller than the bezel footprint allows under it; record the column position in `MECHANICAL.md`. Tune the 1k5 resistors per colour after a test print.
- **Regulator copper (decision 110):** about 20 × 20 mm of top copper per D²PAK tab, via-stitched to a bottom pour; U501 tab = +15V, U502 tab = −20V_RAW: keep apart and off AGND. The 89 / 82 °C worst case assumes 40 °C/W and 40 °C ambient; check against onsemi LM337 Figure 19 once placed.
- **Chain header holes:** KiCad's `IDC-Header_2x17/2x04_P2.54mm_Vertical` drill 1.0 mm; Würth recommends 1.1 ± 0.15 mm for the 0.64 mm square pins: use 1.1 mm drills.
- **Trimmers and jumpers on the underside (decision 112):** RV101, RV151, RV182 (3296W, screw facing down; RV101/RV151 next to their SSI2144s) and JP101/JP151, JP102/JP152, J301/J302 on the bottom side, L/R pairs side by side with matching bottom-silkscreen labels, leads soldered on the top side, outside the keep-out of decision 121 (10 mm from each long edge over the header length plus 15 mm front and back; provisional until the mock-up), at most 10.5 mm below the PCB; nothing tall around them.
- **78L05 U503 (UTC 78L05G-AB3-R):** worst case 0.25 W against UTC's 350 mW SOT-89 rating (no thermal resistance given; about 357 °C/W implied, junction about 129 °C at 40 °C ambient): give the middle (GND) tab a copper pour.
- **FREQ leg (decisions 130, 141):** R108/R158 are plain 820 Ω now (temperature compensation in the backlog); still place them next to their SSI2144 with short traces and leave room for an 0805 TFPT later.
- **Receiver (decision 143):** keep the 0.1 % resistors of each side together and the two input legs symmetrical (same trace lengths to the TL072), RFI caps C1-C4 next to R1-R4.
- **CV jack J181 (Thonkiconn):** 3 mm hole in the PCB under the barrel (Thonk note; the footprint has none), centred 6.48 mm from the S pad toward T; no traces or pour in it. Centred on the strip above CUTOFF (decision 106).
- **Fader:** KiCad `Potentiometer_Bourns_PTA6043_Single_Slide` matches the Bourns PTA drawing (Rev. 08/25). The M2 holes are tapped in the top of the frame, 71 mm apart, for panel screws from above: no PCB feature; choose the M2 screw length (1.6 mm panel + 3.5 mm spacer + the frame's thread depth, not stated by Bourns) so it cannot reach the track. Screwed to the panel before soldering. Keep the footprint compatible with the product-version TT PS60-10MC2BR10K if that costs nothing.
- **Pot footprints:** the stock KiCad RD901F/RD902F footprints (slots 9.6 mm centre to centre, 7.5 mm from the pins) match Alpha's drawing SLH-211-414 (its 11.4 mm spans the slot ends).

## Check on first delivery or assembly

- **GPBS850N buttons:** Mouser's listing says "DPDT Non-Latching ON-(ON)", the maker datasheet Rev 1 (2012) and decision 75 say latching; check that the delivered switches latch.

- **T18 panel pots:** bushing thread M7×0.75 × 5 mm (Alpha's RD902F drawing; confirmed by Thonk support 2026-10-09 for the Thonk pots): check the nut fit; legs bent back parallel to the shaft and bracket tabs in the footprint slots. Tayda sells 9 mm and 16 mm horizontal Alpha pots under similar names (the C10K dual is an RV16A01F-20): check any further Tayda pot against its own drawing.
- **CV jack Thonkiconn:** the nut (thickness not on Thonk's drawing, typically about 2 mm) grips the 2.9 mm of thread left above the printed washer and the panel. Pinout settled (1 sleeve, 2 switch, 3 tip; pads S/TN/T).
- **LED brightness:** even out the button LEDs (12 k from +15 V, about 1 mA) per colour after a test with the printed caps; the same for the meter once its bezel is printed.

## Cost-cut levers (open)

Frame set by the user (2026-10-09): the prototype is 4 channel cards, maybe 2; the full 16-channel console's cost stays in view in case the mixer becomes a product; the filter stays (rejected as a fitting option: the SSI2144 ladder filter is one of the features that make the mixer stand out). Overview: `docs/ROADMAP.md`, Cost review; system review `docs/reviews/2026-10-10-cost-system.md`.

Done 2026-10-10: DG412 → DG413 (139), E24 values (140), tempco to the backlog (141), MUTE/DUCK by the buttons (142), TL072 receiver (143), Bourns trimmers from Mouser (LCSC C83686 would be about €2.70 per card cheaper, noted in `docs/ROADMAP.md`), CUTOFF pot from Tayda A-4730 (Tayda has no T18 9 mm A100K or A10K duals: TRIM and AUX stay at Thonk). `tools/costs.py estimate --channels 4`: €946 (€1,035 on main before 2026-10-10).

Open:

7. **Ceramic coupling capacitors:** 10 µF bipolar electrolytics ×8 → 10 µF X5R ceramic (C13585 1206 50 V, JLCPCB basic): about €1.60 per card and one fee type. Breadboard test 11 decides (user, 2026-10-10). Touches decisions 72 and 111.
11. **Hand-soldering consigned parts (user to decide):** the SSI2144 (QSOP-16, 0.635 mm) stays with JLCPCB. Each other consigned type hand-soldered saves one fee, about €2.76 per order (the $3 of `overheads.csv`, not from an official JLCPCB page); the €30 consignment handling stays while the SSI2144 is consigned. Channel candidates, easiest first: bipolar 10 µF SX-C-023 (large SMD electrolytic pads; 24 in the 4-channel order with the master; gone if test 11 passes) and the SSI2162 (SSOP-10, 1.0 mm pitch; 5 in the order). Both: €5.52 per order; with the master's AD8273 ×2, AS3046D and R421 (the master's call): €13.80; also hand-soldering the SSI2144 drops the €30 handling: €46.56 in all.
13. **Fixed V/oct scale (product):** replace RV182 with an E24 pair if breadboard test 12 shows the chips' scales within about ±2 %; one part and one calibration step fewer per card.

## Component values (decision 134)

This board owns its value selection (rule in `CLAUDE.md`). Since decision 140 (2026-10-10) every resistor and capacitor value is E24 with a JLCPCB basic or preferred part, with one exception:

| Sheet | Value | References | Reason |
|---|---|---|---|
| Level | 30k1 | R217 | SC_ENV into the control summer (decision 97): `docs/ARCHITECTURE.md` names 30.1 kΩ in the SC_ENV chain line, so a change to 30k (E24, ducking scale 0.03 dB off) goes through /system |

E24 pairs (one extra placement each, no fee): R183 + R187 (162k, V/oct feedback), R207 + R223 (113k), R208 + R224 (450k), R213 + R225 (124k) (fader law). R111/R161 and R120/R170 stay provisional until the breadboard. The master still uses the old fader-law set for its AUX returns and master out (its own session; noted in `hardware/master/STATUS.md`).

### Fee-free swaps (decision 137, LCSC search 2026-10-10; four made 2026-10-10, see Where it stands)

| Part | Now | Fee-free candidate | Check before the swap |
|---|---|---|---|
| TL072 (SX-IC-007, 4 here, 13 on the master) | extended | ST TL072CDT, LCSC C6961, basic | done 2026-10-10: pinout and limits as TI's (ST DocID 2298 Rev 7) |
| 78L05 (SX-IC-012) | L78L05ACUTR, extended | UTC 78L05G-AB3-R, LCSC C71136, basic | done 2026-10-10: pins 1 O 2 G 3 I match the footprint |
| 6.2 V zener (SX-D-001, 4 here, 4 on the master) | no part chosen | BZT52C6V2 (hongjiacheng), LCSC C19077403, preferred | done 2026-10-10: RoHS in the maker's datasheet, land pattern matches |
| 13k, 680k, 750 R | counted as extended | UNI-ROYAL 0805W8F series, LCSC C17455, C17797, C17818, preferred | done 2026-10-10 |
| 110 R (SX-R-022) | extended | none found: 110 Ω 1 % 0805 had no fee-free part | done 2026-10-10: the meter ladder no longer uses it (decision 140) |

No fee-free part was found for the LM339, the 220 pF C0G 0805 or the 10 µF 35 V SMD electrolytic. `python3 tools/costs.py extended` lists every type that still costs a fee.
