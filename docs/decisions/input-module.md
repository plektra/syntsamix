# Input module decisions

The passive input module (`hardware/input-module-6p3`) and its header interface (`docs/INPUT-MODULE.md`).

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (sources, rationale, rejected options) is in `record/input-module.md` under the same number; read it when a figure or source is needed or before reopening a decision. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

21. Mono input by L/MONO jack normalling (L alone feeds both sides); no panel mono switch
62. Input jacks live on a separate passive input module cabled to a header on the channel card (`INPUT-MODULE.md`); mono normalling happens on the module. The prototype builds the 6.3 mm module; 3.5 mm and D-SUB modules come later. Receiver, protection, AC coupling and trim stay on the channel card. The 6.3 mm module stands on edge under the rear rail, jacks stacked L above R (160)
67. The cutoff CV jack is on the channel card's filter section, not the input module
68. Input header: since 181 a 2x6 shrouded box header (12 pins); DO_L and DO_R reserved for a stereo pre-fader direct output (backlog)
99. Both boards carry male headers linked by a 1:1 cable; since 181 a self-made IDC flat cable
105. Header signals: two balanced pairs (L±, R±) with AGND between and around them, DO_L and DO_R reserved; pin numbers since 181
179. Ready-made Molex 217796-1101 input cable: replaced by the IDC flat cable (180, 181)
180. Input cable a self-made IDC flat cable on shrouded box headers instead of the Molex lead of 179 (cost, about €4 per channel); the 6.3 mm jacks stay the Rean NYS216 (132); parts and pinout in 181
181. Input header and cable (refines 68, 99, 105, 179, 180): Adam Tech BHR-12-VUA 2x6 shrouded box header on both boards (SX-CONN-024), no latches; cable Würth WR-CAB 12-way 28 AWG (SX-WIRE-006) with an Adam Tech FCS-12-SG IDC socket at each end (SX-CONN-025), 150 mm, 1:1, red conductor at pin 1. Pinout 1 DO_L, 2 AGND, 3 L+, 4 L−, 5-8 AGND, 9 R+, 10 R−, 11 AGND, 12 DO_R, so a 2x4 power socket forced into the shroud puts its rails on signal pins only. On delivery: press a test cable, dry-fit a power socket
