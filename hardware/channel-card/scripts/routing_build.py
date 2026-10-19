# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Routing sheet reference netlist (build/routing.json), written independently of the drawing.

Pre-fader buffers, two stereo AUX sends (dual-gang pot, pre/post jumper),
main/compressor bus assign (CD4052B), PFL and sidechain send (CD4052B), the
open-collector PFL_ACT driver and the three buttons. Bus resistors 22 kΩ
(unity gain into a 22 kΩ virtual-earth amplifier on the master card); the
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
# CD4052B switches at the bus end of each bus resistor (decision 183): the common sits at
# virtual-earth level and every throw is a master virtual earth or AGND, so the switch only
# sees millivolts. A = control, B and INH low: channels 0 and 1 only (X2/X3/Y2/Y3 open).
# Pins: X 13, X0 12, X1 14, Y 3, Y0 1, Y1 5, A 10, B 9, INH 6, VEE 7, VSS 8, VDD 16.
for u,ctrl in (("U302","COMP_CTRL"),("U303","PFL_CTRL"),("U304","SC_OFF")):
    N(ctrl,f"{u}.10"); N("AGND",f"{u}.9",f"{u}.6",f"{u}.8"); N("+5V",f"{u}.16"); N("VEE",f"{u}.7")
# bus assign: U302, A = COMP_CTRL, pressed = compressor bus
N("L_POSTFADE","R301.1"); N("L_BUS","R301.2","U302.13"); N("MAIN_L","U302.12"); N("COMP_L","U302.14")
N("R_POSTFADE","R302.1"); N("R_BUS","R302.2","U302.3"); N("MAIN_R","U302.1"); N("COMP_R","U302.5")
# PFL: U303, A = PFL_CTRL, released = resistor end to AGND, pressed = cue bus
N("L_PRE","R303.1","R305.1"); N("L_PFLR","R303.2","U303.13"); N("AGND","U303.12"); N("CUE_L","U303.14")
N("R_PRE","R304.1","R306.1"); N("R_PFLR","R304.2","U303.3"); N("AGND","U303.1"); N("CUE_R","U303.5")
# SC send: U304 X, A = SC_OFF (high while SW302 is released): 0 = SC bus, 1 = AGND; Y unused
N("SC_SUM","R305.2","R306.2","U304.13"); N("SC","U304.12"); N("AGND","U304.14")
# PFL_ACT open-collector driver
N("PFL_CTRL","R311.1"); N("Q_B","R311.2","Q301.1"); N("PGND","Q301.2"); N("PFL_ACT","Q301.3")
# buttons
for name,sw,led,rl,rp in (("PFL","SW301","D301","R312","R313"),("SC","SW302","D302","R314","R315"),("COMP","SW303","D303","R316","R317")):
    N("SC_OFF" if name=="SC" else f"{name}_CTRL",f"{sw}.1" if name=="SC" else f"{sw}.3",f"{rp}.2"); N("+5V",f"{sw}.2"); N(f"{name}_LEDK",f"{sw}.6",f"{led}.1"); N("PGND",f"{sw}.5")   # SC: released throw 1-2
    N(f"{name}_LED",f"{led}.2",f"{rl}.2"); N("+15V",f"{rl}.1"); N("PGND",f"{rp}.1")
N("L_PRE","TP301.1"); N("R_PRE","TP302.1")
# supplies and decoupling
N("+15V","U93013.8"); N("-15V","U93013.4")
N("+15V","C301.1"); N("AGND","C301.2"); N("-15V","C302.1"); N("AGND","C302.2")
for k in (303,305,307): N("+5V",f"C{k}.1"); N("AGND",f"C{k}.2")
for k in (304,306,308): N("VEE",f"C{k}.1"); N("AGND",f"C{k}.2")   # VEE (about -6.2 V) is made on the Chain and power sheet
T=os.path.join(os.path.dirname(os.path.abspath(__file__)),'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump({"nets":[{"name":k,"pins":v} for k,v in nets.items()]},open(T+'routing.json','w'))
print(len(nets),"nets",sum(len(v) for v in nets.values()),"pins")
