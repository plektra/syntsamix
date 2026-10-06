# Chain interface

Status: **[confirmed]** by the user. Decisions behind this file: `decisions/system.md` items 30, 38 to 42, 66, 97 and 98.

Every channel card has two identical copies of each connector (IN and OUT), wired pin-for-pin straight through. The master card has one copy of each and sits at one end of the chain. Pin numbers follow the IDC convention: on the flat cable, pin n lies next to pin n+1, and pin 1 is on the red stripe.

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
- **SC_ENV:** ducking envelope (decisions 66 and 97), a negative control voltage driven by the master card at low impedance (feedback taken after its series resistor): 0 V = no ducking, −1 V = 10 dB of gain reduction at the channel VCA; the master's DEPTH sets the peak, 0 to −4 V (0 to 40 dB). A Schottky clamp on the master keeps it below about +0.3 V. A channel card (or AUX return) with DUCK on loads it with 30.1 kΩ into a virtual earth; with DUCK off it draws nothing. The scale does not depend on the fader position or the number of cards ducking.
- **SPARE2 to SPARE5:** unconnected on the prototype; reserved for future CV, mute groups and similar. Channel cards pass them through.

## Power ribbon: 8-pin IDC (2x4), shrouded and keyed

| Pin | Name |
|---|---|
| 1, 2 | V- (negative rail, about -20 V nominal; unregulated in general, from a DC-DC module on the prototype) |
| 3, 4, 5, 6 | PGND |
| 7, 8 | V+ (positive rail, about +20 V nominal; unregulated in general, from a DC-DC module on the prototype) |

- Pin 1 (red stripe) is the negative rail, the same habit as Eurorack, so the stripe always marks "negative".
- 10- and 16-pin sizes are deliberately avoided so a Eurorack power cable cannot be plugged in.
- Current per rail (decision 96, `tools/system_power_budget.py`): a channel card draws about 122 mA typical, 253 mA worst case; the sizing figure for shared parts is 189 mA per card. Power is injected in groups of 8 cards (decision 80): the power board (decision 81) has three power headers: one for the master card, chain 1 for cards 1 to 8 and chain 2 for cards 9 to 16, so each pin carries up to about 0.76 A (sizing figure). The IDC headers, sockets and cable must be rated at least 1 A per contact. The audio ribbon still runs through all cards.

## Grounding

- AGND (audio ribbon) and PGND (power ribbon) are separate all along the chain and join at **one point only: the master card** (net tie NT901). Power enters at the power board (decisions 80 and 81), which feeds the master card and chains 1 and 2 through separate power ribbons; PGND from every ribbon returns to the power board and reaches AGND only through the master card's star point.
- On a channel card, the regulator input capacitors return to PGND; the regulators' reference and all audio circuits use AGND.
- Keep ground current on channel cards small: LEDs and logic return to PGND, not AGND (this includes the PFL_ACT drivers and the button pull-downs, decision 98); op amps run rail to rail, so their supply current does not flow in ground.
- Jack sleeves connect to their own card's AGND. FR4 panels do not conduct, so jacks never touch the frame.
- The metal frame (rails, metal side cheeks) is bonded to the system star point at the master card only, through a ground-lift switch (lifted position: frame connected through a small resistor and capacitor).
- With the DC power brick the mixer floats from mains earth and takes its reference from connected gear, normally through the balanced outputs.

## Points still open

- Connector and cable part numbers and their per-pin current ratings: chosen during the channel card schematic (2.54 mm shrouded keyed box headers, 2x17 and 2x4; 28 AWG flat ribbon with IDC sockets); the power ribbon parts need at least 1 A per contact (decision 96).
