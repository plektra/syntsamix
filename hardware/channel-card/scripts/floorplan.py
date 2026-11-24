# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Channel card trial floorplan: does every part fit on 33 x 318 mm, and where do the headers and the meter land?

Design coordinates: d = distance from the card's front edge (0..318 mm, the fader end is the front), u = position
across the card seen from above with the front toward the player (0 = left edge, 33 = right edge). On the KiCad
sheet x = X0 + d, y = Y0 + u (the player's view turned a quarter clockwise, not mirrored).

The panel controls, the chain headers and the hand-set underside parts are placed by hand (FIX: the shaft, plunger
or header centre). Everything else is placed by a simple connectivity placer: ICs go to the free spot nearest
their anchor (IC), each decoupling capacitor to its IC's supply pin, then the part with the most connections to
placed parts goes to the free spot nearest the pads it connects to, until nothing is left. Test pads go on the
underside. Courtyards never overlap; a through-hole pad blocks the other side too.

It is a trial, not the final placement: it shows how full the card is and gives a starting point.

Usage (KiCad's Python, it needs pcbnew):
  <KiCad python> floorplan.py [--0603] [--cans4] [--regsmall] [--twosided | --stack [--gap=2.54]]
    --0603      every 0805 resistor and capacitor as 0603
    --cans4     the 10 uF electrolytics in 4 x 5.4 mm cans instead of 5 x 5.4
    --regsmall  less copper kept free around the regulator tabs
    --twosided  chip resistors and capacitors on the underside (breaks decision 121 and Economic PCBA)
Writes build/floorplan<flags>.json (positions) and -top.svg / -under.svg (drawings).

Result 2026-11-23 (STATUS.md): with every SMD part on the top side 33 to 38 parts find no place within 90 mm of
their circuit, in 0805 and in 0603, with small cans and less regulator copper; with the chips underneath
everything is placed (top 67 % covered, 4 mm cans).
Two-board stack (--stack [--gap=mm]): the controls on an upper board, everything else on the bottom face of a
lower board on pin rows; it fits only with a 2.54 mm gap and 4 mm cans (lower face 80 % covered).
"""
import collections, json, math, os, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(HERE, "..")
BUILD = os.path.join(HERE, "build")
SMALL = "--0603" in sys.argv
CANS4 = "--cans4" in sys.argv        # 10 uF electrolytics in 4 x 5.4 mm cans instead of 5 x 5.4
REGSMALL = "--regsmall" in sys.argv  # regulator copper cut to the part plus a strip (planes carry the heat)
TWOSIDED = "--twosided" in sys.argv  # chip resistors and capacitors on the underside (needs /system: decision 121)
STACK = "--stack" in sys.argv        # two boards: controls on the upper one, the rest on one face of a lower one
TAG = "".join(t for t, on in (("-0603", SMALL), ("-cans4", CANS4), ("-regsmall", REGSMALL), ("-twosided", TWOSIDED),
                              ("-stack", STACK)) if on)
TAG += next((a.replace("--gap=", "-gap") for a in sys.argv if a.startswith("--gap=")), "")
W, L = 33.0, 318.0          # card width and depth (MECHANICAL.md, strip envelope)
X0, Y0 = 50.0, 100.0        # design (d, u) -> KiCad sheet (x, y)
G = 0.25                    # placement grid
EDGE = 0.5                  # courtyard to board edge, placed parts
STD_FP = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
FP_LIBS = {"syntsamix": os.path.join(PROJ, "..", "libs", "syntsamix.pretty")}
SWAP = {"Resistor_SMD:R_0805_2012Metric": "Resistor_SMD:R_0603_1608Metric",
        "Capacitor_SMD:C_0805_2012Metric": "Capacitor_SMD:C_0603_1608Metric"}
CAN4 = {"Capacitor_SMD:CP_Elec_5x5.4": "Capacitor_SMD:CP_Elec_4x5.4"}
POWER = {"AGND", "PGND", "+15V", "-15V", "+5V", "VEE", "/Chain and power/+20V_RAW", "/Chain and power/-20V_RAW"}
GROUNDS = {"AGND", "PGND"}

# ---- panel rows: distance of each control's centre from the card's front edge (MECHANICAL.md row order) --------
FADER_D, FADER_U = 42.0, 25.5     # fader travel centre; travel 60 mm, so its top end is at d = 72
METER_U = 4.0                     # meter LED column; CLIP level with the fader's top travel end, 6.0 mm pitch
ROW = dict(MUTE=92, PFL=92, ROW3=106, AUX2=125, AUX1=143, BYPASS=162, RES=182, CUTOFF=207, JACKS=227,
           LOWCUT=243, TRIM=263)
CEN = 16.5
# ref: (d, u, rotation, side, what the point is)
FIX = {
    "RV201": (FADER_D, FADER_U, 0, "F", "mid"),
    "SW201": (ROW["MUTE"], CEN + 7, 0, "F", "origin"), "SW301": (ROW["PFL"], CEN - 7, 0, "F", "origin"),
    "SW302": (ROW["ROW3"], 5.5, 0, "F", "origin"), "SW202": (ROW["ROW3"], 16.5, 0, "F", "origin"),
    "SW303": (ROW["ROW3"], 27.5, 0, "F", "origin"),
    "RV302": (ROW["AUX2"], CEN + 8, 0, "F", "shaft"), "RV301": (ROW["AUX1"], CEN, 0, "F", "shaft"),
    "SW181": (ROW["BYPASS"], CEN, 0, "F", "origin"),
    "RV183": (ROW["RES"], CEN, 0, "F", "shaft"), "RV181": (ROW["CUTOFF"], CEN, 0, "F", "shaft"),
    "J181": (ROW["JACKS"], CEN - 8, 270, "F", "barrel"), "J182": (ROW["JACKS"], CEN + 8, 270, "F", "barrel"),
    "SW1": (ROW["LOWCUT"], CEN, 0, "F", "origin"), "RV1": (ROW["TRIM"], CEN, 0, "F", "shaft"),
    # underside headers: power in front of audio, one line near the left edge; input header beside TRIM
    "J503": (121.0, 5.0, 270, "B", "mid"), "J501": (157.0, 5.0, 270, "B", "mid"), "J1": (261.0, 5.0, 270, "B", "mid"),
    # regulators at the rear edge, tabs to the rear
    "U501": (307.5, 8.6, 0, "F", "mid"), "U502": (307.5, 24.4, 0, "F", "mid"),
}
BUTTON_LED = {"SW1": "D5", "SW181": "D183", "SW201": "D203", "SW202": "D204", "SW301": "D301", "SW302": "D302",
              "SW303": "D303"}
METER_LEDS = ["D418", "D417", "D416", "D415", "D414", "D413", "D412", "D411"]   # CLIP first (rear), -30 last
# areas kept clear: (d0, d1, u0, u1)
BEZEL = (72 - 42 - 3.5, 72 + 3.5, METER_U - 2.5, METER_U + 2.5)     # printed meter bezel on the top side
REG_COPPER = [(296.0, 317.5, 0.5, 16.3), (296.0, 317.5, 16.7, 32.5)]   # regulator tab copper (decision 110)
if REGSMALL:
    REG_COPPER = [(298.5, 317.5, 2.0, 15.2), (298.5, 317.5, 17.8, 31.0)]
UNDER_FRONT = 41.0             # no underside parts in front of this (decision 162: 40 mm behind the front rail)
BAND_MARGIN = 15.0             # underside keep-out before and after the chain headers (decision 175)
# anchors: ICs and hand-set underside parts (d, u, side); the placer takes the nearest free spot
IC = {
    # chain and power
    "U503": (289, 29, "F"),
    # input: receiver, trim stage, low-cut buffer, low-cut switch
    "U1": (286, 6, "F"), "U2": (262, 27, "F"), "U3": (250, 27, "F"), "U4": (250, 6, "F"),
    # filter: driver, cores (L left, R right), Q VCA, I-V, post gain, CV summer, bypass switch
    "U104": (227, 16.5, "F"), "U101": (213, 5, "F"), "U102": (213, 28, "F"), "U103": (204, 16.5, "F"),
    "U105": (203, 5, "F"), "U106": (192, 28, "F"), "U107": (249, 16.5, "F"), "U108": (190, 5, "F"),
    "RV101": (222, 4.5, "B"), "RV151": (222, 28.5, "B"), "RV182": (251, 22, "B"),
    "JP101": (228, 12, "B"), "JP151": (228, 21, "B"), "JP102": (210, 12, "B"), "JP152": (210, 21, "B"),
    "JP181": (249, 10, "B"),
    # level: VCA, I-V, output, control, fader law
    "U201": (83, 7, "F"), "U202": (83, 26, "F"), "U203": (97, 27, "F"), "U204": (97, 6, "F"), "U205": (76, 12, "F"),
    "J301": (102, 5, "B"), "J302": (102, 28, "B"),
    # routing: pre-fader buffer, bus switches beside the AUX pots
    "U301": (124.5, 24, "F"), "U302": (135, 28, "F"), "U303": (157, 28, "F"), "U304": (171, 28, "F"),
    # meter: beside the fader
    "U401": (68, 12, "F"), "U402": (60, 12, "F"), "U403": (52, 12, "F"), "U404": (44, 12, "F"),
    "U405": (32, 12, "F"), "U406": (18, 12, "F"),
}
# parts with no signal connection of their own: a target by hand
MANUAL = {"C501": (289, 6), "C506": (289, 20), "C504": (291, 12), "C509": (291, 26), "C512": (286, 30),
          "D501": (294, 6), "D503": (294, 22), "D505": (286, 12), "D506": (286, 22), "D507": (150, 30),
          "R505": (150, 30), "JP301": (140, 30), "Q301": (108, 28)}
SHEET_ANCHOR = {"Input": (262, 16), "Filter": (215, 16), "Level": (88, 16), "Routing": (140, 28), "Meter": (40, 12),
                "Chain and power": (290, 16)}

# ---- two-board stack (--stack) ---------------------------------------------------------------------------------
# Upper board: the controls and their LEDs, hung from the panel as before (PCB top 10.0 mm under the panel).
# Lower board: every other part on its bottom face (one-sided assembly), GAP below the upper board on pin rows.
# Inside height under the panel: 20 mm at the front rail's inner face, rising 0.105 mm per mm (about 6 degrees,
# MECHANICAL.md: 40 mm at 190 mm); the card's front edge is 1 mm behind the rail face; 3 mm kept to the cover.
GAP = next((float(a.split("=")[1]) for a in sys.argv if a.startswith("--gap=")), 6.0)   # between the boards
LOWER_FACE = 10.0 + 1.6 + GAP + 1.6      # lower board's bottom face, below the panel underside


def first_d(height):
    """Smallest d at which a part this tall fits under the lower board."""
    return (LOWER_FACE + height + 3.0 - 20.0) / 0.105 - 1.0


MAIN_START = math.ceil(first_d(5.4))     # SMD parts up to the 5.4 mm cans
HAND_START = math.ceil(first_d(10.1))    # 3296W trimmers (10.03 mm), jumper headers with their jumpers
CHAIN_START = math.ceil(first_d(15.0))   # chain header with socket and cable (estimate, check the Wuerth drawings)
if STACK:
    CONTROL = {r for r, v in FIX.items() if v[3] == "F" and not r.startswith("U")} | set(BUTTON_LED.values()) | set(METER_LEDS)
    # zones along the lower board, front to rear: meter, level, regulators, chain headers with the power parts and
    # the routing beside them, input header and input stage, filter (its hand-set parts behind the header band)
    m = MAIN_START; c = CHAIN_START + 1.0; e = c + 72.0; f = e + 28.0; sp = L - f
    FIX.update({"J503": (c + 9.5, 5.0, 270, "B", "mid"), "J501": (c + 45.5, 5.0, 270, "B", "mid"),
                "J1": (e + 13.0, 5.0, 270, "B", "mid"),
                "U501": (c - 12.0, 24.4, 0, "B", "mid"), "U502": (c - 12.0, 8.6, 0, "B", "mid")})
    REG_COPPER = [(c - 23.0, c - 1.0, 0.5, 16.3), (c - 23.0, c - 1.0, 16.7, 32.5)]
    UNDER_FRONT = HAND_START
    # pin rows between the boards (2.54 mm): (d0, d1, u0, u1) kept free on both boards; 2 x 13 and 1 x 11 beside
    # the single buttons for the front controls and the meter, 1 x 15 on each edge further back
    PIN_ROWS = [(77.0, 110.0, 0.5, 5.6), (81.0, 109.0, 30.0, 32.5),
                (max(252.0, e + 26.0), max(252.0, e + 26.0) + 38.0, 0.5, 3.0), (185.0, 223.0, 30.0, 32.5)]
    IC = {
        "U401": (m + 4, 8, "B"), "U402": (m + 4, 17, "B"), "U403": (m + 4, 26, "B"), "U404": (m + 14, 8, "B"),
        "U405": (m + 16, 20, "B"), "U406": (m + 25, 10, "B"),
        "U204": (c - 55, 8, "B"), "U205": (c - 58, 24, "B"), "U201": (c - 46, 10, "B"), "U202": (c - 46, 24, "B"),
        "U203": (c - 36, 24, "B"), "J301": (c - 32, 8, "B"), "J302": (c - 32, 28, "B"),
        "U503": (c + 8, 28, "B"),
        "U301": (c + 20, 24, "B"), "U302": (c + 32, 15, "B"), "U303": (c + 44, 15, "B"), "U304": (c + 56, 15, "B"),
        "U4": (e + 8, 15, "B"), "U3": (e + 6, 26, "B"), "U2": (e + 16, 26, "B"), "U1": (e + 20, 15, "B"),
        "U108": (f + 6, 28, "B"), "U104": (f + 8, 17, "B"), "JP101": (f + 0.12 * sp, 8, "B"), "JP151": (f + 0.12 * sp, 24, "B"),
        "U101": (f + 0.3 * sp, 12, "B"), "U102": (f + 0.3 * sp, 22, "B"),
        "RV101": (f + 0.3 * sp, 5, "B"), "RV151": (f + 0.3 * sp, 28, "B"),
        "U103": (f + 0.5 * sp, 17, "B"), "JP102": (f + 0.5 * sp, 8, "B"), "JP152": (f + 0.5 * sp, 26, "B"),
        "U105": (f + 0.62 * sp, 8, "B"), "U106": (f + 0.62 * sp, 26, "B"),
        "U107": (f + 0.85 * sp, 16, "B"), "JP181": (f + 0.85 * sp, 6, "B"), "RV182": (f + 0.85 * sp, 27, "B"),
    }
    MANUAL = {"C501": (c + 4, 14), "C506": (c + 4, 22), "C504": (c - 26, 24), "C509": (c - 26, 9), "C512": (c + 14, 28),
              "D501": (c + 1, 14), "D503": (c + 1, 22), "D505": (c - 27, 16), "D506": (c - 27, 18),
              "D507": (c + 61, 24), "R505": (c + 61, 24), "JP301": (c + 36, 24), "Q301": (c + 51, 24)}
    SHEET_ANCHOR = {"Input": (e + 12, 20), "Filter": (f + 0.5 * sp, 16), "Level": (c - 46, 16), "Routing": (c + 40, 22),
                    "Meter": (m + 14, 16), "Chain and power": (c - 5, 16)}
else:
    CONTROL = set()


# ---- schematic ---------------------------------------------------------------------------------------------------
def netlist():
    with tempfile.TemporaryDirectory() as t:
        out = os.path.join(t, "n.xml")
        subprocess.run(["/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli", "sch", "export", "netlist",
                        "--format", "kicadxml", "-o", out, os.path.join(PROJ, "channel-card.kicad_sch")],
                       capture_output=True, check=True)
        return ET.parse(out).getroot()


ROOT = netlist()
FPID, SHEET, VALUE = {}, {}, {}
for c in ROOT.iter("comp"):
    r = c.get("ref"); f = c.findtext("footprint")
    f = SWAP.get(f, f) if SMALL else f
    FPID[r] = CAN4.get(f, f) if CANS4 else f
    SHEET[r] = c.find("sheetpath").get("names").strip("/"); VALUE[r] = c.findtext("value")
PIN_NET, NET_PINS = collections.defaultdict(dict), collections.defaultdict(list)
for net in ROOT.iter("net"):
    for n in net.iter("node"):
        PIN_NET[n.get("ref")][n.get("pin")] = net.get("name"); NET_PINS[net.get("name")].append((n.get("ref"), n.get("pin")))


def chip(ref):
    return FPID[ref].split(":")[1][:6] in ("R_0805", "R_0603", "C_0805", "C_0603", "C_1206") or ("--diodes" in sys.argv and "SOD-123" in FPID[ref])


def signal(net):
    return net not in POWER and not net.startswith("unconnected-") and len(NET_PINS[net]) <= 14


# ---- footprint geometry (from pcbnew, so the board step places exactly what was checked) -----------------------
_G = {}
SCRATCH = pcbnew.CreateEmptyBoard()   # Flip needs the footprint on a board


def load(fpid):
    lib, name = fpid.split(":")
    return pcbnew.FootprintLoad(FP_LIBS.get(lib, os.path.join(STD_FP, lib + ".pretty")), name)


def orient(fp, pos, rot, side):
    """The one place that turns a library footprint into a placed one (also used by the board step)."""
    fp.SetPosition(pos)
    if side == "B":
        fp.Flip(pos, pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
    fp.SetOrientationDegrees(rot)


def geom(fpid, rot, side):
    """Courtyard box (x0, x1, y0, y1) and pads {number: [(x, y, box, through-hole)]} relative to the origin, mm."""
    k = (fpid, rot, side)
    if k not in _G:
        fp = load(fpid); SCRATCH.Add(fp); orient(fp, pcbnew.VECTOR2I(0, 0), rot, side)
        fp.BuildCourtyardCaches()
        b = fp.GetCourtyard(pcbnew.B_CrtYd if side == "B" else pcbnew.F_CrtYd).BBox()
        pads = collections.defaultdict(list); boxes = []
        for p in fp.Pads():
            pb = p.GetBoundingBox()
            box = (pb.GetLeft() / 1e6, pb.GetRight() / 1e6, pb.GetTop() / 1e6, pb.GetBottom() / 1e6); boxes.append(box)
            pads[p.GetNumber()].append((p.GetPosition().x / 1e6, p.GetPosition().y / 1e6, box,
                                        p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH)))
        cy = (b.GetLeft() / 1e6, b.GetRight() / 1e6, b.GetTop() / 1e6, b.GetBottom() / 1e6)
        if b.GetWidth() <= 0:   # no courtyard drawn: the pads
            cy = (min(x[0] for x in boxes) - 0.25, max(x[1] for x in boxes) + 0.25,
                  min(x[2] for x in boxes) - 0.25, max(x[3] for x in boxes) + 0.25)
        _G[k] = (cy, dict(pads))
    return _G[k]


def anchor_point(fpid, rot, side, what):
    cy, pads = geom(fpid, rot, side)
    if what == "origin":
        return 0.0, 0.0
    if what == "shaft":      # Alpha RD901F/RD902F: between the two bracket slots
        a, b = pads[""][0], pads[""][1]; return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if what == "barrel":     # PJ398SM: 6.48 mm from the sleeve pad toward the tip pad (Thonk drawing)
        s, t = pads["S"][0], pads["T"][0]; k = 6.48 / math.hypot(t[0] - s[0], t[1] - s[1])
        return s[0] + (t[0] - s[0]) * k, s[1] + (t[1] - s[1]) * k
    return (cy[0] + cy[1]) / 2, (cy[2] + cy[3]) / 2     # "mid": courtyard centre


# ---- occupancy -------------------------------------------------------------------------------------------------
ND, NU = int(round(L / G)), int(round(W / G))


class Grid:
    def __init__(self):
        self.r = [bytearray(NU) for _ in range(ND)]

    @staticmethod
    def cells(b):
        return (max(0, int(math.floor(b[0] / G + 1e-6))), min(ND, int(math.ceil(b[1] / G - 1e-6))),
                max(0, int(math.floor(b[2] / G + 1e-6))), min(NU, int(math.ceil(b[3] / G - 1e-6))))

    def mark(self, b):
        a, e, c, f = self.cells(b)
        for i in range(a, e):
            self.r[i][c:f] = b"\x01" * (f - c)

    def free(self, b):
        if b[0] < EDGE - 1e-6 or b[1] > L - EDGE + 1e-6 or b[2] < EDGE - 1e-6 or b[3] > W - EDGE + 1e-6:
            return False
        a, e, c, f = self.cells(b)
        for i in range(a, e):
            if self.r[i].find(1, c, f) >= 0:
                return False
        return True

    def used(self):
        return sum(sum(r) for r in self.r) * G * G


GRID = {"F": Grid(), "B": Grid()}
PL = {}          # ref -> (d, u of the footprint origin, rotation, side)
PAD = {}         # ref -> {pin: (d, u)}
BOX = {}         # ref -> courtyard box
MOVED = {}       # ref -> distance from its target to where it went
R_MAX = 90.0
OFFS = sorted(((i * G, j * G) for i in range(-int(R_MAX / G), int(R_MAX / G) + 1) for j in range(-NU, NU + 1)
               if math.hypot(i * G, j * G) <= R_MAX), key=lambda o: o[0] ** 2 + o[1] ** 2)


def put(ref, d, u, rot, side, check=True):
    cy, pads = geom(FPID[ref], rot, side)
    box = (d + cy[0], d + cy[1], u + cy[2], u + cy[3])
    if check and not GRID[side].free(box):
        return False
    GRID[side].mark(box)
    other = GRID["B" if side == "F" else "F"]
    for plist in pads.values():
        for (x, y, pb, tht) in plist:
            if tht and not STACK:   # the joint and the lead end on the other side
                other.mark((d + pb[0] - 0.4, d + pb[1] + 0.4, u + pb[2] - 0.4, u + pb[3] + 0.4))
    PL[ref] = (round(d, 3), round(u, 3), rot, side); BOX[ref] = box
    PAD[ref] = {n: (d + pl[0][0], u + pl[0][1]) for n, pl in pads.items()}
    return True


def spot(ref, target, side, rot):
    """Origin of the free spot nearest the target for the courtyard centre, or None."""
    cy, _ = geom(FPID[ref], rot, side)
    cx, cyy = (cy[0] + cy[1]) / 2, (cy[2] + cy[3]) / 2
    hd, hu = (cy[1] - cy[0]) / 2, (cy[3] - cy[2]) / 2
    td, tu = round(target[0] / G) * G, round(target[1] / G) * G
    g = GRID[side]
    for od, ou in OFFS:
        d, u = td + od, tu + ou
        if u - hu < EDGE or u + hu > W - EDGE or d - hd < EDGE or d + hd > L - EDGE:
            continue
        i, j = int(d / G), int(u / G)
        if g.r[min(i, ND - 1)][min(j, NU - 1)]:
            continue
        if g.free((d - hd, d + hd, u - hu, u + hu)):
            return d - cx, u - cyy, math.hypot(od, ou)
    return None


def pin_targets(ref):
    """pin -> centroid of the placed pads on its (signal) net."""
    out = {}
    for pin, net in PIN_NET[ref].items():
        if not signal(net):
            continue
        pts = [PAD[r][p] for r, p in NET_PINS[net] if r != ref and r in PAD and p in PAD[r] and r not in CONTROL]
        if pts:
            out[pin] = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
    return out


def place(ref, target, side="F", rots=(0, 90, 180, 270)):
    """Nearest free spot; among the rotations the one with the shortest connections."""
    tg = pin_targets(ref); best = None
    for rot in rots:
        s = spot(ref, target, side, rot)
        if s is None:
            continue
        _, pads = geom(FPID[ref], rot, side)
        wire = sum(math.hypot(s[0] + pads[p][0][0] - t[0], s[1] + pads[p][0][1] - t[1]) for p, t in tg.items() if p in pads)
        cost = s[2] * max(1, len(tg)) + wire
        if best is None or cost < best[0] - 1e-6:
            best = (cost, s, rot)
    if best is None:
        return False
    _, s, rot = best
    put(ref, s[0], s[1], rot, side); MOVED[ref] = s[2]
    return True


# ---- the run ---------------------------------------------------------------------------------------------------
def run():
    failed = []
    # 1. fixed parts
    for ref, (d, u, rot, side, what) in FIX.items():
        ax, ay = anchor_point(FPID[ref], rot, side, what)
        put(ref, d - ax, u - ay, rot, side, check=False)
    for sw, led in BUTTON_LED.items():      # LED behind each plunger, lying across the card
        d, u = FIX[sw][0], FIX[sw][1]
        ax, ay = anchor_point(FPID[led], 90, "F", "mid"); put(led, d + 5.9 - ax, u - ay, 90, "F", check=False)
    for i, led in enumerate(METER_LEDS):
        ax, ay = anchor_point(FPID[led], 90, "F", "mid"); put(led, 72 - 6.0 * i - ax, METER_U - ay, 90, "F", check=False)
    GRID["F"].mark(BEZEL)
    for b in REG_COPPER:
        GRID["B" if STACK else "F"].mark(b)
    if STACK:
        GRID["B"].mark((0, MAIN_START, 0, W))
        for b in PIN_ROWS:
            GRID["B"].mark(b)
            if not GRID["F"].free(b):
                print("pin row over a control:", b)
    hd = [BOX["J503"], BOX["J501"]]
    band = (min(b[0] for b in hd) - BAND_MARGIN, max(b[1] for b in hd) + BAND_MARGIN, 0, W)
    keep = Grid(); keep.r = [bytearray(r) for r in GRID["B"].r]
    GRID["B"].mark(band); GRID["B"].mark((0, UNDER_FRONT, 0, W))
    # 2. ICs and hand-set parts at their anchors
    order = sorted(IC, key=lambda r: r.startswith("U")) if STACK else list(IC)   # stack: hand-set parts first
    for ref in order:
        if STACK and ref.startswith("U") and GRID["B"] is not keep:   # ICs may sit in the header band
            for r2, v in PL.items():
                if v[3] == "B":
                    keep.mark(BOX[r2])
            GRID["B"] = keep
        d, u, side = IC[ref]
        if not place(ref, (d, u), side, rots=(0, 90, 180, 270)):
            failed.append(ref)
    if TWOSIDED:   # chip parts may sit in the header band and at the front: they are lower than the socket
        for ref, (d, u, rot, side) in PL.items():
            if side == "B":
                keep.mark(BOX[ref])
        for ref, (d, u, rot, side) in PL.items():
            if side == "F":
                for pl in geom(FPID[ref], rot, side)[1].values():
                    for (x, y, pb, t) in pl:
                        if t:
                            keep.mark((d + pb[0] - 0.4, d + pb[1] + 0.4, u + pb[2] - 0.4, u + pb[3] + 0.4))
        GRID["B"] = keep
    # 3. decoupling capacitors: each to a supply pin of an IC on its own sheet
    count = collections.Counter()
    todo = [r for r in FPID if r not in PL]
    for ref in sorted(todo):
        nets = set(PIN_NET[ref].values())
        if not (ref.startswith("C") and VALUE[ref].startswith("100n") and nets <= POWER and len(nets) == 2):
            continue
        rail = next(iter(nets - GROUNDS), None)
        cands = [(count[(ic, rail)], ic, pin) for ic in PL if ic.startswith("U") and SHEET[ic] == SHEET[ref]
                 for pin, net in PIN_NET[ic].items() if net == rail]
        if not cands:
            continue
        _, ic, pin = min(cands); count[(ic, rail)] += 1
        if not place(ref, PAD[ic][pin], "B" if TWOSIDED or STACK else "F", rots=(0, 90)):
            failed.append(ref)
    # 4. manual targets
    for ref, t in MANUAL.items():
        if ref not in PL and not place(ref, t, "B" if STACK else "F", rots=(0, 90)):
            failed.append(ref)
    # 5. the rest, most connected first
    def area(ref):
        cy = geom(FPID[ref], 0, "F")[0]; return (cy[1] - cy[0]) * (cy[3] - cy[2])
    rest = [r for r in FPID if r not in PL and r not in failed]
    big = [r for r in rest if area(r) > 15 and not r.startswith("TP")]   # electrolytics, diodes: before the chips
    for todo in (big, [r for r in rest if r not in big]):
      while todo:
        best = None
        for ref in todo:
            tg = pin_targets(ref)
            n = len([p for p, net in PIN_NET[ref].items() if signal(net)])
            score = (len(tg) / n if n else 0, len(tg))
            if best is None or score > best[0]:
                best = (score, ref, tg)
        score, ref, tg = best
        if tg:
            t = (sum(p[0] for p in tg.values()) / len(tg), sum(p[1] for p in tg.values()) / len(tg))
        else:
            t = SHEET_ANCHOR[SHEET[ref]]
        side = "B" if ref.startswith("TP") or STACK or (TWOSIDED and chip(ref)) else "F"
        if ref.startswith("TP") and not tg:      # a ground test pad: near its sheet, off the header band
            net = next(iter(PIN_NET[ref].values()))
            pts = [PAD[r][p] for r, p in NET_PINS[net] if r in PAD and SHEET[r] == SHEET[ref] and p in PAD[r]]
            if pts:
                t = (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))
        if not place(ref, t, side, rots=(0,) if ref.startswith("TP") else (0, 90, 180, 270)):
            failed.append(ref)
        todo.remove(ref)
    return failed, band


def hpwl():
    tot = 0.0; worst = []
    for net, pins in NET_PINS.items():
        if not signal(net):
            continue
        pts = [PAD[r][p] for r, p in pins if r in PAD and p in PAD[r] and r not in CONTROL]
        if len(pts) > 1:
            w = max(p[0] for p in pts) - min(p[0] for p in pts) + max(p[1] for p in pts) - min(p[1] for p in pts)
            tot += w; worst.append((w, net))
    return tot, sorted(worst, reverse=True)[:12]


COLOUR = {"Input": "#4c78a8", "Filter": "#e45756", "Level": "#54a24b", "Routing": "#b279a2", "Meter": "#f58518",
          "Chain and power": "#9d755d"}


def svg(band):
    """Two drawings (top, underside), each cut into three strips of 106 mm so the picture stays readable."""
    S = 9.0; SEG = 106.0; RH = (W + 7) * S
    for side in "FB":
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{(SEG + 4) * S:.0f}" height="{3 * RH + 16:.0f}" '
               f'font-family="Helvetica" font-size="9"><rect width="100%" height="100%" fill="white"/>']
        for k in range(3):
            d0 = k * SEG; oy = 16 + k * RH
            X = lambda d: (d - d0 + 2) * S
            Y = lambda u: oy + u * S
            out.append(f'<svg x="0" y="{oy - 14}" width="{(SEG + 4) * S}" height="{RH}"><g transform="translate(0,{14 - oy})">')
            out.append(f'<rect x="{X(0)}" y="{Y(0)}" width="{L * S}" height="{W * S}" fill="#f4f4f0" stroke="black"/>')
            out.append(f'<text x="{X(d0)}" y="{oy - 3}" font-size="11">{("control board" if STACK else "top") if side == "F" else ("lower board, seen through it" if STACK else "underside, seen through the board")}'
                       f', d {d0:.0f} to {d0 + SEG:.0f} mm from the front; {"0603" if SMALL else "0805"} passives</text>')
            zones = [BEZEL] + REG_COPPER if side == "F" else [band, (0, UNDER_FRONT, 0, W)]
            if STACK:
                zones = [BEZEL] + PIN_ROWS if side == "F" else [band, (0, UNDER_FRONT, 0, W), (0, MAIN_START, 0, W)] + REG_COPPER + PIN_ROWS
            for b in zones:
                out.append(f'<rect x="{X(b[0])}" y="{Y(b[2])}" width="{(b[1] - b[0]) * S}" height="{(b[3] - b[2]) * S}" fill="#ddd" stroke="#999" stroke-dasharray="3"/>')
            for ref, (d, u, rot, sd) in PL.items():
                b = BOX[ref]
                if b[1] < d0 - 2 or b[0] > d0 + SEG + 2:
                    continue
                if sd == side:
                    out.append(f'<rect x="{X(b[0]):.1f}" y="{Y(b[2]):.1f}" width="{(b[1] - b[0]) * S:.1f}" height="{(b[3] - b[2]) * S:.1f}" '
                               f'fill="{COLOUR[SHEET[ref]]}" fill-opacity="{0.35 if ref in FIX else 0.8}" stroke="black" stroke-width="0.4"/>')
                    if (b[1] - b[0]) * (b[3] - b[2]) > 20 or ref.startswith("TP"):
                        out.append(f'<text x="{X((b[0] + b[1]) / 2):.1f}" y="{Y((b[2] + b[3]) / 2) + 3:.1f}" text-anchor="middle">{ref}</text>')
                elif not STACK:   # through-hole pads of the other side's parts
                    _, pads = geom(FPID[ref], rot, sd)
                    for pl in pads.values():
                        for (x, y, pb, tht) in pl:
                            if tht:
                                out.append(f'<circle cx="{X(d + x):.1f}" cy="{Y(u + y):.1f}" r="{0.8 * S}" fill="#888"/>')
            for dd in range(int(d0), int(min(L, d0 + SEG)) + 1, 10):
                out.append(f'<text x="{X(dd)}" y="{Y(W) + 11}" text-anchor="middle">{dd}</text>')
            out.append("</g></svg>")
        out.append("</svg>")
        os.makedirs(BUILD, exist_ok=True)
        open(os.path.join(BUILD, f"floorplan{TAG}-{'top' if side == 'F' else 'under'}.svg"), "w").write("\n".join(out))


if __name__ == "__main__":
    failed, band = run()
    os.makedirs(BUILD, exist_ok=True)
    json.dump({"placed": PL, "small": SMALL}, open(os.path.join(BUILD, f"floorplan{TAG}.json"), "w"), indent=0)
    svg(band)
    tot, worst = hpwl()
    top = GRID["F"].used()
    print(f"underside used {GRID['B'].used():.0f} mm2 (keep-outs counted unless --twosided)")
    far = sorted(((v, r) for r, v in MOVED.items()), reverse=True)[:15]
    print(f"{'0603' if SMALL else '0805'}{TAG}: {len(PL)} of {len(FPID)} placed, not placed: {failed}")
    print(f"top side used {top:.0f} of {W * L:.0f} mm2 ({100 * top / (W * L):.0f} %), free {W * L - top:.0f} mm2")
    print(f"signal net half-perimeter total {tot:.0f} mm")
    print("longest nets:", ", ".join(f"{n} {w:.0f}" for w, n in worst))
    print("pushed furthest from target:", ", ".join(f"{r} {v:.0f}" for v, r in far))
    print("headers: " + "; ".join(f"{r} pin 1 at d {PAD[r]['1'][0]:.2f} u {PAD[r]['1'][1]:.2f}, pin 2 at d {PAD[r]['2'][0]:.2f} u {PAD[r]['2'][1]:.2f}, "
                                  f"body d {BOX[r][0]:.1f}..{BOX[r][1]:.1f}" for r in ("J503", "J501", "J1")))
    print(f"underside keep-out band d {band[0]:.1f}..{band[1]:.1f}")
    if STACK:
        cross = [n for n, pins in NET_PINS.items() if not n.startswith("unconnected-")
                 and any(r in CONTROL for r, _ in pins) and any(r not in CONTROL for r, _ in pins)]
        sup = [n for n in cross if n in POWER]
        low = W * (L - MAIN_START); usedlow = GRID["B"].used() - W * MAIN_START
        print(f"stack: gap {GAP} mm, lower board from d {MAIN_START} (SMD), hand-set parts from d {HAND_START}, chain headers from d {CHAIN_START}")
        print(f"lower board {low:.0f} mm2, covered {usedlow:.0f} mm2 ({100 * usedlow / low:.0f} %) with pin rows and regulator copper")
        print(f"nets between the boards: {len(cross)} ({len(cross) - len(sup)} signals, supplies {sorted(sup)}); pin places kept: "
              f"{sum((int(max(b[1] - b[0], b[3] - b[2]) / 2.54) + 1) * (2 if min(b[1] - b[0], b[3] - b[2]) > 4 else 1) for b in PIN_ROWS)}")
        for r in ("J503", "J501", "J1", "RV101", "RV151", "RV182", "J301", "J302", "JP101", "JP181"):
            print(f"  {r}: d {BOX[r][0]:.1f}..{BOX[r][1]:.1f}, u {BOX[r][2]:.1f}..{BOX[r][3]:.1f}")
