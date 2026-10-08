# Input module decisions

The passive input module (`hardware/input-module-6p3`) and its header interface (`docs/INPUT-MODULE.md`).

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

21. Mono input: L/MONO jack normalling (L alone feeds both sides); no panel mono switch
62. Input connectors live on a separate passive input module plugged into a header on the channel card (10 pins since decision 68) (interface in `INPUT-MODULE.md`). Mono normalling happens on the module. The prototype builds the 6.3 mm module; 3.5 mm and D-SUB bundle modules come later. Receiver, protection, AC coupling and trim stay on the channel card
67. The cutoff CV jack moves from the input module to the channel card's filter section, keeping filter controls together and and frees header capacity for the backlog direct output
68. Input header grows to 10 pins (1x10 Molex KK 254 style): pins 8 and 9 reserved for a stereo pre-fader direct output (backlog), pin 10 AGND. The cutoff CV jack sits on the top panel next to CUTOFF
99. Input-module cable (system validation 2026-10-06, finding 7; refines item 68, changes `INPUT-MODULE.md`): both boards keep male KK 254 headers; they are linked by a 10-way 1:1 cable (pin 1 to pin 1) with a Molex 22-01-3107 crimp housing (KK 254, 2695 series, 10 positions, friction ramp) and 08-50-0114 crimps (22-30 AWG, tin) at each end, 26 or 28 AWG wire, the hot/cold pairs (pins 2-3, 5-6) twisted. Length set in the mechanical layout (about 10 to 15 cm expected). Part numbers from distributor listings; verify against the Molex drawings. A socket on the module plugging straight onto the card was rejected: it fixes the module position against the rear panel and rules out cabled D-SUB modules
105. Input header pinout confirmed as drawn (`/system` 2026-10-08; closes the pinout proposal in `INPUT-MODULE.md`): pin 1 AGND, 2 L+, 3 L−, 4 AGND, 5 R+, 6 R−, 7 AGND, 8 DO_L, 9 DO_R (reserved), 10 AGND. Both schematics already follow it; fixed before the channel card PCB. Rejected: a 12-pin header giving each direct output its own ground (new housing, both boards redrawn, for a backlog feature); leaving it proposed until layout (a late change would redraw two schematics and the cable)

## Rationale notes

- Why L/MONO jacks: standard on pro mixers, no extra panel controls, nothing to forget on stage. Mono handling for AUX sits on the master card, so channel cards stay simple.
