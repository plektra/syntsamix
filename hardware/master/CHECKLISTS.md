# Master card: checklists and reference

Read for layout, assembly, cost and value work; the session state is in `STATUS.md` (decision 151).

## Check before layout

- **Chain headers (decisions 109, 175; `docs/MECHANICAL.md`):** J101 (audio, 2×17) near the master's left edge, on the underside, on the channel cards' header line: same distance from the front as the channel card layout records, long axis front to back, pin 1 toward the front, key on the same side as the cards. The audio section's right end socket plugs in there; no mock-up, the end-segment length is set at the channel card layout. Keep the underside band around J101 free as on the cards (header length plus 15 mm front and back, decision 175). J901 (power, 2×4) keeps its own two-socket ribbon from the power board: its position is free, placed with the master section.
- **Rear ribbons (decision 163):** J903 pin 25 (lift return) on its own trace straight to the star point NT901, not through the AGND pour; CHASSIS (pin 26) next to J902, R905 and C913. J603/J903 key slots and pin 1 to match the row boards (conductor n = pin n at both ends); measure the cable length at the first fit (no mock-up, decision 175).
- **Panel stack (decision 107):** top-side parts ≤ 9.0 mm. U901-U903 (TO-220) go on the underside (`docs/MECHANICAL.md`, Master section): U901/U902 on HS901/HS902 Wakefield 637-10ABPE, 25.4 mm below the PCB plus 3 mm to the cover (decision 174; the enclosure depth is a `/system` item, `MECHANICAL.md` still allows 25 mm); U903 L7805 without a heatsink. Heatsink footprint (two pins at 25.4 mm pitch) from the Wakefield drawing. Live tabs (+15 V, raw −20 V): heatsinks ≥ 3 mm from each other, the frame and the cover, or on insulating pads (decision 95).
- **Footprints:** D705-D712 `D_SOD-123F` pads are 1.1 mm wide; widen to the maker's 1.5 mm (R+O 1N4007W datasheet Rev 2.0). Würth IDC drill 1.1 mm. R421 next to U402 (a tempco part may return on its pads).
- **Headphone jack (decision 169):** J751 (KK 1x3) near the NYS230 cutout, at least about 90 mm behind the front edge; pin 1 tip, 2 ring, 3 sleeve. The cutout clears the NYS230 body (depth measured on the sample). Bezel windows for the 0805 meter, GR and PFL LEDs (decision 170) placed with the panel artwork.
- **Back-to-back pairs (decision 172):** place each pair's two CP_Elec_5x5.4 side by side with a short − to − link; DRV135 sense pairs C707/C728 … C710/C731 next to U703/U704.
- **Hand-soldered ICs (decision 150):** keep them reachable with an iron (no parts tight against the SOIC/SSOP pins), and mark them in the JLCPCB BOM/CPL export as not placed.
- **Breadboard:** the ducking through the channel's 10 ms smoothing (decision 97); the bottom of the master level pot (about −102 dB, decision 103); the compressor makeup at +22 dB (decision 89); the back-to-back 10 µF pairs (decision 172) ride on the channel's breadboard test 11 (pair against a bipolar at low frequency).
- **RoHS strict (decision 116):** every part needs a `RoHS: <source>` in `docs/parts.csv` before ordering (this session's parts all have one); lead-free finish and assembly.
- **Jack sizes (decision 118), panel fixing (decision 120), underside (decision 121):** as the master section decides.
- **Order codes:** RV501 Thonk dual code by analogy (confirm with the order); Tayda A-5370 (RV402) by hand.

## Cost-cut levers still open [proposed]

1. Done: AUX return MUTE and DUCK on the buttons (decision 177), DG413 ×10 → ×8. The other eight switch audio or are driven by logic or comparators; no relay has a spare contact on a switched signal.
2. Done: master meter, GR and PFL LEDs 0805 (decisions 162, 170, drawn 2026-10-13).
3. Done: the 16 bipolar 10 µF are back-to-back ROQANG pairs (decision 172), nothing consigned; the X5R ceramic option was dropped as on the channel (dearer than the pair, microphonics).
4. Not recommended: TPA6120A2 → NE5532 with a discrete buffer (weaker headphone drive); LM339 → LM393 (twice the packages).

## Component values (decision 134)

Values outside E24 after decisions 144, 146, 147 and 153, each with its reason:

| Sheet | Value | References | Reason |
|---|---|---|---|
| Headphones | 39R2 (2512) | R754, R758 | TI's TPA6120A2 output resistor for full level into 32 Ω (decision 94); no fee-free 2512 or 1206 value from 10 to 51 Ω handles about 0.65 W |

Remaining extended SMD types on the master that have no fee-free part: DG413 (hand-soldered here, JLCPCB on the channel), TPA6120A2, OPA2171, LM339, TL062, 10k 0.1 % (SX-R-107, receiver match), 220p C0G, 47n C0G, 10 µF / 47 µF 35 V electrolytics, 39R2 2512; `python3 tools/costs.py extended` lists them.

Fee-free part swaps already drawn (decision 137, 2026-10-10): button LEDs on the per-colour basic parts (MUTE red; DUCK, COMP BUS, COMP ON, SC BUS green; SC LPF BYPASS white; SC LISTEN yellow); D504 BAT54W; D705-D712 1N4007W SOD-123FL; U641 DG411 → DG413 with a Q601 inverter (R612, R613) making MONO1 for send 1, Q601's emitter on PGND (invariant 4; the user chose PGND over the architect's AGND). R232/R332 30k1 → 30k (decision 153; SX-R-087 no longer used).

## Checks on delivery

- **Rean NYS216 sample:** height above the board (at most about 17 mm for the flat row boards, decision 162), height to the bushing centre, bushing length past the housing; pin roles with a meter against the footprint (decision 132).
- **Rean NYS230 sample:** depth behind a 1.6 mm panel (about 30 mm assumed, decision 162) and pin roles (decision 169).
- **Molex 217797-1031 lead:** pin order of the free ends (decision 169).
