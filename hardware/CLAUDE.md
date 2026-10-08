# Hardware: shared working knowledge

Applies to every board under `hardware/`. Each board folder has its own `CLAUDE.md` (board specifics) and `STATUS.md` (where the board stands, what is next).

## Schematics are scripts

- `<sheet>_build.py` = independent reference netlist, `<sheet>_wired.py` = drawing with real wires (`schlayout.Sheet`). `check_netlist.py` compares them pin by pin; never skip it. Full how-to: `hardware/channel-card/scripts/README.md`. Shared tools live in `hardware/channel-card/scripts/`; the master links to them.
- Rebuilding replaces the whole sheet; edits made by hand in KiCad are lost.
- `mcpcall.py` must run with the Python of the kicad-mcp-pro uv environment (it has the `mcp` package); `rebuild_all.sh` finds it. The KiCad MCP server is registered in Claude Code (profile `schematic_authoring`).
- Rules learned the hard way:
  - Keep resistor/capacitor pin 1 where the reference has it; swap the reference's pin order instead of rotating a part 180°.
  - A wire end on another wire or a pin connects: never cross through endpoints, and split a wire at every pin it should reach.
  - Op-amp symbols: the − input sits at symbol y+2.54 (screen), the + input at y−2.54.
  - KiCad files allow no comments; generated root items are marked by the uuid prefix `c0ffee00`.
  - `sch_create_sheet` numbers every new sheet page 2: `fix_paths.py` renumbers pages and fixes instance paths and project names (otherwise KiCad shows "An error was found when loading the schematic").
  - Multi-unit parts are built with temporary references `U9<3-digit ref><unit>` (units 1-9) and renamed by `post_wired.py`.
  - Duplicate references across sheets are not reported by ERC; `check_netlist.py` checks them.
  - Power flags live only on the power sheet of each project.
  - Diodes at 90/270° render vertical field text; draw them horizontally where text matters.
  - A ground symbol pointing up (rotation 180) puts its "PGND" text on the part it hangs from; tie such pins to a short ground bar with one downward symbol instead.
  - A local label may share a hierarchical label's name on the same sheet; two different names on one net give a multiple_net_names warning.
- Visual check: `kicad-cli sch export svg -o build/svg ../<project>.kicad_sch`, then crop with a small viewBox script and render with `qlmanage -t` (no rsvg/ImageMagick on this Mac). Look at every new sheet before reporting.

## Parts

- Supply budgets: each board has `scripts/power_budget.py`; `tools/system_power_budget.py` adds them up (decision 96). Rerun both after adding or changing parts that draw current, and update `docs/ARCHITECTURE.md` if the totals move.
- Verify every pinout and limit from the maker's datasheet before drawing; record the source in `docs/parts.csv`. Every placed symbol gets the BOM fields in `docs/PART-NUMBERING.md`.
- Custom symbols: `hardware/libs/syntsamix.kicad_sym` (AD8273, SSI2144, SSI2162, AS3046, THAT1646, TPA6120A2).
- Datasheets: `pdftoppm` is not installed, so the Read tool cannot take `pages`; reading a whole PDF works up to about 30 pages. WebFetch often cannot parse TI/ADI PDFs; download with curl and Read the file.
- LCSC stock check: `python3 tools/lcsc_check.py` (the jlcsearch API is flaky; known-good codes are kept in the script).

## Interfaces between boards

`docs/CHAIN.md` (audio and power ribbons) and `docs/INPUT-MODULE.md` (input header) are contracts; `docs/ARCHITECTURE.md` holds the cross-board budgets and invariants. A board session reads them but does not change them: anything that would is noted under "For /system" in the board's `STATUS.md` and settled in a `/system` session.
