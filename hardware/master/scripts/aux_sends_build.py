# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""AUX sends sheet reference netlist (build/aux_sends.json), written independently of the drawing.

Decisions 24 and 51. Per send n (references 6xx: send 1 from 601, send 2 from 621):
dual-gang 10 kΩ log master pot on the inverted bus sums AUXn_L/R_SUM (CCW = off),
inverting stages (47 kΩ / 47 kΩ, NE5532) restore polarity, impedance-balanced outputs
(tip through 100 Ω, ring through 100 Ω to AGND) on 6.3 mm TRS jacks.
L/MONO: the R jack's ring switch contact (RN) detects a plug; with R unplugged, DG411
sections (normally closed, on at logic 0) add the R wiper into the L stage and halve
its feedback, so L carries (L+R)/2. One DG411 (U641) serves both sends.
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,q=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":q})
DG={1:(("U641",2,3,1),("U96412",6,7,8)),2:(("U96413",10,11,9),("U96414",15,14,16))}   # (mono add, feedback halving): left, right, IN
for n,B in ((1,600),(2,620)):
    r=lambda k:f"R{B+k}"; U=f"U{B+1}"; U2=f"U9{B+1}2"; RV=f"RV{B+1}"; JL,JR=f"J{B+1}",f"J{B+2}"
    # master pot
    N("AGND",f"{RV}.1",f"{RV}.4"); N(f"AUX{n}_L_SUM",f"{RV}.3"); N(f"AUX{n}_R_SUM",f"{RV}.6")
    N(f"L{n}_W",f"{RV}.2",r(1)+".1"); N(f"R{n}_W",f"{RV}.5",r(5)+".1",r(3)+".2")
    # L stage with mono switching
    N(f"L{n}_N",r(1)+".2",r(2)+".1",f"{U}.2"); N("AGND",f"{U}.3"); N(f"L{n}_O",f"{U}.1",r(2)+".2",r(4)+".2",r(7)+".1",f"TP{B+1}.1")
    (ma,ma_l,ma_r,ma_in),(fb,fb_l,fb_r,fb_in)=DG[n]
    N(f"L{n}_N",f"{ma}.{ma_l}",f"{fb}.{fb_l}"); N(f"L{n}_MX",f"{ma}.{ma_r}",r(3)+".1"); N(f"L{n}_FB",f"{fb}.{fb_r}",r(4)+".1")
    N(f"DET{n}",f"{ma}.{ma_in}",f"{fb}.{fb_in}")
    # R stage
    N(f"R{n}_N",r(5)+".2",r(6)+".1",f"{U2}.6"); N("AGND",f"{U2}.5"); N(f"R{n}_O",f"{U2}.7",r(6)+".2",r(9)+".1",f"TP{B+2}.1")
    # outputs
    N(f"L{n}_T",r(7)+".2",f"{JL}.T"); N(f"L{n}_RING",f"{JL}.R",r(8)+".1"); N("AGND",r(8)+".2",f"{JL}.S")
    N(f"R{n}_T",r(9)+".2",f"{JR}.T"); N(f"R{n}_RING",f"{JR}.R",r(10)+".1"); N("AGND",r(10)+".2",f"{JR}.S")
    N(f"DET{n}",f"{JR}.RN",r(11)+".2",f"C{B+1}.1"); N("+5V",r(11)+".1"); N("AGND",f"C{B+1}.2")
    # supplies
    N("+15V",f"U9{B+1}3.8",f"C{B+2}.1"); N("-15V",f"U9{B+1}3.4",f"C{B+3}.1"); N("AGND",f"C{B+2}.2",f"C{B+3}.2")
N("+15V","U96415.13","C642.1"); N("-15V","U96415.4","C643.1"); N("+5V","U96415.12"); N("AGND","U96415.5","C642.2","C643.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'aux_sends.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
