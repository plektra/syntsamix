# Master card decisions

The master/compressor card (`hardware/master`): AUX returns and sends, compressor and sidechain, master out, master meter, headphones, output protection and the card's power sheet. This file holds the scope and part choices; the sheet-by-sheet implementations (87-95, 103, 104) are in `master-card-sheets.md`.

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

5. Compressor with selectable/routable sidechain input
6. Sidechain filter is an **LPF** (not an HPF); the main intent is bass pumping
15. Prototype master section has a headphone output fed from the master bus (cue/PFL was first moved to the backlog; see item 28)
24. Mono AUX: L/MONO jacks on the master card. Send outputs give (L+R)/2 on L when R is unplugged; returns normal L to R. Returns have level and a main/compressor bus switch
29. Stereo LED level meter on the master card, always showing the master bus (changed by item 43: it no longer switches to cue)
44. Compressor uses a performance control set: Amount (threshold and makeup gain together), Release, Mix (dry/wet parallel compression), click-free on/off button, about 5 gain-reduction LEDs, plus sidechain LPF frequency/bypass and source select. Attack (fast), ratio (about 4:1) and makeup range are preset inside
45. Sidechain source: INT (compressor bus) / BUS (sidechain bus) / EXT (jack); selected by an SC BUS button and the EXT jack's plug detection since item 90 (was a 3-position switch). Per-channel SC send button tapped pre-fader and pre-mute (ghost triggering from muted channels). EXT input DC-coupled for audio and Eurorack envelopes/gates up to ±12 V. SC listen button routes the filtered sidechain to the cue bus
49. Master meter: stereo, 12 segments per side (-30, -20, -15, -10, -6, -3, 0, +3, +6, +9, +12, clip), measuring the master bus after the master level control. 0 = +4 dBu; clip lights about 3 dB below the internal limit (about +17 dBu internal, +23 dBu at the balanced outputs). All meters (channel and master) are peak-reading with a slow fall of about 1 to 2 s
51. AUX sends and returns levels: each send has a dual-gang master pot (-∞ to 0 dB) on the master card, outputs impedance-balanced TRS at +4 dBu nominal. Each return uses an AD8273 receiver with a gain jumper (-6 dB for pro/Eurorack effects, +6 dB for pedals), a linear pot controlling an SSI2162 VCA (-∞ to +10 dB), a mute button and the main/compressor bus switch
56. Headphone output for the prototype: dual-gang volume pot, NJM4556A-class high-current op amp driver (replaced by the TPA6120A2, item 84), 32 to 600 Ω, 6.3 mm jack on the front or top panel. A dedicated headphone amp chip can be considered for a product version
57. Compressor detector: feed-forward, peak-sensing, log conversion with a matched transistor array (AS3046 / THAT300 class; THAT2252 is obsolete). Amount 0 to 30 dB, Release 50 ms to 1.5 s, attack about 1 ms, ratio 4:1, gain-reduction LEDs at 1/3/6/10/15 dB
58. Power-up/down protection: relays on main and headphone outputs, about 2 s turn-on delay, fast disconnect when the chain voltage drops; AUX sends unprotected
82. The compressor's log detector uses an Alfa AS3046D transistor array (SOIC-14; five NPN, two as a matched pair with VBE within ±1 mV), about 4.50 € from synth-DIY sources such as Electric Druid. Not stocked at LCSC: hand-soldered or consigned like the SSI chips. THAT300 rejected on price (about 12.70 €) and scarce EU stock
83. Main balanced outputs use one THAT1646S08-U OutSmarts line driver per side (about 7 $ each): +24 dBu balanced, full level and no overload with a TS cable. **Cost-cut candidate:** if the budget needs it, fall back to two NE5532 halves per side (buffer + inverter with series output resistors; same +24 dBu, but a TS cable loses 6 dB and loads the cold leg). AUX sends stay impedance-balanced
84. Headphone driver: TI TPA6120A2 (HSOP-20 PowerPAD, ±15 V, 1.5 W per channel into 32 Ω; LCSC C70439, about 1.90 $), replacing the NJM4556A of item 56. The NJM4556AM's DMP8 package is rated for only 300 mW (Nisshinbo datasheet 2025-03-06) but would dissipate about 0.4 W per channel at 1 Vrms into 32 Ω from ±15 V; its DIP8 version is NRND. The thermal pad needs copper and vias under it
85. Output protection relays: three Omron G6K-2F-Y DC12 DPDT signal relays (SMD; LCSC C397194, about 0.94 $): main L (hot and cold), main R (hot and cold) and headphones (L and R). 12 V coils from +15 V through a series resistor, one transistor driver, a comparator and timer for the 2 s power-up delay and instant drop-out. Coil data and contact rating to be checked in the Omron datasheet when drawing

## Rationale notes

- Why a performance compressor: the mixer is played during the set, so the compressor gets a few controls with an obvious musical effect (Amount, Release, Mix, on/off) and the technical settings are preset for pumping. Mix keeps the kick's punch while the rest pumps.
- Why a send master pot but a return gain jumper: the send pot adapts the output to any effect and can be ridden live, so no jumper is needed; L/R mismatch of a dual-gang pot is inaudible on an effect feed. On the returns, a -10 dBV pedal arrives about 8 dB short even with the level pot's +10 dB, so the receiver gain jumper (set once per effect) covers it without running the VCA at high, noisy gain. Returns use a VCA for accurate L/R tracking in the main mix and a click-free mute.
