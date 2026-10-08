# Master card status

Updated 2026-10-08.

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95).
- PCB: not started.

## Waiting for the user's confirmation (**[proposed]** in `docs/decisions/master-card.md`)

- 89: Q5 of the AS3046D unused; makeup reaches +22 dB at full AMOUNT (2 dB past the SSI2162's +20 dB spec), check on the breadboard.
- 90: a silent patched EXT cable still selects EXT; no separate EXT LED.
- 91: no output coupling capacitors on the AUX sends.
- 92: only the positive raw rail is monitored for relay drop-out.
- 93: master meter colours (green -30 to 0, yellow +3 to +9, red +12 and clip).
- 94: headphone gain 2; cue arrives inverted relative to main; PFL LED yellow.

## Check before layout

- **Fader buffer input range (from /system, 2026-10-08):** the fader runs from −15 V to ground and its wiper drives the TL072 buffer's + input directly (U206A and U306A on the AUX returns, U705A on master out). TI SLOS080W gives the TL072H's common-mode range as (VCC−) + 1.5 V to VCC+ (below about −13.6 V is outside it); the older TL072 die is specified at ±11 V minimum, −12 V typical, which puts the bottom fifth or more of the travel out of range. The classic TL07x reverses output phase when the input goes below that limit, which would swing VB positive and could send the VCA to full gain at the bottom of the fader; whether the orderable TL072 (MPN not yet chosen, SX-IC-007) does so is not verified. Possible fixes: a resistor from the fader's pin 1 to −15 V (the wiper then stops about 2 V above the rail; rescale the law resistors), or a part whose input range includes V−. Check the law's bottom end (−113 dB) after the change, and on the breadboard fader test (`simulation/filter/BREADBOARD.md`, control-voltage test). The channel card's answer (decision 102, 2026-10-08): an OPA2171 for the fader buffer and the control summer, with the superdiodes kept on a TL072, because the OPA2171's back-to-back input diodes would conduct in an open-loop superdiode; simulated in `simulation/level/` (bottom about −102 dB).
- **Power lever, [proposed] (from /system, 2026-10-08; `docs/ROADMAP.md`, Power-cut candidate 2):** check U206, U207, U306, U307, U705, U706, U407, U409, U410, U802 and U804 for a TL062 (swing, input range against the fader buffer item above, load, slew), then rerun `scripts/power_budget.py`.
- Power ribbon header J901 (SX-CONN-008) is now Würth 61200821621 (3 A per contact, hand-soldered, not at LCSC; decision 100): check the footprint against Würth's drawing.
- G6K NC/NO contact assignment against Omron's terminal diagram (taken from KiCad's G6K-2 symbol).
- The dual 100 kΩ reverse-log (C) pot for the sidechain LPF may not exist in Alpha's range.
- R421 (compressor, SX-R-021, ERA-V33J102V) has an 0805 footprint; the part is 0603 (as on the channel card). Fix in the compressor scripts (`docs/reviews/2026-10-06-system.md`, finding 3, MAJOR).
- LCSC stock check not yet rerun for the master card parts (`tools/lcsc_check.py`).

## Next

0. **Decision 97 (from /system), before layout:**
   - Sidechain sheet: the SC_ENV buffer U505B becomes a unity inverter (two equal resistors), its feedback taken from after R521 (100 Ω), so SC_ENV runs 0 to −4 V. Add a small Schottky diode (for example BAT54; check its reverse leakage at 4 V) with the anode on SC_ENV and the cathode on AGND, so SC_ENV cannot rise above about +0.3 V; in normal use (0 to −4 V) it is reverse biased. Rerun `simulation/sidechain/run.py` with the inverted output and a 1.7 kΩ load.
   - Both AUX return sheets: the same change as the channel Level sheet (R232/R332 to VSUM as 30k1, remove R233/R333, VPLUS to AGND).
   - Decision 98: Q501's emitter (Sidechain) and the button pull-downs R523, R525, R527 (Sidechain), R455 (Compressor), R237, R239, R241 and R337, R339, R341 (AUX returns) go from AGND to PGND.
   - Rebuild, check the netlists, ERC.

PCB layout, after the power board schematic and the channel card layout.

## For /system

(none)
