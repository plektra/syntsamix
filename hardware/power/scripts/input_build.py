# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board input sheet: reference netlist (build/input.json), written independently of the drawing.

24 V brick on a locking 4-pin DIN jack (Kycon KPJX-4S; brick plug pins 1, 4 = +24 V, 2, 3 = 0 V,
polarity to check on the first brick), 4 A PTC, SMBJ24A TVS, two SQJ457EP P-MOSFETs back to back:
Q101 blocks a reversed brick, Q102 turns on slowly (Miller ramp, C102 47 nF through R103) so the
converter input capacitors charge gently. The power switch (a rear-panel rocker on J102, two wires) only pulls the shared gate to PGND
through R102; R101 / R102 bias the gate to -12 V, D102 clamps it. Power LED on the switched side.
Clock: L78M05 to +5 V, 74HC14 RC oscillator about 400 kHz (4.7k / 560p), two inverters give
CLK_B and CLK_A in opposite phase for the two TPS54560 (decision 100).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
N("VBRICK","J101.1","J101.4","F101.1"); N("PGND","J101.2","J101.3")
N("VFUSED","F101.2","D101.1","C101.1","Q101.5"); N("PGND","D101.2","C101.2")
N("VSRC","Q101.1","Q101.2","Q101.3","Q102.1","Q102.2","Q102.3","R101.1","D102.1")
N("GATE","Q101.4","Q102.4","R101.2","D102.2","R102.1","R103.1")
N("SW_ON","R102.2","J102.1"); N("PGND","J102.2")
N("MILLER","R103.2","C102.1")
N("VIN_SW","Q102.5","C102.2","C103.1","R104.1","U101.1","C104.1","TP101.1")
N("PGND","C103.2","D103.1","U101.2","C104.2","TP102.1")
N("LED_A","R104.2","D103.2")
N("+5V_CLK","U101.3","C105.1","C106.1","U102.14"); N("PGND","C105.2","C106.2","U102.7")
N("OSC_IN","U102.1","R105.1","C107.1"); N("PGND","C107.2")
N("OSC","U102.2","R105.2","U102.3")
N("CLK_B","U102.4","U102.5","TP104.1")
N("CLK_A","U102.6","TP103.1")
N("PGND","U102.9","U102.11","U102.13")   # unused gates: inputs to PGND, outputs open
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'input.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
