# Channel card decisions

The stereo channel card (`hardware/channel-card`): receiver, trim, low-cut, ladder filter, VCA and fader, routing, meter, chain and power sheet.

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

4. Per channel: level fader, mute, ladder filter, two AUX connections, balanced inputs
7. Filters are 24 dB/oct (4-pole) ladder lowpass filters with resonance. "Moog-style" is dropped as a requirement
8. Channel HPF is dropped from the prototype to simplify the build; resonance is therefore LPF-only
9. Filter part: SSI2144 baseline, AS3320 fallback
12. Filter gain structure: "hot" drive by default (+4 dBu at the datasheet nominal ±20 mV), with a per-channel filter bypass. Updated after simulation (item 50): saturation starts around +8 dBu when the cutoff is lowered, and a prototype jumper offers a medium drive
16. L/R filter tracking: shared control path plus a per-chip frequency offset trim and temperature-compensating resistor
17. Resonance limited by a fixed maximum Q current (about 300 µA) so no chip self-oscillates
18. Compensate the passband/bass gain loss that comes with resonance (half compensation, item 50)
19. Fader controls a VCA; part chosen in item 31
20. Per-channel cutoff CV input is included
22. No balance/pan control on the channel
23. AUX sends: post-fader, with a PCB jumper per send for pre-fader
26. One wide input trim (about -20 to +20 dB overall), no pad switch
31. VCA: SSI2162 dual, one per channel card (L/R) and one for the compressor. The clean-path THD+N target is relaxed from 0.01% to 0.05% to fit a tight budget
33. Input receiver: AD8273 dual difference amplifier at G = ½, one chip per channel card
35. Fader: linear 60 mm fader generating the VCA control voltage; a resistor network shapes the law to a pro console feel (fine resolution near 0 dB, fast fade to silence at the bottom)
36. Fader range: +10 dB at the top, -∞ (fully off) at the bottom
37. Fader scale: 0 dB at about 75% of travel; markings +10, +5, 0, -5, -10, -20, -30, -40, -60, -∞
43. Each channel card has an 8-segment mono LED level meter (louder of L/R), measuring after the filter and before the fader (same point as PFL); scale -30, -20, -10, -5, 0, +3, +6, clip relative to +4 dBu nominal. It replaces the peak LED. Built from a peak detector and comparators, not LM3915-type driver chips. Low-current LEDs returning to power ground. PFL is kept for listening
48. Fader part: Bourns PTA6043-2015DPB103 (60 mm, single gang, linear, 10 kΩ, PCB pins, no detent, 15 mm metal lever). Fallback: Taiwan Alpha 60 mm 10k linear (check footprint). An RC filter smooths the fader's control voltage against wiper noise (datasheet: up to 100 mV sliding noise). Rated life 15,000 cycles: fine for the prototype; look for a longer-life fader for a product version
50. Filter simulation outcome: keep hot drive as the default and add a prototype jumper for a medium drive 4 to 6 dB lower (pre-filter attenuator and make-up gain switched together), to choose by ear on the breadboard. Resonance uses half compensation (make-up gain √(1+k) tied to the Q control): -6 dB bass loss and about +9.5 dB peak at maximum Q. Per-chip cutoff trim must inject at least ±12 mV at the frequency control pin
52. Filter cutoff range 20 Hz to 20 kHz on a linear pot (even octave spread through the exponential control)
53. Cutoff CV input: fixed about 1 V/octave, no amount knob (depth set at the source); DC-coupled, about 100 kΩ, protected to ±12 V, summed with the cutoff knob and limited
54. Channel buttons on the prototype are latching push switches with two contact sets (function plus LED); momentary buttons with logic are in the backlog
65. Switchable fixed low-cut per channel at about 150 Hz (12 dB/octave proposed), film capacitors, after the trim stage and before the ladder filter; one more latching button with LED. The sweepable resonant HPF stays in the backlog. Moved to 100 Hz by item 73
71. Resonance compensation uses the SSI2144 datasheet's external Q VCA (Rev 3.0 page 6, Figure 9): half of an LM13700 per filter (one chip per card), driven from one single-gang reverse-audio RESONANCE pot. The chip's own Q pin gets the datasheet's 13 kΩ to ground. A per-side 3-pin jumper selects the input share R10: none (plain SSI2144), half (R10 = 3 x R14, default; -3.5/-5.1/-6.0 dB at k = 1/2/3 against the √(1+k) target of -3.0/-4.8/-6.0 dB) or full (R10 = R14, constant bass). Refines decision 50: same half compensation, built in the feedback loop instead of a make-up gain stage, so no triple-gang pot or second VCA is needed
72. Level sheet: SSI2162 per datasheet Rev 1.2 Figure 1 (10 kΩ in and out, 110 Ω + 2.2 nF input network, 10 µF input coupling for control feedthrough), Class AB by default with a DNP mode resistor for trying Class A. The VCA stage inverts and a unity inverter restores polarity, so post-fader and pre-fader taps share one polarity. The fader law is a 3-segment piecewise curve from a buffered linear fader and two precision (superdiode) breakpoints on TL072s: +10 dB at the top, 0 dB at 75 %, -10 dB at 53 %, -20 dB at 42 %, -40 dB at 19 %, -60 dB at 14 %, -113 dB at the bottom. A 10 ms smoothing in the control summer covers fader noise and the click-free mute ramp. MUTE and DUCK switch through one DG413: mute adds +4.5 V to the control voltage (-127 dB at the top of the fader), DUCK adds SC_ENV at 10 dB of ducking per volt (scale and circuit: item 97, SC_ENV negative, fed into the summer's virtual earth through 30k1)
73. The switchable low-cut moves from about 150 Hz to 100 Hz (refines decision 65): same 12 dB/octave unity-gain Sallen-Key with 47 nF film capacitors, resistors changed to 24 kΩ and 47 kΩ (101 Hz, Q 0.71)
74. Routing sheet: the post-filter signal is buffered (NE5532 followers) before the pre-fader taps (PFL, SC send, meter, AUX pre option), so they do not load the filter's DG413 bypass switch. Every bus is driven through 22 kΩ (was 22.1 kΩ, changed by item 79); the master card's virtual-earth amplifiers use 22 kΩ feedback for unity gain per channel. The SC send sums L and R through 44.2 kΩ each, so the SC bus carries (L+R)/2. AUX sends use a 10 kΩ audio dual-gang pot per send (wiper drives the bus resistor) and a 2x3 header per send for pre/post (default post). Bus assign switches each side's bus resistor to MAIN or COMP through one DG413 (pressed = COMP); PFL and SC send switch through a DG412 (four normally-open switches). PFL_ACT is pulled to AGND by an MMBT3904 open collector (to PGND since item 98)
76. Meter sheet: L, -L, R and -R each drive a precision rectifier (superdiode, TL072) that charges one 1 µF hold capacitor through 1 kΩ outside its feedback loop (about 1 ms attack, stable); 680 kΩ gives a fall of 20 dB in about 1.5 s. A follower drives eight LM339 comparators against a 1% resistor ladder from +15 V (thresholds within 0.06 dB). The clip segment lights at +10 dB re nominal (+14 dBu, the soft-clip onset; confirmed by the user). LEDs: 3 mm, five green (-30 to 0), two yellow (+3, +6), one red (clip), about 2 mA each from +5 V, sinking into the LM339 outputs whose ground is PGND. A 10-segment bar graph and square LEDs were considered and dropped (item 86)
78. Chain and power sheet: the audio (34-pin) and power (8-pin) ribbons each have an IN and an OUT header wired straight through. LM317/LM337 make ±15.1 V from the raw ±20 V (200 Ω / 2.2 kΩ since item 79, 10 µF on ADJ, protection diodes per the TI datasheets), a 78L05 makes +5 V for the DG41x logic and the meter LEDs. Input capacitors return to PGND; dividers, output capacitors and SS14 rail clamps (stop a rail being pulled the wrong way at power-up) return to AGND. Estimated load about 130 mA per rail per card, so about 0.7 W in each TO-220 regulator. With this estimate 16 cards draw about 2.1 A per rail, about 1.05 A per power-ribbon pin: the power ribbon's current capacity must be rechecked in the master card design. Superseded figures: power injection in groups of 8 (item 80); budget and sizing in item 96 (`scripts/power_budget.py`: typical 122 / 105 mA, worst case 253 / 218 mA, regulators 1.24 W worst case)

## VCA comparison (datasheets: THAT 2180 Rev 02, SSI2164 Rev 3.4; ±15 V, 20 kΩ converter resistors)

| | THAT 2180A | THAT 2180B | SSI2164 class AB | SSI2164 class A |
|---|---|---|---|---|
| THD at about 0 dBu, 0 dB gain | 0.005% typ, 0.010% max | 0.010% typ, 0.020% max | 0.05% typ | 0.025% typ |
| Output noise, 20 Hz to 20 kHz | -98 dBV (about -96 dBu) | -98 dBV | -96 dBu | -84 dBu |
| Channels per package | 1 (SIP-8) | 1 (SIP-8) | 4 (SOP-16) | 4 (SOP-16) |
| Control constant | 6.1 mV/dB | 6.1 mV/dB | -33 mV/dB | -33 mV/dB |

The THD+N target of 0.01% (filter bypassed) is only met by the 2180A. Because of the tight budget and the one-chip-per-card rule, the SSI2162 (dual, same family as the SSI2164, 3 dB lower noise) was chosen instead and the target relaxed to 0.05% (item 31). Both parts are current-in/current-out, so each needs a voltage-to-current input resistor and a current-to-voltage output op amp.

## Rationale notes

- Why SSI2144: a 4-pole ladder character without the hard parts of a discrete ladder (transistor matching and temperature compensation). It is a reissue of the SSM2044 (Rossum improved ladder), not a Moog transistor ladder; the user accepted this by dropping "Moog-style". Rejected: discrete OTA ladder (limited headroom, more noise, more tuning) and a state-variable filter (clean but not ladder character).
- Why HPF was dropped: build simplification. Resonance loop count would have doubled to 16 with HPF.
- Why hot drive plus bypass: the SSI2144 clips at ±50 mV and has 92 dB dynamic range. Driving it at its nominal level gains about 8 dB SNR over a clean +20 dBu headroom design (simulated: about 93 versus 85 dB), and its overdrive is musical. The simulation showed about 1.3% THD at +4 dBu when the cutoff is lowered, more colour than first assumed, so a medium-drive jumper lets the prototype settle it by ear. The bypass keeps the clean path within the pro targets, and avoids the 20 kHz roll-off of an open 4-pole filter.
- Why a -6 dB receiver: Eurorack peaks reach ±12 V. Gain ½ passes them on ±15 V rails with margin, at a small noise cost that the hot source levels more than make up for.
- Why AD8273 over the THAT1246: dual (one chip per card, like the SSI2162), active and widely stocked, about $4, noise similar to the 1246. Trade-off: 77 dB minimum CMRR versus the 1246's 90 dB typical, still far above a discrete op amp with 0.1% resistors (about 54 dB).
