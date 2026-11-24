# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master section top panel: a layout draft in the style of the channel strip panel.

Drawn by hardware/channel-card/scripts/panel_render.py on the same page (it imports this file, and uses knob()
for its own pots). Third draft (the user, 2026-11-24): no columns, three strips wide (104.8 x 360 mm; decision 162
says four), the functions as bands across the panel, rear to front: compressor, sidechain, AUX, master; the AUX
band between the same two lines as the channel strips' AUX section; the headphone jack as far forward as it can
go; a master fader (the schematic still has the rotary pot RV701, decision 92); a printed scale at every pot.
Positions are x across the panel and d from the card's front edge as on the channel card (panel front end =
d - 21). Only the panel is drafted: nothing here is checked against the master PCB.

Scales: evenly spaced ticks over the pot's 300 degrees (eleven, or nine where a value sits on a quarter), with the
values the decisions give. Where only the end values
are known (the taper sets the rest) only the ends carry a number.
"""
import math

PW, PL = 104.8, 360.0
OFF_D = 21.0
LED = {"red": "#e0483f", "yellow": "#e6bd3a", "green": "#46b46a", "white": "#ecebe6"}
CAP = 8.0         # visible button cap, square (the user, 2026-11-24: smaller than 10 mm, room between neighbours)
JACK_D = 92.0     # headphone jack: decision 162 keeps it about 90 mm behind the front edge (its depth under the panel)
ENDS = lambda a, b: [(0.0, a), (1.0, b)]
# scale marks: (fraction of the rotation, text); sources in the comments
SCALES = {
    "SEND 1": ENDS("−∞", "0"), "SEND 2": ENDS("−∞", "0"),            # decision 51: off to 0 dB
    # decisions 88, 144: the fader law on a linear pot: 0 dB at three quarters, +10 dB at the top
    "RETURN 1": [(0.0, "−∞"), (0.75, "0"), (1.0, "+10")],
    "RETURN 2": [(0.0, "−∞"), (0.75, "0"), (1.0, "+10")],
    "AMOUNT": ENDS("0", "30"),                      # decision 89: lowers the threshold by up to 30 dB
    "RELEASE": ENDS("44ms", "1.4s"),                # decision 89, per 10 dB
    "MIX": ENDS("DRY", "WET"),                      # decision 89
    "SC LPF": ENDS("45", "480"),                    # decision 90: about 44 to 478 Hz
    "THRESHOLD": ENDS("LO", "HI"),                  # decision 90: 0.1 to 5 V peak
    "DECAY": ENDS("48ms", "1.2s"),                  # decision 90
    "DEPTH": [(0.0, "0"), (0.25, "10"), (0.5, "20"), (0.75, "30"), (1.0, "40")],   # decision 97: linear, 0 to 40 dB
    "PHONES LEVEL": ENDS("0", "10"),
}


def knob(x, y, dia, name, marks, dy=None):
    """A knob with its scale and, below both, its legend (SVG, mm units)."""
    r = dia / 2
    o = [f'<circle cx="{x}" cy="{y}" r="{r}" class="knob"/><path d="M{x} {y - r + 0.7}v{r * 0.5}" class="pointer"/>']
    # evenly spaced ticks: ten steps, or eight when a named mark sits on a quarter (0 dB at 75 %, DEPTH's quarters)
    n = 10 if all(abs(f * 10 - round(f * 10)) < 1e-6 for f, _ in marks) else 8
    fractions = [k / n for k in range(n + 1)]
    for f in fractions:
        t = math.radians(-150 + 300 * f); s, c = math.sin(t), math.cos(t)
        o.append(f'<path d="M{x + (r + 0.7) * s:.2f} {y - (r + 0.7) * c:.2f}L{x + (r + 1.7) * s:.2f} {y - (r + 1.7) * c:.2f}" class="tick"/>')
    for f, text in marks:
        t = math.radians(-150 + 300 * f); s, c = math.sin(t), math.cos(t)
        anchor = "middle" if abs(s) < 0.3 else ("end" if s < 0 else "start")
        o.append(f'<text x="{x + (r + 2.6) * s:.2f}" y="{y - (r + 2.9) * c + 0.65:.2f}" class="sc" text-anchor="{anchor}">{text}</text>')
    o.append(f'<text x="{x}" y="{y + (dy if dy is not None else r + 6.2)}" class="leg" text-anchor="middle">{name}</text>')
    return "".join(o)


# (legend, x, d, kind, knob diameter or LED colour); AUX rows are set by the caller
def controls(aux_hi, aux_lo):
    return [
        # compressor
        ("COMP ON", 14, 280, "button", "green"), ("AMOUNT", 36, 280, "pot", 16), ("RELEASE", 58, 280, "pot", 16),
        ("MIX", 80, 280, "pot", 16),
        # sidechain: source and filter, then the envelope
        ("SC BUS", 16, 238, "button", "green"), ("LISTEN", 30, 238, "button", "yellow"),
        ("SC LPF", 56, 238, "pot", 14), ("BYPASS", 72, 238, "button", "white"),
        ("THRESHOLD", 20, 210, "pot", 16), ("DECAY", 52, 210, "pot", 16), ("DEPTH", 84, 210, "pot", 16),
        # AUX 1 and AUX 2, one row each, in the channel strips' AUX band
        ("SEND 1", 16, aux_hi, "pot", 16), ("RETURN 1", 42, aux_hi, "pot", 16),
        ("MUTE", 66, aux_hi, "button", "red"), ("DUCK", 77, aux_hi, "button", "green"), ("COMP", 88, aux_hi, "button", "green"),
        ("SEND 2", 16, aux_lo, "pot", 16), ("RETURN 2", 42, aux_lo, "pot", 16),
        ("MUTE", 66, aux_lo, "button", "red"), ("DUCK", 77, aux_lo, "button", "green"), ("COMP", 88, aux_lo, "button", "green"),
        # master
        ("PFL", 76, 120, "led", "yellow"), ("PHONES LEVEL", 90, 118, "pot", 16), ("PHONES", 90, JACK_D, "jack63", None),
    ]


LABEL_DY = {"SC LPF": 13.2, "BYPASS": 13.2}
TOP_TITLE = "COMPRESSOR"
SC_LINE = 254.0
GR = ["1", "3", "6", "10", "15"]     # gain-reduction LEDs top to bottom, yellow (decision 170)
GR_X, GR_TOP = 97.0, 292.0
METER = [("CLIP", "red"), ("+12", "red"), ("+9", "yellow"), ("+6", "yellow"), ("+3", "yellow"), ("0", "green"),
         ("−3", "green"), ("−6", "green"), ("−10", "green"), ("−15", "green"), ("−20", "green"),
         ("−30", "green")]
METER_X, METER_TOP = (12.0, 19.0), 90.0      # L and R columns; CLIP; 12 LEDs at 6.0 mm pitch, beside the fader
FADER_X, FADER_D = 56.0, 57.0                # master fader: 60 mm travel, level with the channel faders
FADER = [("+10", 100), ("+5", 87.5), ("0", 75), ("−5", 64), ("−10", 53), ("−20", 42), ("−30", 30.5),
         ("−40", 19), ("−60", 14), ("−∞", 0)]     # the channel fader's marks (same law, decision 144)


def svg(x0, aux_band, title="master section, third draft"):
    """The master panel as SVG, its left edge at x0; aux_band = (rear line, front line) of the channels' AUX section."""
    Y = lambda d: PL - (d + OFF_D) + 8
    hi_line, lo_line = aux_band
    aux_lo = lo_line + 16.2; aux_hi = hi_line - 11.6        # legend above the front line, scale below the rear line
    lines = [(SC_LINE, "SIDECHAIN"), (hi_line, "AUX"), (lo_line, "MASTER")]
    o = [f'<g><text x="{x0 + PW / 2}" y="4.5" class="cap" text-anchor="middle">{title}</text>',
         f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>']
    for y in (8, 8 + PL - 20):
        o.append(f'<rect x="{x0}" y="{y}" width="{PW}" height="20" class="rail"/>')
        for sx in (17.4, PW - 17.4):
            cy = y + 10
            o.append(f'<circle cx="{x0 + sx}" cy="{cy}" r="2.6" class="screw"/><path d="M{x0 + sx - 1.4} {cy}h2.8M{x0 + sx} {cy - 1.4}v2.8" class="slot"/>')
    o.append(f'<text x="{x0 + PW - 3}" y="{Y(316)}" class="sm" text-anchor="end">{TOP_TITLE}</text>')
    for d, name in lines:
        o.append(f'<path d="M{x0 + 2} {Y(d)}h{PW - 4}" class="sect"/>')
        o.append(f'<text x="{x0 + PW - 3}" y="{Y(d) + 3.6}" class="sm" text-anchor="end">{name}</text>')
    for name, cx, d, kind, arg in controls(aux_hi, aux_lo):
        x, y = x0 + cx, Y(d)
        if kind == "pot":
            o.append(knob(x, y, arg, name, SCALES[name], LABEL_DY.get(name)))
        elif kind == "button":
            o.append(f'<rect x="{x - CAP / 2}" y="{y - CAP / 2}" width="{CAP}" height="{CAP}" rx="1.4" fill="{LED[arg]}" class="capbtn"/>')
            o.append(f'<text x="{x}" y="{y + LABEL_DY.get(name, CAP / 2 + 3.5)}" class="leg" text-anchor="middle">{name}</text>')
        elif kind == "jack63":
            o.append(f'<circle cx="{x}" cy="{y}" r="6.5" class="nut"/><circle cx="{x}" cy="{y}" r="3.2" class="hole"/>')
            o.append(f'<text x="{x}" y="{y + 10}" class="leg" text-anchor="middle">{name}</text>')
        else:   # a single indicator window, its legend at the left
            o.append(f'<rect x="{x - 2.5}" y="{y - 2.75}" width="5" height="5.5" rx="0.6" class="bezel"/>'
                     f'<rect x="{x - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[arg]}" opacity="0.92"/>')
            o.append(f'<text x="{x}" y="{y + 6.2}" class="leg" text-anchor="middle">{name}</text>')
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
    # master fader, drawn at 0 dB, marks at its left as on the channel strips
    fx = x0 + FADER_X
    o.append(f'<rect x="{fx - 2.25}" y="{Y(FADER_D) - 32.5}" width="4.5" height="65" rx="1" class="slotf"/>')
    for lab, pc in FADER:
        y = Y(FADER_D - 30 + 0.6 * pc)
        o.append(f'<path d="M{fx - 3.4} {y}h{-2.6 if lab == "0" else -1.6}" class="tick"/><text x="{fx - 6.8}" y="{y + 0.75}" class="sm" text-anchor="end">{lab}</text>')
    y0 = Y(FADER_D - 30 + 0.6 * 75)
    o.append(f'<rect x="{fx - 4.5}" y="{y0 - 7.5}" width="9" height="15" rx="1.2" class="fcap"/><path d="M{fx - 4.5} {y0}h9" class="fline"/>')
    o.append(f'<text x="{fx}" y="{Y(FADER_D) + 37.5}" class="leg" text-anchor="middle">MASTER</text>')
    o.append("</g>")
    return "\n".join(o)


def table():
    groups = [("Compressor (rear)", "COMP ON button, AMOUNT, RELEASE and MIX knobs, five gain-reduction LEDs (1, 3, 6, 10, 15 dB) at the right"),
              ("Sidechain", "SC BUS and LISTEN buttons, SC LPF knob with its BYPASS button; below them THRESHOLD, DECAY and DEPTH"),
              ("AUX", "one row per bus: SEND and RETURN knobs, then MUTE, DUCK and COMP buttons for the return; between the same lines as the channels' AUX section"),
              ("Master (front)", "stereo meter of 2 × 12 LEDs at the left, MASTER fader, PFL light, PHONES LEVEL knob and the headphone jack at the right")]
    return "\n".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in groups)
