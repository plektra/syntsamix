#!/usr/bin/env python3
"""Breadboard layout for the SSI2144 test circuit, with a netlist check.

Describes where every part goes on a standard solderless breadboard, checks
that the resulting connections match the schematic netlist exactly (no
missing connections, no shorts), and draws the layout as SVG.

Usage:  python3 simulation/filter/breadboard_layout.py [--literal]
Exits with an error if the layout does not match the schematic.

Board model: columns 1..45. Each column has a top half (rows f-j) and a
bottom half (rows a-e); the five holes of a half are one node. Rails: +15 V
along the top edge, GND below it; GND and -15 V along the bottom edge.
U1 (SSI2144 on a DIP-16 adapter) straddles the centre gap at columns 8-15,
notch to the left: pin 1 at bottom column 8, pin 16 at top column 8.
U2 (TL072) at columns 30-33, notch to the left: pin 1 at bottom column 30.
"""

import sys
from collections import defaultdict
from pathlib import Path

LITERAL = "--literal" in sys.argv

# --------------------------------------------------------------- placement
# Endpoint forms: ("T", col, row) top half, rows f..j as 0..4 (0 = row f, next to the gap)
#                 ("B", col, row) bottom half, rows e..a as 0..4 (0 = row e, next to the gap)
#                 ("R", rail, col) a rail hole above/below column col
#                 ("X", name) an off-board part terminal (pot, jack)
U1_TOP = {16: 8, 15: 9, 14: 10, 13: 11, 12: 12, 11: 13, 10: 14, 9: 15}
U1_BOT = {1: 8, 2: 9, 3: 10, 4: 11, 5: 12, 6: 13, 7: 14, 8: 15}
U2_TOP = {8: 30, 7: 31, 6: 32, 5: 33}
U2_BOT = {1: 30, 2: 31, 3: 32, 4: 33}

PARTS = [
    # ref, value, kind, end A, end B (trimmers: end A, wiper, end B)
    # ---- input (bottom half, left of U1)
    ("C5", "10 µF film", "cap", ("B", 2, 2), ("B", 4, 2)),
    ("R1", "17.4 kΩ", "res", ("B", 4, 1), ("B", 8, 1)),
    ("C9", "3.3 nF opt.", "cap", ("B", 8, 2), ("B", 9, 2)),
    ("R3", "330 Ω", "res", ("B", 8, 3), ("B", 5, 3)),
    ("J1", "drive", "jumper", ("B", 5, 4), ("R", "GNDB", 5)),
    ("R2", "200 Ω", "res", ("B", 8, 4), ("R", "GNDB", 8)),
    ("R4", "200 Ω", "res", ("B", 9, 4), ("R", "GNDB", 9)),
    ("L4", "IN", "lead", ("B", 2, 4), ("X", "IN")),
    # ---- ladder capacitors
    ("C4", "560 pF", "cap", ("B", 11, 2), ("B", 12, 2)),
    ("C3", "6.8 nF", "cap", ("B", 13, 2), ("B", 14, 2)),
    ("C1", "6.8 nF", "cap", ("T", 11, 1), ("T", 12, 1)),
    ("C2", "6.8 nF", "cap", ("T", 13, 1), ("T", 14, 1)),
    # ---- U1 supply and decoupling (decoupling caps sit across the rails)
    ("W1", "", "wire", ("T", 8, 4), ("R", "P15", 8)),
    ("C10", "100 nF", "cap", ("R", "P15", 7), ("R", "GNDT", 7)),
    ("W2", "", "wire", ("T", 15, 4), ("R", "GNDT", 15)),
    ("W3", "", "wire", ("B", 15, 4), ("R", "N15", 15)),
    ("C11", "100 nF", "cap", ("R", "N15", 16), ("R", "GNDB", 16)),
    # ---- resonance (top half, left of U1)
    ("R7", "499 Ω", "res", ("T", 10, 1), ("T", 6, 1)),
    ("C8", "10 nF", "cap", ("T", 6, 4), ("R", "GNDT", 6)),
    ("R6", "33.2 k → 49.9 k", "res", ("T", 10, 3), ("T", 3, 3)),
    ("L1", "RV2 wiper", "lead", ("T", 3, 2), ("X", "RV2.W")),
    # ---- cutoff: FREQ node extended to column 18
    ("W13", "", "wire", ("T", 9, 2), ("T", 18, 2)),
    ("R8", "1 kΩ", "res", ("T", 18, 4), ("R", "GNDT", 18)),
    ("R10", "499 kΩ", "res", ("T", 18, 3), ("T", 22, 3)),
    ("L2", "RV4 wiper", "lead", ("T", 22, 4), ("X", "RV4.W")),
    ("R9", "100 kΩ", "res", ("T", 18, 1), ("T", 25, 1)),
    ("W4", "", "wire", ("T", 25, 2), ("T", 31, 2)),
    # ---- U2 supply and decoupling
    ("W6", "", "wire", ("T", 30, 4), ("R", "P15", 30)),
    ("C12", "100 nF", "cap", ("R", "P15", 29), ("R", "GNDT", 29)),
    ("W7", "", "wire", ("B", 33, 4), ("R", "N15", 33)),
    ("C13", "100 nF", "cap", ("R", "N15", 34), ("R", "GNDB", 34)),
    # ---- U2A output stage (bottom): U1 OUT to INA-, trimmer and 100 pF across INA- and OUTA
    ("W5", "", "wire", ("B", 10, 1), ("B", 31, 1)),
    ("C6", "100 pF", "cap", ("B", 31, 2), ("B", 30, 2)),
    ("RV3", "50 kΩ trim", "trim", ("B", 31, 4), ("B", 30, 4), ("B", 29, 4)),
    ("W8", "", "wire", ("B", 32, 4), ("R", "GNDB", 32)),
    ("C7", "10 µF film", "cap", ("B", 30, 3), ("B", 25, 3)),
    ("L3", "OUT", "lead", ("B", 25, 4), ("X", "OUT")),
    # ---- U2B summer (top)
    ("W10", "", "wire", ("T", 33, 4), ("R", "GNDT", 33)),
    ("R11", "162 kΩ", "res", ("T", 32, 1), ("T", 28, 1)),
    ("RV5", "50 kΩ trim", "trim", ("T", 28, 4), ("T", 27, 4), ("T", 26, 4)),
    ("W11", "", "wire", ("T", 27, 3), ("T", 31, 3)),
    ("R12", "301 kΩ", "res", ("T", 32, 2), ("T", 41, 2)),
    ("L5", "RV1 wiper", "lead", ("T", 41, 3), ("X", "RV1.W")),
    ("R13", "100 kΩ", "res", ("T", 32, 3), ("T", 35, 3)),
    ("L6", "CV", "lead", ("T", 35, 4), ("X", "CV")),
    # ---- join the two ground rails
    ("W12", "", "wire", ("R", "GNDT", 44), ("R", "GNDB", 44)),
    # ---- off-board pot ends to rails (not drawn; listed under the drawing)
    ("L7", "", "lead", ("R", "P15", 42), ("X", "RV1.CW")),
    ("L8", "", "lead", ("R", "N15", 42), ("X", "RV1.CCW")),
    ("L9", "", "lead", ("R", "P15", 3), ("X", "RV2.CW")),
    ("L10", "", "lead", ("R", "GNDT", 2), ("X", "RV2.CCW")),
    ("L11", "", "lead", ("R", "P15", 5), ("X", "RV4.A")),
    ("L12", "", "lead", ("R", "N15", 5), ("X", "RV4.B")),
]

# Pins of the ICs as nodes
CHIP_PINS = {}
for pin, col in U1_TOP.items():
    CHIP_PINS[f"U1.{pin}"] = ("T", col)
for pin, col in U1_BOT.items():
    CHIP_PINS[f"U1.{pin}"] = ("B", col)
for pin, col in U2_TOP.items():
    CHIP_PINS[f"U2.{pin}"] = ("T", col)
for pin, col in U2_BOT.items():
    CHIP_PINS[f"U2.{pin}"] = ("B", col)

# Expected netlist from the schematic (breadboard_schematic.py)
EXPECTED = [
    {"X:IN", "C5.1"},
    {"C5.2", "R1.1"},
    {"U1.1", "R1.2", "R2.1", "R3.1", "C9.1"},
    {"R3.2", "J1.1"},
    {"U1.2", "R4.1", "C9.2"},
    {"U1.3", "U2.2", "C6.1", "RV3.1"},
    {"U2.1", "C6.2", "RV3.2", "C7.1"},
    {"C7.2", "X:OUT"},
    {"U1.4", "C4.1"}, {"U1.5", "C4.2"}, {"U1.6", "C3.1"}, {"U1.7", "C3.2"},
    {"U1.13", "C1.1"}, {"U1.12", "C1.2"}, {"U1.11", "C2.1"}, {"U1.10", "C2.2"},
    {"U1.14", "R7.1", "R6.1"},
    {"R7.2", "C8.1"},
    {"R6.2", "X:RV2.W"},
    {"U1.15", "R8.1", "R9.1", "R10.1"},
    {"R10.2", "X:RV4.W"},
    {"U2.7", "R9.2", "RV5.2"},
    {"U2.6", "R11.1", "R12.1", "R13.1"},
    {"R11.2", "RV5.1"},
    {"R12.2", "X:RV1.W"},
    {"R13.2", "X:CV"},
    {"P15", "U1.16", "U2.8", "C10.1", "C12.1", "X:RV1.CW", "X:RV2.CW", "X:RV4.A"},
    {"N15", "U1.8", "U2.4", "C11.1", "C13.1", "X:RV1.CCW", "X:RV4.B"},
    {"GND", "U1.9", "U2.3", "U2.5", "R2.2", "J1.2", "R4.2", "C8.2", "R8.2",
     "C10.2", "C11.2", "C12.2", "C13.2", "X:RV2.CCW"},
]


def node_of(end):
    k = end[0]
    if k in ("T", "B"):
        return (k, end[1])
    if k == "R":
        return ("R", end[1])
    return ("X", end[1])


def check():
    parent = {}

    def find(a):
        parent.setdefault(a, a)
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        parent[find(a)] = find(b)

    terminals = defaultdict(set)  # node -> terminal names
    hole_use = defaultdict(list)
    for ref, val, kind, *ends in PARTS:
        nodes = [node_of(e) for e in ends]
        for e in ends:
            if e[0] in ("T", "B"):
                hole_use[(e[0], e[1], e[2])].append(ref)
        if kind in ("wire", "lead"):
            union(nodes[0], nodes[1])
        elif kind == "jumper":
            # J1 fitted: treat as two terminals (the schematic shows it as a jumper)
            terminals[nodes[0]].add(f"{ref}.1")
            terminals[nodes[1]].add(f"{ref}.2")
        elif kind == "trim":
            # end A, wiper, end B; used as a rheostat: end A and wiper
            terminals[nodes[0]].add(f"{ref}.1")
            terminals[nodes[1]].add(f"{ref}.2")
            find(nodes[2])
        else:
            terminals[nodes[0]].add(f"{ref}.1")
            terminals[nodes[1]].add(f"{ref}.2")
        for n in nodes:
            find(n)
    for name, node in CHIP_PINS.items():
        terminals[node].add(name)
        find(node)
    union(("R", "GNDT"), ("R", "GNDB"))
    for n in list(parent):
        if n[0] == "X":
            terminals[n].add("X:" + n[1])
        if n[0] == "R":
            terminals[n].add({"P15": "P15", "N15": "N15", "GNDT": "GND", "GNDB": "GND"}[n[1]])

    nets = defaultdict(set)
    for node, names in terminals.items():
        nets[find(node)] |= names
    got = [frozenset(v) for v in nets.values() if v]
    exp = [frozenset(s) for s in EXPECTED]
    problems = []
    # hole and column capacity
    for hole, refs in hole_use.items():
        if len(refs) > 1:
            problems.append(f"hole {hole} used by {refs}")
    for node in parent:
        if node[0] in ("T", "B"):
            used = len([h for h in hole_use if (h[0], h[1]) == node])
            pins = sum(1 for p in CHIP_PINS.values() if p == node)
            if used + pins > 5:
                problems.append(f"column {node} needs {used + pins} holes")
    for e in exp:
        if e not in got:
            match = [g for g in got if g & e]
            problems.append(f"expected net {sorted(e)} but board has {[sorted(m) for m in match]}")
    for g in got:
        if g not in exp and len(g) > 1:
            if not any(g == e for e in exp):
                problems.append(f"unexpected net on board: {sorted(g)}")
    # trimmer pins must not be on a used chip row etc. (rows 0 next to gap hold chip pins)
    for (half, col, row), refs in hole_use.items():
        if row == 0 and any(CHIP_PINS[p] == (half, col) for p in CHIP_PINS):
            problems.append(f"{refs} uses the chip pin hole at {half}{col} row 0")
    return problems


# --------------------------------------------------------------- drawing
P = 18          # hole pitch in px
X0 = 70
NCOL = 45
Y_P15, Y_GT = 40, 58
YT = [168, 150, 132, 114, 96]      # top rows f..j  (index 0 = row f)
YB = [204, 222, 240, 258, 276]     # bottom rows e..a (index 0 = row e)
Y_GB, Y_N15 = 312, 330
W, H = X0 + NCOL * P + 40, 360

INK = "#1d2430" if LITERAL else "var(--ink)"
MUTED = "#5b6474" if LITERAL else "var(--muted)"
ACCENT = "#b4540a" if LITERAL else "var(--accent)"
BOARD = "#efe9dc" if LITERAL else "var(--board)"
HOLE = "#b9b1a0" if LITERAL else "var(--hole)"
RED = "#c0392b" if LITERAL else "var(--rail-pos)"
BLUE = "#2e5aa8" if LITERAL else "var(--rail-neg)"
GRN = "#2f7d4f" if LITERAL else "var(--rail-gnd)"
CHIP = "#262b33" if LITERAL else "var(--chip)"
CHIPTXT = "#f3f1ea" if LITERAL else "var(--chip-text)"
KIND_COL = {"res": "#7a4b1e" if LITERAL else "var(--part-res)",
            "cap": "#1f6f8b" if LITERAL else "var(--part-cap)",
            "wire": "#6b6f78" if LITERAL else "var(--part-wire)",
            "lead": ACCENT, "jumper": ACCENT,
            "trim": "#6b3fa0" if LITERAL else "var(--part-trim)"}
RAIL_Y = {"P15": Y_P15, "GNDT": Y_GT, "GNDB": Y_GB, "N15": Y_N15}

out = []


def add(s):
    out.append(s)


def xy(end):
    k = end[0]
    if k == "T":
        return X0 + (end[1] - 1) * P, YT[end[2]]
    if k == "B":
        return X0 + (end[1] - 1) * P, YB[end[2]]
    if k == "R":
        return X0 + (end[2] - 1) * P, RAIL_Y[end[1]]
    return None


TAG_SIDE = {"L1": "right", "L2": "right", "L3": "left", "L4": "left", "L5": "right", "L6": "right"}
LABEL_SIDE = {"R2": "left", "R4": "right", "J1": "left", "C8": "right", "R8": "right",
              "W1": None, "C10": "right", "C11": "right", "C12": "right", "C13": "right"}


def halo_text(x, y, s, col, anchor="middle", size=9, weight=700):
    add(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        + (f'fill="{col}">{s}</text>' if LITERAL else
           f'fill="{col}" stroke="{BOARD}" stroke-width="3" paint-order="stroke">{s}</text>'))


def draw():
    add(f'<rect x="{X0 - 30}" y="18" width="{NCOL * P + 44}" height="336" rx="10" fill="{BOARD}"/>')
    # rails
    for name, y, col, lab in (("P15", Y_P15, RED, "+15 V"), ("GNDT", Y_GT, GRN, "GND"),
                              ("GNDB", Y_GB, GRN, "GND"), ("N15", Y_N15, BLUE, "−15 V")):
        add(f'<line x1="{X0 - 14}" y1="{y}" x2="{X0 + (NCOL - 1) * P + 10}" y2="{y}" stroke="{col}" stroke-width="2"/>')
        add(f'<text x="{X0 - 36}" y="{y + 4}" font-size="10" font-weight="700" text-anchor="end" fill="{col}">{lab}</text>')
        for c in range(1, NCOL + 1):
            add(f'<rect x="{X0 + (c - 1) * P - 2.5}" y="{y - 2.5}" width="5" height="5" rx="1" fill="{HOLE}"/>')
    # holes, column numbers, row letters
    for c in range(1, NCOL + 1):
        x = X0 + (c - 1) * P
        for y in YT + YB:
            add(f'<rect x="{x - 2.5}" y="{y - 2.5}" width="5" height="5" rx="1" fill="{HOLE}"/>')
        if c == 1 or c % 5 == 0:
            add(f'<text x="{x}" y="31" font-size="9" text-anchor="middle" fill="{MUTED}">{c}</text>')
            add(f'<text x="{x}" y="345" font-size="9" text-anchor="middle" fill="{MUTED}">{c}</text>')
    for i, r in enumerate("fghij"):
        add(f'<text x="{X0 - 22}" y="{YT[i] + 3}" font-size="9" text-anchor="middle" fill="{MUTED}">{r}</text>')
    for i, r in enumerate("edcba"):
        add(f'<text x="{X0 - 22}" y="{YB[i] + 3}" font-size="9" text-anchor="middle" fill="{MUTED}">{r}</text>')
    # chips
    for name, c1, c2, label, top_pins, bot_pins in (
            ("U1", 8, 15, "U1 SSI2144 on adapter", U1_TOP, U1_BOT),
            ("U2", 30, 33, "U2 TL072", U2_TOP, U2_BOT)):
        x1 = X0 + (c1 - 1) * P - 9
        x2 = X0 + (c2 - 1) * P + 9
        add(f'<rect x="{x1}" y="{YT[0] - 6}" width="{x2 - x1}" height="{YB[0] - YT[0] + 12}" rx="3" fill="{CHIP}"/>')
        add(f'<path d="M {x1} {(YT[0] + YB[0]) / 2 - 6} a 6 6 0 0 1 0 12" fill="{BOARD}"/>')
        add(f'<text x="{(x1 + x2) / 2 + 3}" y="{(YT[0] + YB[0]) / 2 + 4}" font-size="9.5" font-weight="700" text-anchor="middle" fill="{CHIPTXT}">{label}</text>')
        for pin, col in top_pins.items():
            add(f'<text x="{X0 + (col - 1) * P}" y="{YT[0] + 3}" font-size="7.5" font-weight="700" text-anchor="middle" fill="{CHIPTXT}">{pin}</text>')
        for pin, col in bot_pins.items():
            add(f'<text x="{X0 + (col - 1) * P}" y="{YB[0] + 3}" font-size="7.5" font-weight="700" text-anchor="middle" fill="{CHIPTXT}">{pin}</text>')
    # parts: wires first, then components, then tags
    order = {"wire": 0, "jumper": 1, "cap": 2, "res": 2, "trim": 3, "lead": 4}
    for ref, val, kind, *ends in sorted(PARTS, key=lambda p: order[p[2]]):
        col = KIND_COL[kind]
        if kind == "lead":
            if ends[0][0] == "R":
                continue  # pot ends to rails: listed under the drawing
            x, y = xy(ends[0])
            add(f'<circle cx="{x}" cy="{y}" r="4" fill="none" stroke="{col}" stroke-width="2"/>')
            side = TAG_SIDE.get(ref, "right")
            if side == "right":
                halo_text(x + 8, y + 3.5, f"→ {val}", col, "start", size=9.5)
            else:
                halo_text(x - 8, y + 3.5, f"{val} ←", col, "end", size=9.5)
            continue
        if kind == "trim":
            pts = [xy(e) for e in ends]
            xs = [q[0] for q in pts]
            add(f'<rect x="{min(xs) - 7}" y="{pts[0][1] - 8}" width="{max(xs) - min(xs) + 14}" height="16" rx="4" fill="{BOARD}" stroke="{col}" stroke-width="2"/>')
            for q in pts:
                add(f'<circle cx="{q[0]}" cy="{q[1]}" r="2.8" fill="{col}"/>')
            wx = pts[1][0]
            add(f'<path d="M {wx - 3} {pts[1][1] - 12} l 3 4 l 3 -4" fill="none" stroke="{col}" stroke-width="1.5"/>')
            above = pts[0][1] < 186
            halo_text((min(xs) + max(xs)) / 2, pts[0][1] - 12 if above else pts[0][1] + 19, ref, col)
            continue
        a = xy(ends[0])
        b = xy(ends[1])
        w = 2.6 if kind in ("wire", "jumper") else 2
        dash = ' stroke-dasharray="4 3"' if kind == "jumper" else ""
        add(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"{dash}/>')
        for q in (a, b):
            add(f'<circle cx="{q[0]}" cy="{q[1]}" r="2.6" fill="{col}"/>')
        if kind == "wire":
            continue
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        ang = _ang(a, b)
        if kind == "res":
            add(f'<rect x="{mx - 9}" y="{my - 4}" width="18" height="8" rx="3" fill="{col}" transform="rotate({ang} {mx} {my})"/>')
        elif kind == "cap":
            add(f'<rect x="{mx - 4}" y="{my - 5}" width="8" height="10" rx="2" fill="{col}" transform="rotate({ang} {mx} {my})"/>')
        vertical = abs(a[0] - b[0]) < 1
        side = LABEL_SIDE.get(ref, "right" if vertical else None)
        text_s = ref
        if vertical:
            if side == "left":
                halo_text(mx - 8, my + 3, text_s, col, "end")
            else:
                halo_text(mx + 8, my + 3, text_s, col, "start")
        else:
            top_half = a[1] < 186
            halo_text(mx, my - 7 if top_half else my + 14, text_s, col)


def _ang(a, b):
    import math
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


if __name__ == "__main__":
    probs = check()
    if probs:
        print("LAYOUT DOES NOT MATCH SCHEMATIC:")
        for p in probs:
            print(" -", p)
        sys.exit(1)
    print("Layout matches the schematic netlist.")
    draw()
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" role="img" aria-label="SSI2144 breadboard layout">'
           + (f'<rect width="{W}" height="{H}" fill="#ffffff"/>' if LITERAL else "")
           + "".join(out) + "</svg>")
    dest = Path(__file__).with_name("breadboard-layout-preview.svg" if LITERAL else "breadboard-layout.svg")
    dest.write_text(svg)
    print(dest)
