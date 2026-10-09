# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Headphones sheet, drawn with real wires.

Reference netlist: headphones_build.py (check_netlist.py headphones.json).
Left: the main/cue source switch (DG413 on PFL_ACT) and the volume pot block.
Middle: the TPA6120A2 with its input, feedback and output resistors.
Right: the protection relay (drawn rotated, commons on top) and the stereo jack.
Bottom: PFL-active LED, supplies and decoupling.
"""
import json,os
from schlayout import Sheet
R0805="Resistor_SMD:R_0805_2012Metric"; R2512="Resistor_SMD:R_2512_6332Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"; CP="Capacitor_SMD:CP_Elec_5x5.4"
JK="syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal"
VI={"Manufacturer":"Vishay"}
s=Sheet(); NC=[]
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,fp=R0805,**kw): return s.place("Device","R",ref,val,x,y,rot,fp=fp,props=P(pn,**kw))
def C(ref,val,pn,x,y,rot=0): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
def DG(ref,unit,x,y): return s.place("Analog_Switch","DG413xY",ref,"DG413DY",x,y,0,unit,SO16,P("SX-IC-005",**VI))
gnd=lambda at,rot=0: s.power("GNDA",at,rot)
up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])
def lab(at,name,rot=0): s.label(name,at,rot)
def hier(at,name,rot,shape): s.label(name,at,rot,"hierarchical",shape)
def ctrl(p): q=dn(p,2.54); s.wire(p,q,rt(q,5.08)); lab(rt(q,5.08),"PFL_ACT",0)

# ======================================================================== source switch: main while PFL_ACT is high, cue while it is low
for side,ymain,ycue,(um,umu,pm_in,pm_out,pm_c),(uc,ucu,pc_in,pc_out,pc_c),tp in (
        ("L",45.72,66.04,("U751",1,2,3,1),("U97513",3,10,11,9),"TP751"),
        ("R",111.76,132.08,("U97512",2,6,7,8),("U97514",4,15,14,16),"TP752")):
    hier((25.4,ymain),f"MAIN_{side}_OUT",180,"input"); hier((25.4,ycue),f"CUE_{side}_SUM",180,"input")
    a=DG(um,umu,55.88,ymain); s.wire((25.4,ymain),a(pm_in)); ctrl(a(pm_c))
    b=DG(uc,ucu,55.88,ycue); s.wire((25.4,ycue),b(pc_in)); ctrl(b(pc_c))
    sel=(76.2,ymain); s.wire(a(pm_out),sel); s.wire(b(pc_out),(sel[0],ycue),sel)
    s.wire(sel,(88.9,ymain)); lab((88.9,ymain),f"HP_{side}_SEL",0); s.tp(tp,f"HP_{side}_SEL",(sel[0],ymain+10.16),"right")
hier((25.4,160.02),"PFL_ACT",180,"input"); s.wire((25.4,160.02),(33.02,160.02)); lab((33.02,160.02),"PFL_ACT",0)
# volume pot block (dual 10k log): CCW = off
pt=s.place("Device","R_Potentiometer_Dual","RV751","PHONES 10k A dual",111.76,91.44,0,fp="Potentiometer_THT:Potentiometer_Alpha_RD902F-40-00D_Dual_Vertical",
           props=P("SX-POT-005",Manufacturer="Alpha",Note="Panel PHONES level; pin 3/6 = clockwise end"))
s.wire(pt(1),lt(pt(1),2.54),dn(lt(pt(1),2.54),2.54)); gnd(dn(lt(pt(1),2.54),2.54))
s.wire(pt(4),dn(pt(4),5.08)); gnd(dn(pt(4),5.08))
s.wire(pt(3),dn(pt(3),10.16)); lab(dn(pt(3),10.16),"HP_L_SEL",270)
s.wire(pt(6),rt(pt(6),5.08)); lab(rt(pt(6),5.08),"HP_R_SEL",0)
s.wire(pt(2),up(pt(2),7.62)); lab(up(pt(2),7.62),"HP_L_W",90)
s.wire(pt(5),up(pt(5),7.62)); lab(up(pt(5),7.62),"HP_R_W",90)

# ======================================================================== TPA6120A2: non-inverting gain 2 per side (TI SLOS431B Figure 14)
XT,YT=182.88,88.9
u=s.place("syntsamix","TPA6120A2","U752","TPA6120A2DWP",XT,YT,0,
          fp="Package_SO:SO-20-1EP_7.52x12.825mm_P1.27mm_EP6.045x12.09mm_Mask3.56x4.47mm_ThermalVias",
          props=P("SX-IC-015",Manufacturer="Texas Instruments",MPN="TPA6120A2DWPR",Supplier="LCSC",SupplierPN="C70439",Note="Thermal pad to AGND copper with vias (SLOS431B)"))
for pin,net in (("3","+15V"),("18","+15V")): s.wire(u(pin),up(u(pin),5.08)); s.power(net,up(u(pin),5.08))
for pin in ("1","20"): s.wire(u(pin),dn(u(pin),5.08)); s.power("-15V",dn(u(pin),5.08))
s.wire(u("21"),dn(u("21"),5.08)); gnd(dn(u("21"),5.08))
XO=205.74
for side,pin_p,pin_n,pin_o,rs,ri,rf,ro,yfb,sgn in (("L","4","5","2","R751","R752","R753","R754",58.42,-1),("R","17","16","19","R755","R756","R757","R758",119.38,1)):
    yp=u(pin_p)[1]
    s.wire((139.7,yp),(144.78,yp)); lab((139.7,yp),f"HP_{side}_W",180)
    r=R(rs,"51","SX-R-081",152.4,yp); s.wire((144.78,yp),r(1)); s.wire(r(2),u(pin_p))
    n=(165.1,u(pin_n)[1]); s.wire(u(pin_n),n,(n[0],yfb))
    f=R(rf,"1k","SX-R-035",XT,yfb); s.wire((n[0],yfb),f(1)); s.wire(f(2),(XO,yfb))
    o=(XO,u(pin_o)[1]); s.wire(u(pin_o),o); s.wire((XO,yfb),o)
    yi=n[1]+sgn*10.16; ri_=R(ri,"1k","SX-R-035",157.48,yi,270); s.wire((n[0],yi),ri_(1)); s.wire(ri_(2),lt(ri_(2),2.54)); gnd(lt(ri_(2),2.54),270)
    rr=R(ro,"39R2","SX-R-082",XO+10.16,o[1],fp=R2512,Note="2512 (1 W): full-level output into 32 ohm"); s.wire(o,rr(1))
    if side=="L": rol=rr(2)
    else: ror=rr(2)

# ======================================================================== relay and jack
Xr,Yr=264.16,68.58
k=s.place("Relay","G6K-2","K751","G6K-2F-Y DC12",Xr,Yr,180,fp="Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y",
          props=P("SX-K-001",Manufacturer="Omron",MPN="G6K-2F-Y DC12",Supplier="LCSC",SupplierPN="C397194",Note="Pole 2 (6/7/5) left, pole 1 (3/2/4) right; released = jack to AGND through 1k"))
s.wire(rol,(k("5")[0],rol[1]),k("5"))
yro=Yr+45.72; s.wire(ror,(226.06,ror[1]),(226.06,yro),(k("4")[0],yro),k("4"))
for pin,ref in (("7","R759"),("2","R760")):
    r=R(ref,"1k","SX-R-035",k(pin)[0],k(pin)[1]+3.81,0); s.wire(k(pin),r(1)); s.wire(r(2),dn(r(2),1.27)); gnd(dn(r(2),1.27))
kp=(k("1")[0],k("1")[1]+2.54); s.wire(k("1"),kp)
d=s.place("Device","D","D751","1N4148W",kp[0]+6.35,kp[1],0,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003")); s.wire(kp,d(1)); s.wire(d(2),(kp[0]+12.7,kp[1]))
xn=kp[0]+12.7; s.wire((xn,kp[1]),(xn,k("8")[1]-2.54),(k("8")[0],k("8")[1]-2.54),k("8"))
s.wire((xn,k("8")[1]-2.54),(xn+7.62,k("8")[1]-2.54)); hier((xn+7.62,k("8")[1]-2.54),"RLY_N",0,"input")
r=R("R761","330","SX-R-066",kp[0],kp[1]+7.62,0); s.wire(kp,r(1)); s.wire(r(2),dn(r(2),5.08)); s.power("+15V",dn(r(2),5.08),180)
j=s.place("Connector_Audio","AudioJack3_Switch","J751","PHONES",Xr-30.48,Yr-25.4,0,fp=JK,
          props=P("SX-CONN-015",Manufacturer="Rean",MPN="NYS216",Note="6.3 mm stereo headphone jack, front/top panel"))
s.wire(j("R"),(k("3")[0],j("R")[1]),k("3")); s.wire(j("T"),(k("6")[0],j("T")[1]),k("6"))
s.wire(j("S"),rt(j("S"),5.08)); gnd(rt(j("S"),5.08),90)
NC.extend([j("SN"),j("RN"),j("TN")])

# ======================================================================== PFL-active LED, supplies and decoupling
led=s.place("Device","LED","D752","PFL yellow",60.96,182.88,0,fp="LED_THT:LED_D3.0mm",props=P("SX-D-005",Note="PFL active: lights while PFL_ACT is low"))
s.wire(led(1),lt(led(1),7.62)); lab(lt(led(1),7.62),"PFL_ACT",180)
r=R("R762","1k5","SX-R-044",led(2)[0]+10.16,led(2)[1],270); s.wire(led(2),r(2)); s.wire(r(1),rt(r(1),2.54)); s.power("+5V",rt(r(1),2.54),270)
Y2=213.36; x=50.8
p=DG("U97515",5,x,Y2)
s.wire(p(13),up(p(13),5.08)); s.power("+15V",up(p(13),5.08)); s.wire(p(12),up(p(12),2.54),rt(up(p(12),2.54),5.08)); s.power("+5V",rt(up(p(12),2.54),5.08))
s.wire(p(5),dn(p(5),5.08)); gnd(dn(p(5),5.08)); s.wire(p(4),dn(p(4),2.54),rt(dn(p(4),2.54),5.08)); s.power("-15V",rt(dn(p(4),2.54),5.08))
x=91.44
for ref,net in (("C751","+15V"),("C752","+15V"),("C757","+15V")):
    c=C(ref,"100n","SX-C-002",x,Y2-7.62); s.power(net,c(1)); gnd(c(2)); x+=12.7
x=91.44
for ref in ("C753","C754","C758"):
    c=C(ref,"100n","SX-C-002",x,Y2+17.78); s.wire(c(1),up(c(1),2.54)); s.power("-15V",up(c(1),2.54),180); gnd(c(2)); x+=12.7
c=s.place("Device","C_Polarized","C755","10u 35V",x+5.08,Y2-7.62,0,fp=CP,props=P("SX-C-024",Manufacturer="ROQANG",MPN="RVT1V100M0505",Supplier="LCSC",SupplierPN="C72486",Note="TPA6120A2 bulk decoupling")); s.power("+15V",c(1)); gnd(c(2))
c=s.place("Device","C_Polarized","C756","10u 35V",x+5.08,Y2+17.78,0,fp=CP,props=P("SX-C-024",Manufacturer="ROQANG",MPN="RVT1V100M0505",Supplier="LCSC",SupplierPN="C72486",Note="TPA6120A2 bulk decoupling")); s.wire(c(1),up(c(1),5.08)); gnd(up(c(1),5.08),180)
s.wire(c(2),dn(c(2),5.08)); s.power("-15V",dn(c(2),5.08))

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'headphones.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_headphones_wired.json','w'))
json.dump({"no_connect":NC},open(T+'headphones_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
