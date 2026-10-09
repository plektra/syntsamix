# Input module (6.3 mm)

KiCad project `input-module-6p3.kicad_pro`: the passive input module with the channel's 6.3 mm jacks. Decisions: `docs/decisions/input-module.md`. Interface (10-pin header, a contract with the channel card): `docs/INPUT-MODULE.md`. Shared workflow: `hardware/CLAUDE.md`. Status: `STATUS.md`.

This schematic was drawn before the script workflow; it has no generator scripts. Edit it through the KiCad MCP server and run ERC.

## Component values and parts (decisions 134, 137)

This board owns its value selection. Choose every resistor and capacitor value from the E24 series (capacitors preferably E12 or E6). Keep a value outside E24 only where the circuit needs a ratio or accuracy that E24 values cannot give, singly or as a pair of E24 parts, and list it with its references and reason in `STATUS.md`, "Component values". Review that list before layout and after any value change. Each value outside the JLCPCB basic library costs a $3 fee per type per order.

Parts (decision 137): for every SMD part JLCPCB places, take a JLCPCB basic part first, then a "preferred" part (no fee), then another LCSC extended part, and a part LCSC does not stock only as a last resort. Another maker's basic part with the same function is fine once its datasheet confirms pinout, package and limits. Record each part that still costs a fee, with its reason, in `STATUS.md`; `python3 tools/costs.py extended` lists them.
