# Architecture

The system-level view: how the boards fit together, the numbers that cross board boundaries, and the invariants no board may break. Owned by `/system` sessions; board sessions read it but do not change it. Every figure names its source; **[estimate]** marks a figure not yet backed by a budget script or a measurement.

## System diagram

```
 DC brick 24 V (Class II, floating output)
      │
 ┌────▼──────────┐  power ribbon (8-pin)   ┌──────────────┐
 │ Power board   ├────────────────────────►│ Master card  │◄── star point: AGND-PGND join (net tie)
 │ buck/inverter │                         │ ±15 V, +5 V  │──► main out (DRV135), headphones,
 └──┬─────────┬──┘                         │ bus summing, │    AUX sends/returns, SC EXT jack
    │ chain 1 │ chain 2                    │ compressor   │
    │ power   │ power                      └──────▲───────┘
    ▼         ▼                                   │ audio cable (34-way), multi-drop past all cards
 cards 1-8   cards 9-16                    ┌──────┴───────┐   ┌──────────────┐
 (each card regulates ±15 V, +5 V)         │ Channel card ├───┤ Channel card ├── ... up to 16
                                           └──────▲───────┘   └──────────────┘
                                                  │ 12-pin header
                                           ┌──────┴───────┐
                                           │ Input module │ (passive, jacks)
                                           └──────────────┘
```

The diagram is not to scale: left to right the unit holds the channel strips, the master section (4 strips) and the power bay (1 strip) (decisions 109, 162, `MECHANICAL.md`); chain 1 feeds the group next to the master. Each channel card has one audio and one power header on multi-drop flat cables in 8-card sections; audio sections join through a coupler board, each group of 8 has its own power section (decisions 38, 80, 175). The prototype has 4 channel cards on chain 1.

## Interfaces (contracts)

| Interface | Document | Between |
|---|---|---|
| Audio ribbon, 34-pin | `docs/CHAIN.md` | master card, every channel card |
| Power ribbon, 8-pin | `docs/CHAIN.md` | power board, master card, channel cards |
| Input header, 12-pin (2x6 IDC, decision 181) | `docs/INPUT-MODULE.md` | channel card, input module |
| Strip envelope, panels, frame | `docs/MECHANICAL.md` | every board, panels, frame |

## Cross-board budgets

### Power

Sizing rule (decision 96): a card's own parts are sized for its worst case (every IC at datasheet maximum, every LED lit, full signal load); parts shared by many cards (the power board converters, ribbon pins) for IC quiescent current at typical × 1.5 plus the use-dependent loads at their maximum. All figures at 20 V raw from `tools/system_power_budget.py`, which runs both cards' `power_budget.py` (rerun 2026-10-17 after decision 173). The 1.5 factor is a judgment until the prototype cards are measured.

| Item | Value | Source |
|---|---|---|
| Raw rails | ±20 V nominal, unregulated in general; on the prototype from non-isolated converters on the power board (TPS54560 buck and inverter), the 24 V brick providing the isolation | decisions 40, 60, 81, 100 |
| Raw rail minimum under load | about 19 V: the master's relay drop-out comparator trips at 17.9 V; the LM317 needs about 2 V headroom above 15.1 V | decisions 92, 95 |
| Local rails on every card | ±15.1 V (LM317/LM337), +5 V (78L05 on channel cards, L7805 on the master) | decisions 78, 87 |
| Channel card load (+15 / −15 V) | typical 110 / 93 mA; worst case 229 / 194 mA; sizing 171 / 139 mA (TL072 receiver) | decisions 96, 102, 123, 143, `hardware/channel-card/scripts/power_budget.py` |
| Master card load (+15 / −15 V) | typical 295 / 224 mA; worst case 591 / 466 mA; sizing 522 / 408 mA | decisions 95, 96, 103, 125-128, 146, 148, 173, `hardware/master/scripts/power_budget.py` |
| Prototype, 4 cards + master | sizing 1.21 / 0.96 A, about 43 W (typical 0.73 / 0.60 A, 27 W; worst case 1.51 / 1.24 A, 55 W); power board converters about 2 A per rail | decisions 96, 100, 123, 143, 146, 148, 173 |
| Full size, 16 cards + master | sizing 3.26 / 2.63 A, about 118 W (typical 2.06 / 1.71 A, 75 W; worst case 4.25 / 3.57 A, 156 W, not used for sizing) | decisions 96, 123, 143, 146, 148, 173 |
| Brick (24 V, Class II, floating, R7B plug) | prototype Mean Well GSM120B24-R7B (120 W); full size GSM220B24-R7B (221 W): about 131 W at sizing and 173 W at worst case into the brick at about 90 % conversion **[estimate]**, 59 / 78 % of its rating | decisions 100, 145 |
| Power ribbon | one multi-drop section per group of 8 cards (decision 175); about 0.68 A per conductor from the feed (sizing; 0.92 A at worst case), about 0.11 A per contact at each card's socket; connectors and cable rated at least 1 A per contact (the Würth 61200823021 IDC socket is the limit at 1 A at the feed socket, the worst case 8 % below it; the header is 3 A; the Würth WR-CAB 8-way flat cable, `SX-WIRE-005`, is rated 1 A max at 25 °C (decision 178); its derating at the 57 °C inside air is to confirm for a full group of 8) | decisions 80, 96, 100, 123, 175, 178 |
| Capacitance on each raw rail at switch-on | about 0.37 mF (prototype), 1.2 mF (full size), plus about 0.76 mF on the power board; the start-up ramp on both converters holds the brick at about 54 W while charging it (rails at 19 V about 40 ms after switch-on; bench check in `hardware/power/STATUS.md`) | system validation, finding 6; decision 100, `hardware/power/scripts/startup_sim.py` |

### Heat

| Item | Value | Source |
|---|---|---|
| Dissipation inside, typical at 20 V | channel card 4.1 W, master 10.4 W (after decision 173), power board loss at about 88 % **[estimate]**, until the power board session reports the converters' efficiency: about 30 W (prototype), 49 W (8 cards), 86 W (16 cards) | decisions 167, 173, `tools/heat_budget.py` (rerun 2026-10-17) |
| Inside air | design point 22 K above room temperature (57 °C on a 35 °C stage), up to 8 cards; estimate 19 / 22 / 23 K for 4 / 8 / 16 cards (sealed box 23-30 K) | decision 167, `tools/heat_budget.py` (coefficients **[estimate]** until the prototype is measured) |
| Vents | perforated bottom cover; four 2 × 30 mm slots per channel rear strip (about 2.4 cm²), master and bay rear pieces; none in the cheeks or top panels | decision 167, `MECHANICAL.md`, Ventilation |
| Tightest parts | 0 to +70 °C ambient (TL072CDT, NE5532, TL062C, LM339, LM13700): about 13 K above the design air | decision 167 (datasheets in its record) |
| Master heatsinks at 57 °C air | Wakefield 637-10ABPE (12.67 °C/W): LM317 TJ about 111 °C at the worst-case 2.90 W, 84 °C typical, within the 125 °C rating (decision 174's limit; 95's 100 °C would need about 8.8 °C/W) | decisions 167, 173, 174; `tools/heat_budget.py`, `hardware/master/scripts/power_budget.py` |

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
| SC_ENV | master card, low impedance (follower on a negative DEPTH, feedback after 100 Ω) | channel cards and AUX returns with DUCK on, 30 kΩ into a virtual earth (decision 153) | 0 V = no ducking; −1 V = 10 dB, 0 to −4 V; BAT54 clamp keeps it below about +0.3 V (decisions 97, 104) |
| PFL_ACT | any channel PFL, the master's SC listen (open collector, active low) | master headphone switch, PFL LED | pulled up to +5 V on the master (bus sheet); drivers pull to PGND (decision 98) |
| SPARE2 to SPARE5 | nobody | nobody | carried by the multi-drop cable, unconnected on the cards (decision 175); reserved (backlog: CV, mute groups) |

## Invariants

1. **Channel independence:** no channel card depends on another; slots are identical; any number of cards from 1 to 16 works (decisions 30, 46).
2. **One star point:** AGND and PGND join only on the master card; jack sleeves to their card's AGND (the master's rear jacks through the row-board ribbon grounds, decision 163; a CV patch cable between channel cards joins AGND to AGND, decision 166); frame bonded at the star point only, through the ground-lift switch on the master's input row board (J903 pins 25/26) (decisions 42, 61, 87, 163).
3. **Local regulation:** every card regulates its own rails from the raw chain voltage; no regulated rail crosses a ribbon (decision 40).
4. **Ground currents:** LEDs, logic (including the PFL_ACT drivers and button pull-downs) and regulator input capacitors return to PGND; audio returns to AGND (`CHAIN.md`, decision 98).
5. **Contracts change only by a confirmed decision:** `CHAIN.md`, `INPUT-MODULE.md`, `MECHANICAL.md` and the budgets above.
6. **Part facts are verified:** every pinout and limit comes from the maker's datasheet, recorded in `docs/parts.csv`.
7. **Every sheet is double-entry:** a drawing script and an independent reference netlist, checked pin by pin, with ERC 0/0.
8. **Floating supply:** whatever feeds the power ribbons has a DC output floating from mains earth (Class II brick on the prototype); PGND is earthed nowhere except through the master card's star point and the ground-lift switch, and the star point is the only ground reference (decision 101).
9. **RoHS:** every component and every board complies with RoHS 2011/65/EU as amended by (EU) 2015/863; boards are fabricated and assembled lead-free (lead-free HASL or ENIG, lead-free assembly and hand soldering). Parts with a maker part number carry a `RoHS: <source>` in `docs/parts.csv` when chosen; standard passives get theirs when the BOM is fixed (decisions 116, 122).

## Open system items

- Mechanical (`/system mechanical`): the chain header positions and the power LED position from the board layouts; then the full-size cooling after the prototype measurement (`MECHANICAL.md`, Open; settled so far by decisions 106 to 109, 118 to 121, 160, 162, 166, 167, 175 and 176: rear strips, input module on edge, sloped frame with a single front rail, master section, power bay, CV jack pair, ventilation, multi-drop chain cables).
- Chain cable (decisions 175, 178): Würth WR-CAB's 1 A is stated at 25 °C: confirm the derating (Würth statement or a measurement) before a full group of 8 shares a power section; mid-cable use of the Würth sockets checked on the first delivery (`CHAIN.md`, Points still open).
- RoHS gaps before the first PCB order (decision 122; audit done 2026-10-09, `docs/reviews/2026-10-09-rohs-audit.md`): the declaration for the AS3046D (master) (the Alpha pots are cleared by Taiwan Alpha's general declaration, decision 124; the SSI2144 and SSI2162 by an SGS package report via Electrokit, decision 164); rows with no part chosen yet get their source when chosen. The end-of-life parts are gone (THAT1646: DRV135UA, decision 125; ERA-V33J102V: plain resistors, decisions 141 and 149).
- Heat (decision 167): measure the prototype (one hour, every LED lit) to replace the convection estimates; the full-size cooling follows.

Earlier items are closed: the system validation `docs/reviews/2026-10-06-system.md` findings 1, 2 and 4-7 are settled by decisions 96-99 and wording fixes, finding 3 (R421 footprint) by the master card fix in bad26be.
