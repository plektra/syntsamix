# Master card

KiCad project `master.kicad_pro`: compressor, master section, outputs. Decisions: `docs/decisions/master-card.md` (and `system.md` for the chain). Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

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
- Simulations behind the compressor and sidechain: `simulation/compressor/`, `simulation/sidechain/`.
