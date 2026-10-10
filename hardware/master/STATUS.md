# Master card status

Updated 2026-10-10: `/board master` session, SC LPF pot RV501 to a standard Alpha dual B100K (decision 138); non-B pot ratings checked. Before that, 2026-10-09: RELEASE pot to C100K (decision 131). Before that, `/board master` pre-layout session (the user delegated the open points to Claude's recommendation): decisions 89-94 open points confirmed, decisions 125-128 drawn. Rebased on /system decision 124 (Alpha pots RoHS-cleared).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128, 131, 138).
- 2026-10-10:
  - SC LPF RV501 is an Alpha RD902F-40-15K-B100K-0057 dual (Thonk, in stock, SX-POT-015; decision 138): same circuit, sweep 46 / 60 / 85 / 146 / 510 Hz at CCW / 25 % / middle / 75 % / CW (`simulation/sidechain/`). Order code by analogy with Thonk's other dual codes: confirm with the order.
  - Non-B pots against Alpha's 0.02 W rating: THRESHOLD RV502 about 2.5 mW, DECAY RV504 at most 0.2 mW, AUX SEND and PHONES duals audio only (about 6 mW per gang at +20 dBu): no change needed (recorded in decision 138).
- 2026-10-09:
  - RELEASE RV402 is a C100K (Alpha RD901F-40-15K-C100K, Tayda A-5370, SX-POT-014) with R425 6.2 kΩ (decision 131): about 2 mW instead of 20 mW against Alpha's 0.02 W non-B rating; release law unchanged in simulation (44 ms to 1.43 s per 10 dB). Tayda A-5370 still to recheck by hand before ordering (Tayda answers 403 to scripts; Thonk has no C taper).
  - Main output drivers U703/U704 are TI DRV135UA (decision 125): the THAT1646 is end of life (THAT memo 2026-09-01, last-time buy closed 2026-09-30). Same SO-8 pinout, footprint and nets; LCSC C544663.
  - TL062 (SX-IC-024) for U409, U410, U802, U804 (decision 126). Superdiodes U207/U307/U706 and log detector U407 stay TL072.
  - All electrolytics SMD, 5.4 mm tall (decision 127): SX-C-023 bipolars, SX-C-024/025 ROQANG.
  - Relay drop-out watches both raw rails (decision 128): U707C on −20V_RAW through 22k6/100k, wired-OR into UV_O; the power sheet exports −20V_RAW.
  - Würth maker fields on J101 and J901; BAT54T1G D504 has LCSC C152458.
  - Power budget: typical 331 / 260 mA, worst case 701 / 576 mA, sizing 576 / 463 mA; heatsinks still ≤ 11.5 °C/W.
- 2026-10-08: decisions 97, 98, 103, 104 drawn (see the decision files).
- PCB: not started.

## Decided this session (no longer waiting)

- 89: Q5 unused (checked against Alfa's datasheet and the drawing); makeup +22 dB kept, heard on the breadboard; fallback R439 = 330 kΩ caps it at +20 dB.
- 90: a silent patched EXT cable selects EXT; no EXT LED.
- 91: no output coupling capacitors on the AUX sends.
- 92: replaced by decision 128 (both raw rails watched).
- 93: meter colours green / yellow / red as proposed.
- 94: headphone gain 2, cue inverted (inaudible), PFL LED yellow.
- Power lever (Power-cut candidate 2): decision 126.

## Checked this session

- G6K-2F-Y: Omron K106-E1-11 terminal diagram matches the wiring of K701, K702 and K751 (coil + pin 1, COM 6/3, NC 7/2, NO 5/4). KiCad's footprint matches Omron's land pattern. Height 5.2 mm.
- Würth 61200821621 / 61203421621: KiCad IDC outlines match the drawing (rev 002.001) within 0.1 mm. Drill 1.1 mm at layout (KiCad's 1.0 mm is inside tolerance but tight for the 0.905 mm pin diagonal).
- LCSC stock (pcbparts lookup 2026-10-09; `tools/lcsc_check.py`'s jlcsearch API returned nothing that day):
  - In stock: TL072CDR C67473, TL062CDR C67471, LM339DR C7948, DG413DY C141600, DG411DY C17218, OPA2171 C40904, G6K C397194, L7805CV C111887, LM337TG C73683, ST LM317T C361026, MMBT3904LT1G C81464, BAT54T1G C152458, DRV135 C544663.
  - Low stock: TPA6120A2 C70439, 406 pieces.
  - Not at LCSC: AD8273, SSI2162, AS3046D, ERA-V33J102V.

## Open: needs the user or another session

- **Pots:** RoHS cleared by Taiwan Alpha's general declaration (decision 124, /system 2026-10-09) for every standard Alpha model; candidates with order codes in `docs/parts.csv` (SX-POT-004 to -010).
- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **ERA-V33J102V (R421, SX-R-021):** the channel card replaced it with a Vishay TFPT0603L8200FV (820 Ω, +4110 ppm/K, in stock, RoHS) plus 180 Ω in series: 1 k at about +3370 ppm/K (decision 130); the same pair fits here if R421 needs 1 k at about +3300 ppm/K. R421 is End of Life at Mouser with no stock (2026-10-09) and RoHS by exemption; check whether the compressor detector needs exactly 1 k +3300 ppm/K before reusing the pair. The TFPT is Mouser-only (not at LCSC): hand-solder or consign it.
- **Meter LEDs (SX-D-004/005/006):** candidates Kingbright WP710A10LGD/LYD/LID (Mouser). Their body height is unverified, and a 3 mm LED reaching the panel conflicts with the 9 mm top-side rule unless its panel hole is the exception. Settle the form (3 mm or 0805 under a bezel as decision 119) with the master section panel.
- **Ground-lift switch SW901 (SX-SW-002):** part to choose with the rear panel.

## Check before layout

- **Chain headers (decision 109; `docs/MECHANICAL.md`):** J101 along the master's left edge, on the underside, long axis front to back, at the distance from the front that the channel card layout records. J901's position is free until the master section is settled.
- **Panel stack (decision 107):** top-side parts ≤ 9.0 mm. Still too tall: U901-U903 TO-220 (about 19.7 mm seated) and the HS901/HS902 heatsinks (≤ 11.5 °C/W needed). Where they go (outside the panel area, the rear edge, or the power board) is settled in `/system mechanical`. Everything else on top is now ≤ 5.4 mm, except the jacks, pots and buttons that meet the panel.
- **Breadboard:**
  - hear the ducking through the channel's 10 ms smoothing (decision 97);
  - the bottom of the master level pot (about −102 dB, decision 103);
  - the compressor makeup at +22 dB (decision 89).
- **RoHS strict (decision 116):** every part needs a `RoHS: <source>` in `docs/parts.csv` before ordering; lead-free finish and assembly. Standard passives get theirs when the BOM is fixed.
- **Jack sizes (decision 118):** 6.3 mm for the audio connections; EXT sidechain input 3.5 or 6.3 mm, chosen with the master front panel.
- **Panel fixing (decision 120):** one centred M3 button-head screw per end plus a printed key, unless the master section decides otherwise.
- **Underside (decision 121):** underside parts only at the chain headers and hand-set parts (≤ 10.5 mm); 10 mm from the header edges clear.

## Next

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: `/system mechanical` for the master section (heatsinks, meter LED form, rear panel) and the AS3046D declaration.

## Cost-cut levers [proposed] (2026-10-09)

Cost frame set by the user (2026-10-09): prototype of 4 channels (maybe 2), the full console cost kept in view for a possible product, the filter stays; overview in `docs/ROADMAP.md`, Cost review. The master is a fixed cost of about €165 in parts (one per mixer), but JLCPCB assembles at least 2 boards per design, so the prototype pays for a second set of its SMD parts (about €100) unless only one is populated. Through-hole parts are hand-soldered by the user (decision 133). Done: the 13 jacks are Rean NYS216 (decision 132, about €15 saved). Rough prices at 20-50 pieces; none of these is decided:

1. **AUX return receivers AD8273 ×2 → op-amp differential receivers** (as channel lever 2): about €9, and one part type fewer to consign.
2. **DG413 ×9 (about €17):** check which switch sections could move to relay contacts already present or to VCA control (as channel lever 3); probably €4-8.
3. Value selection (E24, JLCPCB extended fees) is a standing rule now, not a lever: see "Component values" below (decision 134).
4. **Master meter:** 24 discrete 3 mm LEDs (meter form still open, decision 86 against 119); the 0805-under-bezel form of the channels saves little money but one hand-soldered part type.
5. Not recommended: TPA6120A2 (about €4) → NE5532 with a discrete buffer; saves about €3 but weakens the headphone drive.

From the system cost review of 2026-10-10 (`docs/reviews/2026-10-10-cost-system.md`, with savings and caveats). None of these is decided:

6. **U641 DG411 → DG413** by inverting DET1 at its comparator (swap the inputs): one part type fewer, and the DG411 may not be at LCSC (unverified).
7. **Hand-solder the expensive ICs on the one master used** (SSI2162 ×4, DG413 ×9, AD8273 ×2, DRV135UA ×2, AS3046D), keeping them off the JLCPCB BOM so the forced spare master does not carry them: about €52. Costs 18 SOIC/SSOP joints to inspect; touches decision 133. Keep the TPA6120A2 on JLCPCB.
8. **10 µF bipolar electrolytics ×16 → X5R ceramic** (as channel lever 7): about €3.30 per master; tap test first. Touches decision 127.
9. **M7 (D705-D712) → R+O 1N4007W SOD-123FL** (C18199088, JLCPCB preferred, 1 kV 1 A): removes a fee type; needs a footprint change and a datasheet check.
10. **R421 ERA-V33J102V is end of life** (decision 130): choose the TFPT pair or consignment; priced as a TFPT in `prices.csv` for now.
11. **Values:** the off-E24 table has 24 types (the 39R2 2512 was missing; no fee-free 2512 or 1206 value from 10 to 51 Ω exists, so keep it as a recorded exception); 560k is E24 but has no fee-free part.

## Component values (decision 134)

This board owns its value selection (rule in `CLAUDE.md`). Values outside E24 on 2026-10-09 (from the BOM export; all resistors; every capacitor is already E24). Each needs a reason recorded here, or a move to E24 values or an E24 pair, before layout.

| Sheet | Value | References | Reason (to record) |
|---|---|---|---|
| AUX returns, master out | 113k, 453k, 221k, 63k4, 124k, 8k66, 33k2, 30k1 | R222-R232, R322-R332, R714-R721 (and compressor R443: 453k) | same values as the channel card's Level set (fader law, decisions 79 and 103 to confirm); settle with the channel card |
| Compressor | 140k, 4k02 | R426, R445 | |
| Master out, meter | 22k6 | R732, R814 | |
| Headphones | 39R2 (2512) | R754, R758 | |
| Meter | 115k, 13k3, 31k6, 16k2, 11k3, 8k06, 5k62, 5k11, 3k83, 2k15, 1k87, 866 | R811-R813, R815-R823 | meter sheet (ladder, to confirm) |

23 types, 39 parts.

From the channel card (2026-10-10, decision 140): the channel settled its copy of the fader-law set on fee-free E24 parts and pairs. 113k = 100k + 13k, 453k → 300k + 150k (450k), 221k → 220k, 63k4 → 62k, 124k = 100k + 24k, 8k66 → 9k1, 33k2 → 33k; 30k1 kept (chain line, /system). `simulation/level/run.py` shows the law within 0.4 dB of the design from +10 to −60 dB. To keep the AUX returns and master out on the same law, take the same values here (the fader-law parts follow the same circuit, decision 103). The channel's meter ladder fit (`docs/decisions/channel-card.md`, item 140) is a model for this board's meter ladder.

Also from the channel card (2026-10-10): its AD8273 receiver became a TL072 difference amplifier with 10k 0.1 % resistors (decision 143, CMRR ≥ 51.5 dB, about €3.20 saved per receiver chip). The AUX returns use the same AD8273 circuit (SPEC, AUX returns), so the same swap would apply here (ROADMAP cost lever 4, AUX returns part) and would end the AD8273 consignment altogether.

### Fee-free candidates [proposed] (decision 137, LCSC search 2026-10-10)

| Part | Now | Fee-free candidate | Check before the swap |
|---|---|---|---|
| TL072 (SX-IC-007, 13 here, 4 on the channel card) | extended | ST TL072CDT, LCSC C6961, basic | chosen in `parts.csv` by the channel card session 2026-10-10 (pinout and limits as TI's); still to do here: the master's TL072 symbols say Manufacturer Texas Instruments (`TI` dict in the wired scripts): give SX-IC-007 the ST fields (Manufacturer STMicroelectronics, MPN TL072CDT, LCSC C6961) at the next master schematic session |
| 6.2 V zener (SX-D-001, 4 here) | no part chosen | BZT52C6V2 (hongjiacheng), LCSC C19077403, preferred | chosen in `parts.csv` 2026-10-10 (RoHS in the maker's datasheet, land pattern matches `D_SOD-123`); symbols carry ProjectPN only, nothing to redraw |
| BAT54T1G (SX-D-014, D504) | onsemi, extended | BAT54W (hongjiacheng), LCSC C7502705, preferred | leakage and forward voltage in the SC_ENV clamp (decision 104) |
| 680k R | counted as extended | UNI-ROYAL 0805W8F6803T5E, LCSC C17797, preferred | chosen in `parts.csv` 2026-10-10 |

No fee-free part was found for the LM339, the M7 (1N4007) SMA rectifier, the 220 pF C0G 0805 or the 10 µF 35 V SMD electrolytic. `python3 tools/costs.py extended` lists every type that still costs a fee.

## For /system

- **Budgets after decisions 125-128 (2026-10-09):**
  - master typical 331 / 260 mA (was 340 / 269), worst case 701 / 576 mA (was 719 / 594), sizing 576 / 463 mA (was 589 / 476);
  - prototype sizing 1.27 / 1.03 A, 46 W (was 1.28 / 1.04 A, 47 W);
  - full size sizing 3.36 / 2.73 A (was 3.37 / 2.75 A); ribbon per pin unchanged.
  - Update the `docs/ARCHITECTURE.md` power table (`tools/system_power_budget.py`).
- **Master section mechanics:** TO-220 regulators and heatsinks (19.7 mm, ≤ 11.5 °C/W, live tabs); meter LED form (3 mm through the panel vs 0805 under a bezel, decision 86 vs 119).
- **`docs/ARCHITECTURE.md` text:** the system diagram (line 12, "main out (THAT1646)") and the RoHS open item (THAT1646 End of Life) predate decision 125: change to DRV135 and drop the End of Life item. The architect review could not run at handoff (account spend limit); run it at the start of the `/system` session on this commit.
- **RoHS open items:** the ERA-V33J102V is also on the master (R421), not only the channel card, as the audit lists it. THAT1646 End of Life closed by decision 125.
