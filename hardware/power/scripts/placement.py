# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board placement: outline, bracket holes, footprint positions, a courtyard check, and the board update.

The board stands on edge in the power bay, hung from the bay's top strip (decision 162), so the panel is the
reference: KiCad x runs from the rear edge (x = 100) to the front (x = 277), the top edge (y = 99) runs parallel to
the panel underside about 5 mm below it, and the board tilts with the panel (about 6.7 degrees). The bottom edge is
35 mm lower (y = 134) at the rear; over the front 65 mm the floor comes closer, so the bottom edge rises to keep
3 mm above the cover (y = 128.41 at the front end, x = 277; from the rail positions, check on the frame). The component
side faces the master. Rows: buck (+20 V) on top, inverter (-20 V, IC ground on the -20V_CONV island) below.
Bracket holes (M3, board-only footprints, copper keep-out of radius 5 mm on both layers): H1 and H2 near the top
edge for the two brackets to the top strip (no fixing to the rear strip); the brackets sit on the back face.

Usage: python3 placement.py            check only (any Python)
       <KiCad python> placement.py --apply   with KiCad closed: write the outline, holes and positions
"""
import json, math, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
PCB = os.path.join(HERE, "..", "power.kicad_pcb")

# small power module (decision 185): master and chain 1 only, so the board ends 18 mm earlier than the first 195 mm
OUTLINE = [(100, 99), (277, 99), (277, 128.41), (229.5, 134), (100, 134)]
# two brackets to the top strip only (the user: no fixing to the rear strip; the brick jack is on the panel since
# decision 182, and the ribbon headers sit under H2)
HOLES = {"H1": (106.0, 103.0), "H2": (271.0, 103.0)}
KEEPOUT_R = 5.0
# where the design coordinates land on the A4 drawing sheet: 40 mm left puts the 177 mm board inside the frame,
# clear of the title block (the scripts, STATUS.md and the decisions keep the design coordinates above)
DX, DY = -40.0, 0.0
# reference designators kept on the silkscreen: parts soldered or plugged by hand and the test points; the
# JLCPCB-placed SMD parts keep theirs on the fabrication layer only (dense parts, silkscreen over pads)
SILK_REFS = {"J101", "J102", "J103", "C212", "C312", "TP102", "TP103", "TP201", "TP301", "TP302"}
# texts placed by hand (x, y, rotation): where the footprint's default spot overlaps pads or the edge
REF_AT = {"J103": (110.8, 103.0, 90)}
# the ribbon headers show their function on the silkscreen (what matters when plugging), not J401/J402
VALUE_SILK = {"J401": (236.4, 124.3, 90), "J402": (276.2, 122.0, 90)}

# ref: (x, y, rotation in degrees, KiCad counter-clockwise on screen)
P = {
 # --- input and protection (rear), clock -------------------------------------------------------
 "J103": (114.5, 102.5, 0),     # power LED lead, near the top edge under the LED hole in the top strip
 "R104": (122.5, 103.0, 0),
 "J101": (103.5, 128.3, 0),     # brick jack lead (decision 182), along the bottom at the rear
 "J102": (121.5, 129.6, 0),     # rocker lead
 "R102": (130.5, 132.0, 0),
 "TP102": (119.5, 125.0, 0),
 "F101": (116.5, 118.0, 0),
 "D101": (116.5, 112.0, 180),  # cathode toward the fuse
 "C101": (116.5, 108.0, 180),
 "Q101": (127.0, 120.0, 180),   # drain to the fuse, sources to Q102
 "Q102": (136.5, 120.0, 0),     # drain to VIN_SW
 "D102": (130.5, 128.5, 0),
 "R101": (135.5, 128.5, 0),
 "R103": (139.5, 128.5, 0),
 "C102": (143.5, 128.5, 0),
 "C103": (143.5, 120.0, 0),     # VIN_SW bulk, radial, hand-soldered
 "C104": (146.0, 132.4, 0),
 "TP101": (147.6, 114.0, 0),
 "U101": (132.0, 105.0, 0),
 "C105": (123.6, 106.5, 0),
 "C106": (123.6, 109.0, 0),
 "U102": (141.5, 105.0, 90),
 "C107": (140.0, 111.5, 0),
 "R105": (144.5, 111.5, 0),
 "TP103": (147.6, 101.5, 0),
 "TP104": (147.6, 105.0, 0),
 # --- +20 V buck (top row) ---------------------------------------------------------------------
 # input ceramics turned so VIN faces the IC's VIN pin, ground (to the plane by vias) away from it
 "C201": (153.6, 101.3, 180), "C202": (153.6, 104.9, 180), "C203": (153.6, 108.5, 180),
 "C204": (161.6, 101.4, 0), "C208": (157.8, 101.4, 0),
 "U201": (161.0, 107.0, 0),
 "D201": (167.6, 106.6, 270),
 "R201": (151.6, 115.4, 0), "R202": (155.4, 115.4, 0),
 "R204": (159.2, 115.4, 0), "C207": (162.9, 115.4, 0),
 "R203": (157.2, 112.2, 90), "C205": (159.4, 112.2, 90), "C206": (161.6, 112.2, 90),
 "R205": (163.8, 112.2, 90), "R206": (166.0, 112.2, 90),
 "D202": (168.2, 115.4, 180), "D203": (173.2, 115.4, 180), "R207": (177.6, 115.4, 0), "C214": (181.4, 115.4, 0),
 "L201": (178.0, 106.6, 0),
 "C209": (192.8, 106.6, 0), "C210": (192.8, 114.6, 0),
 "L202": (204.6, 106.6, 0),
 "C211": (218.0, 106.6, 0),
 "C212": (228.2, 105.0, 270), "C213": (229.6, 113.6, 90),
 "TP201": (234.0, 113.0, 0),
 # --- -20 V inverter (bottom row) ---------------------------------------------------------------
 "C301": (153.6, 122.0, 180), "C302": (153.6, 125.6, 180),
 "C303": (147.6, 127.5, 90),   # VIN to PGND: on the VIN area outside the -20V_CONV island
 "C304": (161.0, 132.4, 0), "C308": (157.0, 132.4, 0),
 "U301": (161.0, 126.6, 0),
 "D301": (170.4, 126.6, 270),
 "R301": (151.6, 118.6, 0), "R302": (155.4, 118.6, 0),
 "R304": (159.2, 118.6, 0), "C307": (162.9, 118.6, 0),
 "R303": (157.2, 121.6, 90), "C305": (159.4, 121.6, 90), "C306": (161.6, 121.6, 90),
 "R305": (163.8, 121.6, 90), "R306": (166.0, 121.6, 90),
 "D302": (177.6, 118.8, 180), "D303": (182.6, 118.8, 180), "R307": (187.0, 118.8, 0), "C314": (190.8, 118.8, 0),
 "L301": (187.0, 126.8, 0),
 "C309": (202.0, 126.8, 0), "C310": (175.6, 128.6, 270),   # C310 at the diode anode: ceramic in the switching loop
 "L302": (213.8, 126.8, 0),
 "C311": (227.2, 126.8, 0),
 "C312": (243.0, 108.0, 0), "C313": (252.0, 109.0, 0),
 "TP301": (257.0, 109.0, 0), "TP302": (211.0, 120.5, 0),
 # --- outputs (front): headers lying along the bottom edge (ribbon folds flat to the floor), pin 1 (stripe, -20 V)
 # toward the front as on the cards; each header's fuses above it, +20 V over pins 7/8, -20 V over pins 1/2
 # each header sits on the sloped bottom edge, so the three step up toward the front
 "J401": (250.5, 124.3, 270), "F401": (244.0, 117.3, 0), "F402": (251.5, 117.3, 0),
 "J402": (269.8, 122.0, 270), "F403": (262.9, 115.0, 0), "F404": (270.4, 115.0, 0),
}

def outline_bottom(x):
    """y of the bottom edge at x (it rises over the front part, where the floor comes closer)."""
    (xa, ya), (xb, yb) = OUTLINE[3], OUTLINE[2]
    return ya if x <= xa else ya + (x - xa) * (yb - ya) / (xb - xa)

def schematic():
    """ref -> (footprint lib id, KiCad symbol path, fields) from the schematic's netlist."""
    import subprocess, tempfile, xml.etree.ElementTree as ET
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "n.xml")
        subprocess.run(["/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli", "sch", "export", "netlist", "--format",
                        "kicadxml", "-o", out, os.path.join(os.path.dirname(PCB), "power.kicad_sch")], capture_output=True, check=True)
        root = ET.parse(out).getroot()
    return {c.get("ref"): (c.findtext("footprint"), c.find("sheetpath").get("tstamps") + c.findtext("tstamps").strip(),
                           {f.get("name"): (f.text or "") for f in c.iter("field")})
            for c in root.iter("comp")}


def courtyards():
    s = open(PCB).read(); out = {}
    for f in re.split(r'\n\t\(footprint ', s)[1:]:
        ref = re.search(r'\(property "Reference" "([^"]+)"', f).group(1)
        pts = []
        items = re.split(r'\n\t\t\((?=fp_|pad |property |model |embedded)', f)
        for it in items:
            kind = it.split(None, 1)[0] if it else ""
            if not kind.startswith("fp_") or '(layer "F.CrtYd")' not in it:
                continue
            xy = [(float(a), float(b)) for a, b in re.findall(r'\((?:start|end|center|xy|mid) ([-\d.]+) ([-\d.]+)\)', it)]
            if kind == "fp_circle":   # center and a point on the circle
                (cx, cy), (ex, ey) = xy; r = math.hypot(ex - cx, ey - cy); xy = [(cx - r, cy - r), (cx + r, cy + r)]
            pts += xy
        out[ref] = (min(p[0] for p in pts), max(p[0] for p in pts), min(p[1] for p in pts), max(p[1] for p in pts))
    return out

def placed_box(box, x, y, rot):
    x0, x1, y0, y1 = box; t = math.radians(rot); c, s = round(math.cos(t), 6), round(math.sin(t), 6)
    pts = [(px * c + py * s, -px * s + py * c) for px in (x0, x1) for py in (y0, y1)]
    return (x + min(p[0] for p in pts), x + max(p[0] for p in pts), y + min(p[1] for p in pts), y + max(p[1] for p in pts))

def check():
    cy = courtyards(); boxes = {}; bad = 0; sch = schematic()
    gone = sorted(set(cy) - set(sch) - set(HOLES))
    if gone: print("on the board but not in the schematic (removed by --apply):", gone)
    missing = sorted(set(sch) - set(P)); extra = sorted(set(P) - set(sch)) + sorted(set(sch) - set(cy))
    if missing or extra: print("missing:", missing, "unknown:", extra); bad += 1
    for r, (x, y, a) in P.items():
        if r in cy: boxes[r] = placed_box(cy[r], x, y, a)
    if sorted(set(sch) - set(cy)): print("in the schematic but not on the board (sync first):", sorted(set(sch) - set(cy)))
    for r, (x0, x1, y0, y1) in boxes.items():
        if x0 < 100.3 or x1 > OUTLINE[1][0] - 0.3 or y0 < 99.3 or y1 > min(outline_bottom(x0), outline_bottom(x1)) - 0.3:
            print(f"outside: {r} x {x0:.2f}..{x1:.2f} y {y0:.2f}..{y1:.2f}"); bad += 1
    for h, (x, y) in HOLES.items():   # the keep-out circle, as its square
        boxes[h] = (x - KEEPOUT_R, x + KEEPOUT_R, y - KEEPOUT_R, y + KEEPOUT_R)
    refs = sorted(boxes)
    for i, a in enumerate(refs):
        for b in refs[i + 1:]:
            A, B = boxes[a], boxes[b]
            if A[0] < B[1] and B[0] < A[1] and A[2] < B[3] and B[2] < A[3]:
                print(f"overlap: {a} / {b}"); bad += 1
    print(f"{len(P)} placed, {len(HOLES)} holes, {bad} problems")
    return bad


FP_LIBS = {"syntsamix": os.path.join(HERE, "..", "..", "libs", "syntsamix.pretty")}
STD_FP = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"


def load(fpid):
    import pcbnew
    lib = str(fpid.GetLibNickname()); name = str(fpid.GetLibItemName())
    return pcbnew.FootprintLoad(FP_LIBS.get(lib, os.path.join(STD_FP, lib + ".pretty")), name)


def apply():
    """Write the outline, bracket holes with keep-outs, fresh library footprints and their positions
    (KiCad's Python, KiCad closed). Everything new is built and configured before the first Remove:
    after a Remove, KiCad's SWIG layer returns untyped objects."""
    import pcbnew
    mm = pcbnew.FromMM
    pt = lambda x, y: pcbnew.VECTOR2I(mm(x + DX), mm(y + DY))
    board = pcbnew.LoadBoard(PCB)
    sch = schematic()
    drawings = [d for d in board.GetDrawings() if d.GetLayer() == pcbnew.Edge_Cuts]
    footprints = [f for f in board.Footprints()]
    old_zones = [z for z in board.Zones() if z.GetIsRuleArea() and z.GetZoneName().startswith("bracket")]
    add = []
    # fresh copies of every footprint from its library (KiCad's Update Footprints from Library), keeping the
    # fields, schematic link, attributes and pad nets, placed from P
    for old in footprints:
        r = old.GetReference()
        if r in HOLES or r not in sch:   # holes are rebuilt; parts gone from the schematic are dropped
            continue
        new = load(old.GetFPID()); new.SetFPID(old.GetFPID())
        for k, v in dict(old.GetFieldsText()).items():
            new.SetField(k, v)
        for k, v in sch[r][2].items():   # the schematic's part fields (ProjectPN, MPN, supplier ...), hidden
            if k in ("Reference", "Value", "Footprint", "Datasheet", "Description"):
                continue
            new.SetField(k, v)
            f = new.GetField(k)
            if f is not None:
                f.SetVisible(False)
        new.SetPath(pcbnew.KIID_PATH(sch[r][1])); new.SetSheetname(old.GetSheetname()); new.SetSheetfile(old.GetSheetfile())
        new.SetAttributes(old.GetAttributes())
        nets = {p.GetNumber(): p.GetNet() for p in old.Pads()}
        for p in new.Pads():
            if p.GetNumber() in nets:
                p.SetNet(nets[p.GetNumber()])
        x, y, a = P[r]
        new.SetPosition(pt(x, y)); new.SetOrientationDegrees(a)
        new.Reference().SetVisible(r in SILK_REFS)
        if r in REF_AT:
            tx, ty, tr = REF_AT[r]; new.Reference().SetPosition(pt(tx, ty)); new.Reference().SetTextAngleDegrees(tr)
        if r in VALUE_SILK:
            tx, ty, tr = VALUE_SILK[r]; v = new.Value()
            v.SetLayer(pcbnew.F_SilkS); v.SetVisible(True); v.SetPosition(pt(tx, ty)); v.SetTextAngleDegrees(tr)
        add.append(new)
    for h, (x, y) in HOLES.items():
        fp = pcbnew.FootprintLoad(STD_FP + "/MountingHole.pretty", "MountingHole_3.2mm_M3")
        fp.SetFPID(pcbnew.LIB_ID("MountingHole", "MountingHole_3.2mm_M3"))
        fp.SetReference(h); fp.SetValue("bracket M3"); fp.Reference().SetVisible(False)
        fp.SetAttributes(pcbnew.FP_BOARD_ONLY | pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
        fp.SetPosition(pt(x, y)); add.append(fp)
        z = pcbnew.ZONE(board); z.SetIsRuleArea(True); z.SetZoneName(f"bracket {h}")
        z.SetLayerSet(pcbnew.LSET.AllCuMask())
        z.SetDoNotAllowZoneFills(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True)
        z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
        o = z.Outline(); o.NewOutline()
        for k in range(24):
            t = 2 * math.pi * k / 24
            o.Append(mm(x + DX + KEEPOUT_R * math.cos(t)), mm(y + DY + KEEPOUT_R * math.sin(t)))
        add.append(z)
    for a, b in zip(OUTLINE, OUTLINE[1:] + OUTLINE[:1]):
        seg = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        seg.SetStart(pt(*a)); seg.SetEnd(pt(*b)); seg.SetLayer(pcbnew.Edge_Cuts); seg.SetWidth(mm(0.05))
        add.append(seg)
    for item in drawings + footprints + old_zones:
        board.Remove(item)
    for item in add:
        board.Add(item)
    pcbnew.SaveBoard(PCB, board)
    print("board written:", len(add), "items")


if __name__ == "__main__":
    bad = check()
    if "--apply" in sys.argv:
        if bad:
            sys.exit("not applied: fix the problems first")
        apply()
