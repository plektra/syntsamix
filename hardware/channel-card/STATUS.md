# Channel card status

Updated 2026-10-09 (decisions 97, 98, 102 drawn; mechanical notes from decisions 106-109).

## Where it stands

- Schematic complete: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0 errors 0 warnings; every sheet matches its reference netlist.
- 2026-10-08: decision 97 (SC_ENV through R217 30k1 into VSUM, R218 removed, summer + input on AGND), decision 98 (Q301's emitter and the pull-downs R17, R186, R220, R222, R313, R315, R317 on PGND) and decision 102 (U204 = OPA2171 for the fader buffer and the summer, both superdiodes on the TL072 U205) are drawn. The Level control is simulated in `simulation/level/` (law within 1.2 dB, ducking 10.07 dB per −1 V at every fader position).
- PCB: not started; waits for the breadboard.

## Provisional until the breadboard

`simulation/filter/BREADBOARD.md` tests 1-10 set R111/R161 (filter output scale) and R120/R170 (Q current limit). Then edit `filter_wired.py` / `filter_build.py`, run `scripts/rebuild_all.sh`, and update `docs/decisions/channel-card.md`.

## Waiting for the user's confirmation

(none)

## Parts still to choose

Power ribbon IDC headers (J503/J504) and the ribbon cable: at least 1 A per contact (decision 96); SX-CONN-008 is now Würth 61200821621 (3 A per contact, hand-soldered, not at LCSC; decision 100): add its ProjectPN field to J503/J504 and check the footprint against Würth's drawing at layout. Regulator cooling: the LM317 dissipates 1.22 W worst case (decision 96 sizes a card's own parts for its worst case); free air at about 50 °C/W (not checked against the datasheet) gives about 101 °C at 40 °C ambient, just over the 100 °C used for the master (decision 95). Choose copper area or a small heatsink at layout. Supply budget: `scripts/power_budget.py` (rerun it after changing parts that draw current).


Resonance pot (10k reverse audio), CV jack (vertical 6.3 mm), meter and button LED parts and colours, IDC headers, CUTOFF/level pot MPNs.

## Check before layout

- **Mechanical contract (from /system, 2026-10-08, decision 106; `docs/MECHANICAL.md`):** strip pitch 35 mm, PCB at most 33.0 mm wide and at most 318 mm deep (fits between the rails, decision 108); the cutoff CV jack (J181, vertical 6.3 mm) moves to its own spot centred above CUTOFF.
- **Chain headers (from /system, 2026-10-08, decision 109):** J501 (audio IN) and J503 (power IN) along the left edge, J502 and J504 (OUT) along the right edge, on the underside, long axis front to back, all at one distance from the front (rear half, clear of the fader). Record the chosen distance in `docs/MECHANICAL.md` (a contract: tell /system). Header orientation and crimping wait for the cable mock-up (decision 109).
- **Panel stack (from /system, 2026-10-08, decision 107):** PCB 10.0 mm below the panel; top-side parts at most 9.0 mm tall. Too tall as drawn: U501/U502 TO-220 vertical (lay flat, tab on copper for the 1.22 W worst case), C5, C6, C101, C107, C151, C157, C221, C271 (10 µF bipolar, footprint drawn 11 mm tall), C501, C506 (47 µF 35 V) and C503, C504, C508, C509, C512 (10 µF 25 V): pick parts at most 9 mm tall (low-profile radial or SMD) and update footprints, `parts.csv` and the budget notes. Check heights: C9-C12 film (FKS2 class), RV101/RV151/RV182 3296W trimmers (about 10 mm, not verified; they also need adjusting with the card assembled: access holes in the panel or a different trimmer), jumper headers with caps (set before the panel goes on). Fader: footprint must keep the frame's M2 holes clear; it is screwed to the panel before soldering. CV jack J181: vertical 6.3 mm with its nut face at 10 mm.
- **Power lever, [proposed] (from /system, 2026-10-08; `docs/ROADMAP.md`, Power-cut candidates 1 and 2):** U107 NE5532 → TL072; check U205, U401 and U404 for a TL062 (swing, input range, load, slew), then rerun `scripts/power_budget.py`. U204 is off the list (OPA2171, decision 102). U205 now holds both superdiodes: their inputs stay between about −5.7 and +6.7 V, and the output runs open loop towards the rail when a diode is off, so check the TL062's swing and recovery there.

## Next

1. Breadboard the SSI2144 when parts arrive (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`). Test 10 (fader law) now wants one OPA2171 (SOIC-8 only, needs an adapter; not in the order yet) and one TL072; with two TL072s, skip the 0 % row (`simulation/filter/BREADBOARD.md`).
2. PCB layout.

## For /system

(none)
