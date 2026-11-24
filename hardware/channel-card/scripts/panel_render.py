# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Channel strip top panel: a drawing of the proposed control positions with their legends (build/panel.html).

Positions are distances from the card's front edge (d), as in floorplan.py; the panel is 34.8 x 360 mm, the card
(33 mm) centred under it and its front edge 21 mm behind the panel's front end (20 mm on the rail, 1 mm clearance).
Layout rules from the user (2026-11-24): fader 9 mm right of the centreline; a 25 mm strip for tape in front of the
fader; the controls pushed up to the rear rail with the freed depth as finger room; RESONANCE (small knob) beside
BYPASS, CUTOFF with a larger knob; AUX 1 and AUX 2 staggered 8 mm left and right; a line between sections;
every legend below its control (toward the operator), where the control does not hide it.
Usage: python3 panel_render.py
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "master", "scripts"))
import panel_draft as master     # the master section's draft, drawn on the same page
PW, PL = 34.8, 360.0          # panel
OFF_U, OFF_D = 0.9, 21.0      # card (u, d) -> panel (x, distance from the panel's front end)
CEN = 16.5
ROW = dict(MUTE=108, PFL=108, ROW3=127, AUX2=151, AUX1=173, RES=210, BYPASS=210, CUTOFF=237, JACKS=262,
           LOWCUT=282, TRIM=304)
LINES = [115.6, 134.3, 188.6, 269.6]     # between fader/PFL/MUTE, the bus buttons, the AUX sends, the filter, the input
FADER_D = 57.0                # travel centre; travel 60 mm
FADER_U = 25.5                # 9 mm right of the card's centreline (the user, 2026-11-24)
METER_U = 4.0
TAPE = (14.0, 39.0)           # tape strip, from the panel's front end: behind the screw head, in front of the fader
LABEL_DY = {"RESONANCE": 13.2, "BYPASS": 13.2}
# scale marks (fraction of the rotation, text): TRIM decision 26; CUTOFF decision 52, one octave per tick on a linear
# pot; AUX sends decision 74 (audio taper, so only the ends carry a value); RESONANCE has no unit
SCALES = {"TRIM": [(0.0, "\u221214"), (1.0, "+28")],
          "CUTOFF": [(0.0, "20"), (0.2, "80"), (0.4, "320"), (0.6, "1.2k"), (0.8, "5k"), (1.0, "20k")],
          "RESONANCE": [(0.0, "0"), (1.0, "10")],
          "AUX 1": [(0.0, "\u2212\u221e"), (1.0, "0")], "AUX 2": [(0.0, "\u2212\u221e"), (1.0, "0")]}   # one baseline for the two legends of a shared row
LED = {"red": "#e0483f", "yellow": "#e6bd3a", "green": "#46b46a", "white": "#ecebe6"}
# (name on the panel, row, u, kind, knob diameter or LED colour)
CONTROLS = [
    ("TRIM", "TRIM", CEN, "pot", 16), ("LOW CUT", "LOWCUT", CEN, "button", "white"),
    ("CV IN", "JACKS", CEN - 8, "jack", None), ("CV OUT", "JACKS", CEN + 8, "jack", None),
    ("CUTOFF", "CUTOFF", CEN, "pot", 20), ("RESONANCE", "RES", CEN - 8, "pot", 14),
    ("BYPASS", "BYPASS", CEN + 8, "button", "white"),
    ("AUX 1", "AUX1", CEN - 6.5, "pot", 16), ("AUX 2", "AUX2", CEN + 6.5, "pot", 16),   # staggered, 6.5 mm each side: room for the scale
    ("SC", "ROW3", 5.0, "button", "green"), ("DUCK", "ROW3", 16.5, "button", "green"),
    ("COMP", "ROW3", 28.0, "button", "green"),   # 11.5 mm apart, the widest the card allows
    ("PFL", "PFL", CEN - 7, "button", "yellow"), ("MUTE", "MUTE", CEN + 7, "button", "red"),
]
METER = [("CLIP", "red"), ("+6", "yellow"), ("+3", "yellow"), ("0", "green"), ("−5", "green"),
         ("−10", "green"), ("−20", "green"), ("−30", "green")]
# fader marks: (label, % of travel), decision 72's law (0 dB at 75 %); +5, -5 and -30 interpolated on its segments
FADER = [("+10", 100), ("+5", 87.5), ("0", 75), ("−5", 64), ("−10", 53), ("−20", 42), ("−30", 30.5),
         ("−40", 19), ("−60", 14), ("−∞", 0)]


def strip(x0, title):
    """One panel strip as SVG, its left edge at x0; the front is at the bottom of the drawing."""
    X = lambda u: x0 + u + OFF_U
    Y = lambda d: PL - (d + OFF_D) + 8
    o = [f'<g><text x="{x0 + PW / 2}" y="4.5" class="cap" text-anchor="middle">{title}</text>',
         f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>']
    for y in (8, 8 + PL - 20):      # the 20 mm resting on each rail
        o.append(f'<rect x="{x0}" y="{y}" width="{PW}" height="20" class="rail"/>')
    for y in (8 + 10, 8 + PL - 10):
        o.append(f'<circle cx="{x0 + PW / 2}" cy="{y}" r="2.6" class="screw"/><path d="M{x0 + PW / 2 - 1.4} {y}h2.8M{x0 + PW / 2} {y - 1.4}v2.8" class="slot"/>')
    for d in LINES:
        o.append(f'<path d="M{x0 + 2} {Y(d)}h{PW - 4}" class="sect"/>')
    ty = 8 + PL - TAPE[1]
    o.append(f'<rect x="{x0 + 2}" y="{ty}" width="{PW - 4}" height="{TAPE[1] - TAPE[0]}" rx="0.8" class="tape"/>'
             f'<text x="{x0 + PW / 2}" y="{ty + (TAPE[1] - TAPE[0]) / 2 + 1}" class="tapet" text-anchor="middle">tape</text>')
    for name, row, u, kind, arg in CONTROLS:
        x, y = X(u), Y(ROW[row])
        if kind == "pot":
            o.append(master.knob(x, y, arg, name, SCALES[name], LABEL_DY.get(name)))
        elif kind == "button":
            c = master.CAP
            o.append(f'<rect x="{x - c / 2}" y="{y - c / 2}" width="{c}" height="{c}" rx="1.4" fill="{LED[arg]}" class="capbtn"/>')
            o.append(f'<text x="{x}" y="{y + LABEL_DY.get(name, c / 2 + 3.5)}" class="leg" text-anchor="middle">{name}</text>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="4" class="nut"/><circle cx="{x}" cy="{y}" r="1.8" class="hole"/>')
            o.append(f'<text x="{x}" y="{y + 7.5}" class="leg" text-anchor="middle">{name}</text>')
    # meter: bezel 5 x 49 mm, 8 windows at 6.0 mm pitch, CLIP level with the fader's top travel end
    top = FADER_D + 30
    mx = X(METER_U)
    o.append(f'<rect x="{mx - 2.5}" y="{Y(top) - 3.5}" width="5" height="49" rx="0.6" class="bezel"/>')
    for i, (lab, col) in enumerate(METER):
        y = Y(top - 6 * i)
        o.append(f'<rect x="{mx - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[col]}" opacity="0.92"/>')
        o.append(f'<text x="{mx + 3.4}" y="{y + 0.75}" class="sm">{lab}</text>')
    # fader: slot 4.5 x 65 mm, cap drawn at 0 dB, marks at its left
    fx = X(FADER_U)
    o.append(f'<rect x="{fx - 2.25}" y="{Y(FADER_D) - 32.5}" width="4.5" height="65" rx="1" class="slotf"/>')
    for lab, pc in FADER:
        y = Y(FADER_D - 30 + 0.6 * pc)
        o.append(f'<path d="M{fx - 3.4} {y}h{-2.6 if lab == "0" else -1.6}" class="tick"/><text x="{fx - 6.8}" y="{y + 0.75}" class="sm" text-anchor="end">{lab}</text>')
    y0 = Y(FADER_D - 30 + 0.6 * 75)
    o.append(f'<rect x="{fx - 4.5}" y="{y0 - 7.5}" width="9" height="15" rx="1.2" class="fcap"/><path d="M{fx - 4.5} {y0}h9" class="fline"/>')
    o.append("</g>")
    return "\n".join(o)


def power_strip(x0, title="power"):
    """The power bay's plain top strip (MECHANICAL.md, power bay): the power LED and the two bracket screws."""
    Y = lambda d: PL - (d + OFF_D) + 8
    cx = x0 + PW / 2
    o = [f'<g><text x="{cx}" y="4.5" class="cap" text-anchor="middle">{title}</text>',
         f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>']
    for y in (8, 8 + PL - 20):
        o.append(f'<rect x="{x0}" y="{y}" width="{PW}" height="20" class="rail"/>')
    # distances in MECHANICAL.md are from the front rail's inner face: d = that - 1
    for d in (-11, 143, 308, 329):      # rail screws at the ends, bracket screws H2 and H1 (decision 188)
        y = Y(d)
        o.append(f'<circle cx="{cx}" cy="{y}" r="2.6" class="screw"/><path d="M{cx - 1.4} {y}h2.8M{cx} {y - 1.4}v2.8" class="slot"/>')
    y = Y(289)                           # power LED: 3 mm LED in a clip, ring 6.1 mm (decision 168)
    o.append(f'<circle cx="{cx}" cy="{y}" r="3.05" class="nut"/><circle cx="{cx}" cy="{y}" r="1.5" fill="{LED["green"]}"/>')
    o.append(f'<text x="{cx}" y="{y + 7.2}" class="leg" text-anchor="middle">POWER</text>')
    o.append("</g>")
    return "\n".join(o)


# ---- underside view: what hangs below the cards, seen from above through the panels (same left and right) ----------
PWR_HDR = (131.1, 150.1, 0.0, 10.0)      # channel power header body (d0, d1, u0, u1), from floorplan.py
AUD_HDR = (154.0, 206.0, 23.0, 33.0)     # channel audio header body
IN_HDR = (290.0, 314.0, 0.0, 10.0)       # input header J1
BAND = (116.1, 221.0)                    # no hand-set parts: the cables run here (decision 175)
REGS = [(62.0, 79.0, 3.0, 14.4), (62.0, 79.0, 18.6, 30.0)]    # regulators underneath, proposed
M_AUD = (154.0, 206.0, 0.0, 10.0)        # master audio header at its left edge, on the channels' audio row
M_PWR = (154.0, 173.0, 93.0, 103.0)      # master power header, proposed: opposite the power board's master header
M_HS_ZONE = (189.0, 318.0, 20.0, 93.0)   # heatsinks: 190 mm or more behind the front rail, 10 mm inside the right edge
M_HS = [(213.0, 225.7, 28.0, 62.9), (247.0, 259.7, 28.0, 62.9)]     # two 34.9 x 12.7 mm heatsinks between the pot rows, position not set
PB_D = (137.0, 314.0)                    # power board on edge, 138 to 315 mm behind the front rail's inner face
PB_HDR = {"chain": 144.2, "master": 163.5}    # its ribbon headers (centres, d), from hardware/power/scripts/placement.py


def underside():
    Y = lambda d: PL - (d + OFF_D) + 8
    o = []

    def box(x0, b, cls, extra=""):
        o.append(f'<rect x="{x0 + OFF_U + b[2]:.2f}" y="{Y(b[1]):.2f}" width="{b[3] - b[2]:.2f}" height="{b[1] - b[0]:.2f}" class="{cls}" {extra}/>')

    def text(x, d, t, anchor="start", cls="ut"):
        o.append(f'<text x="{x:.2f}" y="{Y(d) + 0.8:.2f}" class="{cls}" text-anchor="{anchor}">{t}</text>')

    xm = 22 + 140; xp = xm + master.PW + 0.2
    xb = xp + PW - 6 - 1.6                    # power board's parts face
    for k in range(4):                        # panels as a dark ground, the cards on them
        x0 = 22 + 35 * k
        o.append(f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>')
        box(x0, (0, 318, 0, 33), "card")
    o.append(f'<rect x="{xm}" y="8" width="{master.PW}" height="{PL}" class="panel"/>')
    box(xm, (0, 318, 0, master.PW - 1.8), "card")
    o.append(f'<rect x="{xp}" y="8" width="{PW}" height="{PL}" class="panel"/>')
    o.append(f'<text x="{22 + 70}" y="4.5" class="cap" text-anchor="middle">channel cards 1 to 4</text><text x="{xm + master.PW / 2}" y="4.5" class="cap" text-anchor="middle">master card</text><text x="{xp + PW / 2}" y="4.5" class="cap" text-anchor="middle">power bay</text>')
    # control positions as faint dots, to see what sits above each header
    for k in range(4):
        x0 = 22 + 35 * k
        for name, row, u, kind, arg in CONTROLS:
            o.append(f'<circle cx="{x0 + OFF_U + u}" cy="{Y(ROW[row])}" r="1.6" class="ghost"/>')
        box(x0, (FADER_D - 38, FADER_D + 38, FADER_U - 5, FADER_U + 5), "ghostbox")
    for name, cx, d, kind, arg in master.controls(LINES[2] - 11.6, LINES[1] + 16.2):
        o.append(f'<circle cx="{xm + cx}" cy="{Y(d)}" r="1.6" class="ghost"/>')
    o.append(f'<rect x="{xm + master.FADER_X - 5}" y="{Y(master.FADER_D + 38)}" width="10" height="76" class="ghostbox"/>')
    # cables first, the headers on top of them
    y_p, y_a = Y(140.6), Y(180.0)
    o.append(f'<path d="M{22 + OFF_U + 5} {y_p}H{xm + master.PW - 8}L{xb - 9} {Y(PB_HDR["chain"])}" class="cabp"/>')
    o.append(f'<path d="M{22 + OFF_U + 28} {y_a}H{xm + OFF_U + 5}" class="caba"/>')
    o.append(f'<path d="M{xm + OFF_U + 98} {Y(163.5)}H{xb - 9}" class="cabp"/>')
    for k in range(4):
        x0 = 22 + 35 * k
        box(x0, (0, 41, 0.6, 32.4), "zone")
        box(x0, (BAND[0], BAND[1], 0.6, 32.4), "zone")
        for b in (PWR_HDR, AUD_HDR, IN_HDR):
            box(x0, b, "hdr")
        for b in REGS:
            box(x0, b, "reg")
    x1 = 22 + OFF_U
    text(x1 + 16.5, 20, "nothing below", "middle"); text(x1 + 16.5, 16.8, "the front 41 mm", "middle")
    text(x1 + 16.5, 83, "regulators", "middle"); text(x1 + 16.5, 58, "(proposed)", "middle")
    text(x1 + 11, 128, "power"); text(x1 + 11, 124.8, "header")
    text(x1 + 22, 210, "audio", "end"); text(x1 + 22, 206.8, "header", "end")
    text(x1 + 16.5, 255, "trimmers and", "middle"); text(x1 + 16.5, 251.8, "jumpers here", "middle")
    text(x1 + 11, 303, "input"); text(x1 + 11, 299.8, "header")
    # master card
    box(xm, M_HS_ZONE, "zone")
    for b in M_HS:
        box(xm, b, "hs")
    box(xm, M_AUD, "hdr"); box(xm, M_PWR, "hdr")
    o.append(f'<circle cx="{xm + 90}" cy="{Y(master.JACK_D)}" r="7" class="hs"/>')
    xmc = xm + OFF_U
    text(xmc + 56.5, 312, "heatsink zone: 190 mm or more behind the front rail", "middle")
    text(xmc + 45.5, 263, "two heatsinks, position not set", "middle")
    text(xmc + 11.5, 210, "audio header"); text(xmc + 91.5, 177, "power header", "end"); text(xmc + 91.5, 173.8, "(proposed)", "end")
    text(xm + 90, 81, "headphone jack body", "middle")
    text(xmc + 50, 146, "chain 1 power feed crosses in front of the heatsink zone", "middle")
    # power bay: the board on edge, its parts toward the master
    o.append(f'<rect x="{xb - 17}" y="{Y(PB_D[1])}" width="17" height="{PB_D[1] - PB_D[0]}" class="zone"/>')
    o.append(f'<rect x="{xb}" y="{Y(PB_D[1])}" width="1.6" height="{PB_D[1] - PB_D[0]}" class="card"/>')
    for d in PB_HDR.values():
        o.append(f'<rect x="{xb - 9}" y="{Y(d + 9.5)}" width="9" height="19" class="hdr"/>')
    text(xb - 8.5, 240, "power board on edge,", "middle"); text(xb - 8.5, 236.8, "parts this side", "middle")
    return "\n".join(o)


def dims(x):
    """Distance of each row from the panel's front end, as a ruler left of the first strip."""
    o = []
    rows = [("fader, bottom of travel", FADER_D - 30), ("fader, top of travel", FADER_D + 30)] + \
           [(k, v) for k, v in ROW.items() if k not in ("PFL", "BYPASS")]
    for name, d in rows:
        y = PL - (d + OFF_D) + 8
        o.append(f'<path d="M{x - 1} {y}h-5" class="dim"/><text x="{x - 7}" y="{y + 1.1}" class="dimt" text-anchor="end">{d + OFF_D:.0f}</text>')
    o.append(f'<text x="{x - 7}" y="4.5" class="cap" text-anchor="end">mm</text>')
    return "\n".join(o)


def table():
    rows = [("TRIM", "TRIM", "pot, 16 mm knob", "centreline"), ("LOW CUT", "LOWCUT", "button, white", "centreline"),
            ("CV IN / CV OUT", "JACKS", "3.5 mm jacks", "8 mm left and right"),
            ("CUTOFF", "CUTOFF", "pot, 20 mm knob", "centreline"),
            ("RESONANCE / BYPASS", "RES", "pot with a 14 mm knob; button, white", "8 mm left; 8 mm right"),
            ("AUX 1", "AUX1", "pot, 16 mm knob", "6.5 mm left"), ("AUX 2", "AUX2", "pot, 16 mm knob", "6.5 mm right"),
            ("SC / DUCK / COMP", "ROW3", "three buttons, green", "11.5 mm apart"),
            ("PFL / MUTE", "MUTE", "two buttons, yellow and red", "7 mm left and right")]
    out = []
    for i, (name, row, what, across) in enumerate(rows):
        nxt = ROW[rows[i + 1][1]] if i + 1 < len(rows) else FADER_D + 30
        out.append(f"<tr><td>{name}</td><td>{what}</td><td>{across}</td><td class='n'>{ROW[row]:.0f}</td><td class='n'>{ROW[row] + OFF_D:.0f}</td><td class='n'>{ROW[row] - nxt:.0f}</td></tr>")
    out.append(f"<tr><td>Fader and meter</td><td>60 mm travel; 8 LEDs at 6.0 mm</td><td>fader 9 mm right, meter 12.5 mm left</td><td class='n'>{FADER_D - 30:.0f}–{FADER_D + 30:.0f}</td><td class='n'>{FADER_D - 30 + OFF_D:.0f}–{FADER_D + 30 + OFF_D:.0f}</td><td class='n'></td></tr>")
    out.append(f"<tr><td>Tape strip</td><td>blank panel, 25 mm</td><td>full width</td><td class='n'></td><td class='n'>{TAPE[0]:.0f}–{TAPE[1]:.0f}</td><td class='n'></td></tr>")
    return "\n".join(out)


PAGE = """<title>Mixer Top Panels</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600&display=swap">
<style>
/* layout: one column; the drawing first at full height, the numbers behind it in a table */
:root { --bg: #f3f4f2; --surface: #ffffff; --fg: #1b1f1d; --muted: #5d6662; --line: #d5dad6; --accent: #1f7a5a;
  --display: "Space Grotesk", "Helvetica Neue", Arial, sans-serif; --body: Inter, "Helvetica Neue", Arial, sans-serif; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #141716; --surface: #1c201e; --fg: #e9ece9; --muted: #9aa5a0; --line: #303733; --accent: #58c79b; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #141716; --surface: #1c201e; --fg: #e9ece9; --muted: #9aa5a0; --line: #303733; --accent: #58c79b; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font-family: var(--body); font-size: 15px; line-height: 1.55;
  padding-block: 28px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
main { max-width: 1120px; margin: 0 auto; display: flex; flex-direction: column; gap: 22px; }
h1 { font-family: var(--display); font-size: 1.9rem; line-height: 1.15; margin: 0; text-wrap: balance; }
h2 { font-family: var(--display); font-size: 1.15rem; margin: 0 0 8px; }
p { margin: 0; max-width: 65ch; }
.lede { color: var(--muted); }
.fig { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 14px; overflow-x: auto; }
.fig svg { display: block; width: 100%; min-width: 860px; height: auto; margin: 0 auto; }
ul { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: 6px; max-width: 68ch; }
.tw { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums; }
th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: 0.78rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); font-weight: 600; }
td.n, th.n { text-align: right; white-space: nowrap; }
.note { color: var(--muted); font-size: 0.9rem; }
/* drawing (mm units); the panel is black FR4 with white legends in both themes */
.panel { fill: #131313; stroke: #000; stroke-width: 0.3; }
.rail { fill: #ffffff; opacity: 0.07; }
.screw { fill: #8d8d8d; } .slot { stroke: #333; stroke-width: 0.5; fill: none; }
.knob { fill: #2c2c2c; stroke: #6a6a6a; stroke-width: 0.35; }
.pointer { stroke: #f2f2f2; stroke-width: 0.9; stroke-linecap: round; fill: none; }
.capbtn { stroke: #000; stroke-width: 0.3; opacity: 0.92; }
.nut { fill: #b9b9b9; stroke: #777; stroke-width: 0.3; } .hole { fill: #050505; }
.bezel { fill: #050505; stroke: #4a4a4a; stroke-width: 0.25; }
.slotf { fill: #000; stroke: #4a4a4a; stroke-width: 0.25; }
.fcap { fill: #cfcfcf; stroke: #6d6d6d; stroke-width: 0.3; } .fline { stroke: #222; stroke-width: 0.5; }
.tick { stroke: #f2f2f2; stroke-width: 0.3; fill: none; }
.sect { stroke: #f2f2f2; stroke-width: 0.3; fill: none; }
.tape { fill: #e9e2c8; opacity: 0.16; stroke: #e9e2c8; stroke-width: 0.25; stroke-dasharray: 1.2 1; }
.tapet { fill: #cfc9b2; font: 500 2.6px var(--body); letter-spacing: 0.3px; }
.sc { fill: #f4f4f4; font: 500 1.9px var(--body); }
.card { fill: #1d3a2b; stroke: #37694f; stroke-width: 0.3; }
.ghost { fill: none; stroke: #7d8c84; stroke-width: 0.25; } .ghostbox { fill: none; stroke: #7d8c84; stroke-width: 0.25; }
.hdr { fill: #d8d8d2; stroke: #6d6d6d; stroke-width: 0.3; }
.reg { fill: #6a5d4d; stroke: #a3927b; stroke-width: 0.3; }
.hs { fill: #55595c; stroke: #a9aeb2; stroke-width: 0.3; }
.zone { fill: #ffffff; fill-opacity: 0.05; stroke: #e9e9e9; stroke-width: 0.25; stroke-dasharray: 1.4 1.1; }
.cabp { fill: none; stroke: #e0a13a; stroke-opacity: 0.6; stroke-width: 10.2; stroke-linejoin: round; }
.caba { fill: none; stroke: #7fb0e6; stroke-opacity: 0.45; stroke-width: 43.2; }
.ut { fill: #f4f4f4; font: 500 2.2px var(--body); }
.leg { fill: #f4f4f4; font: 600 2.5px var(--body); letter-spacing: 0.12px; }
.sm { fill: #f4f4f4; font: 500 2.1px var(--body); }
.cap { fill: var(--muted); font: 500 3.2px var(--body); }
.dim { stroke: var(--muted); stroke-width: 0.25; fill: none; } .dimt { fill: var(--muted); font: 400 3px var(--body); }
</style>
<main>
<header>
<h1>Mixer top panels</h1>
<p class="lede">The prototype's top: four channel strips (34.8 &times; 360 mm each), the master section (drawn 104.8 mm wide) and the power bay strip, front edge at the bottom. The channel strip follows your choices; the master section is a third draft.</p>
</header>
<div class="fig">
<svg viewBox="0 0 304 372" role="img" aria-label="Drawing of four channel strip panels, the master section panel and the power bay strip with every control labelled">
__SVG__
</svg>
</div>
<p class="note">Left ruler: distance from the panel's front end in mm. Lighter bands at both ends rest on the frame rails. The dashed field is where tape goes; it is not printed. White lines separate the sections. Button colours are the LED colours already chosen.</p>
<section>
<h2>Underneath</h2>
<p>The same six strips seen from above through the panels, so left and right match the drawing above. Rings mark where the controls sit on top.</p>
<div class="fig" style="margin-top:12px">
<svg viewBox="0 0 304 372" role="img" aria-label="Underside view: the chain headers on each card, the power and audio cables crossing under the cards, the master's heatsink zone and the power board">
__UNDER__
</svg>
</div>
<ul style="margin-top:12px">
<li><strong>Orange: power.</strong> One flat cable links the power headers at the left edge of every channel card and runs on under the master to the power board. A second short one feeds the master.</li>
<li><strong>Blue: audio.</strong> One wide flat cable links the audio headers at the right edge of every channel card and ends at the master's left edge. The last step, from channel 4 to the master, is only about 12 mm.</li>
<li><strong>The two cables run at different depths</strong> and do not cross. Trimmers and jumpers stay out of the dashed band they run in.</li>
<li><strong>Checked by the placement script:</strong> the three headers on the channel card, against the pins of the controls above them.</li>
<li><strong>Not checked, drawn as proposals:</strong> everything on the master card (its headers, the two heatsinks, the headphone jack's body), the regulators under the channel faders, and the exact height of the power board's headers, which I took from its layout script.</li>
</ul>
</section>
<section>
<h2>Channel strip positions</h2>
<div class="tw"><table>
<thead><tr><th>Control</th><th>Part</th><th>Across the strip</th><th class="n">From card front, mm</th><th class="n">From panel front, mm</th><th class="n">To the next one forward, mm</th></tr></thead>
<tbody>
__TABLE__
</tbody></table></div>
</section>
<section>
<h2>Master section, third draft</h2>
<div class="tw"><table>
<thead><tr><th>Band</th><th>Controls, left to right</th></tr></thead>
<tbody>
__MTABLE__
</tbody></table></div>
<ul style="margin-top:12px">
<li><strong>AUX lined up with the channels.</strong> The master's AUX band sits between the same two lines as the channel strips' AUX section.</li>
<li><strong>No columns.</strong> Each function is a band across the panel with a line and its name: compressor at the rear, then sidechain, AUX, and the master at the front.</li>
<li><strong>Three strips wide instead of four</strong> (104.8 mm against 139.8 mm). The four-strip width is a recorded decision, and the master board carries 768 parts, about twice a channel card, so the narrower width needs a fit trial before it can be promised.</li>
<li><strong>Headphone jack as far forward as it can go:</strong> 92 mm behind the card's front edge. Closer to the front the jack's body does not fit under the panel, by the recorded estimate of about 90 mm; a sample still has to be measured.</li>
<li><strong>MASTER is a fader,</strong> your choice: 60 mm travel, level with the channel faders, the meter beside it. The schematic still has a rotary pot there, so the circuit sheet has to follow.</li>
<li><strong>Button colours are assumed</strong> from the channel strip; the master's LED colours are not checked.</li>
<li><strong>Only the panel is drafted.</strong> Nothing is checked against the master board yet.</li>
</ul>
</section>
<section>
<h2>Power bay</h2>
<ul>
<li><strong>A plain strip, one channel wide.</strong> The power board hangs under it; the only thing on the panel is the power light, about 290 mm behind the front rail, as recorded.</li>
<li><strong>Four screws on the centreline:</strong> one at each end into the rails and two for the brackets that carry the power board.</li>
<li><strong>The light's colour and the POWER legend are my assumptions.</strong> The power switch and the supply socket are on the rear panel, not here.</li>
</ul>
</section>
<section>
<h2>What the channel drawing assumes</h2>
<ul>
<li><strong>Tape strip.</strong> 25 mm of blank panel between the front screw and the fader; the fader cap at its lowest point stops 1.5 mm short of it.</li>
<li><strong>Sections,</strong> front to rear: fader with PFL and MUTE; SC, DUCK and COMP; the two AUX sends; the filter with its CV jacks; the input.</li>
<li><strong>Knob sizes.</strong> CUTOFF 20 mm, RESONANCE 14 mm, the others 16 mm. No knob is chosen yet, and the supplier's list for these shafts stops at about 19 mm, so the 20 mm one needs finding.</li>
<li><strong>AUX sends.</strong> 22 mm apart front to back and 13 mm across (6.5 mm each side, so the printed scales stay on the panel); the knob centres are 26 mm apart. AUX 2 cannot move further back: the audio header underneath needs the run between it and BYPASS.</li>
<li><strong>Scales.</strong> Eleven ticks around each pot. CUTOFF is marked in octaves from 20 Hz to 20 kHz, TRIM with its ends in dB, the sends from off to 0 dB. Where only the end values are known, only the ends carry a number; the marks in between depend on the pot's taper and would need measuring.</li>
<li><strong>Legends below the controls,</strong> on the operator's side, so a knob or cap does not hide its own name. MUTE's legend stays 4.7 mm clear of the fader cap at the top of its travel.</li>
<li><strong>Button caps 8 mm square</strong> instead of 10 mm, so a finger on one does not press its neighbour: 3.5 mm between the caps in the row of three (they are 11.5 mm apart, the widest the card allows), 6 mm between PFL and MUTE. The switch body under the panel is 8.5 mm, and each cap is lit by an LED beside the switch, so the printed cap needs a wider skirt under the panel to catch the light: to try on a print.</li>
<li><strong>Legend wording.</strong> SC, DUCK and COMP are short forms of SC SEND, DUCK and COMP BUS; BYPASS stands for FILTER BYPASS.</li>
</ul>
</section>
</main>
"""

if __name__ == "__main__":
    svg = dims(22) + "".join(strip(22 + 35 * k, f"channel {k + 1}") for k in range(4))
    svg += master.svg(22 + 140, (LINES[2], LINES[1]), "master section") + power_strip(22 + 140 + master.PW + 0.2)
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    out = os.path.join(HERE, "build", "panel.html")
    open(out, "w").write(PAGE.replace("__SVG__", svg).replace("__TABLE__", table()).replace("__MTABLE__", master.table()).replace("__UNDER__", underside()))
    print(out)
