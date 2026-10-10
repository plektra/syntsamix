# Channel card decisions

The stereo channel card (`hardware/channel-card`): receiver, trim, low-cut, ladder filter, VCA and fader, routing, meter, chain and power sheet. Part and mechanical choices for the panel stack (110-115, 117) are in `channel-card-parts.md`.

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (figures, sources, simulations, rationale, rejected options) is in `record/channel-card.md` under the same number, along with the VCA comparison table and the rationale notes; read it when a figure or source is needed or before reopening a decision. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

4. Per channel: level fader, mute, ladder filter, two AUX sends, balanced inputs
7. Filters are 24 dB/oct (4-pole) ladder lowpass with resonance ("Moog-style" dropped as a requirement)
8. No channel HPF on the prototype (build simplification); resonance is LPF-only
9. Filter part: SSI2144, AS3320 fallback
12. Filter gain structure: hot drive by default (+4 dBu at about ±19 mV at the SSI2144 input, 140) with a per-channel filter bypass; a jumper offers a medium drive (50)
16. L/R filter tracking: shared control path plus a per-chip cutoff offset trim (RV101/RV151). No temperature-compensating resistor on the prototype (141)
17. Resonance limited by a fixed maximum Q current (about 280 µA, 129/140) so no chip self-oscillates
18. The bass loss that comes with resonance is half-compensated (50, 71)
19. Fader controls a VCA (part: 31)
20. Per-channel cutoff CV input
22. No balance or pan control on the channel
23. AUX sends post-fader, with a jumper per send for pre-fader
26. One wide input trim, no pad switch: about −13.5 to +28.3 dB (115, 140)
31. VCA: SSI2162 dual, one per channel card (L/R). Clean-path THD+N target relaxed from 0.01 % to 0.05 % for budget
33. Input receiver at G = ½, inverting (TL072 difference amplifier since 143)
35. Fader: linear 60 mm, generating the VCA control voltage through a law-shaping network (fine near 0 dB, fast fade at the bottom; circuit 72)
36. Fader range +10 dB at the top to fully off at the bottom
37. Fader scale: 0 dB at about 75 % of travel; marks +10, +5, 0, −5, −10, −20, −30, −40, −60, −∞
43. 8-segment mono meter per card (louder of L/R), after the filter and before the fader (the PFL point); scale −30, −20, −10, −5, 0, +3, +6, clip re +4 dBu. Peak detector and comparators, no LM3915-type driver; low-current LEDs returning to PGND. Replaces the peak LED. LED form: 119
48. Fader: Bourns PTA6043-2015DPB103 (60 mm, linear 10 kΩ, no detent, 15 mm metal lever); fallback Taiwan Alpha 60 mm 10k linear (check footprint). Wiper noise smoothed by the control summer (72). Rated 15,000 cycles: fine for the prototype, revisit for a product
50. Filter drive and compensation (from simulation): hot drive by default plus a prototype jumper for a medium drive about 4 dB lower (attenuator and make-up switched together), chosen by ear on the breadboard. Half compensation (√(1+k), built as 71). The cutoff trim must inject at least ±12 mV at the frequency pin
52. Cutoff range 20 Hz to 20 kHz on a linear pot (even octave spread)
53. Cutoff CV input: about 1 V/oct fixed, no amount knob; DC-coupled, about 100 kΩ, protected to ±12 V, summed with the cutoff knob and limited
54. Channel buttons are latching push switches with two contact sets (function plus LED); momentary buttons with logic are backlog
65. Switchable fixed low-cut per channel after the trim stage, before the filter, with a lit latching button: 100 Hz, 12 dB/oct (73). Sweepable resonant HPF stays in the backlog
71. Resonance compensation by the SSI2144 datasheet's external Q VCA (Rev 3.0 Figure 9): half an LM13700 per filter (one chip per card), one single-gang reverse-audio RESONANCE pot; the chip's Q pin gets 13 kΩ to ground. A per-side jumper selects none, half (default) or full compensation
72. Level sheet: SSI2162 per datasheet Figure 1, Class AB (DNP resistor for trying Class A); the VCA inverts and a unity inverter restores polarity, so pre- and post-fader taps share one polarity. Fader law: 3-segment piecewise curve from a buffered fader and two superdiode breakpoints: +10 dB at the top, 0 dB at 75 %, −10 at 53 %, −20 at 42 %, −40 at 19 %, −60 at 14 %, about −102 dB at the bottom (102). A 10 ms smoothing in the control summer makes mute click-free and filters fader noise. Mute adds +4.5 V to the control voltage; DUCK adds SC_ENV at 10 dB per −1 V (97, 153). Switching: 142
73. The low-cut is a unity-gain Sallen-Key at 101 Hz, Q 0.71 (24 kΩ, 47 kΩ, 47 nF C0G per 113)
74. Routing: the post-filter signal is buffered (NE5532 followers) before the pre-fader taps (PFL, SC send, meter, AUX pre). Every bus is driven through 22 kΩ (the master's virtual earths use 22 kΩ feedback). SC send sums L and R through 47 kΩ each: the SC bus carries 0.47 (L+R) (140). AUX sends: 10 kΩ audio dual pot per send, 2×3 header for pre/post (default post). Bus assign switches each side's bus resistor to MAIN or COMP through a DG413 (pressed = COMP); PFL and SC send through a second DG413 (139). PFL_ACT pulled low by an MMBT3904 open collector to PGND (98)
76. Meter: L, −L, R, −R drive superdiode rectifiers (TL072) charging a 1 µF hold through 1 kΩ (about 1 ms attack); 680 kΩ gives 20 dB fall in about 1.5 s. A follower drives eight LM339 comparators against a 1 % ladder from +15 V. Clip lights at +10 dB re nominal (+14 dBu, soft-clip onset). LEDs: five green (−30 to 0), two yellow (+3, +6), one red (clip), about 2 mA each from +5 V sinking into LM339 outputs on PGND; 0805 under a printed bezel (119)
78. Chain and power sheet: audio (34-pin) and power (8-pin) ribbons each have IN and OUT headers wired straight through. LM317/LM337 make ±15.1 V from the raw ±20 V (200 Ω / 2.2 kΩ dividers, 10 µF on ADJ, protection diodes per TI); a 78L05 makes +5 V for DG41x logic and meter LEDs. Input capacitors to PGND; dividers, output capacitors and SS14 rail clamps to AGND. Load figures: `scripts/power_budget.py` (current values in `ARCHITECTURE.md`); regulator package 110
102. U204 (fader buffer A, control summer B) is an OPA2171: input range to V−, no phase reversal, so the fader wiper at −15 V cannot send the VCA to full gain. Both superdiodes sit on the TL072 U205 (OPA2171 input diodes must not sit in an open-loop stage). Bottom of the fader about −102 dB
123. Op amp power: U107 (cutoff CV summer) is a TL072; U401 (meter inverters) and U404 (hold follower) are TL062CDR. U205 and the meter superdiodes U402/U403 stay TL072
129. RESONANCE pot RV183 (C10K) within Alpha's 0.02 W non-B rating: R184 = 12 k (about 17 mW). R120/R184 set the maximum Q current, provisional until the breadboard (R120 = 36k since 140)
130. Tempco leg R108/R158: superseded by 141 (TFPT part dropped for the prototype); the 820 Ω + 180 Ω (R122/R172) series leg it introduced stays
139. PFL and SC send switch U303 is a DG413 (not a DG412): PFL L on SW1, PFL R on SW4 (NO, by PFL_CTRL); SC send on NC SW2, driven by SC_OFF from SW302 pin 1 (high when released, pulled to PGND by R315 when pressed). SX-IC-008 (DG412) unused
140. Every channel resistor is E24 with a JLCPCB basic or preferred part (134, 137), using series pairs where one value is not close enough. Values and the simulated fader law are in the schematic, `STATUS.md`/`CHECKLISTS.md` and the record. R217 became 30 k by 153
141. No temperature compensation of the filter on the prototype: R108/R158 are standard 820 Ω 0805 with R122/R172 180 Ω in series (1 k leg, scale unchanged at 25 °C; about 0.33 %/K drift accepted, L and R drift together). Putting a TFPT back is a backlog item; breadboard test 12 measures the drift
142. MUTE and DUCK are switched by the spare pole of their latching buttons, no DG413: MUTE pin 3 = −15 V, DUCK pin 3 = SC_ENV, common pin 2 into R216 33k / R217 into the control summer; released throw open and 100 k holds to AGND (conditions of 152). The 10 ms summer smoothing keeps the ramps click-free and filters bounce. U206 removed
143. Input receiver: TL072CDT G = ½ difference amplifier per side, all legs 10k 0.1 % thin film (SX-R-107; the RFI series resistors R1-R4 form half of each 20k input leg). Still inverting. CMRR ≥ 51.5 dB worst case (about 60 typical), EIN about −98 dBu, input impedance 20k (IN+) / 30k (IN−). Enough because runs are 1-5 m and hum rejection does not depend on cable length
155. On the prototype the user hand-solders the SSI2144s (U101/U102) and the SSI2162 (U201): Assembly = "hand (decision 155)", neither type consigned (refines 133 for these parts, like 150 on the master). Bipolar 10 µF capacitors stay consigned until breadboard test 11. Backlog: a product returns them to JLCPCB placement
