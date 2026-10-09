# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Compressor sheet, drawn with real wires.

Reference netlist: compressor_build.py (check_netlist.py compressor.json).
Top: audio path (inputs, dry inverters, SSI2162 with I-V stages, MIX pot, followers,
bus resistors). Middle: detector (full-wave rectifier, log converter on the AS3046D,
gain stage, peak hold, release mirror). Lower: Amount, on/off ramp, gain computer and
VC summer. Right: gain-reduction LEDs and the ON button. Supplies at the bottom.
"""
SMD={"SX-C-023":dict(Manufacturer="Panasonic",MPN="EEE-1VA100NP",Supplier="Mouser",SupplierPN="667-EEE-1VA100NP"),
     "SX-C-024":dict(Manufacturer="ROQANG",MPN="RVT1V100M0505",Supplier="LCSC",SupplierPN="C72486"),
     "SX-C-025":dict(Manufacturer="ROQANG",MPN="RVT1V470M0605",Supplier="LCSC",SupplierPN="C72522")}   # decision 111 parts, 5.4 mm tall
import json,os
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"
CBIP="Capacitor_SMD:C_Elec_6.3x5.4"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
SO14="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm"; SO16="Package_SO:SOIC-16_3.9x9.9mm_P1.27mm"
TI={"Manufacturer":"Texas Instruments"}; VI={"Manufacturer":"Vishay"}
SWFP="syntsamix:SW_Latching_8.5x8.5mm_CW_GPBS850N"; POT1="Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical"
s=Sheet(); NC=[]
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,fp=R0805,**kw): return s.place("Device","R",ref,val,x,y,rot,fp=fp,props=P(pn,**kw))
def C(ref,val,pn,x,y,rot=90,fp=C0805): return s.place("Device","C",ref,val,x,y,rot,fp=fp,props=P(pn,**SMD.get(pn,{})))
def D(ref,x,y,rot=0): return s.place("Device","D",ref,"1N4148W",x,y,rot,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
def NE(ref,unit,x,y): return s.place("Amplifier_Operational","NE5532",ref,"NE5532",x,y,0,unit,SO8,P("SX-IC-004",**TI))
LOWP={"U409","U94092","U94093","U410","U94102","U94103"}   # TL062 (decision 126): light DC and meter loads
def TL(ref,unit,x,y):
    v="TL062" if ref in LOWP else "TL072"
    return s.place("Amplifier_Operational",v,ref,v,x,y,0,unit,SO8,P("SX-IC-024" if ref in LOWP else "SX-IC-007",**TI,**({"MPN":"TL062CDR","Supplier":"LCSC","SupplierPN":"C67471"} if ref in LOWP else {})))
def DG(ref,unit,x,y): return s.place("Analog_Switch","DG413xY",ref,"DG413DY",x,y,0,unit,SO16,P("SX-IC-005",**VI))
def Q(ref,unit,x,y): return s.place("syntsamix","AS3046",ref,"AS3046D",x,y,0,unit,SO14,P("SX-IC-013",Manufacturer="Alfa",MPN="AS3046D",Supplier="Electric Druid"))
gnd=lambda at,rot=0: s.power("GNDA",at,rot)
up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])
def lab(at,name,rot=0): s.label(name,at,rot)
def gnd_plus(p):          # op-amp + input to AGND: left, up, ground symbol
    s.wire(p,lt(p),up(lt(p))); gnd(up(lt(p)),180)
def follower(a,pm,po,below=7.62,xl=None):   # tie - input to the output through a loop below the op-amp
    o=a(po); m=a(pm); xr=o[0]+5.08; xl=xl or m[0]-2.54
    s.wire(o,(xr,o[1])); s.wire((xr,o[1]),(xr,o[1]+below),(xl,o[1]+below),(xl,m[1]),m)
    return (xr,o[1])

# ======================================================================== audio path
XA,XN=25.4,38.1                       # hierarchical inputs, input node
ROWS={"L":dict(dry=30.48,wet=55.88),"R":dict(dry=132.08,wet=106.68)}
XV,YV=116.84,81.28
v=s.place("syntsamix","SSI2162","U401","SSI2162",XV,YV,0,fp="Package_SO:SSOP-10_3.9x4.9mm_P1.00mm",
          props=P("SX-IC-002",Manufacturer="Sound Semiconductor",MPN="SSI2162SS-TU",Supplier="Electrokit",SupplierPN="41019302"))
s.wire(v("10"),up(v("10"),5.08)); s.power("+15V",up(v("10"),5.08)); s.wire(v("6"),dn(v("6"),5.08)); s.power("-15V",dn(v("6"),5.08))
s.wire(v("5"),dn(v("5"),5.08)); gnd(dn(v("5"),5.08))
vc1,vc2=dn(v("3"),5.08),dn(v("8"),5.08); s.wire(v("3"),vc1); s.wire(v("8"),vc2); s.wire(vc1,vc2); s.wire(vc1,lt(vc1,5.08)); lab(lt(vc1,5.08),"VC",180)
r405=R("R405","14k3","SX-R-030",v("1")[0],v("1")[1]-7.62,0,Note="DNP = Class AB (default); fit for Class A")
s.wire(v("1"),r405(2)); s.wire(r405(1),up(r405(1),2.54)); s.power("+15V",up(r405(1),2.54))
for side,(cin,rin,rrc,crc,riv,civ,rdi,rdf,iv,dinv,iin,iout,xrc,xjog,fb_up) in (
        ("L",("C401","R401","R403","C403","R406","C405","R408","R409",("U403",1,(2,3,1)),("U404",1,(2,3,1)),v("2"),v("4"),81.28,99.06,True)),
        ("R",("C402","R402","R404","C404","R407","C406","R410","R411",("U94032",2,(6,5,7)),("U94042",2,(6,5,7)),v("9"),v("7"),93.98,101.6,False))):
    yw,yd=ROWS[side]["wet"],ROWS[side]["dry"]
    s.label(f"COMP_{side}_SUM",(XA,yw),180,"hierarchical","input"); s.wire((XA,yw),(XN,yw))
    # dry inverter (unity), feedback on the outer side
    s.wire((XN,yw),(XN,yd)); r1=R(rdi,"10k","SX-R-002",50.8,yd); s.wire((XN,yd),r1(1))
    a=NE(dinv[0],dinv[1],76.2,yd-2.54); pm,pp,po=dinv[2]; nd=(60.96,yd); s.wire(r1(2),nd,a(pm)); gnd_plus(a(pp))
    on=(91.44,yd-2.54); s.wire(a(po),on); s.wire(on,(101.6,on[1])); lab((101.6,on[1]),f"DRY_{side}",0)
    yf=yd+7.62 if side=="L" else yd+7.62
    r2=R(rdf,"10k","SX-R-002",76.2,yf); s.wire(nd,(nd[0],yf),r2(1)); s.wire(r2(2),(on[0],yf),on)
    # VCA input: 10u, 10k, 100R + 2n2 towards the VCA, jog into IIN
    c=C(cin,"10u bipolar","SX-C-023",50.8,yw,fp=CBIP); s.wire((XN,yw),c(1))
    r=R(rin,"10k","SX-R-002",66.04,yw); s.wire(c(2),r(1)); node=(xrc,yw); s.wire(r(2),node)
    if side=="L":
        rn=R(rrc,"100","SX-R-001",xrc,yw+11.43,0); cn=C(crc,"2n2 C0G","SX-C-009",xrc,yw+21.59,0)
        s.wire(node,rn(1)); s.wire(rn(2),cn(1)); gnd(cn(2))
    else:
        rn=R(rrc,"100","SX-R-001",xrc,yw-11.43,0); cn=C(crc,"2n2 C0G","SX-C-009",xrc,yw-21.59,0)
        s.wire(node,rn(2)); s.wire(rn(1),cn(2)); gnd(cn(1),180)
    s.wire(node,(xjog,yw),(xjog,iin[1]),iin)
    # I-V converter, feedback away from the VCA
    X1=154.94; b=NE(iv[0],iv[1],X1,yw-2.54); pm,pp,po=iv[2]
    s.wire(iout,(134.62,iout[1]),(134.62,yw),b(pm)); gnd_plus(b(pp))
    nf=(140.97,yw); out=(167.64,yw-2.54); s.wire(b(po),out)
    sg=-1 if fb_up else 1
    yr,yc=yw+sg*10.16,yw+sg*17.78
    f1=R(riv,"10k","SX-R-002",154.94,yr); f2=C(civ,"100p C0G","SX-C-008",154.94,yc)
    s.wire(nf,(nf[0],yr)); s.wire((nf[0],yr),(nf[0],yc)); s.wire((nf[0],yr),f1(1)); s.wire((nf[0],yc),f2(1))
    s.wire(f1(2),(out[0],yr)); s.wire(f2(2),(out[0],yc)); s.wire((out[0],yc),(out[0],yr)); s.wire((out[0],yr),out)
    s.wire(out,(180.34,out[1])); lab((180.34,out[1]),f"WET_{side}",0)
    if side=="L": s.tp("TP404","WET_L",(172.72,out[1]),"up")
# MIX pot (dual linear): CCW = dry, CW = wet
mp=s.place("Device","R_Potentiometer_Dual","RV401","MIX 10k lin dual",213.36,81.28,0,fp="Potentiometer_THT:Potentiometer_Alpha_RD902F-40-00D_Dual_Vertical",
           props=P("SX-POT-007",Manufacturer="Alpha",Note="Panel MIX; CCW = dry, CW = wet (pin 3/6 = clockwise end)"))
s.wire(mp(1),lt(mp(1),5.08)); lab(lt(mp(1),5.08),"DRY_L",180)
s.wire(mp(3),dn(mp(3),7.62)); lab(dn(mp(3),7.62),"WET_L",270)
s.wire(mp(4),dn(mp(4),7.62)); lab(dn(mp(4),7.62),"DRY_R",270)
s.wire(mp(6),rt(mp(6),5.08)); lab(rt(mp(6),5.08),"WET_R",0)
s.wire(mp(2),up(mp(2),7.62)); lab(up(mp(2),7.62),"L_MIXW",90)
s.wire(mp(5),up(mp(5),7.62)); lab(up(mp(5),7.62),"R_MIXW",90)
# followers and bus resistors
for side,(ref,unit,(pp,pm,po)),y,rb in (("L",("U405",1,(3,2,1)),55.88,"R412"),("R",("U94052",2,(5,6,7)),106.68,"R413")):
    a=NE(ref,unit,256.54,y+2.54); s.wire(a(pp),lt(a(pp),5.08)); lab(lt(a(pp),5.08),f"{side}_MIXW",180)
    o=follower(a,pm,po)
    r=R(rb,"22k","SX-R-047",281.94,o[1]); s.wire(o,r(1)); s.wire(r(2),(297.18,o[1])); s.label(f"MAIN_{side}",(297.18,o[1]),0,"hierarchical","bidirectional")

# ======================================================================== detector
YS=213.36
s.label("SC_DET",(XA,YS),180,"hierarchical","input"); s0=(XN,YS); s.wire((XA,YS),s0)
# A1: inverting half-wave, hw = -v for v < 0
r=R("R414","10k","SX-R-002",48.26,YS); s.wire(s0,r(1))
a1=TL("U406",1,73.66,YS-2.54); fwn=(58.42,YS); s.wire(r(2),fwn,a1(2)); gnd_plus(a1(3))
fwo=(86.36,YS-2.54); s.wire(a1(1),fwo)
d2=D("D402",71.12,YS+7.62,180); s.wire(fwn,(fwn[0],YS+7.62),d2(2)); s.wire(d2(1),(fwo[0],YS+7.62),fwo)
d1=D("D401",93.98,fwo[1],180); s.wire(fwo,d1(2)); hw=(101.6,fwo[1]); s.wire(d1(1),hw)
r=R("R415","10k","SX-R-002",80.01,YS+15.24); s.wire((fwn[0],YS+7.62),(fwn[0],YS+15.24),r(1)); s.wire(r(2),(hw[0],YS+15.24),hw)
# log node: |v|/20k (R416 from SC_DET, R417 from hw) + 1.5 uA floor (R418)
YL=hw[1]                                          # log node row
r=R("R417","10k","SX-R-002",109.22,YL); s.wire(hw,r(1))
a2=TL("U94062",2,144.78,YL-2.54)                  # - input (6) on the log node row
lnx=(116.84,YL); s.wire(r(2),lnx,a2(6))
r=R("R418","10M","SX-R-052",lnx[0],YL-10.16,0); s.wire(lnx,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
yb=YS+22.86; r=R("R416","20k","SX-R-051",80.01,yb); s.wire(s0,(s0[0],yb),r(1)); s.wire(r(2),(119.38,yb),(119.38,YL))
gnd_plus(a2(5))
# matched pair above the log amp: Q1 collector = log node, Q2 diode-connected reference
Xq,Yq=152.4,YL-27.94
q=Q("U402",1,Xq,Yq)
lnu=(124.46,YL); s.wire(lnu,(lnu[0],q("1")[1]-5.08),(q("1")[0],q("1")[1]-5.08),q("1"))
s.wire(q("2"),lt(q("2"),5.08)); gnd(lt(q("2"),5.08))
o2=(157.48,a2(7)[1]); s.wire(a2(7),o2)
r419=R("R419","2k2","SX-R-049",o2[0],o2[1]-8.89,0); s.wire(o2,r419(2))
em=(o2[0],q("3")[1]+2.54); s.wire(q("3"),(q("3")[0],em[1]),em,r419(1))
d3=D("D403",em[0]+8.89,em[1],180); s.wire(em,d3(2)); s.wire(d3(1),rt(d3(1),2.54)); gnd(rt(d3(1),2.54))
c=C("C407","220p C0G","SX-C-001",141.0,YL+10.16); s.wire((127.0,YL),(127.0,YL+10.16),c(1)); s.wire(c(2),(o2[0],YL+10.16),o2)
ref=(167.64,q("5")[1]-2.54); s.wire(q("5"),(q("5")[0],ref[1]),ref,(ref[0],q("4")[1]),q("4"))
r=R("R420","560k","SX-R-053",ref[0],ref[1]-8.89,0); s.wire(ref,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
# reference buffer (A3) and gain -11 with the ERA-V33 (A4)
a3=TL("U407",1,190.5,ref[1]+2.54); s.wire(ref,a3(3))
vl=follower(a3,2,1,below=7.62)
r421=R("R421","1k +3300 ppm/K","SX-R-021",210.82,vl[1],fp="Resistor_SMD:R_0603_1608Metric",Manufacturer="Panasonic",MPN="ERA-V33J102V",Note="Place against U402 (AS3046D) for thermal tracking")
s.wire(vl,r421(1))
a4=TL("U94072",2,236.22,vl[1]-2.54); gn=(220.98,vl[1]); s.wire(r421(2),gn,a4(6)); gnd_plus(a4(5))
va=(248.92,a4(7)[1]); s.wire(a4(7),va)
r=R("R422","11k","SX-R-054",234.95,vl[1]+10.16); s.wire(gn,(gn[0],vl[1]+10.16),r(1)); s.wire(r(2),(va[0],vl[1]+10.16),va)
# peak hold: superdiode (A5), 470R + 1u, buffer (A6)
a5=TL("U408",1,269.24,va[1]+2.54); s.wire(va,a5(3))
d4=D("D404",284.48,a5(1)[1],180); s.wire(a5(1),d4(2)); pk=(292.1,a5(1)[1]); s.wire(d4(1),pk)
s.wire(pk,(pk[0],pk[1]+10.16),(259.08,pk[1]+10.16),(259.08,a5(2)[1]),a5(2))
r=R("R423","470","SX-R-055",304.8,pk[1]); s.wire(pk,r(1)); hold=(314.96,pk[1]); s.wire(r(2),hold)
c=C("C408","1u","SX-C-010",hold[0],hold[1]+12.7,0); s.wire(hold,c(1)); gnd(c(2))
a6=TL("U94082",2,342.9,hold[1]+2.54); h2=(320.04,hold[1]); s.wire(hold,h2,a6(5))
vd=follower(a6,6,7,below=7.62)
s.wire(vd,rt(vd,10.16)); lab(rt(vd,10.16),"VD",0); s.tp("TP401","VD",rt(vd,5.08),"up")
# release: Q4 diode-connected sets the current from RELEASE through R424, Q3 sinks it from the hold capacitor
q3=Q("U94022",2,h2[0]+2.54-2.54,hold[1]+38.1)     # collector straight below the hold node
s.wire(h2,(h2[0],q3("8")[1])) if q3("8")[0]==h2[0] else s.wire(h2,(h2[0],q3("8")[1]-2.54),(q3("8")[0],q3("8")[1]-2.54),q3("8"))
s.wire(q3("7"),dn(q3("7"),5.08)); s.power("-15V",dn(q3("7"),5.08))
q4=Q("U94023",3,q3("6")[0]-15.24,q3("6")[1])
mir=(q4("11")[0],q4("11")[1]-2.54)
s.wire(q4("11"),mir); s.wire(mir,(q3("6")[0]-2.54,mir[1]),(q3("6")[0]-2.54,q3("6")[1]),q3("6"))
s.wire(q4("9"),lt(q4("9"),2.54),(q4("9")[0]-2.54,mir[1]-5.08),(mir[0],mir[1]-5.08),mir)
s.wire(q4("10"),dn(q4("10"),5.08)); s.power("-15V",dn(q4("10"),5.08))
r424=R("R424","2M2","SX-R-056",q4("9")[0]-17.78,mir[1]-5.08); s.wire(r424(2),(q4("9")[0]-2.54,mir[1]-5.08))
rv=s.place("Device","R_Potentiometer","RV402","RELEASE 100k rev. log",r424(1)[0]-12.7,r424(1)[1],0,fp=POT1,
           props=P("SX-POT-014",Manufacturer="Alpha",MPN="RD901F-40-15K-C100K",Supplier="Tayda",SupplierPN="A-5370",
                   Note="Panel RELEASE: reverse-log (C) taper, CCW = 44 ms, CW = 1.4 s per 10 dB; 100k keeps it at about 2 mW (Alpha non-B rating 0.02 W, decision 131)"))
s.wire(rv(2),r424(1)); s.wire(rv(1),up(rv(1),5.08)); gnd(up(rv(1),5.08),180)
r=R("R425","6k2","SX-R-091",rv(3)[0],rv(3)[1]+7.62,0); s.wire(rv(3),r(1)); s.wire(r(2),dn(r(2),5.08)); s.power("-15V",dn(r(2),5.08))
q5=Q("U94024",4,q3("8")[0]+20.32,q3("6")[1])
s.wire(q5("12"),lt(q5("12"),2.54),(q5("12")[0]-2.54,q5("13")[1]+2.54),(q5("13")[0],q5("13")[1]+2.54)); s.wire(q5("13"),dn(q5("13"),5.08))
s.power("-15V",dn(q5("13"),5.08)); NC.append(q5("14"))

# ======================================================================== Amount, on/off ramp, gain computer, VC summer
YG=279.4
rva=s.place("Device","R_Potentiometer","RV403","AMOUNT 10k lin",40.64,YG,0,fp=POT1,props=P("SX-POT-006",Note="Panel AMOUNT: CCW = 0 dB, CW = 30 dB (threshold down, makeup up)"))
s.wire(rva(1),up(rva(1),5.08)); gnd(up(rva(1),5.08),180)
r=R("R426","140k","SX-R-058",rva(3)[0],rva(3)[1]+7.62,0); s.wire(rva(3),r(1)); s.wire(r(2),dn(r(2),5.08)); s.power("+15V",dn(r(2),5.08),180)
sw1=DG("U413",1,63.5,YG); s.wire(rva(2),sw1(2)); s.wire(sw1(1),dn(sw1(1),7.62)); lab(dn(sw1(1),7.62),"ON_CTRL",270)
r=R("R427","100k","SX-R-007",81.28,YG); s.wire(sw1(3),r(1)); ar=(91.44,YG); s.wire(r(2),ar)
c=C("C409","220n","SX-C-014",ar[0],YG+10.16,0); s.wire(ar,c(1)); gnd(c(2))
# discharge path when off: ramp node -> R428 -> NC switch -> AGND
r428=R("R428","100k","SX-R-007",106.68,YG+20.32); s.wire((96.52,YG),(96.52,YG+20.32),r428(1))
sw3=DG("U94133",3,124.46,YG+20.32); s.wire(r428(2),sw3(10)); s.wire(sw3(11),rt(sw3(11),2.54)); gnd(rt(sw3(11),2.54))
s.wire(sw3(9),dn(sw3(9),7.62)); lab(dn(sw3(9),7.62),"ON_CTRL",270)
a10=TL("U94102",2,111.76,YG+2.54); s.wire(ar,(96.52,YG),a10(5))
vam=follower(a10,6,7,below=7.62)
vamt=(vam[0]+5.08,vam[1]); s.wire(vam,vamt); s.tp("TP403","VAMT",vamt,"up"); s.wire(vamt,dn(vamt,5.08)); lab(dn(vamt,5.08),"VAMT",270)
# gain computer (A7): VD, VAMT, -15 V threshold and the off-state lift -> GRN = -0.75 x excess (0 below threshold)
XG=170.18; gc=(XG,YG)
r=R("R429","100k","SX-R-007",XG-15.24,YG-10.16); s.wire((XG-30.48,YG-10.16),r(1)); lab((XG-30.48,YG-10.16),"VD",180); s.wire(r(2),(XG,YG-10.16),gc)
r=R("R430","100k","SX-R-007",XG-15.24,YG); s.wire(vamt,(140.97,vamt[1]),(140.97,YG),r(1)); s.wire(r(2),gc)
r=R("R431","2M2","SX-R-056",XG-15.24,YG+10.16); s.wire((XG-25.4,YG+10.16),r(1)); s.power("-15V",(XG-25.4,YG+10.16),90); s.wire(r(2),(XG,YG+10.16))
s.wire(gc,(XG,YG+10.16)); s.wire((XG,YG+10.16),(XG,YG+38.1))
a7=TL("U409",1,XG+20.32,YG-2.54); s.wire(gc,a7(2)); gnd_plus(a7(3))
go=(a7(1)[0]+5.08,a7(1)[1]); s.wire(a7(1),go)
fb=(XG+5.08,YG)                                     # feedback column from the summing node
d6=D("D406",XG+15.24,YG+12.7,0); s.wire(fb,(fb[0],YG+12.7),d6(1)); s.wire(d6(2),(go[0],YG+12.7),go)
d5=D("D405",go[0]+8.89,go[1],0); s.wire(go,d5(1)); grn=(go[0]+17.78,go[1]); s.wire(d5(2),grn)
r=R("R435","75k","SX-R-061",XG+20.32,YG+22.86); s.wire((fb[0],YG+12.7),(fb[0],YG+22.86),r(1)); s.wire(r(2),(grn[0],YG+22.86),grn)
# off-state lift: -15 V -> NC switch -> 3M3 -> KILL (220n) -> 1M -> summing node; reset by the NO switch through 1k when on
YK=YG+38.1
sw4=DG("U94134",4,93.98,YK); s.wire(sw4(15),lt(sw4(15),2.54)); s.power("-15V",lt(sw4(15),2.54),90)
s.wire(sw4(16),dn(sw4(16),7.62)); lab(dn(sw4(16),7.62),"ON_CTRL",270)
r=R("R432","3M3","SX-R-059",114.3,YK); s.wire(sw4(14),r(1)); kl=(127.0,YK); s.wire(r(2),kl)
c=C("C410","220n","SX-C-014",kl[0],YK+10.16,0); s.wire(kl,c(1)); gnd(c(2))
r=R("R433","1M","SX-R-060",152.4,YK); s.wire(kl,r(1)); s.wire(r(2),(XG,YK))
kd=(134.62,YK); r434=R("R434","1k","SX-R-035",124.46,YK+25.4)
s.wire(kd,(kd[0],YK+25.4),r434(2))
sw2=DG("U94132",2,104.14,YK+25.4); s.wire(r434(1),sw2(7)); s.wire(sw2(6),lt(sw2(6),2.54)); gnd(lt(sw2(6),2.54))
s.wire(sw2(8),dn(sw2(8),7.62)); lab(dn(sw2(8),7.62),"ON_CTRL",270)
# VC summer (A8): VC = -(GRN + 0.735 x VAMT), 100k || 2n2; R439 (DNP) halves the makeup
XS=grn[0]+30.48; vs=(XS,YG)
r=R("R436","100k","SX-R-007",grn[0]+15.24,grn[1]); s.wire(grn,r(1)); s.wire(r(2),(XS,grn[1]),vs)
a8=TL("U94092",2,XS+20.32,YG-2.54); s.wire(vs,a8(6)); gnd_plus(a8(5))
vco=(a8(7)[0]+7.62,a8(7)[1]); s.wire(a8(7),vco)
r=R("R440","100k","SX-R-007",XS+20.32,YG-12.7); c=C("C411","2n2 C0G","SX-C-009",XS+20.32,YG-22.86)
s.wire(vs,(XS,YG-12.7)); s.wire((XS,YG-12.7),(XS,YG-22.86)); s.wire((XS,YG-12.7),r(1)); s.wire((XS,YG-22.86),c(1))
s.wire(r(2),(vco[0],YG-12.7)); s.wire(c(2),(vco[0],YG-22.86)); s.wire((vco[0],YG-22.86),(vco[0],YG-12.7)); s.wire((vco[0],YG-12.7),vco)
s.wire(vco,rt(vco,10.16)); lab(rt(vco,10.16),"VC",0); s.tp("TP402","VC",rt(vco,5.08),"down")
ym=YG+30.48
s.wire((XS-40.64,ym),(XS-38.1,ym)); lab((XS-40.64,ym),"VAMT",180)
r=R("R437","68k","SX-R-062",XS-30.48,ym); s.wire((XS-38.1,ym),r(1)); mk=(XS-20.32,ym); s.wire(r(2),mk)
r=R("R439","33k","SX-R-006",mk[0],ym+10.16,0,Note="DNP = full makeup (default); fit for half makeup"); s.wire(mk,r(1)); gnd(r(2))
r=R("R438","68k","SX-R-062",XS-10.16,ym); s.wire(mk,r(1)); s.wire(r(2),(XS,ym),vs)
# GR inverter (A9) for the LEDs: GRP = +GR
s.wire(grn,up(grn,7.62)); lab(up(grn,7.62),"GRN",90)
a9=TL("U410",1,386.08,152.4)
r=R("R441","100k","SX-R-007",a9(2)[0]-15.24,a9(2)[1]); s.wire(r(1),lt(r(1),5.08)); lab(lt(r(1),5.08),"GRN",180)
gi=(r(2)[0]+3.81,a9(2)[1]); s.wire(r(2),gi,a9(2)); gnd_plus(a9(3))
gp=(a9(1)[0]+5.08,a9(1)[1]); s.wire(a9(1),gp)
r=R("R442","100k","SX-R-007",a9(1)[0]-7.62,a9(2)[1]+10.16); s.wire(gi,(gi[0],a9(2)[1]+10.16),r(1)); s.wire(r(2),(gp[0],a9(2)[1]+10.16),gp)
s.wire(gp,rt(gp,7.62)); lab(rt(gp,7.62),"GRP",0)

# ======================================================================== gain-reduction LEDs
XL,YT=416.56,40.64
ladder=[("R443","453k","SX-R-024"),("R444","5k1","SX-R-064"),("R445","4k02","SX-R-038"),("R446","3k","SX-R-063"),("R447","2k","SX-R-003"),("R448","1k","SX-R-035")]
y=YT; s.power("+15V",(XL,y)); taps=[]
for i,(ref,val,pn) in enumerate(ladder):
    r=R(ref,val,pn,XL,y+7.62,0); s.wire((XL,y),r(1)); y=y+15.24; s.wire(r(2),(XL,y))
    if i<5: taps.append((XL,y))
gnd((XL,y))
units=[("U411",1,(5,4,2)),("U94112",2,(7,6,1)),("U94113",3,(11,10,13)),("U94114",4,(9,8,14)),("U412",1,(5,4,2))]
names={1:"GR 1 dB",2:"GR 3 dB",3:"GR 6 dB",4:"GR 10 dB",5:"GR 15 dB"}
XC=452.12; xg=XC-17.78
for k in range(5,0,-1):             # 15 dB on top
    t=taps[5-k]; ref,unit,(pp,pm,po)=units[k-1]
    cmp=s.place("Comparator","LM339",ref,"LM339",XC,t[1]+2.54,0,unit,SO14,P("SX-IC-009",**TI))
    s.wire(t,cmp(pp)); s.wire(cmp(pm),(xg,cmp(pm)[1]))
    led=s.place("Device","LED",f"D{406+k}",names[k],XC+17.78,cmp(po)[1],0,fp="LED_THT:LED_D3.0mm",props=P("SX-D-005",Note="Gain-reduction LED; colour to confirm"))
    s.wire(cmp(po),led(1)); r=R(f"R{448+k}","1k5","SX-R-044",XC+33.02,cmp(po)[1],270); s.wire(led(2),r(2)); s.wire(r(1),rt(r(1),3.81)); s.power("+5V",rt(r(1),3.81),270)
ys=[s.pins[(units[k-1][0],str(units[k-1][2][1]))][1] for k in range(1,6)]
for y1,y2 in zip(sorted(ys),sorted(ys)[1:]): s.wire((xg,y1),(xg,y2))
s.wire((xg,max(ys)),(xg,max(ys)+7.62)); lab((xg,max(ys)+7.62),"GRP",270)
# spare comparators: + to AGND, - to +5 V (output held low, open)
for i,(ref,unit,(pp,pm,po)) in enumerate((("U94122",2,(7,6,1)),("U94123",3,(11,10,13)),("U94124",4,(9,8,14)))):
    cmp=s.place("Comparator","LM339",ref,"LM339",XC,150.0+i*17.78,0,unit,SO14,P("SX-IC-009",**TI))
    s.wire(cmp(pp),lt(cmp(pp),2.54),up(lt(cmp(pp),2.54),5.08)); gnd(up(lt(cmp(pp),2.54),5.08),180)
    s.wire(cmp(pm),lt(cmp(pm),10.16)); s.power("+5V",lt(cmp(pm),10.16),90)
    NC.append(cmp(po))
# ON button: pressed = compressor on
b=s.place("Switch","SW_Push_DPDT","SW401","COMP ON (latching)",439.42,236.22,0,fp=SWFP,
          props=P("SX-SW-001",Manufacturer="CW Industries",MPN="GPBS850N",Supplier="Electrokit",SupplierPN="41012905"))
s.wire(b(2),lt(b(2),5.08)); s.power("+5V",lt(b(2),5.08)); s.wire(b(5),lt(b(5),5.08)); s.power("GNDPWR",lt(b(5),5.08))
nd=(b(3)[0]+10.16,b(3)[1]); s.wire(b(3),nd,rt(nd,10.16)); lab(rt(nd,10.16),"ON_CTRL",0)
r=R("R455","100k","SX-R-007",nd[0],nd[1]-10.16,0); s.wire(nd,r(2))
g=lt(up(r(1),2.54),5.08); s.wire(r(1),up(r(1),2.54),g); s.power("GNDPWR",g)   # PGND (decision 98); symbol points down beside the resistor
ld=s.place("Device","LED","D412","COMP ON LED",b(6)[0]+22.86,b(6)[1],0,fp="LED_SMD:LED_0805_2012Metric",props=P("SX-D-002"))
s.wire(b(6),ld(1)); r=R("R454","12k","SX-R-008",ld(2)[0]+8.89,b(6)[1],270); s.wire(ld(2),r(2)); s.wire(r(1),rt(r(1),3.81)); s.power("+15V",rt(r(1),3.81),270)
NC.extend([b(1),b(4)])

# ======================================================================== supplies and decoupling
Y2=375.92; x=33.02
for ref in ("U94033","U94043","U94053"):
    p=NE(ref,3,x,Y2) ; s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
for ref in ("U94063","U94073","U94083","U94093","U94103"):
    p=TL(ref,3,x,Y2); s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
for ref in ("U94115","U94125"):
    p=s.place("Comparator","LM339",ref,"LM339",x,Y2,0,5,SO14,P("SX-IC-009",**TI))
    s.wire(p(3),up(p(3),5.08)); s.power("+15V",up(p(3),5.08)); s.wire(p(12),dn(p(12),5.08)); s.power("GNDPWR",dn(p(12),5.08)); x+=15.24
p=DG("U94135",5,x+5.08,Y2-7.62)
s.wire(p(13),up(p(13),5.08)); s.power("+15V",up(p(13),5.08)); s.wire(p(12),up(p(12),2.54),rt(up(p(12),2.54),5.08)); s.power("+5V",rt(up(p(12),2.54),5.08))
s.wire(p(5),dn(p(5),5.08)); gnd(dn(p(5),5.08)); s.wire(p(4),dn(p(4),2.54),rt(dn(p(4),2.54),5.08)); s.power("-15V",rt(dn(p(4),2.54),5.08))
x+=25.4
for k in range(9):
    cp=C(f"C{412+2*k}","100n","SX-C-002",x,Y2-20.32,0); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{413+2*k}","100n","SX-C-002",x,Y2+5.08,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7
for c in ("C430","C431"):
    cp=C(c,"100n","SX-C-002",x,Y2-20.32,0); s.power("+15V",cp(1)); s.power("GNDPWR",cp(2)); x+=12.7

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'compressor.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_compressor_wired.json','w'))
json.dump({"no_connect":NC},open(T+'compressor_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
