# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master card power sheet: reference netlist (build/power.json), written independently of the drawing.

Power ribbon in from the power board (decision 81). LM317/LM337 to ±15.1 V (200 Ω / 2.2 kΩ,
10 µF on ADJ, protection diodes), SS14 rail clamps, L7805 (TO-220) for +5 V: the master's
LED load (two 12-segment meters, compressor and PFL LEDs) is too much for a 78L05.
AGND and PGND join here and only here, through a net tie (the system star point, CHAIN.md).
The frame bonds to it through a ground-lift switch; lifted, through 100 Ω ∥ 100 nF.
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
N("-20V_RAW","J901.1","J901.2"); N("PGND","J901.3","J901.4","J901.5","J901.6"); N("+20V_RAW","J901.7","J901.8")
N("+20V_RAW","U901.3","C901.1","C902.1","D901.1"); N("PGND","C901.2","C902.2")
N("+15V","U901.2","D901.2","R901.1","D902.1","C904.1","C905.1","D905.1")
N("ADJ_P","U901.1","R901.2","R902.1","C903.1","D902.2"); N("AGND","R902.2","C903.2","C904.2","C905.2","D905.2")
N("-20V_RAW","U902.2","C906.2","C907.1","D903.2"); N("PGND","C906.1","C907.2")
N("-15V","U902.3","D903.1","R903.2","D904.2","C909.2","C910.1","D906.2")
N("ADJ_N","U902.1","R903.1","R904.2","C908.2","D904.1"); N("AGND","R904.1","C908.1","C909.1","C910.2","D906.1")
N("+15V","U903.1","C911.1"); N("PGND","U903.2","C911.2","C912.2"); N("+5V","U903.3","C912.1")
N("AGND","NT901.1"); N("PGND","NT901.2")
N("CHASSIS","J902.1","SW901.1","R905.1","C913.1"); N("AGND","SW901.2","R905.2","C913.2")
for tp,net in (("TP901","+20V_RAW"),("TP902","-20V_RAW"),("TP903","+15V"),("TP904","-15V"),("TP905","+5V"),("TP906","PGND")): N(net,f"{tp}.1")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'power.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
