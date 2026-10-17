# Chain interface

Status: **[confirmed]** by the user. Decisions behind this file: `decisions/system.md` items 30, 38 to 42, 66, 97, 98, 101, 153, 175 and 178; `decisions/mechanical.md` item 162 (feed entry).

Every channel card has one audio and one power connector, each on a multi-drop flat cable that passes under all the cards with a socket at each card (decision 175). The audio cable comes in standard sections of 8 cards joined by a passive coupler board; the power cable is one section per group of 8 from the power board. The master card has one copy of each connector and sits at one end of the chain (the right end, decision 109). Any card can be unplugged without breaking the chain. Pin numbers follow the IDC convention: on the flat cable, pin n lies next to pin n+1, and pin 1 is on the red stripe.

## Audio ribbon: 34-pin IDC (2x17), shrouded and keyed

Pattern: ground on every odd pin, signal on every even pin, so each signal has a ground conductor on at least one side and every pair of signals is separated by a ground.

| Pin | Name | Pin | Name |
|---|---|---|---|
| 1 | AGND | 2 | MAIN_L |
| 3 | AGND | 4 | MAIN_R |
| 5 | AGND | 6 | COMP_L |
| 7 | AGND | 8 | COMP_R |
| 9 | AGND | 10 | AUX1_L |
| 11 | AGND | 12 | AUX1_R |
| 13 | AGND | 14 | AUX2_L |
| 15 | AGND | 16 | AUX2_R |
| 17 | AGND | 18 | CUE_L |
| 19 | AGND | 20 | CUE_R |
| 21 | AGND | 22 | SC |
| 23 | AGND | 24 | SC_ENV |
| 25 | AGND | 26 | SPARE2 |
| 27 | AGND | 28 | SPARE3 |
| 29 | AGND | 30 | SPARE4 |
| 31 | AGND | 32 | SPARE5 |
| 33 | AGND | 34 | PFL_ACT |

Signal definitions:
- **MAIN, COMP, AUX1, AUX2, CUE (L/R):** current-summing buses. Each channel card drives them through a series resistor; the master card holds the virtual-earth summing amplifier for each. Each channel drives every bus through 22 kΩ; the master's summing amplifiers use 22 kΩ feedback, so each channel sums at unity gain (decisions 74 and 79).
- **SC:** sidechain bus, mono. A channel with SC send on adds (L+R) through resistors, tapped pre-fader and pre-mute; the master sums it like the audio buses.
- **PFL_ACT:** logic, active low, open-collector (wired-OR). Pulled up on the master card; any channel with PFL pressed (or the master's SC listen button) pulls it to PGND (decision 98), so the LED and pull-up current returns through the power ribbons, not AGND. Placed at the cable edge, away from the audio buses, with the spares as a buffer.
- **SC_ENV:** ducking envelope (decisions 66 and 97), a negative control voltage driven by the master card at low impedance (feedback taken after its series resistor): 0 V = no ducking, −1 V = 10 dB of gain reduction at the channel VCA; the master's DEPTH sets the peak, 0 to −4 V (0 to 40 dB). A Schottky clamp on the master keeps it below about +0.3 V. A channel card (or AUX return) with DUCK on loads it with 30 kΩ (decision 153) into a virtual earth; with DUCK off it draws nothing. The scale does not depend on the fader position or the number of cards ducking.
- **SPARE2 to SPARE5:** unconnected on the prototype; reserved for future CV, mute groups and similar. Channel cards pass them through.

## Power ribbon: 8-pin IDC (2x4), shrouded and keyed

| Pin | Name |
|---|---|
| 1, 2 | V- (negative rail, about -20 V nominal; unregulated in general, from the power board's non-isolated converters on the prototype, decision 100) |
| 3, 4, 5, 6 | PGND |
| 7, 8 | V+ (positive rail, about +20 V nominal; unregulated in general, from the power board's non-isolated converters on the prototype, decision 100) |

- Pin 1 (red stripe) is the negative rail, the same habit as Eurorack, so the stripe always marks "negative".
- 10- and 16-pin sizes are deliberately avoided so a Eurorack power cable cannot be plugged in.
- Current per rail (decision 96, `tools/system_power_budget.py`): a channel card draws about 110 mA typical, 229 mA worst case on +15 V; the sizing figure for shared parts is 171 mA per card (after decision 143). Power is injected in groups of 8 cards (decision 80): the power board (decision 81) has three power headers: one for the master card, chain 1 for cards 1 to 8 and chain 2 for cards 9 to 16, so each pin carries up to about 0.68 A (sizing figure; 0.92 A at worst case). Chain 1 is the group next to the master; each chain is one multi-drop power section, its feed socket on the power board and a socket at each card of the group (decisions 162, 175, routing in `MECHANICAL.md`), so each card's socket contacts carry only that card's current (about 0.11 A at its worst case) and the cable conductors and the feed socket carry the group's. The power board comes as a module in the power bay; two sizes are planned (up to 8 cards, and larger), both with this pinout. The IDC headers, sockets and cable must be rated at least 1 A per contact (the Würth WR-CAB flat cable is rated 1 A max at 25 °C, decision 178). The audio cable passes all cards, its sections joined by the coupler board.

## Grounding

- AGND (audio ribbon) and PGND (power ribbon) are separate all along the chain and join at **one point only: the master card** (net tie NT901). Power enters at the power board (decisions 80 and 81), which feeds the master card and chains 1 and 2 through separate power ribbons; PGND from every ribbon returns to the power board and reaches AGND only through the master card's star point.
- The supply feeding the power ribbons must have a DC output that floats from mains earth (a Class II brick on the prototype; decision 101). PGND is earthed nowhere except through the master card's star point and the ground-lift switch. The mixer then floats from mains earth and takes its reference from connected gear, normally through the balanced outputs.
- On a channel card, the regulator input capacitors return to PGND; the regulators' reference and all audio circuits use AGND.
- Keep ground current on channel cards small: LEDs and logic return to PGND, not AGND (this includes the PFL_ACT drivers and the button pull-downs, decision 98); op amps run rail to rail, so their supply current does not flow in ground.
- Jack sleeves connect to their own card's AGND. FR4 panels do not conduct, so jacks never touch the frame.
- A patch cable between two channel cards' cutoff CV jacks (CV OUT into another card's CV IN, decision 165) joins their AGNDs in parallel with the audio ribbon's grounds. This is allowed: AGND to AGND inside the unit, a DC control signal (decision 166).
- The master's rear jacks sit on two passive row boards; their sleeves reach the master card's AGND through the ground conductors of ribbons J603 and J903 (decision 163).
- The metal frame (rails, metal side cheeks) is bonded to the system star point at the master card only, through a ground-lift switch (lifted position: frame connected through a small resistor and capacitor).

## Placement

Where the headers sit on each card, how the sections are built and where the coupler goes: `MECHANICAL.md`, Chain headers (decisions 109, 175).

## Points still open

- Connectors chosen: box headers Würth WR-BHD 61203421621 (2x17, audio; decision 117) and 61200821621 (2x4, power, 3 A per contact; decision 100), PCB holes 1.1 mm; power ribbon IDC socket Würth 61200823021 (1 A per contact; decision 100). Cable parts: audio IDC socket Würth 61203423021 (2x17, 1 A per contact, `SX-CONN-023`) and Würth WR-CAB flat cable, 28 AWG, 1.27 mm, 1 A max at 25 °C (34-way 63913415521CAB `SX-WIRE-004`; power a true 8-way 63910815521CAB `SX-WIRE-005`; decision 178). Checked 2026-10-17 (`part-facts`): the Würth socket datasheet (61203423021, MPI 002.000, 2022-08-30) gives 1 A per contact, a 2.54 mm grid (for 1.27 mm flat cable) and the strain relief, but names no cable gauge and does not say whether the socket can sit mid-cable; 3M TS-0080-12 gives the 3365 as 28 AWG 7 × 36 tinned stranded, 300 V, −20 to +105 °C, and no current rating. Distributor listings give 1 A to 1.8 A for 28 AWG 1.27 mm flat cables (Würth WR-CAB 1 A, Amphenol 135-2802 1.3 A, Letronic UL 2651 1.8 A), none from a maker datasheet read here. The 3365's missing rating is why the chain uses the Würth WR-CAB (decision 178): its datasheet states 1 A max at 25 °C with derating above, so the 8-card sizing figure (0.68 A per conductor) is checked against a Würth derating statement or a measurement on the first full group; the prototype's 4 cards draw 0.34 A per conductor. On delivery of the first sockets: check that the cable passes straight through (mid-cable use) before crimping a section.
- Coupler board (decision 175): two shrouded 2x17 headers as on the cards, pin n to pin n, same orientation; drawn before the first build of more than 8 cards.
