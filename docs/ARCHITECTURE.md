# Architecture

The system-level view: how the boards fit together, the numbers that cross board boundaries, and the invariants no board may break. Owned by `/system` sessions; board sessions read it but do not change it. Every figure names its source; **[estimate]** marks a figure not yet backed by a budget script or a measurement.

## System diagram

```
 DC brick 24/48 V
      │
 ┌────▼──────────┐  power ribbon (8-pin)   ┌──────────────┐
 │ Power board   ├────────────────────────►│ Master card  │◄── star point: AGND-PGND join (net tie)
 │ DC-DC ±20 V   │                         │ ±15 V, +5 V  │──► main out (THAT1646), headphones,
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

| Item | Value | Source |
|---|---|---|
| Raw rails | ±20 V nominal, unregulated in general, from an isolated DC-DC on the prototype | decisions 40, 60, 81 |
| Raw rail minimum under load | about 19 V: the master's relay drop-out comparator trips at 17.9 V; the LM317 needs about 2 V headroom above 15.1 V | decisions 92, 95 |
| Local rails on every card | ±15.1 V (LM317/LM337), +5 V (78L05 on channel cards, L7805 on the master) | decisions 78, 87 |
| Channel card load | about 130 mA per rail **[estimate]** (no budget script yet) | decision 78 |
| Master card load | typical +15 V 345 mA, −15 V 275 mA; worst case 730 / 606 mA | decision 95, `hardware/master/scripts/power_budget.py` |
| Total, 16 cards + master | about 2.4 A (typical) to 2.8 A (worst case) per rail, about 100 to 115 W | decision 95 |
| Prototype, 4 cards + master | about 0.9 to 1.3 A per rail **[estimate]** | 4 × 130 mA + master |
| Power ribbon | injected in groups of 8 cards; at most about 0.53 A per pin | decision 80 |

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
| SC_ENV | master card, low impedance | channel cards with DUCK on, high impedance | 0 V = no ducking; **[proposed]** +1 V = 10 dB, about 0 to +4 V (decision 72) |
| PFL_ACT | any channel PFL, the master's SC listen (open collector, active low) | master headphone switch, PFL LED | pulled up to +5 V on the master (bus sheet) |
| SPARE2 to SPARE5 | nobody | nobody | passed through; reserved (backlog: CV, mute groups) |

## Invariants

1. **Channel independence:** no channel card depends on another; slots are identical; any number of cards from 1 to 16 works (decisions 30, 46).
2. **One star point:** AGND and PGND join only on the master card; jack sleeves to their card's AGND; frame bonded at the star point only, through the ground-lift switch (decisions 42, 61, 87).
3. **Local regulation:** every card regulates its own rails from the raw chain voltage; no regulated rail crosses a ribbon (decision 40).
4. **Ground currents:** LEDs, logic and regulator input capacitors return to PGND; audio returns to AGND (`CHAIN.md`).
5. **Contracts change only by a confirmed decision:** `CHAIN.md`, `INPUT-MODULE.md` and the budgets above.
6. **Part facts are verified:** every pinout and limit comes from the maker's datasheet, recorded in `docs/parts.csv`.
7. **Every sheet is double-entry:** a drawing script and an independent reference netlist, checked pin by pin, with ERC 0/0.

## Open system items

- Channel card power budget script (replace the 130 mA estimate), then recheck the total and the DC-DC rating.
- Supply rating for 16 cards (`docs/decisions/power.md`).
- SC_ENV scale (decision 72, proposed).
