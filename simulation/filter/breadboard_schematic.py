#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Draw the SSI2144 breadboard schematic as SVG.

Pinout and the ladder/output/Q component values follow the SSI2144 datasheet
(Rev 3.0, Figures 1 and 3, read from the datasheet images). Input attenuator,
drive jumper, resonance limit and cutoff scaling are this project's values
(see BREADBOARD.md and ../../docs/decisions/channel-card.md items 12 and 50).

Usage:  python3 simulation/filter/breadboard_schematic.py [--literal]
Writes breadboard-schematic.svg next to this file. Colours come from CSS
custom properties (--ink, --muted, --accent) so the page can theme it;
--literal writes plain colours instead, for previewing outside the page.
"""

import sys
from pathlib import Path

LITERAL = "--literal" in sys.argv
INK = "#1d2430" if LITERAL else "var(--ink)"
MUTED = "#5b6474" if LITERAL else "var(--muted)"
ACCENT = "#b4540a" if LITERAL else "var(--accent)"
BG = "#ffffff" if LITERAL else "var(--paper)"

out = []


def add(s):
    out.append(s)


def wire(*pts):
    add('<polyline fill="none" stroke="%s" stroke-width="1.6" points="%s"/>'
        % (INK, " ".join(f"{x},{y}" for x, y in pts)))


def dot(x, y):
    add(f'<circle cx="{x}" cy="{y}" r="3.6" fill="{INK}"/>')


def text(x, y, s, anchor="start", cls="lbl", size=12, weight=400, color=None):
    col = color or (INK if cls == "lbl" else MUTED)
    lines = s.split("\n")
    for i, line in enumerate(lines):
        add(f'<text x="{x}" y="{y + i * (size + 2)}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{col}">{line}</text>')


def term(x, y, label, side="left"):
    add(f'<circle cx="{x}" cy="{y}" r="5" fill="{BG}" stroke="{ACCENT}" stroke-width="2"/>')
    if side == "left":
        text(x - 10, y + 4, label, "end", weight=600, color=ACCENT)
    else:
        text(x + 10, y + 4, label, "start", weight=600, color=ACCENT)


def gnd(x, y):
    wire((x, y), (x, y + 10))
    for i, w in enumerate((11, 7, 3)):
        yy = y + 10 + i * 4
        add(f'<line x1="{x - w}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{INK}" stroke-width="1.6"/>')


def tag(x, y, label, side="right"):
    """Supply connection: short stub ending in a labelled flag."""
    dx = 16 if side == "right" else -16
    wire((x, y), (x + dx, y))
    add(f'<circle cx="{x + dx}" cy="{y}" r="2.6" fill="{BG}" stroke="{INK}" stroke-width="1.4"/>')
    if side == "right":
        text(x + dx + 6, y + 4, label, "start", cls="val", size=11, weight=600)
    else:
        text(x + dx - 6, y + 4, label, "end", cls="val", size=11, weight=600)


def resistor(x1, y1, x2, y2, name, value, lpos="above"):
    horiz = y1 == y2
    L = 44
    if horiz:
        xm = (x1 + x2) / 2
        a, b = (xm - L / 2, y1), (xm + L / 2, y1)
        if x1 > x2:
            a, b = b, a
        wire((x1, y1), a)
        wire(b, (x2, y2))
        s, e = min(a[0], b[0]), max(a[0], b[0])
        pts = [(s, y1)]
        n = 6
        for i in range(1, n + 1):
            pts.append((s + (e - s) * (i - 0.5) / n, y1 + (-6 if i % 2 else 6)))
        pts.append((e, y1))
        wire(*pts)
        if lpos == "above":
            text(xm, y1 - 12, f"{name} {value}", "middle", size=11)
        else:
            text(xm, y1 + 22, f"{name} {value}", "middle", size=11)
    else:
        ym = (y1 + y2) / 2
        a, b = (x1, ym - L / 2), (x1, ym + L / 2)
        if y1 > y2:
            a, b = b, a
        wire((x1, y1), a)
        wire(b, (x2, y2))
        s, e = min(a[1], b[1]), max(a[1], b[1])
        pts = [(x1, s)]
        n = 6
        for i in range(1, n + 1):
            pts.append((x1 + (-6 if i % 2 else 6), s + (e - s) * (i - 0.5) / n))
        pts.append((x1, e))
        wire(*pts)
        if lpos == "left":
            text(x1 - 12, ym, f"{name}\n{value}", "end", size=11)
        else:
            text(x1 + 12, ym, f"{name}\n{value}", "start", size=11)


def capacitor(x1, y1, x2, y2, name, value, lpos="right", polar=False):
    horiz = y1 == y2
    g = 5
    if horiz:
        xm = (x1 + x2) / 2
        wire((x1, y1), (xm - g, y1))
        wire((xm + g, y1), (x2, y2))
        add(f'<line x1="{xm - g}" y1="{y1 - 11}" x2="{xm - g}" y2="{y1 + 11}" stroke="{INK}" stroke-width="2"/>')
        add(f'<line x1="{xm + g}" y1="{y1 - 11}" x2="{xm + g}" y2="{y1 + 11}" stroke="{INK}" stroke-width="2"/>')
        if polar:
            plus_x = xm + g + 7 if x2 < x1 else xm - g - 7
            text(plus_x, y1 - 12, "+", "middle", size=11)
        text(xm, y1 - 16 if lpos != "below" else y1 + 26, f"{name} {value}", "middle", size=11)
    else:
        ym = (y1 + y2) / 2
        wire((x1, y1), (x1, ym - g))
        wire((x1, ym + g), (x2, y2))
        add(f'<line x1="{x1 - 11}" y1="{ym - g}" x2="{x1 + 11}" y2="{ym - g}" stroke="{INK}" stroke-width="2"/>')
        add(f'<line x1="{x1 - 11}" y1="{ym + g}" x2="{x1 + 11}" y2="{ym + g}" stroke="{INK}" stroke-width="2"/>')
        if lpos == "left":
            text(x1 - 16, ym - 2, f"{name}\n{value}", "end", size=11)
        else:
            text(x1 + 16, ym - 2, f"{name}\n{value}", "start", size=11)


def pot(x, ytop, ybot, wy, wiper_side, name, value, lpos, ly=None):
    """Vertical potentiometer between (x,ytop) and (x,ybot), wiper arrow at wy."""
    ym = (ytop + ybot) / 2
    L = 44
    a, b = ym - L / 2, ym + L / 2
    wire((x, ytop), (x, a))
    wire((x, b), (x, ybot))
    add(f'<rect x="{x - 7}" y="{a}" width="14" height="{L}" fill="{BG}" stroke="{INK}" stroke-width="1.6"/>')
    if wiper_side == "left":
        wire((x - 34, wy), (x - 9, wy))
        add(f'<polygon points="{x - 8},{wy} {x - 16},{wy - 4} {x - 16},{wy + 4}" fill="{INK}"/>')
    else:
        wire((x + 34, wy), (x + 9, wy))
        add(f'<polygon points="{x + 8},{wy} {x + 16},{wy - 4} {x + 16},{wy + 4}" fill="{INK}"/>')
    ty = ym + 30 if ly is None else ly
    if lpos == "left":
        text(x - 14, ty, f"{name}\n{value}", "end", size=11)
    else:
        text(x + 14, ty, f"{name}\n{value}", "start", size=11)


def opamp(tipx, tipy, pointing, name):
    """Op amp with output tip at (tipx,tipy); inputs 100 px behind. Returns (inv, noninv, out)."""
    w, h = 100, 100
    back = tipx + w if pointing == "left" else tipx - w
    add(f'<polygon points="{back},{tipy - h / 2} {back},{tipy + h / 2} {tipx},{tipy}" '
        f'fill="{BG}" stroke="{INK}" stroke-width="1.6"/>')
    inv, non = (back, tipy - 20), (back, tipy + 20)
    sx = back - 12 if pointing == "left" else back + 8
    text(sx, inv[1] + 5, "−", "start", size=15, weight=700)
    text(sx, non[1] + 5, "+", "start", size=15, weight=700)
    lx = (back + tipx) / 2
    text(lx, tipy + h / 2 + 18, name, "middle", size=11, weight=600)
    return inv, non, (tipx, tipy)


def jumper(x, y1, y2, name):
    add(f'<circle cx="{x}" cy="{y1 + 6}" r="4" fill="{BG}" stroke="{INK}" stroke-width="1.5"/>')
    add(f'<circle cx="{x}" cy="{y2 - 6}" r="4" fill="{BG}" stroke="{INK}" stroke-width="1.5"/>')
    add(f'<rect x="{x - 8}" y="{y1 + 1}" width="16" height="{y2 - y1 - 2}" rx="4" fill="none" '
        f'stroke="{ACCENT}" stroke-width="1.4" stroke-dasharray="3 2"/>')
    wire((x, y1), (x, y1 + 2))
    wire((x, y2 - 2), (x, y2))
    text(x + 14, (y1 + y2) / 2 + 4, name, "start", size=11, color=ACCENT, weight=600)


# ------------------------------------------------------------------ chip
PY = {1: 200, 2: 270, 3: 340, 4: 410, 5: 480, 6: 550, 7: 620, 8: 690,
      16: 200, 15: 270, 14: 340, 13: 410, 12: 480, 11: 550, 10: 620, 9: 690}
NAMES = {1: "SIG IN+", 2: "SIG IN−", 3: "OUT", 4: "C4A", 5: "C4B", 6: "C3A", 7: "C3B", 8: "V−",
         16: "V+", 15: "FREQ CTRL", 14: "Q CTRL", 13: "C1A", 12: "C1B", 11: "C2A", 10: "C2B", 9: "GND"}
BX1, BX2, BY1, BY2 = 500, 660, 160, 730
add(f'<rect x="{BX1}" y="{BY1}" width="{BX2 - BX1}" height="{BY2 - BY1}" rx="4" fill="{BG}" '
    f'stroke="{INK}" stroke-width="2"/>')
add(f'<path d="M {(BX1 + BX2) / 2 - 14} {BY1} a 14 14 0 0 0 28 0" fill="none" stroke="{INK}" stroke-width="1.6"/>')
text((BX1 + BX2) / 2, 430, "U1", "middle", size=15, weight=700)
text((BX1 + BX2) / 2, 450, "SSI2144", "middle", size=13, weight=600)
text((BX1 + BX2) / 2, 468, "on DIP adapter", "middle", cls="val", size=10)
for n, y in PY.items():
    left = n <= 8
    x0, x1 = (BX1, BX1 - 30) if left else (BX2, BX2 + 30)
    wire((x0, y), (x1, y))
    if left:
        text(BX1 + 8, y + 4, NAMES[n], "start", size=11, weight=600)
        text(BX1 - 6, y - 6, str(n), "end", cls="val", size=10)
    else:
        text(BX2 - 8, y + 4, NAMES[n], "end", size=11, weight=600)
        text(BX2 + 6, y - 6, str(n), "start", cls="val", size=10)

# ladder capacitors (datasheet Figure 1)
for a, b, nm, val, side in ((4, 5, "C4", "560 pF", "left"), (6, 7, "C3", "6.8 nF", "left"),
                            (13, 12, "C1", "6.8 nF", "right"), (11, 10, "C2", "6.8 nF", "right")):
    xc = 440 if side == "left" else 720
    wire((470 if side == "left" else 690, PY[a]), (xc, PY[a]))
    wire((470 if side == "left" else 690, PY[b]), (xc, PY[b]))
    if side == "left":
        capacitor(xc, PY[a], xc, PY[b], nm, val, lpos="left")
    else:
        capacitor(xc, PY[a], xc, PY[b], "", "", lpos="right")
        text(xc - 16, (PY[a] + PY[b]) / 2 - 2, f"{nm}\n{val}", "end", size=11)

# supply pins
wire((470, 690), (450, 690))
tag(450, 690, "−15 V", "left")
wire((690, 200), (705, 200))
tag(705, 200, "+15 V", "right")
wire((690, 690), (720, 690))
gnd(720, 690)

# ------------------------------------------------------------------ input
wire((470, 200), (350, 200))
dot(445, 200)
dot(350, 200)
capacitor(445, 200, 445, 270, "", "", lpos="right")
text(456, 232, "3.3 nF", "start", cls="val", size=10)
text(456, 244, "optional", "start", cls="val", size=10)
dot(445, 270)
wire((470, 270), (445, 270))
resistor(445, 270, 385, 270, "R4", "200 Ω", lpos="above")
gnd(385, 270)
resistor(350, 200, 350, 250, "R2", "200 Ω", lpos="right")
gnd(350, 250)
wire((350, 200), (300, 200))
dot(300, 200)
resistor(300, 200, 300, 240, "R3", "330 Ω (−4 dB)\nor 200 Ω (−6 dB)", lpos="left")
jumper(300, 240, 272, "")
text(286, 266, "J1 = medium drive", "end", size=11, color=ACCENT, weight=600)
gnd(300, 272)
resistor(300, 200, 200, 200, "R1", "17.4 kΩ", lpos="above")
capacitor(200, 200, 130, 200, "C5", "10 µF film")
term(130, 200, "IN", "left")

# ------------------------------------------------------------------ output I-V stage
wire((470, 340), (340, 340), (340, 830), (300, 830))
inv, non, o = opamp(200, 850, "left", "U2A  ½ TL072")
dot(315, 830)
wire((315, 830), (315, 700))
dot(315, 755)
capacitor(315, 700, 170, 700, "C6", "100 pF")
resistor(315, 755, 170, 755, "RV3", "50 kΩ trim, set ≈ 33 kΩ", lpos="above")
wire((170, 700), (170, 850))
dot(170, 755)
wire((200, 850), (170, 850))
dot(170, 850)
wire(non, (325, 870))
gnd(325, 870)
capacitor(170, 850, 100, 850, "C7", "10 µF film", lpos="below")
term(100, 850, "OUT", "left")

# ------------------------------------------------------------------ resonance (pin 14)
wire((690, 340), (760, 340))
dot(760, 340)
resistor(760, 340, 760, 400, "R7", "499 Ω", lpos="right")
capacitor(760, 400, 760, 460, "C8", "10 nF", lpos="right")
gnd(760, 460)
resistor(760, 340, 866, 340, "R6", "33.2 kΩ test → 49.9 kΩ", lpos="above")
pot(900, 296, 384, 340, "left", "RV2 10 kΩ", "RESONANCE", "right")
tag(900, 296, "+15 V", "right")
gnd(900, 384)

# ------------------------------------------------------------------ cutoff (pin 15)
wire((690, 270), (1000, 270))
dot(1000, 270)
resistor(1000, 270, 1000, 330, "R8", "1 kΩ", lpos="left")
gnd(1000, 330)
resistor(1000, 270, 1086, 270, "R10", "499 kΩ", lpos="below")
pot(1120, 226, 314, 270, "left", "RV4 50 kΩ", "offset trim", "right", ly=262)
tag(1120, 226, "+15 V", "right")
tag(1120, 314, "−15 V", "right")
# summer
i2, n2, o2 = opamp(960, 100, "right", "U2B  ½ TL072 (summer)")
wire(o2, (1000, 100))
dot(1000, 100)
resistor(1000, 100, 1000, 270, "R9", "100 kΩ", lpos="right")
wire(n2, (840, 120))
gnd(840, 120)
wire(i2, (810, 80))
dot(810, 80)
wire((810, 80), (810, 36))
resistor(810, 36, 1000, 36, "R11 162 kΩ + RV5 50 kΩ trim", "(1 V/oct)", lpos="above")
wire((1000, 36), (1000, 100))
resistor(810, 80, 714, 80, "R12", "301 kΩ", lpos="above")
pot(680, 36, 124, 80, "right", "RV1 10 kΩ lin", "CUTOFF", "left", ly=72)
tag(680, 36, "+15 V (CW end)", "left")
tag(680, 124, "−15 V", "left")
wire((810, 80), (810, 150))
resistor(810, 150, 720, 150, "R13", "100 kΩ", lpos="below")
term(720, 150, "CV (optional)", "left")

# notes
text(540, 790, "U2 = TL072: pin 8 to +15 V, pin 4 to −15 V, 100 nF to ground at each.", "start", cls="val", size=11)
text(540, 806, "U1: 100 nF from pin 16 and from pin 8 to ground, right at the adapter.", "start", cls="val", size=11)
text(540, 822, "Unmarked values from SSI2144 datasheet Rev 3.0, Figures 1 and 3.", "start", cls="val", size=11)

W, H = 1250, 930
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
       f'font-family="IBM Plex Sans, Helvetica, Arial, sans-serif" role="img" '
       f'aria-label="SSI2144 breadboard schematic">'
       + (f'<rect width="{W}" height="{H}" fill="{BG}"/>' if LITERAL else "")
       + "".join(out) + "</svg>")
dest = Path(__file__).with_name("breadboard-schematic.svg" if not LITERAL else "breadboard-schematic-preview.svg")
dest.write_text(svg)
print(dest)
