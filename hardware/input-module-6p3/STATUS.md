# Input module status

Updated 2026-10-09 (RoHS note, decision 116).

- Schematic done, ERC clean. Header pinout confirmed as drawn (decision 105); no change needed.
- Cable to the channel card defined by decision 99 (`docs/INPUT-MODULE.md`, Cable): 1:1 KK 254 crimp cable, male headers stay on both boards. Length to set with the mechanical layout.
- PCB: not started. Fit it to the channel card's header position and the rear-panel jack spacing (decisions 59, 62).

## For /system

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; the audit of this board's registered parts is planned in /system.
