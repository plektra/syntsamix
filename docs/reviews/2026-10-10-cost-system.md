# Cost review: system, 2026-10-10

Scope: the whole system (channel card, master, power, 6.3 mm input module), with no focus given. Read-only review by the cost controller (decision 136). Nothing below is decided; every lever is a proposal for a `/board` or `/system` session. Prices are before VAT and shipping. Exchange rates come from `docs/costs/overheads.csv` (USD 0.92, GBP 1.17). "Fee" means the JLCPCB extended-part fee: $3 per type, which is EUR 2.76.

## Figures

`python3 tools/costs.py estimate --channels N --md`, run on main at 72e5732 (all worktree branches are merged):

| Item | 2 ch | 4 ch | 16 ch |
|---|---|---|---|
| channel-card parts | 131 | 262 | 1,046 |
| input-module-6p3 parts | 3 | 7 | 26 |
| master parts (1 used, 2 assembled) | 184 | 184 | 184 |
| power parts (1 used, 2 assembled) | 30 | 30 | 30 |
| JLCPCB fees (80 extended or consigned types, 3 designs) | 335 | 338 | 354 |
| PCBs | 75 | 75 | 116 |
| FR4 panels | 55 | 55 | 88 |
| Frame, hardware, ribbons, 24 V brick | 100 | 110 | 170 |
| Knobs and fader caps | 15 | 22 | 64 |
| Consigned parts handling | 30 | 30 | 30 |
| **Total (EUR)** | **958** | **1,112** | **2,109** |

The 16-channel figure still uses one power board as drawn. The full-size supply (4 A design, or power lever 1) is not in it.

**Parts per board** (`costs.py drivers`):
- Channel card: EUR 65.38 (SMD 39.25, THT 26.13).
- Master: EUR 115.89 (SMD 68.43, THT 47.46).
- Power: EUR 19.36.
- Input module: EUR 1.65.

**Top cost drivers:**
- Channel card, per card: SSI2144 ×2 8.77, DG413 ×4 7.07, DG412 5.34, SSI2162 4.09, AD8273 3.78, trimmers ×3 4.14, Alpha pots ×6 about 10.9, latching buttons ×7 7.00, bipolar 10 µF ×8 2.21, TFPT ×2 1.95.
- Master: SSI2162 ×4 16.38, DG413 ×9 15.90, AD8273 ×2 7.56, DRV135UA ×2 6.29, bipolar 10 µF ×16 4.42.
- At 4 channels, the fixed costs (fees, set-up, consignment, the second master and power board) are about 45 % of the total. At 16 channels the channel cards are half.

**Change since the last cost figures:** there is no earlier `docs/reviews/*-cost-*.md`. The last figures are the ROADMAP's "Cost review 2026-10-09": 960 / 1,115 / 2,110 EUR with 82 fee types. They are now 958 / 1,112 / 2,109 EUR with 80 fee types. The difference comes from commit 72e5732: TL072CDT, 78L05G-AB3-R, BZT52C6V2 and the UNI-ROYAL 13k/680k/750R moved to fee-free parts, so two fee types fewer (about −5.5 EUR) and slightly lower part prices. Decision 138 (RV501 B100K dual from Thonk, £1.99) has no visible effect.

**Realized costs** (`costs.py ledger`): EUR 53.80 to date (parts).

### How far to trust the estimate (corrections found, not applied)

| Finding | Effect on the estimate | Status |
|---|---|---|
| JLCPCB **Economic PCBA** costs $8.18 set-up plus $1.53 stencil per design (JLCPCB price page, 2026-10-10). `overheads.csv` uses EUR 35 per design. The channel card's underside has only hand-soldered THT parts (decisions 112, 121), so every board can be single-sided Economic PCBA (2-50 pieces). | about −78 EUR (3 designs × (35 − 9)) | page checked; Economic limits taken from JLCPCB's capabilities page through a search summary |
| The tool counts each extended type **once per order**. If JLCPCB bills each design (each its own PCBA job) separately, the 21 types shared by channel and master (and one shared by channel and power) are billed twice: 45 + 41 + 15 = 101 billed types instead of 80. | about +58 EUR | UNVERIFIED: JLCPCB's page does not say. Ask JLCPCB or check the first quote. |
| Fee types the tool counts as free: 560k (master SX-R-053) and 240k (power SX-R-084) are E24 values with no fee-free part; 56p C0G 0805 (SX-C-027), 47n C0G 0805 (SX-C-016), 22n C0G 0805 (SX-C-017) and 10p C0G 100 V 0805 (SX-C-022) have no fee-free 0805 C0G part; the master's R421 ERA-V33J102V (SX-R-021) is priced as a generic 0.002 USD basic resistor, but it is end of life (decision 130) and needs the TFPT pair or consignment. | about +19 EUR in fees, plus about 1 EUR in parts | jlcsearch class data, 2026-10-10 |
| Stale prices (see "Prices to update"): DG413 is cheaper at the 30+ break; DG412 at LCSC is now 8-9 USD, not 5.80; the Bourns trimmer is 0.75 USD at LCSC (10+); SSI2162 is £3.29 at Thonk with quantity discounts. | net about −10 to −25 EUR at 4 channels | sources below |

With these corrections, the 4-channel prototype would be about 1,050-1,090 EUR, depending on how JLCPCB bills shared types.

## Levers

Each lever is marked with the side of decision 135 it touches: **[relax]** means accuracy, calibration or a studio nicety may be traded; **[neutral]** means same function, no trade-off; **[check]** means a "must stay" item is near and needs a test before the change.

### Prototype (2-4 channels: fixed costs)

1. **Start with 2 channels** (ROADMAP lever 3, still open). Saves 154 EUR (1,112 → 958). Trade-off: no test of 3- and 4-card chain effects (bus noise, chain current). [neutral] Affects no decisions; ordering only.

2. **Make every SMD resistor value fee-free: E24 values that the basic or preferred library holds, or pairs of them** (decision 134 is the rule; this lever puts a number on it and lists the traps).
   - What it removes: 43 off-E24 resistor types (channel 25, master 24 including 39R2 2512, power 4; 11 are shared) plus 3 E24 values with no fee-free part (110 R channel, 560k master, 240k power).
   - Saving: 46 types × 2.76 = about **127 EUR per order**, or about 157 EUR if JLCPCB bills shared types once per design.
   - Trade-off [relax]: the fader law (113k-30k1 set, channel Level, master AUX returns and master out), the meter ladders (±1 dB is enough) and the filter scaling (the V/oct scale is trimmed anyway) move by up to ±2-5 %, or take an E24 pair (one extra placement, no fee).
   - Power board [check]: the converter dividers (732k, 42k2, 15k8, 243k) set ±20 V and the UVLO thresholds. Rerun `scripts/design.py` with E24 values (and E24 pairs where needed); output-voltage tolerance is a reliability matter.
   - Trap: these E24 values have **no** fee-free 1 % 0805 part (jlcsearch, 2026-10-10): 11, 12, 13, 16, 18, 24, 30, 36, 39, 43, 62, 75, 82, 91 Ω; 110, 130, 160, 360, 430, 620, 910 Ω; 1k1, 1k3, 1k6; 91k, 110k, 130k, 160k, 240k, 360k, 430k, 560k, 620k, 750k, 820k, 910k; and everything above 1 MΩ. Every other E24 value from 10 Ω to 1 MΩ is basic or preferred. No 2512 or 1206 value from 10 to 51 Ω is fee-free, so the headphone 39R2 2512 gains nothing by becoming 39 R. Keep it as a recorded exception, or use parallel 0805 parts if their power rating suffices.
   - Affects decisions 79, 92, 93, 103 and 134 and the power design. Boards: all three SMD boards. Effort: value edits in the build scripts, a rerun of `simulation/level/` for the fader law and of the power design script.

3. **Leave the master's expensive ICs off the JLCPCB BOM and hand-solder them on the one master that is used.** JLCPCB assembles at least 2 boards, so today the spare master carries SSI2162 ×4, DG413 ×9, AD8273 ×2, DRV135UA ×2 and AS3046D (about 49 EUR).
   - Saving: about **49 EUR** in parts, plus the DRV135UA fee (2.76); the consigned master types stop needing consignment for the master. About 52 EUR in total.
   - Trade-off [check]: 18 SOIC or SSOP parts to hand-solder (SSOP-10 has a 1.0 mm pitch). Reliability is a must-stay item, so inspect them. The spare master then needs the same ICs before it can serve as a repair spare. Keep the TPA6120A2 (exposed pad) on JLCPCB.
   - Affects decision 133 (JLCPCB places SMD only). Board: master. Effort: ordering only (BOM split).

4. **Hand-solder the consigned parts instead of consigning them**: SSI2144 (QSOP-16, 0.635 mm), SSI2162 (SSOP-10), AD8273 (SOIC-14), AS3046D (SOIC-14) and the TFPT (0603).
   - Saving: the 30 EUR handling (shipping parts to JLCPCB) plus 5 consigned fee types (13.80), so about **44 EUR per order**. It overlaps with lever 3 on the master parts.
   - Trade-off [check]: fine-pitch hand soldering on every channel card (8 SSI2144 at 4 channels). A bad joint on the filter is a mid-gig failure risk, so inspect under magnification. Not for a product, where consignment cost spreads over volume.
   - Affects decision 133. Boards: channel card and master. Effort: ordering only.

5. **DG412 → DG413 on the channel card, with the latching button's free throw giving the inverted logic.**
   - Background: U303 (DG412, four NO switches) uses three sections: PFL L, PFL R and SC send. In a DG413, sections 1 and 4 are NO and 2 and 3 are NC (as the card already uses them in U302 and U206). PFL L/R go on sections 1 and 4, and SC on section 2 driven from SW302 pin 1. The GPBS850N connects pin 1 to pin 2 (+5 V) when released (pressed = 2-3, parts.csv and decision 75), so pin 1 is high when SC is off. Add one 0805 pull-down (fee-free).
   - Master: U641 DG411 (four NC) → DG413 by inverting DET1 at its comparator (input swap). No LCSC listing for the DG411 was found, so this also removes a possible consigned part (UNVERIFIED).
   - Saving: 3.57 EUR per card with the tool's prices (6.07 with today's LCSC prices: DG412 8.24 USD at 10+, DG413 1.64), plus 1-2 fee types (2.76-5.52). That is about 17-30 EUR at 4 channels.
   - Trade-off: none [neutral]. Break-before-make on the button is harmless: SC turns on only once pin 1 opens.
   - Affects decision 74 and the master's AUX-send mono switching (decision in master-card-sheets). Boards: channel card, master. Effort: schematic (two nets and a resistor), no layout yet.

6. **Bipolar 10 µF electrolytics → 10 µF X5R ceramic 0805 25 V** (Samsung CL21A106KAYNNNE, LCSC C15850, JLCPCB basic, $0.077) or 1206 50 V (CL31A106KBHNNNE, C13585, basic, $0.176).
   - Scope: 8 per card and 16 on the master. The EEE-1VA100NP is not stocked at LCSC at all, so today it is global sourcing or hand-soldering.
   - Saving: about 1.6 EUR per card and 3.3 per master, plus one fee type. About 16 EUR at 4 channels (2 masters assembled).
   - Trade-off [relax + check]: a class-2 ceramic in the audio path. The coupling caps carry no DC bias, and at audio frequencies little signal voltage sits across them, so distortion should stay below audibility (may be relaxed). Class-2 MLCCs are piezoelectric, though, and stage vibration could add microphonic noise (must stay: noise for a loud PA). Do a tap test on the breadboard before adopting it.
   - Decision 111 rejected radial bipolars and series electrolytics, not ceramics. Affects decisions 72 and 111 and the master's 127. Boards: channel card, master. Effort: part swap (smaller footprint, before layout).

7. **Buy the 3296W trimmers at LCSC.** Genuine Bourns 3296W-1-503LF costs 0.75 USD at 10+ (C83686) against EUR 1.38 at Mouser; BOCHEN 3296W-1-503 costs 0.14 USD at 50+ (C118911). Saving: 8 EUR (Bourns) to 15 EUR (BOCHEN) at 4 channels.
   - Trade-off [relax]: BOCHEN has a ±250 ppm/K track, which hardly matters in a ratiometric trim, and 30 turns.
   - Check the BOCHEN mechanical life and sealing against the Bourns before choosing it (reliability). Its RoHS source is LCSC's listing ("ROHS Compliant"); decision 116 accepts a supplier statement, but record it. Affects decision 112 only if the BOCHEN body differs (UNVERIFIED drawing). Effort: purchase only.

8. **Not proposed: one panel for all designs** (one PCBA job: one set-up, shared fee types once). Economic PCBA panels are limited to 250 × 250 mm, and the 318 mm channel card does not fit. Master plus power as one panel could still save one set-up (about 9 EUR) once the master size is known; too small to pursue now.

### Console and product (16 channels, volume: per-channel parts ×16, labour)

1. **Remove the DG412 per card** (prototype lever 5). Saving: 3.57-6.07 EUR per card, **57-97 EUR per console**.
   - Going further, removing U303 entirely would need MUTE without a switch section. A logic-level feed into the summer has the wrong polarity, and a 5 V/15 V offset-cancel scheme gives a few dB of unmuted gain error. So only the DG412 → DG413 swap is proposed. A discrete mute switch (NPN with a zener level shift) is possible but UNVERIFIED.

2. **AD8273 → op-amp differential receivers** (ROADMAP lever 4, still open). About 3.6 EUR per card and 7.4 on the master, so about **65 EUR per console**. It also removes a consigned part (product: no Mouser dependency).
   - Trade-off [relax]: CMRR about 50-60 dB instead of 77 dB minimum. Re-check the input stage's ±12 V headroom (must stay). Affects decisions 25, 115 and the master AUX returns.

3. **Trimmers: cheaper part, and fewer of them** (ROADMAP lever 6, with new prices). LCSC Bourns or BOCHEN saves 2.1-3.75 EUR per card, **33-60 EUR per console**.
   - Product labour: each of the 3 trimmers per card (CUTOFF OFFSET ×2, V/OCT) is a calibration step. If the breadboard shows that the TFPT tempco and an E24 pair hold the V/oct scale within a few %, V/OCT (RV182) could become fixed: one part (1.38 EUR) and one calibration step fewer per card. [relax] filter tracking accuracy. Affects decisions 16, 112 and 130.

4. **Buy the Alpha pots from Tayda instead of Thonk.** AUX1, AUX2 and TRIM duals at Thonk £1.90 (EUR 2.22) against Tayda about 1.60 USD (EUR 1.47); CUTOFF £1.30 against about 1.00 USD. About 2.85 EUR per card, **about 46 EUR per console**.
   - Decision 124 makes genuine Alpha RoHS-clear through any reseller. [neutral] Check that Tayda carries the exact order codes (RD902F-40-15K-A10K, A100K, RD901F-40-15K-B50K): Tayda prices are estimates in `prices.csv`, and Tayda blocks automated checks.

5. **Bipolar → ceramic coupling caps** (prototype lever 6). 1.64 EUR per card plus 3.3 on the master, **about 30 EUR per console**. Same trade-off and tap test.

6. **Drop the TFPT tempco leg (R108/R158) for a plain 1 k basic resistor.** 1.95 EUR per card, **31 EUR per console**, plus one consigned type per order. The master's R421 (end-of-life ERA) would follow the same choice.
   - Trade-off [relax]: without compensation, the SSI2144's exponential scale drifts about 0.33 %/K. Over a 10-15 K warm-up that is a few percent of V/oct scale, so tracking over 5 octaves drifts by roughly a semitone. Hand-set cutoff is barely affected. This relaxes filter tracking accuracy, which decision 135 allows, but it reverses confirmed decision 130 (and item 16). Only the user can reopen that.

7. **Volume buying of the Sound Semiconductor parts.** Thonk gives 5 % at 10+, 10 % at 25+ and **50 % at 100+** (Thonk shop page, 2026-10-10).
   - Console: 32 SSI2144 at 10 % saves about 0.88 EUR per card (14 per console).
   - Product (≥100 pieces): 50 % saves about 4.4 EUR per card on the SSI2144 pair and 1.9 on the SSI2162. Also ask Sound Semiconductor's distributors for reel pricing.
   - [neutral] Ordering only.

8. **Labour (product).** Each card has 28 THT parts (6 pots, 7 buttons, 3 trimmers, connectors, jumpers). JLCPCB's manual-assembly rate is $0.0164 per joint, about 2-3 USD per card for about 150 joints. Hand-soldering the prototype (decision 133) costs nothing extra, so THT labour is not a big product cost. Calibration time is the larger labour item: see console lever 3.

Overall: console levers 1-6 together come to about 260-330 EUR on a 2,109 EUR console (12-16 %), without touching the filter or any must-stay item.

## Rule findings

**E24 (decision 134):**
- Channel card: 25 off-E24 types, 44 parts. They match the STATUS table, but no reason has been recorded yet for most of them.
- Master: 24 types, 41 parts. The STATUS table says 23; the BOM also has the 39R2 2512.
- Power: 4 types, 7 parts.
- Input module: none.
- Not in any STATUS list, because they are E24 but cost a fee: 110 R (channel SX-R-022, already noted there), 560k (master SX-R-053) and 240k (power SX-R-084).

**JLCPCB class (decision 137):**
- Channel card: 45 fee types. Master: 41. Power: 15. Unique across boards: 80, plus the undercounts above. New fee-free options found (jlcsearch, 2026-10-10):
- M7 (1N4007, SMA, master D705-D712) → R+O **1N4007W, SOD-123FL, LCSC C18199088, preferred**, 1 kV, 1 A, 30 A surge, RoHS per LCSC, $0.0091 at 50+. It needs a footprint change. The master STATUS says no fee-free M7 was found; this is one.
- SS54 (SMC, power) → **SS54 SMA, LCSC C22452, basic**, $0.037. Smaller package, so check thermals for the converter duty [check]. Power board session.
- 56p C0G 0805 (channel SX-C-027) → CL10C560JB8NNNC 0603, C39148, preferred; or 47p 0805 C0G C14857, basic.
- C0G values that are fee-free in 0805: 22p, 47p, 100p and 2n2 (basic); 12p, 15p, 18p and 33p (preferred). In 0603: 10p-47p, 100p and 330p (basic); 27p, 56p and 68p (preferred).
- There is no fee-free C0G for 220p, 560p, 6n8, 22n or 47n in any size. Those stay extended, unless the circuit tolerates X7R (not in the ladder filter) or uses parallel 2n2.
- LM317 D²PAK → a UTC LM317AG-TN3-R DPAK exists (C75510, preferred, stock 1,505), but decision 110 chose D²PAK for about 1.2 W worst-case dissipation. **Not proposed** (thermal reliability).
- No fee-free LM337, LM339, TL062, OPA2171, DG41x, SMBJ24A or 10 µF bipolar was found.

**Parts LCSC does not stock:**
- Consigned or hand-placed: SSI2144, SSI2162, AD8273, AS3046D, TFPT0603L8200FV and EEE-1VA100NP. The tool counts the EEE-1VA100NP as an extended LCSC part, but it is not at LCSC.
- DG411DY: no listing found (UNVERIFIED).
- End of life: ERA-V33J102V on the master (R421).

**Expensive resellers:** the trimmers are priced at Mouser (EUR 1.38) but cost 0.75 USD at LCSC. The duals are priced from Thonk, while Tayda is about a third cheaper.

**Availability:**
- DG413DY-T1-E3: LCSC shows 8,989 in stock; the JLCPCB-library mirror shows 331. Check JLCPCB stock before ordering.
- DG412DY-T1-E3 C553989: price rose to 8-9 USD.
- EEHZK1V331P (power SX-C-019) is back in stock: 5,666 at C278516. Power lever 4 can be closed.
- GPBS-850N: Mouser lists the Electroswitch-branded part as Obsolete. CW Industries' part is active (804 in stock), but its Mouser listing says "Non-Latching ON-(ON)"; STATUS already flags this. Watch both points for a product.
  - Correction 2026-10-10: the listing is right; GPBS-850N is the momentary twin. The latching part is GPBS-850L (Mouser 629-GPBS-850L, active, 1.61 USD at 25+; Electrokit 41012905 at 8.10 SEK incl. VAT at 25+). `parts.csv` and `prices.csv` corrected.

## Questions for the user

1. **Latching buttons → momentary tact switches with logic latches** (product). 7 GPBS850N per card at about 0.57-1.37 EUR each, against fee-free SMD tact switches placed by JLCPCB plus a latch. That is about 6-9 EUR per card (about 100-140 EUR per console), and 7 THT parts fewer per card. But decision 75 makes latching mechanics "a must" so that every state survives a power cut (must stay: recovery after a power cut). A logic latch would need a defined, safe power-up state (for example everything un-muted as before, which it cannot know) or non-volatile memory. Not proposed as a lever; ask only if the product cost needs it.
2. **TFPT tempco leg** (console lever 6): would you reopen decision 130 to trade V/oct temperature tracking for 1.95 EUR per card and one consigned part?
3. **JLCPCB billing of shared extended types per design**: confirm with JLCPCB or a test quote. It decides whether sharing part types across boards saves fees, and it moves the estimate by about ±58 EUR.

## Prices to update (for `docs/costs/prices.csv` and `overheads.csv`; checked 2026-10-10)

| ProjectPN | Price | Currency | Break | Source | Note |
|---|---|---|---|---|---|
| SX-IC-005 DG413DY-T1-E3 | 1.4526 | USD | 30+ | LCSC C141600 product page | 1.6414 at 10+. JLCPCB-library mirror (jlcsearch): 0.9013 at 30+. Mouser 781-DG413DY-T1-E3: EUR 0.98 at 25. |
| SX-IC-008 DG412DY-T1-E3 | 8.2435 | USD | 10+ | LCSC C553989 product page | 7.7636 at 30+. The lcsc-check value (5.80) is stale. |
| SX-TRIM-001 Bourns 3296W-1-503LF | 0.7546 | USD | 10+ | LCSC C83686 product page | 0.6445 at 50+. Mouser 652-3296W-1-503LF: EUR 1.38 at 25. |
| (candidate) BOCHEN 3296W-1-503 | 0.1433 | USD | 50+ | LCSC C118911 product page | 0.2034 at 5+. RoHS per LCSC. |
| SX-IC-002 SSI2162 | 3.29 | GBP | 1+ | Thonk shop page | 5 % at 10+, 10 % at 25+, 50 % at 100+ (ex VAT). Replaces the £3.50 estimate. |
| SX-IC-001 SSI2144 | 3.75 | GBP | 1+ | Thonk shop page | Same discount table. Price unchanged since 2026-10-03. |
| SX-IC-003 AD8273ARZ | 3.82 | EUR | 10+ | Mouser API 584-AD8273ARZ | 3.52 at 25. |
| SX-C-023 EEE-1VA100NP | 0.25 | EUR | 10+ | Mouser API 667-EEE-1VA100NP | 0.223 at 100. |
| SX-SW-001 GPBS-850N | 1.37 | EUR | 50+ | Mouser API 629-GPBS-850N | 1.43 at 25. Decision 75 records Electrokit at about 0.57 at 25+ (not rechecked: Electrokit page not reached). The current 1.00 EUR estimate sits between. |
| SX-C-019 EEHZK1V331P | 0.5076 | USD | 10+ | JLCPCB library via jlcsearch, C278516 | Stock 5,666 (was 0). |
| SX-IC-015 TPA6120A2DWPR | 1.7668 | USD | 10+ | JLCPCB library via jlcsearch, C70439 | |
| SX-IC-025 DRV135UA/2K5 | 3.6019 | USD | 1-9 | JLCPCB library via jlcsearch, C544663 | 2.5949 at 30+. |
| SX-IC-018 TPS54560DDAR | 0.8948 | USD | 10+ | JLCPCB library via jlcsearch, C31966 | |
| SX-K-001 G6K-2F-Y DC12 | 0.82 | USD | 10+ | JLCPCB library via jlcsearch, C397194 | |
| SX-R-053 560k, SX-R-084 240k | (extended) | | | jlcsearch class | Set jlc = extended (E24 with no fee-free part). |
| SX-C-027, SX-C-016, SX-C-017, SX-C-022 (C0G 0805) | (extended) | | | jlcsearch class | No fee-free 0805 C0G at these values. |
| SX-R-021 ERA-V33J102V | (end of life) | | | decision 130 | Not orderable. Price as the TFPT pair, or consign. |
| overheads `jlc_setup_eur_per_design` | 9.71 | USD | per design | JLCPCB help, "PCB assembly price" (Economic: set-up 8.18 + stencil 1.53) | About EUR 8.9 if Economic PCBA (single-sided) is used. |

New fee-free candidates (not yet in the BOM): CL21A106KAYNNNE 10 µF 25 V X5R 0805, C15850, basic, $0.0773 (1-199); CL31A106KBHNNNE 10 µF 50 V X5R 1206, C13585, basic, $0.1757; 1N4007W (R+O), C18199088, preferred, $0.0091 at 50+; SS54 SMA, C22452, basic, $0.0367; CL10C560JB8NNNC 56 pF C0G 0603, C39148, preferred, $0.0114.

Sources:
- LCSC product pages: [C141600](https://www.lcsc.com/product-detail/C141600.html), [C553989](https://www.lcsc.com/product-detail/C553989.html), [C83686](https://www.lcsc.com/product-detail/C83686.html), [C118911](https://www.lcsc.com/product-detail/C118911.html), [C18199088](https://www.lcsc.com/product-detail/C18199088.html).
- [Thonk Sound Semiconductor ICs](https://www.thonk.co.uk/shop/ssi2162/).
- JLCPCB: [PCB assembly price](https://jlcpcb.com/help/article/pcb-assembly-price), [PCB assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [prototype assembly (Economic 2-50 pcs)](https://jlcpcb.com/solutions/pcb-prototype-assembly).
- JLCPCB-library mirror: [jlcsearch.tscircuit.com](https://jlcsearch.tscircuit.com) (class, stock and price data).
- Mouser through `tools/mouser.py`.

## Not checked

- The `pcbparts` MCP tools (`jlc_search` with `library_type="no_fee"`) were not available in this session. Fee-free searches used the jlcsearch API that `tools/lcsc_check.py` also uses: its category endpoints (resistors, capacitors) work, its free-text search is unreliable, and it returns at most 100 results per query. A fee-free part beyond the first 100 by stock could have been missed.
- jlcsearch prices differ from LCSC's own pages (DG413: 0.90 against 1.45 USD at 30+). Which one JLCPCB charges at assembly was not confirmed.
- Whether JLCPCB bills extended fees per design or per order (see Questions).
- Tayda prices (403 to automated fetches); Electrokit's current GPBS850N price (page not found).
- Cheaper latching switches of the same size and life: no listing found through jlcsearch or TME searches.
- Datasheets not read for this review: BOCHEN 3296W (life, sealing, drawing), R+O 1N4007W (only LCSC's parameters), UTC LM317AG. The DG413 NO/NC section assignment was taken from the card's own reviewed use (U302, U206) and parts.csv, not re-read from Vishay's datasheet (the PDF did not download).
- The X5R microphonics question needs a bench test.
- Master and power PCB sizes (not laid out), the full-size power design, and the frame, panel and knob figures are still estimates from `overheads.csv`.
