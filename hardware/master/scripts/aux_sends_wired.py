# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""AUX sends sheet, drawn with real wires (both sends on one sheet).

Reference netlist: aux_sends_build.py (check_netlist.py aux_sends.json).
Per send: the dual master pot as a labelled block (left), the L stage with its mono
switches below it, the R stage, then the impedance-balanced output jacks (right) with
the plug-detect pull-up. Supplies at the bottom.
"""
import json,os
from schlayout import Sheet
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"; JK="syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal"
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
s=Sheet(); NC=[]
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,**kw): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn,**kw))
def C(ref,val,pn,x,y,rot=90): return s.place("Device","C",ref,val,x,y,rot,fp=C0805,props=P(pn))
def NE(ref,unit,x,y): return s.place("Amplifier_Operational","NE5532",ref,"NE5532",x,y,0,unit,SO8,P("SX-IC-004",**TI))
def DG(ref,unit,x,y): return s.place("Analog_Switch","DG413xY",ref,"DG413DY",x,y,0,unit,SO16,P("SX-IC-005",**VI,Assembly="hand (decision 150)",))
gnd=lambda at,rot=0: s.power("GNDA",at,rot)
up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])
def lab(at,name,rot=0): s.label(name,at,rot)
def gnd_plus(p): s.wire(p,lt(p),up(lt(p))); gnd(up(lt(p)),180)
def ctrl(p,name): q=dn(p,2.54); s.wire(p,q,rt(q,5.08)); lab(rt(q,5.08),name,0)

def stage(ref,unit,pins,y,src,rin,rf):
    """Inverting 47k/47k stage on row y: label src -> rin -> N -> op-amp; feedback rf below. Returns (N column x, O node)."""
    pm,pp,po=pins
    s.wire((78.74,y),(83.82,y)); lab((78.74,y),src,180)
    r=R(rin,"47k","SX-R-032",91.44,y); s.wire((83.82,y),r(1)); nd=(101.6,y)
    a=NE(ref,unit,116.84,y-2.54); s.wire(r(2),nd,a(pm)); gnd_plus(a(pp))
    o=(142.24,a(po)[1]); s.wire(a(po),o)
    f=R(rf,"47k","SX-R-032",121.92,y+10.16); s.wire(nd,(nd[0],y+10.16),f(1)); s.wire(f(2),(o[0],y+10.16),o)
    return nd,o

def output(o,jref,title,rt_ref,rr_ref,tp,tpname,det=None):
    """Impedance-balanced output: O -> 100R -> tip; ring -> 100R -> AGND. Jack pins face right, tip routed round the right."""
    yj=o[1]+12.7
    j=s.place("Connector_Audio","AudioJack3_Switch",jref,title,190.5,yj,0,fp=JK,props=P("SX-CONN-015",Manufacturer="Rean",MPN="NYS216"))
    r=R(rt_ref,"100","SX-R-001",157.48,o[1]); s.wire(o,r(1)); xv=236.22
    s.wire(r(2),(xv,o[1]),(xv,j("T")[1]),j("T"))
    s.tp(tp,tpname,(150.62,o[1]),"up")
    s.wire(j("S"),rt(j("S"),2.54),up(rt(j("S"),2.54),2.54)); gnd(up(rt(j("S"),2.54),2.54),180)
    rr=R(rr_ref,"100","SX-R-001",j("R")[0]+25.4,j("R")[1]); s.wire(j("R"),rr(1)); s.wire(rr(2),rt(rr(2),2.54)); gnd(rt(rr(2),2.54),90)
    if det: s.wire(j("RN"),rt(j("RN"),2.54)); lab(rt(j("RN"),2.54),det,0)
    else: NC.append(j("RN"))
    NC.extend([j("TN"),j("SN")])

for n,B,y0 in ((1,600,30.48),(2,620,215.9)):
    r=lambda k:f"R{B+k}"
    # master pot block
    p=s.place("Device","R_Potentiometer_Dual",f"RV{B+1}",f"AUX{n} SEND 10k A dual",45.72,y0+40.64,0,
              fp="Potentiometer_THT:Potentiometer_Alpha_RD902F-40-00D_Dual_Vertical",props=P("SX-POT-005",Manufacturer="Alpha",Note="Panel AUX send master; pin 3/6 = clockwise end"))
    s.wire(p(1),lt(p(1),2.54),dn(lt(p(1),2.54),2.54)); gnd(dn(lt(p(1),2.54),2.54))
    s.wire(p(4),dn(p(4),5.08)); gnd(dn(p(4),5.08))
    s.wire(p(3),dn(p(3),10.16)); s.label(f"AUX{n}_L_SUM",dn(p(3),10.16),270,"hierarchical","input")
    s.wire(p(6),rt(p(6),5.08)); s.label(f"AUX{n}_R_SUM",rt(p(6),5.08),0,"hierarchical","input")
    s.wire(p(2),up(p(2),7.62)); lab(up(p(2),7.62),f"L{n}_W",90)
    s.wire(p(5),up(p(5),7.62)); lab(up(p(5),7.62),f"R{n}_W",90)
    # L stage, feedback-halving and mono-add switches below it
    yl=y0+20.32
    nd,o=stage(f"U{B+1}",1,(2,3,1),yl,f"L{n}_W",r(1),r(2))
    (ma,mau),(fb,fbu)={1:(("U641",1),("U96412",2)),2:(("U96413",3),("U96414",4))}[n]
    pins={1:(2,3,1),2:(6,7,8),3:(10,11,9),4:(15,14,16)}
    sw=DG(fb,fbu,116.84,yl+20.32); pl,pr,pc=pins[fbu]
    s.wire((nd[0],yl+10.16),(nd[0],yl+20.32),sw(pl)); rr=R(r(4),"47k","SX-R-032",133.35,yl+20.32); s.wire(sw(pr),rr(1)); s.wire(rr(2),(o[0],yl+20.32),(o[0],yl+10.16))
    ctrl(sw(pc),f"DET{n}" if n==2 else "MONO1")
    sw=DG(ma,mau,116.84,yl+35.56); pl,pr,pc=pins[mau]
    s.wire((nd[0],yl+20.32),(nd[0],yl+35.56),sw(pl)); rr=R(r(3),"47k","SX-R-032",133.35,yl+35.56); s.wire(sw(pr),rr(1))
    s.wire(rr(2),rt(rr(2),7.62)); lab(rt(rr(2),7.62),f"R{n}_W",0)
    ctrl(sw(pc),f"DET{n}" if n==2 else "MONO1")
    output(o,f"J{B+1}",f"AUX{n} SEND L/MONO",r(7),r(8),f"TP{B+1}",f"L{n}_O")
    # R stage
    yr=yl+66.04
    nd2,o2=stage(f"U9{B+1}2",2,(6,5,7),yr,f"R{n}_W",r(5),r(6))
    output(o2,f"J{B+2}",f"AUX{n} SEND R",r(9),r(10),f"TP{B+2}",f"R{n}_O",det=f"DET{n}")
    # plug-detect pull-up: high = R plugged (stereo), low = mono
    dd=(170.18,yr+30.48); s.wire((157.48,dd[1]),dd); lab((157.48,dd[1]),f"DET{n}",180)
    rp=R(r(11),"100k","SX-R-007",dd[0],dd[1]-7.62,0); s.wire(dd,rp(2)); s.wire(rp(1),up(rp(1),2.54)); s.power("+5V",up(rp(1),2.54))
    c=C(f"C{B+1}","100n","SX-C-002",dd[0],dd[1]+7.62,0); s.wire(dd,c(1)); gnd(c(2))

# DET1 inverter: send 1 uses the DG413's normally open sections (on at logic 1), so MONO1 = not DET1
yi=185.42; s.wire((55.88,yi),(60.96,yi)); lab((55.88,yi),"DET1",180)
rb=R("R612","100k","SX-R-007",64.77,yi); s.wire((60.96,yi),rb(1))
qi=s.place("Transistor_BJT","Q_NPN_BEC","Q601","MMBT3904",rb(2)[0]+7.62,yi,0,fp="Package_TO_SOT_SMD:SOT-23",props=P("SX-Q-001",Manufacturer="onsemi",MPN="MMBT3904LT1G"))
s.wire(rb(2),qi(1)); s.wire(qi(2),dn(qi(2),2.54)); s.power("GNDPWR",dn(qi(2),2.54))   # emitter to PGND (invariant 4, decision 98)
cn=up(qi(3),5.08); s.wire(qi(3),cn); s.wire(cn,rt(cn,10.16)); lab(rt(cn,10.16),"MONO1",0)
rc=R("R613","100k","SX-R-007",cn[0],cn[1]-7.62,0); s.wire(cn,rc(2)); s.wire(rc(1),up(rc(1),2.54)); s.power("+5V",up(rc(1),2.54))

# supplies and decoupling
Y2=375.92; x=33.02
for ref in ("U96013","U96213"):
    q=NE(ref,3,x,Y2); s.wire(q(8),up(q(8),5.08)); s.power("+15V",up(q(8),5.08)); s.wire(q(4),dn(q(4),5.08)); s.power("-15V",dn(q(4),5.08)); x+=15.24
q=DG("U96415",5,x+5.08,Y2-7.62)
s.wire(q(13),up(q(13),5.08)); s.power("+15V",up(q(13),5.08)); s.wire(q(12),up(q(12),2.54),rt(up(q(12),2.54),5.08)); s.power("+5V",rt(up(q(12),2.54),5.08))
s.wire(q(5),dn(q(5),5.08)); gnd(dn(q(5),5.08)); s.wire(q(4),dn(q(4),2.54),rt(dn(q(4),2.54),5.08)); s.power("-15V",rt(dn(q(4),2.54),5.08))
x+=30.48
for cp_,cn_ in (("C602","C603"),("C622","C623"),("C642","C643")):
    cp=C(cp_,"100n","SX-C-002",x,Y2-20.32,0); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(cn_,"100n","SX-C-002",x,Y2+5.08,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'aux_sends.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_aux_sends_wired.json','w'))
json.dump({"no_connect":NC},open(T+'aux_sends_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
