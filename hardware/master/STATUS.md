# Master card status

Updated 2026-10-09 (decisions 97, 98, 103, 104 drawn; mechanical notes from decisions 107, 109; notes from the channel card's parts session, decisions 110, 111, 116, 117).

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

- **Chain headers (from /system, 2026-10-08, decision 109; `docs/MECHANICAL.md`):** the master sits at the right end of the unit, so J101 (audio) meets the OUT of the card to its left: place it along the master's left edge, on the underside, long axis front to back, at the distance from the front that the channel card layout records. J901 (power) comes from the power board beside the master; its position is free until the master section is settled (`MECHANICAL.md`, Open).
- **Panel stack (from /system, 2026-10-08, decision 107; `docs/MECHANICAL.md`):** PCB 10.0 mm below the top panel, top-side parts at most 9.0 mm tall under it. Too tall as drawn: U901-U903 TO-220 vertical and the decision-95 heatsinks on U901/U902, the 10 µF bipolar radials (C205, C206, C209, C210, C305, C306, C309, C310, C401, C402, C701, C702, C707-C710), the electrolytics C755, C756, C901, C903, C904, C906, C908, C909, C912, and the G6K relays K701, K702, K751 (check their height). Where the heatsinks go (outside the panel area, on the rear edge, or the power board) is settled with the master section in a `/system mechanical` session.
- **Power lever, [proposed] (from /system, 2026-10-08; `docs/ROADMAP.md`, Power-cut candidate 2):** check U207, U307, U706 (superdiodes; U206, U306, U705 are OPA2171s since decision 103), U407, U409, U410, U802 and U804 for a TL062 (swing, input range, load, slew), then rerun `scripts/power_budget.py`.
- Power ribbon header J901 (SX-CONN-008) is now Würth 61200821621 (3 A per contact, hand-soldered, not at LCSC; decision 100): check the footprint against Würth's drawing.
- G6K NC/NO contact assignment against Omron's terminal diagram (taken from KiCad's G6K-2 symbol).
- The dual 100 kΩ reverse-log (C) pot for the sidechain LPF may not exist in Alpha's range.
- LCSC stock check not yet rerun for the master card parts (`tools/lcsc_check.py`); BAT54T1G (SX-D-014) still needs an LCSC code (the OPA2171 has C40904).
- Breadboard: hear the ducking through the channel's 10 ms smoothing (decision 97) and the bottom of the master level pot (about −102 dB, decision 103).

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; the audit of this board's registered parts is planned in /system.
- **From the channel card (decision 111, 2026-10-09):** the channel card's electrolytics went SMD (ROQANG RVT 47 µF / 10 µF 35 V from LCSC, Panasonic EEE-1VA100NP bipolar); the same parts would clear the master's 9 mm limit for its radials listed above.
- **From the channel card (decision 110, 2026-10-09):** the channel card moved its LM317/LM337 to D²PAK on PCB copper (onsemi LM317D2TR4G / LM337D2TR4G, about 36-45 °C/W). Not enough for the master's 10 °C/W need (decision 95; D²PAK floor about 32 °C/W), so the master keeps TO-220 with heatsinks unless its dissipation drops.

- **From the channel card (2026-10-09):** the chain headers are now chosen: SX-CONN-007 = Würth 61203421621 (2×17 straight WR-BHD), SX-CONN-008 = Würth 61200821621; the channel card sets Manufacturer/MPN/Supplier fields on its symbols, the master's bus and power sheets still carry the bare part numbers (add the same fields); drill the header holes 1.1 mm (Würth recommendation; KiCad's IDC footprints use 1.0 mm).

## Next

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: the checks above.

## For /system

(none)
