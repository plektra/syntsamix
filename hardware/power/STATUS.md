# Power board status

Updated 2026-10-10 (/system power brick: full-size brick GSM220B24-R7B, decision 145).

## Where it stands

- Schematic complete: four sheets (input and clock, +20 V buck, −20 V inverter, outputs), every netlist check 0 problems, ERC 0 errors 0 warnings (decision 100). 2026-10-08: start-up ramp added on both converters (C214/D202/D203/R207, C314/D302/D303/R307).
- Converter values derived in `scripts/design.py`; LC filter simulated (about 47 dB at 400 kHz at the filter, 63 dB at the cards; peaking about 4.4 dB near 4 kHz).
- PCB: not started.

## Waiting for the user's confirmation

(none: the UVLO, oscillator, switch and LED position and the L / F categories were confirmed 2026-10-08)

## Check before layout

- **Full-size brick (from /system, 2026-10-10, decision 145):** the 16-card brick is the GSM220B24-R7B (221 W) instead of the GSM160B24-R7B. Same R7B plug and pinout, 24 V ±3 %, so the KPJX-4S jack, the SMBJ24A note and this board are unchanged. In `scripts/startup_sim.py` replace the GSM160B24 limit (168 W) in `P_LIMITS` and the docstring with the GSM220B24: overload 105-135 % in hiccup mode (GSM220B-SPEC 2026-05-09), so 105 % of 221 W = 232 W; the 54 W ramp is far below either limit, so no result changes.
- **Placement (from /system, 2026-10-09, decision 109; `docs/MECHANICAL.md`):** the power board sits beside the master at the right end of the unit. Its output headers (master, chain 1, chain 2), the cable lengths to each group, and the rear-edge brick jack and power switch wait for the master section and power board topic in `MECHANICAL.md` (Open, item 2): do not place them before it.
- **Start-up ramp (settled in decision 100, check on the bench):** `scripts/startup_sim.py` (averaged ngspice model) showed the fixed 2.6 ms soft-start into about 1.1 mF per rail takes 183 to 262 W from the brick (hiccup threshold 126 W). The 47 nF / 1N4148W ramp into FB keeps it at about 54 W; rails reach 19 V about 40 ms after switch-on. On the bench: the start-up with all prototype cards connected (brick input current, no hiccup), and that the output does not misbehave while FB is held up at low output voltage (frequency foldback does not act then; the ramp current is far below the switch limit, so the minimum on-time should only cause pulse skipping).
- **Minimum off-time at 445 kHz:** the buck runs at about 83 % duty, an off-time near 375 ns at the fast end of the oscillator spread; the TPS54560 refreshes BOOT by skipping pulses near 100 % duty. Check SLVSBN0C for a minimum off-time figure before layout.
- **Per-header fuse coordination:** BSMD1812-200 holds 1.66 A at 50 °C; a full chain of 8 cards at the sizing figure is 1.40 A but 1.84 A at worst case (decisions 96, 123; `ARCHITECTURE.md`, Power, updated by /system 2026-10-09), and a 2-4 A fault may not trip it while the 1 A IDC socket contacts carry up to 2 A each. Recheck at full size (larger fuse or 3 pins per rail is a `/system` matter).
- Voltage drop through the per-header fuse (resistance not found) and the 2.2 µH filter against the 19 V raw minimum.
- Brick polarity: Mean Well R7B pins 1 and 4 = +24 V; the jack is wired by Kycon's numbering. Work the pin mapping through the key position on Mean Well's drawing, and check with a meter on the first brick.
- Parts to choose: power switch (SX-SW-003), 100 µF 50 V input bulk capacitor (SX-C-021), 10 pF C0G 100 V sync capacitor (SX-C-022).
- Footprints to draw from the maker's drawings: Kycon KPJX-4S, Bourns SRP1265A (L201, L301).
- Unverified facts: L78M05 DPAK pinout (from KiCad's LM78M05_TO252: 1 IN, 2 GND tab, 3 OUT; ST DS0425 Figure 2 not read as text); SS54 5 A and VF (LCSC listing only); Würth header 3 A per contact (PDF text, not the rendered page); KNSCHA 100 µF size (radial footprint assumed).
- The level of the AC-coupled sync clock at RT/CLK (10 pF into 243 kΩ, TI's recommended network) should cross 1.7 V cleanly: check on the bench.
- The SMBJ24A's 24 V standoff is below the brick's 24.7 V maximum; leakage at 24.7 V is not specified (breakdown 26.7 V minimum).
- LCSC stock check not yet run through `tools/lcsc_check.py` for these parts.

## Layout notes

- Keep each converter's input loop (VIN ceramics, IC, catch diode) tight; on the inverter, its input ceramics go from VIN to the −20 V node.
- Q102 (soft start) gets a copper pad; the 4 A input fuse stays away from the converters' heat (it holds only 3.0 A at 50 °C).
- The power board has no connection to AGND or the frame: mounting holes isolated (the star point is on the master card).

## Next

1. PCB layout (after the channel card PCB, per `docs/CONTINUE-FROM-HERE.md`).
2. Full-size supply (about 4 A per rail) after the prototype cards are measured (decision 96): the −20 V inverter needs a controller with external MOSFETs.

## RoHS

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; invariant 9 (decision 122); standard passives get their source when the BOM is fixed; the audit of this board's registered parts runs before the first PCB order (`docs/CONTINUE-FROM-HERE.md`).

## Cost-cut levers [proposed] (2026-10-09)

Cost frame set by the user (2026-10-09): prototype of 4 channels (maybe 2; 2026-10-10: costs tracked for 4, 8 and 16-channel builds; this board as drawn already covers it), the full console cost kept in view for a possible product; overview in `docs/ROADMAP.md`, Cost review. This board is about €40 in parts plus a 24 V brick (about €45-55 for 150 W). Through-hole parts are hand-soldered by the user (decision 133). None of these is decided:

1. **Full size without a new 4 A design:** instead of the external-MOSFET inverter of Next item 2, use two copies of this board at full size, one per power group (each about the master plus 8 cards, or 8 cards alone). Saves the design work and a new set of extended parts; costs a second board (about €40) and changes how the master and the two chains are fed (decisions 80, 81, 96: a `/system` matter). First check whether this design carries 8 cards plus the master (about 2.0 / 1.6 A at the sizing figures) within the TPS54560 inverter's switch-current limit.
2. **Brick:** settled by decision 145 (2026-10-10): one brick, the GSM220B24-R7B (221 W, EUR 72.90 at TME) for 16 cards, the GSM120B24-R7B stays on the prototype. Two bricks (in series or one per power board) were rejected by the user: one mains cord only.
3. Value selection is a standing rule now: see "Component values" below (decision 134).
4. Supply: the 330 µF hybrid capacitor EEHZK1V331P (SX-C-019, 4 per board) showed 0 stock at LCSC on 2026-10-09 (C278516, minimum order 15); check stock or an alternative before ordering.

From the system cost review of 2026-10-10 (`docs/reviews/2026-10-10-cost-system.md`, with savings and caveats). None of these is decided:

5. **Divider values:** 732k, 42k2, 15k8 and 243k are off E24, and 240k is E24 with no fee-free part. Moving them to fee-free E24 values or pairs needs a rerun of `scripts/design.py`: the ±20 V outputs and UVLO thresholds are reliability items.
6. **SS54 SMC → SS54 SMA** (C22452, JLCPCB basic): one fee type fewer; check its thermals at the converter's duty first.
7. Lever 4 can be closed: the EEHZK1V331P is back in stock at LCSC (5,666 on 2026-10-10).

## Component values (decision 134)

This board owns its value selection (rule in `CLAUDE.md`). Values outside E24 on 2026-10-09 (from the BOM export; all 0805 resistors; every capacitor is already E24):

| Value | References | Reason (to record) |
|---|---|---|
| 732k, 42k2 | R201, R301, R202, R302 | converter dividers, set by `scripts/design.py` |
| 15k8 | R203 | set by `scripts/design.py` |
| 243k | R204, R304 | set by `scripts/design.py` |

4 types, 7 parts. Check in `scripts/design.py` whether E24 values (or E24 pairs) keep the output voltages and UVLO thresholds within tolerance.

### Fee-free parts (decision 137, LCSC search 2026-10-10)

- BZT52C12 (SX-D-010, LCSC C19077410) is already a JLCPCB preferred part: no fee.
- The converter parts (TPS54560, SQJ457EP, SRP inductors, hybrid and 100 V ceramic capacitors, SMC Schottkys, PTC fuses) are extended; not yet searched for fee-free equivalents. `python3 tools/costs.py extended` lists them.

## For /system

(none)
