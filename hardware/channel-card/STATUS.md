# Channel card status

Updated 2026-10-08 (decisions 97, 98, 102 drawn).

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

- **Power lever, [proposed] (from /system, 2026-10-08; `docs/ROADMAP.md`, Power-cut candidates 1 and 2):** U107 NE5532 → TL072; check U205, U401 and U404 for a TL062 (swing, input range, load, slew), then rerun `scripts/power_budget.py`. U204 is off the list (OPA2171, decision 102). U205 now holds both superdiodes: their inputs stay between about −5.7 and +6.7 V, and the output runs open loop towards the rail when a diode is off, so check the TL062's swing and recovery there.

## Next

1. Breadboard the SSI2144 when parts arrive (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`). Test 10 (fader law) now wants one OPA2171 (SOIC-8 only, needs an adapter; not in the order yet) and one TL072; with two TL072s, skip the 0 % row (`simulation/filter/BREADBOARD.md`).
2. PCB layout.

## For /system

- Decision 102 lowers the channel card budget (`scripts/power_budget.py`): typical 121 / 103 mA (was 122 / 105), worst case 249 / 214 mA (was 253 / 218), sizing 186 / 154 mA (was 189 / 157), LM317 1.22 W worst case. `tools/system_power_budget.py`: prototype sizing 1.34 / 1.10 A, 49 W; full size sizing 3.57 / 2.95 A, 130 W ; power ribbon sizing 0.74 A per pin (`docs/ARCHITECTURE.md` lines 47-51 still show 122 / 105, 253 / 218 and 189 / 157 mA, 1.35 / 1.11 A, 3.6 / 3.0 A at 132 W and 0.76 A per pin; `docs/CHAIN.md` line 48 shows the same old channel figures and 0.76 A). No budget is exceeded; update both in the next /system session.
