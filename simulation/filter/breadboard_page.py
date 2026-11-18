#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Build breadboard.html: schematic, EKB14 board layout and wiring tables.

Run breadboard_schematic.py and breadboard_layout.py first (they write the
SVGs this page embeds). The placement tables come from the same PARTS list
the layout check verifies, so the page and the drawing cannot drift apart.

Usage:  python3 simulation/filter/breadboard_page.py
"""

from html import escape
from pathlib import Path

import breadboard_layout as bl

HERE = Path(__file__).resolve().parent

NOTES = {
    "C5": "10 µF 100 V bipolar electrolytic from the order (ø8 mm); either way round. Nothing else in column 3 under its body. Test 11 swaps it for two 10 µF 25 V back to back, − to −",
    "R1": "Input attenuator, the card's 18 kΩ: +4 dBu becomes about ±19 mV at pin 1",
    "R2": "Attenuator shunt (hot drive), the card's 200 Ω",
    "R3": "330 Ω gives about −4 dB; try 200 Ω for −6 dB",
    "J1": "2-pin header with a jumper shunt. Fitted = medium drive, removed = hot drive",
    "C9": "Optional (datasheet): steadier resonance over the sweep. R82 film, 5 mm pitch: sits diagonally",
    "R4": "Terminates the unused SIG IN− (the datasheet's 200 Ω; not critical)",
    "C1": "Ladder capacitor, datasheet Figure 1. R82 film 10 %, 5 mm pitch: sits diagonally",
    "C2": "Ladder capacitor, datasheet Figure 1. R82 film 10 %, 5 mm pitch: sits diagonally",
    "C3": "Ladder capacitor, datasheet Figure 1. R82 film 10 %, 5 mm pitch: sits diagonally",
    "C4": "Ladder capacitor, datasheet Figure 1 (NP0 ceramic)",
    "C10": "Decoupling, +15 V rail to the GND strip at column 7, next to U1 pin 16",
    "C11": "Decoupling, −15 V rail to the GND strip at column 16, next to U1 pin 8",
    "C12": "Decoupling, +15 V rail to U2 pin 5's GND strip",
    "C13": "Decoupling, −15 V rail to U2 pin 3's GND strip",
    "D1": "Reverse-polarity protection: band (cathode) to the +15 V rail, other end to the GND strip. Conducts only if the supply is connected the wrong way round",
    "D2": "Reverse-polarity protection: band (cathode) to the GND strip at column 1, other end to the −15 V rail",
    "C14": "Supply bulk, 10 µF 25 V electrolytic: + to the +15 V rail, − to the GND strip",
    "C15": "Supply bulk, 10 µF 25 V electrolytic: + to the GND strip at column 1, − to the −15 V rail",
    "R7": "Resonance input filter (Figure 3; E24 510 Ω for 499 Ω)", "C8": "Resonance input filter (Figure 3), R82 film",
    "R6": "Fitted for test 2: the second order's 33 kΩ, measured 32.6 kΩ, so up to about 460 µA into pin 14 with RV2 fully up (15 V): enough to find the oscillation onset (datasheet 350-450 µA). The planned 51 kΩ limit (about 294 µA) is not in the E12 kit: 47 kΩ + 3.9 kΩ in series, or 56 kΩ alone (about 268 µA)",
    "R8": "Stands in for the temperature-compensating resistor",
    "R10": "Cutoff offset from RV4, the card's 470 kΩ: about ±32 mV at pin 15",
    "R9": "Summer output into the cutoff pin",
    "C6": "Output stage, datasheet Figure 1",
    "C7": "Output coupling, 10 µF 100 V bipolar electrolytic (ø8 mm): RV3 sits just above it, so lean it outwards over the −15 V rail",
    "R11": "With RV5: summer feedback, sets 1 V/octave for the CV input (E24 160 kΩ; RV5 makes up the rest)",
    "R12": "Scales the cutoff pot to about 10 octaves (the card's 300 kΩ)",
    "R13": "CV input, about 1 V/octave",
    "W13": "Carries the cutoff pin (U1 pin 15) to column 6 for R9 and R10",
    "W23": "Carries the resonance pin (U1 pin 14) to column 3 for R6 and R7; insulated, routed between rows C and D",
    "W26": "R9 to U2 pin 7 (summer output); insulated, along the top edge",
    "W28": "R10 to the RV4 wiper; insulated, along the top edge and down the right edge",
    "W29": "U2 pin 7 to the RV5 wiper strip at column 23",
    "W30": "RV4 pin 1 to +15 V; insulated, up the right edge",
    "RV3": "Output gain: wiper and pin 1 form the feedback resistor; pin 3 is not used: bend it up so it stays out of 17H. Start at about 9 kΩ between pin 1 and the wiper (unity predicted near 8.8 kΩ), set in test 5",
    "RV4": "Cutoff offset: the full track as a divider between +15 V (pin 1, via W30) and −15 V (pin 3, on U2 pin 4's strip); wiper to R10 by W28. Centre it before power-up",
    "RV5": "V/oct scale: pin 1 and the wiper in series with R11 (wiper on U2 pin 7 via W29); pin 3 hangs past column 23: bend it up. Start at about 32 kΩ (1 V/oct needs about 192 kΩ in total)",
    "W5": "U1 output (pin 3) to U2 pin 2; insulated, along the bottom edge, away from the supply leads",
    "W14": "Joins the input node at column 7 to U1 pin 1",
    "W2": "U1 pin 9 (GND) to the GND rail at column 16",
}
VALUES = {"R6": "33 kΩ (32.6 kΩ measured)", "R7": "510 Ω (506 Ω measured)", "R9": "100 kΩ (101.8 kΩ measured)", "C10": "100 nF (88.9 nF measured)", "C14": "10 µF (9.05 µF measured)", "C9": "3.3 nF", "J1": "jumper", "R3": "330 Ω (or 200 Ω)"}
# What each part is, to pick it out of the bags: capacitor dielectric and body, resistor type.
TYPES = {
    "C1": "Film, R82 box 100 V 10 %, 5 mm pitch", "C2": "Film, R82 box 100 V 10 %, 5 mm pitch",
    "C3": "Film, R82 box 100 V 10 %, 5 mm pitch", "C9": "Film, R82 box 100 V 10 %, 5 mm pitch",
    "C8": "Film, R82 box 100 V 5 %, 5 mm pitch",
    "C4": "Ceramic MLCC C0G/NP0 50 V, 2.54 mm", "C6": "Ceramic MLCC C0G/NP0 50 V, 2.54 mm",
    "C10": "Ceramic MLCC X7R 50 V, 2.54 mm", "C11": "Ceramic MLCC X7R 50 V, 2.54 mm",
    "C12": "Ceramic MLCC X7R 50 V, 2.54 mm", "C13": "Ceramic MLCC X7R 50 V, 2.54 mm",
    "C5": "Electrolytic, bipolar (non-polarised) 100 V, ø8×12 mm: either way round",
    "C7": "Electrolytic, bipolar (non-polarised) 100 V, ø8×12 mm: either way round",
    "C14": "Electrolytic, polarised 25 V, ø4×5 mm: stripe (−) to GND",
    "C15": "Electrolytic, polarised 25 V, ø4×5 mm: stripe (−) to −15 V",
    "J1": "Pin header 2-pin with a shunt",
    "RV3": "Trimmer, multiturn 3296W, 25 turns", "RV4": "Trimmer, multiturn 3296W, 25 turns", "RV5": "Trimmer, multiturn 3296W, 25 turns",
    "D1": "Rectifier diode 1N4001, DO-41: band = cathode", "D2": "Rectifier diode 1N4001, DO-41: band = cathode",
}
# Electrokit article numbers, as on the bags (electrokit-order.csv, electrokit-order-2.csv); other resistors from the E12 kit.
SKUS = {
    "C1": "41015666", "C2": "41015666", "C3": "41015666", "C8": "41015667", "C9": "41015664",
    "C4": "41011990", "C6": "41011983",
    "C10": "41016717", "C11": "41016717", "C12": "41016717", "C13": "41016717",
    "C5": "41018168", "C7": "41018168", "C14": "41019084", "C15": "41019084",
    "D1": "40310001", "D2": "40310001", "RV3": "40900268", "RV4": "40900268", "RV5": "40900268",
    "R2": "40811220", "R4": "40811220", "R7": "40811251", "R11": "40811516", "R12": "40811530",
    "R6": "40811433 (33k)",
}
for _r in ("R2", "R4", "R7", "R11", "R12", "R6"):
    TYPES[_r] = "Metal film 1 %, second order"
# Where each part comes from (a: the user's E12 kit, b: first Electrokit order, c: second order)
SRC = {
    "kit": ("a", "E12 kit"), "o1": ("b", "Order 1"), "o2": ("c", "Order 2"),
    "o12": ("b", "Order 1 or 2"), "own": ("x", "Own stock"), "sf": ("x", "SparkFun"),
}
SOURCE = {
    "U1": "o12", "U2": "o1",
    "R1": "kit", "R3": "kit", "R8": "kit", "R9": "kit", "R10": "kit", "R13": "kit",
    "R2": "o2", "R4": "o2", "R6": "o2", "R7": "o2", "R11": "o2", "R12": "o2",
    "C1": "o1", "C2": "o1", "C3": "o1", "C4": "o1", "C5": "o1", "C6": "o1", "C7": "o1", "C8": "o1", "C9": "o1",
    "C10": "o1", "C11": "o1", "C12": "o1", "C13": "o1", "C14": "o1", "C15": "o1",
    "D1": "o1", "D2": "o1", "RV3": "o1", "RV4": "o1", "RV5": "o1", "J1": "own",
}
SOURCE_NOTE = {
    "U1": "Chips 1 and 2 are out (test 2); use the third chip from order 1 or one of order 2's three",
    "C1": "four in order 1, three more in order 2", "C2": "four in order 1, three more in order 2",
    "C3": "four in order 1, three more in order 2",
}
# Off-board parts and build items, for the by-source lists
OFF_SOURCES = [
    ("o1", "RV1, RV2", "10 kΩ linear pots, PC16SH (41037776)"),
    ("o1", "IN, OUT, CV", "6.3 mm mono jacks (41002006)"),
    ("o2", "Board", "ProtoPCB EKB14 (41003657)"),
    ("sf", "U1 adapter", "SparkFun BOB-13994 SSOP-16 to DIP"),
    ("own", "Sockets", "Two 8-pin female header strips for the adapter"),
]


class Badge(str):
    """A table cell rendered as a coloured source label."""


def badge(key):
    cls, label = SRC[key]
    return f'<span class="src src-{cls}">{escape(label)}</span>'


CHIPS = [
    ("U1", "SSI2144", "SSOP-16 filter on the SparkFun BOB-13994 adapter (500 mil)", "41019301",
     "pins 1-8: 8G-15G; pins 16-9: 8D-15D",
     "On two 8-pin female header strips soldered in rows D and G, so chips can be swapped; dot (pin 1) to the left. Rows E and F and the GND rail under the adapter stay empty"),
    ("U2", "TL072", "Dual JFET op amp, DIP-8", "40350072", "pins 1-4: 18F-21F; pins 8-5: 18E-21E",
     "Notch to the left; straddles the GND rail, whose holes under it stay empty. A DIP-8 socket is fine too"),
]


def hole(end):
    return bl.hole_name(end) if end[0] in ("E", "ER", "NC") else end[1]


def rows(kinds):
    out = []
    for ref, val, kind, *ends in bl.PARTS:
        if kind not in kinds:
            continue
        where = " → ".join(hole(e) for e in ends if e[0] != "X") if kind != "trim" else \
            f"pin 1 {hole(ends[0])}, wiper {hole(ends[1])}, pin 3 {hole(ends[2])}"
        value = VALUES.get(ref, val) or ""
        kind_name = TYPES.get(ref, "Metal film 1 %, E12 kit" if kind == "res" else "")
        sku = SKUS.get(ref, "kit" if kind == "res" else "")
        note = NOTES.get(ref, "")
        if kind == "res":
            mount = ("Lies flat (7.62 mm or more: bend the leads close to the body)" if ref in bl.FLAT
                     else "Stands upright")
            note = f"{note}. {mount}" if note else mount
        out.append((ref, value, where, note, kind_name, sku))
    return out


def table(rws, cols, cls, ids=None):
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = []
    for i, r in enumerate(rws):
        rid = f"chk-{escape(str(ids[i] if ids else r[0]))}"
        cells = "".join(f"<td>{badge(c) if isinstance(c, Badge) else escape(str(c))}</td>" for c in r)
        body.append(f'<tr><td class="tick"><input type="checkbox" id="{rid}" aria-label="{escape(str(r[0]))} placed"></td>{cells}</tr>')
    return (f'<div class="tablewrap"><table class="{cls}"><thead><tr><th class="tick"><span class="sr">Done</span></th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


schem = (HERE / "breadboard-schematic.svg").read_text()

parts_rows = [(c[0], c[1], Badge(SOURCE[c[0]]), *c[2:]) for c in CHIPS] + \
    [(r[0], r[1], Badge(SOURCE[r[0]]), r[4], r[5], r[2], r[3]) for r in rows({"res", "cap", "jumper", "diode", "trim"})]
for ref in SOURCE:
    assert any(row[0] == ref for row in parts_rows), ref
for row in parts_rows:
    assert row[0] in SOURCE, f"no source for {row[0]}"

# By-source lists: every on-board part plus the off-board items
by_source = {"kit": [], "o1": [], "o2": [], "other": []}
for row in parts_rows:
    key = SOURCE[row[0]]
    group = {"kit": "kit", "o1": "o1", "o2": "o2", "o12": "o2"}.get(key, "other")
    by_source[group].append((key, row[0], row[1], row[5] if len(row) > 6 else ""))
order = {"U": 0, "R": 1, "C": 2, "D": 3, "RV": 4, "J": 5}
for g in by_source.values():
    g.sort(key=lambda t: (order.get(t[1].rstrip("0123456789"), 6), int(t[1][len(t[1].rstrip("0123456789")):] or 0)))
for key, what, desc in OFF_SOURCES:
    group = key if key in ("kit", "o1", "o2") else "other"
    by_source[group].append((key, what, desc, "off board" if key in ("o1",) else ""))


def source_card(group, title, sub):
    items = "".join(
        f'<li><span class="ref">{escape(ref)}</span> <span class="val">{escape(val)}</span>'
        + (f' {badge(key)}' if group == "other" or key == "o12" else "")
        + (f'<span class="where">{escape(where)}</span>' if where else "") + "</li>"
        for key, ref, val, where in by_source[group])
    head = badge(group) if group != "other" else '<span class="src src-x">Other</span>'
    return (f'<div class="srccard"><h3>{head} <span>{escape(title)}</span></h3><p>{escape(sub)}</p>'
            f'<ul>{items}</ul></div>')


source_html = "".join([
    source_card("kit", "Your E12 resistor set", "Metal film 1 %"),
    source_card("o1", "First Electrokit order", "electrokit-order.csv, delivered 2026-10-13"),
    source_card("o2", "Second Electrokit order", "electrokit-order-2.csv"),
    source_card("other", "Elsewhere", "Not from the kit or either order"),
])
wire_rows = [(r[0], r[2], r[3]) for r in rows({"wire"})]

# Flying leads, grouped by what they go to; the number is the tag on the drawing (no number = named on the drawing)
LEAD_GROUPS = [
    ("Bench supply", ["L11", "L12", "L13"]),
    ("Jacks", ["L4", "L3", "L6"]),
    ("RV1 cutoff, 10 kΩ linear", ["L5", "L7", "L8"]),
    ("RV2 resonance, 10 kΩ linear", ["L1", "L9", "L10"]),
]
part_by_ref = {p[0]: p for p in bl.PARTS}
lead_rows = []
lead_ids = []
for group, refs in LEAD_GROUPS:
    for ref in refs:
        tag = bl.ETAG[ref]
        num = str(bl.KEYED.index(ref) + 1) if tag[3] is None else "named"
        lead_rows.append((f"{group}: {tag[0]}", num, hole(part_by_ref[ref][3])))
        lead_ids.append(ref)

# Hover text for the board drawing: value, type, holes and notes, as in the tables
tips = {}
for ref, value, where, note, kind_name, sku in rows({"res", "cap", "jumper", "diode", "trim", "wire"}):
    head = f"{ref}  {value}".strip() if value else ref
    src = SRC[SOURCE[ref]][1] if ref in SOURCE else ""
    lines = [head, (f"From: {src}" + (f" ({SOURCE_NOTE[ref]})" if ref in SOURCE_NOTE else "")) if src else "",
             kind_name, f"Holes: {where}", note,
             f"Electrokit {sku}" if sku and sku != "kit" else ""]
    tips[ref] = "\n".join(x for x in lines if x)
for ref, part, desc, sku, pins, note in CHIPS:
    tips[ref] = f"{ref}  {part}\nFrom: {SRC[SOURCE[ref]][1]}" + (f" ({SOURCE_NOTE[ref]})" if ref in SOURCE_NOTE else "") + f"\n{desc}\n{pins}\n{note}"
for group, refs in LEAD_GROUPS:
    for ref in refs:
        tips[ref] = f"{bl.ETAG[ref][0]}\nFlying lead ({group}) at {hole(part_by_ref[ref][3])}"
layout = bl.render_svg(tips)

OFFBOARD = [
    ("Jacks (6.3 mm mono, PCB pins; Electrokit 41002006)", "Solder short stranded leads to the tip and sleeve pins; leave the switch pin free. Tips go to the holes in the table above; sleeves to any free hole on the GND rail (the middle strip: columns 3-5, 24 and 25 are free). Use a TS cable from the interface (a TRS plug shorts its ring to sleeve, which is harmless). The CV jack is needed for tests 12 and 13."),
    ("Pots", "Two full-size pots on flying leads: RV1 cutoff and RV2 resonance, 10 kΩ linear. RV3-RV5 are trimmers on the board. If the cutoff falls when you turn RV1 clockwise, swap its two ends. Linear RV2 crowds the resonance into the last part of the turn; that is fine for the tests."),
    ("Bench supply", "+15 V, 0 V and −15 V to the three supply holes. Current limit about 50 mA per rail. Two single supplies in series: their earth terminals stay open (BREADBOARD.md, section 2)."),
]

checks = [
    "Check the adapter: confirm with a multimeter that DIP pin 1 connects to SSOP pin 1 (the chip's dot). Most adapters keep the numbering; a few don't.",
    "Solder the two socket strips first (rows D and G, columns 8-15), then the low parts, the upright resistors, the wires and last the flying leads. After soldering, check with the meter that no neighbouring strips are bridged, and that U1 pin 9's strip (15B) and U2 pins 3 and 5 (20G, 21D) read 0 Ω to the GND rail.",
    "Dot or notch to the left on both chips: U1's adapter with pin 1 at 8G and pin 16 at 8D (the adapter's pin rows are 500 mil apart, so rows E and F and the GND rail under it stay empty); U2 pin 1 at 18F. Before powering a refitted adapter, check that pin 1 sits at 8G.",
    "Power the board without U1 and U2 first: +15 V at 8A and 18A, −15 V at 15J and 21J, 0 V at 15B, 20G and 21D.",
    "With chips in, total current should be roughly 5 mA per rail for U1 plus a few mA for U2 (datasheet: SSI2144 about 5 mA typical). Much more means a short or a reversed chip: switch off.",
    "Pin 14 (Q) and the summer's inverting input (U2 pin 6) sit at about 0 V: both are virtual grounds.",
    "Pin 15 (cutoff) moves within about ±95 mV as RV1 turns (up to about ±127 mV with RV4 at an end; centre RV4 first). Volts there means a wiring fault. Above about +175 mV the chip goes silent until the pin drops back below about +135 mV (datasheet dropout; test 13): with a CV plugged in, a silent filter at the low end can be this, not a fault.",
]

page = f"""<title>SSI2144 Breadboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600;700&family=IBM+Plex+Sans+Condensed:wght@600;700&display=swap">
<style>
/* Layout: one reading column for text; drawings break out wider and scroll inside their own frames. */
:root {{
  --paper: #f5f6f4; --surface: #ffffff; --ink: #1d2430; --muted: #5b6474; --line: #d9ddd6;
  --accent: #b4540a; --accent-soft: #f6e6d6;
  --board: #efe9dc; --hole: #bcb4a3; --chip: #262b33; --chip-text: #f3f1ea;
  --pcb: #e4ecdf; --copper: #b8862b;
  --done: #1f8a4c; --done-ink: #ffffff; --src-a: #8a4f12; --src-a-bg: #f6e3cc; --src-b: #1b5f78; --src-b-bg: #d7ecf3; --src-c: #5b3191; --src-c-bg: #e8ddf6; --src-x: #4d5563; --src-x-bg: #e6e8eb;
  --rail-pos: #c0392b; --rail-neg: #2e5aa8; --rail-gnd: #2f7d4f;
  --part-res: #7a4b1e; --part-cap: #1f6f8b; --part-wire: #6b6f78; --part-trim: #6b3fa0;
  --f-display: "IBM Plex Sans Condensed", "Arial Narrow", Arial, sans-serif;
  --f-body: "IBM Plex Sans", "Helvetica Neue", Arial, sans-serif;
  --f-mono: "IBM Plex Mono", ui-monospace, Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper: #14181d; --surface: #1b2027; --ink: #e6e9ee; --muted: #9aa3b2; --line: #2c333d;
    --accent: #f09a4f; --accent-soft: #3a2a1c;
    --board: #2a2722; --hole: #57524a; --chip: #0c0e11; --chip-text: #e9e6dd;
    --pcb: #1f2a22; --copper: #c9a24e;
    --done: #4cc884; --done-ink: #0d1f15; --src-a: #f2b874; --src-a-bg: #3b2a17; --src-b: #7fd0ec; --src-b-bg: #16323c; --src-c: #c9a6f5; --src-c-bg: #2d2140; --src-x: #b6bdc8; --src-x-bg: #2a3039;
    --rail-pos: #ff7a6b; --rail-neg: #7ea8ff; --rail-gnd: #6fd39a;
    --part-res: #e2a46a; --part-cap: #64c3e0; --part-wire: #a3a9b4; --part-trim: #c39bf0;
    color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --paper: #14181d; --surface: #1b2027; --ink: #e6e9ee; --muted: #9aa3b2; --line: #2c333d;
  --accent: #f09a4f; --accent-soft: #3a2a1c;
  --board: #2a2722; --hole: #57524a; --chip: #0c0e11; --chip-text: #e9e6dd;
  --pcb: #1f2a22; --copper: #c9a24e;
  --done: #4cc884; --done-ink: #0d1f15; --src-a: #f2b874; --src-a-bg: #3b2a17; --src-b: #7fd0ec; --src-b-bg: #16323c; --src-c: #c9a6f5; --src-c-bg: #2d2140; --src-x: #b6bdc8; --src-x-bg: #2a3039;
  --rail-pos: #ff7a6b; --rail-neg: #7ea8ff; --rail-gnd: #6fd39a;
  --part-res: #e2a46a; --part-cap: #64c3e0; --part-wire: #a3a9b4; --part-trim: #c39bf0;
  color-scheme: dark;
}}
* {{ box-sizing: border-box; }}
body {{ background: var(--paper); color: var(--ink); font: 15px/1.55 var(--f-body); }}
.wrap {{ max-width: 1340px; margin: 0 auto; padding-inline: 20px; padding-block: 36px 64px; }}
.col {{ max-width: 68ch; }}
header .eyebrow {{ font: 600 12px/1 var(--f-mono); letter-spacing: .08em; text-transform: uppercase; color: var(--accent); }}
h1 {{ font: 700 clamp(30px, 5vw, 46px)/1.05 var(--f-display); margin: 10px 0 12px; text-wrap: balance; letter-spacing: -.01em; }}
h2 {{ font: 700 24px/1.2 var(--f-display); margin: 0 0 6px; text-wrap: balance; }}
p {{ margin: 0 0 10px; }}
.lede {{ color: var(--muted); font-size: 16.5px; }}
section {{ margin-top: 44px; display: grid; gap: 14px; }}
.frame {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow-x: auto; padding: 14px; }}
.frame svg {{ display: block; height: auto; }}
.frame.schem svg {{ width: 100%; min-width: 980px; }}
.frame.ekb svg {{ width: 100%; max-width: 1100px; min-width: 820px; margin: 0 auto; }}
.frame.ekb svg g.part {{ cursor: help; }}
.frame.ekb svg:has(g.part:hover) g.part:not(:hover) {{ opacity: .28; }}
.frame.ekb svg.pinned g.part:not(.on) {{ opacity: .28; }}
@media (prefers-reduced-motion: no-preference) {{ .frame.ekb svg g.part {{ transition: opacity .08s; }} }}
.tip {{ position: fixed; z-index: 20; max-width: min(340px, calc(100vw - 32px)); padding: 9px 12px; border-radius: 8px;
  background: var(--surface); color: var(--ink); border: 1px solid var(--line); box-shadow: 0 6px 20px rgba(0,0,0,.18);
  font: 13px/1.45 var(--f-body); pointer-events: none; white-space: pre-line; }}
.tip b {{ display: block; font: 600 14px/1.3 var(--f-mono); color: var(--accent); margin-bottom: 3px; }}
.tip .pin {{ display: block; margin-top: 5px; font-size: 11.5px; color: var(--muted); }}
.tip.pinned {{ pointer-events: auto; }}
.tip .body {{ display: block; }}
.tip .actions {{ display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; margin-top: 10px; padding-top: 10px; border-top: 1px solid var(--line); }}
.tip .actions .pin {{ margin: 0; }}
.tip button {{ display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 6px;
  border: 1px solid var(--accent); background: var(--accent); color: var(--surface); font: 600 13px/1.2 var(--f-body); cursor: pointer; }}
.tip button.undo {{ background: transparent; color: var(--accent); }}
.frame.ekb svg .badge {{ pointer-events: none; }}
.frame.ekb svg g.part.done > :not(.badge) {{ opacity: .38; }}
.frame.ekb svg .badge circle {{ fill: var(--done); stroke: var(--pcb); stroke-width: 2.5; }}
.frame.ekb svg .badge path {{ fill: none; stroke: var(--done-ink); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }}
.sw.check {{ width: 15px; height: 15px; border-radius: 50%; background: var(--done); position: relative; }}
.sw.check::after {{ content: ""; position: absolute; left: 4.5px; top: 2.5px; width: 4px; height: 7px; border: solid var(--done-ink); border-width: 0 2px 2px 0; transform: rotate(45deg); }}
.progress {{ font: 600 13px/1.4 var(--f-mono); color: var(--muted); }}
.legend {{ display: flex; flex-wrap: wrap; gap: 8px 18px; font: 13px/1.4 var(--f-body); color: var(--muted); }}
.legend span {{ display: inline-flex; align-items: center; gap: 7px; }}
.sw {{ width: 18px; height: 4px; border-radius: 2px; display: inline-block; }}
.sw.dot {{ width: 11px; height: 11px; border-radius: 50%; border: 2px solid var(--accent); background: transparent; }}
ol.checks {{ margin: 0; padding-left: 22px; display: grid; gap: 6px; }}
.callout {{ border-left: 3px solid var(--accent); background: var(--accent-soft); padding: 10px 14px; border-radius: 0 8px 8px 0; }}
.tablewrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); }}
table {{ border-collapse: collapse; width: 100%; font-size: 14px; }}
th, td {{ text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ font: 600 12px/1.3 var(--f-mono); text-transform: uppercase; letter-spacing: .06em; color: var(--muted); background: var(--paper); }}
tbody tr:last-child td {{ border-bottom: 0; }}
td:nth-child(2) {{ font: 600 13px/1.4 var(--f-mono); white-space: nowrap; }}
.parts td:nth-child(3), .parts td:nth-child(6), .parts td:nth-child(7), .wires td:nth-child(3), .leads td:nth-child(3), .leads td:nth-child(4) {{ font-family: var(--f-mono); font-size: 13px; white-space: nowrap; }}
.leads td:nth-child(2) {{ font: 14px/1.4 var(--f-body); white-space: normal; }}
td.tick, th.tick {{ width: 34px; text-align: center; }}
input[type=checkbox] {{ width: 16px; height: 16px; accent-color: var(--accent); }}
tr:has(input:checked) td:not(.tick) {{ color: var(--muted); text-decoration: line-through; text-decoration-color: var(--line); }}
:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }}
dl.off {{ display: grid; grid-template-columns: minmax(0, 15rem) minmax(0, 1fr); gap: 8px 18px; margin: 0; }}
dl.off dt {{ font-weight: 600; }}
dl.off dd {{ margin: 0; }}
@media (max-width: 640px) {{ dl.off {{ grid-template-columns: minmax(0, 1fr); }} dl.off dd {{ margin-bottom: 8px; }} }}
code {{ font: 13px var(--f-mono); }}
.src {{ display: inline-block; padding: 2px 9px; border-radius: 999px; font: 600 12px/1.4 var(--f-body); white-space: nowrap; }}
.src-a {{ color: var(--src-a); background: var(--src-a-bg); }}
.src-b {{ color: var(--src-b); background: var(--src-b-bg); }}
.src-c {{ color: var(--src-c); background: var(--src-c-bg); }}
.src-x {{ color: var(--src-x); background: var(--src-x-bg); }}
.srcgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 14px; }}
.srccard {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; min-width: 0; }}
.srccard h3 {{ margin: 0 0 2px; display: flex; align-items: center; gap: 8px; font: 700 16px/1.3 var(--f-display); }}
.srccard > p {{ margin: 0 0 10px; color: var(--muted); font-size: 13px; }}
.srccard ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 5px; }}
.srccard li {{ display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 8px; font-size: 14px; }}
.srccard .ref {{ font: 600 13px/1.4 var(--f-mono); min-width: 3.2em; }}
.srccard .where {{ margin-left: auto; font: 12px/1.4 var(--f-mono); color: var(--muted); }}
footer {{ margin-top: 48px; color: var(--muted); font-size: 13px; }}
</style>

<div class="wrap">
<header class="col">
  <div class="eyebrow">Syntsamix · filter test circuit</div>
  <h1>SSI2144 breadboard</h1>
  <p class="lede">One SSI2144 ladder filter core with input attenuator, resonance and cutoff controls, the summer and the output stage, soldered on one Electrokit EKB14 board. Only the RV1 and RV2 pots, the three jacks and the bench supply are off the board, on flying leads; the RV3–RV5 trimmers are on it. It's the circuit for tests 1–7 and 11–13 in <code>simulation/filter/BREADBOARD.md</code>, built from both Electrokit orders, the SSOP adapter and an E12 1 % resistor kit.</p>
</header>

<section class="col">
  <h2>Before you power up</h2>
  <ol class="checks">{"".join(f"<li>{escape(c)}</li>" for c in checks)}</ol>
  <p class="callout">The pinout and the ladder, output and resonance values come from the SSI2144 datasheet (Rev 3.0, Figures 1 and 3). The input attenuator, drive jumper, resonance limit and cutoff scaling are this project's values, on the E12 kit's values and E24 values from the second order (the channel card's own where it has them: 18 kΩ, 200 Ω, 470 kΩ, 300 kΩ). A script checked the board layout against the schematic, connection by connection: no missing links, no shorts, nothing under a chip or a flat resistor.</p>
</section>

<section>
  <div class="col"><h2>Schematic</h2>
  <p>Scroll sideways on a narrow screen. Orange circles are connections to jacks; small rings are supply connections.</p></div>
  <div class="frame schem">{schem}</div>
</section>

<section>
  <div class="col"><h2>Board layout</h2>
  <p>Electrokit ProtoPCB EKB14 (41003657). Columns 1–23, rows A–E on top and F–J at the bottom; each half-column of five holes is one connection, as on a breadboard. +15 V runs along the top edge, GND along the strip between the two halves (with two extra holes at each end), −15 V along the bottom edge. Resistors spanning one or two columns stand upright; R1, R4, R12 and R13 lie flat. The grey wires are insulated and may run over other parts. Orange rings are flying leads: numbered ones are listed under the drawing. Point at a part to see its value, type, holes and notes. Click or tap it to keep them showing and to mark it as placed; placed parts fade back with a green check on them, so what is left stands out, and are ticked in the tables (click elsewhere or press Esc to close).</p>
  <p class="progress" id="progress"></p></div>
  <div class="frame ekb">{layout}</div>
  <div class="legend" aria-label="Legend">
    <span><i class="sw" style="background:var(--part-res)"></i>Resistor</span>
    <span><i class="sw" style="background:var(--part-cap)"></i>Capacitor</span>
    <span><i class="sw" style="background:var(--ink)"></i>Diode (band = cathode)</span>
    <span><i class="sw" style="background:var(--part-wire)"></i>Wire</span>
    <span><i class="sw" style="background:var(--accent)"></i>J1 jumper</span>
    <span><i class="sw" style="background:var(--part-trim)"></i>Trimmer (dashed pin: bent up, not soldered)</span>
    <span><i class="sw dot"></i>Flying lead to a pot, jack or the supply</span>
    <span><i class="sw check"></i>Placed (faded, check on the part)</span>
    <span><i class="sw" style="background:var(--rail-pos)"></i>+15 V</span>
    <span><i class="sw" style="background:var(--rail-gnd)"></i>GND</span>
    <span><i class="sw" style="background:var(--rail-neg)"></i>−15 V</span>
  </div>
</section>

<section>
  <div class="col"><h2>Flying leads</h2>
  <p>Stranded wire, soldered into the hole from the component side. The tag column gives the number on the drawing.</p></div>
  {table(lead_rows, ["Lead", "Tag", "Hole"], "leads", lead_ids)}
</section>

<section>
  <div class="col"><h2>Where to find each part</h2>
  <p>Grouped by where the part comes from: <span class="src src-a">E12 kit</span> your own resistor set, <span class="src src-b">Order 1</span> the first Electrokit order, <span class="src src-c">Order 2</span> the second. The same label is in the parts table and in each part's details on the board drawing.</p></div>
  <div class="srcgrid">{source_html}</div>
</section>

<section>
  <div class="col"><h2>Parts and placement</h2>
  <p>Holes are written as column then row, for example <code>8G</code>. Tick parts off as you place them; the ticks stay in this browser only.</p></div>
  {table(parts_rows, ["Ref", "Value", "Source", "Type", "Electrokit SKU", "Holes", "Notes"], "parts")}
</section>

<section>
  <div class="col"><h2>Wires</h2></div>
  {table(wire_rows, ["Ref", "From → to", "Notes"], "wires")}
</section>

<section class="col">
  <h2>Off-board parts</h2>
  <dl class="off">{"".join(f"<dt>{escape(a)}</dt><dd>{escape(b)}</dd>" for a, b in OFFBOARD)}</dl>
</section>

<footer class="col">Generated by <code>simulation/filter/breadboard_page.py</code> from the same placement list that <code>breadboard_layout.py</code> checks against the schematic. EKB14 hole pattern from the maker's drawing (Electrokit 41003657).</footer>
</div>

<div class="tip" id="tip" role="status" hidden></div>
<script>
(function () {{
  var KEY = 'ssi2144-ekb-';   // storage for the EKB14 build; the old breadboard ticks used another prefix
  function load(id) {{ try {{ return localStorage.getItem(KEY + id) === '1'; }} catch (e) {{ return false; }} }}
  function save(id, on) {{ try {{ localStorage.setItem(KEY + id, on ? '1' : '0'); }} catch (e) {{}} }}

  var svg = document.querySelector('.frame.ekb svg');
  var tip = document.getElementById('tip');
  var progress = document.getElementById('progress');
  var NS = 'http://www.w3.org/2000/svg';
  var parts = svg ? Array.prototype.slice.call(svg.querySelectorAll('g.part')) : [];
  var pinned = null;

  function box(ref) {{ return document.getElementById('chk-' + ref); }}
  function isDone(ref) {{ var b = box(ref); return b ? b.checked : load('chk-' + ref); }}

  // Placed parts fade back and get a check on their body, so what is left to place stands out.
  function badge(g) {{
    var old = g.querySelector('.badge'); if (old) old.remove();
    var done = isDone(g.dataset.ref);
    g.classList.toggle('done', done);
    if (!done) return;
    var x = parseFloat(g.dataset.ax), y = parseFloat(g.dataset.ay);
    var b = document.createElementNS(NS, 'g');
    b.setAttribute('class', 'badge');
    b.setAttribute('transform', 'translate(' + x + ' ' + y + ')');
    var c = document.createElementNS(NS, 'circle'); c.setAttribute('r', 8.5);
    var p = document.createElementNS(NS, 'path'); p.setAttribute('d', 'M-4 0.3 L-1.2 3.2 L4.2 -2.8');
    b.appendChild(c); b.appendChild(p); g.appendChild(b);
  }}
  function count() {{
    if (!progress) return;
    var done = parts.filter(function (g) {{ return isDone(g.dataset.ref); }}).length;
    progress.textContent = done + ' of ' + parts.length + ' parts, wires and leads placed';
  }}

  // Table ticks: load from storage, save on change, mirror on the board.
  document.querySelectorAll('input[type=checkbox]').forEach(function (b) {{
    b.checked = load(b.id);
    b.addEventListener('change', function () {{
      save(b.id, b.checked);
      var g = svg && svg.querySelector('g.part[data-ref="' + b.id.slice(4) + '"]');
      if (g) badge(g);
      if (pinned) fill(pinned);
      count();
    }});
  }});
  if (!svg || !tip) return;

  // Move each part's <title> into data so the slow native tooltip does not also appear.
  parts.forEach(function (g) {{
    var t = g.querySelector('title');
    if (t) {{ g.dataset.tip = t.textContent; t.remove(); }}
    badge(g);
  }});
  count();

  function setDone(ref, on) {{
    var b = box(ref);
    if (b) {{ b.checked = on; b.dispatchEvent(new Event('change')); }}
    else {{ save('chk-' + ref, on); var g = svg.querySelector('g.part[data-ref="' + ref + '"]'); if (g) badge(g); count(); if (pinned) fill(pinned); }}
  }}
  function fill(g) {{
    var ref = g.dataset.ref, done = isDone(ref);
    var lines = (g.dataset.tip || ref).split('\\n');
    tip.textContent = '';
    var h = document.createElement('b'); h.textContent = lines.shift() + (done ? '  ✓ placed' : ''); tip.appendChild(h);
    var body = document.createElement('span'); body.className = 'body'; body.textContent = lines.join('\\n'); tip.appendChild(body);
    if (g === pinned) {{
      var row = document.createElement('div'); row.className = 'actions';
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.id = 'tip-mark';
      btn.textContent = done ? 'Placed ✓ (undo)' : 'Mark as placed';
      if (done) btn.className = 'undo';
      btn.addEventListener('click', function (e) {{ e.stopPropagation(); setDone(ref, !done); }});
      row.appendChild(btn);
      var s = document.createElement('span'); s.className = 'pin'; s.textContent = 'Esc or click elsewhere to close'; row.appendChild(s);
      tip.appendChild(row);
    }}
    tip.hidden = false;
  }}
  function place(x, y) {{
    var w = tip.offsetWidth, h = tip.offsetHeight, vw = window.innerWidth, vh = window.innerHeight;
    var left = x + 16, top = y + 18;
    if (left + w > vw - 12) left = Math.max(12, x - w - 16);
    if (top + h > vh - 12) top = Math.max(12, y - h - 18);
    tip.style.left = left + 'px'; tip.style.top = top + 'px';
  }}
  function unpin() {{
    if (pinned) pinned.classList.remove('on');
    pinned = null; svg.classList.remove('pinned'); tip.classList.remove('pinned'); tip.hidden = true;
  }}
  svg.addEventListener('pointermove', function (e) {{
    if (pinned) return;
    var g = e.target.closest && e.target.closest('g.part');
    if (!g) {{ tip.hidden = true; return; }}
    if (tip.dataset.ref !== g.dataset.ref || tip.hidden) {{ tip.dataset.ref = g.dataset.ref; fill(g); }}
    place(e.clientX, e.clientY);
  }});
  svg.addEventListener('pointerleave', function () {{ if (!pinned) tip.hidden = true; }});
  svg.addEventListener('click', function (e) {{
    var g = e.target.closest && e.target.closest('g.part');
    if (!g || g === pinned) {{ unpin(); return; }}
    unpin();
    pinned = g; g.classList.add('on'); svg.classList.add('pinned'); tip.classList.add('pinned');
    tip.dataset.ref = g.dataset.ref; fill(g); place(e.clientX, e.clientY);
    e.stopPropagation();
  }});
  document.addEventListener('click', function (e) {{ if (pinned && !svg.contains(e.target) && !tip.contains(e.target)) unpin(); }});
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') unpin(); }});
  window.addEventListener('scroll', function () {{ if (!pinned) tip.hidden = true; }}, {{ passive: true }});
}})();
</script>
"""

(HERE / "breadboard.html").write_text(page)
print(HERE / "breadboard.html")
