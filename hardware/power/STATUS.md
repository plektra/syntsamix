# Power board status

Updated 2026-10-06. Unblocked: the power budget is settled (decision 96).

## Where it stands

Not started.

## Next

1. Choose the isolated DC-DC module family and the brick voltage (24 or 48 V).
2. Draw the schematic: DC brick input on a locking DC jack, resettable fuse, reverse-polarity protection, power switch and LED, isolated DC-DC to ±20 V, LC filter, power ribbons to both chains and the master (decisions 60, 80, 81).

## Inputs

Load from decision 96 (`docs/decisions/system.md`; figures from `tools/system_power_budget.py` at 20 V raw):

- **Prototype (4 channel cards + master):** sizing figure 1.35 A (+20 V) and 1.11 A (−20 V), about 49 W; typical 0.83 / 0.69 A. Choose a DC-DC rated about 2 A per rail, from a family with larger versions (decision 60).
- **Full size (16 cards + master):** sizing figure 3.6 / 3.0 A per rail, about 132 W. This is the supply rating for 16 cards; the full-size module is bought only after the prototype cards are measured (decision 96).
- The raw rails must stay above about 19 V under load: the master's relay drop-out comparator trips at 17.9 V, and the LM317 needs about 2 V headroom.
- Capacitive load at switch-on: about 0.37 mF per raw rail for the prototype, 1.2 mF at full size (system validation finding 6); check the module's capacitive-load and start-up limits.
- Power ribbon headers on this board: up to about 0.76 A per pin; choose IDC headers rated at least 1 A per contact (decision 96).

## For /system

(none)
