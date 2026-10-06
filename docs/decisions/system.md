# System and chain decisions

System scope, signal levels, buses, cross-board functions and the chain between cards (audio and power ribbons, grounding).

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

1. Pro audio mixer for connecting synthesizers and instruments in electronic music live performances
2. Modular by design
3. Prototype: 4 stereo channels
13. The compressor processes a dedicated compressor bus; each channel assigns to main or compressor bus
14. AUX sends and returns are stereo by default; the design must also support mono inputs and therefore mono AUX sends
25. Inputs accept hot Eurorack modular levels (up to ±12 V peak) as well as line levels, without an external attenuator
27. All jacks on the mixer are 6.3 mm (channel inputs: 2x 6.3 mm TRS, L/MONO and R; also AUX sends and returns, sidechain input, outputs and headphones). No 3.5 mm jacks on the prototype; Eurorack users connect with 3.5 mm to 6.3 mm cables. Replaces the earlier plans of 3.5 mm alongside 6.3 mm and of 3.5 mm only. Other jack sizes can come later through the interchangeable input module (backlog)
28. PFL is in the prototype: a button per channel (post-filter, pre-fader, pre-mute) feeding a stereo cue bus; headphones switch to cue automatically while any PFL is active; PFL-active LED. No solo-in-place
30. Channel strips can be added one at a time; each stereo channel card has no direct dependency on other channel cards
32. Budget: relatively tight; prefer cost-effective parts where the audible difference is small
34. Expansion: chainable bus from the start, so the system can grow without a fixed slot count (form chosen in item 38)
38. Chain unit: per card. Each channel card has identical IN and OUT connectors wired straight through, linked to its neighbour by short ribbon cables; the master card sits at one end. No backplane PCB
39. Practical maximum: 16 channel cards
40. Chain power: unregulated about ±20 V nominal (raised from ±18 V so the far card's regulators stay out of dropout after ripple and cable drop); each card regulates its own ±15 V. Audio ground and power ground use separate conductors
41. Separate ribbons: a 34-pin IDC audio ribbon (buses, logic lines, interleaved audio grounds, spares) and a keyed 8-pin IDC power ribbon (2× V+, 2× V−, 4× ground). The 10- and 16-pin sizes are avoided so a Eurorack power cable cannot be plugged in
42. Chain pinouts, signal definitions and grounding rules as in `CHAIN.md`. Sidechain bus is mono. Power enters the chain at the master card, which is also the only point where audio ground and power ground join
46. Confirmed in one batch: analog signal path; +4 dBu nominal, about +20 dBu internal maximum, +24 dBu only at balanced outputs; performance targets in SPEC.md section 5; DC-coupled receiver inputs with AC coupling about 3 Hz after the receiver; click-free mute via the VCA; fader bottom drives the VCA past -100 dB (fully off); sidechain LPF 40 to 500 Hz, 12 dB/octave, with bypass; channel independence rules (identical slots, master-side bus summing, wired-OR logic, no shared parts, per-card regulation); master level through an SSI2162 VCA and linear pot; headphone volume knob; balanced outputs on 6.3 mm TRS; external supply delivering unregulated about ±20 V
61. Grounding: jack sleeves to their card's AGND; FR4 panels isolate jacks from the frame; frame bonded to the star point at the master card only, with a ground-lift switch (RC when lifted). Chain connectors are 2.54 mm shrouded keyed box headers (2x17, 2x4) with 28 AWG IDC ribbon; part numbers chosen during the schematic
64. Soft clipping after each channel's input trim stage and on the master bus output, onset about 6 dB below the internal maximum (about +14 dBu). Inspired by the Intellijel Jellymix
66. Sidechain ducking through the channel VCAs (inspired by the Boredbrain Xcelon SL): the master card turns the filtered sidechain into an envelope (THRESHOLD, DEPTH, DECAY; fast fixed attack) on chain line SC_ENV (was SPARE1); each channel has a DUCK button that adds it to its VCA control; AUX returns get a DUCK switch too. Complements the compressor bus
69. Stereo button functions are switched electronically: each latching button has two contact sets, one driving a logic line into a DG413 quad analog switch (Vishay, SOIC-16; 2 NO + 2 NC, so one chip selects between two stereo signals) and one lighting its LED. Audio never runs through mechanical contacts. Each channel card makes a +5 V logic supply locally (for the DG413 VL pins). Refines decision 54
80. Power ribbon current (open since item 78) is solved by injecting power in groups of 8 cards: chain 1 feeds cards 1 to 8, chain 2 runs a separate power ribbon to card 9 and on to card 16 (no cable between cards 8 and 9). With the separate power board (item 81) both chains start at the power board, which also feeds the master card through its own ribbon, so no single ribbon carries more than 8 cards. About 0.53 A per pin at full size. Channel cards are unchanged; the 4-channel prototype uses only chain 1

## Rationale notes

- Why PFL in the prototype: without it, trimming a channel by ear happens in the main mix where the audience hears it. Tapping before the VCA makes PFL pre-mute, so a channel can be prepared while muted. Solo-in-place was rejected because an accidental press silences the main mix.
- Why separate power and audio ribbons: with 16 cards, the card nearest the supply carries every card's current (estimated 1.3 A per rail). A separate power cable keeps that current, the rectifier ripple and switching spikes away from the sensitive mix bus lines, and can be heavier or fed from both ends. Separate ground conductors matter most: shared ground with power return current would put hum on the buses.
- Why no submix per block of cards: the noise is dominated by the sum of the channels' own noise, which grouping cannot change; a local submix lowers the total by only about 0.3 dB at 16 channels (estimate) and would break per-card independence.
- Why keep PFL with channel meters: the meter shows level, PFL lets the performer hear a channel (patch, tuning, filter, hum, timing) before the audience does. The channel meters take over trimming, so the master meter no longer needs to switch to cue.
- Why a compressor bus: classic pumping keys the music from the kick. On a master-bus compressor the kick would duck itself; a separate bus lets the kick stay on main and trigger the compressor.
