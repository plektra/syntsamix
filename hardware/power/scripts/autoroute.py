# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board autoroute trial: net classes, ground planes, Freerouting, zone fill.

Runs in KiCad's own Python (it has pcbnew) with KiCad closed, since it rewrites power.kicad_pro and
power.kicad_pcb (or pass a copy of the project folder for a dry run):
  /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 autoroute.py
Steps: (1) net classes in the project (Power 1.0 mm for the input, switch and rail nets, Default 0.3 mm),
(2) bottom planes: PGND over the board, the inverter's -20V_CONV island under its row (higher priority),
(3) 0.3 mm vias under the TPS54560 exposed pads (locked, so Freerouting keeps them), (4) Specctra DSN out,
Freerouting CLI, SES back in, (5) top pours (PGND, and -20V_CONV over the island), zone fill, save.
The board before routing is kept in build/power_preroute.kicad_pcb.
"""
import json, os, shutil, subprocess, sys
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..")   # a copy of the project for a dry run
PRO = os.path.join(PROJ, "power.kicad_pro")
PCB = os.path.join(PROJ, "power.kicad_pcb")
BUILD = os.path.join(PROJ, "scripts", "build") if len(sys.argv) > 1 else os.path.join(HERE, "build")
# Freerouting 2.5.0 as the jar on Temurin 25 (both under ~/.local/opt): the native macOS CLI build crashes in the
# router thread (GraalVM serialization error) and then hangs
JAVA = os.path.expanduser("~/.local/opt/jdk-25.0.4.1+1/Contents/Home/bin/java")
FREEROUTING = os.path.expanduser("~/.local/opt/freerouting-2.5.0/freerouting-2.5.0.jar")

POWER_NETS = ["/Input and clock/VBRICK", "Net-(D101-K)", "Net-(D102-K)", "/VIN_SW", "Net-(D201-K)",
              "Net-(C209-Pad1)", "/+20V_RAW", "Net-(D301-K)", "/-20V_RAW", "/Outputs/*", "PGND",
              "/-20 V inverter/-20V_CONV"]
sys.path.insert(0, HERE)
from placement import OUTLINE, DX, DY   # board outline (panel reference), offset to the drawing sheet
ISLAND = [(148.5, 116.8), (214.0, 116.8), (214.0, 134), (148.5, 134)]   # under the inverter row
EP_VIAS = [(-0.6, -1.03), (-0.6, 0), (-0.6, 1.03), (0.6, -1.03), (0.6, 0), (0.6, 1.03)]


def set_netclasses():
    pro = json.load(open(PRO))
    ns = pro["net_settings"]
    default = next(c for c in ns["classes"] if c["name"] == "Default")
    default.update(track_width=0.3, clearance=0.2, via_diameter=0.6, via_drill=0.3)
    # 0.2 mm clearance: the TPS54560 footprint has 0.2 mm between its pins and the exposed pad
    power = dict(default, name="Power", priority=0, track_width=1.0, clearance=0.2, via_diameter=0.8, via_drill=0.4)
    ns["classes"] = [default, power]
    ns["netclass_patterns"] = [{"netclass": "Power", "pattern": p} for p in POWER_NETS]
    pro["board"]["design_settings"]["rules"]["min_copper_edge_clearance"] = 0.3   # JLCPCB: 0.3 mm to a routed edge
    pro["board"]["design_settings"]["rules"]["min_track_width"] = 0.15            # Freerouting necks to 0.18 at fine pins
    json.dump(pro, open(PRO, "w"), indent=2)


def mm(v):
    return pcbnew.FromMM(v)


def zone(board, net, layer, pts, priority):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(board.FindNet(net))
    z.SetAssignedPriority(priority)
    z.SetLocalClearance(mm(0.3))
    z.SetMinThickness(mm(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
    z.SetThermalReliefGap(mm(0.4))
    z.SetThermalReliefSpokeWidth(mm(0.6))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o = z.Outline()
    o.NewOutline()
    for x, y in pts:
        o.Append(mm(x + DX), mm(y + DY))
    board.Add(z)
    return z


def inset(pts, d=0.5):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return [(x + (d if x < cx else -d), y + (d if y < cy else -d)) for x, y in pts]


def ep_vias(board):
    for ref in ("U201", "U301"):
        fp = board.FindFootprintByReference(ref)
        pad = next(p for p in fp.Pads() if p.GetNumber() == "9")
        c = pad.GetPosition()
        for dx, dy in EP_VIAS:
            v = pcbnew.PCB_VIA(board)
            v.SetPosition(pcbnew.VECTOR2I(c.x + mm(dx), c.y + mm(dy)))
            v.SetWidth(mm(0.6))
            v.SetDrill(mm(0.3))
            v.SetNet(pad.GetNet())
            v.SetLocked(True)
            board.Add(v)


def fill(board):
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())


def stitch(board, net, pitch=5.0, via=0.6, clearance=0.25):
    """Vias from the top pour of a net to its bottom plane: one in every pour piece that lies over the plane, and on a
    pitch grid in larger pieces; never in a pad (inside the fills, so clear of other copper)."""
    mm = pcbnew.FromMM
    margin = mm(via / 2 + clearance)
    zones = [z for z in board.Zones() if z.GetNetname() == net and not z.GetIsRuleArea()]
    def fills(layer):
        out = pcbnew.SHAPE_POLY_SET()
        for z in zones:
            if z.GetLayer() == layer:
                out.BooleanAdd(z.GetFilledPolysList(layer))
        out.Deflate(margin, pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, mm(0.01))
        return out
    top, bottom = fills(pcbnew.F_Cu), fills(pcbnew.B_Cu)
    pads = pcbnew.SHAPE_POLY_SET()
    for f in board.Footprints():
        for p in f.Pads():
            bb = p.GetBoundingBox(); bb.Inflate(margin)
            pads.NewOutline()
            for x, y in ((bb.GetLeft(), bb.GetTop()), (bb.GetRight(), bb.GetTop()), (bb.GetRight(), bb.GetBottom()),
                         (bb.GetLeft(), bb.GetBottom())):
                pads.Append(x, y)
    for t in board.GetTracks():   # existing vias: keep the new ones a via pitch away
        if t.GetClass() == "PCB_VIA":
            c = t.GetPosition(); r = mm(via) + margin
            pads.NewOutline()
            for x, y in ((c.x - r, c.y - r), (c.x + r, c.y - r), (c.x + r, c.y + r), (c.x - r, c.y + r)):
                pads.Append(x, y)
    top.BooleanIntersection(bottom)
    top.BooleanSubtract(pads)
    netinfo = board.FindNet(net); added = []; placed = []
    for i in range(top.OutlineCount()):
        piece = pcbnew.SHAPE_POLY_SET(); piece.AddOutline(top.COutline(i))
        for h in range(top.HoleCount(i)):
            piece.AddHole(top.CHole(i, h))
        bb = piece.BBox()
        pts = [(x, y) for x in range(bb.GetLeft(), bb.GetRight(), mm(pitch)) for y in range(bb.GetTop(), bb.GetBottom(), mm(pitch))
               if piece.Contains(pcbnew.VECTOR2I(x, y))]
        if not pts:
            v0 = piece.COutline(0).CPoint(0); pts = [(v0.x, v0.y)]
        for x, y in pts:
            if any((x - px) ** 2 + (y - py) ** 2 < (mm(via) + margin) ** 2 for px, py in placed):
                continue   # keep clear of the vias this pass already placed
            placed.append((x, y))
            v = pcbnew.PCB_VIA(board); v.SetPosition(pcbnew.VECTOR2I(x, y)); v.SetWidth(mm(via)); v.SetDrill(mm(via / 2))
            v.SetNet(netinfo); added.append(v)
    for v in added:
        board.Add(v)
    return len(added)


def main():
    os.makedirs(BUILD, exist_ok=True)
    shutil.copy(PCB, os.path.join(BUILD, "power_preroute.kicad_pcb"))
    set_netclasses()
    board = pcbnew.LoadBoard(PCB)
    zone(board, "PGND", pcbnew.B_Cu, inset(OUTLINE), 0)
    zone(board, "/-20 V inverter/-20V_CONV", pcbnew.B_Cu, ISLAND, 1)
    ep_vias(board)
    fill(board)
    dsn, ses = os.path.join(BUILD, "power.dsn"), os.path.join(BUILD, "power.ses")
    if not pcbnew.ExportSpecctraDSN(board, dsn):
        sys.exit("DSN export failed")
    r = subprocess.run([JAVA, "-Djava.awt.headless=true", "-jar", FREEROUTING, "--gui.enabled=false",
                        "-de", dsn, "-do", ses, "--router.autorouter.max_passes=100", "-mt", "1"],
                       capture_output=True, text=True, timeout=1800)
    open(os.path.join(BUILD, "freerouting.log"), "w").write(r.stdout + r.stderr)
    if r.returncode != 0 or not os.path.exists(ses):
        sys.exit(f"Freerouting failed ({r.returncode}); see build/freerouting.log")
    if not pcbnew.ImportSpecctraSES(board, ses):
        sys.exit("SES import failed")
    zone(board, "PGND", pcbnew.F_Cu, inset(OUTLINE), 0)
    zone(board, "/-20 V inverter/-20V_CONV", pcbnew.F_Cu, ISLAND, 1)
    fill(board)
    n = stitch(board, "PGND") + stitch(board, "/-20 V inverter/-20V_CONV")
    fill(board)
    print("stitching vias:", n)
    # Freerouting leaves the odd via or stub connected at one end only: remove them until none are left
    zones, removed = board.Zones(), 0
    while True:
        board.BuildConnectivity(); conn = board.GetConnectivity()
        dangling = [t for t in board.GetTracks() if not t.IsLocked() and conn.TestTrackEndpointDangling(t, False)]
        if not dangling:
            break
        for t in dangling:
            board.Remove(t)
        removed += len(dangling)
    if removed:
        pcbnew.ZONE_FILLER(board).Fill(zones)
    print("dangling vias and stubs removed:", removed)
    pcbnew.SaveBoard(PCB, board)
    print("routed:", len([t for t in board.GetTracks() if t.GetClass() == "PCB_TRACK"]), "tracks,",
          len([t for t in board.GetTracks() if t.GetClass() == "PCB_VIA"]), "vias")


if __name__ == "__main__":
    main()
