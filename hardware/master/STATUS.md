# Master card status

Updated 2026-10-08 (decisions 97, 98, 103, 104 drawn).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104).
- 2026-10-08: decisions 97 and 98 drawn. AUX returns: R232/R332 30k1 into VSUM, R233/R333 removed, summer + input on AGND. Sidechain: DEPTH negative (R518 to −15 V), U505B fed back after R521, D504 BAT54T1G clamp (decision 104). Q501 emitter and the button pull-downs R237/239/241, R337/339/341, R455, R523/525/527 on PGND. Fader-law buffers and summers U206, U306, U705 on OPA2171s, superdiodes on the TL072s U207, U307, U706 (decision 103). R421 on its 0603 footprint (system validation finding 3). Sidechain simulation rerun; power budget 340 / 269 mA typical, sizing 589 / 476 mA.
- PCB: not started.

## Waiting for the user's confirmation (**[proposed]** in `docs/decisions/master-card.md`)

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

- `docs/ARCHITECTURE.md`, chain lines table: SC_ENV is "Driven by master card, low impedance (inverter, feedback after 100 Ω)"; the master now uses a follower on a negative hold voltage (decision 104). Same contract (`CHAIN.md` wording already fits); suggested wording: "(follower on a negative DEPTH, feedback after 100 Ω; decision 104)".
- `docs/ARCHITECTURE.md`, open items paragraph: system validation finding 3 (R421 footprint) is settled; R421 is on `R_0603_1608Metric`.
- `docs/ARCHITECTURE.md`, power budget (update together with the channel card's note, whose system totals predate decision 103): after decisions 102 and 103, `tools/system_power_budget.py` gives master typical 340 / 269 mA, worst case 719 / 594 mA, sizing 589 / 476 mA; prototype typical 0.82 / 0.68 A, sizing 1.33 / 1.09 A (48 W); full size sizing 3.56 / 2.94 A (130 W), typical 2.28 / 1.92 A, worst case 4.70 / 4.02 A; ribbon 0.74 A per pin sizing. All slightly below the recorded figures.
