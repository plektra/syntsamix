# Mechanical interface

Status: **[confirmed]** where a decision is named; sections marked *open* are still to settle in a `/system mechanical` session. Decisions behind this file: `decisions/mechanical.md` items 55, 59, 75, 86, 106 to 109 and 119 to 121; `decisions/system.md` item 118 (jack sizes).

The mechanical contract between the boards, the panels and the frame: what every board layout must fit. Changed only by a confirmed decision (invariant 5 in `ARCHITECTURE.md`).

## Format (decision 59)

Desktop unit. One horizontal PCB per channel strip under its own top panel strip; channel input jacks on the passive input module behind the rear panel (decision 62); front and back aluminium rails cut to length with side cheeks; chain ribbons run under the strips between neighbours. Top and rear panels are black FR4 with white legends from the PCB maker.

## Strip envelope (decision 106)

| Item | Value |
|---|---|
| Strip pitch | 35.0 mm |
| Top panel strip width | 34.8 mm (0.2 mm gap to the neighbour) |
| Panel material | FR4, 1.6 mm |
| Channel card PCB width | at most 33.0 mm, centred on the strip |
| Control area (between the rails' inner faces) | at most 320 mm deep (decisions 106, 108) |
| Top panel length | control area + 2 × 20 mm on the rails, at most 360 mm (decision 108) |
| Channel card PCB depth | fits between the rails: at most 318 mm (1 mm clearance to each rail; decision 108) |

Sixteen strips are 560 mm wide before the master section.

## Channel strip panel layout (decisions 55, 106)

One column, top (rear) to bottom (front), following the signal flow:

1. TRIM
2. [LOW-CUT]
3. Cutoff CV jack (3.5 mm Thonkiconn, vertical, on the channel card; decision 118), centred on the strip
4. CUTOFF
5. RESONANCE
6. [FILTER BYPASS]
7. AUX 1
8. AUX 2
9. [SC SEND] [DUCK] [COMP BUS] in one row (caps at most about 10 mm on an 11 mm pitch)
10. [PFL]
11. [MUTE]
12. 8-LED meter beside the 60 mm fader, at the front edge: printed bezel flush in one panel slot, 6.0 mm pitch, CLIP level with the fader's top travel end (decision 119)

## Panel stack (decision 107)

| Item | Value |
|---|---|
| PCB top to panel underside | 10.0 mm, set by the Alpha 9 mm pots (10 mm body) |
| Panel | 1.6 mm FR4; top surface 11.6 mm above the PCB |
| Pots (RD901F-40, RD902F-40) | hold the panel: M7×0.75 bushing 5 mm, washer 0.4 mm and nut 2 mm (4.0 mm of thread used); shaft 6 mm T18 knurled, L = 15 mm from the body face, about 13.4 mm above the panel, push-on knobs (decision 114); the T18 bushing thread is taken from Alpha's RD902F drawing, check on the first delivery |
| Fader (PTA6043, DP lever 15 mm) | frame top 6.5 mm above the PCB; screwed to the panel with two M2 screws (holes 71 mm apart) through 3.5 mm spacers; lever about 10 mm above the panel; slot about 4.5 × 65 mm |
| Top-side height limit | at most 9.0 mm under the panel (1 mm clearance), except parts that pass through it |
| Buttons (GPBS850N) | printed caps take up the height (measure a sample) |
| Channel meter (decision 119) | 0805 LEDs on the PCB under a 3D-printed bezel 11.6 mm tall, face flush with the panel top, through one slot about 5 × 49 mm; 8 windows at 6.0 mm pitch (about 4 × 4.5 mm, 1.5 mm walls); located by the slot and two printed pegs in 1.5 mm non-plated PCB holes; column position across the strip: *set at channel card layout* |
| Cutoff CV jack | 3.5 mm Thonkiconn PJ398SM (decision 118): body 9 mm on the PCB, 1 mm printed washer on the unthreaded bushing collar to the panel underside, M6×0.5 nut on top (2.9 mm of thread left) |

Assembly order: screw the fader to the panel first, then solder it to the PCB, so its joints carry no stress. The fader is therefore hand-soldered, not assembled by the PCB maker.

## Card fixing (decisions 108, 120)

- Each top panel rests on the front and back 2020 rails, covering each rail's full 20 mm top face.
- One M3 button-head screw (ISO 7380) per end (two per panel), on the strip's centreline, into a drop-in M3 T-nut in the rail's top slot (slot centre 10 mm from the rail edge) (decision 120).
- A 3D-printed locating key under each panel end sits in the rail's top slot and stops the panel rotating in its plane (decision 120). Check rattle and twist on the prototype; the second screw per end (decision 108) returns if needed.
- The card hangs from its panel by the pots and the fader (decision 107); nothing on the PCB reaches over a rail.

## Chain headers (decision 109)

- The master section sits at the right end of the unit; the power board beside it.
- Every channel card: audio (2×17) and power (2×4) **IN headers along the left edge, OUT headers along the right edge**, on the underside, long axis front to back, all at one distance from the front.
- That distance: chosen by the channel card layout (rear half, clear of the fader) and recorded here: *to be filled in*. The master card's headers follow it.
- Neighbours are linked by identical short jumper cables in a U-loop under the gap between card n's OUT and card n+1's IN (about 12 mm apart; about 60 to 80 mm of cable).
- Power ribbon: no jumper between cards 8 and 9; chain 1 (cards 1-8) and chain 2 (cards 9-16) are each fed from the power board (decision 80). Where a feed enters its group and how it is routed is open (Open, item 2).
- Header orientation, socket crimping (pin 1 on pin 1 through the U-loop) and cable length: *to be fixed on a mock-up* before the first PCB order (two box headers about 12 mm apart on scrap board, a real 34-way cable).

## Underside and bottom cover (decision 121)

| Item | Value |
|---|---|
| Underside parts | chain headers at the edges (decision 109); elsewhere only hand-set parts (trimmers, jumper headers; decision 112), at most 10.5 mm below the PCB's bottom face |
| Keep-out | no underside parts other than the chain headers within 10 mm of each long edge, over the header length plus 15 mm front and back (*provisional until the cable mock-up*) |
| Bottom cover | detachable, a few captive or quarter-turn screws into the rails' bottom slots; off without touching side cheeks, cards or feet |
| Feet | on the side cheeks or the rails, not on the cover |
| Cover inside height | clears the headers with sockets and the U-loops: *from the mock-up* (sets the frame height) |

## Panel hardware and ground (note)

Jack sleeves go to their own card's AGND; FR4 panels do not conduct (`CHAIN.md`, Grounding). Keep pot bushings and fader frames off AGND anyway, so metal panels (a product-version option, decision 59) need no ground rework. A jack's metal bushing is usually its sleeve, so on metal panels jacks would need insulated bushings or insulating washers.

## Open

Settled in this order, each by a decision:

1. *Rear and underside:* rear panel height, input module position, input cable length (decision 99); the cover's inside height and the keep-out values from the cable mock-up (underside rules and cover settled by decision 121)
2. *Master section and power board:* which end card 1 is (whether the prototype's chain 1 sits next to the master), where each power feed enters its group and how it is routed at full size (decisions 80, 81: about 280 mm or more to the far group), width in strips, headphone jack, heatsinks, brick jack, power and ground-lift switches
3. *Heat:* ventilation for about 30 W (prototype) to 84 W (full size) typical dissipation inside the unit
