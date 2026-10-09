# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master card bus summing sheet, drawn with real wires.

Reference netlist: bus_build.py (check_netlist.py bus.json).
Layout: audio ribbon header on the left (labels to the buses), then one row per
bus: hierarchical bus node, virtual-earth amplifier with 22k ∥ 100p feedback,
hierarchical <bus>_SUM output. PFL_ACT pull-up beside the header, supplies at the bottom.
"""
import json,os
from schlayout import Sheet
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn))
def C(ref,val,pn,x,y,rot=90): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
def OA(ref,unit,x,y): return s.place("Amplifier_Operational","NE5532",ref,"NE5532",x,y,0,unit,SO8,P("SX-IC-004",**TI))
def gnd(at,rot=0): s.power("GNDA",at,rot)
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])
BUSES=["MAIN_L","MAIN_R","COMP_L","COMP_R","AUX1_L","AUX1_R","AUX2_L","AUX2_R","CUE_L","CUE_R","SC"]
PIN={"MAIN_L":2,"MAIN_R":4,"COMP_L":6,"COMP_R":8,"AUX1_L":10,"AUX1_R":12,"AUX2_L":14,"AUX2_R":16,"CUE_L":18,"CUE_R":20,"SC":22}
TPS={"MAIN_L":101,"MAIN_R":102,"COMP_L":103,"COMP_R":104,"CUE_L":105,"SC":106}
NOCONNECT=[]

# ------------------------------------------------------------- audio ribbon header (master end of the chain)
j=s.place("Connector_Generic","Conn_02x17_Odd_Even","J101","AUDIO CHAIN",45.72,101.6,0,fp="Connector_IDC:IDC-Header_2x17_P2.54mm_Vertical",
          props=P("SX-CONN-007",Manufacturer="Wurth Elektronik",MPN="61203421621",Supplier="Mouser",SupplierPN="710-61203421621",Note="34-pin shrouded keyed box header, pinout docs/CHAIN.md; underside, left edge (decision 109); drill 1.1 mm"))
bx=j(1)[0]-2.54
for p in range(1,35,2): s.wire(j(p),(bx,j(p)[1]))
ys=[j(p)[1] for p in range(1,35,2)]
for y1,y2 in zip(ys,ys[1:]): s.wire((bx,y1),(bx,y2))
s.wire((bx,ys[-1]),(bx,ys[-1]+2.54)); gnd((bx,ys[-1]+2.54))
for b,p in PIN.items(): s.wire(j(p),rt(j(p),5.08)); s.label(b,rt(j(p),5.08),0)
s.wire(j(24),rt(j(24),5.08)); s.label("SC_ENV",rt(j(24),5.08),0,"hierarchical","input")
for p in (26,28,30,32): NOCONNECT.append(j(p))
# PFL_ACT: pulled up here, any channel (or SC listen) pulls it low
pa=rt(j(34),10.16); s.wire(j(34),pa,rt(pa,7.62)); s.label("PFL_ACT",rt(pa,7.62),0,"hierarchical","output")
r=R("R101","10k","SX-R-002",pa[0],pa[1]-7.62,0); s.wire(pa,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+5V",up(r(1),2.54))

# ------------------------------------------------------------- one virtual-earth summing amplifier per bus
X0=101.6
for i,b in enumerate(BUSES):
    y=33.02+i*27.94
    ref=101+i//2
    ref_d,unit,(pm,pp,po)=(f"U{ref}",1,(2,3,1)) if i%2==0 else (f"U9{ref}2",2,(6,5,7))
    s.label(b,(X0,y),180,"hierarchical","bidirectional")
    n=(114.3,y); s.wire((X0,y),n)
    a=OA(ref_d,unit,129.54,y-2.54); s.wire(n,a(pm))
    s.wire(a(pp),lt(a(pp)),up(lt(a(pp)))); gnd(up(lt(a(pp))),180)
    o=(142.24,y-2.54); s.wire(a(po),o)
    rf=R(f"R{111+i}","22k","SX-R-047",128.27,y+7.62); cf=C(f"C{121+i}","100p C0G","SX-C-008",128.27,y+15.24)
    s.wire(n,(n[0],y+7.62)); s.wire((n[0],y+7.62),(n[0],y+15.24))
    s.wire((n[0],y+7.62),rf(1)); s.wire((n[0],y+15.24),cf(1))
    s.wire(rf(2),(o[0],y+7.62)); s.wire(cf(2),(o[0],y+15.24))
    s.wire((o[0],y+15.24),(o[0],y+7.62)); s.wire((o[0],y+7.62),o)
    s.wire(o,(160.02,o[1])); s.label(f"{b}_SUM",(160.02,o[1]),0,"hierarchical","output")
    if b in TPS: s.tp(f"TP{TPS[b]}",f"{b}_SUM",(152.4,o[1]),"up")
# spare half of U106: follower to ground
sp=OA("U91062",2,129.54,350.52)
s.wire(sp(5),lt(sp(5)),up(lt(sp(5)))); gnd(up(lt(sp(5))),180)
s.wire(sp(7),rt(sp(7),2.54),dn(rt(sp(7),2.54),5.08),(sp(6)[0]-2.54,sp(7)[1]+5.08),(sp(6)[0]-2.54,sp(6)[1]),sp(6))

# ------------------------------------------------------------- supplies and decoupling
Y2=375.92; x=210.82
for t in ("U91013","U91023","U91033","U91043","U91053","U91063"):
    u=OA(t,3,x,Y2); s.wire(u(8),up(u(8),5.08)); s.power("+15V",up(u(8),5.08)); s.wire(u(4),dn(u(4),5.08)); s.power("-15V",dn(u(4),5.08)); x+=17.78
x=330.2
for k in range(6):
    cp=C(f"C{141+2*k}","100n","SX-C-002",x,Y2-35.56,0); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{142+2*k}","100n","SX-C-002",x,Y2-17.78,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'bus.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_bus_wired.json','w'))
json.dump({"no_connect":NOCONNECT},open(T+'bus_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
