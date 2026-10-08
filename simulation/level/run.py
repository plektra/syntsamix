#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Channel card Level sheet: fader law and ducking in the control summer (decisions 72, 97, 102).

Control circuit as drawn (hardware/channel-card/scripts/level_build.py): fader wiper (-15 V at
the bottom, 0 V at the top) -> U204A follower (OPA2171) -> VB; R207 113k from VB and R208 453k
from +15 V into the summer's virtual earth VSUM; two superdiode breakpoints on the TL072 (U205)
with 100k from VB, 221k / 124k from +15 V and 63k4 / 8k66 into VSUM; DUCK_V (SC_ENV through
the DG413) into VSUM through R217 30k1; mute through R216 33k2 from -15 V. Summer U204B
(OPA2171), + input on AGND, 10k || 1 uF feedback, output VC to the SSI2162 (-33 mV/dB: a
positive VC lowers the gain).

The OPA2171 model swings to about 0.45 V from the rails (datasheet: 0.35 V over temperature
at 10 kOhm) and has no common-mode limit at V-
(TI SBOS516H: input to (V-) - 0.1 V, rail-to-rail output). The TL072 model is the one in
simulation/compressor. Rails are +-15.0 V, the values the law was designed with.

Requires ngspice on PATH. Standard library only.

Usage:  python3 simulation/level/run.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "compressor"))
from run import OPAMP, MODELS, run  # noqa: E402

MV_PER_DB = 0.033

RRO = """
.subckt rro inp inn out
* OPA2171-like: rail-to-rail output within about 0.45 V of +-15 V, no input limit at V-
B1 0 n1 I = max(min(1e-3*(V(inp)-V(inn)), 0.08e-3), -0.08e-3)
R1 n1 0 1e9
C1 n1 0 53p
D1 n1 hi DCL
D2 lo n1 DCL
Vhi hi 0 14.1
Vlo lo 0 -14.1
E1 o 0 n1 0 1
Ro o out 50
.model DCL D(IS=1e-12 RS=1)
.ends
"""

LAW = [(1.00, 10), (0.75, 0), (0.53, -10), (0.42, -20), (0.19, -40), (0.14, -60), (0.0, -113)]


def circuit(wiper, duck, mute="0", extra=""):
    return f"""* level control
Vcc vcc 0 15
Vee vee 0 -15
Vw w 0 {wiper}
Vd dv 0 {duck}
Vm mv 0 {mute}
X1 w vb vb rro
R207 vb vsum 113k
R208 vcc vsum 453k
R209 vb s1 100k
R210 vcc s1 221k
X2 s1 k1 o1 opamp
D201 k1 o1 D1N4148
R211 k1 vsum 63.4k
R212 vb s2 100k
R213 vcc s2 124k
X3 s2 k2 o2 opamp
D202 k2 o2 D1N4148
R214 k2 vsum 8.66k
R217 dv vsum 30.1k
R216 mv vsum 33.2k
X4 0 vsum vc rro
R215 vsum vc 10k
C224 vsum vc 1u
{extra}{OPAMP}{RRO}{MODELS}.end
"""


OP = ".control\nop\nlet vcx=v(vc)\nlet vbx=v(vb)\nprint vcx\nprint vbx\n.endc\n"


def gain_db(vc):
    return -vc / MV_PER_DB


def law():
    """Static law: fader position (0 = bottom) -> gain, and the ducking step at -1 V SC_ENV."""
    rows = []
    for x in [p for p, _ in LAW] + [0.15, 0.50]:
        vw = -15.0 * (1 - x)
        base = run(circuit(vw, 0, extra=OP))
        duck = run(circuit(vw, -1, extra=OP))
        rows.append((x, base["vbx"], gain_db(base["vcx"]), gain_db(duck["vcx"]) - gain_db(base["vcx"])))
    return sorted(set(rows), reverse=True)


def attack():
    """SC_ENV steps from 0 to -4 V (40 dB) with the fader at 75 % (0 dB)."""
    net = circuit(-3.75, "PWL(0 0 1m 0 1.001m -4)", extra="""
.tran 20u 80m
.control
run
let tgt=v(vc)[0]+0.9*(v(vc)[length(v(vc))-1]-v(vc)[0])
meas tran t90 WHEN v(vc)=tgt RISE=1
meas tran v0 FIND v(vc) AT=0.9m
meas tran vf FIND v(vc) AT=79m
.endc
""")
    return run(net)


def main():
    out = []
    out.append("Fader law (OPA2171 buffer and summer, TL072 superdiodes)")
    out.append("  position   VB (V)   gain (dB)   design (dB)   ducking at SC_ENV -1 V (dB)")
    design = dict(LAW)
    for x, vb, g, d in law():
        ref = f"{design[x]:>7}" if x in design else "      -"
        out.append(f"  {x*100:5.0f} %   {vb:7.2f}   {g:8.1f}   {ref}       {d:6.2f}")
    a = attack()
    t90 = a.get("t90", float("nan")) - 1.001e-3
    out.append("")
    out.append("Ducking attack, SC_ENV 0 -> -4 V at fader 75 %")
    out.append(f"  VC {a['v0']:.3f} V -> {a['vf']:.3f} V ({gain_db(a['vf']) - gain_db(a['v0']):.1f} dB); 90 % after {t90*1e3:.1f} ms")
    text = "\n".join(out)
    print(text)
    (Path(__file__).resolve().parent / "results.txt").write_text(text + "\n")


if __name__ == "__main__":
    main()
