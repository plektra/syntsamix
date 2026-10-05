# Channel card sheet generators

The Filter and Level sheets are generated, not hand-drawn. Each `*_build.py` script describes one sheet's symbols, values, part numbers and nets; the KiCad MCP server's `sch_build_circuit` places them and connects every net by label. Edit the script and rebuild when a value changes (for example after the breadboard tests), instead of editing the sheet by hand.

Rebuilding **replaces the whole sheet**. Hand edits made in KiCad are lost.

## Rebuild a sheet

From this folder (needs `uvx`, KiCad 10 and the `mcp` Python package, which the kicad-mcp-pro environment provides):

```sh
python3 filter_build.py                       # writes build/filter.json and build/calls_filter.json
python3 mcpcall.py build/calls_filter.json    # runs sch_build_circuit through kicad-mcp-pro
./post_filter.sh                              # unit refs, power symbols, no-connects, title block, ERC, netlist check
```

```sh
python3 level_build.py
python3 mcpcall.py build/calls_level.json
python3 post_level.py 64.77,372.11 64.77,382.27 180.34,372.11 180.34,382.27   # no-connects on SW201/SW202 pins 3 and 6
python3 fix_paths.py
python3 check_netlist.py level.json
```

Run `mcpcall.py` with the Python from the kicad-mcp-pro uv environment (it has the `mcp` client package).

## What the post-processing does

- **Multi-unit symbols.** The builder cannot place several units of one symbol, so the scripts use temporary references `U9<ref><unit>` (for example `U91042` = U104 unit 2) and the post-step renames them.
- **Power references.** Power symbols get a per-sheet prefix (`#PWR1xx` Filter, `#PWR2xx` Level) so they do not clash with the Input sheet.
- **Power flags.** The builder's PWR_FLAGs are removed; the Input sheet already flags the rails.
- **No-connects and the title block** are added again, since a rebuild wipes them.
- **Hierarchy paths.** `fix_paths.py` rewrites the symbol instance paths to `/<root>/<sheet>`, sets the project name and gives each sheet a unique page number (`sch_create_sheet` numbers every new sheet page 2). Without it the KiCad app reports "An error was found when loading the schematic" and repairs the file itself.
- **Netlist check.** `check_netlist.py` exports the card's netlist and compares every pin with the intended nets. It also lists duplicate references across sheets, which ERC does not report.

## Layout rules learned the hard way

- Keep two-pin parts on the same axis at least about 25 mm apart. Closer, their label stubs touch and short the nets.
- Reference blocks per sheet: Input 1-99, Filter 101-199 (decoupling C191-C206), Level 201-299 (capacitors from C221).
