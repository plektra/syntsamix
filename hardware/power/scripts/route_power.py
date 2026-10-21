# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board: the power stage routed by hand, as data (locked copper areas, tracks and vias).

Runs after placement.py --apply and before autoroute.py, in KiCad's Python with KiCad closed:
  <KiCad python> route_power.py [project folder copy]
It removes every track, via and copper zone (the bracket keep-outs stay), then writes the items below, locked, so
Freerouting routes only the small-signal connections around them. Coordinates follow placement.py (KiCad x from
the rear edge at 100 to the front at 295, y from the top edge at 99). The top layer carries the power copper; the
bottom layer is the PGND plane with the inverter's -20V_CONV island (added by autoroute.py), cut only by the
-20V_RAW feed to the front headers (it would cross the +20V_RAW feed on top).
"""
import math, os, sys
import pcbnew
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from placement import DX, DY   # design coordinates to the drawing sheet

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..")
PCB = os.path.join(PROJ, "power.kicad_pcb")

VB, DK, SRC = "/Input and clock/VBRICK", "Net-(D101-K)", "Net-(D102-K)"
VPRE = "/Input and clock/VIN_PRE"   # Q102 drain to L101, the input pi filter (decision 187)
VIN, SW1, OUT1, P20 = "/VIN_SW", "Net-(D201-K)", "Net-(C209-Pad1)", "/+20V_RAW"
SW2, M20, CONV, GND = "Net-(D301-K)", "/-20V_RAW", "/-20 V inverter/-20V_CONV", "PGND"
F, B = pcbnew.F_Cu, pcbnew.B_Cu

# copper areas: (name, net, layer, priority, outline); higher priority wins where areas overlap
ZONES = [
    ("power sources", SRC, F, 5, [(120.7, 119.0), (122.8, 119.0), (122.8, 117.7), (125.45, 117.7), (125.45, 121.0),
                                  (123.5, 121.0), (123.5, 122.3), (120.7, 122.3)]),   # Q101/Q102 sources
    # Q102 drain, L101 input, C108 and C102 below L101 (decision 187); the spine starts at L101's output
    ("power VIN_PRE", VPRE, F, 5, [(126.5, 117.2), (135.4, 117.2), (135.4, 123.6), (137.5, 123.6), (137.5, 126.9),
                                   (133.3, 126.9), (133.3, 123.6), (126.5, 123.6)]),
    ("power VIN spine", VIN, F, 5, [(137.3, 116.9), (145.4, 116.9), (145.4, 112.6), (151.3, 112.6), (151.3, 133.5),
                                    (143.8, 133.5), (143.8, 126.2), (145.4, 126.2), (145.4, 123.2), (137.3, 123.2)]),
    ("power VIN buck", VIN, F, 6, [(151.0, 110.3), (154.3, 110.3), (154.3, 99.6), (156.5, 99.6), (156.5, 105.6),
                                   (158.7, 105.6), (158.7, 107.1), (156.5, 107.1), (156.5, 113.1), (151.0, 113.1)]),
    ("power VIN inverter", VIN, F, 7, [(150.9, 127.6), (154.3, 127.6), (154.3, 120.5), (156.5, 120.5), (156.5, 125.4),
                                       (158.7, 125.4), (158.7, 126.6), (156.5, 126.6), (156.5, 130.9), (154.6, 130.9),
                                       (154.6, 133.5), (150.9, 133.5)]),
    # switch nodes kept small (EMI review 2026-10-21): pin 8, the diode's cathode, the inductor's pad, the snubber tap
    ("power SW buck", SW1, F, 5, [(162.6, 103.3), (163.5, 103.3), (163.5, 100.0), (165.0, 100.0), (165.0, 103.3), (171.6, 103.3),
                                  (171.6, 106.5), (165.0, 106.5), (165.0, 105.8), (162.6, 105.8)]),
    ("power out buck", OUT1, F, 5, [(181.8, 103.4), (203.4, 103.4), (203.4, 109.9), (192.8, 109.9), (192.8, 115.9),
                                    (189.8, 115.9), (189.8, 109.9), (181.8, 109.9)]),
    ("power +20V_RAW", P20, F, 5, [(205.6, 103.6), (216.3, 103.6), (216.3, 109.6), (205.6, 109.6)]),
    ("power SW inverter", SW2, F, 5, [(162.6, 123.6), (168.4, 123.6), (168.4, 121.6), (172.6, 121.6), (172.6, 125.4),
                                      (162.6, 125.4)]),
    ("power -20V_RAW", M20, F, 5, [(214.9, 121.0), (234.9, 121.0), (234.9, 132.9), (214.9, 132.9)]),
    # inverter output return on top (L301 to PGND, C309 PGND side): the bottom under it is the -20V_CONV island,
    # so it reaches the PGND plane by vias above the island (y < 116.8)
    ("power PGND inverter out", GND, F, 4, [(193.0, 112.6), (200.5, 112.6), (200.5, 129.8), (190.2, 129.8),
                                            (190.2, 120.3), (191.0, 120.3), (191.0, 117.8), (193.0, 117.8)]),  # takes in C314
]

# tracks: (net, width, layer, points)
TRACKS = [
    (VB, 1.2, F, [(103.5, 128.3), (103.5, 124.6), (115.38, 124.6), (115.38, 128.3)]),    # J101 pins 1 and 4
    (VB, 1.2, F, [(105.5, 124.6), (105.5, 119.4)]),                                       # to F101 (upright)
    (DK, 1.2, F, [(105.5, 112.6), (108.5, 112.6), (109.1, 112.0), (114.35, 112.0)]),      # F101 to D101 cathode
    (DK, 1.2, F, [(114.8, 113.0), (116.5, 114.8), (116.5, 118.5)]),                       # to Q101 drain
    (DK, 0.8, F, [(114.35, 112.0), (114.35, 110.0), (115.55, 108.8), (115.55, 108.0)]),   # to C101
    (P20, 1.2, F, [(213.8, 106.6), (213.8, 101.6), (228.2, 101.6), (228.2, 105.0)]),      # C211 to C212
    (P20, 1.2, F, [(228.2, 105.0), (232.0, 105.0), (232.0, 115.08), (229.6, 115.08)]),    # to C213
    (P20, 1.2, F, [(232.0, 113.0), (234.0, 113.0), (234.0, 113.4), (260.76, 113.4), (260.76, 114.2)]),  # bus, F403
    (P20, 1.2, F, [(241.86, 113.4), (241.86, 116.0)]),                                    # F401
    (M20, 1.2, B, [(234.2, 126.8), (234.2, 121.2), (249.36, 121.2), (268.26, 118.7)]),  # bottom feed
    (M20, 1.0, F, [(249.36, 121.2), (249.36, 118.5)]),                                    # F402
    (M20, 1.0, F, [(268.26, 118.7), (268.26, 116.2)]),                                    # F404
    (M20, 1.0, F, [(245.5, 108.0), (246.6, 106.2), (253.47, 106.2), (253.47, 109.0), (258.6, 109.0)]),  # C312, C313, TP301
    (M20, 1.0, B, [(258.6, 109.0), (258.6, 119.98)]),
    ("/Outputs/+20V_M", 1.0, F, [(246.14, 118.4), (246.14, 120.6), (242.88, 122.6), (242.88, 126.84)]),
    ("/Outputs/-20V_M", 1.0, F, [(253.64, 118.4), (253.64, 120.8), (250.5, 122.6), (250.5, 126.84)]),
    ("/Outputs/+20V_C1", 1.0, F, [(265.04, 116.2), (265.04, 118.0), (262.18, 119.8), (262.18, 124.54)]),
    ("/Outputs/-20V_C1", 1.0, F, [(272.54, 116.2), (272.54, 118.2), (269.8, 120.0), (269.8, 124.54)]),
    (GND, 1.0, F, [(176.95, 127.1), (178.8, 127.1), (178.8, 131.0), (190.0, 131.0), (191.5, 129.0)]),  # C310 to L301
    # spines through the copper areas: same-net areas do not join each other, and a fill can pinch off
    (VIN, 1.5, F, [(149.5, 113.6), (152.5, 111.7), (155.4, 111.7)]),                     # spine to buck VIN area
    (VIN, 1.5, F, [(149.0, 131.0), (153.5, 131.0), (155.4, 129.5)]),                      # spine to inverter VIN area
    (SRC, 0.8, F, [(121.02, 120.64), (123.1, 120.64), (124.3, 119.36), (125.08, 119.36)]),  # Q101 to Q102 sources
    (SRC, 0.4, F, [(121.02, 119.36), (121.02, 121.91)]),                                   # Q101 source pins 1-3
    (SRC, 0.4, F, [(125.08, 118.09), (125.08, 120.64)]),                                   # Q102 source pins 1-3
    (GND, 0.6, F, [(131.5, 125.3), (130.2, 125.3)]),                                       # C108 to its ground via
    (SW1, 1.0, F, [(163.56, 105.09), (167.6, 105.09), (171.0, 105.09), (172.45, 106.6)]),   # U201 SW, D201, L201
    (SW2, 1.0, F, [(163.56, 124.69), (168.0, 124.69), (169.4, 123.4)]),                    # U301 SW to D301
    (SW2, 1.5, F, [(170.4, 123.2), (171.6, 121.1), (178.8, 121.1), (181.45, 123.6), (181.45, 125.2)]),   # D301 to L301, above the snubber
    (SW2, 0.6, F, [(175.5, 121.1), (175.5, 123.4)]),                                       # snubber tap R308
    (SW1, 0.6, F, [(158.75, 101.4), (158.75, 102.4), (159.4, 103.0), (162.9, 103.0), (163.2, 103.6)]),   # C208 to the switch node, on top
    # MOSFET sources to the gate clamp D102 and R101, on top round C108 (keeps the bottom plane under the filter whole)
    (SRC, 0.6, F, [(121.6, 122.0), (121.6, 123.0), (124.0, 125.4), (127.4, 125.4), (128.85, 126.9), (128.85, 128.5)]),
    (SRC, 0.6, F, [(128.85, 128.5), (128.85, 130.2), (134.6, 130.2), (134.6, 128.5)]),
    # DNP snubbers (decision 189): R to C, and C315 to the -20V_CONV island
    ("Net-(C215-Pad1)", 0.4, F, [(166.15, 101.0), (167.85, 101.0)]),
    (SW1, 0.6, F, [(164.25, 101.0), (164.25, 103.6)]),                                    # R208 into the buck switch-node area
    ("Net-(C315-Pad1)", 0.4, F, [(175.5, 125.35), (177.6, 125.35)]),
    (CONV, 0.4, F, [(177.6, 123.45), (177.6, 122.45)]),
    (VIN, 1.0, F, [(155.4, 100.5), (155.4, 111.7)]),                                       # buck input ceramics
    (VIN, 0.6, F, [(155.4, 106.36), (158.44, 106.36)]),                                    # to U201 VIN
    (VIN, 1.0, F, [(155.4, 121.0), (155.4, 129.8)]),                                       # inverter input ceramics
    (VIN, 0.6, F, [(155.4, 125.97), (158.44, 125.97)]),                                    # to U301 VIN
    # small links the 1.0 mm power class cannot reach: feedback divider top and start-up ramp from the buck output,
    # the inverter's boot capacitor to its switch node (under the IC)
    (OUT1, 0.4, F, [(182.6, 109.6), (180.45, 111.8), (180.45, 114.6)]),
    (OUT1, 0.4, F, [(180.45, 111.8), (170.0, 111.8), (167.0, 114.3), (163.8, 114.3), (163.8, 113.4)]),
    (SW2, 0.5, F, [(157.95, 132.4), (158.6, 131.0), (166.2, 131.0), (166.2, 125.0)]),   # clear of U301 pins 5/6
    # 5 V regulator and LED resistor feed, west of the U101 tab; from the spine above L101 and the VIN_PRE copper
    (VIN, 0.5, F, [(138.4, 117.4), (137.0, 115.0), (130.0, 115.0), (129.2, 114.2), (129.2, 102.72), (127.5, 102.72)]),
    (VIN, 0.5, F, [(125.86, 102.72), (124.6, 101.2), (121.59, 101.2), (121.59, 102.4)]),
    (VIN, 0.3, F, [(154.4, 133.2), (154.9, 133.55), (160.05, 133.55), (160.05, 133.0)]),   # C304, under C308
    # sync clocks from the 74HC14: vias right under their pins (leaving the oscillator's RC a channel), then the
    # bottom layer across the VIN copper in a lane below the EN divider; TP104 joins CLK_B through the bottom
    ("/CLK_A", 0.3, F, [(144.04, 108.2), (144.04, 109.65)]),
    ("/CLK_A", 0.3, F, [(147.6, 101.5), (146.3, 102.4), (146.3, 108.9), (144.04, 109.65)]),   # TP103
    ("/CLK_A", 0.3, B, [(144.04, 109.65), (144.04, 115.9), (161.0, 115.9), (162.1, 114.8), (162.1, 114.45)]),
    ("/CLK_A", 0.3, F, [(162.1, 114.45), (162.1, 115.4)]),
    ("/CLK_B", 0.3, F, [(141.5, 108.2), (141.5, 108.9), (142.77, 108.9), (142.77, 108.2)]),
    ("/CLK_B", 0.3, F, [(142.13, 108.9), (142.13, 109.65)]),
    ("/CLK_B", 0.3, B, [(142.13, 109.65), (142.13, 116.5), (160.9, 116.5), (161.2, 118.6)]),
    ("/CLK_B", 0.3, F, [(161.2, 118.6), (161.9, 118.6)]),
    ("/CLK_B", 0.3, B, [(147.6, 105.0), (147.6, 107.0), (142.8, 107.0), (142.13, 107.6), (142.13, 109.65)]),   # TP104
    # oscillator: U102 pins 2/3 to R105
    ("Net-(R105-Pad2)", 0.3, F, [(138.96, 108.2), (138.96, 108.8), (140.23, 108.8)]),
    ("Net-(R105-Pad2)", 0.3, F, [(140.23, 108.2), (140.23, 110.4), (145.41, 110.4), (145.41, 110.9)]),
    # U201 EN: the VIN copper leaves one track's room left of the pins (taken by RT/CLK), so EN drops to the
    # bottom at the pin and comes up again at its divider
    ("Net-(U201-EN)", 0.3, F, [(157.1, 107.64), (157.8, 107.64)]),
    ("Net-(U201-EN)", 0.3, B, [(157.1, 107.64), (157.1, 113.0), (155.3, 114.0)]),
    ("Net-(U201-EN)", 0.3, F, [(155.3, 114.0), (152.51, 114.0), (152.51, 114.8)]),
    ("Net-(U201-EN)", 0.3, F, [(154.49, 114.0), (154.49, 114.8)]),
    ("Net-(U201-COMP)", 0.3, F, [(157.2, 113.4), (157.2, 114.25)]),                       # R203 to C206 through the bottom
    ("Net-(U201-COMP)", 0.3, B, [(157.2, 114.25), (161.3, 114.0)]),
    ("Net-(U201-COMP)", 0.3, F, [(161.3, 114.0), (161.4, 113.4)]),
    # U301 BOOT: from pin 1 down to C308 through the bottom (the left pins' corridor is the VIN finger's)
    ("Net-(U301-BOOT)", 0.3, F, [(157.8, 124.69), (156.75, 124.0)]),
    ("Net-(U301-BOOT)", 0.3, B, [(156.75, 124.0), (156.75, 131.25), (156.05, 131.25)]),
    # U301 COMP: R303 to the COMP via at C306, under C305 and above the IC's pins
    ("Net-(U301-COMP)", 0.3, F, [(157.6, 122.8), (157.9, 123.7), (161.6, 123.7), (161.6, 123.65)]),
    # -20V_CONV ends of the inverter's dividers and compensation: one via to the island between R304 and C305
    (CONV, 0.4, F, [(160.11, 119.2), (160.0, 119.72), (159.9, 120.25)]),
    ("Net-(U301-BOOT)", 0.3, F, [(156.05, 131.25), (156.05, 131.9)]),
    # PGND ends of the EN and RT dividers: the clock lanes run below them on the bottom, so a via east of C207
    (GND, 0.3, F, [(156.31, 116.0), (156.31, 116.6), (160.1, 116.6), (160.1, 116.0)]),
    (GND, 0.3, F, [(160.1, 116.6), (164.6, 116.6), (165.5, 116.2)]),
    (GND, 0.4, F, [(191.75, 118.8), (195.5, 118.8)]),                                       # C314 to the PGND area
    (GND, 0.4, F, [(191.75, 118.8), (192.6, 117.6), (192.6, 116.5)]),                       # and a via above the island
    # U301 COMP is boxed in by the switch-node copper: a hop through the bottom to C306
    ("Net-(U301-COMP)", 0.3, F, [(164.2, 127.24), (165.2, 127.24)]),
    ("Net-(U301-COMP)", 0.3, B, [(165.2, 127.24), (165.2, 123.65), (161.6, 123.65)]),
    ("Net-(U301-COMP)", 0.3, F, [(161.6, 123.65), (161.6, 123.0)]),
]

# no tracks on the bottom under the hot loops and the input filter, so the plane stays whole where the switching
# currents return (EMI review 2026-10-21); gaps for the planned hops (buck EN, inverter BOOT and COMP); vias allowed
# the inverter's EN, RT/CLK and FB have no top path out from under the IC to their dividers above it, so the area
# under and beside the IC stays open to the router; the band below the IC, where the return current runs, is kept
KEEPOUTS = [
    ("buck loop", [(150.6, 99.6), (170.0, 99.6), (170.0, 110.4), (157.6, 110.4), (157.6, 107.1), (156.6, 107.1),
                   (156.6, 110.4), (150.6, 110.4)]),
    ("inverter loop left", [(150.6, 120.6), (155.5, 120.6), (155.5, 133.7), (150.6, 133.7)]),
    ("inverter loop below", [(157.35, 130.0), (176.5, 130.0), (176.5, 133.7), (157.35, 133.7)]),
    ("inverter loop right", [(165.8, 123.0), (176.5, 123.0), (176.5, 128.0), (165.8, 128.0)]),
    ("input filter", [(126.5, 116.8), (140.0, 116.8), (140.0, 127.2), (126.5, 127.2)]),
]

# vias: (net, x, y); 0.8/0.4 for the feeds, 0.6/0.3 for ground stitching at pads
VIAS = [
    (M20, 234.2, 126.8, 0.8), (M20, 249.36, 121.2, 0.8), (M20, 268.26, 118.7, 0.8),
    (M20, 258.6, 109.0, 0.8),
    (GND, 147.6, 125.35, 0.6), (GND, 147.45, 132.4, 0.6),       # C303, C104 ground pads inside the VIN area
    (GND, 197.0, 107.85, 0.6), (GND, 223.0, 128.05, 0.6), (GND, 224.5, 128.05, 0.6),   # C209, C311
    (GND, 250.53, 110.6, 0.6),                                    # C313
    (GND, 151.55, 101.3, 0.6), (GND, 151.55, 104.9, 0.6), (GND, 151.55, 108.5, 0.6),   # buck input ceramics
    (GND, 167.2, 110.0, 0.6), (GND, 168.2, 110.0, 0.6),          # D201 anode
    (GND, 195.0, 113.6, 0.6), (GND, 197.0, 113.6, 0.6), (GND, 199.0, 113.6, 0.6),      # inverter output return
    (GND, 195.0, 115.6, 0.6), (GND, 197.0, 115.6, 0.6), (GND, 199.0, 115.6, 0.6),
    (CONV, 151.55, 122.0, 0.6), (CONV, 151.55, 125.6, 0.6),      # inverter input ceramics, to the island
    (CONV, 170.4, 131.6, 0.6), (CONV, 175.6, 130.9, 0.6),        # D301 anode, C310
    ("/CLK_A", 144.04, 109.65, 0.6), ("/CLK_A", 162.1, 114.45, 0.6),
    ("/CLK_B", 142.13, 109.65, 0.6), ("/CLK_B", 161.2, 118.6, 0.6), ("/CLK_B", 147.6, 105.0, 0.6),
    ("Net-(U201-EN)", 157.1, 107.64, 0.6), ("Net-(U201-EN)", 155.3, 114.0, 0.6), ("Net-(U201-COMP)", 157.2, 114.25, 0.6),
    ("Net-(U301-BOOT)", 156.75, 124.0, 0.6), (CONV, 160.0, 119.72, 0.6), ("Net-(U301-BOOT)", 156.05, 131.25, 0.6),
    (GND, 165.5, 116.2, 0.6), (GND, 192.6, 116.5, 0.6), (GND, 130.2, 125.3, 0.6),   # C108
    (GND, 169.75, 102.25, 0.6), (CONV, 177.6, 122.45, 0.6),       # snubbers C215, C315 (decision 189)
    ("Net-(U201-COMP)", 161.3, 114.0, 0.6),
    ("Net-(U301-COMP)", 165.2, 127.24, 0.6), ("Net-(U301-COMP)", 161.6, 123.65, 0.6),
]


def apply():
    mm = pcbnew.FromMM
    pt = lambda x, y: pcbnew.VECTOR2I(mm(x + DX), mm(y + DY))
    board = pcbnew.LoadBoard(PCB)
    nets = {n: board.FindNet(n) for n in {z[1] for z in ZONES} | {t[0] for t in TRACKS} | {v[0] for v in VIAS}}
    missing = [n for n, ni in nets.items() if ni is None]
    if missing:
        sys.exit(f"unknown nets: {missing}")
    # build everything first: after a Remove, KiCad's SWIG layer returns untyped objects
    # start from an unrouted board: every track, via and copper zone goes (rule areas stay); autoroute.py adds the
    # planes and pours again
    old = [t for t in board.GetTracks()] + [z for z in board.Zones()
                                            if not z.GetIsRuleArea() or z.GetZoneName().startswith("keepout")]
    add = []
    for name, net, layer, prio, pts in ZONES:
        z = pcbnew.ZONE(board); z.SetZoneName(name); z.SetLayer(layer); z.SetNet(nets[net])
        z.SetAssignedPriority(prio); z.SetLocalClearance(mm(0.2)); z.SetMinThickness(mm(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THT_THERMAL)
        z.SetThermalReliefGap(mm(0.4)); z.SetThermalReliefSpokeWidth(mm(0.6)); z.SetLocked(True)
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        o = z.Outline(); o.NewOutline()
        for x, y in pts:
            o.Append(mm(x + DX), mm(y + DY))
        add.append(z)
    for name, pts in KEEPOUTS:
        z = pcbnew.ZONE(board); z.SetIsRuleArea(True); z.SetZoneName("keepout " + name); z.SetLayer(B)
        z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(False); z.SetDoNotAllowZoneFills(False)
        z.SetDoNotAllowPads(False); z.SetDoNotAllowFootprints(False)
        o = z.Outline(); o.NewOutline()
        for x, y in pts:
            o.Append(mm(x + DX), mm(y + DY))
        add.append(z)
    for net, w, layer, pts in TRACKS:
        for a, b in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(board); t.SetStart(pt(*a)); t.SetEnd(pt(*b)); t.SetWidth(mm(w))
            t.SetLayer(layer); t.SetNet(nets[net]); t.SetLocked(True); add.append(t)
    for net, x, y, d in VIAS:
        v = pcbnew.PCB_VIA(board); v.SetPosition(pt(x, y)); v.SetWidth(mm(d)); v.SetDrill(mm(d / 2))
        v.SetNet(nets[net]); v.SetLocked(True); add.append(v)
    for item in old:
        board.Remove(item)
    for item in add:
        board.Add(item)
    pcbnew.SaveBoard(PCB, board)
    print(f"power stage written: {len(ZONES)} areas, {len(KEEPOUTS)} bottom keep-outs, {sum(len(t[3]) - 1 for t in TRACKS)} track segments, {len(VIAS)} vias")


if __name__ == "__main__":
    apply()
