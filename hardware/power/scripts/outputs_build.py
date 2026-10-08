# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board outputs sheet: reference netlist (build/outputs.json), written independently of the drawing.

Three 8-pin power ribbon headers (docs/CHAIN.md: 1-2 V-, 3-6 PGND, 7-8 V+): J401 master card,
J402 chain 1 (cards 1-8), J403 chain 2 (cards 9-16; fitted on the prototype too). Each rail of each
header has its own 2 A PTC (F401-F406) so a shorted card or ribbon trips its own fuse (decision 100).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
for g,name in enumerate(("M","C1","C2")):
    j=f"J{401+g}"; fp,fn=f"F{401+2*g}",f"F{402+2*g}"
    N("+20V_RAW",f"{fp}.1"); N(f"+20V_{name}",f"{fp}.2",f"{j}.7",f"{j}.8")
    N("-20V_RAW",f"{fn}.1"); N(f"-20V_{name}",f"{fn}.2",f"{j}.1",f"{j}.2")
    N("PGND",*(f"{j}.{p}" for p in (3,4,5,6)))
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'outputs.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
