#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Compressor detector and gain computer simulations (master card, Compressor sheet).

Transistor-level model of the side chain: precision full-wave rectifier, log converter
on the AS3046 matched pair (Q1 signal, Q2 diode-connected reference), gain stage with
the ERA-V33 temperature-compensating resistor, peak hold with 1 ms attack and a
current-mirror release (Q3/Q4), threshold and 4:1 ratio (precision half-wave), makeup
and the click-free on/off. Output VC drives the SSI2162 (+33 mV per dB of attenuation).
The VCA itself is not modelled: gain reduction is read from VC.

Requires ngspice on PATH. Standard library only.

Usage:  python3 simulation/compressor/run.py
"""

import math
import re
import subprocess
import tempfile
from pathlib import Path

DBU = 0.7746
MV_PER_DB = 0.033          # SSI2162 control sensitivity

OPAMP = """
.subckt opamp inp inn out
* TL072-like: 200k DC gain, 3 MHz GBW, 13 V/us slew, swings to about +-13.5 V
B1 0 n1 I = max(min(1e-3*(V(inp)-V(inn)), 0.69e-3), -0.69e-3)
R1 n1 0 2e8
C1 n1 0 53p
D1 n1 hi DCL
D2 lo n1 DCL
Vhi hi 0 13
Vlo lo 0 -13
E1 n2 0 n1 0 1
R2 n2 n3 1k
C2 n3 0 15p
E2 o 0 n3 0 1
Ro o out 50
.model DCL D(IS=1e-12 RS=1)
.ends
"""

MODELS = """
.model QN NPN(IS=10f BF=145 VAF=100 CJE=0.6p CJC=0.6p TF=0.4n)
.model D1N4148 D(IS=2.52n RS=0.568 N=1.752 CJO=4p TT=20n BV=100)
"""


def netlist(src, rel=1.0, amount=0.0, on=1, half=False, temp=25.0, analysis="", ratt="470", rrel="2.2Meg", rbot="6.2k", rpot=100e3):
    """rel: release pot wiper position from the -15 V end (1 = CCW, fastest; 0 = CW, slowest).
    amount: Amount pot position (0..1)."""
    ctl = on if isinstance(on, str) else ("1" if on else "0")   # on/off control: 0/1 or a PWL source
    lines = [
        "* compressor side chain",
        f".options TEMP={temp} TNOM=25",
        "Vcc vcc 0 15", "Vee vee 0 -15",
        src,
        # A1: inverting half-wave (hw = -v for v < 0)
        "R401 sc n1 10k", "X1 0 n1 o1 opamp", "D401 o1 hw D1N4148", "R402 hw n1 10k", "D402 n1 o1 D1N4148",
        # log node: |v|/20k + floor
        "R403 sc ln 20k", "R404 hw ln 10k", "R405 vcc ln 10Meg",
        "Q1 ln 0 e QN", "X2 0 ln o2 opamp", "R406 o2 e 2.2k", "C401 o2 ln 220p", "D403 e 0 D1N4148",
        # reference: Q2 diode-connected, buffered
        "R407 vcc b2 560k", "Q2 b2 b2 e QN", "X3 b2 vl vl opamp",
        # gain -11 with ERA-V33 (+3300 ppm/K)
        "R408 vl n4 1k tc1=0.0033", "R409 n4 va 11k", "X4 0 n4 va opamp",
        # peak hold
        f"X5 va k o5 opamp", "D404 o5 k D1N4148", f"R410 k ch {ratt}", "C402 ch 0 1u", "X6 ch vd vd opamp",
        # release: Q4 diode, Q3 sinks from the hold capacitor
        "Q4 m m vee QN", "Q3 ch m vee QN", f"R411 w m {rrel}",
        f"Rp1 0 w {rpot*(1-rel)+1:g}", f"Rp2 w p3 {rpot*rel+1:g}", f"R412 p3 vee {rbot}",
        # Amount pot (10k lin, top at about +1 V); on/off ramps it through S1 (NO) / S2 (NC) and C403
        "R413 vcc top 140k", f"Rpa1 top wa {10e3*(1-amount)+1:g}", f"Rpa2 wa 0 {10e3*amount+1:g}",
        "S1 wa as ctl 0 SWNO", "R414 as ar 100k", "C403 ar 0 220n", "R415 ar ad 100k", "S2 ad 0 ctl 0 SWNC",
        "X10 ar vamt vamt opamp",
        # A7: threshold and 4:1 ratio (grn = -0.75 x excess, 0 below threshold).
        # Off: S3 (NC) slowly raises the threshold about 11 dB (after Amount has ramped away); on: S4 (NO) resets it at once
        "R416 vd g 100k", "R417 vamt g 100k", "R418 vee g 2.2Meg",
        "S3 vee xs ctl 0 SWNC", "R419 xs x 3.3Meg", "C404 x 0 220n", "R420 x g 1Meg", "S4 x 0 ctl 0 SWNO",
        "X7 0 g o7 opamp", "D405 grn o7 D1N4148", "R421 grn g 75k", "D406 o7 g D1N4148",
        # A8: VC = gain reduction - makeup (0.735 x Amount), light smoothing
        "R422 grn s 100k", "R423 vamt y 68k", "R424 y s 68k",
        "R425 s vc 100k", "C405 s vc 2.2n", "X8 0 s vc opamp",
        # A9: GR for the LEDs (positive)
        "R427 grn n9 100k", "R428 n9 grp 100k", "X9 0 n9 grp opamp",
        f"Von ctl 0 {ctl}",
        ".model SWNO SW(VT=0.5 RON=25 ROFF=1e12)", ".model SWNC SW(VT=0.5 RON=1e12 ROFF=25)",
    ]
    if half:
        lines.append("R426 y 0 33k")
    return "\n".join(lines) + "\n" + OPAMP + MODELS + analysis + "\n.end\n"


def run(net):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "c.cir"
        p.write_text(net)
        r = subprocess.run(["ngspice", "-b", str(p)], capture_output=True, text=True)
        out = r.stdout + r.stderr
    vals = {}
    for m in re.finditer(r"^(\w+)\s*=\s*([-+0-9.eE]+)", out, re.M):
        vals[m.group(1).lower()] = float(m.group(2))
    if not vals:
        raise RuntimeError(out[-3000:])
    return vals


def sine(dbu, f=100):
    return f"Vin sc 0 SIN(0 {DBU*math.sqrt(2)*10**(dbu/20):.6g} {f})"


def static(dbu, amount, temp=25.0, half=False):
    an = """
.tran 20u 0.6 0 20u
.measure tran vcavg AVG v(vc) FROM=0.5 TO=0.6
.measure tran vcpp PP v(vc) FROM=0.5 TO=0.6
.measure tran grp AVG v(grp) FROM=0.5 TO=0.6
.measure tran vd AVG v(vd) FROM=0.5 TO=0.6
"""
    v = run(netlist(sine(dbu), rel=0.1, amount=amount, temp=temp, half=half, analysis=an))
    return v


def main():
    print("Static curve (100 Hz sine, release at mid, 25 C). Gain = -VC / 33 mV")
    print("Threshold at Amount 0 is about +14.6 dBu (sine peak); Amount 1 lowers it 30 dB, makeup 0.735 x drop")
    print(f"{'level dBu':>9} | " + " | ".join(f"Amt {a:.1f}: gain dB (ideal)" for a in (0, 0.5, 1.0)))
    for dbu in (-30, -20, -16, -10, -4, 0, 4, 8, 14, 18, 20):
        cells = []
        for a in (0.0, 0.5, 1.0):
            v = static(dbu, a)
            g = -v["vcavg"] / MV_PER_DB
            thr = 14.6 - 30 * a * 0.99          # Amount pot top is about 0.99 V = 30 dB
            ideal = 0.735 * 30 * a * 0.99 - 0.75 * max(0.0, dbu - thr)
            cells.append(f"{g:+6.1f} ({ideal:+6.1f}) ripple {v['vcpp']*1e3/33:4.2f} dB")
        print(f"{dbu:>9} | " + " | ".join(cells))

    print("\nTemperature drift at Amount 0.5, +8 dBu (gain dB):")
    for t in (15, 25, 45):
        v = static(8, 0.5, temp=t)
        print(f"  {t} C: {-v['vcavg']/MV_PER_DB:+.2f} dB")

    print("\nHalf makeup (R426 fitted), Amount 1, -30 dBu (below threshold): "
          f"{-static(-30, 1.0, half=True)['vcavg']/MV_PER_DB:+.1f} dB")

    print("\nAttack: -20 dBu to +14 dBu step at 0.2 s, Amount 1 (gain reduction 63 % and 90 % times)")
    lo, hi = DBU*math.sqrt(2)*10**(-20/20), DBU*math.sqrt(2)*10**(14/20)
    srcs = (f"Bin sc 0 V = (time > 0.2 ? {hi:.5g} : {lo:.5g}) * sin(2*3.14159265*1000*time)")
    an = """
.tran 5u 0.3 0 5u
.measure tran v0 FIND v(vc) AT=0.199
.measure tran v1 FIND v(vc) AT=0.29
"""
    v = run(netlist(srcs, rel=0.1, amount=1.0, analysis=an))
    v0, v1 = v["v0"], v["v1"]
    an2 = f"""
.tran 5u 0.3 0 5u
.measure tran t63 WHEN v(vc)={v0 + 0.63*(v1-v0):.5g} RISE=1 FROM=0.2
.measure tran t90 WHEN v(vc)={v0 + 0.90*(v1-v0):.5g} RISE=1 FROM=0.2
"""
    v = run(netlist(srcs, rel=0.1, amount=1.0, analysis=an2))
    print(f"  GR {(v1-v0)/MV_PER_DB:.1f} dB; 63 % at {(v['t63']-0.2)*1e3:.2f} ms, 90 % at {(v['t90']-0.2)*1e3:.2f} ms")

    print("\nRelease: +14 dBu burst ends at 0.3 s, Amount 1 (recovery rate over the first 10 dB)")
    srcs = f"Bin sc 0 V = (time < 0.3 ? {hi:.5g} : {lo:.5g}) * sin(2*3.14159265*1000*time)"
    for rel, name in ((1.0, "CCW (fast)"), (0.1, "middle"), (0.0, "CW (slow)")):
        tstop = 3.5 if rel < 0.5 else 0.8
        an = f"""
.tran 20u {tstop} 0 20u
.measure tran v0 FIND v(vc) AT=0.299
"""
        v0 = run(netlist(srcs, rel=rel, amount=1.0, analysis=an))["v0"]
        an = f"""
.tran 20u {tstop} 0 20u
.measure tran t10 WHEN v(vc)={v0 - 10*0.75*MV_PER_DB:.5g} FALL=1 FROM=0.3
"""
        v = run(netlist(srcs, rel=rel, amount=1.0, analysis=an))
        t = v["t10"] - 0.3
        print(f"  {name}: 7.5 dB less gain reduction (10 dB of detector level) after {t*1e3:.0f} ms")

    print("\nOn/off ramp: switched on at 0.1 s and off at 0.4 s, Amount 1, 1 kHz (gain dB)")
    an = """
.tran 20u 1.2 0 20u
.measure tran voff FIND v(vc) AT=0.099
.measure tran von FIND v(vc) AT=0.39
.measure tran vend FIND v(vc) AT=1.19
.measure tran vmax MAX v(vc) FROM=0.1 TO=1.2
.measure tran vmin MIN v(vc) FROM=0.1 TO=1.2
"""
    for dbu in (-10, 8, 18):
        v = run(netlist(sine(dbu, 1000), rel=0.1, amount=1.0, on="PWL(0 0 0.1 0 0.1001 1 0.4 1 0.4001 0)", analysis=an))
        g = {k: -x / MV_PER_DB for k, x in v.items()}
        print(f"  {dbu:+} dBu: off {g['voff']:+.1f}, on {g['von']:+.1f}, off again {g['vend']:+.1f};"
              f" during the ramps {g['vmax']:+.1f} to {g['vmin']:+.1f}")

    print("\nLog converter stability: 10 kHz sine at -30 and +18 dBu, VL ripple above the signal (should be smooth)")
    for dbu in (-30, 18):
        an = """
.tran 0.2u 4m 0 0.2u
.measure tran vlpp PP v(vl) FROM=3m TO=4m
.measure tran o2pp PP v(o2) FROM=3m TO=4m
"""
        v = run(netlist(sine(dbu, 10000), amount=0.0, analysis=an))
        print(f"  {dbu:+} dBu: VL p-p {v['vlpp']*1e3:.1f} mV, log amp output p-p {v['o2pp']:.2f} V")


if __name__ == "__main__":
    main()
