# Power board status

Updated 2026-10-08.

## Where it stands

- Schematic complete: four sheets (input and clock, +20 V buck, −20 V inverter, outputs), every netlist check 0 problems, ERC 0 errors 0 warnings (decision 100). 2026-10-08: start-up ramp added on both converters (C214/D202/D203/R207, C314/D302/D303/R307).
- Converter values derived in `scripts/design.py`; LC filter simulated (about 47 dB at 400 kHz at the filter, 63 dB at the cards; peaking about 4.4 dB near 4 kHz).
- PCB: not started.

## Waiting for the user's confirmation

(none: the UVLO, oscillator, switch and LED position and the L / F categories were confirmed 2026-10-08)

## Check before layout

- **Start-up ramp (settled in decision 100, check on the bench):** `scripts/startup_sim.py` (averaged ngspice model) showed the fixed 2.6 ms soft-start into about 1.1 mF per rail takes 183 to 262 W from the brick (hiccup threshold 126 W). The 47 nF / 1N4148W ramp into FB keeps it at about 54 W; rails reach 19 V about 40 ms after switch-on. On the bench: the start-up with all prototype cards connected (brick input current, no hiccup), and that the output does not misbehave while FB is held up at low output voltage (frequency foldback does not act then; the ramp current is far below the switch limit, so the minimum on-time should only cause pulse skipping).
- **Minimum off-time at 445 kHz:** the buck runs at about 83 % duty, an off-time near 375 ns at the fast end of the oscillator spread; the TPS54560 refreshes BOOT by skipping pulses near 100 % duty. Check SLVSBN0C for a minimum off-time figure before layout.
- **Per-header fuse coordination:** BSMD1812-200 holds 1.66 A at 50 °C; a full chain at the sizing figure is 1.51 A (decision 96) but 2.0 A at worst case, and a 2-4 A fault may not trip it while the 1 A IDC socket contacts carry up to 2 A each. Recheck at full size (larger fuse or 3 pins per rail is a `/system` matter).
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

## For /system

(none)
