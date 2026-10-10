# Master card status

Updated 2026-10-10 (/system: decision 153 asks for R232/R332 30k; before that the second `/board master` session): fee-free parts and E24 values throughout (decisions 144, 146-148), R421 plain 1k (149), expensive ICs hand-soldered on the prototype (150). Earlier 2026-10-10: SC LPF pot RV501 a standard Alpha dual B100K (decision 138). 2026-10-09: RELEASE pot C100K (131); pre-layout decisions 125-128.

Reference lists: `CHECKLISTS.md` (checks before layout and on delivery, cost-cut levers, component values; decision 151).

## Where it stands

- Schematic complete: ten sheets, every netlist check 0 problems, ERC 0 errors 0 warnings (decisions 87-95, 103, 104, 125-128, 131, 138, 144, 146-150). Net counts: AUX returns 73, compressor 83, sidechain 55, AUX sends 37, master out 63, meter 83.
- 2026-10-10 (this session; details in the decision files):
  - Fader laws (AUX returns, master level) on the channel's E24 values and pairs (decision 144); single E24 values were simulated and rejected (up to 6.7 dB off near the bottom).
  - Meter ladder fee-free E24 at about 0.45 mA, thresholds within 0.14 dB; R732 22k + R737 560R (decision 146).
  - Compressor R420 510k + 51k, R426 120k + 20k, GR ladder 470k / 4k3; SC LPF C503 + C521 2 × 47n C0G (sweep 44-478 Hz, Q 0.707); TL072 symbols ST TL072CDT (decision 147).
  - AUX return receivers TL072 difference amplifiers with 10k 0.1 % (decision 148); the AD8273 is gone from the project.
  - R421 a plain 1k 0805 (decision 149); compressor temperature compensation in the backlog (threshold drifts about 2 dB over 15-45 °C, simulated).
  - DG413 ×10, SSI2162 ×4, DRV135UA ×2 and AS3046D carry Assembly = "hand (decision 150)": the user solders them on the one master; potential single point of failure, in the backlog.
  - Part swaps (decision 137): button LEDs on the per-colour basic parts (MUTE red; DUCK, COMP BUS, COMP ON, SC BUS green; SC LPF BYPASS white; SC LISTEN yellow); D504 BAT54W; D705-D712 1N4007W SOD-123FL; U641 DG411 → DG413 with a Q601 inverter (R612, R613) making MONO1 for send 1; Q601's emitter on PGND (invariant 4; the architect review flagged AGND, the user chose PGND).
  - Power budget: typical 327 / 256 mA, worst case 701 / 576 mA, sizing 570 / 456 mA; heatsinks still ≤ 11.5 °C/W.
  - Cost (`tools/costs.py`): estimate €794 / €1,074 / €1,671 for 4 / 8 / 16 channels before VAT and shipping; 38 extended or consigned SMD types system-wide, about €105 in fees per order (70 and €193 at the start of the session).
- Earlier: decisions 125-128 and 131 (2026-10-09), 97, 98, 103, 104 (2026-10-08), 138 (2026-10-10).
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

Decision 153 (/system 2026-10-10): redraw R232 and R332 30k1 → 30k (SX-R-050, JLCPCB basic) on the AUX returns sheet and its reference netlist; rebuild, netlist check, ERC; drop 30k1 from the extended list in `CHECKLISTS.md`; change 30k1 in `simulation/sidechain/run.py` and its `README.md`, rerun to refresh `results.txt` (figures move by millivolts).

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: `/system mechanical` for the master section (heatsinks, meter LED form, rear panel) and the AS3046D declaration.

## For /system

- **Master section mechanics:** TO-220 regulators and heatsinks (19.7 mm, ≤ 11.5 °C/W, live tabs); meter LED form (3 mm through the panel vs 0805 under a bezel, decision 86 vs 119).
