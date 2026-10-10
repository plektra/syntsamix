# Input module decisions

The passive input module (`hardware/input-module-6p3`) and its header interface (`docs/INPUT-MODULE.md`).

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (sources, rationale, rejected options) is in `record/input-module.md` under the same number; read it when a figure or source is needed or before reopening a decision. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

21. Mono input by L/MONO jack normalling (L alone feeds both sides); no panel mono switch
62. Input jacks live on a separate passive input module cabled to a header on the channel card (`INPUT-MODULE.md`); mono normalling happens on the module. The prototype builds the 6.3 mm module; 3.5 mm and D-SUB modules come later. Receiver, protection, AC coupling and trim stay on the channel card
67. The cutoff CV jack is on the channel card's filter section, not the input module
68. Input header: 10 pins, 1×10 Molex KK 254 style; pins 8 and 9 reserved for a stereo pre-fader direct output (backlog)
99. Both boards have male KK 254 headers linked by a 10-way 1:1 cable: Molex 22-01-3107 housings, 08-50-0114 crimps, 26 or 28 AWG, hot/cold pairs (2-3, 5-6) twisted; length (about 10-15 cm) set in the mechanical layout. Verify part numbers against the Molex drawings
105. Header pinout: 1 AGND, 2 L+, 3 L−, 4 AGND, 5 R+, 6 R−, 7 AGND, 8 DO_L, 9 DO_R (reserved), 10 AGND
