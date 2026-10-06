# Master card status

Updated 2026-10-06.

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
