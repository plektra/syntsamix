#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Build breadboard.html: schematic, breadboard layout and wiring tables.

Run breadboard_schematic.py and breadboard_layout.py first (they write the
SVGs this page embeds). The placement table comes from the same PARTS list
the layout check verifies, so the page and the drawing cannot drift apart.

Usage:  python3 simulation/filter/breadboard_page.py
"""

from html import escape
from pathlib import Path

import breadboard_layout as bl

HERE = Path(__file__).resolve().parent

NOTES = {
    "C5": "10 µF 100 V bipolar electrolytic from the order (ø8 mm); either way round. Test 11 swaps it for two 10 µF 25 V back to back, − to −",
    "R1": "Input attenuator, the card's 18 kΩ: +4 dBu becomes about ±19 mV at pin 1",
    "R2": "Attenuator shunt (hot drive)",
    "R3": "330 Ω gives about −4 dB; try 200 Ω for about −6 dB",
    "J1": "Wire link. Fitted = medium drive, removed = hot drive",
    "C9": "Optional (datasheet): steadier resonance over the sweep. R82 film, 5 mm pitch: sits diagonally",
    "R4": "Terminates the unused SIG IN−",
    "C1": "Ladder capacitor, datasheet Figure 1. R82 film 10 %, 5 mm pitch: sits diagonally",
    "C2": "Ladder capacitor, datasheet Figure 1. R82 film 10 %, 5 mm pitch: sits diagonally",
    "C3": "Ladder capacitor, datasheet Figure 1. R82 film 10 %, 5 mm pitch: sits diagonally",
    "C4": "Ladder capacitor, datasheet Figure 1 (NP0 ceramic)",
    "C10": "Decoupling across the rails, next to U1", "C11": "Decoupling across the rails, next to U1",
    "C12": "Decoupling across the rails, next to U2", "C13": "Decoupling across the rails, next to U2",
    "C14": "Supply entry, 10 µF 25 V electrolytic: + to the +15 V rail, − to GND",
    "C15": "Supply entry, 10 µF 25 V electrolytic: + to GND, − to the −15 V rail",
    "R7": "Resonance input filter (Figure 3; kit 510 Ω for 499 Ω)", "C8": "Resonance input filter (Figure 3), R82 film",
    "R6": "33 kΩ for test 2 (finds oscillation onset, up to about 450 µA), then 51 kΩ (limits to about 294 µA)",
    "R8": "Stands in for the temperature-compensating resistor",
    "R10": "Cutoff offset from RV4, the card's 470 kΩ: about ±32 mV at pin 15",
    "R9": "Summer output into the cutoff pin",
    "C6": "Output stage, datasheet Figure 1",
    "RV3": "Output gain: wiper and pin 1 end form the feedback. Start at about 9 kΩ (unity predicted near 8.8 kΩ), set in test 5",
    "C7": "Output coupling, 10 µF 100 V bipolar electrolytic",
    "R11": "With RV5: summer feedback, sets 1 V/octave for the CV input",
    "RV5": "Wiper and pin 1 end in series with R11; start at about 32 kΩ (1 V/oct needs about 192 kΩ in total)",
    "R12": "Scales the cutoff pot to about 10 octaves (the card's 300 kΩ)",
    "R13": "CV input, about 1 V/octave",
}
VALUES = {"R6": "33 kΩ → 51 kΩ", "C9": "3.3 nF", "J1": "wire link"}
KIND_NAME = {"res": "Resistor", "cap": "Capacitor", "trim": "Trimmer", "jumper": "Link", "wire": "Wire",
             "lead": "Flying lead"}
RAIL = {"P15": "+15 V rail", "N15": "−15 V rail", "GNDT": "GND rail, top", "GNDB": "GND rail, bottom"}


def hole(end):
    if end[0] == "T":
        return f"{end[1]}{'fghij'[end[2]]}"
    if end[0] == "B":
        return f"{end[1]}{'edcba'[end[2]]}"
    if end[0] == "R":
        return f"{RAIL[end[1]]}, col {end[2]}"
    return end[1]


def rows(kinds):
    out = []
    for ref, val, kind, *ends in bl.PARTS:
        if kind not in kinds:
            continue
        if kind == "lead" and ends[0][0] == "R":
            continue
        where = " → ".join(hole(e) for e in ends) if kind != "trim" else \
            f"pin 1 {hole(ends[0])}, wiper {hole(ends[1])}, pin 3 {hole(ends[2])}"
        value = VALUES.get(ref, val) or ""
        out.append((ref, value, where, NOTES.get(ref, "")))
    return out


def table(rws, cols, cls):
    head = "".join(f"<th>{c}</th>" for c in cols)
    body = []
    for r in rws:
        rid = f"chk-{escape(r[0])}"
        cells = "".join(f"<td>{escape(c)}</td>" for c in r)
        body.append(f'<tr><td class="tick"><input type="checkbox" id="{rid}" aria-label="{escape(r[0])} placed"></td>{cells}</tr>')
    return (f'<div class="tablewrap"><table class="{cls}"><thead><tr><th class="tick"><span class="sr">Done</span></th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')


schem = (HERE / "breadboard-schematic.svg").read_text()
layout = (HERE / "breadboard-layout.svg").read_text()

parts_rows = rows({"res", "cap", "trim", "jumper"})
wire_rows = [(r[0], r[2], r[3]) for r in rows({"wire"})]

OFFBOARD = [
    ("Jacks (6.3 mm mono, PCB pins)", "Solder short stranded leads to the tip and sleeve pins; leave the switch pin free. Use a TS cable from the interface (a TRS plug shorts its ring to sleeve, which is harmless)."),
    ("IN jack", "Tip → “IN” tag (2a); sleeve → GND rail."),
    ("OUT jack", "Tip → “OUT” tag (25a); sleeve → GND rail."),
    ("CV jack (optional)", "Tip → “CV” tag (35j); sleeve → GND rail. Needed for tests 12 and 13."),
    ("Pots (10 kΩ linear PC16SH, PCB pins)", "Solder three short leads to each pot. The third pot is a spare."),
    ("RV1 cutoff, 10 kΩ linear", "Clockwise end → +15 V rail; other end → −15 V rail; wiper → “RV1 wiper” tag (41i). If the cutoff falls when you turn clockwise, swap the two ends."),
    ("RV2 resonance, 10 kΩ linear", "Clockwise end → +15 V rail; other end → GND rail; wiper → “RV2 wiper” tag (3h). Linear crowds the resonance into the last part of the turn; that is fine for the tests."),
    ("RV4 offset trim, 50 kΩ 3296W", "One end → +15 V rail; other end → −15 V rail; wiper → “RV4 wiper” tag (22j). It can also sit on the board next to the tag, with its ends wired to the rails."),
    ("Bench supply", "+15 V → +15 V rail, −15 V → −15 V rail, common → GND rail, all at column 1 next to C14 and C15. Current limit about 50 mA per rail."),
    ("1N4001 reverse protection", "At the supply terminals or on the supply leads, not in the breadboard (the leads are thicker than its 0.7 mm limit): one from +15 V to common, cathode (band) to +15 V; one from −15 V to common, anode to −15 V."),
]

checks = [
    "Check the adapter: confirm with a multimeter that DIP pin 1 connects to SSOP pin 1 (the chip's dot). Most adapters keep the numbering; a few don't.",
    "Check that each power rail runs the full length of the board: meter from its hole at column 1 to its hole at column 44. On many boards the rails are split in the middle; bridge the gap with a short wire if so.",
    "Notch or dot to the left on both chips: U1 pin 1 at 8e, pin 16 at 8f; U2 pin 1 at 30e.",
    "Power the empty board first: +15 V at 8j and 30j, −15 V at 15a and 33a, 0 V at 15j, 33j and 32a.",
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
    --rail-pos: #ff7a6b; --rail-neg: #7ea8ff; --rail-gnd: #6fd39a;
    --part-res: #e2a46a; --part-cap: #64c3e0; --part-wire: #a3a9b4; --part-trim: #c39bf0;
    color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --paper: #14181d; --surface: #1b2027; --ink: #e6e9ee; --muted: #9aa3b2; --line: #2c333d;
  --accent: #f09a4f; --accent-soft: #3a2a1c;
  --board: #2a2722; --hole: #57524a; --chip: #0c0e11; --chip-text: #e9e6dd;
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
.frame.layout svg {{ width: 100%; min-width: 980px; }}
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
.parts td:nth-child(3), .parts td:nth-child(4), .wires td:nth-child(3) {{ font-family: var(--f-mono); font-size: 13px; white-space: nowrap; }}
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
footer {{ margin-top: 48px; color: var(--muted); font-size: 13px; }}
</style>

<div class="wrap">
<header class="col">
  <div class="eyebrow">Syntsamix · filter test circuit</div>
  <h1>SSI2144 breadboard</h1>
  <p class="lede">One SSI2144 ladder filter core with input attenuator, resonance and cutoff controls and the output stage, laid out for a standard solderless breadboard. It's the circuit for tests 1–7 and 11–13 in <code>simulation/filter/BREADBOARD.md</code>, built from the first Electrokit order, the SSOP adapter and an E24 1 % resistor kit. Tests 8–10 add parts from the second order.</p>
</header>

<section class="col">
  <h2>Before you power up</h2>
  <ol class="checks">{"".join(f"<li>{escape(c)}</li>" for c in checks)}</ol>
  <p class="callout">The pinout and the ladder, output and resonance values come from the SSI2144 datasheet (Rev 3.0, Figures 1 and 3). The input attenuator, drive jumper, resonance limit and cutoff scaling are this project's values, on E24 kit values (the channel card's own where it has them: 18 kΩ, 470 kΩ, 300 kΩ). A script checked the breadboard layout against the schematic, connection by connection: no missing links, no shorts.</p>
</section>

<section>
  <div class="col"><h2>Schematic</h2>
  <p>Scroll sideways on a narrow screen. Orange circles are connections to jacks; small rings are supply connections.</p></div>
  <div class="frame schem">{schem}</div>
</section>

<section>
  <div class="col"><h2>Breadboard layout</h2>
  <p>Columns 1–45, rows a–e at the bottom and f–j at the top. Each half-column of five holes is one connection. Orange tags mark where flying leads go to jacks and pots.</p></div>
  <div class="frame layout">{layout}</div>
  <div class="legend" aria-label="Legend">
    <span><i class="sw" style="background:var(--part-res)"></i>Resistor</span>
    <span><i class="sw" style="background:var(--part-cap)"></i>Capacitor</span>
    <span><i class="sw" style="background:var(--part-trim)"></i>Trimmer (3 pins)</span>
    <span><i class="sw" style="background:var(--part-wire)"></i>Wire</span>
    <span><i class="sw" style="background:var(--accent)"></i>J1 link</span>
    <span><i class="sw dot"></i>Flying lead to a jack or pot</span>
    <span><i class="sw" style="background:var(--rail-pos)"></i>+15 V</span>
    <span><i class="sw" style="background:var(--rail-gnd)"></i>GND</span>
    <span><i class="sw" style="background:var(--rail-neg)"></i>−15 V</span>
  </div>
</section>

<section>
  <div class="col"><h2>Parts and placement</h2>
  <p>Holes are written as column then row, for example <code>8a</code>. Tick parts off as you place them; the ticks stay in this browser only.</p></div>
  {table(parts_rows, ["Ref", "Value", "Holes", "Notes"], "parts")}
</section>

<section>
  <div class="col"><h2>Wires</h2></div>
  {table(wire_rows, ["Ref", "From → to", "Notes"], "wires")}
</section>

<section class="col">
  <h2>Off-board wiring</h2>
  <dl class="off">{"".join(f"<dt>{escape(a)}</dt><dd>{escape(b)}</dd>" for a, b in OFFBOARD)}</dl>
</section>

<footer class="col">Generated by <code>simulation/filter/breadboard_page.py</code> from the same placement list that <code>breadboard_layout.py</code> checks against the schematic.</footer>
</div>

<script>
document.querySelectorAll('input[type=checkbox]').forEach(function (box) {{
  var key = 'ssi2144-bb-' + box.id;
  try {{ box.checked = localStorage.getItem(key) === '1'; }} catch (e) {{}}
  box.addEventListener('change', function () {{
    try {{ localStorage.setItem(key, box.checked ? '1' : '0'); }} catch (e) {{}}
  }});
}});
</script>
"""

(HERE / "breadboard.html").write_text(page)
print(HERE / "breadboard.html")
