# Master card status

Updated 2026-10-10 (second `/board master` session): fee-free parts and E24 values throughout (decisions 144, 146-148), R421 plain 1k (149), expensive ICs hand-soldered on the prototype (150). Earlier 2026-10-10: SC LPF pot RV501 a standard Alpha dual B100K (decision 138). 2026-10-09: RELEASE pot C100K (131); pre-layout decisions 125-128.

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

## Check before layout

- **Chain headers (decision 109; `docs/MECHANICAL.md`):** J101 along the master's left edge, on the underside, long axis front to back, at the distance from the front that the channel card layout records. J901's position is free until the master section is settled.
- **Panel stack (decision 107):** top-side parts ≤ 9.0 mm. Still too tall: U901-U903 TO-220 (about 19.7 mm seated) and the HS901/HS902 heatsinks; placement in `/system mechanical`.
- **Footprints:** D705-D712 `D_SOD-123F` pads are 1.1 mm wide; widen to the maker's 1.5 mm (R+O 1N4007W datasheet Rev 2.0). Würth IDC drill 1.1 mm. R421 next to U402 (a tempco part may return on its pads).
- **Hand-soldered ICs (decision 150):** keep them reachable with an iron (no parts tight against the SOIC/SSOP pins), and mark them in the JLCPCB BOM/CPL export as not placed.
- **Breadboard:** the ducking through the channel's 10 ms smoothing (decision 97); the bottom of the master level pot (about −102 dB, decision 103); the compressor makeup at +22 dB (decision 89); a bipolar-to-ceramic tap test.
- **RoHS strict (decision 116):** every part needs a `RoHS: <source>` in `docs/parts.csv` before ordering (this session's parts all have one); lead-free finish and assembly.
- **Jack sizes (decision 118), panel fixing (decision 120), underside (decision 121):** as the master section decides.
- **Order codes:** RV501 Thonk dual code by analogy (confirm with the order); Tayda A-5370 (RV402) by hand.

## Next

PCB layout, after the SSI2144 breadboard and the channel card layout (`docs/CONTINUE-FROM-HERE.md`). Before it: `/system mechanical` for the master section (heatsinks, meter LED form, rear panel) and the AS3046D declaration.

## Cost-cut levers still open [proposed]

1. **DG413 ×10:** check which switch sections could move to relay contacts already present or to VCA control (as channel lever 3).
2. **Master meter:** 24 discrete 3 mm LEDs against the channel's 0805-under-bezel form (decision 86 against 119).
3. **Bipolar 10 µF → X5R ceramic** (see Open).
4. Not recommended: TPA6120A2 → NE5532 with a discrete buffer (weaker headphone drive); LM339 → LM393 (twice the packages).

## Component values (decision 134)

Values outside E24 after decisions 144, 146 and 147, each with its reason:

| Sheet | Value | References | Reason |
|---|---|---|---|
| AUX returns | 30k1 | R232, R332 | SC_ENV scaling into the virtual earth (decision 97, chain line), as the channel's R217; a change goes through /system |
| Headphones | 39R2 (2512) | R754, R758 | TI's TPA6120A2 output resistor for full level into 32 Ω (decision 94); no fee-free 2512 or 1206 value from 10 to 51 Ω handles about 0.65 W |

Remaining extended SMD types on the master that have no fee-free part: DG413 (hand-soldered here, JLCPCB on the channel), TPA6120A2, OPA2171, LM339, TL062, 10k 0.1 % (SX-R-107, receiver match), 220p C0G, 47n C0G, 10 µF / 47 µF 35 V electrolytics, 30k1, 39R2 2512; `python3 tools/costs.py extended` lists them.

## For /system

- **Master budget after decisions 146 and 148:** typical +15 / −15 V 327 / 256 mA, sizing 570 / 456 mA, worst case 701 / 576 mA (ARCHITECTURE line 49 has 331 / 260 and 576 / 463); rerun `tools/system_power_budget.py` and update the master row and the prototype and full-size totals (a few mA, no budget at risk).
- **RoHS open items (ARCHITECTURE line 93):** drop the end-of-life ERA-V33J102V; R421 is a plain 1k (decision 149) and no board uses it.
- **Master section mechanics:** TO-220 regulators and heatsinks (19.7 mm, ≤ 11.5 °C/W, live tabs); meter LED form (3 mm through the panel vs 0805 under a bezel, decision 86 vs 119).
