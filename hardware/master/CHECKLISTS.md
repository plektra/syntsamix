# Master card: checklists and reference

Read for layout, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

## Check before layout

- **Chain headers (decision 109; `docs/MECHANICAL.md`):** J101 along the master's left edge, on the underside, long axis front to back, at the distance from the front that the channel card layout records. J901's position is free until the master section is settled.
- **Panel stack (decision 107):** top-side parts ≤ 9.0 mm. Still too tall: U901-U903 TO-220 (about 19.7 mm seated) and the HS901/HS902 heatsinks; placement in `/system mechanical`.
- **Footprints:** D705-D712 `D_SOD-123F` pads are 1.1 mm wide; widen to the maker's 1.5 mm (R+O 1N4007W datasheet Rev 2.0). Würth IDC drill 1.1 mm. R421 next to U402 (a tempco part may return on its pads).
- **Hand-soldered ICs (decision 150):** keep them reachable with an iron (no parts tight against the SOIC/SSOP pins), and mark them in the JLCPCB BOM/CPL export as not placed.
- **Breadboard:** the ducking through the channel's 10 ms smoothing (decision 97); the bottom of the master level pot (about −102 dB, decision 103); the compressor makeup at +22 dB (decision 89); a bipolar-to-ceramic tap test.
- **RoHS strict (decision 116):** every part needs a `RoHS: <source>` in `docs/parts.csv` before ordering (this session's parts all have one); lead-free finish and assembly.
- **Jack sizes (decision 118), panel fixing (decision 120), underside (decision 121):** as the master section decides.
- **Order codes:** RV501 Thonk dual code by analogy (confirm with the order); Tayda A-5370 (RV402) by hand.

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
