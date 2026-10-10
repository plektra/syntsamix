# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Cost estimate from the schematic BOMs, and the ledger of realized costs (decision 136).

Estimate (tracked inputs, repeatable):
  python3 tools/costs.py estimate [--channels N[,N...]] [--md] [--fees-per-design]
                                                          cost of a build with N channel cards; several counts are shown
                                                          side by side (default: the standard builds 4, 8 and 16); shared
                                                          extended types are billed per design when jlc_fee_per_design is 1
                                                          in overheads.csv (the default) or with --fees-per-design
  python3 tools/costs.py drivers [--board B] [--top N]    most expensive part types per board
  python3 tools/costs.py unpriced                         part types with no price yet (fill docs/costs/prices.csv)
  python3 tools/costs.py extended                         SMD part types that cost a JLCPCB extended-part fee or are consigned
Inputs: the KiCad schematics (BOM by ProjectPN, DNP excluded; a symbol field Assembly = "hand ..." marks a user-soldered SMD part, decision 150), docs/lcsc-check.csv (LCSC price and
JLCPCB class, MOQ), docs/costs/prices.csv (prices for parts LCSC does not sell, and overrides; optional moq column),
docs/costs/overheads.csv (exchange rates, PCB, panel, JLCPCB fee and frame figures).

Ledger of money actually spent (private: git-ignored, kept in the main checkout so every worktree sees it;
SYNTSAMIX_LEDGER=<path> overrides the location, for tests):
  python3 tools/costs.py ledger add --supplier S --category C --amount A [--currency EUR] [--date YYYY-MM-DD]
          [--board B] [--ref ORDER] [--desc TEXT]
  python3 tools/costs.py ledger [--md]                    totals by category, board and supplier
Categories: parts, pcb, assembly, panels, mechanical, tools, shipping, tax, other.
"""
import argparse, csv, datetime, os, re, subprocess, sys, tempfile
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KICAD = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"
# the realistic configurations the cost is tracked for (the user, 2026-10-10)
STANDARD_BUILDS = [4, 8, 16]

BOARDS = {
    "channel-card": "hardware/channel-card/channel-card.kicad_sch",
    "input-module-6p3": "hardware/input-module-6p3/input-module-6p3.kicad_sch",
    "master": "hardware/master/master.kicad_sch",
    "power": "hardware/power/power.kicad_sch",
}
PER_CHANNEL = ("channel-card", "input-module-6p3")
THT_HINTS = ("Potentiometer", "Jack", "PinHeader", "IDC-Header", "Molex", "TO-220", "Relay",
             "SW_Latching", "CP_Radial", "Fuse_2920", "LED_D3.0mm", "heatsink", "KPJX")
NO_FEE = ("basic", "preferred")  # JLCPCB library classes without the extended-part fee in Economic PCBA (decision 137)
JLC_SUPPLIED = ("basic", "preferred", "extended")  # classes JLCPCB buys for the assembly
CATEGORIES = ("parts", "pcb", "assembly", "panels", "mechanical", "tools", "shipping", "tax", "other")
LEDGER_FIELDS = ["date", "supplier", "ref", "category", "board", "description", "amount", "currency", "eur"]


def main_checkout():
    """Root of the main checkout (not a worktree), where the private ledger lives."""
    try:
        common = subprocess.run(["git", "-C", ROOT, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True, check=True).stdout.strip()
        return os.path.dirname(common)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ROOT


LEDGER = os.environ.get("SYNTSAMIX_LEDGER") or os.path.join(main_checkout(), "docs", "costs", "ledger.csv")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if any((v or "").strip() for v in r.values())]


def overheads():
    o = {}
    for r in read_csv(os.path.join(ROOT, "docs", "costs", "overheads.csv")):
        o[r["item"]] = float(r["value"])
    return o


def to_eur(amount, currency, o):
    currency = currency.upper()
    if currency == "EUR":
        return amount
    rate = o.get(f"rate_{currency.lower()}_eur")
    if rate is None:
        sys.exit(f"No exchange rate rate_{currency.lower()}_eur in docs/costs/overheads.csv")
    return amount * rate


def moq(text):
    """Minimum order quantity from a CSV field; blank or unreadable means 1 (JLCPCB: no minimum for parts in stock)."""
    return int(text) if text and str(text).strip().isdigit() else 1


def prices(o):
    """ProjectPN -> dict(eur, source, jlc): jlc is basic, extended, consign or hand."""
    p = {}
    for r in read_csv(os.path.join(ROOT, "docs", "lcsc-check.csv")):
        if r.get("Price"):
            try:
                usd = float(r["Price"])
            except ValueError:
                continue
            p[r["ProjectPN"]] = {"eur": to_eur(usd, "USD", o), "source": f"LCSC {r['LCSC']}",
                                 "jlc": r.get("Class") or "extended", "moq": moq(r.get("MOQ"))}
    for r in read_csv(os.path.join(ROOT, "docs", "costs", "prices.csv")):
        p[r["ProjectPN"]] = {"eur": to_eur(float(r["unit_price"]), r["currency"], o),
                             "source": f"{r['source']} {r['date']}", "jlc": r["jlc"], "moq": moq(r.get("moq"))}
    return p


E24 = (10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82, 91)
# generic USD prices for small parts with no price of their own: (footprint prefix, USD)
GENERIC = (("R_0805", 0.002), ("R_0603", 0.002), ("R_2512", 0.03), ("C_0805", 0.005), ("C_1206", 0.02),
           ("C_1210", 0.05), ("LED_0805", 0.01), ("D_SOD-123", 0.01), ("D_SMA", 0.02), ("D_SMB", 0.05),
           ("D_SMC", 0.08), ("Fuse_", 0.15), ("SOT-23", 0.02), ("SOT-89", 0.05))


def is_e24(value):
    m = re.match(r"^(\d+)([RkMpnu]?)(\d*)", value)
    if not m:
        return False
    v = float(m.group(1) + ("." + m.group(3) if m.group(3) else ""))
    while v >= 100:
        v /= 10
    while v < 10:
        v *= 10
    return any(abs(v - e) < 0.01 for e in E24)


def generic(item, o):
    """Fallback price for a small SMD part; resistors and capacitors outside E24 count as extended (decision 134)."""
    fp = item["footprint"].split(":")[-1]
    for prefix, usd in GENERIC:
        if fp.startswith(prefix):
            passive = fp[:2] in ("R_", "C_")
            jlc = "basic" if (passive and is_e24(item["value"])) or fp.startswith("LED_0805") else "extended"
            return {"eur": to_eur(usd, "USD", o), "source": "generic estimate", "jlc": jlc}
    return None


def priced(items, p, o):
    """Attach a price to each BOM item: own price first, then the generic fallback."""
    for i in items:
        pr = p.get(i["pn"]) or generic(i, o)
        i["price"] = pr
        if pr and pr["jlc"] == "hand":
            i["tht"] = True
    return items


def bom(board):
    """List of dict(pn, value, footprint, qty, tht) for one board, grouped by ProjectPN."""
    sch = os.path.join(ROOT, BOARDS[board])
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "bom.csv")
        subprocess.run([KICAD, "sch", "export", "bom", "--fields",
                        "ProjectPN,Value,Footprint,Assembly,${QUANTITY}", "--labels", "pn,value,footprint,assembly,qty",
                        "--group-by", "ProjectPN,Value,Footprint,Assembly", "--exclude-dnp", "-o", out, sch],
                       capture_output=True, check=True)
        rows = read_csv(out)
    items = []
    for r in rows:
        fp = r["footprint"]
        items.append({"pn": r["pn"] or f"(no PN) {r['value']}", "value": r["value"], "footprint": fp,
                      "qty": int(r["qty"]), "tht": (not fp) or any(h in fp for h in THT_HINTS)
                      or (r.get("assembly") or "").startswith("hand")})   # Assembly field: hand-soldered SMD (decision 150)
    return items


def all_boms(o):
    p = prices(o)
    return {b: priced(bom(b), p, o) for b in BOARDS}


def estimate(channels, o, md, per_design=False):
    lines, total, unpriced = estimate_lines(channels, o, per_design)
    title = f"Estimate, {channels} channel(s), before VAT and shipping"
    if md:
        print(f"| {title} | EUR |\n|---|---|")
        for k, v in lines:
            print(f"| {k} | {v:,.0f} |")
        print(f"| **Total** | **{total:,.0f}** |")
    else:
        print(title)
        for k, v in lines:
            print(f"  {k:78s} {v:9,.0f}")
        print(f"  {'Total':78s} {total:9,.0f}")
    if unpriced:
        print(f"\nUnpriced part types (not in the total): {len(unpriced)}; list them with: python3 tools/costs.py unpriced")
    return total


def compare(channel_counts, o, md, per_design=False):
    """Side-by-side estimate of several builds (the standard set is 4, 8 and 16 channels)."""
    runs = [estimate_lines(n, o, per_design) for n in channel_counts]
    # same lines in the same order for every build; the counts in brackets differ, so label by the text before them
    labels = [k.split(" (")[0] for k, _ in runs[0][0]]
    heads = [f"{n} ch" for n in channel_counts]
    title = "Estimate before VAT and shipping, EUR"
    if md:
        print(f"| {title} | " + " | ".join(heads) + " |\n|---|" + "---:|" * len(heads))
        for i, k in enumerate(labels):
            print(f"| {k} | " + " | ".join(f"{r[0][i][1]:,.0f}" for r in runs) + " |")
        print("| **Total** | " + " | ".join(f"**{r[1]:,.0f}**" for r in runs) + " |")
    else:
        print(f"{title:56s}" + "".join(f"{h:>9s}" for h in heads))
        for i, k in enumerate(labels):
            print(f"  {k:54s}" + "".join(f"{r[0][i][1]:9,.0f}" for r in runs))
        print(f"  {'Total':54s}" + "".join(f"{r[1]:9,.0f}" for r in runs))
    unpriced = set().union(*(r[2] for r in runs))
    if unpriced:
        print(f"\nUnpriced part types (not in the totals): {len(unpriced)}; list them with: python3 tools/costs.py unpriced")


def estimate_lines(channels, o, per_design=False):
    """(lines, total, unpriced) of a build with the given number of channel cards."""
    boms = all_boms(o)
    count = {"channel-card": channels, "input-module-6p3": channels, "master": 1, "power": 1}
    # JLCPCB assembles at least jlc_min_assembled boards of a design (the input module has no SMD parts)
    built = {b: n if b == "input-module-6p3" else max(n, int(o["jlc_min_assembled"])) for b, n in count.items()}
    lines, total, unpriced = [], 0.0, set()
    ext_types = set()
    ext_billed = 0  # extended types counted once per design that uses them
    moq_extra = 0.0
    for b, items in boms.items():
        parts_one = sum(i["price"]["eur"] * i["qty"] for i in items if i["price"])
        smd_one = sum(i["price"]["eur"] * i["qty"] for i in items if i["price"] and not i["tht"])
        unpriced |= {i["pn"] for i in items if not i["price"]}
        # through-hole parts are bought for the boards used; SMD parts for every board JLCPCB assembles
        cost = parts_one * count[b] + smd_one * (built[b] - count[b])
        lines.append((f"{b} parts ({count[b]} used, {built[b]} assembled)", cost))
        total += cost
        # JLCPCB buys at least a part's minimum order quantity for each assembled design (in-stock parts: 1)
        moq_extra += sum(max(0, i["price"].get("moq", 1) - i["qty"] * built[b]) * i["price"]["eur"]
                         for i in items if i["price"] and not i["tht"] and i["price"]["jlc"] in JLC_SUPPLIED)
        board_ext = {i["pn"] for i in items if not i["tht"] and (not i["price"] or i["price"]["jlc"] not in NO_FEE)}
        ext_types |= board_ext
        ext_billed += len(board_ext)
    designs = [b for b in BOARDS if b != "input-module-6p3"]
    smd_parts = sum(i["qty"] * built[b] for b, items in boms.items() for i in items if not i["tht"])
    per_design = per_design or bool(o.get("jlc_fee_per_design"))
    n_ext = ext_billed if per_design else len(ext_types)
    fees = (n_ext * to_eur(o["jlc_extended_fee_usd"], "USD", o)
            + len(designs) * o["jlc_setup_eur_per_design"]
            + smd_parts * to_eur(o["jlc_per_smd_part_usd"], "USD", o))
    billing = f"{n_ext} billed per design, {len(ext_types)} unique" if per_design else f"{len(ext_types)}"
    # Economic PCBA takes at most this many boards of a design unpanelled; the channel card is too long for its 250 mm panel
    over = [b for b in designs if built[b] > o["jlc_economic_max_boards"]]
    note = f"; {', '.join(over)} above Economic's {o['jlc_economic_max_boards']:.0f}: Standard PCBA not modelled" if over else ""
    lines.append((f"JLCPCB fees ({billing} extended/consigned types, {len(designs)} designs, {smd_parts} SMD parts{note})", fees))
    total += fees
    if moq_extra:
        lines.append(("Parts bought up to JLCPCB minimum order quantities", moq_extra)); total += moq_extra
    pcb = (max(o["pcb_min_eur_per_design"], o["pcb_channel_eur"] * built["channel-card"])
           + max(o["pcb_min_eur_per_design"], o["pcb_input_eur"] * channels)
           + max(o["pcb_min_eur_per_design"], o["pcb_master_eur"] * built["master"])
           + max(o["pcb_min_eur_per_design"], o["pcb_power_eur"] * built["power"]))
    lines.append(("PCBs", pcb)); total += pcb
    panels = max(o["pcb_min_eur_per_design"], o["panel_strip_eur"] * channels) + o["panel_master_rear_eur"]
    lines.append(("FR4 panels", panels)); total += panels
    # prototype brick up to one power board's worth of channels, full-size brick above (decision 145)
    brick_pn = "SX-MECH-003" if channels <= o["brick_proto_max_channels"] else "SX-MECH-005"
    frame = o["frame_fixed_eur"] + o["frame_eur_per_channel"] * channels + prices(o)[brick_pn]["eur"]
    lines.append((f"Frame, hardware, ribbons, 24 V brick ({brick_pn})", frame)); total += frame
    knobs = o["knobs_eur_per_channel"] * channels + o["knobs_master_eur"]
    lines.append(("Knobs and fader caps (no schematic symbols)", knobs)); total += knobs
    if any(i["price"] and i["price"]["jlc"] == "consign" for items in boms.values() for i in items):
        lines.append(("Consigned parts handling", o["consign_eur_per_order"])); total += o["consign_eur_per_order"]
    return lines, total, unpriced


def drivers(board, top, o):
    boms = all_boms(o)
    for b in ([board] if board else BOARDS):
        rows = sorted(((i["price"]["eur"] * i["qty"], i["qty"], i["pn"], i["value"], i["price"]["source"])
                       for i in boms[b] if i["price"]), reverse=True)
        print(f"== {b}: parts EUR {sum(r[0] for r in rows):,.2f} per board")
        for c, q, pn, v, s in rows[:top]:
            print(f"  {c:7.2f}  {q:3d} x {pn:12s} {v[:28]:28s} {s}")


def extended(o):
    """SMD part types that cost a JLCPCB extended-part fee (or are consigned), per board, with the boards that share them."""
    boms = all_boms(o)
    types = {}
    for b, items in boms.items():
        for i in items:
            if not i["tht"] and (not i["price"] or i["price"]["jlc"] not in NO_FEE):
                t = types.setdefault(i["pn"], {"value": i["value"], "fp": i["footprint"].split(":")[-1],
                                               "jlc": i["price"]["jlc"] if i["price"] else "?", "boards": set(), "qty": 0})
                t["boards"].add(b)
                t["qty"] += i["qty"]
    fee = to_eur(o["jlc_extended_fee_usd"], "USD", o)
    print(f"{len(types)} extended or consigned SMD part types, about EUR {len(types) * fee:,.0f} in fees per order")
    for pn, t in sorted(types.items(), key=lambda x: (x[1]["fp"][:2], x[0])):
        print(f"  {pn:12s} {t['jlc']:9s} {t['value'][:22]:22s} {t['fp'][:26]:26s} {t['qty']:3d}  {', '.join(sorted(t['boards']))}")


def unpriced(o):
    for b, items in all_boms(o).items():
        miss = [i for i in items if not i["price"]]
        if miss:
            print(f"== {b}")
            for i in miss:
                print(f"  {i['qty']:3d} x {i['pn']:12s} {i['value'][:30]:30s} {i['footprint'].split(':')[-1]}")



def ledger_rows():
    return read_csv(LEDGER) if os.path.exists(LEDGER) else []


def ledger_add(a, o):
    if a.category not in CATEGORIES:
        sys.exit(f"category must be one of {', '.join(CATEGORIES)}")
    if a.board and a.board not in BOARDS and a.board != "system":
        sys.exit(f"board must be one of {', '.join(BOARDS)} or system")
    new = not os.path.exists(LEDGER)
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    eur = to_eur(a.amount, a.currency, o)
    with open(LEDGER, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        if new:
            w.writeheader()
        w.writerow({"date": a.date, "supplier": a.supplier, "ref": a.ref or "", "category": a.category,
                    "board": a.board or "system", "description": a.desc or "", "amount": f"{a.amount:.2f}",
                    "currency": a.currency.upper(), "eur": f"{eur:.2f}"})
    print(f"Added EUR {eur:.2f} to {LEDGER}")


def ledger_summary(md):
    rows = ledger_rows()
    if not rows:
        print(f"No realized costs yet ({LEDGER}).")
        return
    for key in ("category", "board", "supplier"):
        t = defaultdict(float)
        for r in rows:
            t[r[key]] += float(r["eur"])
        if md:
            print(f"\n| {key.capitalize()} | EUR |\n|---|---|")
            for k, v in sorted(t.items(), key=lambda x: -x[1]):
                print(f"| {k} | {v:,.2f} |")
        else:
            print(f"By {key}:")
            for k, v in sorted(t.items(), key=lambda x: -x[1]):
                print(f"  {k:24s} {v:10,.2f}")
    total = sum(float(r["eur"]) for r in rows)
    first, last = min(r["date"] for r in rows), max(r["date"] for r in rows)
    print(f"\nRealized total EUR {total:,.2f} ({len(rows)} entries, {first} to {last})")


def main():
    a = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    s = a.add_subparsers(dest="cmd", required=True)
    e = s.add_parser("estimate"); e.add_argument("--md", action="store_true")
    e.add_argument("--channels", default=STANDARD_BUILDS,
                   type=lambda v: [int(n) for n in v.split(",")])
    e.add_argument("--fees-per-design", action="store_true")
    d = s.add_parser("drivers"); d.add_argument("--board", choices=list(BOARDS)); d.add_argument("--top", type=int, default=10)
    s.add_parser("unpriced")
    s.add_parser("extended")
    l = s.add_parser("ledger"); l.add_argument("--md", action="store_true")
    ls = l.add_subparsers(dest="lcmd")
    la = ls.add_parser("add")
    la.add_argument("--supplier", required=True); la.add_argument("--category", required=True)
    la.add_argument("--amount", type=float, required=True); la.add_argument("--currency", default="EUR")
    la.add_argument("--date", default=datetime.date.today().isoformat())
    la.add_argument("--board"); la.add_argument("--ref"); la.add_argument("--desc")
    o = a.parse_args()
    ov = overheads()
    if o.cmd == "estimate":
        if len(o.channels) == 1:
            estimate(o.channels[0], ov, o.md, o.fees_per_design)
        else:
            compare(o.channels, ov, o.md, o.fees_per_design)
    elif o.cmd == "drivers":
        drivers(o.board, o.top, ov)
    elif o.cmd == "unpriced":
        unpriced(ov)
    elif o.cmd == "extended":
        extended(ov)
    elif o.cmd == "ledger":
        if o.lcmd == "add":
            ledger_add(o, ov)
        else:
            ledger_summary(o.md)


if __name__ == "__main__":
    main()
