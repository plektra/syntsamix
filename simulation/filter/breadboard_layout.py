#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Board layout for the SSI2144 test circuit, with a netlist check.

The whole test circuit is soldered on one Electrokit ProtoPCB EKB14 (the
ladder capacitors' solderless contacts were loose, 2026-10-20), with the
RV3-RV5 trimmers (Bourns 3296W, pins in line). Only the RV1 and RV2 pots,
the jacks and the bench supply are off the board, on flying leads. The script checks that the board's connections
match the schematic netlist exactly (no missing connections, no shorts)
and draws the board as SVG.

Usage:  python3 simulation/filter/breadboard_layout.py [--literal]
Exits with an error if the layout does not match the schematic.

EKB14 model (maker's drawing, Electrokit 41003657): columns 1..23. Rows A-E
(top) and F-J (bottom); the five holes of a half-column are one node.
Three rails: +15 V along the top edge (columns 1-23), GND along the strip
between the two halves (columns -1..25: two extra holes at each end), -15 V
along the bottom edge (columns 1-23). Vertical spacing in hole pitches:
top rail 0, A-E 2-6, GND rail 7.5, F-J 9-13, bottom rail 15.
U1 (SSI2144 on the SparkFun BOB-13994 adapter, pin rows 500 mil apart) sits
on female header sockets in rows D and G, columns 8-15, dot to the left:
pin 1 at 8G, pin 16 at 8D. U2 (TL072, DIP-8) straddles the GND rail in rows
E and F, columns 18-21, notch to the left: pin 1 at 18F, pin 8 at 18E.
The holes under each chip body stay free.
"""

import math
import sys
from html import escape
from collections import defaultdict
from pathlib import Path

LITERAL = "--literal" in sys.argv

# --------------------------------------------------------------- placement
# Endpoint forms:
#   ("E", col, "A".."J") a strip hole
#   ("ER", rail, col)    a rail hole: rail "P15" (top), "GND" (middle), "N15" (bottom)
#   ("X", name)          an off-board terminal (pot, jack, bench supply)
U1_TOP = {16: 8, 15: 9, 14: 10, 13: 11, 12: 12, 11: 13, 10: 14, 9: 15}   # row D
U1_BOT = {1: 8, 2: 9, 3: 10, 4: 11, 5: 12, 6: 13, 7: 14, 8: 15}          # row G
U2_TOP = {8: 18, 7: 19, 6: 20, 5: 21}                                    # row E
U2_BOT = {1: 18, 2: 19, 3: 20, 4: 21}                                    # row F
CHIPS = (("U1", U1_TOP, "D", U1_BOT, "G", range(8, 16), ("E", "F")),
         ("U2", U2_TOP, "E", U2_BOT, "F", range(18, 22), ()))

PARTS = [
    # ref, value, kind, end A, end B
    # ---- supply entry: bench supply leads, 10 µF per rail, reverse-polarity diodes
    ("L11", "+15 V", "lead", ("ER", "P15", 1), ("X", "SUPPLY+")),
    ("L12", "0 V", "lead", ("ER", "GND", -1), ("X", "SUPPLY0")),
    ("L13", "−15 V", "lead", ("ER", "N15", 4), ("X", "SUPPLY−")),
    ("C14", "10 µF", "cap", ("ER", "P15", 15), ("E", 15, "A")),
    ("D1", "1N4001", "diode", ("E", 15, "C"), ("ER", "P15", 16)),     # anode GND, cathode +15 V
    ("W25", "", "wire", ("E", 1, "F"), ("ER", "GND", 0)),
    ("C15", "10 µF", "cap", ("E", 1, "J"), ("ER", "N15", 1)),         # + to GND, − to −15 V
    ("D2", "1N4001", "diode", ("ER", "N15", 2), ("E", 1, "I")),       # anode −15 V, cathode GND
    # ---- input (bottom half, left of U1)
    ("L4", "IN", "lead", ("E", 2, "H"), ("X", "IN")),
    ("C5", "10 µF bipolar", "cap", ("E", 2, "F"), ("E", 4, "F")),
    ("R1", "18 kΩ", "res", ("E", 4, "J"), ("E", 7, "J")),
    ("R3", "330 Ω", "res", ("E", 7, "F"), ("E", 5, "F")),
    ("R2", "200 Ω", "res", ("E", 7, "G"), ("E", 6, "G")),
    ("W14", "", "wire", ("E", 7, "H"), ("E", 8, "H")),
    ("J1", "drive", "jumper", ("E", 5, "H"), ("E", 6, "H")),
    ("W20", "", "wire", ("E", 6, "F"), ("ER", "GND", 6)),
    ("R4", "220 Ω", "res", ("E", 9, "I"), ("E", 6, "I")),
    ("C9", "3.3 nF opt.", "cap", ("E", 8, "J"), ("E", 9, "H")),
    # ---- ladder capacitors, straight across neighbouring adapter pins
    ("C4", "560 pF", "cap", ("E", 11, "H"), ("E", 12, "H")),
    ("C3", "6.8 nF", "cap", ("E", 13, "H"), ("E", 14, "J")),
    ("C1", "6.8 nF", "cap", ("E", 11, "C"), ("E", 12, "A")),
    ("C2", "6.8 nF", "cap", ("E", 13, "C"), ("E", 14, "A")),
    # ---- U1 supply, ground and decoupling
    ("W1", "", "wire", ("E", 8, "A"), ("ER", "P15", 8)),
    ("C10", "100 nF", "cap", ("ER", "P15", 7), ("E", 7, "A")),
    ("W22", "", "wire", ("E", 7, "E"), ("ER", "GND", 7)),
    ("W2", "", "wire", ("E", 15, "B"), ("ER", "GND", 16)),          # U1 pin 9 to GND
    ("W3", "", "wire", ("E", 15, "J"), ("ER", "N15", 15)),
    ("C11", "100 nF", "cap", ("ER", "N15", 16), ("E", 16, "J")),
    ("W21", "", "wire", ("E", 16, "F"), ("ER", "GND", 17)),
    # ---- cutoff (pin 15): FREQ node carried to column 6 by W13
    ("R8", "1 kΩ", "res", ("E", 9, "B"), ("E", 7, "B")),
    ("W13", "", "wire", ("E", 9, "C"), ("E", 6, "C")),
    ("R10", "470 kΩ", "res", ("E", 6, "A"), ("E", 5, "A")),
    ("R9", "100 kΩ", "res", ("E", 6, "B"), ("E", 4, "B")),
    ("W28", "", "wire", ("E", 5, "D"), ("E", 22, "G")),               # R10 to the RV4 wiper
    ("W26", "", "wire", ("E", 4, "A"), ("E", 19, "A")),               # R9 to U2 pin 7
    # ---- resonance (pin 14): Q node carried to column 3 by W23
    ("W23", "", "wire", ("E", 10, "C"), ("E", 3, "D")),
    ("R7", "510 Ω", "res", ("E", 3, "B"), ("E", 2, "B")),
    ("C8", "10 nF", "cap", ("E", 2, "E"), ("ER", "GND", 1)),
    ("R6", "33 k", "res", ("E", 3, "C"), ("E", 1, "C")),
    ("L1", "RV2 wiper", "lead", ("E", 1, "E"), ("X", "RV2.W")),
    # ---- U2 supply and decoupling
    ("W6", "", "wire", ("E", 18, "A"), ("ER", "P15", 18)),
    ("C12", "100 nF", "cap", ("ER", "P15", 21), ("E", 21, "A")),
    ("W10", "", "wire", ("E", 21, "D"), ("ER", "GND", 23)),
    ("W7", "", "wire", ("E", 21, "J"), ("ER", "N15", 21)),
    ("C13", "100 nF", "cap", ("ER", "N15", 20), ("E", 20, "J")),
    ("W8", "", "wire", ("E", 20, "G"), ("ER", "GND", 22)),
    # ---- U2A output stage (bottom): U1 OUT by W5, RV3 trimmer as the feedback resistor
    ("W5", "", "wire", ("E", 10, "J"), ("E", 19, "I")),
    ("C6", "100 pF", "cap", ("E", 19, "G"), ("E", 18, "G")),
    # trimmers: pin 1, wiper, pin 3; ("NC", col, row) = pin bent up, not soldered
    ("RV3", "50 kΩ trim", "trim", ("E", 19, "H"), ("E", 18, "H"), ("NC", 17, "H")),
    ("C7", "10 µF bipolar", "cap", ("E", 18, "J"), ("E", 17, "J")),
    ("L3", "OUT", "lead", ("E", 17, "G"), ("X", "OUT")),
    # ---- U2B summer (top)
    ("R11", "160 kΩ", "res", ("E", 20, "A"), ("E", 22, "A")),
    ("RV5", "50 kΩ trim", "trim", ("E", 22, "B"), ("E", 23, "B"), ("NC", 24, "B")),
    ("W29", "", "wire", ("E", 19, "D"), ("E", 23, "E")),              # U2 pin 7 to the RV5 wiper
    ("R12", "300 kΩ", "res", ("E", 20, "C"), ("E", 17, "C")),
    ("L5", "RV1 wiper", "lead", ("E", 17, "D"), ("X", "RV1.W")),
    ("R13", "100 kΩ", "res", ("E", 20, "B"), ("E", 16, "B")),
    ("L6", "CV", "lead", ("E", 16, "D"), ("X", "CV")),
    # ---- RV4 cutoff offset trimmer (bottom right): the full track between +15 V and −15 V
    ("RV4", "50 kΩ trim", "trim", ("E", 23, "I"), ("E", 22, "I"), ("E", 21, "I")),
    ("W30", "", "wire", ("E", 23, "F"), ("ER", "P15", 22)),           # RV4 pin 1 to +15 V
    # ---- pot ends to the rails
    ("L7", "RV1 CW", "lead", ("ER", "P15", 23), ("X", "RV1.CW")),
    ("L8", "RV1 CCW", "lead", ("ER", "N15", 23), ("X", "RV1.CCW")),
    ("L9", "RV2 CW", "lead", ("ER", "P15", 2), ("X", "RV2.CW")),
    ("L10", "RV2 CCW", "lead", ("ER", "GND", 2), ("X", "RV2.CCW")),
]

# Parts that lie flat across three or more columns: the holes under their bodies stay empty.
# Every other resistor spans one or two columns and stands upright.
FLAT = {"R1", "R4", "R12", "R13"}

EKB_ROWS = "ABCDEFGHIJ"
EKB_Y = {"A": 2, "B": 3, "C": 4, "D": 5, "E": 6, "F": 9, "G": 10, "H": 11, "I": 12, "J": 13}
EKB_RAIL_Y = {"P15": 0, "GND": 7.5, "N15": 15}
EKB_RAIL_COLS = {"P15": range(1, 24), "GND": range(-1, 26), "N15": range(1, 24)}

# Pins of the ICs as nodes, the holes they take and the holes under them
CHIP_PINS = {}
PIN_HOLES = set()
COVERED = set()
for chip, top, trow, bot, brow, cols, under in CHIPS:
    for pins, row in ((top, trow), (bot, brow)):
        for pin, col in pins.items():
            CHIP_PINS[f"{chip}.{pin}"] = ("E", col, "T" if row in "ABCDE" else "B")
            PIN_HOLES.add(("E", col, row))
    for col in cols:
        COVERED.add(("ER", "GND", col))
        COVERED.update(("E", col, r) for r in under)

# Expected netlist from the schematic (breadboard_schematic.py); RV1, RV2, jacks and supply are off board (X:)
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
    {"R10.2", "RV4.2"},
    {"U2.7", "R9.2", "RV5.2"},
    {"U2.6", "R11.1", "R12.1", "R13.1"},
    {"R11.2", "RV5.1"},
    {"R12.2", "X:RV1.W"},
    {"R13.2", "X:CV"},
    {"P15", "X:SUPPLY+", "U1.16", "U2.8", "C10.1", "C12.1", "X:RV1.CW", "X:RV2.CW", "RV4.1", "C14.1", "D1.2"},
    {"N15", "X:SUPPLY−", "U1.8", "U2.4", "C11.1", "C13.1", "X:RV1.CCW", "RV4.3", "C15.2", "D2.1"},
    {"GND", "X:SUPPLY0", "U1.9", "U2.3", "U2.5", "R2.2", "J1.2", "R4.2", "C8.2", "R8.2",
     "C10.2", "C11.2", "C12.2", "C13.2", "X:RV2.CCW", "C14.2", "C15.1", "D1.1", "D2.2"},
]


def node_of(end):
    if end[0] == "NC":
        return None
    if end[0] == "E":
        return ("E", end[1], "T" if end[2] in "ABCDE" else "B")
    if end[0] == "ER":
        return ("ER", end[1])
    return ("X", end[1])


def hole_ok(end):
    if end[0] == "E":
        return 1 <= end[1] <= 23 and end[2] in EKB_ROWS
    return end[1] in EKB_RAIL_COLS and end[2] in EKB_RAIL_COLS[end[1]]


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
    problems = []
    for ref, val, kind, *ends in PARTS:
        nodes = [node_of(e) for e in ends]
        if kind == "trim":
            for i, n in enumerate(nodes):
                if n is not None:
                    terminals[n].add(f"{ref}.{i + 1}")
                    find(n)
        for e in ends:
            if e[0] in ("E", "ER"):
                if not hole_ok(e):
                    problems.append(f"{ref}: {e} is not a hole on the EKB14")
                hole_use[e].append(ref)
        if kind == "trim":
            continue
        if kind in ("wire", "lead"):
            union(nodes[0], nodes[1])
        else:
            terminals[nodes[0]].add(f"{ref}.1")
            terminals[nodes[1]].add(f"{ref}.2")
        for n in nodes:
            find(n)
    for name, node in CHIP_PINS.items():
        terminals[node].add(name)
        find(node)
    for n in list(parent):
        if n[0] == "X":
            terminals[n].add("X:" + n[1])
        if n[0] == "ER":
            terminals[n].add(n[1])

    nets = defaultdict(set)
    for node, names in terminals.items():
        nets[find(node)] |= names
    got = [frozenset(v) for v in nets.values() if v]
    exp = [frozenset(s) for s in EXPECTED]
    for hole, refs in hole_use.items():
        if len(refs) > 1:
            problems.append(f"hole {hole} used by {refs}")
    for e in exp:
        if e not in got:
            match = [g for g in got if g & e]
            problems.append(f"expected net {sorted(e)} but board has {[sorted(m) for m in match]}")
    for g in got:
        if g not in exp and len(g) > 1:
            problems.append(f"unexpected net on board: {sorted(g)}")
    for hole, refs in hole_use.items():
        if hole in PIN_HOLES:
            problems.append(f"{refs} uses the chip pin hole {hole}")
        if hole in COVERED:
            problems.append(f"{refs} uses the hole {hole} under a chip")
    for ref, val, kind, a, b in [p for p in PARTS if p[0] in FLAT]:
        if a[0] != "E" or b[0] != "E" or a[2] != b[2] or abs(a[1] - b[1]) < 3:
            problems.append(f"{ref}: a flat part must lie along one row across three or more columns")
            continue
        for c in range(min(a[1], b[1]) + 1, max(a[1], b[1])):
            if ("E", c, a[2]) in hole_use:
                problems.append(f"{ref} lies over {c}{a[2]}, used by {hole_use[('E', c, a[2])]}")
    return problems


# --------------------------------------------------------------- drawing
INK = "#1d2430" if LITERAL else "var(--ink)"
MUTED = "#5b6474" if LITERAL else "var(--muted)"
ACCENT = "#b4540a" if LITERAL else "var(--accent)"
PCB = "#e4ecdf" if LITERAL else "var(--pcb)"
COPPER = "#b8862b" if LITERAL else "var(--copper)"
HOLE = "#b9b1a0" if LITERAL else "var(--hole)"
RED = "#c0392b" if LITERAL else "var(--rail-pos)"
BLUE = "#2e5aa8" if LITERAL else "var(--rail-neg)"
GRN = "#2f7d4f" if LITERAL else "var(--rail-gnd)"
CHIP = "#262b33" if LITERAL else "var(--chip)"
CHIPTXT = "#f3f1ea" if LITERAL else "var(--chip-text)"
KIND_COL = {"res": "#7a4b1e" if LITERAL else "var(--part-res)",
            "cap": "#1f6f8b" if LITERAL else "var(--part-cap)",
            "wire": "#6b6f78" if LITERAL else "var(--part-wire)",
            "lead": ACCENT, "jumper": ACCENT, "diode": INK,
            "trim": "#6b3fa0" if LITERAL else "var(--part-trim)"}

EP = 30                        # hole pitch in px
EX0 = 120                      # x of column 1
EY0 = 70                       # y of the top rail
EW = EX0 + 26 * EP + 70
EH = EY0 + 17 * EP + 20

# Drawn routes for wires that would otherwise cross parts (column, pitch units); the wires are insulated
ROUTE = {
    "W23": [(10, 4.5), (3, 4.5)],
    "W26": [(4, 1.55), (19, 1.55)],
    "W5": [(10, 14.2), (18.5, 14.2), (18.5, 12.5)],
    "W2": [(15.6, 3), (15.6, 7.0)],
    "W28": [(4.55, 5), (4.55, 0.45), (23.45, 0.45), (23.45, 10)],
    "W29": [(19, 5.45), (23, 5.45)],
    "W30": [(23.72, 9), (23.72, -0.55), (22, -0.55)],
}
# Tags for leads: (text, dx, dy, anchor); anchor None = numbered on the board, named in the key
ETAG = {
    "L4": ("IN", -10, 4, "end"),
    "L1": ("RV2 wiper", -10, 4, "end"),
    "L3": ("OUT", 0, 0, None),
    "L6": ("CV", 0, 0, None),
    "L5": ("RV1 wiper", 0, 0, None),
    "L11": ("supply +15 V", 0, -14, "middle"),
    "L12": ("supply 0 V", 0, -12, "middle"),
    "L13": ("supply −15 V", 0, 22, "middle"),
    "L9": ("RV2 CW", 0, 0, None),
    "L10": ("RV2 CCW", 0, 0, None),
    "L7": ("RV1 CW", 0, 0, None),
    "L8": ("RV1 CCW", 0, 0, None),
}
# Label placement for parts: (dx, dy, anchor) from the part's middle
ELABEL = {
    "C5": (0, -12, "middle"), "R1": (0, 18, "middle"), "R3": (-6, -9, "end"), "R2": (0, 18, "middle"),
    "J1": (0, -9, "middle"), "R4": (0, 18, "middle"), "C9": (10, 18, "start"), "C4": (0, 20, "middle"),
    "C3": (12, 4, "start"), "C1": (12, -2, "start"), "C2": (12, -2, "start"),
    "C10": (-10, 4, "end"), "C11": (10, 14, "start"), "R8": (0, -9, "middle"), "R10": (0, -9, "middle"),
    "R9": (0, -9, "middle"), "R7": (0, -9, "middle"), "R6": (0, 18, "middle"), "C8": (-10, 4, "end"),
    "C14": (-10, 4, "end"), "D1": (10, 0, "start"), "C15": (-10, 4, "end"), "D2": (10, 4, "start"),
    "C12": (10, 4, "start"), "C13": (-10, 4, "end"), "C6": (0, -9, "middle"), "C7": (0, 20, "middle"),
    "R11": (0, 18, "middle"), "R12": (0, 18, "middle"), "R13": (0, -9, "middle"),
    "RV3": (0, 24, "middle"), "RV4": (0, 24, "middle"), "RV5": (0, -14, "middle"),
}
KEYED = [r for r, t in ETAG.items() if t[3] is None]
# Hover text per part (the page script passes a fuller one); default: ref, value, holes
TIPS = {}

out = []


def add(s):
    out.append(s)


def halo_text(x, y, s, col, anchor="middle", size=11, weight=700):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
        + (f'fill="{col}">{s}</text>' if LITERAL else
           f'fill="{col}" stroke="{PCB}" stroke-width="3" paint-order="stroke">{s}</text>'))


def exy(end):
    if end[0] in ("E", "NC"):
        return EX0 + (end[1] - 1) * EP, EY0 + EKB_Y[end[2]] * EP
    return EX0 + (end[2] - 1) * EP, EY0 + EKB_RAIL_Y[end[1]] * EP


def hole_name(end):
    if end[0] == "NC":
        return "bent up, not soldered"
    if end[0] == "E":
        return f"{end[1]}{end[2]}"
    return {"P15": "+15 V rail", "GND": "GND rail", "N15": "−15 V rail"}[end[1]] + f", col {end[2]}"


def two_lead(a, b, kind, s=1.25):
    col = KIND_COL[kind]
    w = (2.6 if kind in ("wire", "jumper") else 2) * s
    dash = ' stroke-dasharray="4 3"' if kind == "jumper" else ""
    add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" '
        f'stroke-width="{w}" stroke-linecap="round"{dash}/>')
    for q in (a, b):
        add(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="{2.6 * s:.1f}" fill="{col}"/>')
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    rot = f'transform="rotate({ang:.1f} {mx:.1f} {my:.1f})"'
    if kind == "res":
        add(f'<rect x="{mx - 9 * s:.1f}" y="{my - 4 * s:.1f}" width="{18 * s:.1f}" height="{8 * s:.1f}" rx="3" fill="{col}" {rot}/>')
    elif kind == "diode":
        add(f'<rect x="{mx - 7 * s:.1f}" y="{my - 4 * s:.1f}" width="{14 * s:.1f}" height="{8 * s:.1f}" rx="2" fill="{col}" {rot}/>')
        add(f'<rect x="{mx + 3 * s:.1f}" y="{my - 4 * s:.1f}" width="{2.5 * s:.1f}" height="{8 * s:.1f}" fill="{PCB}" {rot}/>')
    elif kind == "cap":
        add(f'<rect x="{mx - 4 * s:.1f}" y="{my - 5 * s:.1f}" width="{8 * s:.1f}" height="{10 * s:.1f}" rx="2" fill="{col}" {rot}/>')
    return mx, my


def draw():
    # board outline (71.1 x 43.2 mm = 28 x 17 pitches) and mounting holes
    add(f'<rect x="{EX0 - 3.5 * EP}" y="{EY0 - 1.0 * EP}" width="{28 * EP}" height="{17 * EP}" rx="8" fill="{PCB}"/>')
    for mc, mu in ((-1.6, 1.0), (24.6, 1.0), (-1.6, 14.0), (24.6, 14.0)):
        add(f'<circle cx="{EX0 + (mc - 1) * EP}" cy="{EY0 + mu * EP}" r="{0.6 * EP}" fill="none" stroke="{HOLE}" stroke-width="1.5"/>')
    for c in range(1, 24):
        x = EX0 + (c - 1) * EP
        for y1, y2 in ((EKB_Y["A"], EKB_Y["E"]), (EKB_Y["F"], EKB_Y["J"])):
            add(f'<line x1="{x}" y1="{EY0 + y1 * EP}" x2="{x}" y2="{EY0 + y2 * EP}" stroke="{COPPER}" stroke-width="4" opacity=".55"/>')
        for r in EKB_ROWS:
            add(f'<circle cx="{x}" cy="{EY0 + EKB_Y[r] * EP}" r="5.5" fill="{PCB}" stroke="{COPPER}" stroke-width="2.4"/>')
        add(f'<text x="{x}" y="{EY0 - 40}" font-size="10" text-anchor="middle" fill="{MUTED}">{c}</text>')
        add(f'<text x="{x}" y="{EY0 + 15 * EP + 46}" font-size="10" text-anchor="middle" fill="{MUTED}">{c}</text>')
    for r in EKB_ROWS:
        add(f'<text x="{EX0 - 3.0 * EP}" y="{EY0 + EKB_Y[r] * EP + 4}" font-size="10" font-weight="600" text-anchor="middle" fill="{MUTED}">{r}</text>')
    for name, col, lab in (("P15", RED, "+15 V"), ("GND", GRN, "GND"), ("N15", BLUE, "−15 V")):
        cols = EKB_RAIL_COLS[name]
        y = EY0 + EKB_RAIL_Y[name] * EP
        xa, xb = EX0 + (cols[0] - 1) * EP, EX0 + (cols[-1] - 1) * EP
        add(f'<line x1="{xa}" y1="{y}" x2="{xb}" y2="{y}" stroke="{col}" stroke-width="3"/>')
        for c in cols:
            add(f'<circle cx="{EX0 + (c - 1) * EP}" cy="{y}" r="5.5" fill="{PCB}" stroke="{col}" stroke-width="2.4"/>')
        add(f'<text x="{xa - 14}" y="{y + 4}" font-size="10" font-weight="700" text-anchor="end" fill="{col}">{lab}</text>')
    for chip, top, trow, bot, brow, cols, under in CHIPS:
        x1 = EX0 + (cols[0] - 1) * EP - 0.5 * EP
        x2 = EX0 + (cols[-1] - 1) * EP + 0.5 * EP
        yt, yb = EY0 + EKB_Y[trow] * EP, EY0 + EKB_Y[brow] * EP
        open_group(chip, (x2 - 14, (yt + yb) / 2 - 22 if chip == "U1" else (yt + yb) / 2 - 18))
        add(f'<rect x="{x1}" y="{yt - 9}" width="{x2 - x1}" height="{yb - yt + 18}" rx="4" fill="{CHIP}" opacity=".93"/>')
        if chip == "U1":
            add(f'<circle cx="{x1 + 10}" cy="{yb - 16}" r="3" fill="{CHIPTXT}"/>')
            add(f'<text x="{(x1 + x2) / 2}" y="{(yt + yb) / 2 - 2}" font-size="12" font-weight="700" text-anchor="middle" fill="{CHIPTXT}">U1 SSI2144 on the adapter</text>')
            add(f'<text x="{(x1 + x2) / 2}" y="{(yt + yb) / 2 + 13}" font-size="10" text-anchor="middle" fill="{CHIPTXT}">sockets in rows D and G · dot = pin 1</text>')
        else:
            add(f'<path d="M {x1} {(yt + yb) / 2 - 7} a 7 7 0 0 1 0 14" fill="{PCB}"/>')
            add(f'<text x="{(x1 + x2) / 2 + 4}" y="{(yt + yb) / 2 + 4}" font-size="12" font-weight="700" text-anchor="middle" fill="{CHIPTXT}">U2 TL072</text>')
        for pins, yy in ((top, yt), (bot, yb)):
            for pin, col in pins.items():
                add(f'<text x="{EX0 + (col - 1) * EP}" y="{yy + 3.5}" font-size="9.5" font-weight="700" text-anchor="middle" fill="{CHIPTXT}">{pin}</text>')
        add("</g>")
    order = {"wire": 0, "jumper": 1, "cap": 2, "res": 2, "diode": 2, "trim": 3, "lead": 4}
    for ref, val, kind, *ends in sorted(PARTS, key=lambda p: order[p[2]]):
        col = KIND_COL[kind]
        open_group(ref, anchor(ref, kind, ends))
        draw_part(ref, kind, ends, col)
        add("</g>")


def open_group(ref, at):
    """Start a part's group; at = where the 'placed' check goes (on the part's body)."""
    add(f'<g class="part" data-ref="{escape(ref)}" data-ax="{at[0]:.1f}" data-ay="{at[1]:.1f}">'
        f'<title>{escape(tip(ref))}</title>')


def anchor(ref, kind, ends):
    """The middle of the part's body: a lead's hole, a trimmer's wiper, a wire's longest run."""
    if kind == "lead":
        return exy(ends[0])
    if kind == "trim":
        x, y = exy(ends[1])
        return x, y
    a, b = exy(ends[0]), exy(ends[1])
    if ref in ROUTE:
        pts = [a] + [(EX0 + (c - 1) * EP, EY0 + u * EP) for c, u in ROUTE[ref]] + [b]
        seg = max(zip(pts, pts[1:]), key=lambda s: math.dist(*s))
        return (seg[0][0] + seg[1][0]) / 2, (seg[0][1] + seg[1][1]) / 2
    return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2


def tip(ref):
    if ref in TIPS:
        return TIPS[ref]
    for p in PARTS:
        if p[0] == ref:
            holes = " → ".join(hole_name(e) for e in p[3:] if e[0] != "X")
            return f"{ref}  {p[1]}\n{holes}".strip()
    return ref


def hit(pts):
    """An invisible wide stroke so thin parts are easy to hover."""
    add(f'<polyline points="{" ".join(f"{q[0]:.1f},{q[1]:.1f}" for q in pts)}" fill="none" stroke="#000" '
        f'stroke-opacity="0" stroke-width="14" stroke-linecap="round" pointer-events="stroke"/>')


def draw_part(ref, kind, ends, col):
    if True:
        if kind == "lead":
            x, y = exy(ends[0])
            add(f'<circle cx="{x}" cy="{y}" r="11" fill="#000" fill-opacity="0"/>')
            add(f'<circle cx="{x}" cy="{y}" r="7.5" fill="none" stroke="{col}" stroke-width="2.4"/>')
            t, dx, dy, anc = ETAG[ref]
            if anc is None:
                halo_text(x + 9, y - 7, str(KEYED.index(ref) + 1), col, "start", size=10)
            else:
                halo_text(x + dx, y + dy, t, col, anc)
            return
        if kind == "trim":
            pts = [exy(e) for e in ends]
            xs = [q[0] for q in pts]
            y = pts[0][1]
            x1, x2 = min(xs) - 11, max(xs) + 11
            add(f'<rect x="{x1}" y="{y - 11}" width="{x2 - x1}" height="22" rx="5" fill="{PCB}" fill-opacity=".85" stroke="{col}" stroke-width="2.4"/>')
            for e, q in zip(ends, pts):
                if e[0] == "NC":
                    add(f'<circle cx="{q[0]}" cy="{q[1]}" r="3.4" fill="none" stroke="{col}" stroke-width="1.6" stroke-dasharray="2 1.5"/>')
                else:
                    add(f'<circle cx="{q[0]}" cy="{q[1]}" r="3.6" fill="{col}"/>')
            wx = pts[1][0]
            add(f'<path d="M {wx - 4} {y - 17} l 4 5 l 4 -5" fill="none" stroke="{col}" stroke-width="2"/>')
            dx, dy, anc = ELABEL.get(ref, (0, -14, "middle"))
            halo_text((x1 + x2) / 2 + dx, y + dy, ref, col, anc)
            return
        a, b = exy(ends[0]), exy(ends[1])
        if ref in ROUTE:
            pts = [a] + [(EX0 + (c - 1) * EP, EY0 + u * EP) for c, u in ROUTE[ref]] + [b]
            hit(pts)
            add(f'<polyline points="{" ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)}" fill="none" stroke="{col}" '
                f'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
            for q in (a, b):
                add(f'<circle cx="{q[0]}" cy="{q[1]}" r="3.2" fill="{col}"/>')
            return
        hit([a, b])
        mx, my = two_lead(a, b, kind)
        if kind == "wire":
            return
        dx, dy, anc = ELABEL.get(ref, (0, -10, "middle"))
        halo_text(mx + dx, my + dy, ref, col, anc)


def key_rows():
    """Numbered lead tags drawn on the board: (number, text, hole)."""
    ends = {p[0]: p[3] for p in PARTS}
    return [(i + 1, ETAG[r][0], hole_name(ends[r])) for i, r in enumerate(KEYED)]


def render_svg(tips=None):
    """The board drawing as an SVG string; tips maps refs to hover text."""
    TIPS.clear()
    TIPS.update(tips or {})
    out.clear()
    draw()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {EW} {EH}" width="{EW}" height="{EH}" '
           f'font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" aria-label="SSI2144 test circuit on the EKB14 board">'
           + (f'<rect width="{EW}" height="{EH}" fill="#ffffff"/>' if LITERAL else "")
           + "".join(out) + "</svg>")


if __name__ == "__main__":
    probs = check()
    if probs:
        print("LAYOUT DOES NOT MATCH SCHEMATIC:")
        for p in probs:
            print(" -", p)
        sys.exit(1)
    print("Layout matches the schematic netlist.")
    svg = render_svg()
    dest = Path(__file__).with_name("ekb14-layout-preview.svg" if LITERAL else "ekb14-layout.svg")
    dest.write_text(svg)
    print(dest)
