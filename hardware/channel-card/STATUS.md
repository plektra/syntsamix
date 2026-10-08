# Channel card status

Updated 2026-10-06.

## Where it stands

- Schematic complete: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0 errors 0 warnings.
- PCB: not started; waits for the breadboard.

## Provisional until the breadboard

`simulation/filter/BREADBOARD.md` tests 1-10 set R111/R161 (filter output scale) and R120/R170 (Q current limit). Then edit `filter_wired.py` / `filter_build.py`, run `scripts/rebuild_all.sh`, and update `docs/decisions/channel-card.md`.

## Waiting for the user's confirmation

(none)

## Parts still to choose

Power ribbon IDC headers (J503/J504) and the ribbon cable: at least 1 A per contact (decision 96); SX-CONN-008 is now Würth 61200821621 (3 A per contact, hand-soldered, not at LCSC; decision 100): add its ProjectPN field to J503/J504 and check the footprint against Würth's drawing at layout. Regulator cooling: the LM317 dissipates 1.24 W worst case (decision 96 sizes a card's own parts for its worst case); free air at about 50 °C/W (not checked against the datasheet) gives about 102 °C at 40 °C ambient, just over the 100 °C used for the master (decision 95). Choose copper area or a small heatsink at layout. Supply budget: `scripts/power_budget.py` (rerun it after changing parts that draw current).


Resonance pot (10k reverse audio), CV jack (vertical 6.3 mm), meter and button LED parts and colours, IDC headers, CUTOFF/level pot MPNs.

## Next

0. **Level sheet, decision 97 (from /system):** SC_ENV is now negative (0 to −4 V, −1 V = 10 dB). Move R217 from VPLUS to VSUM and change it to 30k1 (register the value in `parts.csv`), remove R218, tie U205B's + input (VPLUS) to AGND. Update `level_build.py` and `level_wired.py`, rebuild, check the netlist, ERC. Then simulate the summer: 10 dB/V at fader 15 %, 50 %, 75 % and 100 %, and the ducking attack with C224.
0. **Decision 98 (from /system):** Q301's emitter (Routing) and the button pull-downs R17 (Input, drawn only in `input_wired.py`), R186 (Filter), R220, R222 (Level), R313, R315, R317 (Routing) go from AGND to PGND. Same rebuild, netlist check and ERC.
1. Breadboard the SSI2144 when parts arrive (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`).
2. PCB layout.

## For /system

(none)
