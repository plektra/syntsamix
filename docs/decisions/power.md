# Power decisions

The power board (`hardware/power`): DC brick input, isolated DC-DC to the raw ±20 V chain rails, protection. Chain voltage and power injection (decisions 40 and 80) are in `system.md`.

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

60. Prototype power: certified DC power brick (24 or 48 V) into the master section, isolated DC-DC module to about ±20 V, LC filter, per-card linear regulation. Power switch, resettable fuse, reverse-polarity protection, locking DC connector, power LED. A linear external supply box can be considered for a product version
81. The power input section is a separate small power board (`hardware/power`) next to the master card: DC brick input, fuse, reverse-polarity protection, power switch and LED, isolated DC-DC to ±20 V and LC filter. It feeds the master card and both power chains with short power ribbons, keeping switching noise and its ground currents off the audio boards. The master card takes power like a channel card and regulates locally

## Open items

- [x] Supply rating for 16 cards plus the master: decision 96 (`system.md`), 3.6 / 3.0 A per rail, about 132 W; prototype 1.35 / 1.11 A, DC-DC about 2 A per rail. Raw rails above about 19 V under load
