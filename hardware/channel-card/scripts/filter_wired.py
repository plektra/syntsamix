# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Filter sheet, drawn with real wires.

Same parts, references and connections as filter_build.py, which stays the
reference netlist (check_netlist.py filter.json). Per side (L top, R middle):
drive stage on the left, LM13700 Q VCA and its compensation jumper above the
SSI2144, cutoff network below-left of it, ladder capacitors beside their pin
pairs, then the I-V and make-up stages and the DG413 bypass on the right.
The shared cutoff summer, resonance pot, bypass button and supplies sit in
the bottom band.
"""
import json,os
from schlayout import Sheet
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CBIP="Capacitor_THT:C_Radial_D5.0mm_H11.0mm_P2.00mm"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"; SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"
TRIM="Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical"
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
PROV="Provisional: set from the SSI2144 breadboard (simulation/filter/BREADBOARD.md)"
s=Sheet()
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,fp=R0805,**k): return s.place("Device","R",ref,val,x,y,rot,fp=fp,props=P(pn,**k))
def C(ref,val,pn,x,y,rot=90,fp=C0805,**k): return s.place("Device","C",ref,val,x,y,rot,fp=fp,props=P(pn,**k))
def OA(part,ref,unit,x,y,pn,fp=SO8,props=TI): return s.place("Amplifier_Operational",part,ref,part,x,y,0,unit,fp,P(pn,**props))
def gnd(at,rot=0): s.power("GNDA",at,rot)
def pgnd(at,rot=0): s.power("GNDPWR",at,rot)
def up(p,d=2.54): return (p[0],p[1]-d)
def dn(p,d=2.54): return (p[0],p[1]+d)
def lt(p,d=2.54): return (p[0]-d,p[1])
def rt(p,d=2.54): return (p[0]+d,p[1])
NOCONNECT=[]

def side(Pn,o,y0,ssi,ota,pre,iv,post,dg_dry,dg_filt):
    rr=lambda n:f"R{n+o}"; cc=lambda n:f"C{n+o}"
    # ---- input and drive stage
    yi=y0-10.16
    s.wire((25.4,yi),(31.75,yi)); s.label(f"{Pn}_PREFILT",(25.4,yi),180,"hierarchical","input")
    ci=C(cc(101),"10u bipolar","SX-C-003",35.56,yi,fp=CBIP)
    fac=(45.72,yi); s.wire(ci(2),fac)
    s.wire(fac,(fac[0],yi-10.16)); s.label(f"{Pn}_FAC",(fac[0],yi-10.16),90)
    r1=R(rr(101),"10k","SX-R-002",58.42,yi); s.wire(fac,r1(1))
    ps=(76.2,yi); s.wire(r1(2),ps)
    a=OA("NE5532",pre[0],pre[1],91.44,y0-12.7,"SX-IC-004")
    s.wire(ps,a(pre[2][0]))
    s.wire(a(pre[2][1]),lt(a(pre[2][1])),up(lt(a(pre[2][1])))); gnd(up(lt(a(pre[2][1]))),180)
    FX=109.22; s.wire(a(pre[2][2]),(101.6,y0-12.7)); s.wire((101.6,y0-12.7),(FX,y0-12.7))
    r2=R(rr(102),"10k","SX-R-002",88.9,y0-2.54)
    s.wire(ps,(ps[0],y0-2.54)); s.wire((ps[0],y0-2.54),r2(1)); s.wire(r2(2),(101.6,y0-2.54),(101.6,y0-12.7))
    r3=R(rr(103),"16k9","SX-R-017",85.09,y0+12.7)
    s.wire((ps[0],y0-2.54),(ps[0],y0+12.7),r3(1))
    jp=s.place("Connector_Generic","Conn_02x02_Odd_Even",f"JP{101+o}","DRIVE: fit both = MEDIUM",99.06,y0+12.7,0,
               fp="Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical",props=P("SX-CONN-004"))
    s.wire(r3(2),jp(1)); s.wire(jp(2),(FX,y0+12.7))
    s.wire(jp(3),(88.9,y0+15.24)); s.label(f"{Pn}_PGN",(88.9,y0+15.24),180)
    s.wire(jp(4),dn(jp(4),5.08)); gnd(dn(jp(4),5.08))
    # FIN bus: pre-stage output, drive jumper, R104 tap, compensation taps on top
    for y1,y2 in ((y0-20.32,y0-12.7),(y0-12.7,y0-7.62),(y0-7.62,y0+12.7)): s.wire((FX,y1),(FX,y2))
    r4=R(rr(104),"17k4","SX-R-009",124.46,y0-7.62); s.wire((FX,y0-7.62),r4(1))
    sin=(134.62,y0-7.62); s.wire(r4(2),sin)
    r5=R(rr(105),"200","SX-R-010",sin[0],y0-3.81,0); s.wire(sin,r5(1)); gnd(r5(2))
    # ---- SSI2144
    XS=180.34
    u=s.place("syntsamix","SSI2144",ssi,"SSI2144",XS,y0,0,fp="Package_SO:QSOP-16_3.9x4.9mm_P0.635mm",
              props=P("SX-IC-001",Manufacturer="Sound Semiconductor",MPN="SSI2144SS-TU",Supplier="Electrokit",SupplierPN="41019301"))
    s.wire(sin,u(1))
    s.wire(u(16),up(u(16),5.08)); s.power("+15V",up(u(16),5.08))
    s.wire(u(8),dn(u(8),5.08)); s.power("-15V",dn(u(8),5.08))
    s.wire(u(9),dn(u(9),2.54),rt(dn(u(9),2.54),5.08)); gnd(rt(dn(u(9),2.54),5.08))
    for (pa,pb,ref,val,pn) in ((13,12,cc(102),"6n8 C0G","SX-C-006"),(11,10,cc(103),"6n8 C0G","SX-C-006"),
                               (6,7,cc(104),"6n8 C0G","SX-C-006"),(4,5,cc(105),"560p C0G","SX-C-007")):
        c=C(ref,val,pn,XS+17.78,(u(pa)[1]+u(pb)[1])/2,0)
        s.wire(u(pa),c(1)); s.wire(u(pb),c(2))
    # SIG IN- : 200R to ground (upwards) and the Q VCA output
    sn=(162.56,y0-15.24); s.wire(sn,u(2))
    r6=R(rr(106),"200","SX-R-010",sn[0],y0-19.05,0); s.wire(sn,r6(2)); gnd(r6(1),180)
    # cutoff: FREQ pin network
    fq=u(15); n1=(162.56,fq[1]); n2=(152.4,fq[1])
    s.wire(fq,n1); s.wire(n1,n2)
    r8=R(rr(108),"1k +3300ppm","SX-R-021",n1[0],fq[1]+3.81,0,fp="Resistor_SMD:R_0603_1608Metric",Manufacturer="Panasonic",MPN="ERA-V33J102V",Note="Temperature-compensating; place against the SSI2144")
    s.wire(n1,r8(1)); gnd(r8(2))
    r9=R(rr(109),"499k","SX-R-020",n2[0],fq[1]+3.81,0); s.wire(n2,r9(1))
    tv=s.place("Device","R_Potentiometer_Trim",f"RV{101+o}","50k CUTOFF OFFSET",144.78,fq[1]+11.43,0,fp=TRIM,props=P("SX-TRIM-001",Manufacturer="Bourns",MPN="3296W-1-503LF"))
    s.wire(r9(2),(n2[0],tv(2)[1]),tv(2))
    s.wire(tv(1),up(tv(1),2.54)); s.power("+15V",up(tv(1),2.54))
    s.wire(tv(3),dn(tv(3),2.54)); s.power("-15V",dn(tv(3),2.54))
    r10=R(rr(110),"100k","SX-R-007",140.97,fq[1]); s.wire(r10(2),n2); s.wire(r10(1),lt(r10(1),5.08)); s.label("FCV",lt(r10(1),5.08),180)
    # Q pin: 13k to ground (Q is set by the external Q VCA)
    qp=u(14); s.wire(qp,(167.64-5.08,qp[1]))
    r7=R(rr(107),"13k","SX-R-011",162.56,qp[1]+3.81,0); gnd(r7(2))
    # ---- Q VCA (LM13700 half) above-left of the chip
    XO,YO=147.32,y0-38.1
    q=OA("LM13700",ota[0],ota[1],XO,YO,"SX-IC-006",SO16)
    pm,pp,pb,po,pi=ota[2]
    NOCONNECT.append(q(pb))
    s.wire(q(po),(160.02,YO),(160.02,sn[1]),sn)
    s.wire(q(pi),rt(q(pi))); r20=R(rr(120),"41k2","SX-R-015",q(pi)[0]+2.54,q(pi)[1]+7.62,0,Note=PROV)
    s.wire(rt(q(pi)),r20(1)); s.wire(r20(2),dn(r20(2),2.54)); s.label("QW",dn(r20(2),2.54),270)
    qs=(106.68,q(pm)[1]); s.wire(q(pm),(134.62,qs[1])); s.wire((134.62,qs[1]),(121.92,qs[1])); s.wire((121.92,qs[1]),qs)
    r17=R(rr(117),"17k4","SX-R-009",134.62,qs[1]-3.81,0); s.wire(r17(2),(134.62,qs[1])); s.wire(r17(1),up(r17(1),2.54)); s.label(f"{Pn}_IV",up(r17(1),2.54),90)
    r16=R(rr(116),"604","SX-R-012",121.92,qs[1]-3.81,0); s.wire(r16(2),(121.92,qs[1])); gnd(r16(1),180)
    s.wire(q(pp),(134.62,q(pp)[1])); r15=R(rr(115),"604","SX-R-012",134.62,q(pp)[1]+3.81,0); s.wire((134.62,q(pp)[1]),r15(1)); gnd(r15(2))
    jq=s.place("Connector_Generic","Conn_01x03",f"JP{102+o}","Q COMP: 1-2 HALF, 2-3 FULL",101.6,qs[1],180,
               fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",props=P("SX-CONN-005",Note="Open = no bass compensation"))
    # jq pin 2 sits on qs; pin 1 (half) below, pin 3 (full) above
    r18=R(rr(118),"52k3","SX-R-013",114.3,y0-30.48,0,Note="Half compensation (default)")
    s.wire(jq(1),(114.3,jq(1)[1]),r18(1)); s.wire(r18(2),(114.3,y0-20.32),(FX,y0-20.32))
    r19=R(rr(119),"17k4","SX-R-009",jq(3)[0],jq(3)[1]-5.08,0,Note="Full compensation")
    s.wire(jq(3),r19(2)); s.wire(r19(1),up(r19(1),2.54),(93.98,r19(1)[1]-2.54),(93.98,y0-20.32),(FX,y0-20.32))
    # ---- I-V converter (inverting), feedback below
    out=u(3); XI=233.68
    b=OA("NE5532",iv[0],iv[1],XI,out[1]-2.54,"SX-IC-004")
    nf=(220.98,out[1]); s.wire(out,nf); s.wire(nf,b(iv[2][0]))
    s.wire(b(iv[2][1]),lt(b(iv[2][1])),up(lt(b(iv[2][1])))); gnd(up(lt(b(iv[2][1]))),180)
    ivn=(243.84,out[1]-2.54); s.wire(b(iv[2][2]),ivn)
    rf=R(rr(111),"8k66","SX-R-014",XI-1.27,out[1]+10.16,Note=PROV); cf=C(cc(106),"100p C0G","SX-C-008",XI-1.27,out[1]+20.32)
    s.wire(nf,(nf[0],out[1]+10.16)); s.wire((nf[0],out[1]+10.16),(nf[0],out[1]+20.32))
    s.wire((nf[0],out[1]+10.16),rf(1)); s.wire((nf[0],out[1]+20.32),cf(1))
    s.wire(rf(2),(ivn[0],out[1]+10.16)); s.wire(cf(2),(ivn[0],out[1]+20.32))
    s.wire((ivn[0],out[1]+20.32),(ivn[0],out[1]+10.16)); s.wire((ivn[0],out[1]+10.16),ivn)
    s.wire(ivn,(ivn[0],ivn[1]-7.62)); s.label(f"{Pn}_IV",(ivn[0],ivn[1]-7.62),90)
    # ---- coupling and make-up stage (non-inverting)
    c7=C(cc(107),"10u bipolar","SX-C-003",254.0,ivn[1],fp=CBIP); s.wire(ivn,c7(1))
    pa=(264.16,ivn[1]); s.wire(c7(2),pa)
    r12=R(rr(112),"100k","SX-R-007",pa[0],ivn[1]+6.35,0); s.wire(pa,r12(1)); gnd(r12(2))
    m=OA("NE5532",post[0],post[1],281.94,ivn[1]+2.54,"SX-IC-004")
    s.wire(pa,m(post[2][0]))
    fo=(292.1,ivn[1]+2.54); s.wire(m(post[2][2]),fo)
    pf=(271.78,ivn[1]+12.7)
    s.wire(m(post[2][1]),lt(m(post[2][1])),(271.78,pf[1]))
    r13=R(rr(113),"6k04","SX-R-016",281.94,pf[1]); s.wire(pf,r13(1)); s.wire(r13(2),(fo[0],pf[1]),fo)
    r14=R(rr(114),"10k","SX-R-002",pf[0],pf[1]+7.62,0); s.wire(pf,r14(1)); s.wire(r14(2),dn(r14(2),2.54)); s.label(f"{Pn}_PGN",dn(r14(2),2.54),270)
    # ---- bypass: DG413, pressed = dry signal
    XD=320.04; pnode=(332.74,fo[1])
    for (ref,unit,rot,pin_in,pin_s,pin_d,src,ys) in (dg_filt+(f"{Pn}_FILT",fo[1]),dg_dry+(f"{Pn}_FAC",fo[1]-15.24)):
        d=s.place("Analog_Switch","DG413xY",ref,"DG413DY",XD,ys,rot,unit,SO16,P("SX-IC-005",**VI))
        if src.endswith("FILT"): s.wire(fo,d(pin_s))
        else: s.wire(d(pin_s),lt(d(pin_s),7.62)); s.label(src,lt(d(pin_s),7.62),180)
        s.wire(d(pin_d),(pnode[0],ys))
        e=up(d(pin_in),2.54) if rot==180 else dn(d(pin_in),2.54)
        s.wire(d(pin_in),e); s.label("BYP",e,90 if rot==180 else 270)
    s.wire((pnode[0],fo[1]-15.24),pnode)
    rpd=R(rr(121),"100k","SX-R-007",pnode[0],pnode[1]+6.35,0); s.wire(pnode,rpd(1)); gnd(rpd(2))
    s.wire(pnode,(350.52,pnode[1])); s.label(f"{Pn}_POSTFILT",(350.52,pnode[1]),0,"hierarchical","output")

# DG413 units: L dry SW1 (pins 1 IN, 3 S, 2 D), L filtered SW2 (16, 14, 15); R dry SW4 (8, 6, 7), R filtered SW3 (9, 11, 10)
side("L",0,85.09,"U101",("U103",3,(4,3,2,5,1)),("U104",1,(2,3,1)),("U105",1,(2,3,1)),("U106",1,(3,2,1)),
     ("U108",1,180,1,3,2),("U91084",4,180,16,14,15))
side("R",50,205.74,"U102",("U91031",1,(13,14,15,12,16)),("U91042",2,(6,5,7)),("U91052",2,(6,5,7)),("U91062",2,(5,6,7)),
     ("U91082",2,0,8,6,7),("U91083",3,180,9,11,10))

# ------------------------------------------------------------- shared: cutoff summer
Y=300.0
cp=s.place("Device","R_Potentiometer","RV181","50k lin CUTOFF",40.64,Y,0,fp="Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical",
           props=P("SX-POT-003",Note="Panel; clockwise end (pin 3) raises the cutoff"))
s.wire(cp(1),up(cp(1),5.08)); s.power("-15V",up(cp(1),5.08),180)
s.wire(cp(3),dn(cp(3),5.08)); s.power("+15V",dn(cp(3),5.08),180)
r181=R("R181","301k","SX-R-018",55.88,Y); s.wire(cp(2),r181(1))
FS=(71.12,Y); s.wire(r181(2),FS)
jk=s.place("Connector_Audio","AudioJack2_SwitchT","J181","CUTOFF CV 1 V/oct",35.56,Y+20.32,0,props=P("SX-CONN-003",Note="6.3 mm mono switched jack on the top panel; part and footprint to choose"))
r182=R("R182","100k","SX-R-007",55.88,jk("T")[1]); s.wire(jk("T"),r182(1)); s.wire(r182(2),(FS[0],jk("T")[1]))
s.wire(jk("S"),rt(jk("S"),5.08)); gnd(rt(jk("S"),5.08),180)
s.wire(jk("TN"),rt(jk("TN"),5.08),dn(rt(jk("TN"),5.08),2.54)); gnd(dn(rt(jk("TN"),5.08),2.54))
sm=OA("NE5532","U107",1,86.36,Y-2.54,"SX-IC-004")
s.wire(FS,sm(2)); s.wire(sm(3),lt(sm(3)),up(lt(sm(3)))); gnd(up(lt(sm(3))),180)
fcv=(99.06,Y-2.54); s.wire(sm(1),fcv); s.wire(fcv,(106.68,fcv[1])); s.label("FCV",(106.68,fcv[1]),0)
r183=R("R183","162k","SX-R-019",78.74,Y+10.16)
tr=s.place("Device","R_Potentiometer_Trim","RV182","50k V/OCT",91.44,Y+10.16,90,fp=TRIM,props=P("SX-TRIM-001",Manufacturer="Bourns",MPN="3296W-1-503LF"))
s.wire(FS,(FS[0],Y+10.16)); s.wire((FS[0],Y+10.16),(FS[0],Y+20.32))
s.wire((FS[0],Y+10.16),r183(1)); s.wire(r183(2),tr(1))
s.wire(tr(2),up(tr(2),2.54),(fcv[0],tr(2)[1]-2.54)); s.wire(tr(3),(fcv[0],Y+10.16))
c181=C("C181","22p C0G","SX-C-004",85.09,Y+20.32); s.wire((FS[0],Y+20.32),c181(1)); s.wire(c181(2),(fcv[0],Y+20.32))
for y1,y2 in ((fcv[1],tr(2)[1]-2.54),(tr(2)[1]-2.54,Y+10.16),(Y+10.16,Y+20.32)): s.wire((fcv[0],y1),(fcv[0],y2))
sp=OA("NE5532","U91072",2,86.36,Y+38.1,"SX-IC-004")
s.wire(sp(5),lt(sp(5)),up(lt(sp(5)))); gnd(up(lt(sp(5))),180)
s.wire(sp(7),rt(sp(7),2.54),dn(rt(sp(7),2.54),5.08),(sp(6)[0]-2.54,sp(7)[1]+5.08),(sp(6)[0]-2.54,sp(6)[1]),sp(6))
# resonance pot with series resistor and bias diodes
r184=R("R184","10k","SX-R-002",134.62,Y-12.7,0); s.wire(r184(1),up(r184(1),2.54)); s.power("+15V",up(r184(1),2.54))
rp=s.place("Device","R_Potentiometer","RV183","10k rev. audio RESONANCE",134.62,Y,180,fp="Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical",
           props=P("SX-POT-004",Note="Reverse-audio (C) taper per SSI2144 datasheet Figure 3; part to choose"))
s.wire(r184(2),rp(3))
s.wire(rp(2),lt(rp(2),5.08)); s.label("QW",lt(rp(2),5.08),180)
yd=Y+8.89
d1=s.place("Device","D","D181","1N4148W",144.78,yd,180,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
d2=s.place("Device","D","D182","1N4148W",157.48,yd,180,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
s.wire(rp(1),(rp(1)[0],yd),d1(2)); s.wire(d1(1),d2(2)); s.wire(d2(1),rt(d2(1),2.54),dn(rt(d2(1),2.54),2.54)); s.power("-15V",dn(rt(d2(1),2.54),2.54))
# bypass button
b=s.place("Switch","SW_Push_DPDT","SW181","FILTER BYPASS (latching)",185.42,Y,0,props=P("SX-SW-001"))
s.wire(b(2),lt(b(2),5.08)); s.power("+5V",lt(b(2),5.08))
s.wire(b(5),lt(b(5),5.08)); pgnd(lt(b(5),5.08))
nd=(b(1)[0]+10.16,b(1)[1]); s.wire(b(1),nd,rt(nd,10.16)); s.label("BYP",rt(nd,10.16),0)
r186=R("R186","100k","SX-R-007",nd[0],nd[1]-7.62,0); s.wire(nd,r186(2)); gnd(r186(1),180)
ld=s.place("Device","LED","D183","BYPASS LED",b(4)[0]+22.86,b(4)[1],0,fp="LED_THT:LED_D3.0mm",props=P("SX-D-002"))
s.wire(b(4),ld(1))
r185=R("R185","12k","SX-R-008",ld(2)[0]+8.89,b(4)[1],270); s.wire(ld(2),r185(2)); s.wire(r185(1),rt(r185(1),3.81)); s.power("+15V",rt(r185(1),3.81),270)
NOCONNECT+= [b(3),b(6)]
# supplies: op-amp, OTA and switch power units, unused LM13700 buffers
x=165.1; Y2=345.44
for t in ("U91043","U91053","U91063","U91073"):
    u=OA("NE5532",t,3,x,Y2,"SX-IC-004"); s.wire(u(8),up(u(8),5.08)); s.power("+15V",up(u(8),5.08)); s.wire(u(4),dn(u(4),5.08)); s.power("-15V",dn(u(4),5.08)); x+=17.78
u=OA("LM13700","U91035",5,x,Y2,"SX-IC-006",SO16); s.wire(u(11),up(u(11),5.08)); s.power("+15V",up(u(11),5.08)); s.wire(u(6),dn(u(6),5.08)); s.power("-15V",dn(u(6),5.08)); x+=20.32
for t,unit,pin_in,pin_out in (("U91034",4,7,8),("U91032",2,10,9)):
    u=OA("LM13700",t,unit,x,Y2,"SX-IC-006",SO16); s.wire(u(pin_in),lt(u(pin_in),2.54),dn(lt(u(pin_in),2.54),2.54)); gnd(dn(lt(u(pin_in),2.54),2.54)); NOCONNECT.append(u(pin_out)); x+=20.32
u=s.place("Analog_Switch","DG413xY","U91085","DG413DY",x+5.08,Y2,0,5,SO16,P("SX-IC-005",**VI))
s.wire(u(13),up(u(13),5.08)); s.power("+15V",up(u(13),5.08))
s.wire(u(12),up(u(12),2.54),rt(up(u(12),2.54),5.08)); s.power("+5V",rt(up(u(12),2.54),5.08))
s.wire(u(5),dn(u(5),5.08)); gnd(dn(u(5),5.08))
s.wire(u(4),dn(u(4),2.54),rt(dn(u(4),2.54),5.08)); s.power("-15V",rt(dn(u(4),2.54),5.08))
k=191; x=330.2
for i in range(8):
    cpos=C(f"C{k}","100n","SX-C-002",x,Y2-7.62,0); s.power("+15V",cpos(1)); gnd(cpos(2)); k+=1
    cneg=C(f"C{k}","100n","SX-C-002",x,Y2+20.32,0); s.wire(cneg(1),up(cneg(1),2.54)); s.power("-15V",up(cneg(1),2.54),180); gnd(cneg(2)); k+=1
    x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'filter.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_filter_wired.json','w'))
json.dump({"no_connect":NOCONNECT},open(T+'filter_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
