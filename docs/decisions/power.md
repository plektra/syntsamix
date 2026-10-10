# Power decisions

The power board (`hardware/power`): 24 V DC brick input, protection, non-isolated converters to the raw ±20 V chain rails. Chain voltage and power injection (40, 80) are in `system.md`.

Current rulings (decision 154): each entry says what holds now, with later refinements folded in. The full text (figures, simulations, sources, rejected options) is in `record/power.md` under the same number; read it when a figure or source is needed or before reopening a decision. Decision 100 in the record is the power board's design reference. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

60. Power comes from a certified 24 V DC brick through the power board to unregulated about ±20 V, LC-filtered, with per-card linear regulation. Power switch, resettable fuse, reverse-polarity protection, locking DC connector, power LED. A linear external supply box is a product-version option (details: 100)
81. The power input section is a separate small power board (`hardware/power`) beside the master card; it feeds the master and both power chains with short ribbons, keeping switching noise and its ground currents off the audio boards. The master takes power like a channel card and regulates locally
100. Power board conversion and parts. Non-isolated: the Class II brick provides the isolation and its negative is PGND (output must float, 101).
    - **Brick:** 24 V, Class II, floating output, R7B locking 4-pin DIN (pins 1, 4 = +24 V; 2, 3 = 0 V): Mean Well GSM120B24-R7B for the prototype, GSM220B24-R7B for 16 cards (145)
    - **Jack:** Kycon KPJX-4S right-angle at the rear edge; check polarity with a meter on the first brick
    - **Converters:** two TPS54560: a buck to +20 V and an inverting buck-boost to −20 V, about 2 A per rail, synchronised at 400 kHz in opposite phase from a 74HC14 oscillator (4.7 kΩ / 560 pF); UVLO start 21.1 V, stop 18.7 V. Raw rails stay above about 19 V under load
    - **Input protection:** 4 A resettable fuse (2920L400/30GR), SMBJ24A TVS, two SQJ457EP P-MOSFETs back to back (reverse block, about 7 ms soft turn-on); the switch drives the shared gate; power LED on the switched side
    - **Output:** one LC filter per rail shared by three headers (2.2 µH SRP7028A, 330 µF polymer, 100 µF electrolytic damping, 4.7 µF ceramic); one 2 A resettable fuse per rail per header (six; chain 2 header fitted on the prototype)
    - **Power ribbon parts (SX-CONN-008):** Würth 61200821621 header, 61200823021 IDC socket (1 A per contact, two per rail); hand-soldered, from a distributor
    - **Start-up ramp:** 47 nF C0G + 1N4148W from each output into FB (with a 1 MΩ and a second 1N4148W reset) give an 11 ms RC rise, so the brick sees about 54 W peak instead of tripping its hiccup limit
    - **Full size** (about 3.3 / 2.7 A per rail at the sizing figure, 4.4 / 3.7 A worst case): the +20 V buck probably carries it (thermal check); the −20 V inverter and the 2920 input fuse do not. Settled with the full-size supply after the prototype cards are measured (96)
    - Values and derivation: `hardware/power/scripts/design.py`. Still to choose: the 100 µF 50 V input bulk capacitor and the 10 pF C0G 100 V sync capacitor; power switch part
145. Full-size brick: Mean Well GSM220B24-R7B (SX-MECH-005, 221 W, Class II, same R7B plug and pinout, so jack and board unchanged); the prototype keeps the GSM120B24-R7B (SX-MECH-003). At the sizing figure it runs at about 60 % of its rating, about 81 % worst case. One brick and one mains cord only (two bricks rejected as unprofessional)
