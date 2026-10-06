# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""System supply budget (decision 96): runs both card budget scripts and adds them up.

Typical and worst case per rail for N channel cards plus the master, and the sizing figure
for the shared parts (DC-DC, ribbon pins at the start of a chain): IC quiescent current at
typical x 1.5, use-dependent loads at their maximum.
Usage: python3 tools/system_power_budget.py [raw rail, default 20]
"""
import re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
RAW=sys.argv[1] if len(sys.argv)>1 else "20"
def run(board):
    out=subprocess.run([sys.executable,str(ROOT/"hardware"/board/"scripts"/"power_budget.py"),RAW],
                       capture_output=True,text=True,check=True).stdout
    get=lambda k: tuple(float(x) for x in re.search(rf"^{k}: \+15 V (\d+) mA, -15 V (\d+) mA",out,re.M).groups())
    return {k:get(k) for k in ("typ","max","sizing")}
ch,ms=run("channel-card"),run("master")
for k in ("typ","max","sizing"):
    print(f"channel {k}: +15 V {ch[k][0]:.0f} mA, -15 V {ch[k][1]:.0f} mA; master {k}: +15 V {ms[k][0]:.0f} mA, -15 V {ms[k][1]:.0f} mA")
for n in (4,16):
    for k in ("typ","max","sizing"):
        p=n*ch[k][0]+ms[k][0]; m=n*ch[k][1]+ms[k][1]
        print(f"{n:2d} cards + master, {k:6s}: +15 V {p/1000:.2f} A, -15 V {m/1000:.2f} A, {(p+m)*float(RAW)/1000:.0f} W")
for k in ("typ","max","sizing"):
    print(f"power ribbon, 8 cards on 2 pins per rail, {k}: {8*max(ch[k])/2/1000:.2f} A per pin")
