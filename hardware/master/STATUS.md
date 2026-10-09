# Master card status

Updated 2026-10-09, `/board master` pre-layout session (the user delegated the open points to Claude's recommendation): decisions 89-94 open points confirmed, decisions 125-128 drawn. Rebased on /system decision 124 (Alpha pots RoHS-cleared).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128).
- 2026-10-09:
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
- **SC LPF pot RV501 (SX-POT-008), dual 100k reverse-log (C).** No T18 source found; a special-order Alpha part needs its own RoHS check (decision 124 covers standard models only); the only lead is Mesa/Boogie 596110 "RD902F C100K dual" (shaft unknown). An A100K dual is not a substitute: RV501 is a rheostat falling CW, so a reversed A law turns the sweep direction round. Options:
  - ask Alpha or a distributor for RD902F-40-15K-C100K;
  - a dual 100k linear pot with a law-bending resistor (redraw);
  - accept CW = lower cutoff with an A100K dual.
- **RELEASE pot RV402 power rating (from `/board channel-card schematic` 2026-10-09, decision 129):** Taiwan Alpha's RD901F specification rates the track at 0.05 W for B taper and only 0.02 W for other tapers (A, C). RV402 (C10K, `compressor_wired.py`; the symbol still says SX-POT-004 while `parts.csv` names the SX-POT-012 part) sits from AGND through R425 620 Ω to −15.1 V: 15.1 V / 10.62 kΩ = 1.42 mA, about 20.2 mW, at the limit (the 2M2 wiper load is negligible). The channel card had the same problem and raised R184 10 k → 12 k (decision 129). Here, raising R425 also moves the RELEASE range (44 ms to 1.4 s per 10 dB), so it needs a recheck of the release law; for example 1.5 k gives about 17 mW. Also check the other non-B master pots (SX-POT-005 to -010) against 0.02 W, and point RV402's ProjectPN at SX-POT-012.
- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **ERA-V33J102V (R421, SX-R-021):** the same tempco resistor as the channel card. The RoHS audit lists it as End of Life at Mouser and RoHS by exemption. It affects the master's compressor detector too: choose a replacement together with the channel card.
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

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: `/system mechanical` for the master section (heatsinks, meter LED form, rear panel), the RV501 pot, and the AS3046D declaration.

## For /system

- **Budgets after decisions 125-128 (2026-10-09):**
  - master typical 331 / 260 mA (was 340 / 269), worst case 701 / 576 mA (was 719 / 594), sizing 576 / 463 mA (was 589 / 476);
  - prototype sizing 1.27 / 1.03 A, 46 W (was 1.28 / 1.04 A, 47 W);
  - full size sizing 3.36 / 2.73 A (was 3.37 / 2.75 A); ribbon per pin unchanged.
  - Update the `docs/ARCHITECTURE.md` power table (`tools/system_power_budget.py`).
- **Master section mechanics:** TO-220 regulators and heatsinks (19.7 mm, ≤ 11.5 °C/W, live tabs); meter LED form (3 mm through the panel vs 0805 under a bezel, decision 86 vs 119).
- **`docs/ARCHITECTURE.md` text:** the system diagram (line 12, "main out (THAT1646)") and the RoHS open item (THAT1646 End of Life) predate decision 125: change to DRV135 and drop the End of Life item. The architect review could not run at handoff (account spend limit); run it at the start of the `/system` session on this commit.
- **RoHS open items:** the ERA-V33J102V is also on the master (R421), not only the channel card, as the audit lists it. THAT1646 End of Life closed by decision 125.
