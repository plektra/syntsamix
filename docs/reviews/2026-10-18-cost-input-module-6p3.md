# Cost review: input-module-6p3, 2026-10-18

Scope: input-module-6p3, focus on ROADMAP "Cost-cut candidates" item 8 (the user's question of 2026-10-17): a self-made IDC ribbon on a 2x6 or 2x7 header against the ready-made Molex 217796-1101 of decision 179. Nothing in the design files was changed.

## Figures

`python3 tools/costs.py estimate` (EUR, before VAT and shipping):

| Item | 4 ch | 8 ch | 16 ch |
|---|---|---|---|
| channel-card parts | 194 | 382 | 758 |
| input-module-6p3 parts | 27 | 55 | 100 |
| master parts | 115 | 114 | 114 |
| power parts | 28 | 28 | 28 |
| JLCPCB fees | 138 | 144 | 156 |
| PCBs | 105 | 118 | 146 |
| FR4 panels | 55 | 64 | 88 |
| Frame, hardware, 24 V brick | 105 | 125 | 194 |
| Chain cables | 38 | 38 | 93 |
| Knobs and fader caps | 22 | 36 | 64 |
| **Total** | **827** | **1,105** | **1,740** |

Change since 2026-10-13 (831 / 1,110 / 1,693): the 4 and 8 channel totals are within EUR 5 (master -6, JLCPCB fees -6, power +2, chain cables now a separate line of 38 / 38 / 93, consigned handling gone). The 16-channel total rose EUR 47, almost all from the 16-card chain cables (EUR 93) of decision 175. The input module itself did not change: EUR 6.83 per board.

Input module drivers (`costs.py drivers --board input-module-6p3`, EUR 6.83 per board): Molex input cable 5.18 (76 %), two NYS216 jacks 1.26, KK header 0.40. The board has no SMD parts, no resistors or capacitors, so no JLCPCB fee, no E24 issue and no extended-part issue. The channel card's matching KK header (SX-CONN-002, 0.40 in the tool) sits on the channel-card line.

Realized ledger total (private): EUR 53.80, 1 entry; not relevant to this scope.

## Levers

### Console and product (per channel; counts sixteen times)

**L1. IDC ribbon on a 2x6 header instead of the Molex lead and KK headers.** Largest and only real lever on this board.

Prices (Mouser, 2026-10-18, EUR):

| Item | At 10 | At 100 |
|---|---|---|
| Adam Tech BHR-12-VUA 2x6 shrouded header (737-BHR-12-VUA), x2 | 0.445 each | 0.354 each |
| Adam Tech FCS-12-SG 12-way IDC socket (737-FCS-12-SG), x2 | 0.323 each | 0.266 each |
| 3M 3365/14 ribbon, 0.5 ft (150 mm) (517-3365/14FT; a 12-way is not listed, a 14-way cut is the nearest priced) | 0.11 | 0.11 |
| IDC route per channel | 1.65 | 1.35 |

Today per channel in the tool: Molex lead 5.18 + two KK headers 0.80 = 5.98. At real Mouser prices: Molex 4.28 at 10 (4.00 at 25) + two Molex 22-27-2101 headers 0.60 each at 10 = 5.48. Hand-crimped KK fallback: about 1.60 housings and crimps + 1.20 headers = 2.80.

Saving: about EUR 4.3 per channel against the tool figure (about EUR 17 on the 4-channel prototype, about EUR 69 on a 16-channel console); about EUR 3.8 per channel (EUR 15 / EUR 61) against real Molex prices; about EUR 1.1 to 1.4 per channel against hand crimping. Same size as lever C3 of the 2026-10-13 report.

Work: two presses per cable (the same vise or IDC press that decision 175 already needs for the chain cables, 21 sockets on the prototype), against none for the Molex lead and about 20 crimps for the fallback. The tool and skill are already required, so the extra manual work is small.

Pin map proposal for a 2x6 header (12 wires, ribbon order): L+, G, L-, G, R+, G, R-, G, DO_L, G, DO_R, G. Each signal has a ground wire beside it, and the hot/cold pairs are kept apart by one ground. A 2x5 would be enough electrically for the prototype (4 signals) but is the Eurorack power size that decision 41 keeps off the unit, so 2x6 is the smallest allowed size; 2x7 buys nothing. The final map is a /system choice.

Decision 135 side: neutral (no audio accuracy involved; ribbon with ground wires is at least as good against crosstalk as discrete wires, UNVERIFIED by measurement). Reliability: IDC sockets are normal practice and the shroud is polarised; a KK friction lock has similar retention. A latch-less 2.54 box header can be pulled out by vibration; Adam Tech makes latch versions (BHR-xx-VUA-SL, ML) at higher price, not needed for a cable that is strain-relieved by the frame, but a point for a product (UNVERIFIED).

Decisions and boards affected: 68 and 105 (header size and pinout), 99 and 179 (cable), `docs/INPUT-MODULE.md`, both boards' footprints (channel card `input.kicad_sch`, SX-CONN-002 used there; input module). Pins 8 and 9 stay reserved. Header becomes SX-CONN-new (2x6 shrouded) and socket SX-CONN-new (2x6 IDC); the chain-connector separation rule in INPUT-MODULE.md must be restated: a 2x6 shroud cannot take the 2x13, 2x17 sockets and 2x4 power sockets do not fit the 2x4 power header from a 2x6 ribbon, but a 2x4 power socket could be forced into a 2x6 shroud (the key notch is centred on the 2x6 body, the 2x4 socket's key is not, so it should not seat; check on a sample, UNVERIFIED). Both are a power-versus-audio risk only if the unit has a mis-plugged power ribbon.

Effort: connector and footprint change on two boards, before channel layout places the input header (a /system decision). Both schematics need ERC again. No layout yet, so no rework.

**L2. Take both headers from the same cheap Adam Tech family as the chain headers.** Combined with L1 it needs no extra work: BHR-xx-VUA is the candidate already named for the chain headers in prices.csv, so one more size does not add a manufacturer. Included in the figures above.

### Prototype (fixed costs dominate)

There is no further lever on this board. The module has no SMD parts and is ordered as a bare PCB; the real PCB cost is the EUR 15 minimum per design (`pcb_min_eur_per_design`), which the 2026-10-13 report already questions (JLCPCB quotes small 2-layer boards well below that; not re-checked here). The prototype saving from L1 is about EUR 17 of EUR 827 (2 %).

Ideas looked at and dropped:
- Cheaper jacks than the Rean NYS216 (EUR 0.63 each at 50+): decision 132 already took this lever; the jack is rated 1,000 cycles, so a cheaper jack would touch reliability ("must stay").
- Soldering the cable to the board: no. Modules must stay cabled for the 3.5 mm and D-SUB variants (INPUT-MODULE.md).
- Dropping the module header pins 8 and 9 reservation: saves nothing in a 2x6 header; the pins are free.
- Merging two channel modules onto one PCB (two channels' jacks): saves PCB minimum (EUR 15 / 2 per module) but contradicts the one-module-per-channel and on-edge mounting layout of decision 160; not proposed. Question below.

## Rule findings

- E24 (decision 134): no resistors or capacitors on this board; nothing to flag.
- JLCPCB class (decision 137): no SMD parts on this board; nothing to flag. `costs.py extended` lists 26 types for other boards (about EUR 73 in fees), outside this scope.
- Expensive reseller: Molex 217796-1101 (Mouser only, EUR 4.28 at 10) is the one part here; L1 removes it.
- `docs/parts.csv` carries the Molex header SX-CONN-002 price as a 0.40 estimate; Mouser shows 0.60 at 10, 0.51 at 100 (see Prices).

## Questions for the user

1. L1 reverses the agreement of 2026-10-13 (ready-made cable to avoid hand crimping, decision 179). It is not hand crimping in the KK sense: two presses per cable with the tool already needed for the chain cables. Do you accept two presses per cable for about EUR 17 (4 ch) to EUR 69 (16 ch)? It is a /system decision (the header contract changes).
2. Should the 2x6 IDC header on the channel card carry a latch or ejector version for product use? Not needed for the prototype; costs about EUR 1 more per header.
3. Should the PCB for the input module be one panel-sharing board for two channels? It would save the PCB minimum only; recorded as a question because decision 160 fixes one module per channel.

## Prices to update (`docs/costs/prices.csv`)

| ProjectPN | Price | Currency | Source | Date |
|---|---|---|---|---|
| SX-CONN-002 | 0.60 (10+; 0.514 at 100) | EUR | Mouser 538-22-27-2101 | 2026-10-18 |
| SX-CONN-022 | 4.28 (25+: 4.00) | EUR | Mouser 538-217796-1101 (file shows USD 5.63) | 2026-10-18 |
| new, 2x6 shrouded header | 0.445 (10+; 0.354 at 100) | EUR | Mouser 737-BHR-12-VUA | 2026-10-18 |
| new, 2x6 IDC socket | 0.323 (10+; 0.266 at 100) | EUR | Mouser 737-FCS-12-SG | 2026-10-18 |
| new, 3M 3365/14 cut length (ribbon, 150 mm = 0.5 ft) | 0.249 per ft at 10 | EUR | Mouser 517-3365/14FT | 2026-10-18 |

## Not checked

- Datasheet pinouts and shroud dimensions of the Adam Tech BHR-12-VUA and FCS-12-SG (key notch, whether a 2x4 power socket seats in the 2x6 shroud): not read. UNVERIFIED.
- A 12-conductor 3M ribbon is not in the Mouser listing; the 14-way cut length is priced as a stand-in (a 12-way is within a few cents). A plain 28 AWG 12-way from another maker would also do; RoHS statements for the Adam Tech and 3M parts are not recorded in parts.csv yet (invariant 9).
- Crosstalk or noise difference between the ribbon and discrete wires, not measured.
- JLCPCB PCB prices for the module (instant quote), shipping and VAT.
