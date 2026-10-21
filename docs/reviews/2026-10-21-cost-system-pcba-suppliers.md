# Cost review: system, PCBA suppliers (JLCPCB vs AISLER vs PCBWay), 2026-10-21

Scope: system. Focus: compare other PCBA suppliers, such as AISLER in Europe and PCBWay. Nothing here is decided. Prices are before VAT and shipping, at USD 0.92 as in `docs/costs/overheads.csv`. Run on main at 3d5b736. It builds on `docs/reviews/2026-10-21-cost-system.md` from the same day.

**User response (2026-10-21):** stay with JLCPCB. Follow-up: research when the pre-reflow soldering charge applies (prototype lever 2).

## Short answer
On the published numbers, neither AISLER nor PCBWay beats JLCPCB for this BOM, and AISLER is far worse.

- **Why:** the three assembled designs have 230 distinct SMD part types (channel card 81, master 116, power 33, from `tools/costs.py`).
- **JLCPCB** charges only for the 28 extended types ($3.07 each).
- **AISLER** charges per distinct part.
- **Limit of this comparison:** AISLER's current rates sit behind its upload calculator, and PCBWay publishes no fee schedule. The figures below are bounds, not quotes.
- **Next step:** a free test quote from each on the power board would settle it (prototype lever 1).

## Figures
`python3 tools/costs.py estimate` (EUR). The figures are unchanged since the earlier review today.

| Item | 4 ch | 8 ch | 16 ch |
|---|---|---|---|
| channel-card parts | 168 | 332 | 656 |
| input-module-6p3 parts | 11 | 22 | 44 |
| master parts | 115 | 114 | 114 |
| power parts | 29 | 29 | 29 |
| JLCPCB fees | 144 | 150 | 162 |
| PCBs | 105 | 118 | 146 |
| FR4 panels | 55 | 64 | 88 |
| Frame, hardware, 24 V brick | 105 | 125 | 194 |
| Chain cables | 38 | 38 | 93 |
| Knobs and fader caps | 22 | 36 | 64 |
| **Total** | **793** | **1,028** | **1,590** |

- **JLCPCB prices confirmed:** the JLCPCB help page (read 2026-10-21, last updated 2026-09-09) still matches `overheads.csv`. Economic PCBA is $8.18 set-up, $1.53 stencil and $3.07 per extended type. Standard PCBA is $25.56 set-up, $8.21 stencil and $1.53 loading per type.
- **What a supplier switch can move:** only the "JLCPCB fees" line (144 at 4 ch) and the three assembled boards' share of "PCBs" (about 60). The rest of the total is parts and mechanics, which a PCBA supplier does not change.

## Comparison

| | JLCPCB (baseline) | AISLER (Germany) | PCBWay (China) |
|---|---|---|---|
| Model | Own library: basic and preferred free, extended $3.07 per type. Set-up $8.18 plus stencil $1.53 per design, $0.0016 per joint | Task-based: set-up, per-panel and per-part tasks. Parts bought from distributor partners. Customer-supplied part fee EUR 15 per part (2023) | Turnkey, kitted or hybrid. Quote per project after human review (1-2 working days). No public fee table |
| Per distinct SMD part | 0 for basic and preferred, $3.07 for extended | EUR 7.50 "part variance" per part (community post 2022-05-31). A forum snippet gives EUR 3.75 set-up per SMD part (2023). Neither is confirmed current | Not published. An old user report (about 2019) says 50 unique parts cost $142 for 10 boards, plus a $10 stencil, with about 2x parts markup |
| Stencil | $1.53 | EUR 5 + EUR 0.095 per cm² (2023), about EUR 15 for the 33 x 318 mm card | $10 up to 190 x 290 mm, free in some promos |
| Parts price | LCSC price | Distributor price plus handling; reel and cut-tape minimums not checked | Digi-Key, Mouser or Arrow plus an unpublished markup |
| Board size | Economic: 250 mm panel limit, 30-board cap | Not published | Not published |
| Hand-soldered chips | Consign or hand-solder (decisions 150, 155) | EUR 15 fee per customer-supplied part type | Kitted or consigned allowed |
| Lead time | Economic build 1-3 days | 6 to 9 working days (the site gives both) | 3-5 days after parts are in |
| Tax and shipping to EU | China: import VAT and a possible courier fee, not in the estimate | EU invoice, no customs, "free shipping" | China, same as JLCPCB |

Sources, all read 2026-10-21:
- [AISLER pricing](https://community.aisler.net/t/our-simple-pricing) (2023-08-27)
- [AISLER price cut post](https://community.aisler.net/t/amazing-assembly-gets-radical-price-cuts/905) (2022-05-31)
- [AISLER assembly page](https://aisler.net/products/assembly)
- [AISLER feature thread](https://community.aisler.net/t/standard-smd-components-without-setup-fee/1060)
- [PCBWay assembly page](https://www.pcbway.com/pcb-assembly.html)
- [lead-pcb comparison](https://lead-pcb.com/blog/jlcpcb-vs-pcbway) (2026-09-20, third party)
- [Anypcba](https://www.anypcba.com/decoding-pcbway-assembly-cost-a-comprehensive-guide.html) (its author calls the figures illustrative only)
- [JLCPCB price page](https://jlcpcb.com/help/article/pcb-assembly-price) (2026-09-09)

### AISLER bound (per-part fee only, not a quote)
Placements and handling are not added.

| Rate | Channel card (81 types) | Master (116) | Power (33) | Total |
|---|---|---|---|---|
| EUR 7.50 per type | 608 | 870 | 248 | 1,725 |
| EUR 3.75 per type | 304 | 435 | 124 | 863 |

- JLCPCB's whole fee line for the same prototype is EUR 144.
- AISLER's fees alone would be 6 to 12 times higher: about EUR 720 to 1,580 more per 4-channel build, or +90 % to +200 % on the EUR 793 total.
- Parts would be extra, at distributor prices rather than LCSC prices.
- The stencils (about EUR 15 for a card, more for the master) would also be extra.
- AISLER would only compete with fewer than about 20 distinct SMD types per design.
- **Bare boards only at AISLER** (2023 rates, 2-layer HASL budget, minimum 3 pieces; board areas not checked beyond the sizes in the STATUS files):
  - Channel card, 4 pieces: about EUR 40.
  - Master, 2 pieces: about EUR 71.
  - Power board, 3 pieces: about EUR 25.
  - Together about EUR 136, against about EUR 60 in the JLCPCB estimate. Not a saving either.
  - Lead-free finish is unchecked (invariant 9).

### PCBWay
- It cannot be bounded from public data.
- The old report implies a lower per-type fee than AISLER but a parts markup of about 2x.
- SMD parts on the JLCPCB-placed boards cost EUR 10.28 per card, 13.02 for the master and 11.70 for the power board. A 2x markup is therefore about EUR 70 at 4 channels. The expensive chips are bought separately anyway.
- PCBWay could land close to JLCPCB. Nothing in the evidence supports claiming it.
- It has no "extended" class, so its quote depends on how many distinct parts it must source.

## Levers
None of these is a saving I can confirm. This was a comparison, not a hunt for savings.

### Prototype
1. **Request a quote from AISLER and PCBWay for the power board** (33 types, 75 placements, 177 x 35 mm), and one from JLCPCB for the same Gerbers and BOM.
   - Cost: EUR 0 and about 30 minutes.
   - It gives real numbers where the web gives bounds.
   - The JLCPCB quote also confirms two assumptions in `overheads.csv`: the extended fee billed per design, and the two-board minimum.
   - Touches nothing under decision 135.
2. **Check JLCPCB's "pre-reflow soldering" line on the first quote.** This is a risk, not a saving.
   - The price page lists $0.016 per joint for it, next to $0.0016 per joint for SMT assembly.
   - `overheads.csv` does not model it.
   - If it applied to every joint (about 8,400 at 4 ch, from 2,810 placements at 3 joints each), it would add about $135, or EUR 124.
   - Which orders trigger it is UNVERIFIED.
   - It matters here because it would move the break-even toward PCBWay.
   - Source: JLCPCB help page, 2026-09-09.
3. **Do not move the prototype to AISLER or PCBWay for cost.** Choosing AISLER for convenience (no import VAT or customs, 6 to 9 days) would cost about EUR 720 to 1,580 more on fees alone. That is the user's decision.

### Console and product (16 channels, volume)
1. **Re-run the comparison with real quotes at 16 cards and about 50 consoles.** Volume changes the ranking.
   - AISLER's part fee is once per job. Its 2022 example falls from EUR 77.80 for one prototype of 10 types to 355 for 100 pieces.
   - JLCPCB Standard PCBA (needed above 30 cards) adds $1.53 loading per type. For 230 types that is about EUR 320 per order.
   - PCBWay's base fee is only available as an illustration: $50 to $150 per project (third party, UNVERIFIED).
   - A European assembler might win once reel purchases and customs are counted. Today there is no number.
2. **JLCPCB manual assembly of through-hole parts: possible labour saving, UNVERIFIED.**
   - JLCPCB lists $0.0164 per joint for manual assembly, plus $3.58 per order for hand-soldering labour.
   - The card has 31 on-board through-hole parts and the input module 3. Many are panel-mounted, so this may not be possible.
   - Decision 133 puts all through-hole parts on the user. The question to ask JLCPCB is whether it can solder headers, buttons and trimmers.
   - Touches nothing under decision 135.
3. **Returning the hand-soldered chips to JLCPCB placement for production** is already product lever 2 in the earlier report. It is not re-priced here.

## Rule findings
- No new E24 or JLCPCB-class findings. I did not re-audit them.
- A supplier change would reopen decisions 79 and 137. The fee-free-class rule means nothing at AISLER, which charges per type.
- `tools/lcsc_check.py` and `docs/lcsc-check.csv` are LCSC-based and would not carry over.

## Questions for the user
- Is the interest in AISLER about cost, or about convenience (EU delivery, no import tax, no China shipping)? On cost it loses by hundreds of euros.
- Do JLCPCB shipping, import VAT and any courier fee (none in the estimate) justify asking AISLER for a quote? A quote needs an upload but no payment.
- Should the extended-type count (28) and the 27 hand-soldered chips stay fixed while quotes are compared? A change in either moves the JLCPCB figure the others are measured against.

## Prices to update
- None. JLCPCB's USD figures match `overheads.csv`.
- Optional row if you want the pre-reflow risk tracked: `jlc_prereflow_usd_per_joint,0.016,"JLCPCB pre-reflow soldering per joint (help page 2026-09-09), not modelled: check on the first quote"`.

## Not checked
- **AISLER's current fees.** The upload calculator needs a project. The figures are from 2022 and 2023 posts and a forum snippet. That snippet contradicts the 2022 post (EUR 75 set-up and EUR 0.38 per placement, against EUR 7.50 per type and EUR 0.04 per placement). Treat the table as order of magnitude.
- **Board size limits, minimum pitch, lead-free finish and RoHS declarations** at AISLER and PCBWay.
- **Any PCBWay fee schedule.** None is public.
- **Shipping, import VAT and duty** for each route, including IOSS and the EUR 150 threshold. I found no source.
- **Other suppliers** (Eurocircuits, NextPCB, Seeed Fusion). A forum post puts Eurocircuits at 2 to 4 times AISLER.
- **Panelisation.** I checked nothing for AISLER or PCBWay.

## Follow-up: when does JLCPCB's pre-reflow soldering fee apply? (2026-10-21)

Asked by the user after deciding to stay with JLCPCB. Researched in the main session from JLCPCB's own pages. All pages were read 2026-10-21.

**Finding: no JLCPCB page defines the fee.** The evidence says it is a charge for through-hole joints soldered in the reflow oven (pin-in-paste). It is not a charge on every SMT joint. The 4-channel risk of about EUR 124 (prototype lever 2) is therefore very likely zero for this project, provided the order follows decision 133. Confirm on the first quote, or ask JLCPCB support.

Evidence:
- **The price page names the fee but does not explain it.** The [price page](https://jlcpcb.com/help/article/pcb-assembly-price) (2026-09-09) lists "Pre-reflow Soldering: 1–1,000,000 joints: $0.016/joint" with the same rate for Economic and Standard. Its "Fee Details and Explanations" section covers set-up, stencil, SMT, manual assembly, extended parts, feeder loading, X-ray, handling and the single-board surcharge, but not pre-reflow.
- **The FAQ and capabilities pages do not mention it.** The [FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs) (2026-09-09) and the [capabilities page](https://jlcpcb.com/capabilities/pcb-assembly-capabilities) list set-up, stencil, SMT per joint, hand-soldering labour and manual assembly per joint. Parts marked "wave soldering" in the parts library are assembled manually, at the hand-soldering labour fee plus the manual per-joint fee.
- **JLCPCB's default for through-hole parts is soldering after reflow, not in the oven.** The [assembly guide](https://jlcpcb.com/blog/printed-circuit-board-assembly) (2026-09-09) says: "reflow soldering for SMT components, followed by wave soldering or selective soldering for through-hole components".
- **JLCPCB does support pin-in-paste, but only on request.** The [mixed-technology blog](https://jlcpcb.com/blog/mixed-technology-pcb-assembly-combining-smt-and-tht) (2026-08-24) and the [pin-in-paste stencil guide](https://jlcpcb.com/blog/pin-in-paste-through-hole-reflow-stencil-guide) (2026-08-25) describe it: through-hole parts are "inserted before the reflow process". The customer asks for it: "note which parts should be pin-in-paste in your order remarks", with the through-hole pads on the paste layer and the parts listed in the BOM. Neither page names a fee.
- **The rate fits a through-hole charge.** $0.016 per joint is the same order as manual assembly ($0.0164 per joint) and ten times SMT ($0.0016). That suits labour on inserted through-hole parts, not a surcharge on every SMT joint. This is an inference.
- **No third-party source explains it.** A third-party [overview](https://techoverflow.net/2024/04/09/jlcpcb-pcba-assembly-price-overview/) predates the line. JLCPCB's [newer through-hole assembly service](https://github.com/rjwalters/kicad-tools/issues/7239) (third party, 2026-10-18), offered in both Economic and Standard, is the likely context for the new line.

What this means for this project:
- **The fee should not apply to the prototype if the order follows decision 133.** Under decision 133, JLCPCB places SMD parts only and the user hand-solders every through-hole part. The position file and BOM sent to JLCPCB must therefore leave out all through-hole parts (`tools/costs.py` already treats them that way).
- **Keep pin-in-paste out of the order.** Do not mark through-hole parts for pin-in-paste in the order remarks, and do not put through-hole pads on the paste layer. Check both when the fabrication outputs are written.
- **If the quote still shows the line, ask JLCPCB support before paying.** That would settle what the fee is.
- **Production:** if through-hole assembly is ever moved to JLCPCB (console lever 2), this fee or the manual-assembly fee would apply to those joints. With about 31 through-hole parts per card that is roughly 31 × 3 joints × 16 cards ≈ 1,500 joints, or about $24 at $0.016 per joint. That is far less than the EUR 124 worst case, and it buys an hour or more of soldering.
- **No change to `overheads.csv`.** The optional tracking row above is no longer needed. A checklist item for the fabrication outputs covers it.
