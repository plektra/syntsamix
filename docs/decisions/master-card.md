# Master card decisions

The master/compressor card (`hardware/master`): AUX returns and sends, compressor and sidechain, master out, master meter, headphones, output protection and the card's power sheet. This file holds the scope and part choices; the sheet-by-sheet implementations are in `master-card-sheets.md`.

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (figures, sources, rationale, rejected options) is in `record/master-card.md` under the same number; read it when a figure or source is needed or before reopening a decision. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

5. Compressor with a selectable, routable sidechain input
6. The sidechain filter is an LPF (main intent: bass pumping)
15. Headphone output on the master (master bus, or cue while PFL is active: 28, 94)
24. Mono AUX: L/MONO jacks; a send gives (L+R)/2 on L when R is unplugged; returns normal L to R. Returns have level and a main/compressor bus switch
29. Stereo LED meter always showing the master bus (no switching to cue, 43)
44. Performance compressor controls: Amount (threshold and makeup together), Release, Mix (dry/wet parallel), click-free on/off button, five gain-reduction LEDs, sidechain LPF frequency and bypass, source select. Attack (fast), ratio (about 4:1) and makeup range preset inside
45. Sidechain source INT (compressor bus) / BUS (sidechain bus) / EXT (jack): SC BUS button, overridden by a plug in EXT (90). Per-channel SC send taps pre-fader and pre-mute (ghost triggering from muted channels). EXT DC-coupled for audio and Eurorack envelopes/gates up to ±12 V. SC LISTEN sends the filtered sidechain to the cue bus
49. Master meter: stereo, 12 segments per side (−30, −20, −15, −10, −6, −3, 0, +3, +6, +9, +12, clip) after the master level; 0 = +4 dBu; clip about +17 dBu internal (+23 dBu at the balanced outputs). All meters are peak-reading with a fall of about 1-2 s
51. AUX sends: dual-gang master pot per send (−∞ to 0 dB), impedance-balanced TRS at +4 dBu. AUX returns: G = ½ receiver (TL072 since 148) with a −6 / +6 dB jumper (pro/Eurorack vs pedals), a linear level pot on an SSI2162 VCA (−∞ to +10 dB), mute and main/compressor bus switch
56. Headphones: dual-gang volume pot, high-current driver (TPA6120A2, 84), 32 to 600 Ω, 6.3 mm jack on the front or top panel
57. Compressor detector: feed-forward, peak-sensing, log conversion on a matched transistor array (AS3046D, 82). Amount 0-30 dB, Release about 50 ms to 1.5 s, attack about 1 ms, ratio 4:1, gain-reduction LEDs at 1/3/6/10/15 dB
58. Power-up/down protection: relays on main and headphone outputs, about 2 s turn-on delay, instant drop-out when the chain voltage falls (both raw rails, 128); AUX sends unprotected
82. Log detector transistor array: Alfa AS3046D (SOIC-14), not at LCSC (hand-soldered, 150)
83. Main balanced outputs: one OutSmarts-type driver per side (DRV135UA since 125), +24 dBu balanced, no overload into a TS cable. Cost-cut candidate: two NE5532 halves per side. AUX sends stay impedance-balanced
84. Headphone driver: TI TPA6120A2 (HSOP-20 PowerPAD, ±15 V; LCSC C70439); the thermal pad needs copper and vias
85. Output relays: three Omron G6K-2F-Y DC12 DPDT (LCSC C397194): main L (hot, cold), main R (hot, cold), headphones (L, R); circuit in 92
125. Main output driver: TI DRV135UA (LCSC C544663), pin for pin with the end-of-life THAT1646S08 (symbol `syntsamix:THAT1646` kept); 10 µF non-polarised capacitor at each sense pin; a TS plug puts it in TI's single-ended mode at +6 dB
150. Master DG413 ×10, SSI2162 ×4, DRV135UA ×2 and AS3046D ×1 are hand-soldered by the user on the prototype's populated master (Assembly = "hand (decision 150)", counted by `tools/costs.py`). Backlog: a product build returns them to JLCPCB placement (one bad joint on the only master silences the mixer)

Rationale notes (performance compressor; send master pot vs return gain jumper): `record/master-card.md`.
