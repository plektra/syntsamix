# Chain interface

Status: **[confirmed]** by the user. Decisions behind this file: `DECISIONS.md` items 30, 38 to 42.

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
| 23 | AGND | 24 | SPARE1 |
| 25 | AGND | 26 | SPARE2 |
| 27 | AGND | 28 | SPARE3 |
| 29 | AGND | 30 | SPARE4 |
| 31 | AGND | 32 | SPARE5 |
| 33 | AGND | 34 | PFL_ACT |

Signal definitions:
- **MAIN, COMP, AUX1, AUX2, CUE (L/R):** current-summing buses. Each channel card drives them through a series resistor; the master card holds the virtual-earth summing amplifier for each. Bus resistor values are set during the schematic phase.
- **SC:** sidechain bus, mono. A channel with SC send on adds (L+R) through resistors, tapped pre-fader and pre-mute; the master sums it like the audio buses.
- **PFL_ACT:** logic, active low, open-collector (wired-OR). Pulled up on the master card; any channel with PFL pressed (or the master's SC listen button) pulls it to AGND. Placed at the cable edge, away from the audio buses, with the spares as a buffer.
- **SPARE1 to SPARE5:** unconnected on the prototype; reserved for future CV, mute groups and similar. Channel cards pass them through.

## Power ribbon: 8-pin IDC (2x4), shrouded and keyed

| Pin | Name |
|---|---|
| 1, 2 | V- (unregulated negative rail, about -20 V nominal) |
| 3, 4, 5, 6 | PGND |
| 7, 8 | V+ (unregulated positive rail, about +20 V nominal) |

- Pin 1 (red stripe) is the negative rail, the same habit as Eurorack, so the stripe always marks "negative".
- 10- and 16-pin sizes are deliberately avoided so a Eurorack power cable cannot be plugged in.
- Estimated current per rail at 16 cards: about 1.3 A, so about 0.65 A per pin (estimate; recheck once the card schematic exists, and check the connector's per-pin current rating).

## Grounding

- AGND (audio ribbon) and PGND (power ribbon) are separate all along the chain and join at **one point only: the master card**. Power enters the chain there.
- On a channel card, the regulator input capacitors return to PGND; the regulators' reference and all audio circuits use AGND.
- Keep ground current on channel cards small: LEDs and logic return to PGND, not AGND; op amps run rail to rail, so their supply current does not flow in ground.

## Points still open

- Supply rating for 16 cards.
- Connector and cable parts, and their current ratings.
