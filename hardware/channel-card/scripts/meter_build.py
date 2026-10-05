# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Meter sheet reference netlist (build/meter.json), written independently of the drawing.

8-segment mono peak meter, louder of L and R (decision 43). L, -L, R and -R each
drive a precision rectifier (superdiode) whose output charges one hold capacitor
through 1 kΩ (1 ms attack, outside the feedback loop for stability); 680 kΩ
discharges it (20 dB fall in about 1.5 s). A follower drives eight LM339
comparators against a ladder from +15 V. Thresholds relative to +4 dBu peak:
-30, -20, -10, -5, 0, +3, +6, +10 dB (clip at +14 dBu, the soft-clip onset).
LEDs run from +5 V and sink into the LM339 outputs, whose ground is PGND.
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
# inverters (U401 TL072)
N("L_PRE","R401.1"); N("INVL","R401.2","R402.1","U401.2"); N("AGND","U401.3"); N("L_NEG","R402.2","U401.1")
N("R_PRE","R403.1"); N("INVR","R403.2","R404.1","U94012.6"); N("AGND","U94012.5"); N("R_NEG","R404.2","U94012.7")
# superdiodes: + input, - input = X node, output -> diode (A) -> X (K) -> 1k -> HOLD
for (ref,pp,pm,po,src,d,r,tag) in (("U402",3,2,1,"L_PRE","D401","R405","L1"),("U94022",5,6,7,"L_NEG","D402","R406","L2"),
                                   ("U403",3,2,1,"R_PRE","D403","R407","R1"),("U94032",5,6,7,"R_NEG","D404","R408","R2")):
    N(src,f"{ref}.{pp}"); N(f"X{tag}",f"{ref}.{pm}",f"{d}.1",f"{r}.1"); N(f"O{tag}",f"{ref}.{po}",f"{d}.2"); N("HOLD",f"{r}.2")
# hold, decay, buffer
N("HOLD","C401.1","R409.1","U404.3"); N("AGND","C401.2","R409.2")
N("MV","U404.2","U404.1")
N("AGND","U94042.5"); N("SPARE_OA","U94042.6","U94042.7")
# threshold ladder: +15 V - R410 - T8 - R411 - T7 ... T1 - R418 - AGND
N("+15V","R410.1")
taps=["T8","T7","T6","T5","T4","T3","T2","T1"]
for i,t in enumerate(taps): N(t,f"R{410+i}.2",f"R{411+i}.1")
N("AGND","R418.2")
# comparators: + = threshold, - = MV, output sinks the LED (on when MV > threshold)
units=[("U405",5,4,2),("U94052",7,6,1),("U94053",11,10,13),("U94054",9,8,14),
       ("U406",5,4,2),("U94062",7,6,1),("U94063",11,10,13),("U94064",9,8,14)]
for k,(ref,pp,pm,po) in enumerate(units,start=1):      # k = 1 (-30 dB) ... 8 (clip)
    N(f"T{k}",f"{ref}.{pp}"); N("MV",f"{ref}.{pm}"); N(f"SEG{k}",f"{ref}.{po}",f"D{410+k}.1")
    N(f"LEDA{k}",f"D{410+k}.2",f"R{418+k}.2"); N("+5V",f"R{418+k}.1")
N("MV","TP401.1")
# supplies and decoupling
for ref in ("U94013","U94023","U94033","U94043"): N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
for ref in ("U94055","U94065"): N("+15V",f"{ref}.3"); N("PGND",f"{ref}.12")
for k in (402,404,406,408): N("+15V",f"C{k}.1"); N("AGND",f"C{k}.2")
for k in (403,405,407,409): N("-15V",f"C{k}.1"); N("AGND",f"C{k}.2")
for k in (410,411): N("+15V",f"C{k}.1"); N("PGND",f"C{k}.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'meter.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
