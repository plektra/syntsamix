# Channel card: checklists and reference

Read for layout, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

## Check before layout

- **Mechanical contract (decisions 106-109, 175, `docs/MECHANICAL.md`):** strip pitch 35 mm, PCB at most 33.0 mm wide and 318 mm deep; PCB 10.0 mm below the panel, top-side parts at most 9.0 mm (all parts now comply); one audio header J501 (2×17) and one power header J503 (2×4) on the multi-drop chain cables (decision 175), underside, long axis front to back, pin 1 toward the front, key on the same side on every card; record each header's distance from the front and position across the card in `MECHANICAL.md` (tell /system); keep-out band across the full width over each header's length plus 15 mm front and back; check header, socket and cable depth against the inside height at that distance.
- **Meter (decision 119):** D411-D418 are drawn as `LED_SMD:LED_0805_2012Metric` (KT-0805G D411-D415, KT-0805Y D416-D417, NCD0805R1 D418; 2026-10-09). At layout: LEDs on a 6.0 mm pitch in one column, CLIP level with the fader's top travel end, two 1.5 mm non-plated holes for the bezel pegs, nothing taller than the bezel footprint allows under it; record the column position in `MECHANICAL.md`. Tune the 1k5 resistors per colour after a test print.
- **Regulator copper (decision 110):** about 20 × 20 mm of top copper per D²PAK tab, via-stitched to a bottom pour; U501 tab = +15V, U502 tab = −20V_RAW: keep apart and off AGND. The 89 / 82 °C worst case assumes 40 °C/W and 40 °C ambient (about 97-107 °C for U501 at the 57 °C design air of decision 167); check against onsemi LM337 Figure 19 once placed.
- **Chain header holes:** KiCad's `IDC-Header_2x17/2x04_P2.54mm_Vertical` drill 1.0 mm; Würth recommends 1.1 ± 0.15 mm for the 0.64 mm square pins: use 1.1 mm drills.
- **Input header J1 (decision 181):** Adam Tech BHR-12-VUA on KiCad `Connector_IDC:IDC-Header_2x06_P2.54mm_Vertical` (body 22.9 mm long as the drawing's 22.86; drill 1.0 mm against Adam Tech's 1.02 mm, fine for 0.64 mm square pins; key slot on the odd-pin side). The KiCad outline is 10.4 mm wide against the part's 8.80 mm, so the courtyard is a little generous. Place it near the rear edge within reach of the 150 mm flat cable (decision 160) and report its position to /system; pin 1 marked on the silkscreen, the key slot facing the same way on every card.
- **Trimmers and jumpers on the underside (decision 112):** RV101, RV151, RV182 (3296W, screw facing down; RV101/RV151 next to their SSI2144s) and JP101/JP151, JP102/JP152, JP182, J301/J302 on the bottom side, L/R pairs side by side with matching bottom-silkscreen labels, leads soldered on the top side, outside the keep-out of decision 121 (10 mm from each long edge over the header length plus 15 mm front and back; provisional until the mock-up), at most 10.5 mm below the PCB; nothing tall around them.
- **78L05 U503 (UTC 78L05G-AB3-R):** with R506 + R507 (decision 193) about 0.11 W worst case, about 95 °C junction at 57 °C inside air on the 357 °C/W implied by UTC's 350 mW SOT-89 rating (TJ 150 °C absolute maximum). Still give the middle (GND) tab a copper pour, and keep R506/R507 (73 mW each) a little apart from it. Bring-up: U503 pin 3 at least 7 V with every LED lit (about 8.5 V expected).
- **Solder jumper JP301 (decision 192):** bridged 1-2 (AGND) by the footprint; leave it. With 2-3 bridged (cut 1-2 first, or +5 V shorts to AGND) the bus assign selects FLT1/FLT2.
- **FREQ leg (decisions 130, 141):** R108/R158 are plain 820 Ω now (temperature compensation in the backlog); still place them next to their SSI2144 with short traces and leave room for an 0805 TFPT later.
- **Receiver (decision 143):** keep the 0.1 % resistors of each side together and the two input legs symmetrical (same trace lengths to the TL072), RFI caps C1-C4 next to R1-R4.
- **CV jack J181 (Thonkiconn):** 3 mm hole in the PCB under the barrel (Thonk note; the footprint has none), centred 6.48 mm from the S pad toward T; no traces or pour in it. Centred on the strip above CUTOFF (decision 106).
- **Fader:** KiCad `Potentiometer_Bourns_PTA6043_Single_Slide` matches the Bourns PTA drawing (Rev. 08/25). The M2 holes are tapped in the top of the frame, 71 mm apart, for panel screws from above: no PCB feature; choose the M2 screw length (1.6 mm panel + 3.5 mm spacer + the frame's thread depth, not stated by Bourns) so it cannot reach the track. Screwed to the panel before soldering. Keep the footprint compatible with the product-version TT PS60-10MC2BR10K if that costs nothing.
- **SSI2144 footprint (U101/U102):** `Package_SO:QSOP-16_3.9x4.9mm_P0.635mm` matches Sound Semiconductor's drawing PODPSSL16 (16-lead SSOP, JEDEC MO-137-AB, 0.635 mm pitch) and a measured chip (2026-10-14); pin 1 top-left at the notch, as the footprint. No further check before ordering.
- **Pot footprints:** the stock KiCad RD901F/RD902F footprints (slots 9.6 mm centre to centre, 7.5 mm from the pins) match Alpha's drawing SLH-211-414 (its 11.4 mm spans the slot ends).

## Panel and underside positions (decisions 194, 195; distances proposed)

d = distance from the card's front edge, u = from its left edge seen from above; the card's front edge is 1 mm behind the front rail's inner face and 21 mm behind the panel's front end. Source of truth: `ROW` and `FIX` in `scripts/floorplan.py` and `ROW` in `scripts/panel_render.py` (change them together).

| Item | Position |
|---|---|
| Fader | **the user 2026-11-24:** 9 mm right of the centreline (u 25.5); travel centre d 57 (body d 19 to 95), moved back so 25 mm of blank panel stays in front of it for tape (panel 14 to 39 mm from its front end, behind the screw head); panel drawing `scripts/panel_render.py` |
| Meter column | u 4.0 (12.5 mm left of the centreline); CLIP at d 87 (the fader's top travel end), −30 at d 45 |
| Rows (centres, d), the user's arrangement 2026-11-24 | controls pushed up to the rear rail, the freed depth as finger room: PFL (u 9.5) and MUTE (u 23.5) side by side at 108; SC SEND / DUCK / COMP BUS 127 (u 5.0, 16.5, 28.0: 11.5 mm apart, the widest the card allows; visible caps 8 mm square instead of 10 mm, the user 2026-11-24, on all buttons; the cap print needs a skirt under the panel to catch the LED beside the 8.5 mm switch body); AUX 2 at 151 (u 23.0) and AUX 1 at 173 (u 10.0), 6.5 mm each side of the centreline and 22 mm apart front to back (room for the printed scales; AUX 2 stays put because the audio header needs the run between it and BYPASS); RESONANCE (u 8.5, small knob) and BYPASS (u 24.5) side by side at 211; CUTOFF 236; CV AMT (u 8.5) and +KNOB (u 24.5) at 261; CV IN (u 8.5) and CV OUT (u 24.5) at 281; TRIM (u 8.5) and LOW CUT (u 24.5) at 303 (option C, decision 197) |
| Section lines (legend) | at d 115.6, 134.3, 188.6 and 288.0: fader with PFL and MUTE / SC, DUCK, COMP / AUX / filter with the CV jacks / input |
| Knob sizes (drawing) | CUTOFF 18 mm, RESONANCE and TRIM 12 mm, CV AMT 11 mm, AUX 16 mm; none chosen yet, and decision 114's list for these shafts ends at about 19 mm |
| Scales (drawing only, the user 2026-11-24) | eleven ticks around each pot: TRIM −14 and +28 dB at the ends (decision 26), CUTOFF one octave per tick, 20 Hz to 20 kHz (decision 52), RESONANCE 0 to 10, AUX −∞ to 0; marks between the ends of the audio-taper pots would need measuring |
| Legends (drawing only) | below each control, on the operator's side (the user, 2026-11-24): TRIM, LOW CUT, CV IN, CV OUT, CV AMT, +KNOB, CUTOFF, RESONANCE, BYPASS, AUX 1, AUX 2, SC, DUCK, COMP, PFL, MUTE; fader marks +10 to −∞ on decision 72's law, meter marks of decision 43 |
| Button LEDs | behind each plunger (5.9 mm toward the rear) |
| Power header J503 | underside, left edge (u 5.0), centre d 140.6 (body d 131.1 to 150.1, between the SC SEND button's pins and the AUX 1 pot's), pin 1 at d 136.8 toward the front |
| Audio header J501 | underside, right edge (u 28.0), centre d 180 (body d 154 to 206, between the AUX 2 pot's pins and the BYPASS button's), pin 1 at d 159.7 toward the front. The two headers are no longer on one line: with pots and buttons off the centreline neither edge has 71 mm free of control pins; the cables still do not share a depth |
| Underside keep-out band (decision 175) | d 116 to 221 |
| Input header J1 | **[proposed]** underside, along the card between the CV jacks, centre d 282, u 17.6 (KiCad courtyard d 270 to 294). The across-the-card candidate of decision 197 (d 287 to 296) collides with the CV jack and TRIM pins; the free alternative is across at about d 312, behind TRIM. Check the jack bodies beside it and the 150 mm cable at layout |
| Regulators | **[proposed]** on the underside under the fader's middle (d about 62 to 79, no control pins there), facing the perforated cover: TRIM now takes the rear, and decision 110 puts them on top. Copper to check at layout |
| Hand-set parts | J301/J302 in front of the band; filter trimmers and jumpers behind it |

With this arrangement the two-sided placement places 401 of 402 parts (C271, a 5 mm coupling capacitor, left over; 2026-11-25) with the 5 mm cans as drawn (top 65 % covered); no underside header sits on a control's pins.

Why the headers sit there: each header needs a run along one edge with no control pins above its body, 3.5 mm or more behind the front controls for the inside height (about 34 mm under the panel at the power header, so about 19 mm for header, socket and cable after the PCB and 3 mm to the cover **[estimate: check the Würth drawings]**), and the power header stays in front of the master's heatsink zone (decision 188).

Still to check at layout: the header, socket and cable depth on the Würth drawings; the printed button cap with its skirt (8 mm face over the 8.5 mm switch, LED beside it); the 11, 12 and 18 mm knobs on the T18 shaft; the scale marks between the ends of the audio-taper pots (measure); the regulator copper underneath against decision 110's figures.

## Check on first delivery or assembly

- **GPBS850L buttons (Electrokit 41012905):** the MPN was corrected on 2026-10-10 from GPBS850N, which is the momentary twin (Electrokit 41015527). When the second Electrokit order arrives, check that the delivered switches latch and that the pins match the GPBS850L datasheet Rev 2 (pin grid 2.5 mm, rows 5.4 mm, pressed = 2-3 and 5-6); size the printed caps for the 4.0 mm plunger.

- **T18 panel pots:** bushing thread M7×0.75 × 5 mm (Alpha's RD902F drawing; confirmed by Thonk support 2026-10-09 for the Thonk pots): check the nut fit; legs bent back parallel to the shaft and bracket tabs in the footprint slots. Tayda sells 9 mm and 16 mm horizontal Alpha pots under similar names (the C10K dual is an RV16A01F-20): check any further Tayda pot against its own drawing.
- **CV jack Thonkiconn:** the nut (thickness not on Thonk's drawing, typically about 2 mm) grips the 2.9 mm of thread left above the printed washer and the panel. Pinout settled (1 sleeve, 2 switch, 3 tip; pads S/TN/T).
- **LED brightness:** even out the button LEDs (12 k from +15 V, about 1 mA) per colour after a test with the printed caps; the same for the meter once its bezel is printed. Check on the first assembled card, not the bench (the 0805 LEDs come only with JLCPCB assembly, 2026-10-20): light one button LED at a time and look for bleed into the neighbouring caps; fix any bleed in the cap print (opaque wall or skirt, two-material print), since the LED position beside the switch is fixed at layout.
- **BOCHEN 3296W trimmers (decision 184):** the BOCHEN sheet numbers pins 1-2-3 but does not name the wiper: check with a meter that pin 2 is the wiper (as on the Bourns) before soldering, and that the body fits the Bourns 3296W footprint (2.5 mm drawn pitch against 2.54 mm).
- **CD4052B switches (decision 183):** at bring-up measure VEE at TP507 (about −5.9 to −6.5 V); press and release COMP BUS, PFL and SC SEND with audio running and listen for clicks on the main, cue and SC buses (charge injection into the master's virtual earths, expected no worse than the DG413's); check that a released PFL and SC send leave nothing on the cue and SC buses.

## Cost-cut levers (open)

Frame set by the user (2026-10-09): the prototype is 4 channel cards, maybe 2; the full 16-channel console's cost stays in view in case the mixer becomes a product; the filter stays (rejected as a fitting option: the SSI2144 ladder filter is one of the features that make the mixer stand out). Overview: `docs/ROADMAP.md`, Cost review; system review `docs/reviews/2026-10-10-cost-system.md`.

Done 2026-10-10: DG412 → DG413 (139), E24 values (140), tempco to the backlog (141), MUTE/DUCK by the buttons (142), TL072 receiver (143), Bourns trimmers from Mouser (LCSC C83686 would be about €2.70 per card cheaper, noted in `docs/ROADMAP.md`), CUTOFF pot from Tayda A-4730 (Tayda has no T18 9 mm A100K or A10K duals: TRIM and AUX stay at Thonk). `tools/costs.py estimate --channels 4`: €946 (€1,035 on main before 2026-10-10).

Open:

7. **Coupling capacitors: decided (decision 161, 2026-10-11).** Each 10 µF bipolar became two ROQANG 10 µF (SX-C-024) back to back, placed by JLCPCB with no new fee type; the X5R option is dropped (dearer than the pair). Breadboard test 11 checks the pair.
11. **Hand-soldering consigned parts: decided (decision 155, 2026-10-10).** The user hand-solders the SSI2144 ×2 (U101/U102) and the SSI2162 (U201) on the prototype (Assembly = "hand (decision 155)"), so neither type is consigned: 38 → 36 fee types, €794 → €788 for 4 channels. The bipolar 10 µF SX-C-023 is gone from the card since decision 161 (lever 7), so nothing here is consigned; the €30 handling ends once the master swaps too.
13. **Fixed V/oct scale (product):** replace RV182 with an E24 pair if breadboard test 12 shows the chips' scales within about ±2 %; one part and one calibration step fewer per card.
14. **Done 2026-10-19 (commercial-console comparison, levers 1 and 2):** trimmers BOCHEN 3296W from LCSC (decision 184, about €4.35 per card) and bus assign, PFL and SC send on CD4052B at the virtual-earth bus ends (decision 183, about €2.0 per card). Still open from that comparison: low-cut and filter bypass as virtual-earth switches too (would take the DG413 off the card: about €2.3 per card more, but needs a summing stage around each, so a circuit change), and the same review of the master's eight DG413s.

## Component values (decision 134)

This board owns its value selection (rule in `CLAUDE.md`). Since decision 140 (2026-10-10) every resistor and capacitor value is E24 with a JLCPCB basic or preferred part, with no exceptions since R217 became 30k (SX-R-050, basic; decision 153, 2026-10-10).

| Sheet | Value | References | Reason |
|---|---|---|---|
| (none) | | | |

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

Fee types the channel shares with the master: the fee only goes away when both boards drop the part. The master checked these candidates (`hardware/master/CHECKLISTS.md`, Component values):

- **OPA2171 → LM358DR2G: dropped.** onsemi LM358/D Rev. 27 gives no output figure within 0.5 V of V− while sinking, and ±15.1 V is only 0.9 V from its ±16 V rating; the fader buffer needs the −15 V end (decision 102).
- **10 µF / 47 µF SMD electrolytics → ceramic: not on the LM337 output.** onsemi LM337/D Rev. 11 p. 7 warns ceramic or low-ESR output capacitors can oscillate. JLCPCB has no fee-free SMD aluminium electrolytic.
- **220p C0G (SX-C-001):** no fee-free C0G 220p exists; 2 × 100p C0G basic (C1790, 200 pF) or 220p X7R basic (C107145) would remove the type if both boards switch (master: AUX return RFI and C407).
- **TL062 (SX-IC-024):** a TL072 instead would remove the type on both boards but undoes decisions 123 and 126 (about +1.2 mA per amplifier).
- **LM339 → LM393 (basic, dual):** twice the packages; not recommended.
