# Master card: checklists and reference

Read for layout, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

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

## Checked part facts

- G6K-2F-Y: Omron K106-E1-11 terminal diagram matches the wiring of K701, K702 and K751 (coil + pin 1, COM 6/3, NC 7/2, NO 5/4). KiCad's footprint matches Omron's land pattern. Height 5.2 mm.
- Würth 61200821621 / 61203421621: KiCad IDC outlines match the drawing (rev 002.001) within 0.1 mm. Drill 1.1 mm at layout (KiCad's 1.0 mm is inside tolerance but tight for the 0.905 mm pin diagonal).
- LCSC stock (pcbparts lookup 2026-10-09; `tools/lcsc_check.py`'s jlcsearch API returned nothing that day):
  - In stock: TL072CDR C67473, TL062CDR C67471, LM339DR C7948, DG413DY C141600, DG411DY C17218, OPA2171 C40904, G6K C397194, L7805CV C111887, LM337TG C73683, ST LM317T C361026, MMBT3904LT1G C81464, BAT54T1G C152458, DRV135 C544663.
  - Low stock: TPA6120A2 C70439, 406 pieces.
  - Not at LCSC: AD8273, SSI2162, AS3046D, ERA-V33J102V.

## Cost-cut levers [proposed] (2026-10-09)

Cost frame set by the user (2026-10-09): prototype of 4 channels (maybe 2; 2026-10-10: costs tracked for 4, 8 and 16-channel builds), the full console cost kept in view for a possible product, the filter stays; overview in `docs/ROADMAP.md`, Cost review. The master is a fixed cost of about €165 in parts (one per mixer), but JLCPCB assembles at least 2 boards per design, so the prototype pays for a second set of its SMD parts (about €100) unless only one is populated. Through-hole parts are hand-soldered by the user (decision 133). Done: the 13 jacks are Rean NYS216 (decision 132, about €15 saved). Rough prices at 20-50 pieces; none of these is decided:

1. **AUX return receivers AD8273 ×2 → op-amp differential receivers** (as channel lever 2): about €9, and one part type fewer to consign.
2. **DG413 ×9 (about €17):** check which switch sections could move to relay contacts already present or to VCA control (as channel lever 3); probably €4-8.
3. Value selection (E24, JLCPCB extended fees) is a standing rule now, not a lever: see "Component values" (decision 134).
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
