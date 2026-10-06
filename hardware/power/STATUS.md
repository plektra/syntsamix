# Power board status

Updated 2026-10-06.

## Where it stands

Not started.

## Next

1. Choose the isolated DC-DC module family and the brick voltage (24 or 48 V).
2. Draw the schematic: DC brick input on a locking DC jack, resettable fuse, reverse-polarity protection, power switch and LED, isolated DC-DC to ±20 V, LC filter, power ribbons to both chains and the master (decisions 60, 80, 81).

## Inputs

- Load: about 2.4 to 2.8 A per rail at ±20 V for 16 channel cards plus the master (about 100 to 115 W). Master card share from decision 95 (`hardware/master/scripts/power_budget.py`): typical +15 V 345 mA, −15 V 275 mA; worst case 730 / 606 mA.
- The raw rails must stay above about 19 V under load: the master's relay drop-out comparator trips at 17.9 V, and the LM317 needs about 2 V headroom.
- Open item: the supply rating for 16 cards (`docs/decisions/power.md`).

## For /system

(none)
