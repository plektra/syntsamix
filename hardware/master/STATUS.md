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
- LCSC stock check not yet rerun for the master card parts (`tools/lcsc_check.py`).

## Next

PCB layout, after the power board schematic and the channel card layout.

## For /system

(none)
