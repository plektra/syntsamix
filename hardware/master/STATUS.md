# Master card status

Updated 2026-10-10: `/board master` session, SC LPF pot RV501 to a standard Alpha dual B100K (decision 138); non-B pot ratings checked. Before that, 2026-10-09: RELEASE pot to C100K (decision 131). Before that, `/board master` pre-layout session (the user delegated the open points to Claude's recommendation): decisions 89-94 open points confirmed, decisions 125-128 drawn. Rebased on /system decision 124 (Alpha pots RoHS-cleared).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

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

## Open: needs the user or another session

- **Pots:** RoHS cleared by Taiwan Alpha's general declaration (decision 124, /system 2026-10-09) for every standard Alpha model; candidates with order codes in `docs/parts.csv` (SX-POT-004 to -010).
- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **ERA-V33J102V (R421, SX-R-021):** the channel card replaced it with a Vishay TFPT0603L8200FV (820 Ω, +4110 ppm/K, in stock, RoHS) plus 180 Ω in series: 1 k at about +3370 ppm/K (decision 130); the same pair fits here if R421 needs 1 k at about +3300 ppm/K. R421 is End of Life at Mouser with no stock (2026-10-09) and RoHS by exemption; check whether the compressor detector needs exactly 1 k +3300 ppm/K before reusing the pair. The TFPT is Mouser-only (not at LCSC): hand-solder or consign it.
- **Meter LEDs (SX-D-004/005/006):** candidates Kingbright WP710A10LGD/LYD/LID (Mouser). Their body height is unverified, and a 3 mm LED reaching the panel conflicts with the 9 mm top-side rule unless its panel hole is the exception. Settle the form (3 mm or 0805 under a bezel as decision 119) with the master section panel.
- **Ground-lift switch SW901 (SX-SW-002):** part to choose with the rear panel.

## Next

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: `/system mechanical` for the master section (heatsinks, meter LED form, rear panel) and the AS3046D declaration.

## For /system

- **Master section mechanics:** TO-220 regulators and heatsinks (19.7 mm, ≤ 11.5 °C/W, live tabs); meter LED form (3 mm through the panel vs 0805 under a bezel, decision 86 vs 119).
