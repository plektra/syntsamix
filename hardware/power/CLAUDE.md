# Power board

The power input board (decision 81), next to the master card. Decisions: `docs/decisions/power.md`; chain voltage and power injection are decisions 40 and 80 in `docs/decisions/system.md`; ribbon pinouts in `docs/CHAIN.md`. Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

No KiCad project yet. When creating it, follow the master card's setup (`hardware/master/CLAUDE.md`): `scripts/` with `_build.py` / `_wired.py` per sheet and symlinks to the shared tools in `hardware/channel-card/scripts/`.
