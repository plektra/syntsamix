# Input module status

Updated 2026-10-19 (schematic: input header J3 redrawn as the 2x6 box header of decision 181). 2026-10-18 (/system input-cable: header, cable and pinout, decision 181; /cost: IDC flat cable, decision 180). 2026-10-17 (/system: ready-made input cable, decision 179). 2026-10-13 (/system: exhaust slots in the rear strip, decision 167). 2026-10-11 (/system mechanical: decision 160).

- Schematic done, ERC 0/0; the Rean NYS216 jacks J1, J2 stay (decision 132).
- J3 (2026-10-19, decision 181): Adam Tech BHR-12-VUA 2x6 box header (SX-CONN-024) on the stock KiCad parts of the channel card's J1 (`Conn_02x06_Odd_Even`, `IDC-Header_2x06_P2.54mm_Vertical`; the user's choice), pinout as `docs/INPUT-MODULE.md` checked pin by pin in the netlist, DO_L/DO_R no-connect; footprint check in `CHECKLISTS.md`. Estimate €811 / €1,072 / €1,684 at 4 / 8 / 16 channels (was €812 / €1,073 / €1,687).
- Header and cable settled (decision 181, `docs/INPUT-MODULE.md`): Adam Tech BHR-12-VUA 2x6 box header (SX-CONN-024), no latches; cable Würth WR-CAB 12-way (SX-WIRE-006) with two Adam Tech FCS-12-SG sockets (SX-CONN-025), 150 mm, 1:1. Pinout 1 DO_L, 2 AGND, 3 L+, 4 L−, 5-8 AGND, 9 R+, 10 R−, 11 AGND, 12 DO_R (misplug-safe against a 2x4 power socket).
- Cost (2026-10-18): estimate in `CHECKLISTS.md`, Cost-cut levers; the header saving is counted since J3 is on SX-CONN-024 (2026-10-19).
- PCB: not started. Layout per decision 160 (`docs/MECHANICAL.md`, Rear and input module); checks in `CHECKLISTS.md`.

## Next

1. PCB after the channel card PCB (`docs/CONTINUE-FROM-HERE.md`); J3 placed facing forward (`CHECKLISTS.md`).

## For /system

- At layout: report the module's height and whether the rear bottom angle clears the lower jack and slots (decision 167).
