# Input module decisions

The passive input module (`hardware/input-module-6p3`) and its header interface (`docs/INPUT-MODULE.md`).

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

21. Mono input: L/MONO jack normalling (L alone feeds both sides); no panel mono switch
62. Input connectors live on a separate passive input module plugged into a header on the channel card (10 pins since decision 68) (interface in `INPUT-MODULE.md`). Mono normalling happens on the module. The prototype builds the 6.3 mm module; 3.5 mm and D-SUB bundle modules come later. Receiver, protection, AC coupling and trim stay on the channel card
67. The cutoff CV jack moves from the input module to the channel card's filter section, keeping filter controls together and and frees header capacity for the backlog direct output
68. Input header grows to 10 pins (1x10 Molex KK 254 style): pins 8 and 9 reserved for a stereo pre-fader direct output (backlog), pin 10 AGND. The cutoff CV jack sits on the top panel next to CUTOFF

## Rationale notes

- Why L/MONO jacks: standard on pro mixers, no extra panel controls, nothing to forget on stage. Mono handling for AUX sits on the master card, so channel cards stay simple.
