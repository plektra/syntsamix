# Channel card status

Updated 2026-10-10 (/system: decision 152 confirms the MUTE/DUCK button wiring, decision 153 asks for R217 30k; earlier, schematic sessions, delegated by the user: "work autonomously and follow recommendations", then "work on this autonomously"): U303 DG413 (139), all values E24 with fee-free parts (140), temperature compensation to the backlog (141), MUTE/DUCK switched by the buttons (142), TL072 difference receiver (143), trimmers from Mouser, CUTOFF pot from Tayda, breadboard tests 11 and 12. Earlier the same day: fee-free part swaps (decision 137). Before that, 2026-10-09: pots, R184, TFPT tempco, mechanical parts, meter LEDs and power levers (decisions 110-130).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0 errors 0 warnings; every sheet matches its reference netlist.
- 2026-10-08: decisions 97, 98 and 102 drawn (SC_ENV into VSUM through R217; PGND returns for Q301 and the button pull-downs; U204 = OPA2171). The Level control is simulated in `simulation/level/`.
- 2026-10-09, mechanical parts (decisions 110-117): every top-side part now fits the 9 mm limit under the panel. Regulators D²PAK on copper (110); electrolytics SMD at most 5.4 mm (111); trimmers and jumper headers on the underside (112); low-cut caps C0G 1206 (113); pot shaft standard T18 (114); trim stage scaled to a 100 k pot and the pots chosen (115); RoHS strict for every part (116, project-wide); button LEDs and chain headers chosen (117). Sheets rebuilt, netlists match, ERC 0/0.
- 2026-10-09, /system mechanical: 3.5 mm CV jack by the new jack-size rule (118), meter as 0805 LEDs under a printed bezel at 6.0 mm pitch (119), one centred panel screw per end with a printed key (120), underside rules, keep-out and bottom cover (121), RoHS invariant 9 with standard passives at BOM time (122).
- 2026-10-09, schematic: meter LEDs D411-D418 drawn as 0805 (KT-0805G, KT-0805Y, NCD0805R1; decision 119); power levers (decision 123): U107 NE5532 → TL072, meter U401/U404 TL072 → TL062CDR (SX-IC-024). Card load now 113 / 95 mA typical, 229 / 194 mA worst case, sizing 174 / 142 mA. Netlists match, ERC 0/0. RoHS audit of `parts.csv` done (report `docs/reviews/2026-10-09-rohs-audit.md`).
- 2026-10-09, schematic (pots): Alpha MPNs on RV1, RV181, RV301/RV302 (Thonk `-0057` codes); RV183 is SX-POT-012 (Tayda RD901F-40-15K-C10K) in the reference too; R184 10 k → 12 k (SX-R-008) so RV183 stays within Alpha's 0.02 W rating for non-B tapers (decision 129; RD901F spec facts in `parts.csv`). Netlists match, ERC 0/0.
- 2026-10-09, schematic (tempco): R108/R158 Vishay TFPT0603L8200FV (820 Ω, +4110 ppm/K) with new R122/R172 180 Ω in series to AGND replace the end-of-life ERA-V33J102V: 1 k, about +3370 ppm/K (decision 130). Trim pot value text shortened to "50k OFFSET" for room. Netlists match (filter 80 nets), ERC 0/0, sheet looked at.
- 2026-10-10, fee-free parts (decision 137, confirmed by the user): SX-IC-007 TL072 → ST TL072CDT (LCSC C6961, basic; U107, U205, U402, U403), SX-IC-012 78L05 → UTC 78L05G-AB3-R (C71136, basic; U503), SX-D-001 → hongjiacheng BZT52C6V2 (C19077403, preferred; D1-D4), SX-R-011/036/042 → UNI-ROYAL 0805W8F (C17455, C17797, C17818, preferred). Datasheets checked (facts and RoHS sources in `parts.csv`): TL072CDT pinout and limits as TI's, ICC the same, so the power budget is unchanged; 78L05G-AB3-R pins 1 O 2 G 3 I as the KiCad symbol (the -AB3-C-R variant is G I O); BZT52C6V2 SOD-123 matches KiCad `D_SOD-123`. Filter, level, meter and chain sheets rebuilt; netlists match, ERC 0/0. `costs.py extended`: 82 → 80 fee types.
- 2026-10-10, schematic (levers, delegated): U303 is a DG413: PFL L/R on the NO sections 1 and 4, SC send on the NC section 2 driven by SC_OFF from SW302 pin 1 (released = high), R315 moved to pin 1, no part added (decision 139). Values on E24 with JLCPCB basic/preferred UNI-ROYAL parts (decision 140): input trim stage, filter scaling, cutoff summer (R183 = 150k + new R187 12k; RV182 redrawn in the FCV column), fader law (new pairs R207+R223, R208+R224, R213+R225; `simulation/level/` rerun, within 0.4 dB of the design from +10 to −60 dB), SC send 47k, meter ladder (within 0.21 dB). New SX-R-092 to SX-R-106. Reference scripts give the button LEDs their 0805 footprints and part numbers. Netlists match (filter 81, level 44, routing 46 nets), ERC 0/0, changed areas looked at. `tools/costs.py estimate` (4 channels): €1,035 → €963.
- 2026-10-10, schematic (levers, delegated: "work on this autonomously"): TL072 difference receiver with 10k 0.1 % resistors instead of the AD8273 (decision 143; new R19-R26, SX-R-107); MUTE and DUCK switched by the buttons, U206 DG413 and C235/C236 removed, R220/R222 now 100k hold resistors on MUTE_V/DUCK_V with pin 1 open so no contact sequence can short the rail (decision 142, after the architect review); temperature compensation to the backlog, R108/R158 plain 820 Ω (decision 141); trimmers from Mouser, CUTOFF pot from Tayda A-4730. Netlists match (input 46, level 41 nets), ERC 0/0, drawings looked at. Card load 110 / 93 mA typical, sizing 171 / 139 mA. `tools/costs.py estimate` (4 channels): €946 (€1,035 on main before this day's sessions).
- PCB: not started; waits for the breadboard, the SSI2144/SSI2162 RoHS declaration and the cable mock-up.

## Provisional until the breadboard

`simulation/filter/BREADBOARD.md` tests 1-10 set R111/R161 (filter output scale, now 9k1 for the 18k attenuator; scale a breadboard value found with 17.4k by 18/17.4) and R120/R170 (Q current limit, now 36k: about 281 µA maximum with R184 = 12 k, decisions 129 and 140). Keep any new value on E24 or an E24 pair (decision 140). Then edit `filter_wired.py` / `filter_build.py`, run `scripts/rebuild_all.sh`, and update `docs/decisions/channel-card.md`.

## Waiting for the user's confirmation

- **Lever 11, hand-soldering consigned parts:** which of the easy consigned types to hand-solder (estimate in `CHECKLISTS.md`, Cost-cut levers, item 11). The SSI2144 stays with JLCPCB (user, 2026-10-10).
- Decisions 139-143 were made under the user's delegation ("confirmed (delegated)" in `INDEX.md`): review them in `docs/decisions/channel-card.md`.

## Waiting on others

- **Alpha `-0057` suffix (left open by the user 2026-10-09):** the variant code on Thonk's three Alpha order codes is not defined in the RD901F spec; RV183 (Tayda) has none. Check the shaft and knurl of the Tayda RESONANCE pot against the Thonk pots on delivery.
- **RD902F dual specification:** not read yet (the Mouser RD901F PDF is blocked to scripts; the Tayda copy covers the RD901F single); confirm the dual's power rating when it is found.

- **RoHS declaration for the SSI2144 (SX-IC-001) and SSI2162 (SX-IC-002) (decision 122):** no RoHS statement from Sound Semiconductor, Electrokit or the datasheets; requested by the user by email (2026-10-09). Without it they block the PCB order.
- **Knobs:** after the pots (T18 push-on, up to about 19 mm across; for example Thonk Davies 1900H clone, Tall Satin Synthpointer, Mini MXR); need a RoHS source.

## Parts

Chosen (fields on the symbols, sources and RoHS in `docs/parts.csv`): regulators onsemi LM317D2TR4G / LM337D2TR4G; ROQANG SMD electrolytics; Panasonic EEE-1VA100NP bipolar (land pattern checked: size D, KiCad `C_Elec_6.3x5.4`); Murata C0G low-cut caps; Bourns 3296W trimmers; Bourns PTA6043 fader; chain headers Würth 61203421621 (2×17) and 61200821621 (2×4); button LEDs JLCPCB basic 0805 (MUTE red NCD0805R1, PFL yellow KT-0805Y, SC SEND/DUCK/COMP BUS green KT-0805G, LOW-CUT/BYPASS white KT-0805W); CV jack Thonkiconn PJ398SM (decision 118). Printed in-house: button caps, the meter bezel (decision 119) and the 1 mm M6 washer for the CV jack (SX-MECH-004). Supply budget: `scripts/power_budget.py` (rerun after changing parts that draw current).

## Next

First, decision 153 (/system 2026-10-10): redraw R217 30k1 → 30k (SX-R-050, JLCPCB basic) in the level sheet and its reference netlist; rebuild, netlist check, ERC; update `CHECKLISTS.md` (component values) and the 30k1 in `simulation/level/run.py` (rerun; figures move by millivolts).

1. Breadboard the SSI2144 when parts arrive (now with test 11, X5R coupling caps, and test 12, fixed V/oct and drift; buy two LCSC C13585 for test 11) (second Electrokit order on hold: `simulation/filter/electrokit-order-2.csv`). Test 10 (fader law) wants one OPA2171 (SOIC-8, adapter) and one TL072; with two TL072s, skip the 0 % row (`simulation/filter/BREADBOARD.md`).
2. RoHS gaps: SSI2144/SSI2162 declaration (requested, waiting); copy the orderable MPNs the audit checked (NE5532DR, LM339DR, DG413DY-T1-E3, LM13700MX/NOPB) into the MPN column at BOM time. At the next LCSC check run, add SX-R-089 (TFPT, Mouser-only: hand-solder or consign) and SX-R-090 to `docs/lcsc-check.csv` / `tools/lcsc_check.py`.
3. Cable mock-up (decision 109).
4. PCB layout.

## For /system

- Settled by /system 2026-10-10: decision 152 refines 69 (a button pole may switch a DC control voltage when the wiring does not depend on the contact sequence and a smoothing ramp follows; the board already meets both) and confirms the scope wording; the input impedances are in `docs/INPUT-MODULE.md`. Keep conditions (a) and (b) of 152 if MUTE/DUCK are redrawn.

- (none open; decisions 152 and 153 settled the last flags)
