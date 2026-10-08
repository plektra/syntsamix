# Master card status

Updated 2026-10-08 (decisions 97, 98, 103, 104 drawn).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104).
- 2026-10-08: decisions 97 and 98 drawn. AUX returns: R232/R332 30k1 into VSUM, R233/R333 removed, summer + input on AGND. Sidechain: DEPTH negative (R518 to −15 V), U505B fed back after R521, D504 BAT54T1G clamp (decision 104). Q501 emitter and the button pull-downs R237/239/241, R337/339/341, R455, R523/525/527 on PGND. Fader-law buffers and summers U206, U306, U705 on OPA2171s, superdiodes on the TL072s U207, U307, U706 (decision 103). R421 on its 0603 footprint (system validation finding 3). Sidechain simulation rerun; power budget 340 / 269 mA typical, sizing 589 / 476 mA.
- PCB: not started.

## Waiting for the user's confirmation (**[proposed]** in `docs/decisions/master-card-sheets.md`)

- 89: Q5 of the AS3046D unused; makeup reaches +22 dB at full AMOUNT (2 dB past the SSI2162's +20 dB spec), check on the breadboard.
- 90: a silent patched EXT cable still selects EXT; no separate EXT LED.
- 91: no output coupling capacitors on the AUX sends.
- 92: only the positive raw rail is monitored for relay drop-out.
- 93: master meter colours (green -30 to 0, yellow +3 to +9, red +12 and clip).
- 94: headphone gain 2; cue arrives inverted relative to main; PFL LED yellow.

## Check before layout

- **Power lever, [proposed] (from /system, 2026-10-08; `docs/ROADMAP.md`, Power-cut candidate 2):** check U207, U307, U706 (superdiodes; U206, U306, U705 are OPA2171s since decision 103), U407, U409, U410, U802 and U804 for a TL062 (swing, input range, load, slew), then rerun `scripts/power_budget.py`.
- Power ribbon header J901 (SX-CONN-008) is now Würth 61200821621 (3 A per contact, hand-soldered, not at LCSC; decision 100): check the footprint against Würth's drawing.
- G6K NC/NO contact assignment against Omron's terminal diagram (taken from KiCad's G6K-2 symbol).
- The dual 100 kΩ reverse-log (C) pot for the sidechain LPF may not exist in Alpha's range.
- LCSC stock check not yet rerun for the master card parts (`tools/lcsc_check.py`); BAT54T1G (SX-D-014) still needs an LCSC code (the OPA2171 has C40904).
- Breadboard: hear the ducking through the channel's 10 ms smoothing (decision 97) and the bottom of the master level pot (about −102 dB, decision 103).

## Next

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: the checks above.

## For /system

(none)
