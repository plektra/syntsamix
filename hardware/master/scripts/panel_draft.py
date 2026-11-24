# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master section top panel: a first layout draft in the style of the channel strip panel.

Drawn by hardware/channel-card/scripts/panel_render.py on the same page (it imports this file). Panel 139.8 x 360 mm,
four columns of one strip width each: AUX, sidechain, compressor, master. Distances d are from the card's front
edge as on the channel card (panel front end = d - 21). Only the panel is drafted: nothing here is checked against
the master PCB (heatsink zone, headers, the headphone jack's depth). The controls come from the schematic.
"""
PW, PL = 139.8, 360.0
OFF_D = 21.0
COL = [17.475 + 34.95 * k for k in range(4)]            # column centres across the panel
TITLE = ["AUX", "SIDECHAIN", "COMPRESSOR", "MASTER"]
LED = {"red": "#e0483f", "yellow": "#e6bd3a", "green": "#46b46a", "white": "#ecebe6"}
# (legend, column, offset across, d, kind, knob diameter or LED colour)
CONTROLS = [
    ("SEND 1", 0, 0, 302, "pot", 16), ("RETURN 1", 0, 0, 274, "pot", 16),
    ("MUTE", 0, -11, 250, "button", "red"), ("DUCK", 0, 0, 250, "button", "green"), ("COMP", 0, 11, 250, "button", "green"),
    ("SEND 2", 0, 0, 222, "pot", 16), ("RETURN 2", 0, 0, 194, "pot", 16),
    ("MUTE", 0, -11, 170, "button", "red"), ("DUCK", 0, 0, 170, "button", "green"), ("COMP", 0, 11, 170, "button", "green"),
    ("SC BUS", 1, -7, 302, "button", "green"), ("LISTEN", 1, 7, 302, "button", "yellow"),
    ("SC LPF", 1, -8, 276, "pot", 14), ("BYPASS", 1, 8, 276, "button", "white"),
    ("THRESHOLD", 1, 0, 244, "pot", 16), ("DECAY", 1, 0, 214, "pot", 16), ("DEPTH", 1, 0, 184, "pot", 16),
    ("COMP ON", 2, 0, 280, "button", "green"),
    ("AMOUNT", 2, 0, 252, "pot", 16), ("RELEASE", 2, 0, 222, "pot", 16), ("MIX", 2, 0, 192, "pot", 16),
    ("PHONES", 3, -6, 302, "jack63", None), ("PFL", 3, 10, 302, "led", "yellow"),
    ("PHONES LEVEL", 3, 0, 274, "pot", 16),
    ("MASTER", 3, 0, 128, "pot", 24),
]
LABEL_DY = {"SC LPF": 10.0, "BYPASS": 10.0}
LINES = [(0, 238.0), (0, 157.0), (1, 262.0), (1, 167.0), (2, 175.0), (3, 258.0), (3, 164.0)]   # (column, d)
GR = [("1", -12), ("3", -6), ("6", 0), ("10", 6), ("15", 12)]      # gain-reduction LEDs, one row, yellow (decision 170)
GR_D = 304.0
METER = [("CLIP", "red"), ("+12", "red"), ("+9", "yellow"), ("+6", "yellow"), ("+3", "yellow"), ("0", "green"),
         ("−3", "green"), ("−6", "green"), ("−10", "green"), ("−15", "green"), ("−20", "green"),
         ("−30", "green")]
METER_TOP = 244.0             # CLIP; 12 LEDs at 6.0 mm pitch, L and R columns 7 mm apart


def svg(x0, title="master section"):
    """The master panel as SVG, its left edge at x0; the front is at the bottom of the drawing."""
    Y = lambda d: PL - (d + OFF_D) + 8
    o = [f'<g><text x="{x0 + PW / 2}" y="4.5" class="cap" text-anchor="middle">{title}</text>',
         f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>']
    for y in (8, 8 + PL - 20):
        o.append(f'<rect x="{x0}" y="{y}" width="{PW}" height="20" class="rail"/>')
        for sx in (COL[0], COL[3]):
            cy = y + 10
            o.append(f'<circle cx="{x0 + sx}" cy="{cy}" r="2.6" class="screw"/><path d="M{x0 + sx - 1.4} {cy}h2.8M{x0 + sx} {cy - 1.4}v2.8" class="slot"/>')
    for k, t in enumerate(TITLE):   # section names on the rear rail band, between the screws
        o.append(f'<text x="{x0 + COL[k]}" y="{8 + 16.5}" class="leg" text-anchor="middle">{t}</text>')
    for k, d in LINES:
        o.append(f'<path d="M{x0 + COL[k] - 15.4} {Y(d)}h30.8" class="sect"/>')
    for name, k, dx, d, kind, arg in CONTROLS:
        x, y = x0 + COL[k] + dx, Y(d)
        if kind == "pot":
            r = arg / 2
            o.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="knob"/><path d="M{x} {y - r + 0.7}v{r * 0.5}" class="pointer"/>')
            o.append(f'<text x="{x}" y="{y + LABEL_DY.get(name, r + 3.5)}" class="leg" text-anchor="middle">{name}</text>')
        elif kind == "button":
            o.append(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" rx="1.6" fill="{LED[arg]}" class="capbtn"/>')
            o.append(f'<text x="{x}" y="{y + LABEL_DY.get(name, 8.5)}" class="leg" text-anchor="middle">{name}</text>')
        elif kind == "jack63":
            o.append(f'<circle cx="{x}" cy="{y}" r="6.5" class="nut"/><circle cx="{x}" cy="{y}" r="3.2" class="hole"/>')
            o.append(f'<text x="{x}" y="{y + 10}" class="leg" text-anchor="middle">{name}</text>')
        else:   # a single indicator window
            o.append(f'<rect x="{x - 2.5}" y="{y - 2.75}" width="5" height="5.5" rx="0.6" class="bezel"/>'
                     f'<rect x="{x - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[arg]}" opacity="0.92"/>')
            o.append(f'<text x="{x}" y="{y + 10}" class="leg" text-anchor="middle">{name}</text>')
    # gain-reduction row
    gx, gy = x0 + COL[2], Y(GR_D)
    o.append(f'<rect x="{gx - 15}" y="{gy - 2.75}" width="30" height="5.5" rx="0.6" class="bezel"/>')
    for lab, dx in GR:
        o.append(f'<rect x="{gx + dx - 2.25}" y="{gy - 2}" width="4.5" height="4" rx="0.4" fill="{LED["yellow"]}" opacity="0.92"/>')
        o.append(f'<text x="{gx + dx}" y="{gy + 5.6}" class="sm" text-anchor="middle">{lab}</text>')
    o.append(f'<text x="{gx}" y="{gy + 9.2}" class="sm" text-anchor="middle">GAIN REDUCTION dB</text>')
    # stereo meter
    mx = x0 + COL[3]
    for side, dx in (("L", -3.5), ("R", 3.5)):
        o.append(f'<rect x="{mx + dx - 2.5}" y="{Y(METER_TOP) - 3.5}" width="5" height="73" rx="0.6" class="bezel"/>')
        for i, (lab, col) in enumerate(METER):
            y = Y(METER_TOP - 6 * i)
            o.append(f'<rect x="{mx + dx - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[col]}" opacity="0.92"/>')
            if side == "L":
                o.append(f'<text x="{mx - 7.4}" y="{y + 0.75}" class="sm" text-anchor="end">{lab}</text>')
        o.append(f'<text x="{mx + dx}" y="{Y(METER_TOP - 66) + 6.4}" class="sm" text-anchor="middle">{side}</text>')
    o.append("</g>")
    return "\n".join(o)


def table():
    groups = [("AUX", "SEND 1 and SEND 2 (send levels to the rear jacks), RETURN 1 and RETURN 2 (return levels), each return with MUTE, DUCK and COMP buttons"),
              ("Sidechain", "SC BUS and LISTEN buttons, SC LPF knob with its BYPASS button, THRESHOLD, DECAY and DEPTH knobs"),
              ("Compressor", "five gain-reduction LEDs (1, 3, 6, 10, 15 dB), COMP ON button, AMOUNT, RELEASE and MIX knobs"),
              ("Master", "headphone jack with the PFL light beside it, PHONES LEVEL knob, stereo meter of 2 × 12 LEDs, MASTER knob")]
    return "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in groups)
