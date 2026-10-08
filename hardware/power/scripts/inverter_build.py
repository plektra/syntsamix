# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board -20 V inverter sheet: reference netlist (build/inverter.json), written independently of the drawing.

TPS54560 as an inverting buck-boost (TI SLVA317B): the IC ground is the -20 V node (-20V_CONV),
the inductor (22 uH) goes from SW to PGND, the catch diode (SS510C, 100 V) from -20V_CONV to SW.
FB 240k from PGND / 10k to -20V_CONV = -20.0 V. Compensation 27k + 220n, 100p (design.py).
Sync from CLK_B through 10 pF (100 V: it bridges about 20 V). The input capacitors from VIN to the
IC ground see VIN + 20 V (100 V parts). Second-stage LC filter as on the buck (decision 100).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
NEG="-20V_CONV"
N("VIN_SW","U301.2","C301.1","C302.1","C303.1","C304.1","R301.1"); N("PGND","C303.2")
N(NEG,"U301.7","U301.9","C301.2","C302.2","C304.2","R302.2","C305.2","C306.2","R304.2","TP302.1")
N("EN","U301.3","R301.2","R302.1")
N("COMP","U301.6","R303.1","C306.1"); N("CZ","R303.2","C305.1")
N("RT","U301.4","R304.1","C307.2"); N("CLK_B","C307.1")
N("BOOT","U301.1","C308.1"); N("SW","U301.8","C308.2","D301.1","L301.1"); N(NEG,"D301.2"); N("PGND","L301.2")
N("PGND","C309.1","C310.1","R305.2"); N(NEG,"C309.2","C310.2","R306.1","L302.1")
N("FB","U301.5","R305.1","R306.2")
N("-20V_RAW","L302.2","C311.2","C312.2","C313.2","TP301.1"); N("PGND","C311.1","C312.1","C313.1")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'inverter.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
