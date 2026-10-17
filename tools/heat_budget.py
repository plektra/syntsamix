# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Heat budget and ventilation estimate (decision 167).

Typical dissipation inside the unit from both card budget scripts (cards draw their raw-rail power, all of it
ends as heat inside) plus the power board's conversion loss, then two estimates for a closed box and for the
passive vents of decision 167: the air rise of a sealed box (natural convection and radiation from the panels,
cover and cheeks), the rise with the rear-strip slots of decision 167, and the exhaust area that would hold the
inside air at 15 K (stack effect from the perforated bottom cover, taken as much larger than the exhaust, to the
rear slots). The coefficients are textbook
estimates, not measurements: the prototype measurement replaces them (decision 167).
Usage: python3 tools/heat_budget.py [raw rail, default 20]
"""
import math, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
RAW=sys.argv[1] if len(sys.argv)>1 else "20"
ETA=0.88            # power board conversion efficiency [estimate]; TPS54560 buck and inverter
DEPTH=0.36          # m, top panel length (decision 108)
H_FRONT,H_REAR=0.020,0.060   # m inside (decisions 160, 162)
H_TOP,H_BOTTOM,H_SIDE=6.0,3.0,5.0   # W/m2K, convection plus radiation [estimate]
DESIGN=22.0         # K, design rise of the inside air above room temperature (decision 167)
REF=15.0            # K, rise for the comparison area
AMBIENT=35.0        # C, warm stage
STACK=0.05          # m, height from intake to exhaust
CD=0.6              # discharge coefficient of a slotted opening
SINK,JC=12.67,6.0   # C/W master heatsink (Wakefield 637-10ABPE, decision 174) and junction-to-sink: change together with hardware/master/scripts/power_budget.py
SLOTS_STRIP,SLOTS_FIXED=2.4,5.0   # cm2 exhaust: 4 slots 2 x 30 mm per channel rear strip; master (3) and bay (2) rear pieces [estimate]
def rise(total,ha,area):
    """Inside air rise (K) with `area` m2 of exhaust: panels plus stack flow, solved by bisection."""
    lo,hi=0.0,100.0
    for _ in range(60):
        dt=(lo+hi)/2
        v=CD*math.sqrt(2*9.81*STACK*dt/(AMBIENT+273.15))
        lo,hi=(dt,hi) if ha*dt+1.2*1005*v*area*dt<total else (lo,dt)
    return dt
def run(board):
    out=subprocess.run([sys.executable,str(ROOT/"hardware"/board/"scripts"/"power_budget.py"),RAW],
                       capture_output=True,text=True,check=True).stdout
    p,m=(float(x) for x in re.search(r"^typ: \+15 V (\d+) mA, -15 V (\d+) mA",out,re.M).groups())
    return out,(p+m)*float(RAW)/1000
_,ch=run("channel-card")
mout,ms=run("master")
reg=[float(x) for x in re.search(r"^max:.*LM317 ([\d.]+) W, LM337 ([\d.]+) W",mout,re.M).groups()]
regt=[float(x) for x in re.search(r"^typ:.*LM317 ([\d.]+) W, LM337 ([\d.]+) W",mout,re.M).groups()]
print(f"channel card {ch:.1f} W, master {ms:.1f} W typical at {RAW} V raw")
for n in (4,8,16):
    cards=n*ch+ms; loss=cards*(1/ETA-1); total=cards+loss
    w=0.035*(n+5)
    ha=H_TOP*w*DEPTH+H_BOTTOM*w*DEPTH+H_SIDE*(w*(H_FRONT+H_REAR)+DEPTH*(H_FRONT+H_REAR))
    v=CD*math.sqrt(2*9.81*STACK*REF/(AMBIENT+273.15))
    area=max(0.0,total-ha*REF)/(1.2*1005*v*REF)
    slots=SLOTS_STRIP*n+SLOTS_FIXED
    print(f"{n:2d} cards: cards+master {cards:.0f} W, power board loss {loss:.0f} W, total {total:.0f} W; "
          f"sealed rise {total/ha:.0f} K; rear slots {slots:.0f} cm2: rise {rise(total,ha,slots/1e4):.0f} K; "
          f"{REF:.0f} K would need {area*1e4:.0f} cm2 of exhaust")
air=AMBIENT+DESIGN
print(f"master regulator at {air:.0f} C air: worst {max(reg):.2f} W -> TJ {air+max(reg)*(SINK+JC):.0f} C, "
      f"typical {max(regt):.2f} W -> TJ {air+max(regt)*(SINK+JC):.0f} C")
