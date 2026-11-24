#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Sidechain sheet simulations (master card): sidechain LPF range, the trigger-style ducker, THRESHOLD range and ducking LED.

LPF: unity-gain Sallen-Key, 22 nF / 47 nF, 10 kOhm + 100 kOhm dual linear (B) pot per side (decision 138).
Ducker: window comparator (TL072s) against +-THRESHOLD, two DG413 NO switches charge
2.2 uF from DEPTH (0 to -4 V) through 470 Ohm; DECAY (500 kOhm log + 22 kOhm) discharges it; a follower
with its feedback taken after the 100 Ohm drives SC_ENV (-1 V = 10 dB of ducking, decision 97) into
18 loads of 30k (1.67 kOhm, decision 153); a BAT54 clamps SC_ENV to AGND. Uses the TL072-like model of simulation/compressor.

Requires ngspice on PATH. Standard library only.

Usage:  python3 simulation/sidechain/run.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "compressor"))
from run import OPAMP, MODELS, run  # noqa: E402

DBU = 0.7746


def lpf(rpot):
    net = f"""* sidechain LPF
Vin src 0 DC 0 AC 1
R1 src a {10e3 + rpot:g}
R2 a b {10e3 + rpot:g}
C1 a out 47n
C2 b 0 22n
X1 b out out opamp
.save v(out)
.ac dec 200 5 5k
.measure ac fc WHEN vm(out)=0.70795 FALL=1
.measure ac pk MAX vm(out)
{OPAMP}{MODELS}.end
"""
    return run(net)


def ducker(src, tstop, thr=0.6, depth=4.0, decay=0.0, extra=""):
    """thr: threshold (V peak), depth: DEPTH voltage, decay: DECAY pot resistance (0..500k)."""
    net = f"""* ducker
Vcc vcc 0 15
Vee vee 0 -15
{src}
Vthr tp 0 {thr}
Vthn tn 0 {-thr}
Vdep dep 0 {-depth}
X1 sc tp c1 opamp
X2 tn sc c2 opamp
S1 dep e c1 0 SWNO
S2 dep e c2 0 SWNO
.model SWNO SW(VT=1.6 RON=40 ROFF=1e12)
R1 e h 470
C1 h 0 2.2u
R2 h d 22k
R3 d 0 {decay + 1:g}
X3 h scenv env opamp
Rout env scenv 100
Rload scenv 0 1.667k
Dcl scenv 0 BAT54
.model BAT54 D(IS=2e-7 N=1.05 RS=2 CJO=10p BV=30)
.tran 50u {tstop} 0 50u
{extra}
{OPAMP}{MODELS}.end
"""
    return run(net)


def led(env, bleed=22e3, is_=1e-20, n=2.2, tc=27):
    """Ducking LED current (A) at SC_ENV = env (decision 199): NPN follower, PNP current source, bleed across the LED."""
    net = f"""* ducking LED
Vm vee 0 -15.1
Vs sc 0 {env:g}
Qn 0 sc en QN
Rn en vee 47k
Qp c en ep QP
Re 0 ep 2k
Vl c cl 0
Dl cl vee LEDG
Rb c vee {bleed:g}
.model QN NPN(IS=6.7f BF=200 VAF=74)
.model QP PNP(IS=1.4f BF=180 VAF=18.7 BR=5)
.model LEDG D(IS={is_:g} N={n:g} RS=20)
.temp {tc}
.tran 1u 10u
.measure tran il AVG i(Vl) FROM=5u TO=10u
.measure tran im AVG i(Vm) FROM=5u TO=10u
.end
"""
    return run(net)


def threshold(x, top=75e3, bot=1.5e3, pot=10e3, load=100e3):
    """THRESHOLD wiper voltage at rotation x of a linear pot (R514, R515, loaded by R516 into a virtual earth)."""
    rl, rh = bot + x * pot, top + (1 - x) * pot
    rl = rl * load / (rl + load)
    return 15.1 * rl / (rl + rh)


def main():
    print("Sidechain LPF (Sallen-Key, 22n/47n, 10k + 100k pot):")
    # B100K linear dual (decision 138): rheostat wiper to CW end, so the resistance is 100k x (1 - rotation)
    for name, r in (("CW (pot 0)", 0.0), ("75 % (25k)", 25e3), ("middle (50k)", 50e3), ("25 % (75k)", 75e3),
                    ("CCW (pot 100k)", 100e3), ("CCW, track -20 % (80k)", 80e3), ("CCW, track +20 % (120k)", 120e3)):
        v = lpf(r)
        print(f"  {name}: -3 dB at {v['fc']:.0f} Hz, peak {20*math.log10(v['pk']):+.2f} dB")

    print("\nDucker (THRESHOLD 0.6 V peak, DEPTH -4 V = 40 dB, 100 Hz kick burst of 30 ms at 0.1 s, load 18 x 30k = 1.67 kOhm)")
    a = DBU * math.sqrt(2) * 10 ** (4 / 20)
    src = f"Bsc sc 0 V = (time > 0.1 && time < 0.13 ? {a:.4g} : 0) * sin(2*3.14159265*100*(time-0.1))"
    for decay, name in ((0.0, "DECAY CCW"), (500e3, "DECAY CW")):
        tstop = 0.6 if decay == 0 else 4.0
        extra = """
.measure tran vpk MIN v(scenv)
.measure tran t90 WHEN v(scenv)=-3.5 FALL=1
.measure tran thalf WHEN v(scenv)=-1.95 RISE=1 FROM=0.13
.measure tran vmax MAX v(scenv)
"""
        v = ducker(src, tstop, decay=decay, extra=extra)
        print(f"  {name}: peak {v['vpk']:.2f} V ({-v['vpk']*10:.0f} dB), 90 % after {(v['t90']-0.1)*1e3:.1f} ms,"
              f" half (20 dB) recovered {(v['thalf']-0.13)*1e3:.0f} ms after the burst, most positive {v['vmax']*1e3:.1f} mV")
    extra = ".measure tran vpk MIN v(scenv)\n"
    lo = 0.5 * 10 ** (-3 / 20)
    v = ducker(f"Bsc sc 0 V = {lo:.4g} * sin(2*3.14159265*100*time)", 0.3, extra=extra)
    print(f"  signal 3 dB below threshold: SC_ENV peak {v['vpk']*1e3:.1f} mV (no trigger)")
    v = ducker("Vsc sc 0 PWL(0 0 0.1 0 0.1001 10 0.2 10 0.2001 0)", 0.6, extra=extra)
    print(f"  Eurorack gate 10 V for 100 ms: SC_ENV peak {v['vpk']:.2f} V")

    print("\nTHRESHOLD (B10K, R514 75k, R515 1k5, loaded by R516 100k, decision 199)")
    print("  " + ", ".join(f"{int(100 * x)} %: {threshold(x):.2f} V" for x in (0, 0.25, 0.5, 0.75, 1)))

    print("\nDucking LED current against SC_ENV (R529 2k, R528 47k; decision 199)")
    for name, kw in (("22k across the LED, VF about 2.3 V", {}), ("22k, VF about 2.8 V (KT-0805G mid)", dict(is_=2e-24)),
                     ("no bleed, VF about 2.3 V", dict(bleed=1e9)), ("22k, 57 C", dict(tc=57))):
        r = [(db, led(-db / 10, **kw)) for db in (0, 1, 2, 3, 5, 10, 20, 40)]
        print(f"  {name}: " + ", ".join(f"{db} dB {1e6 * v['il']:.0f} uA" for db, v in r) + f"; -15 V load at 40 dB {1e3 * abs(r[-1][1]['im']):.2f} mA")


if __name__ == "__main__":
    main()
