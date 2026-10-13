#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0

"""Channel cutoff summer U107A with the back-to-back zener clamp (decision 165).

DC sweep of the total cutoff control (pot plus CV, in CV volts at 1 V/oct) through the
inverting summer (100k input, V/oct feedback trimmed to 182k / 192k / 202k for a
-18 / -19 / -20 mV/oct SSI2144) with two zeners back to back across the feedback, then
the 100k / 1k divider into the SSI2144 frequency pin and the 470k offset trim (set to
+-10 mV at the pin for the worst case). For each zener type at both ends of its
tolerance it reports:
  - the largest error inside the pot's range (+-5.03 V: the pot across +-15.1 V through
    300k), in octaves, against the unclamped line;
  - the clamp level of FCV;
  - the extreme pin voltage, to compare with the SSI2144 datasheet (Rev 3.0, p2/p5):
    specified range -120 to +150 mV, dropout above about +175 mV, recovery at about
    +135 mV.

The zener knee below the datasheet's 0.5 mA curves is not specified: NBV (breakdown
emission coefficient) is swept over 2, 4 and 6 as a soft-to-softer knee assumption.
Leakage: 70 Mohm across each zener (0.1 uA at 7-8 V, the datasheet maximum).

Requires ngspice on PATH. Standard library only.

Usage:  python3 simulation/cutoff/run.py
"""

import subprocess
import tempfile
from pathlib import Path

OPAMP = """
.subckt opamp inp inn out
* TL072-like (as simulation/compressor/run.py): 200k DC gain, swings to about +-13.5 V
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

# BZT52 series, hongjiacheng datasheet Rev 2.1: VZ min / max at 5 mA
ZENERS = {"C9V1": (8.65, 9.56), "C10": (9.50, 10.50), "C11": (10.45, 11.55), "C12": (11.40, 12.60)}
VPOT = 15.1 / 3          # pot full scale in CV volts (R181 + R188 = 300k against R182 100k)
VTRIM = 4.75             # 470k from the trim wiper: about +-10 mV at the pin


def netlist(vz, nbv, rf, vtrim, clamp=True):
    z = ""
    if clamp:   # D184 cathode on the summing node, D185 cathode on FCV, anodes joined
        z = f"""Dz1 m s ZD
Dz2 m fcv ZD
Rlk1 s m 70Meg
Rlk2 fcv m 70Meg
.model ZD D(IS=1e-14 N=1 RS=10 BV={vz} IBV=5m NBV={nbv})"""
    return f"""* cutoff summer with clamp
Vt vt 0 0
Rin vt s 100k
Rf s fcv {rf}
C181 s fcv 22p
X1 0 s fcv opamp
{z}
R110 fcv pin 100k
R108 pin 0 1k
Vtr tr 0 {vtrim}
R109 tr pin 470k
{OPAMP}
.dc Vt -17 17 0.05
.control
run
wrdata out.txt v(fcv) v(pin)
.endc
.end
"""


def sim(**k):
    with tempfile.TemporaryDirectory() as d:
        Path(d, "c.cir").write_text(netlist(**k))
        subprocess.run(["ngspice", "-b", "c.cir"], cwd=d, capture_output=True, check=True)
        rows = [list(map(float, l.split())) for l in Path(d, "out.txt").read_text().splitlines() if l.strip()]
    return [(r[0], r[1], r[3]) for r in rows]   # total CV, FCV, pin


def main():
    out = [f"Cutoff summer clamp (decision 165): pot range +-{VPOT:.2f} V CV; trim +-10 mV at the pin for the extremes",
           "Columns: zener, tolerance end, V/oct feedback, worst error inside the pot range (oct),",
           "FCV clamp (V), pin extremes (mV). SSI2144: -120..+150 mV specified, dropout > ~+175 mV, recovery ~+135 mV."]
    for nbv in (2, 4, 6):
        out.append(f"\nknee NBV = {nbv}")
        for name, (lo, hi) in ZENERS.items():
            for tol, vz in (("min", lo), ("max", hi)):
                for rf in (182e3, 192e3, 202e3):
                    s_oct = rf / 100e3 / 101   # pin volts per CV volt (= the chip's V/oct after trimming)
                    ref = {round(v, 3): p for v, _, p in sim(vz=vz, nbv=nbv, rf=rf, vtrim=0, clamp=False)}
                    base = sim(vz=vz, nbv=nbv, rf=rf, vtrim=0)
                    err = max(abs(p - ref[round(v, 3)]) / s_oct for v, _, p in base if abs(v) <= VPOT + 1e-9)
                    fmax = max(f for _, f, _ in base)
                    pmax = max(p for _, _, p in sim(vz=vz, nbv=nbv, rf=rf, vtrim=VTRIM))
                    pmin = min(p for _, _, p in sim(vz=vz, nbv=nbv, rf=rf, vtrim=-VTRIM))
                    out.append(f"{name:5} {tol}  {rf/1e3:3.0f}k  err {err:5.3f} oct  FCV +-{fmax:5.2f} V  pin {pmax*1e3:+6.1f} / {pmin*1e3:+6.1f} mV")
    b = sim(vz=11, nbv=4, rf=192e3, vtrim=0, clamp=False)
    out.append(f"\nno clamp (192k): FCV {max(x[1] for x in b):+.2f} / {min(x[1] for x in b):+.2f} V, "
               f"pin {max(x[2] for x in b)*1e3:+.1f} / {min(x[2] for x in b)*1e3:+.1f} mV before the trim")
    print("\n".join(out))


if __name__ == "__main__":
    main()
