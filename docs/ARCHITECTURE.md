# Architecture

The system-level view: how the boards fit together, the numbers that cross board boundaries, and the invariants no board may break. Owned by `/system` sessions; board sessions read it but do not change it. Every figure names its source; **[estimate]** marks a figure not yet backed by a budget script or a measurement.

## System diagram

```
 DC brick 24 V (Class II, floating output)
      │
 ┌────▼──────────┐  power ribbon (8-pin)   ┌──────────────┐
 │ Power board   ├────────────────────────►│ Master card  │◄── star point: AGND-PGND join (net tie)
 │ buck/inverter │                         │ ±15 V, +5 V  │──► main out (THAT1646), headphones,
 └──┬─────────┬──┘                         │ bus summing, │    AUX sends/returns, SC EXT jack
    │ chain 1 │ chain 2                    │ compressor   │
    │ power   │ power                      └──────▲───────┘
    ▼         ▼                                   │ audio ribbon (34-pin), runs through every card
 cards 1-8   cards 9-16                    ┌──────┴───────┐   ┌──────────────┐
 (each card regulates ±15 V, +5 V)         │ Channel card ├───┤ Channel card ├── ... up to 16
                                           └──────▲───────┘   └──────────────┘
                                                  │ 10-pin header
                                           ┌──────┴───────┐
                                           │ Input module │ (passive, jacks)
                                           └──────────────┘
```

Each channel card has identical IN and OUT copies of both ribbons, wired straight through (decision 38). The prototype has 4 channel cards on chain 1.

## Interfaces (contracts)

| Interface | Document | Between |
|---|---|---|
| Audio ribbon, 34-pin | `docs/CHAIN.md` | master card, every channel card |
| Power ribbon, 8-pin | `docs/CHAIN.md` | power board, master card, channel cards |
| Input header, 10-pin | `docs/INPUT-MODULE.md` | channel card, input module |

## Cross-board budgets

### Power

Sizing rule (decision 96): a card's own parts are sized for its worst case (every IC at datasheet maximum, every LED lit, full signal load); parts shared by many cards (the power board converters, ribbon pins) for IC quiescent current at typical × 1.5 plus the use-dependent loads at their maximum. All figures at 20 V raw from `tools/system_power_budget.py`, which runs both cards' `power_budget.py` (rerun 2026-10-08 after decisions 102 and 103). The 1.5 factor is a judgment until the prototype cards are measured.

| Item | Value | Source |
|---|---|---|
| Raw rails | ±20 V nominal, unregulated in general; on the prototype from non-isolated converters on the power board (TPS54560 buck and inverter), the 24 V brick providing the isolation | decisions 40, 60, 81, 100 |
| Raw rail minimum under load | about 19 V: the master's relay drop-out comparator trips at 17.9 V; the LM317 needs about 2 V headroom above 15.1 V | decisions 92, 95 |
| Local rails on every card | ±15.1 V (LM317/LM337), +5 V (78L05 on channel cards, L7805 on the master) | decisions 78, 87 |
| Channel card load (+15 / −15 V) | typical 121 / 103 mA; worst case 249 / 214 mA; sizing 186 / 154 mA (AD8273 supply current **[unverified]**, 5 mA of the total) | decisions 96, 102, `hardware/channel-card/scripts/power_budget.py` |
| Master card load (+15 / −15 V) | typical 340 / 269 mA; worst case 719 / 594 mA; sizing 589 / 476 mA | decisions 95, 96, 103, `hardware/master/scripts/power_budget.py` |
| Prototype, 4 cards + master | sizing 1.33 / 1.09 A, about 48 W (typical 0.82 / 0.68 A); power board converters about 2 A per rail | decisions 96, 100 |
| Full size, 16 cards + master | sizing 3.56 / 2.94 A, about 130 W (typical 2.28 / 1.92 A; worst case 4.70 / 4.02 A, not used for sizing) | decision 96 |
| Power ribbon | injected in groups of 8 cards; about 0.74 A per pin (sizing; 1.00 A at worst case); connectors and cable rated at least 1 A per contact (the chosen Würth 61200823021 IDC socket is the limit at 1 A, so the worst case sits at its rating; the header is 3 A) | decisions 80, 96, 100 |
| Capacitance on each raw rail at switch-on | about 0.37 mF (prototype), 1.2 mF (full size), plus about 0.76 mF on the power board; the start-up ramp on both converters holds the brick at about 54 W while charging it (rails at 19 V about 40 ms after switch-on; bench check in `hardware/power/STATUS.md`) | system validation, finding 6; decision 100, `hardware/power/scripts/startup_sim.py` |

### Signal levels

| Item | Value | Source |
|---|---|---|
| Nominal level | +4 dBu | decision 46 |
| Internal maximum | about +20 dBu (±15 V rails) | decision 46 |
| Balanced outputs | up to +24 dBu | decisions 46, 83 |
| Soft-clip onset | about +14 dBu (channels and master bus) | decision 64 |
| Inputs | line levels up to hot Eurorack (±12 V peak); receiver at G = ½ | decisions 25, 33 |
| Buses | current summing: each card drives each bus through 22 kΩ, the master sums with 22 kΩ feedback (unity per channel) | decisions 74, 79; `CHAIN.md` |
| Meters | 0 = +4 dBu; master clip about 3 dB below the internal limit | decisions 43, 49 |

### Chain lines (audio ribbon)

| Line | Driven by | Read by | Notes |
|---|---|---|---|
| MAIN, COMP, AUX1, AUX2, CUE (L/R) | each channel card (22 kΩ) | master summing amps | |
| SC | channel cards with SC send on | master sidechain | mono, pre-fader, pre-mute |
| SC_ENV | master card, low impedance (follower on a negative DEPTH, feedback after 100 Ω) | channel cards and AUX returns with DUCK on, 30.1 kΩ into a virtual earth | 0 V = no ducking; −1 V = 10 dB, 0 to −4 V; BAT54 clamp keeps it below about +0.3 V (decisions 97, 104) |
| PFL_ACT | any channel PFL, the master's SC listen (open collector, active low) | master headphone switch, PFL LED | pulled up to +5 V on the master (bus sheet); drivers pull to PGND (decision 98) |
| SPARE2 to SPARE5 | nobody | nobody | passed through; reserved (backlog: CV, mute groups) |

## Invariants

1. **Channel independence:** no channel card depends on another; slots are identical; any number of cards from 1 to 16 works (decisions 30, 46).
2. **One star point:** AGND and PGND join only on the master card; jack sleeves to their card's AGND; frame bonded at the star point only, through the ground-lift switch (decisions 42, 61, 87).
3. **Local regulation:** every card regulates its own rails from the raw chain voltage; no regulated rail crosses a ribbon (decision 40).
4. **Ground currents:** LEDs, logic (including the PFL_ACT drivers and button pull-downs) and regulator input capacitors return to PGND; audio returns to AGND (`CHAIN.md`, decision 98).
5. **Contracts change only by a confirmed decision:** `CHAIN.md`, `INPUT-MODULE.md` and the budgets above.
6. **Part facts are verified:** every pinout and limit comes from the maker's datasheet, recorded in `docs/parts.csv`.
7. **Every sheet is double-entry:** a drawing script and an independent reference netlist, checked pin by pin, with ERC 0/0.
8. **Floating supply:** whatever feeds the power ribbons has a DC output floating from mains earth (Class II brick on the prototype); PGND is earthed nowhere except through the master card's star point and the ground-lift switch, and the star point is the only ground reference (decision 101).

## Open system items

(none; the floating-brick rule is settled by decision 101)

Earlier items are closed: the system validation `docs/reviews/2026-10-06-system.md` findings 1, 2 and 4-7 are settled by decisions 96-99 and wording fixes, finding 3 (R421 footprint) by the master card fix in bad26be.
