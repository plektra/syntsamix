# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board +20 V buck sheet: reference netlist (build/buck.json), written independently of the drawing.

TPS54560 buck from VIN_SW (24 V) to +20 V at 2 A, synced to CLK_A at about 400 kHz (RT 240k sets
405 kHz when the clock is absent). FB 240k / 10k = 20.0 V. Compensation 16k + 220n, 560p
(design.py). SS54 catch diode, 15 uH. Second-stage LC filter 2.2 uH with 330 uF polymer,
100 uF electrolytic (damping) and 4.7 uF ceramic, feedback taken before the filter (decision 100).
Start-up ramp: 47 nF from the output through D202 into FB stretches the start to about 40 ms
(tau 240k x 47n), so charging the rail capacitance stays under the brick's overload threshold
(startup_sim.py); R207 1M and the clamp D203 reset the node, D202 is off in steady state.
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
N("VIN_SW","U201.2","C201.1","C202.1","C203.1","C204.1","R201.1")
N("PGND","U201.7","U201.9","C201.2","C202.2","C203.2","C204.2","R202.2","C205.2","C206.2","R204.2")
N("EN","U201.3","R201.2","R202.1")
N("COMP","U201.6","R203.1","C206.1"); N("CZ","R203.2","C205.1")
N("RT","U201.4","R204.1","C207.2"); N("CLK_A","C207.1")
N("BOOT","U201.1","C208.1"); N("SW","U201.8","C208.2","D201.1","L201.1"); N("PGND","D201.2")
N("+20V_CONV","L201.2","C209.1","C210.1","R205.1","L202.1"); N("PGND","C209.2","C210.2","R206.2")
N("FB","U201.5","R205.2","R206.1","D202.1")
N("+20V_CONV","C214.1"); N("SS","C214.2","D202.2","D203.1","R207.1"); N("PGND","D203.2","R207.2")
N("+20V_RAW","L202.2","C211.1","C212.1","C213.1","TP201.1"); N("PGND","C211.2","C212.2","C213.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'buck.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
