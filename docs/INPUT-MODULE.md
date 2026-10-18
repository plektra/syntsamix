# Input module interface

Status: **[confirmed]** by the user (decisions 62, 67, 68, 99, 105, 160, 180 and 181; the pinout below by decision 181).

The channel card carries no input jacks. Its input sockets connect to a small **input module** that holds the connectors. The module options are interchangeable:

| Module | Connectors | Mono handling | Status |
|---|---|---|---|
| `input-module-6p3` | 2x 6.3 mm TRS (L/MONO, R) | R jack switch contacts normal L to R | Prototype |
| `input-module-3p5` | 2x 3.5 mm stereo switched jacks | Same as 6.3 mm | Backlog |
| `input-module-dsub` | One DB-25 carrying several channels (common 8-channel analog pinout), cables to each card's header | Jumper or switch per channel | Backlog |

The module is passive: connectors, normalling and nothing that needs power. The input receiver (a TL072 difference amplifier, G = ½, decision 143; the AD8273 before it), its protection, the AC coupling and the trim stay on the channel card, so every module gets the same hot-level handling (up to ±12 V peak, decision 25). Input impedance seen by the source (decision 143): 20 kΩ on each hot pin (L+, R+) and 30 kΩ on each cold pin (L−, R−); a mono source normalled to both hot pins sees 10 kΩ, which any line output or Eurorack module drives.

## Input header: 12 pins, 2x6 shrouded box header, 2.54 mm (decision 181)

| Pin | Signal | Notes |
|---|---|---|
| 1 | DO_L | Reserved for the pre-fader direct output, left (backlog). Unconnected on the prototype |
| 2 | AGND | |
| 3 | L+ | Hot, left (or mono) |
| 4 | L− | Cold, left. Tied to AGND at the jack sleeve for unbalanced sources |
| 5, 6, 7, 8 | AGND | Ground between the two channels |
| 9 | R+ | Hot, right. Carries L+ when the module normals mono |
| 10 | R− | Cold, right. Carries L− when the module normals mono |
| 11 | AGND | |
| 12 | DO_R | Reserved for the pre-fader direct output, right (backlog). Unconnected on the prototype |

- Standard two-row numbering: odd pins on the key-slot row. On the flat cable conductor n is pin n, so the order across the cable is DO_L, AGND, L+, L−, four AGND, R+, R−, AGND, DO_R: each hot/cold pair sits between grounds.
- **Misplug rule:** a 2x4 power-ribbon socket (`CHAIN.md`) fits into the 2x6 shroud, but its key holds it centred on pins 3-10: V− on 3-4, PGND on 5-8, V+ on 9-10. With this pinout the rails reach only L± and R±, where the receiver sees them through its 20 kΩ / 30 kΩ legs (about 1 mA; the header pins go only into the 10 kΩ RFI resistors, no clamps), so no rail is shorted. PGND then lands on AGND pins 5-8: a second PGND–AGND join against the single-join rule of `CHAIN.md` (Grounding), accepted because it lasts only as long as the fault. Any pinout change keeps pins 3, 4, 9 and 10 for signals that tolerate the raw rails through at least 20 kΩ. A Eurorack 2x5 socket enters but sits half a pitch off and cannot mate (the intent of decision 41); the 2x6 socket cannot mate the 2x17 audio, 2x13 rear or 2x4 power headers.
- The cutoff CV jack is not on the input module: it belongs to the filter section on the channel card (decision 67).
- DO_L and DO_R are reserved for the stereo pre-fader direct output in the backlog (decision 68), so adding it later needs no interface change. Direct output jacks would sit on the input module.
- Connector on both boards: Adam Tech BHR-12-VUA (`SX-CONN-024`), straight, through-hole, holes 1.02 mm, 3 A per contact, no latches. Drawing BHR-XX-VUA: outer 22.86 × 8.80 mm, 9.10 mm tall, key slot 4.50 mm wide centred on the odd-pin side; check the KiCad footprint against it.
- The jack sleeves and the D-SUB shell connect to AGND through the module's AGND pins, matching the grounding rules in `CHAIN.md`.

## Cable (decisions 99, 180, 181)

Both the channel card and the module carry the 2x6 box header. They are linked by a self-made 12-way IDC flat cable wired 1:1 (pin n to pin n):

| Item | Part |
|---|---|
| Flat cable | Würth WR-CAB 63911215521CAB, 12-way, 1.27 mm, 28 AWG, 1 A, UL 2651 (`SX-WIRE-006`); one 1 m piece makes six cables |
| Sockets | Adam Tech FCS-12-SG IDC, 2x6, 1 A per contact (`SX-CONN-025`), one at each end, red conductor at pin 1, pressed with the chain cables' tool (decision 175); no strain relief needed |
| Length | 150 mm; the channel card layout places its header near the rear edge, within reach, and reports the position |
| On delivery | press one test cable first (the FCS drawing names no cable pitch or gauge) and check it 1:1 with a meter; dry-fit a 2x4 power socket in the shroud once to confirm it sits centred on pins 3-10 |
| Former parts | the ready-made Molex 217796-1101 (decision 179) and the hand-crimped KK cable (decision 99) are no longer used |

Module position (decision 160, `MECHANICAL.md`): the 6.3 mm module stands on edge below the rear rail, jacks stacked L/MONO above R, fixed only by the jack nuts on its rear strip.

Part numbers and dimensions come from the Adam Tech and Würth drawings (checked 2026-10-18). A module with a socket that plugs straight onto the card is not allowed: it would fix the module position and rule out cabled modules such as the D-SUB bundle.
