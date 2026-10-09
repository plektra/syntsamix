# SPDX-FileCopyrightText: 2026 Lari Mahlio
# SPDX-License-Identifier: PolyForm-Noncommercial-1.0.0
"""Master out sheet, drawn with real wires.

Reference netlist: master_out_build.py (check_netlist.py master_out.json).
Top left: SSI2162 with the I-V stages and their soft-clip zeners (MAIN_L/R_OUT).
Right: per side the DRV135 driver (THAT1646 pinout, decision 125) with its common-mode capacitors and rail clamps,
the protection relay (drawn rotated, commons on top) and the output jack.
Bottom: master level law (as the channel fader), relay control, supplies.
"""
SMD={"SX-C-023":dict(Manufacturer="Panasonic",MPN="EEE-1VA100NP",Supplier="Mouser",SupplierPN="667-EEE-1VA100NP"),
     "SX-C-024":dict(Manufacturer="ROQANG",MPN="RVT1V100M0505",Supplier="LCSC",SupplierPN="C72486"),
     "SX-C-025":dict(Manufacturer="ROQANG",MPN="RVT1V470M0605",Supplier="LCSC",SupplierPN="C72522")}   # decision 111 parts, 5.4 mm tall
import json,os
from schlayout import Sheet,pins_of
R0805="Resistor_SMD:R_0805_2012Metric"; C0805="Capacitor_SMD:C_0805_2012Metric"; SO8="Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
SO14="Package_SO:SOIC-14_3.9x8.7mm_P1.27mm"; CBIP="Capacitor_SMD:C_Elec_6.3x5.4"
JK="syntsamix:Jack_6.35mm_Rean_NYS216_Horizontal"
TI={"Manufacturer":"Texas Instruments"}
s=Sheet(); NC=[]
P=lambda pn,**k: {"ProjectPN":pn,**k}
def R(ref,val,pn,x,y,rot=90,**kw): return s.place("Device","R",ref,val,x,y,rot,fp=R0805,props=P(pn,**kw))
def C(ref,val,pn,x,y,rot=90,fp=C0805): return s.place("Device","C",ref,val,x,y,rot,fp=fp,props=P(pn,**SMD.get(pn,{})))
def NE(ref,unit,x,y): return s.place("Amplifier_Operational","NE5532",ref,"NE5532",x,y,0,unit,SO8,P("SX-IC-004",**TI))
def TL(ref,unit,x,y): return s.place("Amplifier_Operational","TL072",ref,"TL072",x,y,0,unit,SO8,P("SX-IC-007",**TI))
def OPA(ref,unit,x,y): return s.place("Amplifier_Operational","Opamp_Dual",ref,"OPA2171",x,y,0,unit,SO8,P("SX-IC-021",**TI,MPN="OPA2171AIDR"))   # no OPA2171 symbol in the KiCad library; same pinout
def DZ(ref,x,y,rot): return s.place("Device","D_Zener",ref,"6V2",x,y,rot,fp="Diode_SMD:D_SOD-123",props=P("SX-D-001"))
def DR(ref,x,y,rot): return s.place("Device","D",ref,"M7 (1N4007)",x,y,rot,fp="Diode_SMD:D_SMA",props=P("SX-D-008",Note="Phantom-power surge clamp (THAT doc 600078 Figure 8)"))
def DS(ref,x,y,rot): return s.place("Device","D",ref,"1N4148W",x,y,rot,fp="Diode_SMD:D_SOD-123",props=P("SX-D-003"))
gnd=lambda at,rot=0: s.power("GNDA",at,rot); pgnd=lambda at,rot=0: s.power("GNDPWR",at,rot)
up=lambda p,d=2.54:(p[0],p[1]-d); dn=lambda p,d=2.54:(p[0],p[1]+d); lt=lambda p,d=2.54:(p[0]-d,p[1]); rt=lambda p,d=2.54:(p[0]+d,p[1])
def lab(at,name,rot=0): s.label(name,at,rot)
def hier(at,name,rot,shape): s.label(name,at,rot,"hierarchical",shape)
def gnd_plus(p): s.wire(p,lt(p),up(lt(p))); gnd(up(lt(p)),180)

# ======================================================================== VCA, I-V, soft clip
XV,YV=101.6,81.28
v=s.place("syntsamix","SSI2162","U701","SSI2162",XV,YV,0,fp="Package_SO:SSOP-10_3.9x4.9mm_P1.00mm",
          props=P("SX-IC-002",Manufacturer="Sound Semiconductor",MPN="SSI2162SS-TU",Supplier="Electrokit",SupplierPN="41019302"))
s.wire(v("10"),up(v("10"),5.08)); s.power("+15V",up(v("10"),5.08)); s.wire(v("6"),dn(v("6"),5.08)); s.power("-15V",dn(v("6"),5.08))
s.wire(v("5"),dn(v("5"),5.08)); gnd(dn(v("5"),5.08))
vc1,vc2=dn(v("3"),5.08),dn(v("8"),5.08); s.wire(v("3"),vc1); s.wire(v("8"),vc2); s.wire(vc1,vc2); s.wire(vc1,lt(vc1,5.08)); lab(lt(vc1,5.08),"VC",180)
r=R("R705","14k3","SX-R-030",v("1")[0],v("1")[1]-7.62,0,Note="DNP = Class AB (default); fit for Class A")
s.wire(v("1"),r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
for side,yw,(cin,rin,rrc,crc,riv,civ,rz,dza,dzb,iv,xrc,xjog,iin,iout,fb_up,tp) in (
        ("L",55.88,("C701","R701","R703","C703","R706","C705","R708","D701","D702",("U702",1,(2,3,1)),68.58,83.82,v("2"),v("4"),True,"TP701")),
        ("R",106.68,("C702","R702","R704","C704","R707","C706","R709","D703","D704",("U97022",2,(6,5,7)),76.2,86.36,v("9"),v("7"),False,"TP702"))):
    s.label(f"MAIN_{side}_SUM",(25.4,yw),180,"hierarchical","input")
    c=C(cin,"10u bipolar","SX-C-023",38.1,yw,fp=CBIP); s.wire((25.4,yw),c(1))
    r=R(rin,"10k","SX-R-002",53.34,yw); s.wire(c(2),r(1)); node=(xrc,yw); s.wire(r(2),node)
    if side=="L":
        rn=R(rrc,"100","SX-R-001",xrc,yw+11.43,0); cn=C(crc,"2n2 C0G","SX-C-009",xrc,yw+21.59,0); s.wire(node,rn(1)); s.wire(rn(2),cn(1)); gnd(cn(2))
    else:
        rn=R(rrc,"100","SX-R-001",xrc,yw-11.43,0); cn=C(crc,"2n2 C0G","SX-C-009",xrc,yw-21.59,0); s.wire(node,rn(2)); s.wire(rn(1),cn(2)); gnd(cn(1),180)
    s.wire(node,(xjog,yw),(xjog,iin[1]),iin)
    a=NE(iv[0],iv[1],139.7,yw-2.54); pm,pp,po=iv[2]
    s.wire(iout,(119.38,iout[1]),(119.38,yw),a(pm)); gnd_plus(a(pp))
    nf=(124.46,yw); out=(162.56,yw-2.54); s.wire(a(po),out)
    sg=-1 if fb_up else 1
    yc,yr,yz=yw+sg*12.7,yw+sg*20.32,yw+sg*27.94
    for y1,y2 in ((yw,yc),(yc,yr),(yr,yz)): s.wire((nf[0],y1),(nf[0],y2))
    for y1,y2 in ((out[1],yc),(yc,yr),(yr,yz)): s.wire((out[0],y1),(out[0],y2))
    cf=C(civ,"100p C0G","SX-C-008",143.51,yc); s.wire((nf[0],yc),cf(1)); s.wire(cf(2),(out[0],yc))
    rf=R(riv,"10k","SX-R-002",143.51,yr); s.wire((nf[0],yr),rf(1)); s.wire(rf(2),(out[0],yr))
    d2=DZ(dzb,130.81,yz,0); s.wire((nf[0],yz),d2(1))
    d1=DZ(dza,143.51,yz,180); s.wire(d2(2),d1(2))
    rr=R(rz,"4k7","SX-R-004",156.21,yz,Note="Soft clip: onset about +14 dBu as on the channels"); s.wire(d1(1),rr(1)); s.wire(rr(2),(out[0],yz))
    s.wire(out,(175.26,out[1])); hier((175.26,out[1]),f"MAIN_{side}_OUT",0,"output"); s.tp(tp,f"MAIN_{side}_OUT",(167.64,out[1]),"up" if side=="L" else "down")

# ======================================================================== drivers, clamps, relays, jacks
def output(side,Yt,u_ref,ccp,ccn,dpp,dpn,dnp,dnn,k_ref,rgh,rgc,j_ref,coil_r,fly):
    Xt=223.52; Xr=Xt+76.2; Xj=Xr-30.48
    lab((Xt-20.32,Yt),f"MAIN_{side}_OUT",180)
    u=s.place("syntsamix","THAT1646",u_ref,"DRV135UA",Xt,Yt,0,fp=SO8,
              props=P("SX-IC-025",Manufacturer="Texas Instruments",MPN="DRV135UA/2K5",Supplier="LCSC",SupplierPN="C544663",Note="DRV135 replaces the end-of-life THAT1646 (decision 125); same SO-8 pinout (TI SBOS094B), symbol kept"))
    s.wire((Xt-20.32,Yt),u("4"))
    s.wire(u("6"),up(u("6"),5.08)); s.power("+15V",up(u("6"),5.08)); s.wire(u("5"),dn(u("5"),5.08)); s.power("-15V",dn(u("5"),5.08))
    s.wire(u("3"),dn(u("3"),5.08)); gnd(dn(u("3"),5.08))
    yop,yon=Yt-15.24,Yt+15.24
    s.wire(u("8"),(Xt+12.7,u("8")[1]),(Xt+12.7,yop))
    s.wire(u("1"),(Xt+12.7,u("1")[1]),(Xt+12.7,yon))
    cp=C(ccp,"10u bipolar","SX-C-023",Xt+20.32,Yt-6.35,0,fp=CBIP); s.wire(u("7"),(Xt+20.32,u("7")[1])); s.wire(cp(1),(Xt+20.32,yop))
    cn=C(ccn,"10u bipolar","SX-C-023",Xt+20.32,Yt+6.35,0,fp=CBIP); s.wire(u("2"),(Xt+20.32,u("2")[1])); s.wire(cn(2),(Xt+20.32,yon))
    k=s.place("Relay","G6K-2",k_ref,"G6K-2F-Y DC12",Xr,Yt-30.48,180,fp="Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y",
              props=P("SX-K-001",Manufacturer="Omron",MPN="G6K-2F-Y DC12",Supplier="LCSC",SupplierPN="C397194",Note="Pole 2 (6/7/5) hot, pole 1 (3/2/4) cold; released = output grounded through 1k"))
    xc=Xt+30.48
    s.wire((Xt+12.7,yop),(xc,yop)); s.wire((xc,yop),(k("5")[0],yop),k("5"))
    s.wire((Xt+12.7,yon),(xc,yon)); s.wire((xc,yon),(k("4")[0],yon),k("4"))
    # rail clamps: hot leg above its row, cold leg below
    for (ref_p,ref_n,row,sgn) in ((dpp,dnp,yop,-1),(dpn,dnn,yon,1)):
        y1,y2=row+sgn*7.62,row+sgn*15.24
        s.wire((xc,row),(xc,y2))
        d=DR(ref_p,xc+7.62,y1,180); s.wire((xc,y1),d(2)); s.wire(d(1),rt(d(1),7.62)); s.power("+15V",rt(d(1),7.62),270)
        d=DR(ref_n,xc+7.62,y2,0); s.wire((xc,y2),d(1)); s.wire(d(2),rt(d(2),7.62)); s.power("-15V",rt(d(2),7.62),270)
    # released-state grounding resistors from the NC contacts
    for pin,ref in (("7",rgh),("2",rgc)):
        r=R(ref,"1k","SX-R-035",k(pin)[0],k(pin)[1]+3.81,0); s.wire(k(pin),r(1)); s.wire(r(2),dn(r(2),1.27)); gnd(dn(r(2),1.27))
    # coil: + (pin 1) through 330R to +15 V, - (pin 8) to RLY_N; flyback diode
    kp=(k("1")[0],k("1")[1]+2.54); s.wire(k("1"),kp)
    d=DS(fly,kp[0]+6.35,kp[1],0); s.wire(kp,d(1)); s.wire(d(2),(kp[0]+12.7,kp[1]))
    xn=kp[0]+12.7; s.wire((xn,kp[1]),(xn,k("8")[1]-2.54),(k("8")[0],k("8")[1]-2.54),k("8"))
    s.wire((xn,k("8")[1]-2.54),(xn+7.62,k("8")[1]-2.54)); lab((xn+7.62,k("8")[1]-2.54),"RLY_N",0)
    r=R(coil_r,"330","SX-R-066",kp[0],kp[1]+7.62,0); s.wire(kp,r(1)); s.wire(r(2),dn(r(2),5.08)); s.power("+15V",dn(r(2),5.08),180)
    # jack: ring to pole 1 COM (3), tip to pole 2 COM (6)
    j=s.place("Connector_Audio","AudioJack3_Switch",j_ref,f"MAIN OUT {side}",Xj,Yt-55.88,0,fp=JK,props=P("SX-CONN-015",Manufacturer="Rean",MPN="NYS216",Note="Balanced main output"))
    s.wire(j("R"),(k("3")[0],j("R")[1]),k("3")); s.wire(j("T"),(k("6")[0],j("T")[1]),k("6"))
    s.wire(j("S"),rt(j("S"),5.08)); gnd(rt(j("S"),5.08),90)
    NC.extend([j("SN"),j("RN"),j("TN")])
output("L",101.6,"U703","C707","C708","D705","D706","D707","D708","K701","R710","R711","J701","R730","D715")
output("R",203.2,"U704","C709","C710","D709","D710","D711","D712","K702","R712","R713","J702","R731","D716")

# ======================================================================== master level law (as the channel fader, decision 72)
Y=279.4; VBX=96.52; SUMX=241.3
fv=s.place("Device","R_Potentiometer","RV701","MASTER 10k lin",45.72,Y,0,fp="Potentiometer_THT:Potentiometer_Alpha_RD901F-40-00D_Single_Vertical",
           props=P("SX-POT-006",Note="Panel MASTER: pin 1 = fully counter-clockwise (off); 0 dB at 75 %, +10 dB at full"))
s.wire(fv(1),up(fv(1),5.08)); s.power("-15V",up(fv(1),5.08),180); s.wire(fv(3),dn(fv(3),5.08)); gnd(dn(fv(3),5.08))
# U705 = OPA2171: input range includes V- (the wiper reaches -15 V), no phase reversal (TI SBOS516H).
# Its inputs have back-to-back diodes, so the superdiodes (open loop when off) stay on the TL072 U706 (decision 102)
bu=OPA("U705",1,68.58,Y+2.54); s.wire(fv(2),bu(3))
bo=(78.74,Y+2.54); s.wire(bu(1),bo,(VBX,Y+2.54)); s.wire(bo,(78.74,Y+10.16),(58.42,Y+10.16),(58.42,bu(2)[1]),bu(2))
ra=R("R714","113k","SX-R-023",170.18,Y-20.32); s.wire((VBX,Y-20.32),ra(1)); s.wire(ra(2),(SUMX,Y-20.32))
rc=R("R715","453k","SX-R-024",170.18,Y-10.16); s.wire((152.4,Y-10.16),rc(1)); s.power("+15V",(152.4,Y-10.16)); s.wire(rc(2),(SUMX,Y-10.16))
def superdiode(y,rp,rq,rqval,rqpn,opa,unit,pins,d,rs,rsval,rspn):
    a=R(rp,"100k","SX-R-007",106.68,y); s.wire((VBX,y),a(1)); nd=(114.3,y); s.wire(a(2),nd)
    q=R(rq,rqval,rqpn,114.3,y-10.16,0); s.wire(nd,q(2)); s.wire(q(1),up(q(1),1.27)); s.power("+15V",up(q(1),1.27))
    o=TL(opa,unit,129.54,y+2.54); s.wire(nd,o(pins[0]))
    dd=DS(d,144.78,y+2.54,0); s.wire(o(pins[2]),dd(1)); k=(152.4,y+2.54); s.wire(dd(2),k)
    s.wire(k,(k[0],y+10.16),(119.38,y+10.16),(119.38,o(pins[1])[1]),o(pins[1]))
    r=R(rs,rsval,rspn,200.66,y+2.54); s.wire(k,r(1)); s.wire(r(2),(SUMX,y+2.54))
superdiode(Y+17.78,"R716","R717","221k","SX-R-025","U97062",2,(5,6,7),"D713","R718","63k4","SX-R-026")
superdiode(Y+50.8,"R719","R720","124k","SX-R-027","U706",1,(3,2,1),"D714","R721","8k66","SX-R-014")
for y1,y2 in ((Y-20.32,Y+2.54),(Y+2.54,Y+17.78),(Y+17.78,Y+50.8)): s.wire((VBX,y1),(VBX,y2))
taps=sorted({Y-38.1,Y-30.48,Y-20.32,Y-10.16,Y+5.08,Y+20.32,Y+53.34})
for y1,y2 in zip(taps,taps[1:]): s.wire((SUMX,y1),(SUMX,y2))
su=OPA("U97052",2,256.54,Y+2.54); s.wire((SUMX,Y+5.08),su(6)); gnd_plus(su(5))
so=(266.7,Y+2.54); s.wire(su(7),so,(279.4,so[1])); lab((279.4,so[1]),"VC",0); s.tp("TP703","VC",(274.32,so[1]),"down")
f1=R("R722","10k","SX-R-002",254.0,Y-30.48); f2=C("C711","1u","SX-C-010",254.0,Y-38.1)
s.wire((SUMX,Y-30.48),f1(1)); s.wire((SUMX,Y-38.1),f2(1)); s.wire(f1(2),(so[0],Y-30.48)); s.wire(f2(2),(so[0],Y-38.1))
s.wire((so[0],Y-38.1),(so[0],Y-30.48)); s.wire((so[0],Y-30.48),so)

# ======================================================================== relay control
XC,YC=355.6,256.54
# A: raw +20 V / 2 against REF (8.9 V = raw 17.9 V); output low pulls TIMER down at once
ca=s.place("Comparator","LM339","U707","LM339",XC,YC-7.62,0,1,SO14,P("SX-IC-009",**TI))
hier((XC-58.42,ca(5)[1]),"+20V_RAW",180,"input")
r=R("R723","10k","SX-R-002",XC-45.72,ca(5)[1]); s.wire((XC-58.42,ca(5)[1]),r(1)); rd=(XC-33.02,ca(5)[1]); s.wire(r(2),rd,ca(5))
r=R("R724","10k","SX-R-002",rd[0],rd[1]+7.62,0); s.wire(rd,r(1)); s.wire(r(2),dn(r(2),2.54)); pgnd(dn(r(2),2.54))
ref=(XC-12.7,YC+20.32); s.wire(ca(4),(ref[0],ca(4)[1]),ref)
rr=(XC-20.32,ref[1]); s.wire(ref,rr)
r=R("R725","6k8","SX-R-067",rr[0],rr[1]-7.62,0); s.wire(rr,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
r=R("R726","10k","SX-R-002",rr[0],rr[1]+7.62,0); s.wire(rr,r(1)); s.wire(r(2),dn(r(2),2.54)); pgnd(dn(r(2),2.54))
# B: TIMER (1M from +15 V, 2u2) against REF: about 2 s after power-up its output releases RLY_B
cb=s.place("Comparator","LM339","U97072","LM339",XC+38.1,YC+20.32,0,2,SO14,P("SX-IC-009",**TI))
s.wire(ref,(XC-2.54,ref[1]),(XC-2.54,cb(6)[1]),cb(6))
tm=(XC+20.32,cb(7)[1])
r=R("R727","1k","SX-R-035",XC+12.7,ca(2)[1]); s.wire(ca(2),r(1)); s.wire(r(2),(tm[0],ca(2)[1]),tm); s.wire(tm,cb(7))
yb=YC+5.08; s.wire((tm[0],yb),(tm[0]-7.62,yb))
c=C("C712","2u2","SX-C-015",tm[0]-7.62,yb+5.08,0); s.wire((tm[0]-7.62,yb),c(1)); pgnd(c(2))
yr=YC+12.7; s.wire((tm[0],yr),(tm[0]+10.16,yr))
r=R("R728","1M","SX-R-060",tm[0]+10.16,yr-7.62,0); s.wire((tm[0]+10.16,yr),r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
s.tp("TP704","TIMER",(tm[0],YC-2.54),"right")
rb=(cb(1)[0]+7.62,cb(1)[1]); s.wire(cb(1),rb)
r=R("R729","4k7","SX-R-004",rb[0],rb[1]-10.16,0); s.wire(rb,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
q=s.place("Transistor_BJT","Q_NPN_BEC","Q701","MMBT3904",rb[0]+10.16,rb[1],0,fp="Package_TO_SOT_SMD:SOT-23",props=P("SX-Q-001",Manufacturer="onsemi",MPN="MMBT3904LT1G"))
s.wire(rb,q(1)); s.wire(q(2),dn(q(2),2.54)); pgnd(dn(q(2),2.54))
qc=up(q(3),5.08); s.wire(q(3),qc,rt(qc,10.16)); lab(rt(qc,10.16),"RLY_N",0)
s.wire(qc,up(qc,7.62)); hier(up(qc,7.62),"RLY_N",90,"output")
# spare comparator D: + to PGND, - to +5 V
# C: raw -20 V watch (decision 128): NEG_DIV = 0.816 x 15 V + 0.184 x raw -20 V, above REF when raw is weaker than -17.9 V
cc=s.place("Comparator","LM339","U97073","LM339",XC+76.2,YC+50.8,0,3,SO14,P("SX-IC-009",**TI))
s.wire(cc(11),lt(cc(11),5.08)); lab(lt(cc(11),5.08),"REF",180)
nd=lt(cc(10),17.78); s.wire(cc(10),nd)
r=R("R732","22k6","SX-R-071",nd[0],nd[1]-7.62,0); s.wire(nd,r(2)); s.wire(r(1),up(r(1),2.54)); s.power("+15V",up(r(1),2.54))
r=R("R733","100k","SX-R-007",nd[0],nd[1]+7.62,0); s.wire(nd,r(1)); s.wire(r(2),dn(r(2),7.62)); hier(dn(r(2),7.62),"-20V_RAW",90,"input")
s.wire(cc(13),rt(cc(13),5.08)); lab(rt(cc(13),5.08),"UV_O",0)
s.wire(ref,dn(ref,15.24)); lab(dn(ref,15.24),"REF",0)
s.wire(ca(2),dn(ca(2),5.08)); lab(dn(ca(2),5.08),"UV_O",0)
for i,(ref_,unit,(pp,pm,po)) in enumerate((("U97074",4,(9,8,14)),),1):
    cs=s.place("Comparator","LM339",ref_,"LM339",XC+76.2,YC+50.8+i*17.78,0,unit,SO14,P("SX-IC-009",**TI))
    s.wire(cs(pp),lt(cs(pp),2.54),up(lt(cs(pp),2.54),5.08)); pgnd(up(lt(cs(pp),2.54),5.08),180)
    s.wire(cs(pm),lt(cs(pm),10.16)); s.power("+5V",lt(cs(pm),10.16),90)
    NC.append(cs(po))

# ======================================================================== supplies and decoupling
Y2=375.92; x=33.02
for ref in ("U97023",):
    p=NE(ref,3,x,Y2); s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
for ref,f in (("U97053",OPA),("U97063",TL)):
    p=f(ref,3,x,Y2); s.wire(p(8),up(p(8),5.08)); s.power("+15V",up(p(8),5.08)); s.wire(p(4),dn(p(4),5.08)); s.power("-15V",dn(p(4),5.08)); x+=15.24
p=s.place("Comparator","LM339","U97075","LM339",x,Y2,0,5,SO14,P("SX-IC-009",**TI))
s.wire(p(3),up(p(3),5.08)); s.power("+15V",up(p(3),5.08)); s.wire(p(12),dn(p(12),5.08)); pgnd(dn(p(12),5.08)); x+=20.32
for k_ in range(6):
    cp=C(f"C{713+2*k_}","100n","SX-C-002",x,Y2-20.32,0); s.power("+15V",cp(1)); gnd(cp(2))
    cn=C(f"C{714+2*k_}","100n","SX-C-002",x,Y2+5.08,0); s.wire(cn(1),up(cn(1),2.54)); s.power("-15V",up(cn(1),2.54),180); gnd(cn(2))
    x+=12.7
cp=C("C725","100n","SX-C-002",x,Y2-20.32,0); s.power("+15V",cp(1)); pgnd(cp(2))

HERE=os.path.dirname(os.path.abspath(__file__)); CARD=os.path.dirname(HERE)+'/'
T=os.path.join(HERE,'build')+'/'; os.makedirs(T,exist_ok=True)
json.dump([["kicad_set_project",{"project_dir":CARD.rstrip('/'),"sch_file":CARD+'master_out.kicad_sch'}],["sch_build_circuit",s.build_args()]],open(T+'calls_master_out_wired.json','w'))
json.dump({"no_connect":NC},open(T+'master_out_wired_extra.json','w'))
print(len(s.symbols),"symbols",len(s.wires),"wires",len(s.labels),"labels",len(s.powers),"power symbols")
