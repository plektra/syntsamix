# Master card

KiCad project `master.kicad_pro`: compressor, master section, outputs. Decisions: `docs/decisions/master-card.md` and `master-card-sheets.md` (and `system.md` for the chain). Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

## Sheets and reference prefixes

| Sheet | Scripts | References | Power prefix |
|---|---|---|---|
| Bus summing | `bus_*` | 1xx | 1 |
| AUX return 1 / 2 | `aux_return_*` | 2xx / 3xx | 2 / 3 |
| Compressor | `compressor_*` | 4xx | 4 |
| Sidechain and ducking | `sidechain_*` | 5xx | 5 |
| AUX sends | `aux_sends_*` | 6xx | 6 |
| Master out | `master_out_*` | 701-731 | 7 |
| Headphones | `headphones_*` | 751+ | 0 |
| Master meter | `meter_*` | 8xx | 8 |
| Power | `power_*` | 9xx | 9 |

Power prefixes 0-9 are all used. References stay three digits.

## Working knowledge

- `scripts/rebuild_all.sh` regenerates every sheet with new UUIDs. After rebuilding for one sheet, restore the unchanged sheets and the root with `git checkout -- <files>`, then rerun `check_netlist.py` and ERC, so commits stay focused.
- New sheet: `sch_create_sheet` through `mcpcall.py` (see `build/calls_*_sheet.json`), add `<name>:<power prefix>` to `SHEETS` in `rebuild_all.sh`, write `reference/<name>_title.json`.
- Root sheet pins nobody uses: list them in `scripts/reference/root_nc.json`; `root_links.py` puts no-connect markers on them.
- Shared scripts (`check_netlist.py`, `mcpcall.py`, `post_wired.py`, `fix_paths.py`, `root_links.py`, `schlayout.py`, `make_reference.py`) are symlinks to `hardware/channel-card/scripts/`.
- Power budget: `scripts/power_budget.py [raw volts]` (decision 95). LM317/LM337 need heatsinks of 10 °C/W or better; the heatsinks are live (LM317 tab = +15 V, LM337 tab = raw −20 V), so keep them apart or insulate them.
- Simulations behind the compressor and sidechain: `simulation/compressor/`, `simulation/sidechain/`. The shared op-amp model's 0.69 mA limit is its slew current; the output is a 50 Ω source, so it drives low-ohm loads like SC_ENV's 1.7 kΩ.
- Never hang a resistor (inverter input, divider) on a hold capacitor (C504 in the ducker, the compressor's peak hold): it adds a discharge path and shortens the release. Get the polarity upstream instead (decision 104).
- After `rebuild_all.sh`, restoring the root `master.kicad_sch` from git is safe: the sheet instance paths still resolve (checked with a netlist export, 2026-10-08).
- Raw rails reach the Master out sheet as hierarchical labels from the Power sheet (+20V_RAW, −20V_RAW, decision 128); a new root sheet pin is added by hand in `master.kicad_sch` (copy an existing `(pin ...)` block on a free 2.54 mm slot of the sheet edge), then `root_links.py` (run by `rebuild_all.sh`) labels it.
- Op amp type per reference: `LOWP` in `compressor_wired.py` and `meter_wired.py` lists the TL062 positions (decision 126); add references there, including the temporary multi-unit names (`U9<ref><unit>`).

## Component values and parts (decisions 134, 137)

This board owns its value selection. Choose every resistor and capacitor value from the E24 series (capacitors preferably E12 or E6). Keep a value outside E24 only where the circuit needs a ratio or accuracy that E24 values cannot give, singly or as a pair of E24 parts, and list it with its references and reason in `STATUS.md`, "Component values". Review that list before layout and after any value change. Each value outside the JLCPCB basic library costs a $3 fee per type per order.

Parts (decision 137): for every SMD part JLCPCB places, take a JLCPCB basic part first, then a "preferred" part (no fee), then another LCSC extended part, and a part LCSC does not stock only as a last resort. Another maker's basic part with the same function is fine once its datasheet confirms pinout, package and limits. Record each part that still costs a fee, with its reason, in `STATUS.md`; `python3 tools/costs.py extended` lists them.
