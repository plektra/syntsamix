# Continue from here

Session handoff, 2026-10-06. Read `CLAUDE.md` first; this file holds what the other docs do not: where the work stands, what is pending, and the working knowledge behind the scripts.

## Where we are

- Spec complete, decisions 1-91 (`docs/DECISIONS.md`).
- **Channel card schematic complete**: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0/0. Rebuild and check everything with `hardware/channel-card/scripts/rebuild_all.sh`.
- **Master card schematic in progress** (`hardware/master`): Bus summing, Power, AUX return 1 and 2, Compressor, Sidechain, AUX sends done (`hardware/master/scripts/rebuild_all.sh`). Remaining ERC items are Bus summing outputs that later sheets will use.
- Input module schematic done (`hardware/input-module-6p3`). Power board (`hardware/power`, decision 81) not started.
- Last pushed commit: `6b86189`.

## Next: remaining master card sheets

Reference prefixes so far: Bus 1xx, AUX return 1 2xx, AUX return 2 3xx, Compressor 4xx, Sidechain 5xx, AUX sends 6xx, Power 9xx. Suggested order and notes (specs in `docs/SPEC.md` section 4):

1. **Compressor** (4xx): done (decision 89, `simulation/compressor/`). Its detector input is SC_DET: the filtered sidechain after the source switch and LPF, at low impedance, with INT = (COMP_L + COMP_R)/2 at unity so the threshold (+14.6 dBu sine peak at AMOUNT 0) refers to the bus level.
2. **Sidechain and ducking** (5xx): done (decision 90, `simulation/sidechain/`).
3. **AUX sends** (6xx): done (decision 91).
4. **Master out** (7xx): MAIN_L/R_SUM in, master level pot driving an SSI2162 VCA, soft clip (same onset as the channels, about +14 dBu), THAT1646S08 balanced drivers (decision 83; pinout to verify; cost-cut fallback NE5532 buffer + inverter), Omron G6K-2F-Y DC12 relays (decision 85; coil/contact data to verify) with 2 s power-up delay and instant drop-out when the incoming raw rail drops.
5. **Master meter** (8xx): 12 segments per side, -30 -20 -15 -10 -6 -3 0 +3 +6 +9 +12 clip (0 = +4 dBu, clip about +17 dBu), round 3 mm LEDs (decision 86), same detector/LM339 approach as the channel meter.
6. **Headphones**: main normally, cue when PFL_ACT is low; TPA6120A2 (decision 84; pinout and thermal pad to verify), dual-gang volume pot, 6.3 mm jack, PFL-active LED, relay in series.

After the master card: recheck the master's rail currents and regulator heat (decision 87), then the power board (choose the isolated DC-DC module and brick voltage).

## Pending outside the schematics

- **Breadboard** (`simulation/filter/BREADBOARD.md`): parts ordered, not arrived. Tests 1-10 set the provisional values R111/R161 (filter output scale) and R120/R170 (Q current limit); then edit `filter_wired.py`/`filter_build.py` and run `rebuild_all.sh`.
- **Second Electrokit order on hold**: `simulation/filter/electrokit-order-2.csv` (LM13700N, 1N4148, 6.8 nF, breadboard, TL072, 10 GPBS850N switches).
- **Parts still to choose**: resonance pot (10k reverse audio), CV jack (vertical 6.3 mm), meter and button LED parts and colours, IDC headers, ground-lift switch, CUTOFF/level pot MPNs.
- **Backlog** is in `docs/ROADMAP.md` (includes the 3D-printed LED bar diffuser and cost-cut candidates).

## Working knowledge (the scripts README has the full how-to)

- Sheets are scripts: `<sheet>_build.py` = independent reference netlist, `<sheet>_wired.py` = drawing with real wires. `check_netlist.py` compares them pin by pin; never skip it. Shared tools live in `hardware/channel-card/scripts/`; the master links to them.
- `mcpcall.py` must run with the Python of the kicad-mcp-pro uv environment (it has the `mcp` package); `rebuild_all.sh` finds it. The KiCad MCP server itself is registered in Claude Code (profile `schematic_authoring`).
- Rules learned the hard way:
  - Keep resistor/capacitor pin 1 where the reference has it; swap the reference's pin order instead of rotating a part 180°.
  - A wire end on another wire or a pin connects: never cross through endpoints.
  - KiCad files allow no comments; generated root items are marked by the uuid prefix `c0ffee00`.
  - `sch_create_sheet` numbers every new sheet page 2: `fix_paths.py` renumbers pages and fixes instance paths and project names (otherwise the KiCad app shows "An error was found when loading the schematic").
  - Duplicate references across sheets are not reported by ERC; `check_netlist.py` checks them.
  - Power flags live only on the power sheet of each project.
  - Field text: diodes at 90/270° render vertical text; draw them horizontally where text matters.
- Part facts: verify every pinout from the maker's datasheet before drawing (CLAUDE.md rule 8); record the source in `docs/parts.csv`.
- LCSC stock check: `python3 tools/lcsc_check.py` (the public jlcsearch API is flaky; known-good codes are kept in the script).

## How the user likes to work

- Commit and push only when asked; pause for review before each commit.
- Give a recommendation with alternatives; one topic at a time; tight budget (flag cost-cut candidates).
- Mark proposals as proposed until confirmed; ask before changing a confirmed decision.
