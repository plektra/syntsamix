# Process decisions

Tools, workflow, part numbering, licensing, test points and assembly.

Part of the decision log; the index of all decisions is `INDEX.md`. Numbers are global and never reused. Text marked **[proposed]** still needs the user's confirmation.

## Decisions

10. Design tool: KiCad, using its MCP server
11. Write the specification before starting implementation
47. Tooling: one KiCad project per module with hierarchical sheets, custom symbol and footprint libraries, ngspice simulation, ERC/DRC checks, BOM export
63. Part numbering: each unique part type gets a project part number `SX-<category>-<nnn>` (register `docs/parts.csv`), used as Mouser's customer part number. KiCad symbols carry ProjectPN, Manufacturer, MPN, Supplier and SupplierPN fields, and BOMs are exported grouped by ProjectPN (`docs/PART-NUMBERING.md`)
70. Licensing is non-commercial source-available; the author keeps all commercial rights (`LICENSE.md`, `REUSE.toml`, texts in `LICENSES/`): hardware design files and documentation CC-BY-NC-SA-4.0, source code PolyForm-Noncommercial-1.0.0 with SPDX headers, repository configuration CC0-1.0. Applies from this change on; earlier commits stay under GPL-3.0
77. Test points: bare 1.5 mm SMD pads only (no wire loops), named on the silkscreen with their net and kept out of the BOM. Channel card pads: L/R receiver out, trim out and PREFILT, AGND (Input); L/R SSI2144 input, I-V out and POSTFILT, FCV, QW, AGND (Filter); VC, VB, L/R POSTFADE, SC_ENV (Level); L/R PRE (Routing); MV (Meter). The Chain and power sheet adds pads for the raw rails, +15 V, -15 V, +5 V and PGND
79. Assembly at JLCPCB (or PCBWay) for the prototype is planned around the LCSC stock check (`docs/lcsc-check.csv`, `tools/lcsc_check.py`). To cut extended-part setup fees, non-critical resistors use JLC basic values: bus resistors 22 kΩ (was 22.1 kΩ), the VCA input network 100 Ω (was 110 Ω), the cutoff offset injection 470 kΩ (was 499 kΩ, range still about ±32 mV) and the regulator dividers 200 Ω / 2.2 kΩ (15.1 V; was 120 Ω / 1.33 kΩ). Filter scaling, fader law and meter ladder keep their exact values. Not stocked at LCSC and to be consigned or hand-soldered: SSI2144, SSI2162, AD8273 and the ERA-V33 temperature-compensating resistor
116. RoHS compliance is a strict requirement (confirmed by the user 2026-10-09, during `/board channel-card mechanical parts`; for EU compliance). Every component on every board, and the boards themselves, must comply with the RoHS directive 2011/65/EU as amended by Delegated Directive (EU) 2015/863 (ten restricted substances); compliance through an Annex III exemption counts as compliant. A part may be chosen only when its maker or supplier states RoHS compliance (datasheet mark, declaration, or the distributor's RoHS field), and the source is recorded in the Notes column of `docs/parts.csv` as `RoHS: <source>`. Parts without such a statement (for example unbranded synth-DIY pots, knobs and jacks) are not chosen until compliance is confirmed. Fabrication and assembly are lead-free: lead-free HASL or ENIG board finish and lead-free assembly at JLCPCB (not the default leaded HASL), lead-free solder for hand soldering. The parts already registered are audited against this rule (all boards) (invariant 9, standard passives and the audit: item 122 in `system.md`)
124. A maker's general RoHS declaration covers that maker's standard parts (confirmed by the user 2026-10-09, `/system`; refines item 116). Taiwan Alpha's RoHS II declaration (2020-10-26, signed; 2011/65/EU with 2015/863, all ten substances) covers "our standard models or series", so every standard Alpha potentiometer counts as RoHS compliant under item 116, whichever reseller sells it (Thonk, Tayda), provided the part is genuine Alpha. This clears the channel pots CUTOFF, TRIM, AUX (Thonk, Alpha order codes RD901F-40-15K-B50K-0057, RD902F-40-15K-A100K-0057, RD902F-40-15K-A10K-0057) and RESONANCE (Tayda, RD901F-40-15K-C10K), and gives the master card's Alpha pots their source once a standard model is chosen. Supplier declarations received by email are kept in `docs/rohs/`, which is git-ignored: they are the suppliers' documents and not ours to publish in the public repository; `parts.csv` names the document, its date and scope. The same reading applies to other makers' general declarations

## Availability notes (checked 2026-10-03; recheck before ordering)

- SSI2144 (SSOP-16): not at the big distributors; sold through Sound Semiconductor's resellers. In stock at Thonk (about £3.75), also listed by synthCube and Modular Addict.
- SSI2164 (SOP-16): widely in stock (Thonk, Modular Addict, CE Distribution, AI Synthesis).
- THAT 2180A/B (SIP-8, through-hole): in stock at Newark, Farnell and element14 (tens to a few hundred units).
- Bourns PTA6043-2015DPB103 fader: active, about $1.92 at Mouser (about 1,300 in stock), €2.01 at Farnell. Alps RS60N11 is no longer manufactured.
- AD8273 (SOIC-14): active, widely stocked (DigiKey, Mouser, Arrow, Farnell), about $4.11. ADI's suggested replacement for the obsolete SSM2143.
- INA2137 (TI, dual, G = ½ or 2): active, $7.37 at quantity 1 at Mouser.
- SSM2143: obsolete.
- THAT1246: the SOIC-8 version (THAT1246S08-U) was in stock at Farnell and Newark, but one Farnell listing marks it "No Longer Manufactured"; the DIP-8 version shows a 20-week lead time. Treat it as at risk: buy prototype quantities plus spares early, and keep a fallback. Replaced by the AD8273 (proposed).
