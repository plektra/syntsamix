# Cost review: system, 2026-10-13

Scope: the whole system, no focus given. Read-only review by the cost controller (decision 136). Nothing below is decided; every lever is a proposal. Prices are before VAT and shipping. Rates from `docs/costs/overheads.csv` (USD 0.92, GBP 1.17). "Fee" means the JLCPCB extended-part fee, $3.07 = EUR 2.82 per type and design. Run on main at d172dd2.

## Figures

`python3 tools/costs.py estimate`:

| Item | 4 ch | 8 ch | 16 ch |
|---|---|---|---|
| channel-card parts | 195 | 385 | 763 |
| input-module-6p3 parts | 27 | 55 | 100 |
| master parts (1 used, 2 assembled) | 121 | 120 | 120 |
| power parts (1 used, 2 assembled) | 26 | 26 | 26 |
| JLCPCB fees (37 billed per design, 28 unique types) | 144 | 150 | 162 |
| PCBs | 105 | 118 | 146 |
| FR4 panels | 55 | 64 | 88 |
| Frame, hardware, ribbons, 24 V brick | 105 | 125 | 194 |
| Knobs and fader caps | 22 | 36 | 64 |
| Consigned parts handling | 30 | 30 | 30 |
| **Total (EUR)** | **831** | **1,110** | **1,693** |

A 2-channel build is EUR 700.

**Top drivers** (`costs.py drivers`):
- Channel card, EUR 48.79 per board: SSI2144 x2 8.77, DG413 x4 5.35, SSI2162 3.85, three trimmers 4.74, Alpha duals (AUX1, AUX2, TRIM) 6.66, fader 1.77, CUTOFF pot 1.19, latching buttons x7 3.92.
- Master, EUR 105.17 per board: SSI2162 x4 15.40, DG413 x10 13.36, rear jacks 6.88, DRV135UA x2 6.63, rear IDC sockets 5.32, bipolar 10 uF x16 4.00 (consigned), heatsinks 3.00, AS3046D 2.50.
- Power, EUR 16.83 per board: 24 V jack 3.68, 4u7 100 V x10 2.48, 330 uF x4 1.87, TPS54560 x2 1.65.
- At 4 channels the fixed costs (fees 144, PCBs 105, panels 55, consignment 30, frame fixed, second master and power board) are about 45 % of the total. At 16 channels the channel cards are 45 % and the per-channel parts count sixteen times.

**Change since the last cost reports.** Last full reports: `2026-10-10-cost-system.md` (958 / 1,112 / 2,109 EUR for 2 / 4 / 16 channels, 80 fee types) and `2026-10-10-cost-system-15v-rails.md` (946 for 4 channels, 1,795 for 16). Now 831 / 1,110 / 1,693 for 4 / 8 / 16 (ROADMAP track for 4 channels: EUR 1,112 on 2026-10-10 -> 831). The fall comes from decisions 139-161: DG412 -> DG413, TL072 difference receiver instead of the AD8273 (143, 148), MUTE/DUCK by the button poles (142), E24 and fee-free values (140, 144, 146, 147, 156), hand-soldered consigned ICs (150, 155), bipolar coupling caps as ROQANG pairs on the channel card (161), the cheaper fee model (Economic set-up EUR 8.93 per design), the power board redesign (156-159). Fee types: 80 -> 28 unique. Decisions 162-171 then put EUR 56 back for every off-board part (rear jacks, cables, row boards, `docs/costs/offboard.csv`).

**Realized costs** (`costs.py ledger`): EUR 53.80 parts to date (1 entry, 2026-10-04).

### The estimate is still too low in two places

| Finding | Effect | Status |
|---|---|---|
| Chain ribbons (decision 109) are in neither `offboard.csv` nor the EUR 5 per channel frame overhead (on hold, `CONTINUE-FROM-HERE.md` item 5) | about +36 EUR at 4 ch (the user's figure; I get the same: 8 audio sockets, about 10 power sockets, cable), about +100 EUR at 16 ch | Mouser prices in `prices.csv`, 2026-10-13 |
| Box headers SX-CONN-007 (Wurth 2x17) and SX-CONN-008 (Wurth 2x4) are still "estimate" at 0.90 and 0.40; Mouser today is 1.35 and 0.894 at 10+ | +0.45 and +0.49 each, two of each per card: +1.9 EUR per card, +7.6 at 4 ch, +30 at 16 ch (master +1) | Mouser 710-61203421621 and 710-61200821621, 2026-10-13 |

With both, the corrected totals are about 880 / 1,170 / 1,830 EUR (4 / 8 / 16). The lever list below is priced against the true Mouser figures.

Other classification errors found: SX-D-009 SMBJ24A has no price row, so the tool falls back to "extended", but LCSC C19077578 (hongjiacheng) is **preferred**: one fee type less (lever P3). SX-D-013 SS510C (extended, C19229, 0.0966 USD at 50+), SX-F-002 BSMD1812-200-33V (extended, C7433877, 0.1387 USD at 50+) and SX-R-082 (39R2 2512) also have no price row and use the fallback.

## Levers

Marks: **[relax]** = accuracy the audience cannot hear (decision 135 may trade it); **[neutral]** = same function; **[check]** = a must-stay item is near and needs a test.

### Prototype (fixed costs dominate)

**P1. Start with 2 channels.** Saves EUR 131 (831 -> 700). Trade-off: chain effects of 3 and 4 cards (bus noise, power ribbon current) go untested. [neutral]. Ordering only; open since ROADMAP lever 3.

**P2. Master bipolar 10 uF x16 (SX-C-023, consigned) -> back-to-back ROQANG pairs (SX-C-024, C72486, already on the board).** Saves about EUR 36: the whole EUR 30 consignment handling (the master is the last consigned type), one consigned fee type EUR 2.82, about EUR 3.4 of parts (Mouser EEE-1VA100NP EUR 4.00 against 32 x EUR 0.019). The 32 extra placements cost under EUR 0.2. Same as channel decision 161 (refines 127); already listed in `hardware/master/STATUS.md`. Trade-off [relax + check]: breadboard test 11 must clear the pair. The DRV135 sense-pin caps C707-C710: TI recommends 10 uF non-polarised, so these four may need a different part (a new extended type, EUR 2.82, would eat part of the saving); check the datasheet first. Effort: schematic part swap, before layout. Evidence: prices.csv rows SX-C-023 and SX-C-024, `overheads.csv` consign line.

**P3. Three fee types with a fee-free equivalent.** Saves about EUR 8.5 (3 x 2.82), the same at every size.
- SMBJ24A (SX-D-009): already preferred (LCSC C19077578, 0.054 USD, stock 5,209, pcbparts 2026-10-13). A price-table fix, no design change.
- 56p C0G 0805 (SX-C-027, channel, 2 parts) -> 56p C0G 0603, Samsung CL10C560JB8NNNC, C39148, **preferred**, 0.0113 USD. Needs the 0603 footprint; channel card only.
- 240k 0805 (SX-R-084, power, 4 parts) -> UNI-ROYAL 0603WAF2403T5E, C4197, **preferred**, 0.0036 USD, 100 mW, 75 V. The earlier "no fee-free 240k" finding was for 0805 only. Power board [check]: the part sets the buck feedback and RT, so re-run `scripts/design.py` to confirm a 1 % 0603 changes nothing (resistor power is microwatts).

[neutral]. Effort: footprint changes before layout.

**P4. Merge the two master rear row boards into one design** (output board and input board, decision 163). Saves one PCB minimum, about EUR 13.5 at any size (15 - 1.5), plus one layout. Both carry six positions on a 26-pin ribbon; make the position map identical and give the ground-lift switch a footprint next to one jack position. [neutral]. Effort: layout of the two row projects, which are not drawn yet. UNVERIFIED: whether the two signal maps can share one pin order without hurting the master's routing.

**P5. Chain connector family** (console lever C1; it helps at 4 channels too): about EUR 30 at 4 channels against true Mouser prices (the tool, with its estimated headers, would show about 17).

**P6. LCSC trimmers.** Bourns 3296W-1-503LF at LCSC C83686 is 0.7487 USD (EUR 0.69) at 10+, 0.639 USD at 50+, against EUR 1.58 at Mouser at 10+: saves about EUR 2.7 per card, EUR 10.7 at 4 channels. LCSC shipping is a second parcel (not priced), which eats most of it at 4 channels; take it when an LCSC order is placed anyway. [neutral]. Same part, no design change.

**Not a lever, but check: PCB minimum.** `pcb_min_eur_per_design = 15` (estimate) sets the PCB line to EUR 105 at 4 channels: six designs at the minimum. JLCPCB's marketing page quotes 5 pcs of a 100 x 100 mm 2-layer board from $2.00 (typical market price $10-20; search result, 2026-10-13). The input module, power board and row boards are small, so the real PCB line could be tens of euros lower, shipping aside. Confirm with an instant quote before treating EUR 105 as fixed. UNVERIFIED.

### Console and product (per channel x16, volume, labour)

**C1. Chain connectors from Wurth WR-BHD to Adam Tech BHR / FCS (headers and IDC sockets).** The 2x4 power socket is the dearest chain part (Wurth 61200823021: EUR 1.81 at 1, 1.53 at 25, 1.32 at 50). Mouser, 2026-10-13, 10+ prices:

| Part | Wurth now | Adam Tech | Saving each |
|---|---|---|---|
| 2x17 box header | 61203421621: 1.35 | BHR-34-VUA: 0.415 | 0.94 |
| 2x4 box header | 61200821621: 0.894 | BHR-08-VUA: 0.218 | 0.68 |
| 2x17 IDC socket | 61203423021: 1.07 | FCS-34-SG: 0.561 | 0.51 |
| 2x4 IDC socket | 61200823021: 1.75 | FCS-08-SG: 0.518 | 1.23 |
| 2x13 IDC socket (master rear ribbons) | 61202623021: 1.33 | FCS-26-SG: 0.634 | 0.70 |
| 2x13 box header | 61202621621: 0.937 | BHR-26-VUA: 0.350 | 0.59 |

Per added channel card (two headers of each size, one jumper of each size): 2 x 0.94 + 2 x 0.68 + 2 x 0.51 + 2 x 1.23 = EUR 6.7 per card. At 16 channels about EUR 105 (about EUR 90 with break prices); at 4 channels about EUR 30; the master's rear ribbons (4 sockets, 3 headers) add EUR 5. Evidence: Mouser 2026-10-13; Adam Tech FCS-08-SG rated 1 A, 250 V, 2.54 mm, ribbon cable (Master Electronics, Kynix, DigiKey listings); no wire gauge stated, so the 28 AWG fit stays a mock-up item as with Wurth (decision 109). Trade-off [check, reliability]: the plating of Adam Tech's stocked BHR-xx-VUA header is UNVERIFIED (I could not open the datasheet; the gold variant BHR-34-VSGA has a 2,000-piece minimum), while the FCS-xx-SG sockets are selective gold. Do not pair gold sockets with tin headers on a bus that carries low-level audio without a contact test; take a tin/tin or gold/gold pair, or run the mock-up with both. Footprints: all 2.54 mm shrouded box headers; the Wurth drawing figures (50.84 mm long, 9.1 mm high) must be compared with Adam Tech's before layout. Effort: part swap and footprint, before layout. Affects decisions 100, 109, 117, 163. Note: Mouser lists the Wurth 61203421621 as "Angld Box Hdr", while `parts.csv` calls it straight (drawing rev 002.001): confirm which is true.

**C2. One bus cable with a socket per card, instead of U-loop jumpers** (extends C1; changes decision 109). A card's IN and OUT headers are wired straight through (`CHAIN.md`), and the strip pitch is 35.0 mm, so a continuous 34-way (and an 8-way) cable with a socket crimped every 35 mm into each card's IN header does the same job. Saves one socket per gap and the OUT headers: about EUR 8 at 4 channels and EUR 25 at 16 on top of C1 (Adam Tech prices), or about EUR 45 on top of the Wurth set. A benefit: pulling one card no longer breaks the chain (a straight-through daisy chain does). Costs: a longer cable is needed when channels are added (or build the cable for 8 or 16 and leave unused sockets dangling), and mid-cable crimping of these sockets is UNVERIFIED (no listing says the part is made for it). Needs the user: it changes confirmed decision 109 and the "add one card at a time" habit. [neutral] on decision 135.

**C3. Input module cable: IDC ribbon instead of the ready-made Molex 217796-1101** (ROADMAP cost watch 8). Molex 217796-1101: EUR 4.84 at 1, 4.28 at 10, 4.00 at 25 (the tool uses EUR 5.18 per channel). IDC route: Adam Tech FCS-10-SG 10-way socket EUR 0.297 at 10+ (x2 = 0.59), 3M 3365/10 cable at EUR 0.258 per foot (150 mm = 0.5 ft = 0.13); the headers stay at about EUR 0.40 each (KK today, Wurth 10-pin box 61201021621 EUR 0.404): about EUR 0.75 against 5.18. Saves about EUR 4.2 per channel: EUR 17 at 4 channels, EUR 67 at 16 (about EUR 55 against the 25+ price). It avoids hand crimping: a socket is pressed in a vise or a cheap IDC press. Trade-offs [check]: a 2x5 box header must not accept a 2x4 power socket (the shroud is longer, so a 2x4 socket can sit off-centre in it: check the key slot on a sample, or use a size no other socket fits), and signal pairs need ground wires between them (pin map in `INPUT-MODULE.md`). Affects decision 99 and the connector on the input module and channel card. Effort: connector and footprint change on two boards, before layout.

**C4. Trimmers: LCSC Bourns and one fewer.** LCSC C83686 as P6: EUR 2.7 per card, about EUR 43 per console (EUR 47 at 50+). Then the fixed V/oct scale (`channel-card/CHECKLISTS.md` open item 13, if breadboard test 12 shows the chips within about +-2 %): remove RV182, EUR 1.58 per card (EUR 25 per console) and one calibration step per card, which counts as labour in a product. [relax] filter tracking accuracy (decision 135 allows it); the two cutoff offset trimmers per card stay.

**C5. Volume buying of the Sound Semiconductor parts.** Thonk gives 5 % at 10+, 10 % at 25+, 50 % at 100+ (already in the tool: 10 % at 16 channels). A product bought in a 100-piece lot halves the SSI2144 x2 and SSI2162 (EUR 12.6 per card -> about EUR 6.3): about EUR 100 per 16 cards. [neutral], ordering. Distributor reel pricing not checked.

**C6. TL062 -> TL072CDT (basic).** Removes the TL062 fee type (shared by channel and master, billed twice): about EUR 5.6, the same at all sizes. The cost: 2.4 mA more per package per rail (TL072 1.4 mA per amplifier, TL062 0.2 mA; datasheets), six packages at 4 channels, 36 at 16 = +86 mA per rail at 16 channels (about +4 % of the typical 2.1 A). Better noise (about 18 against 42 nV per root hertz). Reverses the power cut of decisions 123 and 126. [neutral] for audio. Only worth it if the power budget has the room; low priority.

**C7. THT labour at product volume.** Each card has 28 through-hole parts and three trimmers. JLCPCB manual assembly is about $0.0164 per joint (about USD 2.5 per card); calibration is the larger item (see C4). Hand-soldering costs nothing here (decision 133).

**Order of size at 16 channels** (rough): C1 105 (plus C2 25), C5 up to 100 (product only), C3 67, C4 43-68, then C6 5.6.

## Rule findings

**E24 (decision 134).** Nothing new. The channel card has no off-E24 values (`CHECKLISTS.md`: none since R217 = 30k). The master's only exception is the 39R2 2512 (R754, R758, recorded with its reason). The power board has none; 240k is E24 but extended in 0805 (lever P3 gives a preferred 0603).

**JLCPCB class (decision 137).** 28 unique extended or consigned types (37 billed per design), about EUR 79 per order in fees plus set-ups. By lever:
- SX-D-009 SMBJ24A: preferred (C19077578); the tool's class is wrong because the price row is missing.
- SX-C-027 56p: preferred in 0603 (C39148). SX-R-084 240k: preferred in 0603 (C4197).
- SX-C-016 47n C0G 0805 (master, power) has a basic X7R 47n in 0805 (CL21B473KBCNNNC, C53134, 0.0173 USD). Whether the two uses tolerate X7R (C0G was chosen for a reason) is for the board sessions: UNVERIFIED.
- Still no fee-free part: 220p C0G, 6n8, 560p, 47n C0G 1206, 4u7 100 V 1210 (no X7R 50 V 1210 found either), 330u hybrid, ROQANG 10 u / 47 u, fuse 2 A 33 V 1812 (none in the library), SS510C SMC, 2u2 SRP7028A, SQJ457EP, DG413, LM13700, LM339, TL062, OPA2171, LM317 / LM337 D2PAK, TPS54560, TPA6120A2, 39R2 2512 and 10k 0.1 % (SX-R-107; no 0.1 % part is basic or preferred).
- Stock watch: LCSC C278516 (330u hybrid EEHZK1V331P, power board, minimum order 15) shows **0 in stock** in the pcbparts database on 2026-10-13. It was 5,666 on 2026-10-10 (power STATUS lever 7). Re-check with the stock-check helper before ordering.

**Parts LCSC does not stock.** SSI2144, SSI2162, AS3046D, TFPT0603L8200FV (hand-soldered or consigned, decisions 150, 155). SX-C-023 (Panasonic EEE-1VA100NP, master) is the only consigned type left (lever P2). Wurth box headers and IDC sockets are Mouser-only (lever C1).

**Parts from expensive resellers.** Wurth chain connectors (C1); the Molex ready-made input cable (C3); Bourns trimmers at Mouser against LCSC (P6).

## Questions for the user

1. **CMRR of the receivers (touches "noise and hum" in the must-stay list).** The 36 resistors of type SX-R-107 (10k 0.1 %; channel 12 per card, master 24) cost a fee type billed twice (EUR 5.6) and about EUR 0.45 per card more than 1 % parts. With 1 % resistors the worst-case CMRR falls from 51.5 dB to about 34 dB (about 40 dB typical): fine for short runs, a weaker hum defence on a stage with long cables to ground-lifted gear. Saves about EUR 13 at 4 channels, EUR 20 at 16. I do not propose it; hum rejection is on the must-stay side. Tell me if you want a measured hum figure from the breadboard first.
2. **Decision 109 (U-loop jumpers) -> bus cable** (lever C2): changes a confirmed decision and the build habit. Savings EUR 8 (4 ch) to 25-45 (16 ch).
3. **Decision 99 (input module header) -> IDC ribbon** (lever C3) reverses your agreement of 2026-10-13 to use ready-made Molex cables to avoid hand crimping. The saving is EUR 4.2 per channel (EUR 17 for the prototype). Your call whether that justifies a vise squeeze per cable.
4. **TL062 -> TL072** (C6): reopens the power cut of decisions 123 and 126 for EUR 5.6.
5. **Decision 100 (16-channel power):** the 16-channel figure still prices one power board. A second power board is mostly already paid for by the two-board assembly minimum; the open question is whether one TPS54560 inverter holds 8 cards + master, not the price.

## Prices to update (`docs/costs/prices.csv`)

| ProjectPN | Price | Currency | Source | Date | Note |
|---|---|---|---|---|---|
| SX-CONN-007 | 1.35 (50: 1.19; 100: 1.02) | EUR | Mouser 710-61203421621 (10+) | 2026-10-13 | replaces estimate 0.90 |
| SX-CONN-008 | 0.894 (50: 0.783; 100: 0.671) | EUR | Mouser 710-61200821621 (10+) | 2026-10-13 | replaces estimate 0.40 |
| SX-CONN-012 | 1.75 (25: 1.53; 50: 1.32) | EUR | Mouser 710-61200823021 (10+) | 2026-10-13 | breaks for the row already in the file |
| SX-D-009 | 0.054 (50+: 0.0439) | USD | LCSC C19077578 | 2026-10-13 | class **preferred** (add a row) |
| SX-D-013 | 0.0966 (1+: 0.115) | USD | LCSC C19229 | 2026-10-13 | class extended (add a row) |
| SX-F-002 | 0.1387 (1+: 0.1803) | USD | LCSC C7433877 | 2026-10-13 | class extended (add a row) |
| SX-CONN-022 | 4.28 (25: 4.00; 50: 3.81; 1: 4.84) | EUR | Mouser 538-217796-1101 | 2026-10-13 | file has USD 5.63 at 1+, close enough |
| (candidate) Adam Tech FCS-34-SG | 0.561 (25: 0.495; 120: 0.47) | EUR | Mouser 737-FCS-34-SG | 2026-10-13 | lever C1 |
| (candidate) Adam Tech FCS-08-SG | 0.518 (25: 0.463; 100: 0.42) | EUR | Mouser 737-FCS-08-SG | 2026-10-13 | lever C1 |
| (candidate) Adam Tech FCS-26-SG | 0.634 (25: 0.562; 80: 0.53) | EUR | Mouser 737-FCS-26-SG | 2026-10-13 | lever C1 |
| (candidate) Adam Tech FCS-10-SG | 0.297 (25: 0.265; 100: 0.243) | EUR | Mouser 737-FCS-10-SG | 2026-10-13 | lever C3 |
| (candidate) Adam Tech BHR-34-VUA | 0.415 (100: 0.352) | EUR | Mouser 737-BHR-34-VUA | 2026-10-13 | lever C1 |
| (candidate) Adam Tech BHR-08-VUA | 0.218 (100: 0.214) | EUR | Mouser 737-BHR-08-VUA | 2026-10-13 | lever C1 |
| (candidate) Adam Tech BHR-26-VUA | 0.35 (120: 0.294) | EUR | Mouser 737-BHR-26-VUA | 2026-10-13 | lever C1 |
| (candidate) 56p C0G 0603 | 0.0113 | USD | LCSC C39148, preferred | 2026-10-13 | lever P3 |
| (candidate) 240k 0603 | 0.0036 | USD | LCSC C4197, preferred | 2026-10-13 | lever P3 |

DG413DY C141600 reads 1.9311 / 1.631 / 1.4435 / 1.251 USD at 1 / 10 / 30 / 100+, the same as the file's 30+ break. The Bourns 3296W trimmer at LCSC C83686: 0.7487 USD at 10+, 0.6394 at 50+ (extended, through-hole).

## Not checked

- Contact plating of the Adam Tech BHR-xx-VUA headers and FCS-xx-SG sockets, their mid-cable use and the 28 AWG fit: the datasheet fetch timed out; only distributor listings read.
- JLCPCB instant quote for the six small PCB designs (the estimate's EUR 15 minimum); Standard-PCBA panelling of the 33 mm channel card above 30 boards.
- Real JLCPCB billing of extended types shared by two designs (`jlc_fee_per_design` still assumed 1).
- Frame, panel, knob and brick overheads are estimates in `overheads.csv` (frame_fixed EUR 40, panel EUR 3 per strip, knobs EUR 3.5 per channel); no supplier quote.
- Alpha duals (AUX1, AUX2, TRIM): only Thonk carries the exact order codes (Tayda has no T18 duals), so no cheaper source was found; Mouser and DigiKey alternatives not searched.
- DG413 count per card (4) and on the master (10): I did not audit which sections could go (master `CHECKLISTS.md` lever 1 already asks). The only fee-free analog switches in the library are CD4051 and CD4052 (3-20 V supply, too low for the +-15 V audio rails).
- Brick: the GSM120B24 (EUR 44.60) is sized for the worst case of 59 W; no smaller Class II brick was priced.
