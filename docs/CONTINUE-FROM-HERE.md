# Continue from here

Session handoff, 2026-10-06. Read `CLAUDE.md` first; this file holds what the other docs do not: where the work stands, what is pending, and the working knowledge behind the scripts.

## Where we are

- Spec complete, decisions 1-94 (`docs/DECISIONS.md`).
- **Channel card schematic complete**: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0/0. Rebuild and check everything with `hardware/channel-card/scripts/rebuild_all.sh`.
- **Master card schematic complete** (`hardware/master`, decisions 87-94): Bus summing, Power, AUX return 1 and 2, Compressor, Sidechain, AUX sends, Master out, Master meter, Headphones. ERC 0/0 (`hardware/master/scripts/rebuild_all.sh`; unused bus-node pins listed in `scripts/reference/root_nc.json`).
- Input module schematic done (`hardware/input-module-6p3`). Power board (`hardware/power`, decision 81) not started.
- Last pushed commit: `6b86189`.

## Next

1. **Recheck the master card power** (decision 87): add up the +15 V, -15 V and +5 V loads of all ten sheets, including the TPA6120A2 (about 30 mA quiescent, peaks of a few hundred mA at full level into 32 ohm), three relay coils (about 27 mA from +15 V) and about 75 LEDs on +5 V (the L7805 draws its current from +15 V). Then size the LM317/LM337/L7805 heatsinks.
2. **Power board** (`hardware/power`, decision 81): choose the isolated DC-DC module family and brick voltage, then draw it.
3. **Channel card PCB layout**, after the breadboard has settled the filter values.

Reference prefixes on the master: Bus 1xx, AUX return 1 2xx, AUX return 2 3xx, Compressor 4xx, Sidechain 5xx, AUX sends 6xx, Master out 701-731, Headphones 751+, Master meter 8xx, Power 9xx (power-symbol prefix 0 for Headphones).

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
