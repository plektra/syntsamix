# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Routing sheet, drawn with real wires.

Reference netlist: routing_build.py (check_netlist.py routing.json).
Layout: pre-fader buffers (top left), bus assign (top middle), AUX sends with
their pre/post jumpers (right), PFL and sidechain send with the PFL_ACT driver
(middle), buttons and supplies (bottom).
"""
import json,os
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,**k): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn,**k))
def C(ref,val,pn,x,y,rot=0): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
def gnd(at,rot=0): s.power("GNDA",at,rot)
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])
def lab(p,name,rot): s.label(name,p,rot)
def hier(p,name,rot,shape): s.label(name,p,rot,"hierarchical",shape)
NOCONNECT=[]
BUS="22k"

# ------------------------------------------------------------- pre-fader buffers
for Pn,ref,unit,pins,y in (("L","U301",1,(3,2,1),50.8),("R","U93012",2,(5,6,7),76.2)):
    a=s.place("Amplifier_Operational","NE5532",ref,"NE5532",45.72,y+2.54,0,unit,SO8,P("SX-IC-004",**TI))
    pp,pm,po=pins
    s.wire((25.4,y),a(pp)); hier((25.4,y),f"{Pn}_POSTFILT",180,"input")
    o=(55.88,a(po)[1]); s.wire(a(po),o,(68.58,o[1])); hier((68.58,o[1]),f"{Pn}_PRE",0,"output")
    s.tp("TP301" if Pn=="L" else "TP302",f"{Pn}_PRE",(63.5,o[1]),"up")
    s.wire(o,(o[0],o[1]+7.62),(35.56,o[1]+7.62),(35.56,a(pm)[1]),a(pm))

# ------------------------------------------------------------- bus assign (DG413, pressed = compressor bus)
def switch(lib,ref,unit,x,y,pn,left,right,ctrl,ctrl_net):
    d=s.place("Analog_Switch",lib,ref,lib[:5]+("DY" if lib=="DG413xY" else "DY"),x,y,0,unit,SO16,P(pn,**VI))
    s.wire(d(ctrl),dn(d(ctrl),2.54)); lab(dn(d(ctrl),2.54),ctrl_net,270)
    return d(left),d(right)
for Pn,rref,y,main,comp in (("L","R301",50.8,("U93024",4,15,14,16),("U302",1,2,3,1)),
                            ("R","R302",101.6,("U93023",3,10,11,9),("U93022",2,6,7,8))):
    hier((101.6,y),f"{Pn}_POSTFADE",180,"input")
    r=R(rref,BUS,"SX-R-047",114.3,y); s.wire((101.6,y),r(1))
    node=(124.46,y); s.wire(r(2),node)
    for (ref,unit,pl,pr,pc),yy,bus in ((main,y,f"MAIN_{Pn}"),(comp,y+20.32,f"COMP_{Pn}")):
        l,rr=switch("DG413xY",ref,unit,137.16,yy,"SX-IC-005",pl,pr,pc,"COMP_CTRL")
        s.wire(node,(node[0],yy)) if yy!=y else None
        s.wire((node[0],yy),l); s.wire(rr,(154.94,yy)); hier((154.94,yy),bus,0,"output")

# ------------------------------------------------------------- PFL to the cue bus (NO sections 1, 4), SC send (NC section 2, on while SW302 pin 1 is open)
def tap(name,ref,val,pn,y):
    lab((101.6,y),name,180); r=R(ref,val,pn,114.3,y); s.wire((101.6,y),r(1)); return r(2)
for Pn,rref,y,(ref,unit,pl,pr,pc) in (("L","R303",147.32,("U303",1,2,3,1)),("R","R304",167.64,("U93032",2,6,7,8))):
    e=tap(f"{Pn}_PRE",rref,BUS,"SX-R-047",y)
    l,rr=switch("DG413xY",ref,unit,137.16,y,"SX-IC-005",pl,pr,pc,"PFL_CTRL")
    s.wire(e,l); s.wire(rr,(154.94,y)); hier((154.94,y),f"CUE_{Pn}",0,"output")
e1=tap("L_PRE","R305","47k","SX-R-032",193.04); e2=tap("R_PRE","R306","47k","SX-R-032",203.2)
nd=(124.46,193.04); s.wire(e1,nd); s.wire(e2,(nd[0],203.2),nd)
l,rr=switch("DG413xY","U93034",4,137.16,193.04,"SX-IC-005",15,14,16,"SC_OFF")
s.wire(nd,l); s.wire(rr,(154.94,193.04)); hier((154.94,193.04),"SC",0,"output")
u=s.place("Analog_Switch","DG413xY","U93033","DG413DY",137.16,223.52,0,3,SO16,P("SX-IC-005",**VI))
for n,(px,py,ang) in pins_of("Analog_Switch","DG413xY",3).items():
    p=u(n); e={0:lt(p,5.08),180:rt(p,5.08),90:dn(p,5.08)}[int(ang)]; s.wire(p,e); gnd(e)
# PFL_ACT open-collector driver
rb=R("R311","10k","SX-R-002",175.26,157.48); lab((166.37,157.48),"PFL_CTRL",180); s.wire((166.37,157.48),rb(1))
q=s.place("Transistor_BJT","Q_NPN_BEC","Q301","MMBT3904",190.5,157.48,0,fp="Package_TO_SOT_SMD:SOT-23",props=P("SX-Q-001",Manufacturer="onsemi",MPN="MMBT3904LT1G"))
s.wire(rb(2),q(1)); s.wire(q(2),dn(q(2),2.54)); pgnd(dn(q(2),2.54))   # PGND (decision 98)
s.wire(q(3),up(q(3),7.62)); hier(up(q(3),7.62),"PFL_ACT",90,"output")

# ------------------------------------------------------------- AUX sends: pre/post jumper and dual-gang level pot
for n,j,rv,rl,rr,YA in ((1,"J301","RV301","R307","R308",50.8),(2,"J302","RV302","R309","R310",111.76)):
    XA=228.6
    h=s.place("Connector_Generic","Conn_02x03_Odd_Even",j,f"AUX{n} PRE 1-3/2-4, POST 3-5/4-6",XA,YA,0,
              fp="Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical",props=P("SX-CONN-006",Note="Default: POST (jumpers on 3-5 and 4-6)"))
    for pin,net in (("1","L_PRE"),("3",f"L_AUX{n}_SRC"),("5","L_POSTFADE")):
        s.wire(h(pin),lt(h(pin),7.62)); lab(lt(h(pin),7.62),net,180)
    for pin,net in (("2","R_PRE"),("4",f"R_AUX{n}_SRC"),("6","R_POSTFADE")):
        s.wire(h(pin),rt(h(pin),7.62)); lab(rt(h(pin),7.62),net,0)
    XP,YP=XA+60.96,YA+7.62
    p=s.place("Device","R_Potentiometer_Dual",rv,f"AUX{n} 10k A dual",XP,YP,0,fp="Potentiometer_THT:Potentiometer_Alpha_RD902F-40-00D_Dual_Vertical",
              props=P("SX-POT-013",Manufacturer="Alpha",MPN="RD902F-40-15K-A10K-0057",Supplier="Thonk",Note="Panel AUX level; pin 3/6 = clockwise end"))
    s.wire(p(1),lt(p(1),2.54),dn(lt(p(1),2.54),2.54)); gnd(dn(lt(p(1),2.54),2.54))
    s.wire(p(4),dn(p(4),5.08)); gnd(dn(p(4),5.08))
    s.wire(p(3),dn(p(3),5.08)); lab(dn(p(3),5.08),f"L_AUX{n}_SRC",270)
    s.wire(p(6),rt(p(6),5.08)); lab(rt(p(6),5.08),f"R_AUX{n}_SRC",0)
    for wpin,ref,bus in ((2,rl,f"AUX{n}_L"),(5,rr,f"AUX{n}_R")):
        w=p(wpin); r=R(ref,BUS,"SX-R-047",w[0],w[1]-10.16,0); s.wire(w,r(2))
        s.wire(r(1),up(r(1),2.54)); hier(up(r(1),2.54),bus,90,"output")

# ------------------------------------------------------------- buttons
def button(name,sw,led,rl,rp,x,y,title,ctrl=3,net=None):
    b=s.place("Switch","SW_Push_DPDT",sw,f"{title} (latching)",x,y,0,fp="syntsamix:SW_Latching_8.5x8.5mm_CW_GPBS850N",props=P("SX-SW-001",Manufacturer="CW Industries",MPN="GPBS850N",Supplier="Electrokit",SupplierPN="41012905"))
    s.wire(b(2),lt(b(2),5.08)); s.power("+5V",lt(b(2),5.08))
    s.wire(b(5),lt(b(5),5.08)); pgnd(lt(b(5),5.08))
    nd=(b(ctrl)[0]+10.16,b(ctrl)[1]); s.wire(b(ctrl),nd,rt(nd,10.16)); lab(rt(nd,10.16),net or f"{name}_CTRL",0)
    r=R(rp,"100k","SX-R-007",nd[0],nd[1]-7.62,0); s.wire(nd,r(2))
    g=lt(up(r(1),2.54),5.08); s.wire(r(1),up(r(1),2.54),g); pgnd(g)   # PGND (decision 98); symbol points down beside the resistor
    ld=s.place("Device","LED",led,f"{title} LED",b(6)[0]+22.86,b(6)[1],0,fp="LED_SMD:LED_0805_2012Metric",props=LEDPN[title])
    s.wire(b(6),ld(1))
    r2=R(rl,"12k","SX-R-008",ld(2)[0]+8.89,b(6)[1],270); s.wire(ld(2),r2(2)); s.wire(r2(1),rt(r2(1),3.81)); s.power("+15V",rt(r2(1),3.81),270)
    NOCONNECT.extend([b(4-ctrl),b(4)])   # the unused throw of the logic pole
LEDPN={"PFL":P("SX-D-016",Manufacturer="Hubei KENTO",MPN="KT-0805Y",Supplier="LCSC",SupplierPN="C2296"),"SC SEND":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297"),"COMP BUS":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297")}   # button LED colours (user, 2026-10-09)
button("PFL","SW301","D301","R312","R313",40.64,279.4,"PFL")
button("SC","SW302","D302","R314","R315",137.16,279.4,"SC SEND",ctrl=1,net="SC_OFF")   # released = 1-2 closed: SC_OFF high, NC section off
button("COMP","SW303","D303","R316","R317",233.68,279.4,"COMP BUS")

# ------------------------------------------------------------- supplies and decoupling
Y2=340.36
u=s.place("Amplifier_Operational","NE5532","U93013","NE5532",50.8,Y2,0,3,SO8,P("SX-IC-004",**TI))
s.wire(u(8),up(u(8),5.08)); s.power("+15V",up(u(8),5.08)); s.wire(u(4),dn(u(4),5.08)); s.power("-15V",dn(u(4),5.08))
for ref,lib,pn,x in (("U93025","DG413xY","SX-IC-005",76.2),("U93035","DG413xY","SX-IC-005",101.6)):
    u=s.place("Analog_Switch",lib,ref,lib[:5]+"DY",x,Y2,0,5,SO16,P(pn,**VI))
    s.wire(u(13),up(u(13),5.08)); s.power("+15V",up(u(13),5.08))
    s.wire(u(12),up(u(12),2.54),rt(up(u(12),2.54),5.08)); s.power("+5V",rt(up(u(12),2.54),5.08))
    s.wire(u(5),dn(u(5),5.08)); gnd(dn(u(5),5.08))
    s.wire(u(4),dn(u(4),2.54),rt(dn(u(4),2.54),5.08)); s.power("-15V",rt(dn(u(4),2.54),5.08))
x=137.16
for k in (301,303,305):
    cp=C(f"C{k}","100n","SX-C-002",x,Y2-7.62); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{k+1}","100n","SX-C-002",x,Y2+20.32); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'routing.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_routing_wired.json','w'))
json.dump({"no_connect":NOCONNECT},open(T+'routing_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
