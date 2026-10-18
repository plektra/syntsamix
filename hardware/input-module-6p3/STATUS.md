# Input module status

Updated 2026-10-18 (/system input-cable: header, cable and pinout, decision 181; /cost: IDC flat cable, decision 180). 2026-10-17 (/system: ready-made input cable, decision 179). 2026-10-13 (/system: exhaust slots in the rear strip, decision 167). 2026-10-11 (/system mechanical: decision 160).

- Schematic done, ERC clean, but with the old 1×10 KK 254 header J3; the Rean NYS216 jacks J1, J2 stay (decision 132).
- Header and cable settled (decision 181, `docs/INPUT-MODULE.md`): Adam Tech BHR-12-VUA 2x6 box header (SX-CONN-024), no latches; cable Würth WR-CAB 12-way (SX-WIRE-006) with two Adam Tech FCS-12-SG sockets (SX-CONN-025), 150 mm, 1:1. Pinout 1 DO_L, 2 AGND, 3 L+, 4 L−, 5-8 AGND, 9 R+, 10 R−, 11 AGND, 12 DO_R (misplug-safe against a 2x4 power socket).
- Cost (2026-10-18): estimate in `CHECKLISTS.md`, Cost-cut levers; the header saving counts once J3 is redrawn on SX-CONN-024.
- PCB: not started. Layout per decision 160 (`docs/MECHANICAL.md`, Rear and input module); checks in `CHECKLISTS.md`.

## Next

1. `/board input-module-6p3 schematic`: replace J3 with a 2x6 symbol (SX-CONN-024) on the pinout of decision 181 through the KiCad MCP server, footprint checked against the Adam Tech drawing (outer 22.86 × 8.80 mm, key slot on the odd-pin side), facing forward; run ERC.
2. PCB after the channel card PCB (`docs/CONTINUE-FROM-HERE.md`).

## For /system

- At layout: report the module's height and whether the rear bottom angle clears the lower jack and slots (decision 167).
