# Channel card status

Updated 2026-10-10 (schematic sessions, delegated by the user: "work autonomously and follow recommendations", then "work on this autonomously"): U303 DG413 (139), all values E24 with fee-free parts (140), temperature compensation to the backlog (141), MUTE/DUCK switched by the buttons (142), TL072 difference receiver (143), trimmers from Mouser, CUTOFF pot from Tayda, breadboard tests 11 and 12. Earlier the same day: fee-free part swaps (decision 137). Before that, 2026-10-09: pots, R184, TFPT tempco, mechanical parts, meter LEDs and power levers (decisions 110-130).

## Where it stands

- Schematic complete: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0 errors 0 warnings; every sheet matches its reference netlist.
- 2026-10-08: decisions 97, 98 and 102 drawn (SC_ENV into VSUM through R217; PGND returns for Q301 and the button pull-downs; U204 = OPA2171). The Level control is simulated in `simulation/level/`.
- 2026-10-09, mechanical parts (decisions 110-117): every top-side part now fits the 9 mm limit under the panel. Regulators D²PAK on copper (110); electrolytics SMD at most 5.4 mm (111); trimmers and jumper headers on the underside (112); low-cut caps C0G 1206 (113); pot shaft standard T18 (114); trim stage scaled to a 100 k pot and the pots chosen (115); RoHS strict for every part (116, project-wide); button LEDs and chain headers chosen (117). Sheets rebuilt, netlists match, ERC 0/0.
- 2026-10-09, /system mechanical: 3.5 mm CV jack by the new jack-size rule (118), meter as 0805 LEDs under a printed bezel at 6.0 mm pitch (119), one centred panel screw per end with a printed key (120), underside rules, keep-out and bottom cover (121), RoHS invariant 9 with standard passives at BOM time (122).
- 2026-10-09, schematic: meter LEDs D411-D418 drawn as 0805 (KT-0805G, KT-0805Y, NCD0805R1; decision 119); power levers (decision 123): U107 NE5532 → TL072, meter U401/U404 TL072 → TL062CDR (SX-IC-024). Card load now 113 / 95 mA typical, 229 / 194 mA worst case, sizing 174 / 142 mA. Netlists match, ERC 0/0. RoHS audit of `parts.csv` done (report `docs/reviews/2026-10-09-rohs-audit.md`).
- 2026-10-09, schematic (pots): Alpha MPNs on RV1, RV181, RV301/RV302 (Thonk `-0057` codes); RV183 is SX-POT-012 (Tayda RD901F-40-15K-C10K) in the reference too; R184 10 k → 12 k (SX-R-008) so RV183 stays within Alpha's 0.02 W rating for non-B tapers (decision 129; RD901F spec facts in `parts.csv`). Netlists match, ERC 0/0.
- 2026-10-09, schematic (tempco): R108/R158 Vishay TFPT0603L8200FV (820 Ω, +4110 ppm/K) with new R122/R172 180 Ω in series to AGND replace the end-of-life ERA-V33J102V: 1 k, about +3370 ppm/K (decision 130). Trim pot value text shortened to "50k OFFSET" for room. Netlists match (filter 80 nets), ERC 0/0, sheet looked at.
- 2026-10-10, fee-free parts (decision 137, confirmed by the user): SX-IC-007 TL072 → ST TL072CDT (LCSC C6961, basic; U107, U205, U402, U403), SX-IC-012 78L05 → UTC 78L05G-AB3-R (C71136, basic; U503), SX-D-001 → hongjiacheng BZT52C6V2 (C19077403, preferred; D1-D4), SX-R-011/036/042 → UNI-ROYAL 0805W8F (C17455, C17797, C17818, preferred). Datasheets checked (facts and RoHS sources in `parts.csv`): TL072CDT pinout and limits as TI's, ICC the same, so the power budget is unchanged; 78L05G-AB3-R pins 1 O 2 G 3 I as the KiCad symbol (the -AB3-C-R variant is G I O); BZT52C6V2 SOD-123 matches KiCad `D_SOD-123`. Filter, level, meter and chain sheets rebuilt; netlists match, ERC 0/0. `costs.py extended`: 82 → 80 fee types.
- 2026-10-10, schematic (levers, delegated): U303 is a DG413: PFL L/R on the NO sections 1 and 4, SC send on the NC section 2 driven by SC_OFF from SW302 pin 1 (released = high), R315 moved to pin 1, no part added (decision 139). Values on E24 with JLCPCB basic/preferred UNI-ROYAL parts (decision 140): input trim stage, filter scaling, cutoff summer (R183 = 150k + new R187 12k; RV182 redrawn in the FCV column), fader law (new pairs R207+R223, R208+R224, R213+R225; `simulation/level/` rerun, within 0.4 dB of the design from +10 to −60 dB), SC send 47k, meter ladder (within 0.21 dB). New SX-R-092 to SX-R-106. Reference scripts give the button LEDs their 0805 footprints and part numbers. Netlists match (filter 81, level 44, routing 46 nets), ERC 0/0, changed areas looked at. `tools/costs.py estimate` (4 channels): €1,035 → €963.
- 2026-10-10, schematic (levers, delegated: "work on this autonomously"): TL072 difference receiver with 10k 0.1 % resistors instead of the AD8273 (decision 143; new R19-R26, SX-R-107); MUTE and DUCK switched by the buttons, U206 DG413 and C235/C236 removed, R220/R222 now 100k hold resistors on MUTE_V/DUCK_V with pin 1 open so no contact sequence can short the rail (decision 142, after the architect review); temperature compensation to the backlog, R108/R158 plain 820 Ω (decision 141); trimmers from Mouser, CUTOFF pot from Tayda A-4730. Netlists match (input 46, level 41 nets), ERC 0/0, drawings looked at. Card load 110 / 93 mA typical, sizing 171 / 139 mA. `tools/costs.py estimate` (4 channels): €946 (€1,035 on main before this day's sessions).
- PCB: not started; waits for the breadboard, the SSI2144/SSI2162 RoHS declaration and the cable mock-up.

## Provisional until the breadboard

`simulation/filter/BREADBOARD.md` tests 1-10 set R111/R161 (filter output scale, now 9k1 for the 18k attenuator; scale a breadboard value found with 17.4k by 18/17.4) and R120/R170 (Q current limit, now 36k: about 281 µA maximum with R184 = 12 k, decisions 129 and 140). Keep any new value on E24 or an E24 pair (decision 140). Then edit `filter_wired.py` / `filter_build.py`, run `scripts/rebuild_all.sh`, and update `docs/decisions/channel-card.md`.

## Waiting for the user's confirmation

- **Lever 11, hand-soldering consigned parts:** which of the easy consigned types to hand-solder (estimate under Cost-cut levers, item 11). The SSI2144 stays with JLCPCB (user, 2026-10-10).
- **Prototype-scope wording (decision 142):** root `CLAUDE.md` now says buttons carry logic, LED and DC control currents, audio never; the user confirmed the redesign, not yet this wording.
- Decisions 139-143 were made under the user's delegation ("confirmed (delegated)" in `INDEX.md`): review them in `docs/decisions/channel-card.md`.

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

## Next

1. Breadboard the SSI2144 when parts arrive (now with test 11, X5R coupling caps, and test 12, fixed V/oct and drift; buy two LCSC C13585 for test 11) (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`). Test 10 (fader law) wants one OPA2171 (SOIC-8, adapter) and one TL072; with two TL072s, skip the 0 % row (`simulation/filter/BREADBOARD.md`).
2. RoHS gaps: SSI2144/SSI2162 declaration (requested, waiting); copy the orderable MPNs the audit checked (NE5532DR, LM339DR, DG413DY-T1-E3, LM13700MX/NOPB) into the MPN column at BOM time. At the next LCSC check run, add SX-R-089 (TFPT, Mouser-only: hand-solder or consign) and SX-R-090 to `docs/lcsc-check.csv` / `tools/lcsc_check.py`.
3. Cable mock-up (decision 109).
4. PCB layout.

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

### From the master session (2026-10-10, for this board to decide)

Fee types the channel shares with the master: the fee only goes away when both boards drop the part. The master checked these candidates (`hardware/master/STATUS.md`, Extended-part review):

- **OPA2171 → LM358DR2G: dropped.** onsemi LM358/D Rev. 27 gives no output figure within 0.5 V of V− while sinking, and ±15.1 V is only 0.9 V from its ±16 V rating; the fader buffer needs the −15 V end (decision 102).
- **10 µF / 47 µF SMD electrolytics → ceramic: not on the LM337 output.** onsemi LM337/D Rev. 11 p. 7 warns ceramic or low-ESR output capacitors can oscillate. JLCPCB has no fee-free SMD aluminium electrolytic.
- **220p C0G (SX-C-001):** no fee-free C0G 220p exists; 2 × 100p C0G basic (C1790, 200 pF) or 220p X7R basic (C107145) would remove the type if both boards switch (master: AUX return RFI and C407).
- **TL062 (SX-IC-024):** a TL072 instead would remove the type on both boards but undoes decisions 123 and 126 (about +1.2 mA per amplifier).
- **LM339 → LM393 (basic, dual):** twice the packages; not recommended.

## For /system

- **Decision 142 against decision 69 (architect review 2026-10-10, CONFLICT):** decision 69 (system) has one button pole drive a logic line into a DG413; MUTE and DUCK now switch −15 V and SC_ENV through the contacts, and the confirmed prototype-scope line in the root `CLAUDE.md` was reworded in this board session. Needs a /system refinement of 69 and the user's confirmation of the wording. The contact-sequence risk the review also raised is removed on the board (pin 1 open, 100k hold resistors).
- `docs/INPUT-MODULE.md` (receiver name fixed by /system 2026-10-10): still note the new input impedances (20k on IN+, 30k on IN−; a mono source normalled to both IN+ sees 10k).

- R217 30k1 (SC_ENV into the channel control summer; also the master's AUX-return DUCK inputs): the only off-E24 value left on the channel card. 30k (E24, SX-R-050 basic) moves the ducking scale by 0.03 dB; the SC_ENV chain line in `docs/ARCHITECTURE.md` names 30.1 kΩ, so the change is a /system call.

