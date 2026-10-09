# Power board

The power input board (decisions 81, 100), next to the master card. Decisions: `docs/decisions/power.md`; chain voltage and power injection are decisions 40 and 80 in `docs/decisions/system.md`; ribbon pinouts in `docs/CHAIN.md`. Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

KiCad project `power.kicad_pro`: 24 V brick in, TPS54560 buck to +20 V and inverting buck-boost to −20 V, three power ribbon headers.

## Sheets and reference prefixes

| Sheet | Scripts | References | Power prefix |
|---|---|---|---|
| Input and clock | `input_*` | 1xx | 1 |
| +20 V buck | `buck_*` | 2xx | 2 |
| −20 V inverter | `inverter_*` | 3xx | 3 |
| Outputs | `outputs_*` | 4xx | 4 |

## Working knowledge

- `scripts/rebuild_all.sh` regenerates every sheet, runs the netlist checks and ERC. On an empty root it first creates the sheets (`sheets.py`).
- `scripts/parts.py` holds each part type's project number, BOM fields and footprint; `scripts/convlib.py` draws the TPS54560 left side shared by the buck and the inverter (pass the IC ground: PGND on the buck, `-20V_CONV` label stubs on the inverter).
- `scripts/design.py` derives every converter value (TI SLVSBN0C, SLVA317B); rerun it after changing a value.
- `scripts/startup_sim.py` is an averaged ngspice model of switch-on (brick ramp, UVLO, soft-start, current limit, rail capacitance, card load) against the brick's overload threshold; rerun it when the rail capacitance, the loads or the start-up ramp change.
- Start-up ramp (C214/D202/D203/R207 and the 3xx twins): 47 nF from the output through a diode into FB slows the start to τ = 240k × 47n; on the inverter it is referred to the IC ground.
- On the inverter the IC ground is the −20 V node: the input ceramics and EN divider from VIN to that node see VIN + 20 V (44.7 V), and the sync capacitor bridges about 20 V (100 V parts).
- Power flags sit where each net starts (PGND and VIN_SW on the input sheet, `-20V_CONV` on the inverter): the whole board is a power board.
- Footprints still to draw at layout (blank footprint field with a note): Kycon KPJX-4S, Bourns SRP1265A.
- Shared scripts are symlinks to `hardware/channel-card/scripts/`.

## Component values and parts (decisions 134, 137)

This board owns its value selection. Choose every resistor and capacitor value from the E24 series (capacitors preferably E12 or E6). Keep a value outside E24 only where the circuit needs a ratio or accuracy that E24 values cannot give, singly or as a pair of E24 parts, and list it with its references and reason in `STATUS.md`, "Component values". Review that list before layout and after any value change. Each value outside the JLCPCB basic library costs a $3 fee per type per order.

Parts (decision 137): for every SMD part JLCPCB places, take a JLCPCB basic part first, then a "preferred" part (no fee), then another LCSC extended part, and a part LCSC does not stock only as a last resort. Another maker's basic part with the same function is fine once its datasheet confirms pinout, package and limits. Record each part that still costs a fee, with its reason, in `STATUS.md`; `python3 tools/costs.py extended` lists them.
