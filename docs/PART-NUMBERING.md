# Part numbering and BOM fields

Status: **[confirmed]** by the user (decision 63).

## Project part numbers

Every unique part type gets one project part number, used on all boards:

```
SX-<category>-<nnn>
```

| Category | For |
|---|---|
| IC | Integrated circuits |
| R | Fixed resistors |
| C | Capacitors |
| POT | Panel potentiometers and faders |
| TRIM | Trimmers |
| D | Diodes and LEDs |
| Q | Transistors |
| CONN | Connectors, jacks, headers |
| SW | Switches and buttons |
| MECH | Mechanical parts (knobs, standoffs, panels) |

- The number names a part type, not a board position: every 100 nF X7R capacitor on every board shares one number. Board positions stay in the reference designators (C12, U3).
- Numbers are never reused. A changed part (different value, tolerance or package) gets a new number.
- The register of numbers is `docs/parts.csv`.

At Mouser, the project part number goes in the **customer part number** field, so it shows on order lines, invoices and bag labels. Suppliers without that field (Electrokit, Thonk) get the number written on the bag by hand.

## Symbol fields in KiCad

Every placed symbol carries these fields (blank until verified from a datasheet or a supplier page):

| Field | Content |
|---|---|
| `ProjectPN` | Project part number, for example `SX-IC-001` |
| `Manufacturer` | Manufacturer name |
| `MPN` | Manufacturer part number |
| `Supplier` | Preferred supplier (Mouser, Electrokit, Thonk) |
| `SupplierPN` | Supplier's own part number |
| `DNP` | Use KiCad's native Do Not Populate flag, not a field |

## BOM export

Each board's BOM is exported from KiCad grouped by `ProjectPN`, with columns: `ProjectPN`, `Manufacturer`, `MPN`, `Supplier`, `SupplierPN`, quantity per board, references. Order files are generated from it per supplier, multiplied by the number of boards plus spares. For Mouser the order file uses the upload columns Mouser part number (or MPN), quantity and customer part number.
