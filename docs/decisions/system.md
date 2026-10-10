# System and chain decisions

System scope, signal levels, buses, cross-board functions and the chain between cards (audio and power ribbons, grounding). Project-wide rules (118, 122, 132, 135) are in `system-rules.md`.

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (figures, sources, rationale, rejected options) is in `record/system.md` under the same number; read it when a figure or source is needed or before reopening a decision. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

1. Pro audio mixer for synthesizers and instruments in electronic music live performances
2. Modular by design
3. Prototype: 4 stereo channels
13. The compressor processes a dedicated compressor bus; each channel assigns to main or compressor bus (the kick stays on main and keys the compressor)
14. AUX sends and returns are stereo by default and mono-capable
25. Inputs take hot Eurorack levels (up to ±12 V peak) as well as line levels, with no external attenuator
27. Channel inputs are 2× 6.3 mm TRS (L/MONO, R); jack size by function is now item 118
28. PFL per channel (post-filter, pre-fader, pre-mute) onto a stereo cue bus; headphones switch to cue while any PFL is active; PFL-active LED. No solo-in-place (an accidental press would silence the main mix)
30. Channel cards are added one at a time; no card depends on another
32. Budget relatively tight: prefer cost-effective parts where the audible difference is small (made precise by 135)
34. Chainable bus from the start, no fixed slot count (form: 38)
38. Chain per card: identical IN and OUT connectors wired straight through, short ribbons to the neighbour, master at one end; no backplane
39. Practical maximum: 16 channel cards
40. Chain power: unregulated about ±20 V nominal; each card regulates its own ±15 V; audio ground and power ground on separate conductors
41. Separate ribbons: 34-pin IDC audio (buses, logic lines, interleaved audio grounds, spares) and keyed 8-pin IDC power (2× V+, 2× V−, 4× ground). No 10- or 16-pin sizes, so a Eurorack power cable cannot be plugged in
42. Chain pinouts, signals and grounding rules as in `CHAIN.md`; the sidechain bus is mono. Power enters at the power board (80, 81); the master card's star point is the only AGND-PGND join
46. Batch: analog path; +4 dBu nominal, about +20 dBu internal maximum, +24 dBu only at balanced outputs; targets in `SPEC.md` section 5; DC-coupled receivers with about 3 Hz AC coupling after them; click-free mute via the VCA; fader bottom takes the VCA past −100 dB; sidechain LPF 40-500 Hz, 12 dB/oct, with bypass; channel independence (identical slots, master-side bus summing, wired-OR logic, no shared parts, per-card regulation); master level through an SSI2162 and a linear pot; headphone volume knob; balanced outputs on 6.3 mm TRS; unregulated about ±20 V chain supply
61. Grounding: jack sleeves to their card's AGND; FR4 panels isolate jacks from the frame; frame bonded to the master's star point only, through a ground-lift switch (RC when lifted). Chain connectors: 2.54 mm shrouded keyed box headers (2×17, 2×4), 28 AWG IDC ribbon
64. Soft clipping after each channel's trim stage and on the master bus output, onset about +14 dBu (6 dB below the internal maximum)
66. Sidechain ducking through the channel VCAs: the master turns the filtered sidechain into the envelope SC_ENV (THRESHOLD, DEPTH, DECAY; fast fixed attack); a DUCK button on each channel and AUX return adds it to that VCA's control (scale: 97)
69. Stereo button functions switch through DG413 quad switches (2 NO + 2 NC): one pole of each latching button drives a logic line, the other its LED; audio never runs through contacts; each card makes its own +5 V logic supply. A pole may switch a DC control voltage directly under the conditions of 152
80. Power is injected in groups of 8 cards: chain 1 feeds cards 1-8, chain 2 a separate ribbon to cards 9-16, and the master has its own ribbon, all from the power board, so no ribbon carries more than 8 cards. Current per pin is kept in `ARCHITECTURE.md`. The prototype uses chain 1 only
96. Power sizing rule: a card's own parts (regulators, heatsinks, its ribbon segment) are sized for its worst case (every IC at datasheet maximum, every LED lit, full signal); shared parts (converters, ribbon pins at a chain start) for IC quiescent current at typical × 1.5 plus use-dependent loads at maximum. Current figures in `ARCHITECTURE.md` (`tools/system_power_budget.py`). Ribbon contacts must be rated at least 1 A. Replace the 1.5 factor with prototype bench measurements before sizing the full-size supply
97. SC_ENV is negative: 0 V = no ducking, −1 V = 10 dB of gain reduction, DEPTH 0 to −4 V = 0 to 40 dB. Each DUCK-switched card feeds SC_ENV as a current into its control summer's virtual earth (30 kΩ since 153, against 10 kΩ feedback), so ducking does not depend on the fader position. The master drives the line at low impedance for up to 18 loads (104); a Schottky to AGND limits a positive fault to about +0.3 V; a disconnected line gives no ducking. Effective attack about 10 ms through the channel's control smoothing (accepted; hear it on the breadboard)
98. Logic returns to PGND: the open-collector PFL_ACT drivers and every button pull-down return to PGND on both cards, so LED and pull-up current never flows in AGND (invariant 4). DG41x GND pins stay on AGND
101. Whatever feeds the power ribbons must float from mains earth (invariant 8): today the Class II 24 V brick. PGND is earthed nowhere; the master's star point is the only ground reference and the mixer takes its earth from connected gear. Ground lift as 61. An internal mains supply and an external linear box are backlog items
152. A button pole may switch a DC control voltage directly (today MUTE: −15 V and DUCK: SC_ENV into the channel's control summer) when (a) the released throw is open and a hold resistor ties the switched line to ground, so no contact sequence can short a rail or a shared chain line, and (b) a smoothing ramp after the contact keeps the switching click-free and filters bounce. Audio never runs through a button; stereo audio switching stays on DG413s (69)
153. SC_ENV load per DUCK-switched card or AUX return is 30 kΩ (E24): 10.10 dB per −1 V; the master's driver sees about 1.67 kΩ with 18 loads

Rationale notes (why PFL, separate ribbons, no per-block submix, PFL beside channel meters, a compressor bus): `record/system.md`.
