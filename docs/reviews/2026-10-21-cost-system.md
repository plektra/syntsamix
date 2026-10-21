# Cost review: system, 2026-10-21

Scope: the whole system. Focus from the user: "what are the SMD components I'm supposed to solder?" Read-only review by the cost controller (decision 136). Nothing below is decided; every lever is a proposal. Prices are before VAT and shipping. Rates from `docs/costs/overheads.csv` (USD 0.92, GBP 1.17). "Fee" means the JLCPCB extended-part fee, $3.07 = EUR 2.82 per type and design. Run on main at 7f6185e.

## Answer to the focus: SMD parts the user hand-solders

Source: the symbol field Assembly = "hand ..." in the schematics (decisions 150 and 155), which `tools/costs.py` counts as user-soldered. Counts are for the 4-channel prototype with one populated master. JLCPCB places everything else that is SMD. All through-hole parts (pots, jacks, headers, trimmers, buttons, TO-220s, the C103 radial) are hand-soldered too under decision 133, but they are not SMD and not listed.

| Board | Ref | Part (ProjectPN) | Package | Qty | Why JLCPCB does not place it |
|---|---|---|---|---|---|
| channel-card (per card) | U101, U102 | SSI2144 ladder filter (SX-IC-001) | QSOP-16, 0.635 mm pitch | 2 | Not stocked at LCSC (Thonk, Electrokit): would be consigned (decision 155) |
| channel-card (per card) | U201 | SSI2162 dual VCA (SX-IC-002) | SSOP-10, 1.00 mm pitch | 1 | Same (decision 155) |
| master | U203, U303, U401, U701 | SSI2162 (SX-IC-002) | SSOP-10 | 4 | Not at LCSC (decision 150) |
| master | U209, U309, U413, U506, U507, U508, U641, U751 | DG413DY (SX-IC-005) | SOIC-16 | 8 | At LCSC but extended (fee per type and design); user cost choice (150, 177) |
| master | U703, U704 | DRV135UA (SX-IC-025) | SOIC-8 | 2 | At LCSC (C544663), extended; user cost choice (150) |
| master | U402 | AS3046D matched NPN array (SX-IC-013) | SOIC-14 | 1 | Not at LCSC (decisions 82, 150) |

Totals: 4 channels = 4 x 3 = 12 chips on the cards (8 SSI2144, 4 SSI2162) plus 15 on the master = 27 chips, about 366 pins (SSI2144 128, SSI2162 80, DG413 128, DRV135 16, AS3046D 14). A 2-channel build is 21 chips. A 16-channel console would be 48 + 15 = 63 chips, about 870 pins.

Other SMD footprints the user may solder (not in the base build):
- Power board snubbers R208, C215 (D201) and R308, C315 (D301): 0805, DNP, fitted only if the bench shows switch-node ringing (decision 189).
- DNP options R206 (channel), R221, R321, R405, R439, R705 (master): 0805, only for bench experiments.
- The channel-card DG413 (2 per card) and everything else SMD are JLCPCB-placed.

Cost impact (4 channels):
- Parts the user buys separately (prices.csv): SSI2144 8 x 4.39 = 35.1; SSI2162 8 x 3.85 = 30.8; DG413 8 x 1.34 = 10.7; DRV135UA 2 x 3.31 = 6.6; AS3046D 2.5 (estimate). About EUR 86. Sources: Thonk (GBP), LCSC (DG413, DRV135), Electric Druid (AS3046D); shipping per order is not in the estimate.
- Avoided by hand-soldering: consignment handling EUR 30 per order (overheads.csv estimate; the estimate has no consign line now), two master fees (DG413, DRV135) 2 x 2.82 = 5.6, and the chips JLCPCB would otherwise place on the second assembled master (two-board minimum; about EUR 35 of ICs). Total about EUR 70. The DG413 fee on the channel card remains either way.
- Price paid: 27 chips and about 366 fine-pitch joints by hand; one bad joint on the master can silence the mixer (ROADMAP backlog). Decision 135: prototype-only cost choice; for a product the roadmap already says to return them to JLCPCB placement.

## Figures

`python3 tools/costs.py estimate` (EUR):

| Item | 4 ch | 8 ch | 16 ch |
|---|---|---|---|
| channel-card parts | 168 | 332 | 656 |
| input-module-6p3 parts | 11 | 22 | 44 |
| master parts (1 used, 2 assembled) | 115 | 114 | 114 |
| power parts (1 used, 2 assembled) | 29 | 29 | 29 |
| JLCPCB fees (28 extended types, 3 designs) | 144 | 150 | 162 |
| PCBs | 105 | 118 | 146 |
| FR4 panels | 55 | 64 | 88 |
| Frame, hardware, 24 V brick | 105 | 125 | 194 |
| Chain cables | 38 | 38 | 93 |
| Knobs and fader caps | 22 | 36 | 64 |
| **Total** | **793** | **1,028** | **1,590** |

2 channels: EUR 683. Realized (ledger): EUR 91.05, 2 entries.

Top drivers: channel card EUR 42.10 per board (SSI2144 x2 8.77, SSI2162 3.85, DG413 x2 2.67, Alpha pots 2.22 each, fader 1.77); master EUR 101.54 (SSI2162 x4 15.40, DG413 x8 10.69, rear jacks 6.88, DRV135 x2 6.63, IDC sockets 5.32); power EUR 17.41 (4u7 100 V x11 2.73, brick jack 2.30, 330u x4 1.87). At 4 channels fixed costs (fees, PCBs, panels, frame fixed) are about 45 % of the total.

Change since `2026-10-13-cost-system.md` (831 / 1,110 / 1,693): now 793 / 1,028 / 1,590 (-38 / -82 / -103). Channel-card parts 195 -> 168 at 4 ch (decisions 183 and 184 and other swaps), input module 27 -> 11 (decision 181), consigned-parts handling EUR 30 -> 0 (nothing is consigned now).

## Levers

### Prototype

1. **Build 2 channels, not 4: EUR 110 saved (793 -> 683).** No decision-135 item touched. The frame already says "maybe 2". Removes 6 of 27 hand-soldered chips. Effort: ordering choice. Evidence: `costs.py estimate --channels 2`.
2. **Relax the 0.1 % 10k receiver resistors (SX-R-107) to basic 1 %: about EUR 5.6 of fees plus part price.** Side of 135: CMRR beyond stage needs (may be relaxed). My calculation: worst-case difference-amp CMRR about 48 dB at 0.1 % and about 28 dB at 1 %. Affects channel-card and master (decisions 143, 148). Part swap. UNVERIFIED which references need the match; LCSC search 2026-10-21 found no basic or preferred 0.1 % 10k 0805.
3. The other extended types (LM339, LM13700, OPA2171, TL062, TPA6120A2, C0G 220p/6n8/560p/56p/47n, 4u7 100 V, 240k) have no fee-free equivalent: LCSC `no_fee` search 2026-10-21 for 240k 0805, 220p C0G 0805, 0.1 % 10k and LM339 SOIC-14 returned nothing.

### Console and product (16 channels)

1. **Ladder and VCA chips at volume: about EUR 80 per console at 100+ pieces of each.** SSI2144 (32 per console) and SSI2162 (20) are the biggest per-channel cost. Thonk tier modelled: 10 % at 25+; the 50 % tier at 100+ (prices.csv, 2026-10-10) would save 32 x 4.39 x 0.40 + 16 x 3.85 x 0.40 = about EUR 81 (channel cards only). A direct order from Sound Semiconductor is UNVERIFIED. No decision-135 effect. Needs a volume decision.
2. **Return the 63 hand-soldered chips to JLCPCB placement (labour): about 870 joints less per console.** DG413 and DRV135 are at LCSC (extended); SSI chips and AS3046D need consignment (EUR 30 per order, estimate). Costs about EUR 35 to 70 per order in fees; removes the single point of failure. Reliability side of 135: improves it.
3. **Alpha dual pots: EUR 2.25 per channel, EUR 36 per console.** AUX1, AUX2 and TRIM are priced at the Thonk estimate (GBP 1.90 = EUR 2.22) while other Alpha RD902F duals are priced at Tayda (USD 1.60 = EUR 1.47). Both are estimates dated 2026-10-09. UNVERIFIED that the part numbers match. Source change only.
4. **Fixed V/oct scale (open lever 13 in the channel CHECKLISTS):** one trimmer and one calibration step less per card after breadboard test 12. Already listed; not re-priced. Calibration side of 135 (may be relaxed).

## Rule findings

- E24 (decision 134): no exceptions on the channel card. Master and power were not re-audited line by line here.
- JLCPCB class (decision 137): `costs.py extended` lists 28 extended types (about EUR 79 per order). Nothing is consigned. SX-R-089 and SX-R-021 (TFPT, Mouser-only, consign) are priced in prices.csv but on no schematic.
- `docs/costs/overheads.csv` `consign_eur_per_order` note still names SX-C-023; the line is inert now, the note is stale.

## Questions for the user

- Keep the master's 8 hand-soldered DG413? Hand-soldering them saves only about EUR 5.6 in fees plus the second board's chips, against joint risk on parts every signal path crosses (decision 150).
- Does the JLCPCB two-board minimum really put a second set of master ICs on the second board (about EUR 35)? Confirm on the first quote.

## Prices to update

None new; no price was looked up. Thonk and Electric Druid prices (SX-IC-001, -002, -013, SX-POT-011, -013) are 11 days old and the AS3046D and pots are estimates.

## Not checked

- Datasheets (no lever proposed needs a pinout change).
- Live stock, shipping and import cost of the separate small orders for the hand-soldered chips.
- The JLCPCB quote itself (fee model per `overheads.csv`).
- A fresh LCSC search of all 28 extended types (four checked).
- Master and power E24 audit.
