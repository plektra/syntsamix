# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Power board outputs sheet, drawn with real wires.

Reference netlist: outputs_build.py (check_netlist.py outputs.json). The two rails run along the
top; each group drops through its two PTCs to labels that feed its header (wired like the master
card's power input, power_wired.py).
"""
import json,os
from schlayout import Sheet
from parts import part
s=Sheet()
def pl(lib,sym,ref,val,key,x,y,rot=0,**extra):
    fp,props=part(key,**extra); return s.place(lib,sym,ref,val,x,y,rot,fp=fp,props=props)
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)
YP,YNR=60.96,86.36
s.label("+20V_RAW",(40.64,YP),180,"hierarchical","input")
s.label("-20V_RAW",(40.64,YNR),180,"hierarchical","input")
xp,xn=[40.64],[40.64]
NOTE=("Power ribbon to the master card","Power ribbon chain 1 (cards 1-8)","Power ribbon chain 2 (cards 9-16)")
for g,name in enumerate(("M","C1","C2")):
    X0=76.2+76.2*g; xp.append(X0); xn.append(X0+10.16)
    f=pl("Device","Polyfuse",f"F{401+2*g}","2A 33V","PTC 2A",X0,68.58,0)
    s.wire((X0,YP),f(1)); s.wire(f(2),(X0,74.93)); s.label(f"+20V_{name}",(X0,74.93),0)
    f=pl("Device","Polyfuse",f"F{402+2*g}","2A 33V","PTC 2A",X0+10.16,93.98,0)
    s.wire((X0+10.16,YNR),f(1)); s.wire(f(2),(X0+10.16,100.33)); s.label(f"-20V_{name}",(X0+10.16,100.33),0)
    j=pl("Connector_Generic","Conn_02x04_Odd_Even",f"J{401+g}",("MASTER","CHAIN 1","CHAIN 2")[g],"HDR 2x4",X0+20.32,127.0,0,
         Note=NOTE[g]+": 8-pin shrouded keyed box header, 1-2 V-, 3-6 PGND, 7-8 V+ (docs/CHAIN.md); 3 A per contact")
    for side,pins in (("L",(1,3,5,7)),("R",(2,4,6,8))):
        a,b,cc,d=pins; x=j(a)[0]+(-5.08 if side=="L" else 5.08); sg=-1 if side=="L" else 1
        for p in pins: s.wire(j(p),(x,j(p)[1]))
        s.wire((x,j(b)[1]),(x,j(cc)[1])); pg=(x+sg*20.32,j(b)[1]); s.wire((x,j(b)[1]),pg); pgnd(pg,90 if side=="L" else 270)
        for p,lab in ((a,f"-20V_{name}"),(d,f"+20V_{name}")):
            e=(x+sg*7.62,j(p)[1]); s.wire((x,j(p)[1]),e); s.label(lab,e,180 if side=="L" else 0)
for y,xs in ((YP,xp),(YNR,xn)):
    for a,b in zip(xs,xs[1:]): s.wire((a,y),(b,y))

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'outputs.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_outputs_wired.json','w'))
json.dump({"no_connect":[]},open(T+'outputs_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
