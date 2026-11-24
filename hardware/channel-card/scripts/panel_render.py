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
    ("SC", "ROW3", 5.5, "button", "green"), ("DUCK", "ROW3", 16.5, "button", "green"),
    ("COMP", "ROW3", 27.5, "button", "green"),
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
            o.append(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" rx="1.6" fill="{LED[arg]}" class="capbtn"/>')
            o.append(f'<text x="{x}" y="{y + LABEL_DY.get(name, 8.5)}" class="leg" text-anchor="middle">{name}</text>')
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
            ("SC / DUCK / COMP", "ROW3", "three buttons, green", "11 mm apart"),
            ("PFL / MUTE", "MUTE", "two buttons, yellow and red", "7 mm left and right")]
    out = []
    for i, (name, row, what, across) in enumerate(rows):
        nxt = ROW[rows[i + 1][1]] if i + 1 < len(rows) else FADER_D + 30
        out.append(f"<tr><td>{name}</td><td>{what}</td><td>{across}</td><td class='n'>{ROW[row]:.0f}</td><td class='n'>{ROW[row] + OFF_D:.0f}</td><td class='n'>{ROW[row] - nxt:.0f}</td></tr>")
    out.append(f"<tr><td>Fader and meter</td><td>60 mm travel; 8 LEDs at 6.0 mm</td><td>fader 9 mm right, meter 12.5 mm left</td><td class='n'>{FADER_D - 30:.0f}–{FADER_D + 30:.0f}</td><td class='n'>{FADER_D - 30 + OFF_D:.0f}–{FADER_D + 30 + OFF_D:.0f}</td><td class='n'></td></tr>")
    out.append(f"<tr><td>Tape strip</td><td>blank panel, 25 mm</td><td>full width</td><td class='n'></td><td class='n'>{TAPE[0]:.0f}–{TAPE[1]:.0f}</td><td class='n'></td></tr>")
    return "\n".join(out)


PAGE = """<title>Channel Strip Panel</title>
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
main { max-width: 860px; margin: 0 auto; display: flex; flex-direction: column; gap: 22px; }
h1 { font-family: var(--display); font-size: 1.9rem; line-height: 1.15; margin: 0; text-wrap: balance; }
h2 { font-family: var(--display); font-size: 1.15rem; margin: 0 0 8px; }
p { margin: 0; max-width: 65ch; }
.lede { color: var(--muted); }
.fig { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 14px; overflow-x: auto; }
.fig svg { display: block; width: 100%; min-width: 620px; max-width: 900px; height: auto; margin: 0 auto; }
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
.leg { fill: #f4f4f4; font: 600 2.5px var(--body); letter-spacing: 0.12px; }
.sm { fill: #f4f4f4; font: 500 2.1px var(--body); }
.cap { fill: var(--muted); font: 500 3.2px var(--body); }
.dim { stroke: var(--muted); stroke-width: 0.25; fill: none; } .dimt { fill: var(--muted); font: 400 3px var(--body); }
</style>
<main>
<header>
<h1>Channel strip and master panels</h1>
<p class="lede">Two channel strips (34.8 &times; 360 mm each) beside the master section (drawn 104.8 mm wide), front edge at the bottom. The channel strip follows your choices; the master section is a third draft.</p>
</header>
<div class="fig">
<svg viewBox="0 0 200 372" role="img" aria-label="Drawing of two channel strip panels and the master section panel with every control labelled">
__SVG__
</svg>
</div>
<p class="note">Left ruler: distance from the panel's front end in mm. Lighter bands at both ends rest on the frame rails. The dashed field is where tape goes; it is not printed. White lines separate the sections. Button colours are the LED colours already chosen.</p>
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
<h2>What the channel drawing assumes</h2>
<ul>
<li><strong>Tape strip.</strong> 25 mm of blank panel between the front screw and the fader; the fader cap at its lowest point stops 1.5 mm short of it.</li>
<li><strong>Sections,</strong> front to rear: fader with PFL and MUTE; SC, DUCK and COMP; the two AUX sends; the filter with its CV jacks; the input.</li>
<li><strong>Knob sizes.</strong> CUTOFF 20 mm, RESONANCE 14 mm, the others 16 mm. No knob is chosen yet, and the supplier's list for these shafts stops at about 19 mm, so the 20 mm one needs finding.</li>
<li><strong>AUX sends.</strong> 22 mm apart front to back and 13 mm across (6.5 mm each side, so the printed scales stay on the panel); the knob centres are 26 mm apart. AUX 2 cannot move further back: the audio header underneath needs the run between it and BYPASS.</li>
<li><strong>Scales.</strong> Eleven ticks around each pot. CUTOFF is marked in octaves from 20 Hz to 20 kHz, TRIM with its ends in dB, the sends from off to 0 dB. Where only the end values are known, only the ends carry a number; the marks in between depend on the pot's taper and would need measuring.</li>
<li><strong>Legends below the controls,</strong> on the operator's side, so a knob or cap does not hide its own name. MUTE's legend stays 4.7 mm clear of the fader cap at the top of its travel.</li>
<li><strong>Legend wording.</strong> SC, DUCK and COMP are short forms of SC SEND, DUCK and COMP BUS; BYPASS stands for FILTER BYPASS.</li>
</ul>
</section>
</main>
"""

if __name__ == "__main__":
    svg = dims(22) + strip(22, "channel strip") + strip(22 + 35, "its neighbour") + master.svg(22 + 70, (LINES[2], LINES[1]))
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    out = os.path.join(HERE, "build", "panel.html")
    open(out, "w").write(PAGE.replace("__SVG__", svg).replace("__TABLE__", table()).replace("__MTABLE__", master.table()))
    print(out)
