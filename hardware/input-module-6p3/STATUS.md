# Input module status

Updated 2026-10-09 (RoHS note, decision 116).

- Schematic done, ERC clean. Header pinout confirmed as drawn (decision 105); no change needed.
- Cable to the channel card defined by decision 99 (`docs/INPUT-MODULE.md`, Cable): 1:1 KK 254 crimp cable, male headers stay on both boards. Length to set with the mechanical layout.
- PCB: not started. Fit it to the channel card's header position and the rear-panel jack spacing (decisions 59, 62).

## Cost (2026-10-09)

- Jacks J1 and J2 are now Rean NYS216 (SX-CONN-015, decision 132) instead of the Neutrik NMJ6HCD2: about €3.50 per module in parts instead of about €6. Footprint `syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal` (rows 16.50 mm apart, panel cut-out 11.4 mm); its pin roles are inferred, so check them with a meter on the first delivered jack before ordering this PCB. ERC 0/0 after the change.
- Hand-soldered by the user, like every through-hole part (decision 133).
- Remaining cost: the KK 254 cable (two housings and 20 crimps, about €1.50). No further lever proposed.
- Component values (decision 134): this board has no resistors or capacitors; the rule in `CLAUDE.md` applies if any are added.

## RoHS

- **RoHS strict (decision 116, from the channel card session 2026-10-09):** every part on this board needs a maker or supplier RoHS statement recorded in `docs/parts.csv` as `RoHS: <source>` before ordering, and the board is ordered with a lead-free finish (lead-free HASL or ENIG) and lead-free assembly; invariant 9 (decision 122); standard passives get their source when the BOM is fixed; the audit of this board's registered parts runs before the first PCB order (`docs/CONTINUE-FROM-HERE.md`).

## For /system

(none)
