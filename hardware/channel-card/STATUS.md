# Channel card status

Updated 2026-10-06.

## Where it stands

- Schematic complete: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0 errors 0 warnings.
- PCB: not started; waits for the breadboard.

## Provisional until the breadboard

`simulation/filter/BREADBOARD.md` tests 1-10 set R111/R161 (filter output scale) and R120/R170 (Q current limit). Then edit `filter_wired.py` / `filter_build.py`, run `scripts/rebuild_all.sh`, and update `docs/decisions/channel-card.md`.

## Waiting for the user's confirmation

- 72: SC_ENV scale +1 V = 10 dB of ducking (**[proposed]** in `docs/decisions/channel-card.md`).

## Parts still to choose

Resonance pot (10k reverse audio), CV jack (vertical 6.3 mm), meter and button LED parts and colours, IDC headers, CUTOFF/level pot MPNs.

## Next

1. Breadboard the SSI2144 when parts arrive (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`).
2. PCB layout.

## For /system

- SC_ENV ducking scale depends on the fader position (finding 1, MAJOR): once `/system` settles the scale and circuit, change the Level sheet's control summer (R215, R217, R218, U205B). `docs/reviews/2026-10-06-system.md`
- Q301 base current and the button pull-downs return through AGND (finding 4, MINOR).
- The channel card budget script (finding 2) belongs to the `/system power budget` session.
