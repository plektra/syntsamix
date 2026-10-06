# Continue from here

Session handoff, 2026-10-06. Read `CLAUDE.md` first; this file holds what the other docs do not: where the work stands, what is pending, and the working knowledge behind the scripts.

## Where we are

- Spec complete, decisions 1-95 (`docs/DECISIONS.md`).
- **Channel card schematic complete**: Input, Filter, Level, Routing, Meter, Chain and power. ERC 0/0. Rebuild and check everything with `hardware/channel-card/scripts/rebuild_all.sh`.
- **Master card schematic complete** (`hardware/master`, decisions 87-95): Bus summing, Power, AUX return 1 and 2, Compressor, Sidechain, AUX sends, Master out, Master meter, Headphones. ERC 0/0 (`hardware/master/scripts/rebuild_all.sh`; unused bus-node pins listed in `scripts/reference/root_nc.json`).
- Input module schematic done (`hardware/input-module-6p3`). Power board (`hardware/power`, decision 81) not started.
- Last pushed commit: see `git log -1` (master card complete with the power recheck, decision 95).

## Next

1. **Master card power recheck**: done (decision 95, `hardware/master/scripts/power_budget.py`): heatsinks of 10 °C/W or better on the LM317 and LM337. Power board load: about 2.4 to 2.8 A per rail.
2. **Power board** (`hardware/power`, decision 81; spec section 2 line "DC-DC module chosen from a family ... supply rating for 16 cards is open"): choose the isolated DC-DC module family and the brick voltage (24 or 48 V), then draw it. Inputs: about 2.4 to 2.8 A per rail at ±20 V for 16 channel cards plus the master (about 100 to 115 W); the raw rails must stay above about 19 V under load because the master's relay drop-out comparator trips at 17.9 V and the LM317 needs about 2 V headroom; LC filter after the module; fuse, reverse-polarity protection, power switch and LED, locking DC jack; ribbons to both chains and the master (decisions 80, 81).
3. **Channel card PCB layout**, after the breadboard has settled the filter values.

Reference prefixes on the master: Bus 1xx, AUX return 1 2xx, AUX return 2 3xx, Compressor 4xx, Sidechain 5xx, AUX sends 6xx, Master out 701-731, Headphones 751+, Master meter 8xx, Power 9xx (power-symbol prefix 0 for Headphones).

## Proposals waiting for the user's confirmation (marked **[proposed]** in DECISIONS.md)

- 89: Q5 of the AS3046D unused; makeup reaches +22 dB at full AMOUNT (2 dB past the SSI2162's +20 dB spec), check on the breadboard.
- 90: a silent patched EXT cable still selects EXT; no separate EXT LED.
- 91: no output coupling capacitors on the AUX sends.
- 92: only the positive raw rail is monitored for relay drop-out.
- 93: master meter colours (green -30 to 0, yellow +3 to +9, red +12 and clip).
- 94: headphone gain 2; cue arrives inverted relative to main; PFL LED yellow.
- 72: SC_ENV scale +1 V = 10 dB of ducking.
- Also to check before layout: the G6K NC/NO contact assignment against Omron's terminal diagram (taken from KiCad's G6K-2 symbol); the dual 100 kΩ reverse-log (C) pot for the sidechain LPF may not exist in Alpha's range.

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
- LCSC stock check: `python3 tools/lcsc_check.py` (the public jlcsearch API is flaky; known-good codes are kept in the script). Not yet rerun for the master card parts.
- Master card specifics:
  - `rebuild_all.sh` regenerates every sheet with new UUIDs. After rebuilding for one sheet, restore the unchanged sheets and the root with `git checkout -- <files>` and rerun `check_netlist.py` and ERC, so commits stay focused.
  - New sheet: `sch_create_sheet` through `mcpcall.py` (see `build/calls_*_sheet.json`), add `<name>:<power prefix>` to `SHEETS` in `rebuild_all.sh`, write `reference/<name>_title.json`. Power prefixes 0-9 are all used on the master (Headphones uses 0). Temporary unit references must be `U9<3 digits><unit>`, so references stay three digits.
  - A local label may share a hierarchical label's name on the same sheet (no warning); two different names on one net give a multiple_net_names warning.
  - Root pins nobody uses: list them in `scripts/reference/root_nc.json`; `root_links.py` puts no-connect markers on them.
  - Custom symbols added this session to `hardware/libs/syntsamix.kicad_sym`: AS3046 (4 units), THAT1646, TPA6120A2.
- Visual check: `kicad-cli sch export svg -o build/svg ../master.kicad_sch`, then crop and render with a small viewBox script plus `qlmanage -t` (no rsvg/ImageMagick on this Mac). Look at every new sheet before reporting.
- Datasheets: `pdftoppm` is not installed, so the Read tool cannot take `pages`; reading a whole PDF works for short datasheets (up to about 30 pages). WebFetch often cannot parse TI/ADI PDFs; download with curl and Read the file instead.
- Simulations: `simulation/compressor/run.py` (detector, gain computer) and `simulation/sidechain/run.py` (LPF, ducker) share a TL072-like op-amp model. ngspice `.measure` needs `.save v(node)` for AC analyses, and `vm()`/`vdb()` give a harmless parse warning.

## How the user likes to work

- Commit and push only when asked; pause for review before each commit.
- Give a recommendation with alternatives; one topic at a time; tight budget (flag cost-cut candidates).
- Mark proposals as proposed until confirmed; ask before changing a confirmed decision.
