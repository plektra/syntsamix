# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master card bus summing sheet: reference netlist (build/bus.json), written independently of the drawing.

The 34-pin audio ribbon (docs/CHAIN.md) brings the current-summing buses from the
channel cards. Each bus node is the inverting input of a virtual-earth amplifier
(NE5532, 22 kΩ ∥ 100 pF feedback: unity gain per 22 kΩ bus resistor, decisions 74 and 79).
Bus nodes are also hierarchical, so other master sheets can sum into them; the
amplifier outputs (<bus>_SUM, inverted) feed the rest of the master card.
PFL_ACT gets its pull-up here.
"""
import json,os
BUSES=["MAIN_L","MAIN_R","COMP_L","COMP_R","AUX1_L","AUX1_R","AUX2_L","AUX2_R","CUE_L","CUE_R","SC"]
PIN={"MAIN_L":2,"MAIN_R":4,"COMP_L":6,"COMP_R":8,"AUX1_L":10,"AUX1_R":12,"AUX2_L":14,"AUX2_R":16,"CUE_L":18,"CUE_R":20,"SC":22}
TPS={"MAIN_L":101,"MAIN_R":102,"COMP_L":103,"COMP_R":104,"CUE_L":105,"SC":106}
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
def unit(i):    # bus i -> (reference as drawn, pins (-, +, out))
    ref=101+i//2
    return (f"U{ref}",(2,3,1)) if i%2==0 else (f"U9{ref}2",(6,5,7))
for p in range(1,35,2): N("AGND",f"J101.{p}")
for i,b in enumerate(BUSES):
    u,(pm,pp,po)=unit(i)
    N(b,f"J101.{PIN[b]}",f"{u}.{pm}",f"R{111+i}.1",f"C{121+i}.1")
    N("AGND",f"{u}.{pp}"); N(f"{b}_SUM",f"{u}.{po}",f"R{111+i}.2",f"C{121+i}.2")
    if b in TPS: N(f"{b}_SUM",f"TP{TPS[b]}.1")
N("SC_ENV","J101.24"); N("PFL_ACT","J101.34","R101.2"); N("+5V","R101.1")
N("AGND","U91062.5"); N("SPARE_OA","U91062.6","U91062.7")      # spare half of U106
for k,ref in enumerate(["U91013","U91023","U91033","U91043","U91053","U91063"]):
    N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
    N("+15V",f"C{141+2*k}.1"); N("AGND",f"C{141+2*k}.2"); N("-15V",f"C{142+2*k}.1"); N("AGND",f"C{142+2*k}.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'bus.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
