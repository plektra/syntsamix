# Master card status

Updated 2026-10-10 (third `/board master` session: R232/R332 30k drawn, decision 153).

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128, 131, 138, 144, 146-150, 153). Net counts: AUX returns 73, compressor 83, sidechain 55, AUX sends 37, master out 63, meter 83.
- Values E24 and parts fee-free wherever one fits (decisions 144, 146-149, 153; exceptions and drawn swaps in `CHECKLISTS.md`); DG413, SSI2162, DRV135UA and AS3046D hand-soldered on the prototype (150).
- Power budget: typical 327 / 256 mA, worst case 701 / 576 mA (`ARCHITECTURE.md`); heatsinks ≤ 11.5 °C/W.
- Cost (`tools/costs.py estimate`, 2026-10-11 after the power board decisions 156-159, the GPBS850L price, the JLCPCB fee model fix and Thonk volume breaks): €778 / €1,040 / €1,600 for 4 / 8 / 16 channels before VAT and shipping; 28 fee types system-wide, billed per design as 38 at $3.07. Series of 8-channel mixers: `tools/costs.py sets`. Economic PCBA assumed (conditions in `hardware/CLAUDE.md`, Parts).
- `simulation/sidechain` reflects the 30k loads (1.667 kΩ); results unchanged.
- 2026-10-10, button MPN corrected: SX-SW-001 is CW GPBS850L (latching, Electrokit 41012905); GPBS850N, recorded until now, is the momentary twin. MPN, footprint `SW_Latching_8.5x8.5mm_CW_GPBS850L` (same geometry per datasheet Rev 2), parts.csv and prices.csv changed; erratum on decision 75; no wiring change, ERC 0/0. Estimate €769 / €1,037 / €1,609 for 4 / 8 / 16 channels.
- PCB: not started.

## Waiting for the user's confirmation

- Decision 147 was made under the user's delegation of minor changes ("ask me only about major changes"): review the compressor pairs, the GR LED shift (at most 0.2 dB) and the SC LPF sweep (3-6 % lower).

## Open: needs the user or another session

- **AS3046D RoHS declaration:** requested by the user (2026-10-09), waiting.
- **Meter LEDs (SX-D-004/005/006):** form (3 mm or 0805 under a bezel as decision 119) settled with the master section panel.
- **Ground-lift switch SW901 (SX-SW-002):** part to choose with the rear panel.
- **Bipolar 10 µF ×16 (SX-C-023, consigned) → X5R ceramic:** waits for a breadboard tap test (user, 2026-10-10); touches decision 127.
- **Fee types shared with the channel** (220p C0G, TL062, LM339): only go away if both boards change; noted in `hardware/channel-card/STATUS.md`. Checked and dropped: OPA2171 → LM358 (onsemi LM358/D Rev. 27) and ceramic LM337 output capacitors (onsemi LM337/D Rev. 11 p. 7, can oscillate).

## Next

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: `/system mechanical` for the master section (heatsinks, meter LED form, rear panel) and the AS3046D declaration.

## For /system

- **Master section mechanics:** TO-220 regulators and heatsinks (19.7 mm, ≤ 11.5 °C/W, live tabs); meter LED form (3 mm through the panel vs 0805 under a bezel, decision 86 vs 119).
