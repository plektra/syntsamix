# Power board: checklists and reference

Read for layout, ordering, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

## Before ordering

- Footprints drawn from the maker drawings: print `L_Bourns_SRP1265A` (L201, L301) 1:1 and check it against the part; the board's other footprints are KiCad's own.
- Brackets and the top strip's holes (decision 186, /system): the board side is two M3 holes H1/H2 with a 5 mm copper keep-out; check the bracket against the parts near H1 (J103) and H2 (the fuses) on the parts side.
- Power LED hole position in the top strip above J103 (decision 168, /system).
- RoHS audit of this board's parts; LCSC stock (`tools/lcsc_check.py` not run yet for these parts; recheck the EEHZK1V331P hybrid capacitors).
- Rebuild with `scripts/build_pcb.sh` after any schematic change and check DRC with schematic parity.

## Check before layout (kept for the bench and the full-size module)

- **Start-up ramp (settled in decision 100, check on the bench):** `scripts/startup_sim.py` (averaged ngspice model) showed the fixed 2.6 ms soft-start into about 1.1 mF per rail takes 183 to 262 W from the brick (hiccup threshold 126 W). The 47 nF / 1N4148W ramp into FB keeps it at about 54 W; rails reach 19 V about 40 ms after switch-on (rerun 2026-10-10 with the 21.31 V UVLO start of decision 156 and the GSM220B24's 232 W limit: unchanged). On the bench: the start-up with all prototype cards connected (brick input current, no hiccup), and that the output does not misbehave while FB is held up at low output voltage (frequency foldback does not act then; the ramp current is far below the switch limit, so the minimum on-time should only cause pulse skipping).
- **Minimum off-time at 445 kHz:** the buck runs at about 83 % duty, an off-time near 375 ns at the fast end of the oscillator spread; the TPS54560 refreshes BOOT by skipping pulses near 100 % duty. Check SLVSBN0C for a minimum off-time figure before layout.
- **Per-header fuse coordination:** BSMD1812-200 holds 1.66 A at 50 °C; a full chain of 8 cards at the sizing figure is 1.40 A but 1.84 A at worst case (decisions 96, 123; `ARCHITECTURE.md`, Power, updated by /system 2026-10-09), and a 2-4 A fault may not trip it while the 1 A IDC socket contacts carry up to 2 A each. Recheck at full size (larger fuse or 3 pins per rail is a `/system` matter).
- Voltage drop through the per-header fuse (resistance not found) and the 2.2 µH filter against the 19 V raw minimum.
- Brick polarity: Mean Well R7B pins 1 and 4 = +24 V; the panel jack (KPJX-PM-4S, decision 182) is wired pin n to J101 pin n by Kycon's numbering. Work the pin mapping through the key position on Mean Well's drawing, and check with a meter on the first brick.
- Brick jack lead (decision 182), on assembly: four 18 AWG wires crimped with SVH-21T-P1.1 contacts into a VHR-4N housing, soldered to the KPJX-PM-4S tails with heat-shrink, pin n to pin n; long enough to take the rear strip off. Screws: two M2.5 self-tapping, 6.6 mm plus the strip's 1.6 mm (about 8 mm), from the front.
- Parts: all chosen. Power switch: Legion SS11-BBIWG-R20-R rocker on the rear panel, wired to J102 (JST XH 2-pin; decision 157). C103: Nichicon UHE1H101MPD radial, hand-soldered; C207/C307: Samsung CL10C100JB8NNNC 10 pF C0G 50 V 0603 (decision 158). Power LED: Kingbright WP710A10LGD in a Bivar CR-104 clip on the top strip, wired to J103 (decision 168).
- Power rocker (decision 157), on delivery: the cheap rockers state no DC rating, minimum load or contact material; check that it switches the gate (about 0.12 mA, 24.7 V open) reliably over many operations. Make up the two leads (pre-crimped XH leads, soldered or crimped to the 4.8 mm tabs), long enough to take the rear panel off.
- Power LED (decision 168), on assembly: solder the pre-crimped XH leads to the LED with one heat-shrink sleeve per lead (Kingbright precautions), pin 1 to the anode (long lead); leave enough length to lift the top strip off. Check the brightness at about 2.2 mA under stage light; if it is too dim, R104 can drop to 4k7 (about 4.7 mA, IF max 25 mA).
- Unverified facts: L78M05 DPAK pinout (from KiCad's LM78M05_TO252: 1 IN, 2 GND tab, 3 OUT; ST DS0425 Figure 2 not read as text); Würth header 3 A per contact (PDF text, not the rendered page); KNSCHA 100 µF size (radial footprint assumed).
- The level of the AC-coupled sync clock at RT/CLK (10 pF into 243 kΩ, TI's recommended network) should cross 1.7 V cleanly: check on the bench.
- **Input EMI filter (decision 187), on the bench:** the 400 kHz ripple on the brick lead (current probe or a small loop around the lead, or the voltage at J101 against VIN_SW) with all prototype cards connected, compared with the model's roughly 36 dB gain; the start-up with C108 and L101 in (no change expected: the soft start charges them); no ringing on VIN_SW at a load step (filter damping by C103's ESR, assumed 0.05-0.4 Ω, not taken from the UHE datasheet). A medium-wave radio held near the brick lead and the ribbons is a cheap first check.
- The SMBJ24A's 24 V standoff is below the brick's 24.7 V maximum; leakage at 24.7 V is not specified (breakdown 26.7 V minimum).

## Layout notes (as routed, decision 186)

- Each converter's input loop is tight (input ceramics turned with VIN to the IC's VIN pin, their ground by vias to the plane; catch diode at the SW pin); on the inverter the input ceramics go from VIN to the −20 V node, and C310 sits at D301's anode.
- D201 (SS54, SMA) gets a copper pad for heat (decision 159: up to about 0.5 W worst case with hot leakage); check its temperature at full load on the bench.
- Input pi filter (decision 187): F101 upright in the rear corner, Q101/Q102 moved 8.7 mm to the rear, L101 between Q102 and C103, C108 and C102 on the VIN_PRE copper under L101 (C108's ground by a via next to it), the VIN_SW spine from L101's output.
- Q102 (soft start) gets a copper pad; the 4 A input fuse stays away from the converters' heat (it holds only 3.0 A at 50 °C).
- The power board has no connection to AGND or the frame: the bracket holes are unplated with a 5 mm copper keep-out (the star point is on the master card).

## Cost-cut levers [proposed] (2026-10-09)

Cost frame set by the user (2026-10-09): prototype of 4 channels (maybe 2; 2026-10-10: costs tracked for 4, 8 and 16-channel builds; this board as drawn already covers it), the full console cost kept in view for a possible product; overview in `docs/ROADMAP.md`, Cost review. This board is about €40 in parts plus a 24 V brick (about €45-55 for 150 W). Through-hole parts are hand-soldered by the user (decision 133). None of these is decided:

1. **Full size without a new 4 A design:** instead of the external-MOSFET inverter of Next item 2, use two copies of this board at full size, one per power group (each about the master plus 8 cards, or 8 cards alone). Saves the design work and a new set of extended parts; costs a second board (about €40) and changes how the master and the two chains are fed (decisions 80, 81, 96: a `/system` matter). First check whether this design carries 8 cards plus the master (about 2.0 / 1.6 A at the sizing figures) within the TPS54560 inverter's switch-current limit.
2. **Brick:** settled by decision 145 (2026-10-10): one brick, the GSM220B24-R7B (221 W, EUR 72.90 at TME) for 16 cards, the GSM120B24-R7B stays on the prototype. Two bricks (in series or one per power board) were rejected by the user: one mains cord only.
3. Value selection is a standing rule now: see "Component values" (decision 134).
4. Supply: the 330 µF hybrid capacitor EEHZK1V331P (SX-C-019, 4 per board) showed 0 stock at LCSC on 2026-10-09 (C278516, minimum order 15); check stock or an alternative before ordering.

From the system cost review of 2026-10-10 (`docs/reviews/2026-10-10-cost-system.md`, with savings and caveats). None of these is decided:

5. **Divider values:** done by decision 156 (2026-10-10): UVLO 680k / 39k, RT 240k, buck compensation 16k, four fee types fewer. The 240k feedback resistor stays extended (no fee-free part; a 24k / 1k divider would need a 470 nF ramp capacitor).
6. **SS54 SMC → SS54 SMA:** done by decision 159 (2026-10-11): D201 on D_SMA to match C22452 (JLCPCB basic); the D_SMC footprint did not match the recorded part.
7. Lever 4 closed (2026-10-11): the EEHZK1V331P is back in stock at LCSC (5,666 on 2026-10-10); recheck stock before ordering.

## Component values (decision 134)

This board owns its value selection (rule in `CLAUDE.md`). Since decision 156 (2026-10-10) every resistor and capacitor value is E24; none to list. The 240k (R204, R205, R304, R305: feedback and RT) is E24 but has no fee-free 0805 part (one fee type, kept: see lever 5).

### Fee-free parts (decision 137, LCSC search 2026-10-10)

- BZT52C12 (SX-D-010, LCSC C19077410) is already a JLCPCB preferred part: no fee.
- The converter parts (TPS54560, SQJ457EP, SRP inductors, hybrid and 100 V ceramic capacitors, SMC Schottkys, PTC fuses) are extended; not yet searched for fee-free equivalents. `python3 tools/costs.py extended` lists them.
