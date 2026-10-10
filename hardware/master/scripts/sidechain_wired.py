# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Sidechain and ducking sheet, drawn with real wires.

Reference netlist: sidechain_build.py (check_netlist.py sidechain.json).
Top: sources (INT summer, BUS inverter, EXT jack and buffer), the two-stage selector,
the Sallen-Key LPF with its dual pot as a labelled block, bypass, the SC_DET buffer and
SC listen with the PFL_ACT driver. Bottom: the ducker (THRESHOLD, window comparator,
DEPTH, charge switches, hold, DECAY, SC_ENV buffer), buttons and supplies.
"""
import json,os
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
ST072={"Manufacturer":"STMicroelectronics","MPN":"TL072CDT","Supplier":"LCSC","SupplierPN":"C6961"}   # SX-IC-007 fee-free (decision 137)
SWFP="syntsamix:SW_Latching_8.5x8.5mm_CW_GPBS850N"; POT1="Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical"
s=Sheet(); NC=[]
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,**kw): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn,**kw))
def C(ref,val,pn,x,y,rot=90,fp=C0805): return s.place("Device","C",ref,val,x,y,rot,fp=fp,props=P(pn))
def TL(ref,unit,x,y): return s.place("Amplifier_Operational","TL072",ref,"TL072",x,y,0,unit,SO8,P("SX-IC-007",**ST072))
def DG(ref,unit,x,y): return s.place("Analog_Switch","DG413xY",ref,"DG413DY",x,y,0,unit,SO16,P("SX-IC-005",**VI,Assembly="hand (decision 150)",))
gnd=lambda at,rot=0: s.power("GNDA",at,rot)
up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])
def lab(at,name,rot=0): s.label(name,at,rot)
def hier(at,name,rot,shape): s.label(name,at,rot,"hierarchical",shape)
def gnd_plus(p): s.wire(p,lt(p),up(lt(p))); gnd(up(lt(p)),180)
def follower(a,pm,po,below=7.62):
    o=a(po); m=a(pm); xr=o[0]+5.08; xl=m[0]-2.54
    s.wire(o,(xr,o[1])); s.wire((xr,o[1]),(xr,o[1]+below),(xl,o[1]+below),(xl,m[1]),m)
    return (xr,o[1])
def inverting(ref,unit,pins,x_in,row,rin,rf,rpn,yf):
    """Inverting stage: input resistor ending at the summing node on `row`, op-amp, feedback resistor on row yf."""
    pm,pp,po=pins
    a=TL(ref,unit,x_in+27.94,row-2.54); nd=(x_in+12.7,row); s.wire(rin(2),nd,a(pm)); gnd_plus(a(pp))
    o=(a(po)[0]+7.62,a(po)[1]); s.wire(a(po),o)
    f=R(rf[0],rf[1],rpn,x_in+27.94,yf); s.wire(nd,(nd[0],yf),f(1)); s.wire(f(2),(o[0],yf),o)
    return o

# ======================================================================== sources
XA=25.4
hier((XA,40.64),"COMP_L_SUM",180,"input"); r=R("R501","20k","SX-R-051",45.72,40.64); s.wire((XA,40.64),r(1)); r501=r
hier((XA,50.8),"COMP_R_SUM",180,"input"); r=R("R502","20k","SX-R-051",45.72,50.8); s.wire((XA,50.8),r(1))
s.wire(r(2),(58.42,50.8),(58.42,40.64))
o_int=inverting("U501",1,(2,3,1),45.72,40.64,r501,("R503","10k"),"SX-R-002",27.94)
hier((XA,76.2),"SC_SUM",180,"input"); r=R("R504","10k","SX-R-002",45.72,76.2); s.wire((XA,76.2),r(1))
o_bus=inverting("U95012",2,(6,5,7),45.72,76.2,r,("R505","10k"),"SX-R-002",86.36)
# EXT jack: tip to the inverting buffer, tip switch to AGND, ring and sleeve to AGND, ring switch = plug detect
JK="syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal"
j=s.place("Connector_Audio","AudioJack3_Switch","J501","SC EXT IN",30.48,109.22,0,fp=JK,
          props=P("SX-CONN-015",Manufacturer="Rean",MPN="NYS216",Note="DC-coupled sidechain input; a plug overrides INT/BUS (ring switch RN)"))
sx=j("S")[0]+2.54
s.wire(j("S"),(sx,j("S")[1]),(sx,j("S")[1]-5.08)); gnd((sx,j("S")[1]-5.08),180); s.wire(j("R"),(sx,j("R")[1]),(sx,j("S")[1]))
s.wire(j("TN"),rt(j("TN"),2.54),dn(rt(j("TN"),2.54),5.08)); gnd(dn(rt(j("TN"),2.54),5.08))
NC.append(j("SN"))
s.wire(j("RN"),rt(j("RN"),7.62)); lab(rt(j("RN"),7.62),"EXT_SEL",0)
ye=j("T")[1]+10.16; tx=j("T")[0]+7.62; s.wire(j("T"),(tx,j("T")[1]),(tx,ye))
r=R("R506","100k","SX-R-007",53.34,ye); s.wire((tx,ye),r(1))
o_ext=inverting("U502",1,(2,3,1),53.34,ye,r,("R507","100k"),"SX-R-007",ye+12.7)
# plug detect pull-up and debounce
ne=(68.58,160.02); s.wire((38.1,ne[1]),ne); lab((38.1,ne[1]),"EXT_SEL",180)
r=R("R508","100k","SX-R-007",ne[0],ne[1]-7.62,0); s.wire(ne,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+5V",up(r(1),2.54))
c=C("C501","100n","SX-C-002",ne[0],ne[1]+7.62,0); s.wire(ne,c(1)); gnd(c(2))

# ======================================================================== selector (U506): BUS/INT, then EXT override
XS=124.46
u3=DG("U95063",3,XS,o_int[1]); s.wire(o_int,u3(10)); s.wire(u3(9),dn(u3(9),7.62)); lab(dn(u3(9),7.62),"BUS_CTRL",270)
u1=DG("U506",1,XS,o_bus[1]); s.wire(o_bus,u1(2)); s.wire(u1(1),dn(u1(1),7.62)); lab(dn(u1(1),7.62),"BUS_CTRL",270)
x1=XS+17.78; s.wire(u3(11),(x1,u3(11)[1])); s.wire(u1(3),(x1,u1(3)[1])); s.wire((x1,u3(11)[1]),(x1,u1(3)[1]))
ym=(o_int[1]+o_bus[1])/2+1.27
u4=DG("U95064",4,XS+30.48,ym); s.wire((x1,ym),u4(15)); s.wire(u4(16),dn(u4(16),7.62)); lab(dn(u4(16),7.62),"EXT_SEL",270)
u2=DG("U95062",2,XS+30.48,o_ext[1]); s.wire(o_ext,u2(6)); s.wire(u2(8),dn(u2(8),7.62)); lab(dn(u2(8),7.62),"EXT_SEL",270)
sel2=(XS+45.72,ym); s.wire(u4(14),sel2); s.wire(u2(7),(sel2[0],u2(7)[1]),sel2)

# ======================================================================== Sallen-Key LPF
YF=ym
r=R("R509","10k","SX-R-002",sel2[0]+12.7,YF); s.wire(sel2,r(1)); s.wire(r(2),dn(r(2),7.62)); lab(dn(r(2),7.62),"LPF_P1",270)
la=(sel2[0]+27.94,YF); s.wire((la[0]-5.08,YF),la); lab((la[0]-5.08,YF),"LPF_A",180)
r=R("R510","10k","SX-R-002",la[0]+10.16,YF); s.wire(la,r(1)); s.wire(r(2),dn(r(2),7.62)); lab(dn(r(2),7.62),"LPF_P2",270)
lb=(la[0]+33.02,YF); s.wire((lb[0]-5.08,YF),lb); lab((lb[0]-5.08,YF),"LPF_B",180)
# 22n as two 47n C0G in series, 23.5 nF (decision 147): Q 0.707, sweep about 3 % lower
c=C("C503","47n C0G","SX-C-016",lb[0],YF+10.16,0); s.wire(lb,c(1))
c2=C("C521","47n C0G","SX-C-016",lb[0],YF+20.32,0); s.wire(c(2),c2(1)); gnd(c2(2))
a=TL("U95022",2,lb[0]+17.78,YF+2.54); s.wire(lb,a(5)); lo=follower(a,6,7)
c=C("C502","47n C0G","SX-C-016",(la[0]+lo[0])/2,YF-12.7); s.wire(la,(la[0],YF-12.7),c(1)); s.wire(c(2),(lo[0],YF-12.7),lo)
# dual pot as a labelled block: segment wiper-pin 3 per gang (pin 1 tied to the wiper)
pt=s.place("Device","R_Potentiometer_Dual","RV501","SC LPF B100K dual",sel2[0]+40.64,YF+30.48,0,
           fp="Potentiometer_THT:Potentiometer_Alpha_RD902F-40-00D_Dual_Vertical",
           props=P("SX-POT-015",Manufacturer="Alpha",MPN="RD902F-40-15K-B100K-0057",Supplier="Thonk",Note="Panel SC LPF: linear (B) taper, CW = 478 Hz, middle 80 Hz, CCW = 44 Hz (decisions 138, 147)"))
for pin,name,d in (("1","LPF_A","l"),("2","LPF_A","u"),("3","LPF_P1","d"),("4","LPF_B","d2"),("5","LPF_B","u"),("6","LPF_P2","r")):
    p=pt(pin)
    if d=="l": e=lt(p,5.08); rot=180
    elif d=="r": e=rt(p,5.08); rot=0
    elif d=="u": e=up(p,7.62); rot=90
    elif d=="d": e=dn(p,7.62); rot=270
    else: e=dn(p,12.7); rot=270
    s.wire(p,e); lab(e,name,rot)

# ======================================================================== bypass, SC_DET buffer, SC listen
XB=lo[0]+25.4
b3=DG("U95073",3,XB,lo[1]); s.wire(lo,b3(10)); s.wire(b3(9),dn(b3(9),7.62)); lab(dn(b3(9),7.62),"BYP_CTRL",270)
b1=DG("U507",1,XB,YF-27.94); s.wire(sel2,(sel2[0],b1(2)[1]),b1(2)); s.wire(b1(1),dn(b1(1),5.08)); lab(dn(b1(1),5.08),"BYP_CTRL",270)
fi=(XB+15.24,lo[1]); s.wire(b3(11),fi); s.wire(b1(3),(fi[0],b1(3)[1]),fi)
a=TL("U503",1,fi[0]+20.32,fi[1]+2.54); s.wire(fi,a(3)); so=follower(a,2,1)
sd=(so[0]+25.4,so[1]); s.wire(so,sd); hier(sd,"SC_DET",0,"output"); s.tp("TP501","SC_DET",(so[0]+12.7,so[1]),"up")
s.wire((so[0]+5.08,so[1]),(so[0]+5.08,so[1]-10.16)); lab((so[0]+5.08,so[1]-10.16),"SC_DET",90)
b2=DG("U95072",2,so[0]+15.24,so[1]+25.4); s.wire((so[0],so[1]+7.62),(so[0],b2(6)[1]),b2(6))
s.wire(b2(8),dn(b2(8),7.62)); lab(dn(b2(8),7.62),"LISTEN_CTRL",270)
ls=(b2(7)[0]+5.08,b2(7)[1]); s.wire(b2(7),ls)
for k,(ref,bus) in enumerate((("R511","CUE_L"),("R512","CUE_R"))):
    y=ls[1]+k*10.16; r=R(ref,"22k","SX-R-047",ls[0]+10.16,y)
    if k: s.wire(ls,(ls[0],y))
    s.wire((ls[0],y),r(1)); s.wire(r(2),(r(2)[0]+7.62,y)); hier((r(2)[0]+7.62,y),bus,0,"bidirectional")
# PFL_ACT open-collector driver
yq=ls[1]+40.64; r=R("R513","10k","SX-R-002",ls[0]+2.54,yq); s.wire((ls[0]-10.16,yq),r(1)); lab((ls[0]-10.16,yq),"LISTEN_CTRL",180)
q=s.place("Transistor_BJT","Q_NPN_BEC","Q501","MMBT3904",r(2)[0]+7.62,yq,0,fp="Package_TO_SOT_SMD:SOT-23",props=P("SX-Q-001",Manufacturer="onsemi",MPN="MMBT3904LT1G"))
s.wire(r(2),q(1)); s.wire(q(2),dn(q(2),2.54)); s.power("GNDPWR",dn(q(2),2.54))   # emitter to PGND (decision 98)
s.wire(q(3),up(q(3),7.62)); hier(up(q(3),7.62),"PFL_ACT",90,"bidirectional")
# spare section of U507
sp=DG("U95074",4,XB+71.12,YF-27.94)
for n,(px,py,ang) in pins_of("Analog_Switch","DG413xY",4).items():
    p=sp(n); e={0:lt(p,5.08),180:rt(p,5.08),90:dn(p,5.08)}[int(ang)]; s.wire(p,e); gnd(e)

# ======================================================================== ducker
YD=190.5
rv=s.place("Device","R_Potentiometer","RV502","THRESHOLD 10k log",40.64,YD,0,fp=POT1,
           props=P("SX-POT-009",Note="Panel THRESHOLD: log (A) taper, CCW = 0.1 V, CW = 5 V peak"))
r=R("R515","200","SX-R-010",rv(1)[0],rv(1)[1]-7.62,0); s.wire(rv(1),r(2)); s.wire(r(1),up(r(1),5.08)); gnd(up(r(1),5.08),180)
r=R("R514","20k","SX-R-051",rv(3)[0],rv(3)[1]+7.62,0); s.wire(rv(3),r(1)); s.wire(r(2),dn(r(2),5.08)); s.power("+15V",dn(r(2),5.08),180)
thr=(58.42,YD); s.wire(rv(2),thr)
c1=TL("U504",1,96.52,YD-2.54); s.wire(thr,c1(2)); s.wire(c1(3),lt(c1(3),7.62)); lab(lt(c1(3),7.62),"SC_DET",180)
s.wire(c1(1),rt(c1(1),7.62)); lab(rt(c1(1),7.62),"TRIG1",0)
r=R("R516","100k","SX-R-007",68.58,YD+20.32); s.wire(thr,(thr[0],YD+20.32),r(1))
o_thrn=inverting("U95032",2,(6,5,7),68.58,YD+20.32,r,("R517","100k"),"SX-R-007",YD+30.48)
c2=TL("U95042",2,129.54,o_thrn[1]+2.54); s.wire(o_thrn,c2(5)); s.wire(c2(6),lt(c2(6),7.62)); lab(lt(c2(6),7.62),"SC_DET",180)
s.wire(c2(7),rt(c2(7),7.62)); lab(rt(c2(7),7.62),"TRIG2",0)
# DEPTH
YP=YD+66.04
rv=s.place("Device","R_Potentiometer","RV503","DEPTH 10k lin",40.64,YP,0,fp=POT1,props=P("SX-POT-006",Note="Panel DEPTH: CCW = 0 dB, CW = 40 dB of ducking"))
s.wire(rv(1),up(rv(1),5.08)); gnd(up(rv(1),5.08),180)
r=R("R518","27k","SX-R-065",rv(3)[0],rv(3)[1]+7.62,0); s.wire(rv(3),r(1)); s.wire(r(2),dn(r(2),5.08)); s.power("-15V",dn(r(2),5.08))   # DEPTH 0 to -4 V (decision 97)
a=TL("U505",1,66.04,YP+2.54); s.wire(rv(2),a(3)); dep=follower(a,2,1)
YQ=dep[1]
# charge switches
d1=DG("U508",1,104.14,YQ); s.wire(dep,(91.44,YQ)); s.wire((91.44,YQ),d1(2)); s.wire(d1(1),dn(d1(1),7.62)); lab(dn(d1(1),7.62),"TRIG1",270)
d2=DG("U95082",2,104.14,YQ+20.32); s.wire((91.44,YQ),(91.44,YQ+20.32),d2(6)); s.wire(d2(8),dn(d2(8),7.62)); lab(dn(d2(8),7.62),"TRIG2",270)
chg=(119.38,YQ); s.wire(d1(3),chg); s.wire(d2(7),(chg[0],d2(7)[1]),chg)
r=R("R519","470","SX-R-055",129.54,YQ); s.wire(chg,r(1)); hold=(139.7,YQ); s.wire(r(2),hold)
c=C("C504","2u2","SX-C-015",hold[0],YQ+10.16,0); s.wire(hold,c(1)); gnd(c(2))
r=R("R520","22k","SX-R-047",152.4,YQ+10.16,0); s.wire(hold,(152.4,YQ),r(1)); dk=(152.4,YQ+20.32); s.wire(r(2),dk)
rd=s.place("Device","R_Potentiometer","RV504","DECAY 500k log",152.4,YQ+30.48,180,fp=POT1,
           props=P("SX-POT-010",Note="Panel DECAY: log (A) taper, CCW = 48 ms, CW = 1.15 s time constant"))
s.wire(dk,rd(3))
s.wire(rd(2),lt(rd(2),2.54)); s.wire(lt(rd(2),2.54),(rd(2)[0]-2.54,rd(3)[1]-1.27),(rd(3)[0],rd(3)[1]-1.27))
s.wire(rd(1),dn(rd(1),2.54)); gnd(dn(rd(1),2.54))
# SC_ENV follower, feedback taken after R521 so the line stays low impedance under up to 18 loads of 30k1 (decision 97)
a=TL("U95052",2,180.34,YQ+2.54); s.wire((152.4,YQ),a(5)); o=a(7); m=a(6)
r=R("R521","100","SX-R-001",o[0]+10.16,o[1]); s.wire(o,r(1)); n=(r(2)[0]+2.54,o[1]); s.wire(r(2),n)
s.wire(n,(n[0],o[1]+7.62),(m[0]-2.54,o[1]+7.62),(m[0]-2.54,m[1]),m)
tp=(n[0]+5.08,o[1]); q=(n[0]+10.16,o[1]); se=(n[0]+17.78,o[1]); s.wire(n,tp); s.wire(tp,q); s.wire(q,se)
hier(se,"SC_ENV",0,"output"); s.tp("TP502","SC_ENV",tp,"up")
# Schottky clamp: SC_ENV cannot rise above about +0.3 V (pin 1 = cathode to AGND, pin 2 = anode on SC_ENV)
dc=(q[0]-3.81,o[1]+15.24); s.wire(q,(q[0],dc[1]))
dd=s.place("Device","D","D504","BAT54W",dc[0],dc[1],0,fp="Diode_SMD:D_SOD-123",props=P("SX-D-014",Manufacturer="hongjiacheng",MPN="BAT54W",Supplier="LCSC",SupplierPN="C7502705",Note="SC_ENV clamp to AGND (decision 97)"))
s.wire(dd(1),dn(dd(1),2.54)); gnd(dn(dd(1),2.54))
# spare sections of U508
for i,(ref,unit) in enumerate((("U95083",3),("U95084",4))):
    sp=DG(ref,unit,104.14+i*25.4,YQ+45.72)
    for n,(px,py,ang) in pins_of("Analog_Switch","DG413xY",unit).items():
        p=sp(n); e={0:lt(p,5.08),180:rt(p,5.08),90:dn(p,5.08)}[int(ang)]; s.wire(p,e); gnd(e)

# ======================================================================== buttons
# button LED colours as the channel (decision 117): SC BUS green, LPF bypass white (as FILTER BYPASS), SC LISTEN yellow (a listen, as PFL)
LEDPN={"BUS":P("SX-D-011",Manufacturer="Hubei KENTO",MPN="KT-0805G",Supplier="LCSC",SupplierPN="C2297"),"BYP":P("SX-D-017",Manufacturer="Hubei KENTO",MPN="KT-0805W",Supplier="LCSC",SupplierPN="C34499"),"LISTEN":P("SX-D-016",Manufacturer="Hubei KENTO",MPN="KT-0805Y",Supplier="LCSC",SupplierPN="C2296")}
def button(name,title,sw,led,rl,rp,x,y):
    b=s.place("Switch","SW_Push_DPDT",sw,f"{title} (latching)",x,y,0,fp=SWFP,
              props=P("SX-SW-001",Manufacturer="CW Industries",MPN="GPBS850N",Supplier="Electrokit",SupplierPN="41012905"))
    s.wire(b(2),lt(b(2),5.08)); s.power("+5V",lt(b(2),5.08)); s.wire(b(5),lt(b(5),5.08)); s.power("GNDPWR",lt(b(5),5.08))
    nd=(b(3)[0]+10.16,b(3)[1]); s.wire(b(3),nd,rt(nd,10.16)); lab(rt(nd,10.16),f"{name}_CTRL",0)
    r=R(rp,"100k","SX-R-007",nd[0],nd[1]-10.16,0); s.wire(nd,r(2))
    g=lt(up(r(1),5.08),5.08); s.wire(r(1),up(r(1),5.08),g); s.power("GNDPWR",g)   # PGND (decision 98); symbol points down beside the resistor
    ld=s.place("Device","LED",led,f"{title} LED",b(6)[0]+22.86,b(6)[1],0,fp="LED_SMD:LED_0805_2012Metric",props=LEDPN[name])
    s.wire(b(6),ld(1)); r=R(rl,"12k","SX-R-008",ld(2)[0]+8.89,b(6)[1],270); s.wire(ld(2),r(2)); s.wire(r(1),rt(r(1),3.81)); s.power("+15V",rt(r(1),3.81),270)
    NC.extend([b(1),b(4)])
button("BUS","SC BUS","SW501","D501","R522","R523",261.62,198.12)
button("BYP","SC LPF BYPASS","SW502","D502","R524","R525",261.62,236.22)
button("LISTEN","SC LISTEN","SW503","D503","R526","R527",261.62,274.32)

# ======================================================================== supplies and decoupling
Y2=375.92; x=33.02
for ref in ("U95013","U95023","U95033","U95043","U95053"):
    p=TL(ref,3,x,Y2); s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
for ref in ("U95065","U95075","U95085"):
    p=DG(ref,5,x+5.08,Y2-7.62)
    s.wire(p(13),up(p(13),5.08)); s.power("+15V",up(p(13),5.08)); s.wire(p(12),up(p(12),2.54),rt(up(p(12),2.54),5.08)); s.power("+5V",rt(up(p(12),2.54),5.08))
    s.wire(p(5),dn(p(5),5.08)); gnd(dn(p(5),5.08)); s.wire(p(4),dn(p(4),2.54),rt(dn(p(4),2.54),5.08)); s.power("-15V",rt(dn(p(4),2.54),5.08)); x+=22.86
x+=5.08
for k in range(8):
    cp=C(f"C{505+2*k}","100n","SX-C-002",x,Y2-20.32,0); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{506+2*k}","100n","SX-C-002",x,Y2+5.08,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'sidechain.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_sidechain_wired.json','w'))
json.dump({"no_connect":NC},open(T+'sidechain_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
