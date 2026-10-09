# RoHS audit of `docs/parts.csv`, 2026-10-09

The audit of decision 122 (rule: decision 116, invariant 9). A sub-agent went through every row of `docs/parts.csv` and recorded a `RoHS: <source>` in the Notes wherever the maker or a distributor states compliance. Spot-checked by the main session against Mouser (GPBS-850N, 1646S08-U, NE5532DR: all match).

## Counts (198 parts)

| | Rows |
|---|---|
| Already sourced before the audit | 20 (4 of them the blocked Alpha pots, SX-POT-003, -011, -012, -013) |
| Newly sourced | 47 (34 from Mouser's RoHS field, 13 from LCSC's; LCSC-only listings from little-known makers say "distributor field only") |
| Standard passives, sourced at BOM time (decision 122) | 103 |
| Gaps | 28 (3 with a maker part number, 25 with no part chosen yet) |

Where a row's part number was incomplete, the note names the orderable part checked (for example NE5532DR, TL072CDR, LM339DR, AD8273ARZ, DG413DY-T1-E3, LM13700MX/NOPB); the board session should copy it into the MPN column when it fixes the BOM. Not compliant: none. (Same-name parts from other makers are marked No or Obsolete at Mouser: Crydom SMBJ24A, Electroswitch GPBS-850N, ROHM LM339DR. The rows name other makers, so they are unaffected.)

## Gaps with a maker part number (the user decides: declaration or replacement)

| Part | Board | Why | Next step |
|---|---|---|---|
| SX-IC-001 SSI2144SS-TU | channel | not at Mouser; no statement from Electrokit, Sound Semiconductor's site or the datasheet (only a 260 °C reflow rating) | ask Sound Semiconductor (or Electrokit) for a RoHS declaration |
| SX-IC-002 SSI2162SS-TU | channel | same as the SSI2144 | same request |
| SX-IC-013 Alfa AS3046D | master | not at Mouser; no statement from Electric Druid or in the Alfa datasheet | ask Alfa (Riga) or Electric Druid |

## Gaps with no part chosen yet (source them when the part is chosen)

- Diodes: SX-D-001 (BZT52C6V2 class), SX-D-003 (1N4148W), SX-D-007 (SS14 class), SX-D-008 (M7)
- LEDs: SX-D-004, -005, -006 (3 mm, master meter)
- Alpha pots without a part number: SX-POT-005 to -010 (master and the channel AUX returns); SX-POT-004 has no maker
- Switches: SX-SW-002 (ground lift, decision 61), SX-SW-003 (power switch)
- Headers and jumper: SX-CONN-004, -005, -006, SX-MECH-001
- Heatsink: SX-MECH-002
- Printed washer SX-MECH-004: made in-house, out of scope unless the filament is to be declared
- Not used any more: SX-POT-002, SX-D-002, SX-CONN-003 (and SX-C-005)

## Compliant but End of Life at Mouser

- **SX-IC-014 THAT1646S08-U** (master main outputs, decision 83): Mouser stock 0. Buy prototype quantities early or plan a fallback (master session).
- **SX-R-021 Panasonic ERA-V33J102V** (SSI2144 tempco resistor, channel card; Compliant By Exemption).
- **SX-CONN-010 Molex 08-50-0114** (KK crimp terminal): still well stocked.

## Other findings

- Mouser describes **SX-SW-001 GPBS-850N** as "DPDT Non-Latching ON-(ON)", while the row (maker datasheet Rev 1, 2012) and decision 75 say latching. Most likely a catalogue text error; check the switches when the second Electrokit order arrives.
- Mouser lists the Omron relay G6K-2F-Y-DC12 under the maker name "Aratas"; SX-K-001 uses the LCSC Omron listing (C397194) instead.
- Four rows (SX-IC-009, SX-IC-014, SX-IC-015, SX-K-001) had unquoted commas in their Notes; quoted properly, so every row now parses as 7 columns.
