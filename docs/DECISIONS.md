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
12. Filter gain structure: "hot" drive (+4 dBu at the datasheet nominal ±20 mV, musical saturation above about +12 dBu), with a per-channel filter bypass
13. The compressor processes a dedicated compressor bus; each channel assigns to main or compressor bus
14. AUX sends and returns are stereo by default; the design must also support mono inputs and therefore mono AUX sends
15. Prototype master section has a headphone output fed from the master bus (cue/PFL was first moved to the backlog; see item 28)
16. L/R filter tracking: shared control path plus a per-chip frequency offset trim and temperature-compensating resistor
17. Resonance limited by a fixed maximum Q current (about 300 µA) so no chip self-oscillates
18. Compensate the passband/bass gain loss that comes with resonance
19. Fader controls a VCA; SSI2164 quad is a candidate alongside THAT 2180-class (part choice open)
20. Per-channel cutoff CV input is included
21. Mono input: L/MONO jack normalling (L alone feeds both sides); no panel mono switch
22. No balance/pan control on the channel
23. AUX sends: post-fader, with a PCB jumper per send for pre-fader
24. Mono AUX: L/MONO jacks on the master card. Send outputs give (L+R)/2 on L when R is unplugged; returns normal L to R. Returns have level and a main/compressor bus switch
25. Inputs accept hot Eurorack modular levels (up to ±12 V peak) as well as line levels, without an external attenuator
26. One wide input trim (about -20 to +20 dB overall), no pad switch
27. The prototype has 3.5 mm input jacks for Eurorack cables, alongside the 6.3 mm jacks
28. PFL is in the prototype: a button per channel (post-filter, pre-fader, pre-mute) feeding a stereo cue bus; headphones switch to cue automatically while any PFL is active; PFL-active LED. No solo-in-place
29. Stereo LED level meter on the master card: shows the cue bus during PFL, the master bus otherwise

## Proposed but NOT confirmed

- TRS 6.3 mm input connectors, with the 6.3 mm jack taking priority over its 3.5 mm partner
- Input receiver THAT1246 at -6 dB with DC-coupled inputs (availability unverified)
- AC coupling about 3 Hz after the receiver; per-channel peak LED
- 60 mm fader; click-free mute via the VCA
- ±15 V external supply with local regulation; backplane architecture with plug-in cards
- +4 dBu nominal; about +20 dBu internal maximum, +24 dBu only at balanced outputs; performance targets in SPEC.md section 5, split into filter bypassed and filter engaged
- Sidechain LPF 40 to 500 Hz with bypass; stereo-linked compressor; fast attack and long release
- Sidechain source select: compressor bus, external jack, or a backplane bus
- Master level control

## Open items to settle before schematics

- [x] SSI2144 supply, headroom and noise (datasheet Rev 3.0, January 2018; facts in SPEC.md section 3)
- [ ] SSI2144 and THAT1246 availability from distributors
- [ ] Simulate or breadboard one filter channel to set the gain structure
- [ ] Fader law and VCA part (THAT 2180 vs SSI2164; check availability)
- [ ] Backplane connector and pinout
- [ ] Confirm the proposed items above, or replace them

## Backlog (after the prototype)

The backlog is kept in `ROADMAP.md`. Items moved there by decision: channel HPF. (Cue/PFL was in the backlog but is now in the prototype.)

## Rationale notes

- Why SSI2144: a 4-pole ladder character without the hard parts of a discrete ladder (transistor matching and temperature compensation). It is a reissue of the SSM2044 (Rossum improved ladder), not a Moog transistor ladder; the user accepted this by dropping "Moog-style". Rejected: discrete OTA ladder (limited headroom, more noise, more tuning) and a state-variable filter (clean but not ladder character).
- Why HPF was dropped: build simplification. Resonance loop count would have doubled to 16 with HPF.
- Why hot drive plus bypass: the SSI2144 clips at ±50 mV and has 92 dB dynamic range. Driving it at its nominal level gains about 8 dB SNR over a clean +20 dBu headroom design, and its overdrive is musical. The bypass keeps the clean path within the pro targets, and avoids the 20 kHz roll-off of an open 4-pole filter.
- Why L/MONO jacks: standard on pro mixers, no extra panel controls, nothing to forget on stage. Mono handling for AUX sits on the master card, so channel cards stay simple.
- Why THAT1246 rather than the 1243 THAT recommends for pro inputs: Eurorack peaks reach ±12 V. The 1246's -6 dB gain passes them on ±15 V rails with margin, at a small noise cost that the hot source levels more than make up for.
- Why PFL in the prototype: without it, trimming a channel by ear happens in the main mix where the audience hears it. Tapping before the VCA makes PFL pre-mute, so a channel can be prepared while muted. Solo-in-place was rejected because an accidental press silences the main mix.
- Why a compressor bus: classic pumping keys the music from the kick. On a master-bus compressor the kick would duck itself; a separate bus lets the kick stay on main and trigger the compressor.
