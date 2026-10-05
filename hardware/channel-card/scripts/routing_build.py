# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Routing sheet reference netlist (build/routing.json), written independently of the drawing.

Pre-fader buffers, two stereo AUX sends (dual-gang pot, pre/post jumper),
main/compressor bus assign (DG413), PFL and sidechain send (DG412), the
open-collector PFL_ACT driver and the three buttons. Bus resistors 22.1 kΩ
(unity gain into a 22.1 kΩ virtual-earth amplifier on the master card); the
sidechain send sums L and R through 44.2 kΩ each, so the SC bus carries (L+R)/2.
Temporary references U9<ref><unit> mark extra units of multi-unit symbols.
"""
import json,os
nets={}
def N(net,*pins):
    for p in pins:
        r,n=p.split('.'); nets.setdefault(net,[]).append({"ref":r,"pin":n})
# pre-fader buffers (U301 NE5532)
N("L_POSTFILT","U301.3"); N("L_PRE","U301.2","U301.1")
N("R_POSTFILT","U93012.5"); N("R_PRE","U93012.6","U93012.7")
# AUX sends: J301/J302 pre-post header (1 L_PRE, 3 L_SRC, 5 L_POSTFADE; 2 R_PRE, 4 R_SRC, 6 R_POSTFADE)
for n,j,rv,rl,rr in ((1,"J301","RV301","R307","R308"),(2,"J302","RV302","R309","R310")):
    N("L_PRE",f"{j}.1"); N(f"L_AUX{n}_SRC",f"{j}.3"); N("L_POSTFADE",f"{j}.5")
    N("R_PRE",f"{j}.2"); N(f"R_AUX{n}_SRC",f"{j}.4"); N("R_POSTFADE",f"{j}.6")
    N("AGND",f"{rv}.1",f"{rv}.4"); N(f"L_AUX{n}_SRC",f"{rv}.3"); N(f"R_AUX{n}_SRC",f"{rv}.6")
    N(f"L_AUX{n}_W",f"{rv}.2",f"{rl}.2"); N(f"AUX{n}_L",f"{rl}.1")
    N(f"R_AUX{n}_W",f"{rv}.5",f"{rr}.2"); N(f"AUX{n}_R",f"{rr}.1")
# bus assign: U302 DG413, pressed = compressor bus
N("L_POSTFADE","R301.1"); N("L_BUS","R301.2","U302.2","U93024.15"); N("COMP_L","U302.3"); N("MAIN_L","U93024.14")
N("R_POSTFADE","R302.1"); N("R_BUS","R302.2","U93023.10","U93022.6"); N("MAIN_R","U93023.11"); N("COMP_R","U93022.7")
N("COMP_CTRL","U302.1","U93024.16","U93023.9","U93022.8")
# PFL and SC send: U303 DG412
N("L_PRE","R303.1","R305.1"); N("L_PFLR","R303.2","U303.2"); N("CUE_L","U303.3")
N("R_PRE","R304.1","R306.1"); N("R_PFLR","R304.2","U93034.15"); N("CUE_R","U93034.14")
N("PFL_CTRL","U303.1","U93034.16")
N("SC_SUM","R305.2","R306.2","U93032.6"); N("SC","U93032.7"); N("SC_CTRL","U93032.8")
N("AGND","U93033.9","U93033.10","U93033.11")
# PFL_ACT open-collector driver
N("PFL_CTRL","R311.1"); N("Q_B","R311.2","Q301.1"); N("AGND","Q301.2"); N("PFL_ACT","Q301.3")
# buttons
for name,sw,led,rl,rp in (("PFL","SW301","D301","R312","R313"),("SC","SW302","D302","R314","R315"),("COMP","SW303","D303","R316","R317")):
    N(f"{name}_CTRL",f"{sw}.1",f"{rp}.2"); N("+5V",f"{sw}.2"); N(f"{name}_LEDK",f"{sw}.4",f"{led}.1"); N("PGND",f"{sw}.5")
    N(f"{name}_LED",f"{led}.2",f"{rl}.2"); N("+15V",f"{rl}.1"); N("AGND",f"{rp}.1")
# supplies and decoupling
N("+15V","U93013.8","U93025.13","U93035.13"); N("-15V","U93013.4","U93025.4","U93035.4")
N("+5V","U93025.12","U93035.12"); N("AGND","U93025.5","U93035.5")
for k in (301,303,305): N("+15V",f"C{k}.1"); N("AGND",f"C{k}.2")
for k in (302,304,306): N("-15V",f"C{k}.1"); N("AGND",f"C{k}.2")
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'routing.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
