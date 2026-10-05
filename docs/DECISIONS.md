# Decisions

## Confirmed by the user

1. Pro audio mixer for connecting synthesizers and instruments in electronic music live performances
2. Modular by design
3. Prototype: 4 stereo channels
4. Per channel: level fader, mute, ladder filter, two AUX connections, balanced inputs
5. Compressor with selectable/routable sidechain input
6. Sidechain filter is an **LPF** (not an HPF); the main intent is bass pumping
7. Filters are 24 dB/oct (4-pole) ladder lowpass filters with resonance. "Moog-style" is dropped as a requirement
8. Channel HPF is dropped from the prototype to simplify the build; resonance is therefore LPF-only
9. Filter part: SSI2144 baseline, AS3320 fallback
10. Design tool: KiCad, using its MCP server
11. Write the specification before starting implementation
12. Filter gain structure: "hot" drive by default (+4 dBu at the datasheet nominal ±20 mV), with a per-channel filter bypass. Updated after simulation (item 50): saturation starts around +8 dBu when the cutoff is lowered, and a prototype jumper offers a medium drive
13. The compressor processes a dedicated compressor bus; each channel assigns to main or compressor bus
14. AUX sends and returns are stereo by default; the design must also support mono inputs and therefore mono AUX sends
15. Prototype master section has a headphone output fed from the master bus (cue/PFL was first moved to the backlog; see item 28)
16. L/R filter tracking: shared control path plus a per-chip frequency offset trim and temperature-compensating resistor
17. Resonance limited by a fixed maximum Q current (about 300 µA) so no chip self-oscillates
18. Compensate the passband/bass gain loss that comes with resonance (half compensation, item 50)
19. Fader controls a VCA; part chosen in item 31
20. Per-channel cutoff CV input is included
21. Mono input: L/MONO jack normalling (L alone feeds both sides); no panel mono switch
22. No balance/pan control on the channel
23. AUX sends: post-fader, with a PCB jumper per send for pre-fader
24. Mono AUX: L/MONO jacks on the master card. Send outputs give (L+R)/2 on L when R is unplugged; returns normal L to R. Returns have level and a main/compressor bus switch
25. Inputs accept hot Eurorack modular levels (up to ±12 V peak) as well as line levels, without an external attenuator
26. One wide input trim (about -20 to +20 dB overall), no pad switch
27. All jacks on the mixer are 6.3 mm (channel inputs: 2x 6.3 mm TRS, L/MONO and R; also AUX sends and returns, sidechain input, outputs and headphones). No 3.5 mm jacks on the prototype; Eurorack users connect with 3.5 mm to 6.3 mm cables. Replaces the earlier plans of 3.5 mm alongside 6.3 mm and of 3.5 mm only. Other jack sizes can come later through the interchangeable input module (backlog)
28. PFL is in the prototype: a button per channel (post-filter, pre-fader, pre-mute) feeding a stereo cue bus; headphones switch to cue automatically while any PFL is active; PFL-active LED. No solo-in-place
29. Stereo LED level meter on the master card, always showing the master bus (changed by item 43: it no longer switches to cue)
30. Channel strips can be added one at a time; each stereo channel card has no direct dependency on other channel cards
31. VCA: SSI2162 dual, one per channel card (L/R) and one for the compressor. The clean-path THD+N target is relaxed from 0.01% to 0.05% to fit a tight budget
32. Budget: relatively tight; prefer cost-effective parts where the audible difference is small
33. Input receiver: AD8273 dual difference amplifier at G = ½, one chip per channel card
34. Expansion: chainable bus from the start, so the system can grow without a fixed slot count (form chosen in item 38)
35. Fader: linear 60 mm fader generating the VCA control voltage; a resistor network shapes the law to a pro console feel (fine resolution near 0 dB, fast fade to silence at the bottom)
36. Fader range: +10 dB at the top, -∞ (fully off) at the bottom
37. Fader scale: 0 dB at about 75% of travel; markings +10, +5, 0, -5, -10, -20, -30, -40, -60, -∞
38. Chain unit: per card. Each channel card has identical IN and OUT connectors wired straight through, linked to its neighbour by short ribbon cables; the master card sits at one end. No backplane PCB
39. Practical maximum: 16 channel cards
40. Chain power: unregulated about ±20 V nominal (raised from ±18 V so the far card's regulators stay out of dropout after ripple and cable drop); each card regulates its own ±15 V. Audio ground and power ground use separate conductors
41. Separate ribbons: a 34-pin IDC audio ribbon (buses, logic lines, interleaved audio grounds, spares) and a keyed 8-pin IDC power ribbon (2× V+, 2× V−, 4× ground). The 10- and 16-pin sizes are avoided so a Eurorack power cable cannot be plugged in
42. Chain pinouts, signal definitions and grounding rules as in `CHAIN.md`. Sidechain bus is mono. Power enters the chain at the master card, which is also the only point where audio ground and power ground join
43. Each channel card has an 8-segment mono LED level meter (louder of L/R), measuring after the filter and before the fader (same point as PFL); scale -30, -20, -10, -5, 0, +3, +6, clip relative to +4 dBu nominal. It replaces the peak LED. Built from a peak detector and comparators, not LM3915-type driver chips. Low-current LEDs returning to power ground. PFL is kept for listening
44. Compressor uses a performance control set: Amount (threshold and makeup gain together), Release, Mix (dry/wet parallel compression), click-free on/off button, about 5 gain-reduction LEDs, plus sidechain LPF frequency/bypass and source select. Attack (fast), ratio (about 4:1) and makeup range are preset inside
45. Sidechain source: 3-position switch INT (compressor bus) / BUS (sidechain bus) / EXT (jack). Per-channel SC send button tapped pre-fader and pre-mute (ghost triggering from muted channels). EXT input DC-coupled for audio and Eurorack envelopes/gates up to ±12 V. SC listen button routes the filtered sidechain to the cue bus
46. Confirmed in one batch: analog signal path; +4 dBu nominal, about +20 dBu internal maximum, +24 dBu only at balanced outputs; performance targets in SPEC.md section 5; DC-coupled receiver inputs with AC coupling about 3 Hz after the receiver; click-free mute via the VCA; fader bottom drives the VCA past -100 dB (fully off); sidechain LPF 40 to 500 Hz, 12 dB/octave, with bypass; channel independence rules (identical slots, master-side bus summing, wired-OR logic, no shared parts, per-card regulation); master level through an SSI2162 VCA and linear pot; headphone volume knob; balanced outputs on 6.3 mm TRS; external supply delivering unregulated about ±20 V
47. Tooling: one KiCad project per module with hierarchical sheets, custom symbol and footprint libraries, ngspice simulation, ERC/DRC checks, BOM export
48. Fader part: Bourns PTA6043-2015DPB103 (60 mm, single gang, linear, 10 kΩ, PCB pins, no detent, 15 mm metal lever). Fallback: Taiwan Alpha 60 mm 10k linear (check footprint). An RC filter smooths the fader's control voltage against wiper noise (datasheet: up to 100 mV sliding noise). Rated life 15,000 cycles: fine for the prototype; look for a longer-life fader for a product version
49. Master meter: stereo, 12 segments per side (-30, -20, -15, -10, -6, -3, 0, +3, +6, +9, +12, clip), measuring the master bus after the master level control. 0 = +4 dBu; clip lights about 3 dB below the internal limit (about +17 dBu internal, +23 dBu at the balanced outputs). All meters (channel and master) are peak-reading with a slow fall of about 1 to 2 s
50. Filter simulation outcome: keep hot drive as the default and add a prototype jumper for a medium drive 4 to 6 dB lower (pre-filter attenuator and make-up gain switched together), to choose by ear on the breadboard. Resonance uses half compensation (make-up gain √(1+k) tied to the Q control): -6 dB bass loss and about +9.5 dB peak at maximum Q. Per-chip cutoff trim must inject at least ±12 mV at the frequency control pin
51. AUX sends and returns levels: each send has a dual-gang master pot (-∞ to 0 dB) on the master card, outputs impedance-balanced TRS at +4 dBu nominal. Each return uses an AD8273 receiver with a gain jumper (-6 dB for pro/Eurorack effects, +6 dB for pedals), a linear pot controlling an SSI2162 VCA (-∞ to +10 dB), a mute button and the main/compressor bus switch
52. Filter cutoff range 20 Hz to 20 kHz on a linear pot (even octave spread through the exponential control)
53. Cutoff CV input: fixed about 1 V/octave, no amount knob (depth set at the source); DC-coupled, about 100 kΩ, protected to ±12 V, summed with the cutoff knob and limited
54. Channel buttons on the prototype are latching push switches with two contact sets (function plus LED); momentary buttons with logic are in the backlog
55. Channel strip layout follows the signal flow top to bottom: trim, cutoff, resonance, filter bypass, AUX 1, AUX 2, SC send and compressor bus buttons, PFL, mute, then meter beside the fader
56. Headphone output for the prototype: dual-gang volume pot, NJM4556A-class high-current op amp driver, 32 to 600 Ω, 6.3 mm jack on the front or top panel. A dedicated headphone amp chip can be considered for a product version
57. Compressor detector: feed-forward, peak-sensing, log conversion with a matched transistor array (AS3046 / THAT300 class; THAT2252 is obsolete). Amount 0 to 30 dB, Release 50 ms to 1.5 s, attack about 1 ms, ratio 4:1, gain-reduction LEDs at 1/3/6/10/15 dB
58. Power-up/down protection: relays on main and headphone outputs, about 2 s turn-on delay, fast disconnect when the chain voltage drops; AUX sends unprotected
59. Mechanical format: desktop unit; one PCB plus FR4 top panel (about 35 mm) per strip; rear-panel PCB-mount jacks; aluminium rail frame cut to length with side cheeks; chain ribbons under the strips
60. Prototype power: certified DC power brick (24 or 48 V) into the master section, isolated DC-DC module to about ±20 V, LC filter, per-card linear regulation. Power switch, resettable fuse, reverse-polarity protection, locking DC connector, power LED. A linear external supply box can be considered for a product version
61. Grounding: jack sleeves to their card's AGND; FR4 panels isolate jacks from the frame; frame bonded to the star point at the master card only, with a ground-lift switch (RC when lifted). Chain connectors are 2.54 mm shrouded keyed box headers (2x17, 2x4) with 28 AWG IDC ribbon; part numbers chosen during the schematic
62. Input connectors live on a separate passive input module plugged into a header on the channel card (10 pins since decision 68) (interface in `INPUT-MODULE.md`). Mono normalling happens on the module. The prototype builds the 6.3 mm module; 3.5 mm and D-SUB bundle modules come later. Receiver, protection, AC coupling and trim stay on the channel card
63. Part numbering: each unique part type gets a project part number `SX-<category>-<nnn>` (register `docs/parts.csv`), used as Mouser's customer part number. KiCad symbols carry ProjectPN, Manufacturer, MPN, Supplier and SupplierPN fields, and BOMs are exported grouped by ProjectPN (`docs/PART-NUMBERING.md`)
64. Soft clipping after each channel's input trim stage and on the master bus output, onset about 6 dB below the internal maximum (about +14 dBu). Inspired by the Intellijel Jellymix
65. Switchable fixed low-cut per channel at about 150 Hz (12 dB/octave proposed), film capacitors, after the trim stage and before the ladder filter; one more latching button with LED. The sweepable resonant HPF stays in the backlog
66. Sidechain ducking through the channel VCAs (inspired by the Boredbrain Xcelon SL): the master card turns the filtered sidechain into an envelope (THRESHOLD, DEPTH, DECAY; fast fixed attack) on chain line SC_ENV (was SPARE1); each channel has a DUCK button that adds it to its VCA control; AUX returns get a DUCK switch too. Complements the compressor bus
67. The cutoff CV jack moves from the input module to the channel card's filter section, keeping filter controls together and and frees header capacity for the backlog direct output
68. Input header grows to 10 pins (1x10 Molex KK 254 style): pins 8 and 9 reserved for a stereo pre-fader direct output (backlog), pin 10 AGND. The cutoff CV jack sits on the top panel next to CUTOFF
69. Stereo button functions are switched electronically: each latching button has two contact sets, one driving a logic line into a DG413 quad analog switch (Vishay, SOIC-16; 2 NO + 2 NC, so one chip selects between two stereo signals) and one lighting its LED. Audio never runs through mechanical contacts. Each channel card makes a +5 V logic supply locally (for the DG413 VL pins). Refines decision 54
70. Licensing is non-commercial source-available; the author keeps all commercial rights (`LICENSE.md`, `REUSE.toml`, texts in `LICENSES/`): hardware design files and documentation CC-BY-NC-SA-4.0, source code PolyForm-Noncommercial-1.0.0 with SPDX headers, repository configuration CC0-1.0. Applies from this change on; earlier commits stay under GPL-3.0

## Proposed but NOT confirmed

(none at the moment)

## Open items to settle before schematics

- [x] SSI2144 supply, headroom and noise (datasheet Rev 3.0, January 2018; facts in SPEC.md section 3)
- [x] Part availability, checked 2026-10-03 (details in the availability notes below)
- [x] Simulate one filter channel to set the gain structure (behavioural model; `simulation/filter/README.md`)
- [ ] Breadboard one SSI2144 channel to verify the real chip's distortion, noise and output scale, and pick the drive jumper setting by ear (plan: `simulation/filter/BREADBOARD.md`)
- [x] Fader part (item 48)
- [x] Pin assignment of the 34-pin audio and 8-pin power connectors (`CHAIN.md`)
- [x] Chain voltage headroom: raised to about ±20 V nominal (item 40)
- [ ] Supply rating for 16 cards (include channel meter LEDs, about 10–15 mA per card)
- [x] Master meter scale and segment count (item 49)

## Availability notes (checked 2026-10-03; recheck before ordering)

- SSI2144 (SSOP-16): not at the big distributors; sold through Sound Semiconductor's resellers. In stock at Thonk (about £3.75), also listed by synthCube and Modular Addict.
- SSI2164 (SOP-16): widely in stock (Thonk, Modular Addict, CE Distribution, AI Synthesis).
- THAT 2180A/B (SIP-8, through-hole): in stock at Newark, Farnell and element14 (tens to a few hundred units).
- Bourns PTA6043-2015DPB103 fader: active, about $1.92 at Mouser (about 1,300 in stock), €2.01 at Farnell. Alps RS60N11 is no longer manufactured.
- AD8273 (SOIC-14): active, widely stocked (DigiKey, Mouser, Arrow, Farnell), about $4.11. ADI's suggested replacement for the obsolete SSM2143.
- INA2137 (TI, dual, G = ½ or 2): active, $7.37 at quantity 1 at Mouser.
- SSM2143: obsolete.
- THAT1246: the SOIC-8 version (THAT1246S08-U) was in stock at Farnell and Newark, but one Farnell listing marks it "No Longer Manufactured"; the DIP-8 version shows a 20-week lead time. Treat it as at risk: buy prototype quantities plus spares early, and keep a fallback. Replaced by the AD8273 (proposed).

## VCA comparison (datasheets: THAT 2180 Rev 02, SSI2164 Rev 3.4; ±15 V, 20 kΩ converter resistors)

| | THAT 2180A | THAT 2180B | SSI2164 class AB | SSI2164 class A |
|---|---|---|---|---|
| THD at about 0 dBu, 0 dB gain | 0.005% typ, 0.010% max | 0.010% typ, 0.020% max | 0.05% typ | 0.025% typ |
| Output noise, 20 Hz to 20 kHz | -98 dBV (about -96 dBu) | -98 dBV | -96 dBu | -84 dBu |
| Channels per package | 1 (SIP-8) | 1 (SIP-8) | 4 (SOP-16) | 4 (SOP-16) |
| Control constant | 6.1 mV/dB | 6.1 mV/dB | -33 mV/dB | -33 mV/dB |

The THD+N target of 0.01% (filter bypassed) is only met by the 2180A. Because of the tight budget and the one-chip-per-card rule, the SSI2162 (dual, same family as the SSI2164, 3 dB lower noise) was chosen instead and the target relaxed to 0.05% (item 31). Both parts are current-in/current-out, so each needs a voltage-to-current input resistor and a current-to-voltage output op amp.

## Backlog (after the prototype)

The backlog is kept in `ROADMAP.md`. Items moved there by decision: channel HPF. (Cue/PFL was in the backlog but is now in the prototype.)

## Rationale notes

- Why SSI2144: a 4-pole ladder character without the hard parts of a discrete ladder (transistor matching and temperature compensation). It is a reissue of the SSM2044 (Rossum improved ladder), not a Moog transistor ladder; the user accepted this by dropping "Moog-style". Rejected: discrete OTA ladder (limited headroom, more noise, more tuning) and a state-variable filter (clean but not ladder character).
- Why HPF was dropped: build simplification. Resonance loop count would have doubled to 16 with HPF.
- Why hot drive plus bypass: the SSI2144 clips at ±50 mV and has 92 dB dynamic range. Driving it at its nominal level gains about 8 dB SNR over a clean +20 dBu headroom design (simulated: about 93 versus 85 dB), and its overdrive is musical. The simulation showed about 1.3% THD at +4 dBu when the cutoff is lowered, more colour than first assumed, so a medium-drive jumper lets the prototype settle it by ear. The bypass keeps the clean path within the pro targets, and avoids the 20 kHz roll-off of an open 4-pole filter.
- Why L/MONO jacks: standard on pro mixers, no extra panel controls, nothing to forget on stage. Mono handling for AUX sits on the master card, so channel cards stay simple.
- Why a -6 dB receiver: Eurorack peaks reach ±12 V. Gain ½ passes them on ±15 V rails with margin, at a small noise cost that the hot source levels more than make up for.
- Why AD8273 over the THAT1246: dual (one chip per card, like the SSI2162), active and widely stocked, about $4, noise similar to the 1246. Trade-off: 77 dB minimum CMRR versus the 1246's 90 dB typical, still far above a discrete op amp with 0.1% resistors (about 54 dB).
- Why PFL in the prototype: without it, trimming a channel by ear happens in the main mix where the audience hears it. Tapping before the VCA makes PFL pre-mute, so a channel can be prepared while muted. Solo-in-place was rejected because an accidental press silences the main mix.
- Why separate power and audio ribbons: with 16 cards, the card nearest the supply carries every card's current (estimated 1.3 A per rail). A separate power cable keeps that current, the rectifier ripple and switching spikes away from the sensitive mix bus lines, and can be heavier or fed from both ends. Separate ground conductors matter most: shared ground with power return current would put hum on the buses.
- Why no submix per block of cards: the noise is dominated by the sum of the channels' own noise, which grouping cannot change; a local submix lowers the total by only about 0.3 dB at 16 channels (estimate) and would break per-card independence.
- Why keep PFL with channel meters: the meter shows level, PFL lets the performer hear a channel (patch, tuning, filter, hum, timing) before the audience does. The channel meters take over trimming, so the master meter no longer needs to switch to cue.
- Why a performance compressor: the mixer is played during the set, so the compressor gets a few controls with an obvious musical effect (Amount, Release, Mix, on/off) and the technical settings are preset for pumping. Mix keeps the kick's punch while the rest pumps.
- Why a send master pot but a return gain jumper: the send pot adapts the output to any effect and can be ridden live, so no jumper is needed; L/R mismatch of a dual-gang pot is inaudible on an effect feed. On the returns, a -10 dBV pedal arrives about 8 dB short even with the level pot's +10 dB, so the receiver gain jumper (set once per effect) covers it without running the VCA at high, noisy gain. Returns use a VCA for accurate L/R tracking in the main mix and a click-free mute.
- Why a compressor bus: classic pumping keys the music from the kick. On a master-bus compressor the kick would duck itself; a separate bus lets the kick stay on main and trigger the compressor.
