# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master section top panel: a layout draft in the style of the channel strip panel.

Drawn by hardware/channel-card/scripts/panel_render.py on the same page (it imports this file). Second draft
(the user, 2026-11-24: no columns, narrower, the headphone jack as far forward as it can go): three strips wide
(104.8 x 360 mm; decision 162 says four) with the functions as bands across the panel, rear to front: compressor,
sidechain, AUX, master. Positions are x across the panel and d from the card's front edge as on the channel card
(panel front end = d - 21). Only the panel is drafted: nothing here is checked against the master PCB (its 768
parts on a narrower board, the heatsink zone, the headers). The controls come from the schematic; the master level
is a rotary pot there (decision 92), so it is drawn as a knob.
"""
PW, PL = 104.8, 360.0
OFF_D = 21.0
LED = {"red": "#e0483f", "yellow": "#e6bd3a", "green": "#46b46a", "white": "#ecebe6"}
JACK_D = 92.0     # headphone jack: decision 162 keeps it about 90 mm behind the front edge (its depth under the panel)
# (legend, x, d, kind, knob diameter or LED colour)
CONTROLS = [
    # compressor
    ("COMP ON", 14, 290, "button", "green"), ("AMOUNT", 36, 290, "pot", 16), ("RELEASE", 58, 290, "pot", 16),
    ("MIX", 80, 290, "pot", 16),
    # sidechain: source and filter, then the envelope
    ("SC BUS", 16, 254, "button", "green"), ("LISTEN", 30, 254, "button", "yellow"),
    ("SC LPF", 56, 254, "pot", 14), ("BYPASS", 72, 254, "button", "white"),
    ("THRESHOLD", 20, 228, "pot", 16), ("DECAY", 52, 228, "pot", 16), ("DEPTH", 84, 228, "pot", 16),
    # AUX 1 and AUX 2, one row each
    ("SEND 1", 16, 196, "pot", 16), ("RETURN 1", 40, 196, "pot", 16),
    ("MUTE", 64, 196, "button", "red"), ("DUCK", 75, 196, "button", "green"), ("COMP", 86, 196, "button", "green"),
    ("SEND 2", 16, 170, "pot", 16), ("RETURN 2", 40, 170, "pot", 16),
    ("MUTE", 64, 170, "button", "red"), ("DUCK", 75, 170, "button", "green"), ("COMP", 86, 170, "button", "green"),
    # master
    ("MASTER", 56, 72, "pot", 24),
    ("PFL", 90, 140, "led", "yellow"), ("PHONES LEVEL", 88, 118, "pot", 16), ("PHONES", 88, JACK_D, "jack63", None),
]
LABEL_DY = {"SC LPF": 10.0, "BYPASS": 10.0}
LINES = [(268.0, "SIDECHAIN"), (210.0, "AUX"), (152.0, "MASTER")]    # (d, name of the band in front of the line)
TOP_TITLE = "COMPRESSOR"
GR = ["1", "3", "6", "10", "15"]     # gain-reduction LEDs top to bottom, yellow (decision 170)
GR_X, GR_TOP = 97.0, 303.0
METER = [("CLIP", "red"), ("+12", "red"), ("+9", "yellow"), ("+6", "yellow"), ("+3", "yellow"), ("0", "green"),
         ("−3", "green"), ("−6", "green"), ("−10", "green"), ("−15", "green"), ("−20", "green"),
         ("−30", "green")]
METER_X, METER_TOP = (12.0, 19.0), 132.0     # L and R columns; CLIP; 12 LEDs at 6.0 mm pitch


def svg(x0, title="master section, second draft"):
    """The master panel as SVG, its left edge at x0; the front is at the bottom of the drawing."""
    Y = lambda d: PL - (d + OFF_D) + 8
    o = [f'<g><text x="{x0 + PW / 2}" y="4.5" class="cap" text-anchor="middle">{title}</text>',
         f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>']
    for y in (8, 8 + PL - 20):
        o.append(f'<rect x="{x0}" y="{y}" width="{PW}" height="20" class="rail"/>')
        for sx in (17.4, PW - 17.4):
            cy = y + 10
            o.append(f'<circle cx="{x0 + sx}" cy="{cy}" r="2.6" class="screw"/><path d="M{x0 + sx - 1.4} {cy}h2.8M{x0 + sx} {cy - 1.4}v2.8" class="slot"/>')
    o.append(f'<text x="{x0 + PW - 3}" y="{Y(316)}" class="sm" text-anchor="end">{TOP_TITLE}</text>')
    for d, name in LINES:
        o.append(f'<path d="M{x0 + 2} {Y(d)}h{PW - 4}" class="sect"/>')
        o.append(f'<text x="{x0 + PW - 3}" y="{Y(d) + 3.6}" class="sm" text-anchor="end">{name}</text>')
    for name, cx, d, kind, arg in CONTROLS:
        x, y = x0 + cx, Y(d)
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
        else:   # a single indicator window, its legend at the left
            o.append(f'<rect x="{x - 2.5}" y="{y - 2.75}" width="5" height="5.5" rx="0.6" class="bezel"/>'
                     f'<rect x="{x - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[arg]}" opacity="0.92"/>')
            o.append(f'<text x="{x - 4}" y="{y + 0.9}" class="leg" text-anchor="end">{name}</text>')
    # gain-reduction column beside the compressor knobs
    gx = x0 + GR_X
    o.append(f'<rect x="{gx - 2.5}" y="{Y(GR_TOP) - 3.5}" width="5" height="31" rx="0.6" class="bezel"/>')
    for i, lab in enumerate(GR):
        y = Y(GR_TOP - 6 * i)
        o.append(f'<rect x="{gx - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED["yellow"]}" opacity="0.92"/>')
        o.append(f'<text x="{gx - 3.4}" y="{y + 0.75}" class="sm" text-anchor="end">{lab}</text>')
    o.append(f'<text x="{gx}" y="{Y(GR_TOP - 24) + 6.6}" class="sm" text-anchor="middle">GR dB</text>')
    # stereo meter
    for side, mx in zip("LR", METER_X):
        o.append(f'<rect x="{x0 + mx - 2.5}" y="{Y(METER_TOP) - 3.5}" width="5" height="73" rx="0.6" class="bezel"/>')
        for i, (lab, col) in enumerate(METER):
            y = Y(METER_TOP - 6 * i)
            o.append(f'<rect x="{x0 + mx - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[col]}" opacity="0.92"/>')
            if side == "R":
                o.append(f'<text x="{x0 + mx + 3.4}" y="{y + 0.75}" class="sm">{lab}</text>')
        o.append(f'<text x="{x0 + mx}" y="{Y(METER_TOP - 66) + 6.4}" class="sm" text-anchor="middle">{side}</text>')
    o.append("</g>")
    return "\n".join(o)


def table():
    groups = [("Compressor (rear)", "COMP ON button, AMOUNT, RELEASE and MIX knobs, five gain-reduction LEDs (1, 3, 6, 10, 15 dB) at the right"),
              ("Sidechain", "SC BUS and LISTEN buttons, SC LPF knob with its BYPASS button; below them THRESHOLD, DECAY and DEPTH"),
              ("AUX", "one row per bus: SEND and RETURN knobs, then MUTE, DUCK and COMP buttons for the return"),
              ("Master (front)", "stereo meter of 2 × 12 LEDs at the left, MASTER knob, PFL light, PHONES LEVEL knob and the headphone jack at the right")]
    return "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in groups)
