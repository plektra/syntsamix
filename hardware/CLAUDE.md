# Hardware: shared working knowledge

Applies to every board under `hardware/`. Each board folder has its own `CLAUDE.md` (board specifics) and `STATUS.md` (where the board stands, what is next).

## Schematics are scripts

- `<sheet>_build.py` = independent reference netlist, `<sheet>_wired.py` = drawing with real wires (`schlayout.Sheet`). `check_netlist.py` compares them pin by pin; never skip it. Full how-to: `hardware/channel-card/scripts/README.md`. Shared tools live in `hardware/channel-card/scripts/`; the master links to them.
- Rebuilding replaces the whole sheet; edits made by hand in KiCad are lost.
- `mcpcall.py` must run with the Python of the kicad-mcp-pro uv environment (it has the `mcp` package); `rebuild_all.sh` finds it. In an isolated worktree session, shell loops or `$(...)` that pick that Python are refused: find it with `ls -d ~/.cache/uv/archive-v0/*/lib/python*/site-packages/mcp` and call `<env>/bin/python` by its plain path. The KiCad MCP server is registered in Claude Code (profile `schematic_authoring`).
- Rules learned the hard way:
  - Keep resistor/capacitor pin 1 where the reference has it; swap the reference's pin order instead of rotating a part 180°.
  - A wire end on another wire or a pin connects: never cross through endpoints, and split a wire at every pin it should reach.
  - Op-amp symbols: the − input sits at symbol y+2.54 (screen), the + input at y−2.54.
  - KiCad files allow no comments; generated root items are marked by the uuid prefix `c0ffee00`.
  - `sch_create_sheet` numbers every new sheet page 2: `fix_paths.py` renumbers pages and fixes instance paths and project names (otherwise KiCad shows "An error was found when loading the schematic").
  - Multi-unit parts are built with temporary references `U9<3-digit ref><unit>` (units 1-9) and renamed by `post_wired.py`.
  - Duplicate references across sheets are not reported by ERC; `check_netlist.py` checks them.
  - `check_netlist.py` only checks the pins the reference lists: a pin or net dropped from the reference (for example by a stray `#` mid-line) passes unnoticed. Compare the "nets checked" count with the previous run and explain any change.
  - Net names in a reference script must be unique: a new net that reuses an existing name (L_INV for a second stage) merges both in the reference, and `check_netlist.py` reports it as SPLIT. After a reference edit, diff the net names against the committed script's output: a removed name means a dropped pin (a `#` comment pasted mid-line did that once).
  - References made in loops (decoupling caps, LED resistors) never appear as literals in the scripts: find free numbers in the committed `.kicad_sch`, not by searching the scripts.
  - Power flags live only on the power sheet of each project.
  - Diodes at 90/270° render vertical field text; draw them horizontally where text matters.
  - `Device:D` pin 1 is the cathode, pin 2 the anode: read netlists (and write SPICE models from them) with that in mind.
  - Op amps without a KiCad symbol (OPA2171): use `Amplifier_Operational:Opamp_Dual` (same pins and geometry as the TL072) with the part as the value.
  - A ground symbol pointing up (rotation 180) puts its "PGND" text on the part it hangs from; tie such pins to a short ground bar with one downward symbol instead.
  - A local label may share a hierarchical label's name on the same sheet; two different names on one net give a multiple_net_names warning.
- Visual check: `kicad-cli sch export svg -o build/svg ../<project>.kicad_sch`, then crop with a small viewBox script and render with `qlmanage -t` (no rsvg/ImageMagick on this Mac). Look at every new sheet before reporting.

## Parts

- Supply budgets: each board has `scripts/power_budget.py`; `tools/system_power_budget.py` adds them up (decision 96). Rerun both after adding or changing parts that draw current, and update `docs/ARCHITECTURE.md` if the totals move.
- **RoHS is strict (decision 116):** choose a part only when its maker or supplier states RoHS compliance (2011/65/EU with 2015/863), and record the source in the `parts.csv` Notes as `RoHS: <source>`. No statement, no part. Declarations received by email go in `docs/rohs/` (git-ignored: suppliers' documents are not ours to publish in this public repo); `parts.csv` names the document, its date and scope. Standard passives chosen only by value and package get their source when the BOM is fixed (decision 122). Boards are ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; hand soldering uses lead-free solder.
- Verify every pinout and limit from the maker's datasheet before drawing; record the source in `docs/parts.csv`. Every placed symbol gets the BOM fields in `docs/PART-NUMBERING.md`.
- Confirm a part's form (straight or angled, 9 mm or 16 mm, threaded or not) on the maker's drawing, not the shop title: Mouser called the straight Würth 61203421621 "angled", Tayda sells 16 mm horizontal Alpha pots beside the 9 mm ones under similar names, and one LCSC jack had no thread at all; E-Switch 100-series toggles with the right-angle PC termination come standard with the unthreaded B4 bushing (no nut).
- Check that the package of the recorded LCSC code matches the footprint: power D201 carried C22452 (SS54 in SMA) on a D_SMC footprint (decision 159).
- Datasheet routes that work: `pcbparts jlc_get_part` gives an LCSC datasheet URL (datasheet.lcsc.com; when `lcsc.com/datasheet/<file>.pdf` returns HTML, the same file name under `wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/` downloads); Bourns `bourns.com/docs/Product-Datasheets/<series>.pdf`; Würth `we-online.com/components/products/datasheet/<MPN>.pdf`. Vishay `vishay.com/docs/<doc no>/<name>.pdf`. Mouser-hosted PDFs (mouser.com and mouser.fi) are bot-blocked even with a browser user agent, and some maker sites return HTML to curl. To read a drawing, split the page with pypdf and render it with `qlmanage -t -s 1800`; crop with `sips -c`.
- Check sub-agent part reports against the drawing before recording them: pin roles and taper claims have come back wrong.
- Op amps with back-to-back diodes across the inputs (OPA2171 and many bipolar or CMOS parts) do not belong in superdiodes, comparators or other open-loop stages: the diodes conduct and leak current into the circuit (decision 102). The TL072's JFET inputs have none.
- Custom symbols: `hardware/libs/syntsamix.kicad_sym` (AD8273, SSI2144, SSI2162, AS3046, THAT1646, TPA6120A2).
- Datasheets: `pdftoppm` is not installed, so the Read tool cannot take `pages`; reading a whole PDF works up to about 30 pages. WebFetch often cannot parse TI/ADI PDFs; download with curl and Read the file. `pdftotext` is missing too: for text search, install `pypdf` in a temporary venv. TI product pages can disagree with the datasheet table (NE5532: page 4 mA per channel, SLOS075K 6 mA per package): take figures from the datasheet.
- LCSC stock check: `python3 tools/lcsc_check.py` (the jlcsearch API is flaky; known-good codes are kept in the script). When it reports "not found" even for known parts (TL072, LM339), the API is down: check by MPN or LCSC code with `pcbparts jlc_get_part` instead and do not commit `docs/lcsc-check.csv` from that run.
- Lifecycle: check the maker's own end-of-life notices, not only the distributor's status (THAT's 2026-09-01 memo ended the 1606/1646 drivers and its 120x/124x/125x/128x/129x, 1510/1512, 2162/2180/2181, 4305/4315/4320 and 300-series parts).
- Tayda answers 403 to curl and WebFetch: check its listings by hand (its hosted Alpha spec PDFs still download). Thonk sells no C-taper Alpha pots.
- Pot dissipation: Alpha RD901F tracks take 0.02 W in non-B tapers (0.05 W in B): compute it for every pot across a rail (decisions 129, 131). Before changing a resistor in series with a pot, check which end of the control law it sets; scaling the pot and that resistor together keeps the law (decision 131).
- Decision numbers: parallel sessions take numbers before they commit. The same goes for SX part numbers. Before numbering, grep `docs/decisions/INDEX.md` and `docs/parts.csv` in every worktree (`.claude/worktrees/*/`), not only on main.
- TME catalogue (parametric search, parameters, prices and stock, datasheets): `python3 tools/tme.py` (usage in its docstring; credentials in the macOS Keychain, service `tme-api`). Also available: the `pcbparts` MCP server (LCSC parametric search, SamacSys KiCad models as a starting point to check against the maker's drawing, Mouser/DigiKey lookup by MPN)).
- `pcbparts jlc_search`: value filters in kΩ and C0G/NP0 filters can silently return nothing in every class; give resistance in plain ohms ("10000Ohm"), search by maker part number, or list a whole subcategory by package with `library_type: no_fee`. The classes in `docs/lcsc-check.csv` go stale (16k became preferred): recheck before calling a part extended.
- Hand-soldered SMD parts: give the symbol the field Assembly = "hand (decision N)"; `tools/costs.py` then counts that symbol as user-soldered, per symbol, so the same part type can stay JLCPCB-placed on another board.
- Mouser catalogue (keyword and part-number search, stock, price breaks, datasheets; no parametric filters): `python3 tools/mouser.py` (key in the macOS Keychain, service `mouser-api`).

## Interfaces between boards

`docs/CHAIN.md` (audio and power ribbons) and `docs/INPUT-MODULE.md` (input header) and `docs/MECHANICAL.md` (strip envelope, panels, frame) are contracts; `docs/ARCHITECTURE.md` holds the cross-board budgets and invariants. A board session reads them but does not change them: anything that would is noted under "For /system" in the board's `STATUS.md` and settled in a `/system` session.
