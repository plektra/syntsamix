# Mechanical interface

Status: **[confirmed]** where a decision is named; sections marked *open* are still to settle in a `/system mechanical` session. Decisions behind this file: `decisions/mechanical.md` items 55, 59, 75, 86, 106 to 109, 119 to 121, 160 and 162; `decisions/system-rules.md` item 118 (jack sizes).

The mechanical contract between the boards, the panels and the frame: what every board layout must fit. Changed only by a confirmed decision (invariant 5 in `ARCHITECTURE.md`).

## Format (decision 59)

Desktop unit. One PCB per channel strip under its own top panel strip; channel input jacks on the passive input module behind the rear panel (decision 62, position: decision 160); front and back aluminium rails cut to length with wedge side cheeks, so the top panels slope toward the player (decisions 160, 162); left to right: the channel strips, the master section, the power bay (decision 162); chain ribbons run under the strips between neighbours. Top and rear panels are black FR4 with white legends from the PCB maker.

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

Sixteen strips are 560 mm wide before the master section. Unit width: 35 mm × (channels + 5) plus the cheeks (master 4 strips, power bay 1; decision 162): about 315 mm for the prototype, 735 mm for 16 channels.

## Channel strip panel layout (decisions 55, 106)

One column, top (rear) to bottom (front), following the signal flow:

1. TRIM
2. [LOW-CUT]
3. Cutoff CV IN and CV OUT jacks (3.5 mm Thonkiconn, vertical, on the channel card; decisions 118, 165), side by side, IN left and OUT right, 16 mm between centres, centred on the strip (decision 166)
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
| Pots (RD901F-40, RD902F-40) | hold the panel: M7×0.75 bushing 5 mm, washer 0.4 mm and nut 2 mm (4.0 mm of thread used); shaft 6 mm T18 knurled, L = 15 mm from the body face, about 13.4 mm above the panel, push-on knobs (decision 114); bushing thread from Alpha's RD902F drawing, confirmed by Thonk support for the Thonk T18 pots (2026-10-09); check the nut fit on the first delivery |
| Fader (PTA6043, DP lever 15 mm) | frame top 6.5 mm above the PCB; screwed to the panel with two M2 screws (holes 71 mm apart) through 3.5 mm spacers; lever about 10 mm above the panel; slot about 4.5 × 65 mm |
| Top-side height limit | at most 9.0 mm under the panel (1 mm clearance), except parts that pass through it |
| Buttons (GPBS850L) | printed caps take up the height (measure a sample) |
| Channel meter (decision 119) | 0805 LEDs on the PCB under a 3D-printed bezel 11.6 mm tall, face flush with the panel top, through one slot about 5 × 49 mm; 8 windows at 6.0 mm pitch (about 4 × 4.5 mm, 1.5 mm walls); located by the slot and two printed pegs in 1.5 mm non-plated PCB holes; column position across the strip: *set at channel card layout* |
| Cutoff CV jacks (IN, OUT) | 3.5 mm Thonkiconn PJ398SM (decisions 118, 166), each: body 9 mm on the PCB, 1 mm printed washer on the unthreaded bushing collar to the panel underside, M6×0.5 nut on top (2.9 mm of thread left) |

Assembly order: screw the fader to the panel first, then solder it to the PCB, so its joints carry no stress. The fader is therefore hand-soldered, not assembled by the PCB maker.

## Card fixing (decisions 108, 120)

- Each top panel rests on the front and back 2020 rails, covering each rail's full 20 mm top face.
- One M3 button-head screw (ISO 7380) per end (two per panel), on the strip's centreline, into a drop-in M3 T-nut in the rail's top slot (slot centre 10 mm from the rail edge) (decision 120).
- A 3D-printed locating key under each panel end sits in the rail's top slot and stops the panel rotating in its plane (decision 120). Check rattle and twist on the prototype; the second screw per end (decision 108) returns if needed.
- The card hangs from its panel by the pots and the fader (decision 107); nothing on the PCB reaches over a rail.

## Chain headers (decision 109)

- Left to right: the channel strips, the master section (4 strips), the power bay (1 strip) (decision 162).
- Every channel card: audio (2×17) and power (2×4) **IN headers along the left edge, OUT headers along the right edge**, on the underside, long axis front to back, all at one distance from the front.
- That distance: chosen by the channel card layout (rear half, clear of the fader) and recorded here: *to be filled in*. The master card's headers follow it.
- Neighbours are linked by identical short jumper cables in a U-loop under the gap between card n's OUT and card n+1's IN (about 12 mm apart; about 60 to 80 mm of cable).
- Power ribbon: no jumper between the two groups of 8; chain 1 feeds the group next to the master (the prototype's cards), chain 2 the far group, each from the power board (decisions 80, 162). Each feed plugs into the power OUT header of its group's rightmost card, which is otherwise unused. The chain 1 feed runs under the master section; the chain 2 feed (about 0.5 m) along the rear floor in front of the input modules, on printed clips on the rear bottom angle (no cross band under the cards).
- Header orientation, socket crimping (pin 1 on pin 1 through the U-loop) and cable length: *to be fixed on a mock-up* before the first PCB order (two box headers about 12 mm apart on scrap board, a real 34-way cable).

## Rear panel and input module (decision 160)

| Item | Value |
|---|---|
| Rear panel | one black FR4 strip per channel, 34.8 mm wide (as the top panels), 1.6 mm; the master section and the power bay have their own rear pieces (decision 162) |
| Rear strip fixing | top: one M3 screw into a T-nut in the rear 2020 rail's back slot; bottom: one screw into an aluminium angle (about 20 × 20 × 2 mm, cut to length) along the rear bottom edge |
| Input module (6.3 mm) | PCB on edge in the front-to-back vertical plane, below the rear rail, centred on its strip; NYS216 jacks stacked, L/MONO above R, about 19 mm between centres; module about 40 mm tall; fixed only by the jack nuts on the rear strip; KK 254 header facing forward |
| Why stacked | NYS216 is 17.7 mm wide across its pin rows (footprint from Rean's drawing): two side by side need 35.4 mm, more than the 35.0 mm pitch |
| Rear inside height | about 60 mm: 20 mm rail plus about 40 mm of jack zone; *from the module layout* |
| Input cable (decision 99) | 100 mm, *provisional until the channel card layout places its KK header* |

## Frame shape (decision 160)

- Sloped: wedge side cheeks, flat bottom cover; the rear about 60 mm inside (above), the front a single 2020 rail, 20 mm inside (decision 162), so the top panels tilt about 6° toward the player.
- Front: no member below the front rail; the bottom cover screws into the rail's bottom slot. At the front only fader and part pins pass a card's underside; underside parts (decision 121) sit at least about 40 mm behind the front rail's inner face, where the floor is deep enough.
- The cards hang from their panels (decision 107): the tilt changes nothing on a board. The cheeks are the same for every channel count.

## Master section (decision 162)

| Item | Value |
|---|---|
| Width | 4 strips (140 mm), right of the channels; one top panel 139.8 mm wide, at most 360 mm long |
| Master card | at most 138 mm wide and 318 mm deep, hung 10 mm under its panel like a channel card (decision 107); chain headers on its left edge at the channel distance (decision 109) |
| Controls | 13 pots, 10 buttons, stereo meter, 5 gain-reduction LEDs, headphone jack; three columns (compressor and sidechain, AUX, master/phones/meter) set at layout |
| Meters | 0805 LEDs under printed bezels as decision 119: 2 × 12 at 6.0 mm pitch plus the 5 gain-reduction LEDs |
| Rear jacks | one rear piece 139.8 mm; 12 positions in 2 rows × 6 at about 23 mm: 11 jacks and the ground-lift switch, on two flat passive row boards fixed only by the jack nuts: output board (main L/R, AUX send 1 L/R, AUX send 2 L/R) and input board (AUX return 1 L/R, AUX return 2 L/R, SC EXT, ground lift), each cabled to the master card by one 26-pin ribbon (J603 outputs, J903 inputs and ground lift; decision 163). Needs the NYS216 at most about 17 mm tall above its board: *measure a sample*; if taller, on-edge 2-jack boards as the input module |
| Headphones | panel-mounted 6.3 mm stereo jack, nut on the master top panel, body through a cutout in the master card, short twisted cable to a header on the card; at least about 90 mm behind the front edge (about 30 mm of depth) |
| Regulators | U901-U903 TO-220 with one heatsink each (about 19.7 mm, ≤ 11.5 °C/W) on the card's underside, hand-soldered, behind the card's middle, up to 25 mm below the PCB (master-only exception to decision 121); ≥ 3 mm from each other, the frame and the cover (live tabs) |

## Power bay (decision 162)

| Item | Value |
|---|---|
| Width | 1 strip (35 mm) at the right end, with a plain top strip (34.8 mm; may carry the power LED) |
| Power board | on edge in the front-to-back plane, outline up to about 300 × 35 mm following the slope; hangs from the bay's top strip on two brackets and is fixed at its rear edge to the bay's rear strip; panels only, nothing on the cheeks; insulating hardware keeps PGND off the frame (invariant 8) |
| Rear strip | brick jack (KPJX-4S) and power rocker (decision 157, cutout 19.2 × 12.9 mm for a 0.8-1.2 mm panel, 19.4 mm for 1.3-2.0 mm) |
| Module sizes | planned: one power module for up to 8 channel cards, one for larger builds; same bay and ribbons |

## Underside and bottom cover (decision 121)

| Item | Value |
|---|---|
| Underside parts | chain headers at the edges (decision 109); elsewhere only hand-set parts (trimmers, jumper headers; decision 112), at most 10.5 mm below the PCB's bottom face |
| Keep-out | no underside parts other than the chain headers within 10 mm of each long edge, over the header length plus 15 mm front and back (*provisional until the cable mock-up*) |
| Bottom cover | detachable, a few captive or quarter-turn screws: at the rear into the bottom angle (decision 160), at the front into the front rail's bottom slot (decision 162); off without touching side cheeks, cards or feet |
| Feet | on the side cheeks or the rails, not on the cover |
| Inside height | 20 mm at the front rail, about 60 mm at the rear (decisions 160, 162); the mock-up checks that the header zone clears the sockets and U-loops |

## Panel hardware and ground (note)

Jack sleeves go to their own card's AGND; FR4 panels do not conduct (`CHAIN.md`, Grounding). Keep pot bushings and fader frames off AGND anyway, so metal panels (a product-version option, decision 59) need no ground rework. A jack's metal bushing is usually its sleeve, so on metal panels jacks would need insulated bushings or insulating washers.

## Open

Settled in this order, each by a decision:

1. *Underside:* the keep-out values and a check that the header zone clears sockets and U-loops, from the cable mock-up; the input cable length at the channel card layout (rear, frame shape, master section and power bay settled by decisions 160 and 162; underside rules and cover by decision 121)
2. *Heat:* ventilation for the typical dissipation inside the unit (about 28 W prototype to 77 W full size, `ARCHITECTURE.md`)
