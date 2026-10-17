# Input module decisions

The passive input module (`hardware/input-module-6p3`) and its header interface (`docs/INPUT-MODULE.md`).

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (sources, rationale, rejected options) is in `record/input-module.md` under the same number; read it when a figure or source is needed or before reopening a decision. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

21. Mono input by L/MONO jack normalling (L alone feeds both sides); no panel mono switch
62. Input jacks live on a separate passive input module cabled to a header on the channel card (`INPUT-MODULE.md`); mono normalling happens on the module. The prototype builds the 6.3 mm module; 3.5 mm and D-SUB modules come later. Receiver, protection, AC coupling and trim stay on the channel card. The 6.3 mm module stands on edge under the rear rail, jacks stacked L above R (160)
67. The cutoff CV jack is on the channel card's filter section, not the input module
68. Input header: 10 pins, 1×10 Molex KK 254 style as drawn, moving to an IDC box header (180); pins 8 and 9 reserved for a stereo pre-fader direct output (backlog)
99. Both boards have male headers linked by a 1:1 cable: drawn as KK 254 with the ready-made Molex 217796-1101 (179), to become a self-made IDC ribbon on box headers (180)
105. Header pinout: 1 AGND, 2 L+, 3 L−, 4 AGND, 5 R+, 6 R−, 7 AGND, 8 DO_L, 9 DO_R (reserved), 10 AGND
179. Input cable ready-made Molex 217796-1101 (150 mm, KK 254 both ends; refines 99, 160): stands as drawn until the IDC ribbon of 180 is settled in /system; its 1:1 check on delivery applies only if it is still ordered
180. Input cable becomes a self-made IDC ribbon (flat cable, one IDC socket pressed at each end) on shrouded box headers on both boards, instead of the Molex lead of 179 (cost: about €4 per channel); 1:1 wiring and the signal roles of 105 kept; the 6.3 mm jacks stay the Rean NYS216 (132). **[proposed]** for /system before the channel layout: a 2x6 header (smallest size decision 41 allows; Adam Tech BHR-12-VUA headers, FCS-12-SG sockets, a flat ribbon with a stated rating, as decision 178 requires of the chain cable), the mapping of 105 onto 12 pins, keying so the 8-pin power socket cannot be plugged in, headers without latches
