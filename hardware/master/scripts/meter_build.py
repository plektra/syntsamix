# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master meter sheet reference netlist (build/meter.json), written independently of the drawing.

Spec section 4 (12 segments per side), decisions 76 and 86. Per side: the signal and its
inverse each drive a superdiode (TL072) charging a 1 µF hold through 1 kΩ (about 1 ms
attack); 680 kΩ gives a fall of 20 dB in about 1.5 s; a follower drives 12 LM339
comparators. One 1% ladder from +15 V sets both sides' thresholds relative to +4 dBu peak:
-30 -20 -15 -10 -6 -3 0 +3 +6 +9 +12 and clip (+13, about +17 dBu), within 0.14 dB
(fee-free E24 values at about 0.45 mA, decision 146).
LEDs: 3 mm, about 2 mA from +5 V into the LM339 outputs (ground PGND).
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
# ---------------------------------------------------------------- detectors
for side,(sdp,sdn,inv,fol,rin,rfb,rp,rn,rd,dp,dn,ch,tp) in (
        ("L",(("U801",3,2,1),("U98012",5,6,7),("U802",3,2,1),("U98022",5,6,7),"R801","R802","R803","R804","R805","D801","D802","C801","TP801")),
        ("R",(("U803",3,2,1),("U98032",5,6,7),("U804",3,2,1),("U98042",5,6,7),"R806","R807","R808","R809","R810","D803","D804","C802","TP802"))):
    src=f"MAIN_{side}_OUT"
    N(src,f"{sdp[0]}.{sdp[1]}",f"{rin}.1")
    N(f"{side}_INVN",f"{rin}.2",f"{rfb}.1",f"{inv[0]}.{inv[2]}"); N("AGND",f"{inv[0]}.{inv[1]}")
    N(f"{side}_NEG",f"{inv[0]}.{inv[3]}",f"{rfb}.2",f"{sdn[0]}.{sdn[1]}")
    for (ref,pp,pm,po),d,r,tag in ((sdp,dp,rp,"P"),(sdn,dn,rn,"N")):
        N(f"{side}_X{tag}",f"{ref}.{pm}",f"{d}.1",f"{r}.1"); N(f"{side}_O{tag}",f"{ref}.{po}",f"{d}.2"); N(f"{side}_HOLD",f"{r}.2")
    N(f"{side}_HOLD",f"{ch}.1",f"{rd}.1",f"{fol[0]}.{fol[1]}"); N("AGND",f"{ch}.2",f"{rd}.2")
    N(f"MV_{side}",f"{fol[0]}.{fol[2]}",f"{fol[0]}.{fol[3]}",f"{tp}.1")
# ---------------------------------------------------------------- ladder: +15 V - R811 - T12 - R812 - T11 ... T1 - R823 - AGND
N("+15V","R811.1"); N("T12","R811.2")
for i in range(1,12):                 # R812 between T12 (top, pin 1) and T11 ... R822 between T2 and T1
    N(f"T{13-i}",f"R{811+i}.1"); N(f"T{12-i}",f"R{811+i}.2")
N("T1","R823.1"); N("AGND","R823.2")
# ---------------------------------------------------------------- comparators: + = threshold, - = MV, output sinks the LED
UNIT={1:(5,4,2),2:(7,6,1),3:(11,10,13),4:(9,8,14)}
for side,chips,d0,r0 in (("L",("805","806","807"),804,823),("R",("808","809","810"),816,835)):
    for k in range(1,13):
        chip=chips[(k-1)//4]; unit=(k-1)%4+1; ref=f"U{chip}" if unit==1 else f"U9{chip}{unit}"; pp,pm,po=UNIT[unit]
        N(f"T{k}",f"{ref}.{pp}"); N(f"MV_{side}",f"{ref}.{pm}"); N(f"{side}_SEG{k}",f"{ref}.{po}",f"D{d0+k}.1")
        N(f"{side}_LEDA{k}",f"D{d0+k}.2",f"R{r0+k}.2"); N("+5V",f"R{r0+k}.1")
# ---------------------------------------------------------------- supplies and decoupling
for ref in ("U98013","U98023","U98033","U98043"): N("+15V",f"{ref}.8"); N("-15V",f"{ref}.4")
for chip in ("805","806","807","808","809","810"): N("+15V",f"U9{chip}5.3"); N("PGND",f"U9{chip}5.12")
for k in (803,805,807,809): N("+15V",f"C{k}.1"); N("AGND",f"C{k}.2"); N("-15V",f"C{k+1}.1"); N("AGND",f"C{k+1}.2")
for k in range(811,817): N("+15V",f"C{k}.1"); N("PGND",f"C{k}.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'meter.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
