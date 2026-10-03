#!/usr/bin/env python3
"""Filter gain-structure simulations for the SSI2144 channel filter.

Generates ngspice netlists from the behavioural ladder model in ladder.lib,
runs them in batch mode and prints the result tables used in README.md.
Requires ngspice on PATH. Standard library only.

Usage:  python3 simulation/filter/run.py
"""

import math
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIB = HERE / "ladder.lib"

DBU_REF = 0.7746  # 0 dBu in V rms

# Gain structures: V peak at the chip input for a +4 dBu internal sine
NOMINAL_DBU = 4.0
STRUCTURES = {
    # confirmed "hot" drive: +4 dBu -> +-20 mV (datasheet nominal)
    "hot": 0.020,
    # alternative "clean": +20 dBu (internal max) -> +-50 mV (clip point)
    "clean": 0.050 / (DBU_REF * math.sqrt(2) * 10 ** (20 / 20))
    * (DBU_REF * math.sqrt(2) * 10 ** (NOMINAL_DBU / 20)),
}


def dbu_to_vpeak(dbu):
    return DBU_REF * math.sqrt(2) * 10 ** (dbu / 20)


def run_ngspice(netlist):
    with tempfile.TemporaryDirectory() as tmp:
        cir = Path(tmp) / "sim.cir"
        cir.write_text(netlist)
        res = subprocess.run(
            ["ngspice", "-b", str(cir)], capture_output=True, text=True, cwd=tmp
        )
        return res.stdout + res.stderr


def thd(dbu, structure, fc, k, f0=100.0):
    """THD (%) of the ladder for a sine at internal level `dbu`."""
    scale = STRUCTURES[structure] / dbu_to_vpeak(NOMINAL_DBU)
    amp = dbu_to_vpeak(dbu) * scale
    period = 1 / f0
    netlist = f"""* thd
.include {LIB}
Vin in 0 SIN(0 {amp} {f0})
X1 in out ladder4 fc={fc} k={k}
.tran {period/2000} {period*12} {period*6} {period/2000}
.four {f0} V(out)
.options numdgt=7
.end
"""
    out = run_ngspice(netlist)
    m = re.search(r"THD:\s*([0-9.eE+-]+)\s*%", out)
    if not m:
        raise RuntimeError(out[-2000:])
    return float(m.group(1))


def ac_response(k_values, fc=1000.0):
    """Small-signal response: (gain at 20 Hz dB, peak gain dB, peak freq Hz) per k."""
    results = {}
    for k in k_values:
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "ac.txt"
            netlist = f"""* ac
.include {LIB}
Vin in 0 DC 0 AC 1
X1 in out ladder4 fc={fc} k={k}
.ac dec 400 10 100k
.control
run
wrdata {data} db(v(out))
.endc
.end
"""
            run_ngspice(netlist)
            rows = [
                tuple(float(x) for x in line.split()[:2])
                for line in data.read_text().splitlines()
                if line.strip()
            ]
        g20 = min(rows, key=lambda r: abs(r[0] - 20))[1]
        fpk, gpk = max(rows, key=lambda r: r[1])
        results[k] = {"dc_gain": g20, "pk_gain": gpk, "pk_freq": fpk}
    return results


def main():
    print("== Passband loss vs resonance (fc = 1 kHz, small signal) ==")
    print("k is the resonance loop gain; 4 = self-oscillation.")
    print("Q current at k: about k x 100 uA (datasheet: oscillation at 350-450 uA).")
    k_values = [0, 1, 2, 3, 3.43]
    ac = ac_response(k_values)
    print(f"{'k':>5} {'20 Hz dB':>9} {'peak dB':>8} {'peak Hz':>8}"
          f" {'half-comp 20Hz':>15} {'half-comp peak':>15}")
    for k in k_values:
        r = ac[k]
        half = 10 * math.log10(1 + k)  # +half of the dB loss, i.e. sqrt(1+k)
        pk_freq = f"{r['pk_freq']:.0f}" if r["pk_gain"] > r["dc_gain"] + 0.1 else "-"
        print(f"{k:>5} {r['dc_gain']:>9.2f} {r['pk_gain']:>8.2f} {pk_freq:>8}"
              f" {r['dc_gain'] + half:>15.2f} {r['pk_gain'] + half:>15.2f}")

    print()
    print("== THD vs internal level, filter open (fc = 20 kHz, k = 0), 100 Hz tone ==")
    levels = [-10, -6, 0, 4, 8, 12, 16, 20]
    print(f"{'dBu':>5} {'hot THD %':>10} {'clean THD %':>12}")
    for lv in levels:
        print(f"{lv:>5} {thd(lv, 'hot', 20000, 0):>10.3f} {thd(lv, 'clean', 20000, 0):>12.3f}")

    print()
    print("== THD vs internal level, cutoff lowered (fc = 1 kHz, k = 0), 100 Hz tone ==")
    print(f"{'dBu':>5} {'hot THD %':>10} {'clean THD %':>12}")
    for lv in levels:
        print(f"{lv:>5} {thd(lv, 'hot', 1000, 0):>10.3f} {thd(lv, 'clean', 1000, 0):>12.3f}")

    print()
    print("== THD at +4 dBu with resonance (fc = 1 kHz, 100 Hz tone, hot drive) ==")
    for k in [0, 1, 2, 3]:
        print(f"k = {k}: THD {thd(4, 'hot', 1000, k):.3f} %")


if __name__ == "__main__":
    main()
