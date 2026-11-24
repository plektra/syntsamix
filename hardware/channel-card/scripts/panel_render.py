# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Channel strip top panel: a drawing of the proposed control positions with their legends (build/panel.html).

Positions are distances from the card's front edge (d), as in floorplan.py; the panel is 34.8 x 360 mm, the card
(33 mm) centred under it and its front edge 21 mm behind the panel's front end (20 mm on the rail, 1 mm clearance).
The fader sits 9 mm right of the centreline (the user, 2026-11-24); two neighbouring strips are drawn.
Usage: python3 panel_render.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PW, PL = 34.8, 360.0          # panel
OFF_U, OFF_D = 0.9, 21.0      # card (u, d) -> panel (x, distance from the panel's front end)
CEN = 16.5
ROW = dict(MUTE=92, PFL=92, ROW3=106, AUX2=129, AUX1=141, BYPASS=160, RES=180, CUTOFF=205, JACKS=225,
           LOWCUT=241, TRIM=261)
FADER_D = 42.0                # travel centre; travel 60 mm
FADER_U = 25.5                # 9 mm right of the card's centreline (the user, 2026-11-24)
METER_U = 4.0
LED = {"red": "#e0483f", "yellow": "#e6bd3a", "green": "#46b46a", "white": "#ecebe6"}
# (name on the panel, row, u, kind, LED colour)
CONTROLS = [
    ("TRIM", "TRIM", CEN, "pot", None), ("LOW CUT", "LOWCUT", CEN, "button", "white"),
    ("CV IN", "JACKS", CEN - 8, "jack", None), ("CV OUT", "JACKS", CEN + 8, "jack", None),
    ("CUTOFF", "CUTOFF", CEN, "pot", None), ("RESONANCE", "RES", CEN, "pot", None),
    ("BYPASS", "BYPASS", CEN, "button", "white"),
    ("AUX 1", "AUX1", CEN - 8, "pot", None), ("AUX 2", "AUX2", CEN + 8, "pot", None),   # staggered, 8 mm each side
    ("SC", "ROW3", 5.5, "button", "green"), ("DUCK", "ROW3", 16.5, "button", "green"),
    ("COMP", "ROW3", 27.5, "button", "green"),
    ("PFL", "PFL", CEN - 7, "button", "yellow"), ("MUTE", "MUTE", CEN + 7, "button", "red"),   # one row, 14 mm apart
]
METER = [("CLIP", "red"), ("+6", "yellow"), ("+3", "yellow"), ("0", "green"), ("−5", "green"),
         ("−10", "green"), ("−20", "green"), ("−30", "green")]
# fader marks: (label, % of travel), decision 72's law (0 dB at 75 %); +5, -5 and -30 interpolated on its segments
FADER = [("+10", 100), ("+5", 87.5), ("0", 75), ("−5", 64), ("−10", 53), ("−20", 42), ("−30", 30.5),
         ("−40", 19), ("−60", 14), ("−∞", 0)]


def strip(x0, fader_u, title):
    """One panel strip as SVG, its left edge at x0; the front is at the bottom of the drawing."""
    X = lambda u: x0 + u + OFF_U
    Y = lambda d: PL - (d + OFF_D) + 8
    o = [f'<g><text x="{x0 + PW / 2}" y="4.5" class="cap" text-anchor="middle">{title}</text>',
         f'<rect x="{x0}" y="8" width="{PW}" height="{PL}" class="panel"/>']
    for y in (8, 8 + PL - 20):      # the 20 mm resting on each rail
        o.append(f'<rect x="{x0}" y="{y}" width="{PW}" height="20" class="rail"/>')
    for y in (8 + 10, 8 + PL - 10):
        o.append(f'<circle cx="{x0 + PW / 2}" cy="{y}" r="2.6" class="screw"/><path d="M{x0 + PW / 2 - 1.4} {y}h2.8M{x0 + PW / 2} {y - 1.4}v2.8" class="slot"/>')
    for name, row, u, kind, col in CONTROLS:
        x, y = X(u), Y(ROW[row])
        if kind in ("pot", "potleft"):
            o.append(f'<circle cx="{x}" cy="{y}" r="9.5" class="knobmax"/><circle cx="{x}" cy="{y}" r="8" class="knob"/>'
                     f'<path d="M{x} {y - 7.4}v4.2" class="pointer"/>')
            if kind == "pot":
                o.append(f'<text x="{x}" y="{y - 10.6}" class="leg" text-anchor="middle">{name}</text>')
            else:
                o.append(f'<text x="{x - 11}" y="{y + 0.9}" class="leg" text-anchor="end">{name}</text>')
        elif kind == "button":
            o.append(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" rx="1.6" fill="{LED[col]}" class="capbtn"/>')
            o.append(f'<text x="{x}" y="{y - 6.6}" class="leg" text-anchor="middle">{name}</text>')
        else:
            o.append(f'<circle cx="{x}" cy="{y}" r="4" class="nut"/><circle cx="{x}" cy="{y}" r="1.8" class="hole"/>')
            o.append(f'<text x="{x}" y="{y - 5.6}" class="leg" text-anchor="middle">{name}</text>')
    # meter: bezel 5 x 49 mm, 8 windows at 6.0 mm pitch, CLIP level with the fader's top travel end
    top = FADER_D + 30
    mx = X(METER_U)
    o.append(f'<rect x="{mx - 2.5}" y="{Y(top) - 3.5}" width="5" height="49" rx="0.6" class="bezel"/>')
    for i, (lab, col) in enumerate(METER):
        y = Y(top - 6 * i)
        o.append(f'<rect x="{mx - 2}" y="{y - 2.25}" width="4" height="4.5" rx="0.4" fill="{LED[col]}" opacity="0.92"/>')
        o.append(f'<text x="{mx + 3.4}" y="{y + 0.75}" class="sm">{lab}</text>')
    # fader: slot 4.5 x 65 mm, cap drawn at 0 dB
    fx = X(fader_u); right = fader_u <= CEN
    o.append(f'<rect x="{fx - 2.25}" y="{Y(FADER_D) - 32.5}" width="4.5" height="65" rx="1" class="slotf"/>')
    for lab, pc in FADER:
        y = Y(FADER_D - 30 + 0.6 * pc)
        if right:
            o.append(f'<path d="M{fx + 3.4} {y}h{2.6 if lab == "0" else 1.6}" class="tick"/><text x="{fx + 6.8}" y="{y + 0.75}" class="sm">{lab}</text>')
        else:
            o.append(f'<path d="M{fx - 3.4} {y}h{-2.6 if lab == "0" else -1.6}" class="tick"/><text x="{fx - 6.8}" y="{y + 0.75}" class="sm" text-anchor="end">{lab}</text>')
    y0 = Y(FADER_D - 30 + 0.6 * 75)
    o.append(f'<rect x="{fx - 4.5}" y="{y0 - 7.5}" width="9" height="15" rx="1.2" class="fcap"/><path d="M{fx - 4.5} {y0}h9" class="fline"/>')
    o.append("</g>")
    return "\n".join(o)


def dims(x):
    """Distance of each row from the panel's front end, as a ruler left of the first strip."""
    o = []
    rows = [("fader, bottom of travel", FADER_D - 30), ("fader, top of travel", FADER_D + 30)] + \
           [(k, v) for k, v in ROW.items() if k != "PFL"]
    for name, d in rows:
        y = PL - (d + OFF_D) + 8
        o.append(f'<path d="M{x - 1} {y}h-5" class="dim"/><text x="{x - 7}" y="{y + 1.1}" class="dimt" text-anchor="end">{d + OFF_D:.0f}</text>')
    o.append(f'<text x="{x - 7}" y="4.5" class="cap" text-anchor="end">mm</text>')
    return "\n".join(o)


def table():
    rows = [("TRIM", "TRIM", "pot"), ("LOW CUT", "LOWCUT", "button, white"), ("CV IN / CV OUT", "JACKS", "3.5 mm jacks, 16 mm apart"),
            ("CUTOFF", "CUTOFF", "pot"), ("RESONANCE", "RES", "pot"), ("BYPASS", "BYPASS", "button, white"),
            ("AUX 1", "AUX1", "pot, 8 mm left of the centreline"), ("AUX 2", "AUX2", "pot, 8 mm right of the centreline"),
            ("SC / DUCK / COMP", "ROW3", "three buttons, green, 11 mm apart"),
            ("PFL / MUTE", "MUTE", "two buttons, yellow and red, 14 mm apart")]
    out = []
    for i, (name, row, what) in enumerate(rows):
        nxt = ROW[rows[i + 1][1]] if i + 1 < len(rows) else FADER_D + 30
        gap = ROW[row] - nxt
        out.append(f"<tr><td>{name}</td><td>{what}</td><td class='n'>{ROW[row]:.0f}</td><td class='n'>{ROW[row] + OFF_D:.0f}</td><td class='n'>{gap:.0f}</td></tr>")
    out.append(f"<tr><td>Fader and meter</td><td>60 mm travel; 8 LEDs at 6.0 mm</td><td class='n'>{FADER_D - 30:.0f}–{FADER_D + 30:.0f}</td><td class='n'>{FADER_D - 30 + OFF_D:.0f}–{FADER_D + 30 + OFF_D:.0f}</td><td class='n'></td></tr>")
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
.fig svg { display: block; width: 100%; max-width: 380px; height: auto; margin: 0 auto; }
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
.knob { fill: #2c2c2c; stroke: #6a6a6a; stroke-width: 0.35; } .knobmax { fill: none; stroke: #5a5a5a; stroke-width: 0.25; stroke-dasharray: 1 1; }
.pointer { stroke: #f2f2f2; stroke-width: 0.9; stroke-linecap: round; fill: none; }
.capbtn { stroke: #000; stroke-width: 0.3; opacity: 0.92; }
.nut { fill: #b9b9b9; stroke: #777; stroke-width: 0.3; } .hole { fill: #050505; }
.bezel { fill: #050505; stroke: #4a4a4a; stroke-width: 0.25; }
.slotf { fill: #000; stroke: #4a4a4a; stroke-width: 0.25; }
.fcap { fill: #cfcfcf; stroke: #6d6d6d; stroke-width: 0.3; } .fline { stroke: #222; stroke-width: 0.5; }
.tick { stroke: #f2f2f2; stroke-width: 0.3; fill: none; }
.leg { fill: #f4f4f4; font: 600 2.5px var(--body); letter-spacing: 0.12px; }
.sm { fill: #f4f4f4; font: 500 2.1px var(--body); }
.cap { fill: var(--muted); font: 500 3.2px var(--body); }
.dim { stroke: var(--muted); stroke-width: 0.25; fill: none; } .dimt { fill: var(--muted); font: 400 3px var(--body); }
</style>
<main>
<header>
<h1>Channel strip panel</h1>
<p class="lede">Control positions for the 34.8 &times; 360 mm top panel, front edge at the bottom. The fader position is chosen; the row distances and legend wording are still proposals.</p>
</header>
<div class="fig">
<svg viewBox="0 0 96 372" role="img" aria-label="Drawing of two neighbouring channel strip panels with every control labelled">
__SVG__
</svg>
</div>
<p class="note">Left ruler: distance from the panel's front end in mm. Lighter bands at both ends rest on the frame rails. Solid circle: a 16 mm knob; dashed circle: the largest knob the pots take, 19 mm. Button colours are the LED colours already chosen. Legend wording and the fader scale are proposals.</p>
<section>
<h2>Positions</h2>
<div class="tw"><table>
<thead><tr><th>Control</th><th>Part</th><th class="n">From card front, mm</th><th class="n">From panel front, mm</th><th class="n">To the next one forward, mm</th></tr></thead>
<tbody>
__TABLE__
</tbody></table></div>
</section>
<section>
<h2>Decided and open</h2>
<ul>
<li><strong>Fader position: decided.</strong> 9 mm right of the centreline, the meter column 12.5 mm left of it.</li>
<li><strong>PFL and MUTE side by side</strong>, PFL left over the meter, MUTE right over the fader.</li>
<li><strong>AUX pots staggered.</strong> Side by side they would need more than the strip's width for two knobs, so AUX 1 sits 8 mm left of the centreline and AUX 2 8 mm right of it, 12 mm further forward, in the same columns as the CV jacks; the knob centres are 20 mm apart.</li>
<li><strong>Spacing.</strong> Knob to knob 20 to 25 mm, a knob and a button 16 to 20 mm. CUTOFF has the most room around it. About 58 mm of panel behind TRIM stays blank.</li>
<li><strong>Legend wording.</strong> SC, DUCK and COMP are short forms of SC SEND, DUCK and COMP BUS, so they fit the 11 mm pitch. BYPASS stands for FILTER BYPASS.</li>
<li><strong>Knob size.</strong> Not chosen yet; the drawing shows 16 mm with the 19 mm limit dashed.</li>
</ul>
</section>
</main>
"""

if __name__ == "__main__":
    svg = dims(22) + strip(22, FADER_U, "channel strip") + strip(22 + 35, FADER_U, "its neighbour")
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    out = os.path.join(HERE, "build", "panel.html")
    open(out, "w").write(PAGE.replace("__SVG__", svg).replace("__TABLE__", table()))
    print(out)
